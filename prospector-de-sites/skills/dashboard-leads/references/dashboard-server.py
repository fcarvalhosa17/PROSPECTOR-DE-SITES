#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prospector — servidor local do dashboard (SQLite). Sem dependências: só Python padrão.
Uso: python dashboard-server.py  (ou duplo clique em iniciar-dashboard.bat)
Abre em http://localhost:8765 — edições, exclusões e drag&drop salvam no prospector.db"""
import json, sqlite3, os, sys, webbrowser, subprocess, shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PASTA = os.path.dirname(os.path.abspath(__file__))
os.chdir(PASTA)
DB = os.path.join(PASTA, 'prospector.db')
CONFIG = os.path.join(PASTA, 'prospector-config.json')

def ler_config():
    try: return json.load(open(CONFIG, encoding='utf-8'))
    except Exception: return {}

def achar_bin(nome):
    """Caminho absoluto do executável (claude/vercel/npm...). O PATH do .bat aberto por
    duplo-clique às vezes não inclui ~/.local/bin nem o bin global do npm — por isso o fallback."""
    p = shutil.which(nome)
    if p: return p
    home = os.path.expanduser('~')
    cands = [os.path.join(home, '.local', 'bin', nome + ext) for ext in ('.exe', '.cmd', '')]
    cands += [os.path.join(os.environ.get('APPDATA', ''), 'npm', nome + ext) for ext in ('.cmd', '.exe', '')]
    for c in cands:
        if c and os.path.isfile(c): return c
    return None

def achar_ttyd():
    """ttyd é um .exe único (terminal na web). Procura no PATH, em ~/.local/bin e NA PRÓPRIA PASTA
    (o jeito mais fácil: o usuário baixa ttyd.win10.exe do GitHub e joga na pasta conectada)."""
    for nome in ('ttyd', 'ttyd.win10', 'ttyd.win32'):
        p = achar_bin(nome)
        if p: return p
    for nome in ('ttyd.exe', 'ttyd.win10.exe', 'ttyd.win32.exe', 'ttyd'):
        c = os.path.join(PASTA, nome)
        if os.path.isfile(c): return c
    return None

NODE_BIN = achar_bin('node')

def ambiente():
    """Copia do ambiente com o diretório do node no PATH — o vercel.cmd chama `node`, e o
    .bat aberto por duplo-clique às vezes não tem o node no PATH (erro 'node não reconhecido')."""
    env = dict(os.environ)
    if NODE_BIN:
        d = os.path.dirname(NODE_BIN)
        if d and d.lower() not in (env.get('PATH', '') or '').lower():
            env['PATH'] = d + os.pathsep + env.get('PATH', '')
    return env

CLAUDE_BIN = achar_bin('claude')
VERCEL_BIN = achar_bin('vercel')
TTYD_BIN = achar_ttyd()
TTYD_PORTA = 7681
_ttyd_proc = [None]
PORTA = 8765

