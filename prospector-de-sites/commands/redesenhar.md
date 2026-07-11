---
description: Redesenha os sites dos leads com estética premium (lote de 5 ou mais)
argument-hint: "[URLs ou nomes dos leads] — opcional, usa os 5+ melhores de leads.md"
---

Redesenhe as páginas dos leads seguindo a skill `redesign-premium`. Ela é obrigatória — leia a skill ANTES de escrever qualquer HTML.

## Seleção dos clientes

1. Leia `prospector-config.json` e `leads.md` na pasta conectada.
2. Se `$ARGUMENTS` trouxer URLs ou nomes, use-os. Senão, selecione os leads com status `novo` mais bem ranqueados — **mínimo de 5 clientes por lote** (se houver menos de 5 leads novos, use todos e avise que rodar `/prospectar` de novo aumenta o lote).
3. Confirme a lista com o usuário antes de começar.

## Para cada cliente do lote

1. **Extração (site INTEIRO, não só a home)**: abra o site original no Claude in Chrome (o sandbox costuma bloquear fetch direto a esses domínios). Primeiro **mapeie todas as páginas** (menu, rodapé, links internos) e liste-as. Depois, em CADA página: extraia todo o conteúdo real (textos, serviços, formação/credenciais, endereço, telefone/WhatsApp, e-mail, redes sociais, horários, paleta) e — OBRIGATÓRIO — as URLs reais do logo e de TODAS as fotos (via JavaScript: colete `img.currentSrc` de todas as imagens, rolando cada página até o fim para vencer lazy-load). Consolide a lista completa de fotos do site — ela é o gabarito da regra "todas as fotos no site novo". Tire screenshot de cada página e salve o da home como `sites/[slug]/original.png` (vai para o comparador).
2. **Direção de arte**: antes de escrever HTML, escreva o conceito da página (3-5 linhas, conforme a seção "Direção de arte" da skill) e confira que ele é DIFERENTE dos outros clientes do lote — fontes e composição não podem se repetir entre clientes.
3. **Redesign**: aplique a skill `redesign-premium` na íntegra. Regra de ouro: NADA inventado — é uma nova versão da página do cliente, não uma página nova. O logo original e as fotos originais DEVEM aparecer na página nova (se o cliente não tem site/logo, use composição tipográfica — nunca invente logo).
4. **Salvar** na pasta conectada, com o nome do cliente no arquivo para fácil identificação:
   - `sites/[slug]/[slug].html` — a página principal (arquivo único, autocontido, responsivo)
   - `sites/[slug]/[pagina].html` — CADA página interna do original ganha sua versão redesenhada (paridade de páginas da skill), com navegação relativa funcionando entre todas
   - `[nome]-editor.html` para CADA página gerada — a mesma página com a camada de edição visual injetada antes de `</body>` (script completo em `references/editor-visual.md` da skill `redesign-premium`). Gere SEMPRE, sem esperar o usuário pedir.
   - `sites/[slug]/original.png` — screenshot da home original (da extração)
5. **Comparador (OBRIGATÓRIO — não é opcional)**: crie/atualize `comparar.html` na RAIZ da pasta conectada usando o template pronto `references/comparador-template.html` da skill `redesign-premium`: copie o template, substitua `__CLIENTES__` pelo array JSON dos clientes (formato documentado no rodapé do próprio template — inclua `"oldshot": "sites/[slug]/original.png"` para o antes/depois funcionar mesmo quando o site antigo bloqueia iframe). Se `comparar.html` já existir, LEIA o array atual e acrescente os novos clientes no topo — nunca perca os antigos.
6. **Atualizar** o status do lead em `leads.md` para `redesenhado` e o `dashboard.html` (skill `dashboard-leads`): `status: redesenhado`.

## Revisão cruzada (obrigatória — depois do QA visual, antes da entrega)

Para cada cliente, lance um subagente revisor INDEPENDENTE (via ferramenta de agentes) com este mandato: ler a skill `redesign-premium`, ler o(s) HTML(s) gerado(s), ver os screenshots do QA e o `original.png`, e devolver veredito **APROVADO/REPROVADO** julgando: (a) cara de IA — alguma proibição presente?; (b) nível Awwwards — as 5+ qualidades exigidas estão lá de verdade?; (c) todas as fotos da lista de extração presentes?; (d) paridade de páginas cumprida?; (e) zero fato inventado (comparar com o conteúdo extraído). REPROVADO → corrigir os apontamentos e re-submeter ao revisor. Só entra na entrega quem foi APROVADO. Os revisores dos vários clientes podem rodar em paralelo.

## Checklist de saída (bloqueante)

Antes de apresentar qualquer resultado ao usuário, confirme que TODOS estes arquivos existem — se faltar algum, gere-o agora:

- [ ] `sites/[slug]/[slug].html` para CADA cliente do lote
- [ ] `sites/[slug]/[pagina].html` para CADA página interna do site original de cada cliente (ou consolidação anotada)
- [ ] `[nome]-editor.html` para CADA página gerada
- [ ] `sites/[slug]/original.png` para CADA cliente com site
- [ ] `comparar.html` na raiz, com abas para TODOS os clientes do lote (com `oldshot`)
- [ ] Veredito APROVADO do revisor independente para CADA cliente

Um redesign sem o editor ou sem o comparador é entrega incompleta — o usuário usa o comparador na proposta e no conteúdo dele.

## Verificação do lote

Antes de encerrar, para cada página criada: execute o **QA visual da skill** (abrir no Claude in Chrome, screenshots em 375/768/1440, julgar contra a barra Awwwards, corrigir e re-verificar até passar). Além disso, revise o HTML procurando textos placeholder esquecidos, links quebrados, seções vazias e problemas de contraste. Todos os CTAs devem apontar para o WhatsApp ou contato REAL do cliente. Página não vista renderizada = página não entregue.

## Saída (TRAVADA — siga exatamente este formato)

A entrega final ao usuário DEVE conter, nesta ordem, sem exceção:

1. **Cards de arquivo apresentados no chat** (via ferramenta de apresentação de arquivos): o `comparar.html` PRIMEIRO, depois a página e o editor de cada cliente. Se você não apresentou o card do `comparar.html`, a entrega está errada — apresente antes de escrever qualquer resumo.
2. **Resumo de 1 linha por cliente** (o que melhorou).
3. **Confirmação do dashboard**: frase explícita "Dashboard atualizado: [N] leads com status redesenhado" após atualizar o banco/dashboard conforme a skill `dashboard-leads` (se a pasta ainda não tem dashboard, CRIE-o agora pela skill — pasta nova nunca é desculpa para pular).
4. Orientação curta: `comparar.html` = antes/depois lado a lado · `[slug]-editor.html` = editar textos/imagens · próximo passo `/publicar`.

É PROIBIDO encerrar a resposta sem os itens 1 e 3. Se qualquer arquivo do checklist não existir, gere-o antes de responder.
