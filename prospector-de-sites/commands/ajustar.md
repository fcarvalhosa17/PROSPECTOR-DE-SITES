---
description: Ajusta o site de um cliente já redesenhado — pelo nome, com memória do projeto
argument-hint: "[nome do cliente] [o que mudar] — ex.: /ajustar Dr Fulano troca a foto do hero"
---

Ajuste o site de um cliente existente. O usuário identifica o cliente pelo NOME — encontre-o e carregue toda a memória antes de mexer em qualquer arquivo.

## Localizar o cliente

1. Leia `prospector-config.json` para achar a pasta conectada.
2. Encontre o cliente citado em `$ARGUMENTS`: busque por nome (aceite match parcial e sem acento) no `prospector.db` (ou `leads.md` como fallback) e confirme o slug. Se houver mais de um match ou nenhum, liste os clientes com status `redesenhado`/`publicado` e pergunte qual é.
3. Carregue a memória do cliente: `sites/[slug]/cliente.json` (conceito de direção de arte, fontes, paleta, páginas, fotos, consolidações). Se o manifesto não existir (site feito antes dessa versão do plugin), reconstrua-o agora lendo os HTMLs existentes e salve — a partir daí ele é a fonte da verdade.

## Aplicar o ajuste

1. Entenda o pedido do usuário. Se `$ARGUMENTS` só trouxer o nome, pergunte o que ajustar (mostre a lista de páginas do manifesto).
2. Toda mudança RESPEITA a skill `redesign-premium`: o conceito de direção de arte do manifesto se mantém (fontes, paleta, composição coerentes), nada de fato inventado, contraste AA, responsividade total. Ajuste ≠ redesign: mude o que foi pedido sem descaracterizar o resto.
3. Edite a(s) página(s) em `sites/[slug]/` e REGENERE o par `-editor.html` de cada página alterada (a camada de edição de `references/editor-visual.md` da skill `redesign-premium` sobre o HTML novo — nunca deixe editor dessincronizado).
4. Se o usuário editou textos pelo `-editor.html` e quer incorporar: leia o HTML salvo pelo editor e aplique as mudanças na página principal antes do seu ajuste.

## QA e sincronização (mesmo rigor do /redesenhar)

1. **QA visual** nas páginas alteradas: screenshots em 375/768/1440 no Claude in Chrome, julgar, corrigir até passar.
2. Atualize o `cliente.json` (conceito/fontes/páginas se mudaram) e o campo `obs` do lead no banco: "Ajuste em [data]: [resumo]".
3. Se o site está `publicado`: avise que o ajuste é LOCAL até republicar e ofereça rodar `/publicar [cliente]` agora.

## Saída

1. Card do(s) arquivo(s) alterado(s) no chat.
2. 1 linha: o que mudou.
3. Status: local ou republicado (com URL).
