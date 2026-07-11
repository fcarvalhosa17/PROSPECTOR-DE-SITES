---
name: redesign-premium
description: Esta skill deve ser usada ao redesenhar o site de um cliente prospectado — criar uma versão nova, premium e de alta conversão da página existente, mantendo conteúdo, logo e paleta do cliente. Acione quando o usuário disser "redesenhar site", "melhorar página", "refazer o site do cliente" ou rodar /redesenhar ou /editor.
---

# Redesign premium de páginas

Criar uma NOVA VERSÃO da página do cliente — não uma página nova. O cliente precisa reconhecer o próprio negócio, só que elevado ao padrão que o faturamento dele merece.

## Regras invioláveis

1. **Nenhum FATO inventado — mas o texto deve ser APRIMORADO.** Todo serviço, credencial, número, endereço e contato vem do site original (ou do perfil do Google). Sem dados fictícios, sem depoimentos criados, sem serviços que o cliente não oferece. Porém o TEXTO não é copiado cru: reescreva com copy melhor — títulos mais fortes, frases mais claras, hierarquia de leitura — sempre dizendo a mesma verdade que o original diz.
2. **TODAS as fotos e o logo originais são OBRIGATÓRIOS no site novo — de TODAS as páginas.** Não é "algumas fotos": é o acervo completo. Percorra CADA página do site original (home, sobre, serviços, galeria…) coletando `img.currentSrc` de todas as imagens (rolar cada página até o fim para vencer lazy-load). Toda foto utilizável (profissional, equipe, consultório, trabalhos, logo) deve constar no site novo, pelas URLs originais. Descartar só o que for lixo real (ícone genérico, banner de cookie, foto de banco de imagens quebrada). O cliente precisa se reconhecer na hora — e sentir que nada do site dele se perdeu.
3. **Identidade preservada.** Manter logo, paleta de cores e fotos do cliente. Se a paleta original for fraca (ex.: cores puras saturadas), refinar os tons — nunca trocar a família de cores.
4. **Paridade de páginas (obrigatória).** Antes de redesenhar, mapeie o site original INTEIRO: menu, rodapé e links internos. Se o original tem outras páginas (serviços detalhados, sobre, galeria, blog institucional…), o site novo cobre TODAS: cada página relevante ganha versão redesenhada própria em `sites/[slug]/[pagina].html`, com o MESMO sistema de design (fontes, paleta, direção de arte) e navegação funcional entre elas (links relativos). Página rasa do original (ex.: "contato" com 3 linhas) pode ser consolidada como seção da principal — mas nenhum conteúdo se perde e a decisão é anotada. Entregar só a home melhor quando o original tem 5 páginas é entrega INCOMPLETA: o site novo não pode ser menor que o atual em nada.
5. **Mais completo que o original.** O site novo deve ser MUITO mais profissional e bem estruturado. Se o original tem poucas seções, CRIE as seções relevantes que faltam — desde que preenchidas só com informação real: prova social (nota + avaliações reais do Google), "como funciona o atendimento" (se dedutível do original), localização com mapa, horários (do perfil do Maps), FAQ com dúvidas respondíveis pelo conteúdo real. Seção que exigiria inventar fato = não criar.
6. **Arquivo único por página.** Cada página gerada (`sites/[slug]/[slug].html` e as internas `sites/[slug]/[pagina].html`) é autocontida: CSS inline no `<head>`, sem build, sem dependências além de Google Fonts.
7. **Responsividade TOTAL (inegociável).** A página será vista no celular do cliente E dentro da moldura da página-capa (~1000-1500px). Ela deve ser perfeita em QUALQUER largura: 360, 375, 768, 1024, 1280 e 1440px — sem rolagem horizontal, sem texto vazando, sem imagem esticada, sem seção quebrada em nenhum desses pontos. Usar grid/flex fluidos, `clamp()` para tipografia e breakpoints testados um a um. Página que quebra em alguma largura NÃO é entregue.
8. **Editor sempre.** CADA página gerada tem seu par `[nome]-editor.html` (camada de edição de `references/editor-visual.md`) — nunca entregar página sem a versão editável.
9. **Comparador sempre.** Todo lote de redesign termina com `comparar.html` na raiz da pasta conectada, gerado a partir de `references/comparador-template.html` (substituir `__CLIENTES__` pelo array JSON; mesclar com clientes já existentes). No array, além de `old` (URL), inclua `"oldshot": "sites/[slug]/original.png"` — o screenshot da home original tirado na extração (muitos sites bloqueiam iframe via `X-Frame-Options`; o screenshot garante o antes/depois sempre visível). A entrega padrão de cada cliente: TODAS as páginas redesenhadas + editor de cada uma + `original.png` + aba no comparador.

## Estrutura da página (adaptar à profissão)