def ligar_ttyd():
    """Sobe o ttyd servindo um cmd na pasta conectada (só localhost). Idempotente."""
    if not TTYD_BIN: return False
    if _ttyd_proc[0] and _ttyd_proc[0].poll() is None: return True
    # abre um cmd que já entra no claude; se o claude fechar, o cmd continua (git, vercel, etc.)
    alvo = ['cmd', '/k', 'echo Abrindo o Claude (pode levar alguns segundos)... & "%s"' % CLAUDE_BIN] if CLAUDE_BIN else ['cmd']
    try:
        _ttyd_proc[0] = subprocess.Popen(
            [TTYD_BIN, '-p', str(TTYD_PORTA), '-i', '127.0.0.1', '-W', '-t', 'titleFixed=Prospector'] + alvo,
            cwd=PASTA, stdin=subprocess.DEVNULL, env=ambiente(),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False
CAMPOS = ['slug','nome','nicho','cidade','nota','avaliacoes','email','telefone','whatsapp',
          'siteAntigo','motivo','status','urlNova','dataProposta','valor','obs',
          'contratoStatus','contratoEm','manutencao','pago','docCliente','endCliente']

def conexao():
    c = sqlite3.connect(DB)
    c.execute('''CREATE TABLE IF NOT EXISTS leads(
        slug TEXT PRIMARY KEY, nome TEXT, nicho TEXT, cidade TEXT, nota REAL, avaliacoes INTEGER,
        email TEXT, telefone TEXT, whatsapp TEXT, siteAntigo TEXT, motivo TEXT,
        status TEXT DEFAULT 'novo', urlNova TEXT, dataProposta TEXT, valor REAL, obs TEXT,
        contratoStatus TEXT DEFAULT 'pendente', contratoEm TEXT, manutencao REAL, pago INTEGER DEFAULT 0,
        atualizado TEXT DEFAULT (datetime('now','localtime')))''')
    for col, tipo in [('contratoStatus',"TEXT DEFAULT 'pendente'"),('contratoEm','TEXT'),('manutencao','REAL'),('pago','INTEGER DEFAULT 0'),('docCliente','TEXT'),('endCliente','TEXT')]:
        try: c.execute('ALTER TABLE leads ADD COLUMN %s %s' % (col, tipo))
        except sqlite3.OperationalError: pass
    c.execute('''CREATE TABLE IF NOT EXISTS acoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, nicho TEXT, cidade TEXT,
        fase INTEGER DEFAULT 1, criado TEXT DEFAULT (datetime('now','localtime')))''')
    c.execute('''CREATE TABLE IF NOT EXISTS conversas(
        id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT, autor TEXT, texto TEXT,
        criado TEXT DEFAULT (datetime('now','localtime')))''')
    return c

def importar_snapshot():
    """Primeira execução sem banco: importa os leads embutidos no dashboard.html."""
    try:
        html = open(os.path.join(PASTA, 'dashboard.html'), encoding='utf-8').read()
        ini = html.index('<script id="dados" type="application/json">') + len('<script id="dados" type="application/json">')
        fim = html.index('</script>', ini)
        dados = json.loads(html[ini:fim])
        c = conexao()
        for l in dados.get('leads', []):
            c.execute('INSERT OR IGNORE INTO leads (%s) VALUES (%s)' % (','.join(CAMPOS), ','.join('?'*len(CAMPOS))),
                      [l.get(k) for k in CAMPOS])
        c.commit(); c.close()
        print('Snapshot importado do dashboard.html para o prospector.db')
    except Exception as e:
        print('(sem snapshot para importar: %s)' % e)

class App(SimpleHTTPRequestHandler):
    def _json(self, code, obj):
        corpo = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers(); self.wfile.write(corpo)
    def _corpo(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n).decode('utf-8')) if n else {}
    def do_GET(self):
        if self.path.split('?')[0] == '/api/config':
            cfg = ler_config()
            hg = dict(cfg.get('hostgator', {}))
            hg['senhaDefinida'] = bool(hg.get('senha'))
            hg.pop('senha', None)  # a senha NUNCA sai do arquivo
            vc = dict(cfg.get('vercel', {}))
            vc['tokenDefinido'] = bool(vc.get('token'))
            vc.pop('token', None)  # o token NUNCA sai do arquivo
            return self._json(200, {'contratante': cfg.get('contratante', {}), 'hostgator': hg, 'vercel': vc})
        if self.path.split('?')[0] == '/api/acoes':
            c = conexao(); c.row_factory = sqlite3.Row
            rows = [dict(r) for r in c.execute('SELECT * FROM acoes ORDER BY id DESC').fetchall()]; c.close()
            return self._json(200, rows)
        if self.path.split('?')[0] == '/api/terminal':
            if not TTYD_BIN:
                return self._json(200, {'ok': False, 'instalado': False, 'porta': TTYD_PORTA})
            ligar_ttyd()
            vivo = bool(_ttyd_proc[0] and _ttyd_proc[0].poll() is None)
            return self._json(200, {'ok': vivo, 'instalado': True, 'porta': TTYD_PORTA})
        if self.path.split('?')[0] == '/api/conversas':
            import urllib.parse
            qs = urllib.parse.parse_qs(self.path.split('?')[1] if '?' in self.path else '')
            slug = (qs.get('slug', ['']) or [''])[0]
            c = conexao(); c.row_factory = sqlite3.Row
            rows = [dict(r) for r in c.execute('SELECT autor,texto,criado FROM conversas WHERE slug=? ORDER BY id', (slug,)).fetchall()]
            c.close(); return self._json(200, rows)
        if self.path.split('?')[0] == '/api/leads':
            c = conexao(); c.row_factory = sqlite3.Row
            rows = [dict(r) for r in c.execute('SELECT * FROM leads').fetchall()]; c.close()
            return self._json(200, rows)
        if self.path in ('/', ''):
            self.path = '/dashboard.html'
        return SimpleHTTPRequestHandler.do_GET(self)
    def _deploy_vercel(self, slug):
        """Deploy MANUAL de um site no Vercel — só roda quando o usuário clica no botão."""
        if not slug.replace('-', '').replace('_', '').isalnum():
            return self._json(400, {'erro': 'slug inválido'})
        pasta = os.path.join(PASTA, 'sites', slug)
        pagina = os.path.join(pasta, slug + '.html')
        if not os.path.isfile(pagina):
            return self._json(404, {'erro': 'não achei sites/%s/%s.html' % (slug, slug)})
        if not VERCEL_BIN:
            return self._json(500, {'erro': 'Vercel CLI não instalado. No terminal: npm i -g vercel (o token você salva na aba Configurações)'})
        vc = ler_config().get('vercel', {})
        cmd = [VERCEL_BIN, 'deploy', '--prod', '--yes']
        if vc.get('token'): cmd += ['--token', vc['token']]
        if vc.get('escopo'): cmd += ['--scope', vc['escopo']]
        shutil.copyfile(pagina, os.path.join(pasta, 'index.html'))
        with open(os.path.join(pasta, '.vercelignore'), 'w') as f:
            f.write('*-editor.html\noriginal.png\ncliente.json\n%s.html\n' % slug)
        try:
            r = subprocess.run(cmd, shell=False, cwd=pasta, env=ambiente(),
                               capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            return self._json(500, {'erro': 'deploy passou de 5 minutos — tente pelo terminal: vercel deploy --prod'})
        if r.returncode != 0:
            return self._json(500, {'erro': ((r.stderr or r.stdout) or 'falha desconhecida').strip()[-400:]})
        url = ''
        for linha in reversed((r.stdout or '').strip().splitlines()):
            if 'http' in linha:
                url = linha.strip().split()[-1]; break
        c = conexao()
        c.execute('''UPDATE leads SET urlNova=?, status=CASE WHEN status IN ('novo','redesenhado') THEN 'publicado' ELSE status END,
                     atualizado=datetime('now','localtime') WHERE slug=?''', (url, slug))
        c.commit(); c.close()
        return self._json(200, {'ok': True, 'url': url})

    def _rodar_claude(self, comando):
        """Abre um terminal com o Claude Code já executando o comando na pasta conectada.
        O Claude pergunta no terminal o que faltar — o dashboard só dispara."""
        if not comando.startswith('/'):
            return self._json(400, {'erro': 'comando deve começar com /'})
        if not CLAUDE_BIN:
            return self._json(500, {'erro': 'Claude Code não encontrado. Instale/verifique: claude no terminal (ou ~/.local/bin/claude)'})
        try:
            if os.name == 'nt':
                # /k mantém a janela; caminho absoluto do claude entre aspas para vencer PATH e espaços
                subprocess.Popen('start "Prospector — %s" cmd /k ""%s" "%s""' % (comando.split()[0], CLAUDE_BIN, comando.replace('"', '')),
                                 shell=True, cwd=PASTA, env=ambiente())
            else:
                subprocess.Popen(['x-terminal-emulator', '-e', CLAUDE_BIN, comando], cwd=PASTA, env=ambiente())
        except Exception as e:
            return self._json(500, {'erro': str(e)})
        return self._json(200, {'ok': True, 'msg': 'Terminal aberto com o Claude rodando %s — responda lá o que ele perguntar.' % comando.split()[0]})

    def _salvar_msg(self, slug, autor, texto):
        c = conexao(); c.execute('INSERT INTO conversas (slug,autor,texto) VALUES (?,?,?)', (slug, autor, texto)); c.commit(); c.close()

    def _chat_claude(self, msg, slug='', rotulo=''):
        """Chat embutido: repassa a mensagem ao Claude Code CLI na pasta conectada.
        -c continua a conversa anterior; acceptEdits deixa ele editar os sites (servidor é só localhost).
        slug agrupa o histórico por cliente (persiste no banco); rotulo é o texto humano exibido."""
        if not msg:
            return self._json(400, {'erro': 'mensagem vazia'})
        if not CLAUDE_BIN:
            return self._json(500, {'erro': 'Claude Code não encontrado. Instale/verifique: claude no terminal (ou ~/.local/bin/claude)'})
        # allowedTools = só ferramentas de arquivo local. Em -p, ferramenta fora da lista é NEGADA
        # na hora (não abre prompt), então o processo nunca trava esperando aprovação de rede/bash.
        ferramentas = 'Read,Edit,Write,MultiEdit,Glob,Grep,LS'
        base = [CLAUDE_BIN, '-p', '--permission-mode', 'acceptEdits',
                '--allowedTools', ferramentas, '--output-format', 'json']
        try:
            r = subprocess.run(base + ['-c', msg], shell=False, cwd=PASTA, stdin=subprocess.DEVNULL,
                               capture_output=True, text=True, timeout=300, encoding='utf-8', errors='replace')
            if r.returncode != 0:  # primeira mensagem: ainda não existe conversa para continuar
                r = subprocess.run(base + [msg], shell=False, cwd=PASTA, stdin=subprocess.DEVNULL,
                                   capture_output=True, text=True, timeout=300, encoding='utf-8', errors='replace')
        except subprocess.TimeoutExpired:
            return self._json(500, {'erro': 'o Claude passou de 5 min — provável tarefa que precisa de rede/terminal. Use a aba Ações (terminal) para esse tipo de pedido.'})
        if r.returncode != 0:
            erro = ((r.stderr or r.stdout) or 'falha').strip()[-400:]
            self._salvar_msg(slug, 'eu', rotulo or msg); self._salvar_msg(slug, 'claude', 'Falhou: ' + erro)
            return self._json(500, {'erro': erro})
        try:
            resposta = json.loads(r.stdout).get('result', r.stdout)
        except Exception:
            resposta = r.stdout.strip()
        self._salvar_msg(slug, 'eu', rotulo or msg)
        self._salvar_msg(slug, 'claude', resposta)
        return self._json(200, {'ok': True, 'resposta': resposta})

    def do_POST(self):
        partes = self.path.split('?')[0].split('/')
        if len(partes) == 4 and partes[1] == 'api' and partes[2] == 'vercel':
            return self._deploy_vercel(partes[3])
        if self.path.split('?')[0] == '/api/chat':
            corpo = self._corpo()
            return self._chat_claude((corpo.get('msg') or '').strip(), (corpo.get('slug') or '').strip(), corpo.get('rotulo') or '')
        if self.path.split('?')[0] == '/api/conversas':
            corpo = self._corpo()
            texto = (corpo.get('texto') or '').strip()
            if not texto:
                return self._json(400, {'erro': 'texto vazio'})
            self._salvar_msg((corpo.get('slug') or '').strip(), corpo.get('autor') or 'eu', texto)
            return self._json(200, {'ok': True})
        if self.path.split('?')[0] == '/api/acoes':
            a = self._corpo()
            if not (a.get('nome') or '').strip():
                return self._json(400, {'erro': 'nome obrigatório'})
            c = conexao()
            c.execute('INSERT INTO acoes (nome,nicho,cidade) VALUES (?,?,?)',
                      (a['nome'].strip(), (a.get('nicho') or '').strip(), (a.get('cidade') or '').strip()))
            c.commit(); c.close(); return self._json(200, {'ok': True})
        if self.path.split('?')[0] == '/api/claude':
            return self._rodar_claude((self._corpo().get('comando') or '').strip())
        if self.path.split('?')[0] == '/api/leads':
            l = self._corpo(); c = conexao()
            c.execute('INSERT OR REPLACE INTO leads (%s) VALUES (%s)' % (','.join(CAMPOS), ','.join('?'*len(CAMPOS))),
                      [l.get(k) for k in CAMPOS])
            c.commit(); c.close(); return self._json(200, {'ok': True})
        return self._json(404, {'erro': 'rota'})
    def do_PUT(self):
        if self.path.split('?')[0] == '/api/config':
            cfg = ler_config(); corpo = self._corpo()
            if 'vercel' in corpo:
                vc = cfg.get('vercel', {})
                for k, v in corpo['vercel'].items():
                    if not isinstance(v, str): continue
                    if k == 'token' and v == '': continue  # em branco = mantém o atual
                    vc[k] = v
                cfg['vercel'] = vc
                json.dump(cfg, open(CONFIG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
                return self._json(200, {'ok': True})
            if 'contratante' in corpo or 'hostgator' in corpo:
                if 'contratante' in corpo:
                    ct = cfg.get('contratante', {})
                    ct.update({k: v for k, v in corpo['contratante'].items() if isinstance(v, str)})
                    cfg['contratante'] = ct
                if 'hostgator' in corpo:
                    hg = cfg.get('hostgator', {})
                    for k, v in corpo['hostgator'].items():
                        if not isinstance(v, str): continue
                        if k == 'senha' and v == '': continue  # em branco = mantém a atual
                        hg[k] = v
                    cfg['hostgator'] = hg
            else:  # compatibilidade: corpo plano = contratante
                ct = cfg.get('contratante', {})
                ct.update({k: v for k, v in corpo.items() if isinstance(v, str)})
                cfg['contratante'] = ct
            json.dump(cfg, open(CONFIG, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            return self._json(200, {'ok': True})
        partes = self.path.split('?')[0].split('/')
        if len(partes) == 4 and partes[1] == 'api' and partes[2] == 'acoes':
            ch = self._corpo()
            if 'fase' in ch:
                c = conexao()
                c.execute('UPDATE acoes SET fase=? WHERE id=?', (int(ch['fase']), int(partes[3])))
                c.commit(); c.close()
            return self._json(200, {'ok': True})
        if len(partes) == 4 and partes[1] == 'api' and partes[2] == 'leads':
            slug, ch = partes[3], self._corpo()
            sets = [k for k in ch if k in CAMPOS and k != 'slug']
            if sets:
                c = conexao()
                c.execute('UPDATE leads SET %s, atualizado=datetime("now","localtime") WHERE slug=?' %
                          ','.join('%s=?' % k for k in sets), [ch[k] for k in sets] + [slug])
                c.commit(); c.close()
            return self._json(200, {'ok': True})
        return self._json(404, {'erro': 'rota'})
    def do_DELETE(self):
        partes = self.path.split('?')[0].split('/')
        if len(partes) == 4 and partes[1] == 'api' and partes[2] == 'acoes':
            c = conexao(); c.execute('DELETE FROM acoes WHERE id=?', (int(partes[3]),)); c.commit(); c.close()
            return self._json(200, {'ok': True})
        if len(partes) == 4 and partes[1] == 'api' and partes[2] == 'leads':
            c = conexao(); c.execute('DELETE FROM leads WHERE slug=?', (partes[3],)); c.commit(); c.close()
            return self._json(200, {'ok': True})
        return self._json(404, {'erro': 'rota'})
    def log_message(self, *a): pass

if __name__ == '__main__':
    novo = not os.path.exists(DB)
    conexao().close()
    if novo: importar_snapshot()
    if TTYD_BIN: ligar_ttyd()  # sobe o terminal web junto, se o ttyd estiver disponível
    print('Prospector rodando em http://localhost:%d  (Ctrl+C para parar)' % PORTA)
    try: webbrowser.open('http://localhost:%d' % PORTA)
    except Exception: pass
    try: ThreadingHTTPServer(('127.0.0.1', PORTA), App).serve_forever()
    except KeyboardInterrupt: print('\nEncerrado.')
