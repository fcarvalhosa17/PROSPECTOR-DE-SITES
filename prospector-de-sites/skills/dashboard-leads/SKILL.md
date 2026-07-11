---
name: dashboard-leads
description: Esta skill deve ser usada para criar e ATUALIZAR o dashboard de leads — o painel de controle local (SQLite + página web) onde o usuário administra prospecções, sites, publicações e propostas. Acione sempre que qualquer comando do plugin mudar dados de leads (/prospectar, /redesenhar, /publicar, /proposta), ou quando o usuário disser "dashboard", "painel", "meus leads", "controle de clientes", "banco de dados de leads".
---

# Dashboard de leads (SQLite + página local)

Arquitetura na RAIZ da pasta conectada:

- **`prospector.db`** — banco SQLite, a FONTE DA VERDADE dos leads.
- **`dashboard-server.py` + `iniciar-dashboard.bat`** — mini-servidor local (Python padrão, sem dependências). O usuário dá duplo clique no .bat → abre `http://localhost:8765` com o painel completo: editar, excluir e arrastar cards salvam direto no banco.
- **`dashboard.html`** — a página do painel (gerada do template). Servida pelo servidor (modo banco) ou aberta por duplo clique (modo arquivo: só leitura + edições presas ao navegador). O badge no topo indica o modo.

## Setup (uma vez, no /setup ou no primeiro uso)

1. Copie `references/dashboard-server.py` e `references/iniciar-dashboard.bat` desta skill para a raiz da pasta conectada.
2. Crie o `prospector.db` com o schema abaixo (via python3/sqlite3 no bash).
3. Gere o `dashboard.html` a partir de `references/dashboard-template.html` substituindo `__DADOS__` pelo snapshot JSON.
4. Diga ao usuário: "duplo clique em `iniciar-dashboard.bat` abre o painel com o banco conectado" (requer Python instalado no Windows — se não tiver, o dashboard.html funciona no modo arquivo).

## Schema do banco

```sql
CREATE TABLE IF NOT EXISTS leads(
  slug TEXT PRIMARY KEY, nome TEXT, nicho TEXT, cidade TEXT, nota REAL, avaliacoes INTEGER,
  email TEXT, telefone TEXT, whatsapp TEXT, siteAntigo TEXT, motivo TEXT,
  status TEXT DEFAULT 'novo', urlNova TEXT, dataProposta TEXT, valor REAL, obs TEXT,
  contratoStatus TEXT DEFAULT 'pendente', contratoEm TEXT, manutencao REAL, pago INTEGER DEFAULT 0,
  docCliente TEXT, endCliente TEXT,
  atualizado TEXT DEFAULT (datetime('now','localtime')));
```

Status: `novo | redesenhado | publicado | proposta | respondeu | fechado | descartado`. `slug` é a chave.

## Como os comandos atualizam (SEMPRE os 2 passos)

1. **Upsert no banco** via bash (exemplo):
```bash
python3 - <<'EOF'
import sqlite3
c = sqlite3.connect('CAMINHO/prospector.db')
c.execute("INSERT INTO leads (slug,nome,status,...) VALUES (?,?,?,...) ON CONFLICT(slug) DO UPDATE SET status=excluded.status, atualizado=datetime('now','localtime')", (...))
c.commit()
EOF
```
   - `/prospectar` → insere leads (`novo`) e descartados (`descartado`, motivo em `obs`). NUNCA sobrescreva um lead cujo status já avançou.
   - `/redesenhar` → `status='redesenhado'` · `/publicar` → `status='publicado'`, `urlNova` · `/proposta` → `status='proposta'`, `dataProposta`.
   - Usuário conta que respondeu/fechou → `status='respondeu'|'fechado'`, `valor` (+ `manutencao` se houver mensalidade).
   - `/contrato` → `contratoStatus='enviado'` + `contratoEm`. Cliente assinou → `contratoStatus='assinado'`. Pagamento recebido → `pago=1`.
2. **Regenerar o snapshot**: leia todos os leads do banco e regrave `dashboard.html` do template com o JSON embutido atualizado (`{"atualizado": "...", "leads": [...]}`) — é o fallback para quem abre sem servidor.

Se o banco não existir ainda (usuário antigo), crie-o e importe os leads do snapshot embutido no `dashboard.html` atual antes do upsert. Respeite edições do usuário: antes de regravar um lead, leia o registro atual do banco.

## Ações, Chat e Vercel (modo banco apenas)

Com o servidor rodando, o painel também opera o funil inteiro:

- **Vista Ações**: botões que abrem um terminal com o Claude Code já executando o comando (`/setup`, `/prospectar`, `/redesenhar`, `/ajustar`, `/publicar`, `/proposta`, `/respostas`, `/followup`) na pasta conectada — informação que faltar, o Claude pergunta no terminal. Requer `claude` no PATH.
- **Vista Chat Claude**: chat embutido (`POST /api/chat`) que fala com o Claude Code CLI (`claude -p -c`, permissão acceptEdits, servidor só em localhost) — bom para ajustes de site e perguntas; tarefas com navegador vão pela vista Ações.
- **Botão ▲ Vercel** (card do site, vista Sites): deploy MANUAL — `POST /api/vercel/[slug]` copia `[slug].html` → `index.html`, gera `.vercelignore` (editor/manifesto/screenshot ficam de fora) e roda `vercel deploy --prod --yes`; ao concluir grava `urlNova` e status `publicado`. NUNCA publicar automaticamente — só quando o usuário clica. Requer `npm i -g vercel` + `vercel login` (uma vez).

## O que o painel faz sozinho (não reimplementar)

Kanban drag & drop, edição em modal, exclusão, busca, paginação automática, funil, follow-ups (proposta 4+ dias), receita fechada/potencial, vista Contratos (status pendente/enviado/assinado + link do documento + pago) e vista Financeiro (recebido, a receber, MRR de manutenções, projeção 12 meses) — tudo no template. O plugin só mantém o BANCO correto e o snapshot em dia.