1. **Hero**: nome + especialidade, promessa clara em 1 linha, CTA primário (WhatsApp) visível sem rolar, foto do profissional/clínica.
2. **Prova social**: nota do Google em destaque ("5.0 ★ · 121 avaliações no Google") — é real e verificável. Citar 2-3 trechos de avaliações reais do Google Maps se coletados.
3. **Serviços/áreas de atuação**: cards clicáveis — cada card leva à âncora da seção detalhada ou direto ao WhatsApp com mensagem pré-preenchida (`https://wa.me/55DDDNUMERO?text=Olá! Vim pelo site e quero saber sobre [serviço]`).
4. **Sobre**: formação e credenciais reais (geram autoridade — nunca cortar).
5. **Oferta estruturada** (quando fizer sentido): transformar "agende uma consulta" em opções de engajamento (ex.: sessão pontual, acompanhamento 90 dias, plano semestral) — SEM preços, apenas nomes e o que incluem, todos levando ao WhatsApp. Só criar planos que sejam agrupamento óbvio do serviço já oferecido.
6. **Localização e contato**: endereço, mapa (iframe do Google Maps), horários, telefone, redes.
7. **Rodapé**: dados do profissional (registro de classe se existir no original).

## Copywriting (aprimorar sem inventar — reescrever é obrigatório)

O texto do site novo NUNCA é o texto do site velho colado. Reescreva tudo com técnica, dizendo apenas o que o cliente já diz/oferece:

- **Headline do hero = benefício, não rótulo.** "Nutrição esportiva em SP" é rótulo; "Seu treino merece resultados que aparecem" é headline (com o rótulo virando kicker/subtítulo pra SEO).
- **Estrutura PAS suave** ao longo da página: toque na dor real do público, mostre o caminho, apresente o serviço como solução — no tom do nicho, sem agressividade de lançamento.
- **Escaneabilidade**: ninguém lê parágrafo de 8 linhas. Quebre em blocos de 2-3 linhas, bullets com verbo, subtítulos que contam a história sozinhos (quem só lê os títulos entende a página).
- **1 CTA por dobra**, sempre orientado à ação e ao benefício ("Quero minha avaliação" > "Clique aqui"), todos pro WhatsApp com mensagem pré-preenchida contextual.
- **Prova social costurada**, não empilhada: nota do Google perto do CTA, citação real perto da seção a que se refere.
- **Microcopy**: legendas sob botões ("resposta em poucos minutos"), rótulos humanos em formulários e seções.
- Proibido: clichês vazios ("qualidade e compromisso", "excelência no atendimento") sem fato que os sustente; superlativos inventados; promessas de resultado que o cliente não faz.

## Barra de qualidade (o teste Awwwards)

A página pronta deve passar por trabalho de estúdio que cobra R$ 15-50 mil — teste honesto: submetida ao Awwwards/SOTD, ela não pode parecer feita por IA nem por template. Um designer sênior olhando por 5 segundos precisa pensar "alguém dirigiu isso", não "isso saiu de um gerador". Isso exige duas camadas:

**Rigor estrutural**: grid consistente, alinhamento impecável, alternância de ritmo entre seções (fundo claro/escuro/acento, largura cheia/contida), imagens com tratamento coerente, escala tipográfica harmônica, nenhuma seção "órfã".

**Direção de arte** (a camada que separa 15k de template — seção abaixo). Estrutura correta com estética genérica = entrega reprovada.

## Direção de arte (obrigatória — decidir ANTES de escrever HTML)

Antes de qualquer código, escrever em 3-5 linhas o **conceito** da página: qual sensação o negócio deve transmitir (ex.: advocacia tradicional → peso institucional, serifa editorial, densidade controlada; barbearia → cru, tipografia condensada gigante, contraste duro; clínica estética → etéreo, respiro extremo, fotografia dominante). O conceito nasce do NEGÓCIO real do cliente — nicho, público, cidade, fotos disponíveis — nunca de um padrão fixo. Duas páginas do mesmo lote NUNCA podem ter a mesma cara: variar direção, fontes e composição entre clientes é obrigatório. Para inspiração por nicho, consulte `references/direcoes-por-nicho.md` — ponto de partida a adaptar, nunca menu a copiar.

### Proibições absolutas (a "cara de IA")

- **Fontes proibidas**: Inter, Roboto, Open Sans, Lato, Montserrat, Poppins, Arial, system fonts — e proibido repetir o mesmo par de fontes em dois clientes do lote. Playfair Display só se o nicho realmente pedir e nunca com Inter.
- **Layout proibido**: hero centrado com título + parágrafo + botão empilhados no meio; grade de 3 cards idênticos com ícone em cima; seções todas com o mesmo padding simétrico; tudo alinhado ao centro.
- **Estética proibida**: gradiente roxo/azul sobre branco; sombras suaves idênticas em todos os cards; border-radius uniforme em tudo; fundo 100% chapado em todas as seções; emoji como ícone.
- **Copy proibida**: "Bem-vindo ao nosso site", títulos de seção literais ("Nossos Serviços", "Sobre Nós", "Contato") — títulos de seção também são copy e devem carregar a voz da página.

### Qualidades exigidas (toda página precisa de pelo menos 5)

1. **Tipografia com caráter**: display font inesperada e adequada ao nicho (explorar o catálogo inteiro do Google Fonts: Fraunces, Libre Caslon, Bricolage Grotesque, Instrument Serif, Unbounded, DM Serif Display, Space Mono como acento…) + corpo refinado. Escala dramática: h1 pode ser 15-20vw se a composição pedir. Peso, largura e itálico usados com intenção.
2. **Composição que quebra a grade**: assimetria deliberada, sobreposição de elementos (texto sobre foto sangrada, número gigante atrás de card), diagonais, elementos que atravessam limites de seção, hero em layout editorial (tipo revista) em vez de banner centrado.
3. **Atmosfera de fundo**: nunca só cor chapada — grain/noise sutil (SVG inline), gradiente da paleta do cliente em mesh discreto, padrão geométrico do nicho, textura de papel, vinheta. Sempre derivado da paleta do cliente.
4. **Motion com propósito**: reveals em scroll (IntersectionObserver, ~10 linhas de JS), stagger na entrada do hero (animation-delay em CSS), hovers que surpreendem (imagem que desloca, sublinhado que desenha, card que inclina levemente). CSS-first, nada de biblioteca.
5. **Detalhe assinatura**: pelo menos UM elemento memorável e único da página — número de seção tipográfico gigante, marquee com as especialidades, borda desenhada à mão, régua de horários visual, mapa estilizado. O elemento que a pessoa lembra depois de fechar.
6. **Ritmo espacial intencional**: seções com densidades diferentes — uma comprimida e densa, a próxima com respiro extremo; largura cheia alternando com colunas estreitas; texto vertical ou girado onde couber.
7. **Fotografia dirigida**: fotos do cliente tratadas como matéria-prima de design — duotone na paleta da marca, recortes inesperados (não só retângulo arredondado), molduras que sangram, sobreposição com tipografia.

### O que continua inegociável (não sacrificar pela estética)

- Contraste AA no texto, CTA do WhatsApp visível sem rolar, botão flutuante do WhatsApp.
- Paleta = família de cores do CLIENTE (a direção de arte trabalha DENTRO dela — refinar tons, jamais trocar).
- Máx. 2-3 famílias de fonte (a terceira só como acento mono/display pontual).
- Velocidade: arquivo único, sem bibliotecas, JS mínimo (só reveals/interações leves), `prefers-reduced-motion` respeitado.
- Legibilidade mobile: a ousadia da composição desktop degrada com elegância para o empilhamento no celular — nunca vira bagunça.

## QA visual (obrigatório — nenhuma página é entregue sem ser VISTA)

Checklist de texto não substitui olho. Para cada página gerada, antes de marcar como pronta:

1. Abra o arquivo no Claude in Chrome (`file://`) e tire screenshot em **3 larguras**: 375 (celular), 768 (tablet) e 1440 (desktop).
2. Julgue cada screenshot contra a barra Awwwards: composição realmente quebra o padrão genérico? Tipografia tem o impacto planejado no conceito? Fotos do cliente carregaram (URL externa pode ter quebrado)? Algum texto vazando, seção quebrada ou contraste ruim?
3. **Se qualquer coisa falhar, corrija e re-screenshot.** Repita até as 3 larguras passarem. Página que o modelo não viu renderizada é página não entregue.

## Checklist final (obrigatório antes de entregar)

- [ ] Zero texto placeholder / lorem ipsum
- [ ] Conceito de direção de arte escrito ANTES do código e refletido na página
- [ ] Nenhuma proibição da lista "cara de IA" presente (fontes, layout, estética, copy)
- [ ] Pelo menos 5 das 7 qualidades exigidas presentes e identificáveis
- [ ] Página visualmente DIFERENTE das outras do lote (fontes e composição distintas)
- [ ] Todos os links e CTAs apontam para contato REAL do cliente
- [ ] Número do WhatsApp no formato wa.me correto (55 + DDD + número)
- [ ] QA visual executado: screenshots em 375/768/1440 tirados, julgados e aprovados
- [ ] Responsivo verificado em 360, 375, 768, 1024, 1280 e 1440px — zero rolagem horizontal e zero quebra em TODAS
- [ ] Título e meta description preenchidos com nome + especialidade + cidade
- [ ] JSON-LD `LocalBusiness` (ou subtipo do nicho) com dados reais do cliente em cada página; 1 só `h1` por página; `alt` em todas as fotos
- [ ] Comparação com o original: todo conteúdo importante do site antigo está presente
- [ ] TODAS as fotos utilizáveis de TODAS as páginas do original presentes no site novo (conferir contra a lista coletada na extração)
- [ ] Paridade de páginas: cada página do original tem equivalente redesenhado (ou consolidação anotada) e a navegação entre elas funciona
- [ ] Logo e fotos ORIGINAIS do cliente presentes na página nova
- [ ] `[slug]-editor.html` gerado e `comparar.html` atualizado

## Editor visual e comparador

A camada de edição visual (para gerar `[slug]-editor.html`) está em `references/editor-visual.md` — injetar o script exatamente como documentado lá. O comparador antes/depois está em `references/comparador-template.html` — substituir `__CLIENTES__` pelo array JSON e salvar como `comparar.html` na raiz da pasta conectada (mesclando com clientes existentes).
