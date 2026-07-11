---
description: Escreve e envia (ou cria rascunho) da proposta por e-mail via Gmail
argument-hint: "[nome do cliente ou todos]"
---

Envie propostas para os leads com página publicada, seguindo a skill `proposta-email`.

## Passos

1. Leia `prospector-config.json` (assinatura e modo de envio) e `leads.md`.
2. Determine os destinatários: `$ARGUMENTS`, ou todos os leads com status `publicado` que ainda não receberam proposta. Somente leads com e-mail confirmado — para os demais, informe que a abordagem fica manual via WhatsApp (ofereça o texto adaptado).
3. **Descubra onde o site está hospedado — o `urlNova` do lead é a fonte da verdade** (o deploy do Vercel grava a URL `.vercel.app` ali; o `/publicar` grava a URL da HostGator). Monte o link da capa assim:
   - **`urlNova` contém `vercel.app`** → hospedado no Vercel. Link da capa = `[urlNova]/proposta.html`. A capa precisa estar no deploy: se `sites/[slug]/proposta.html` ainda não existia quando o site subiu, gere-a agora (template da skill `proposta-email`) e peça ao usuário para clicar em ▲ Vercel de novo (o deploy inclui o `proposta.html` da pasta) — só então o link fica válido.
   - **`urlNova` é um domínio HostGator** (ou vazio, mas há dados HostGator no config) → link da capa = `https://[dominio]/[pastaBase]/[slug]/proposta.html`. Se a capa não foi publicada, gere e publique agora via skill `deploy-hostgator` antes do rascunho.
   - **`urlNova` vazio e sem HostGator configurado** → o site ainda não está no ar em lugar nenhum: avise o usuário e pare (não dá pra mandar proposta sem link público). Sugira publicar (▲ Vercel na aba Sites ou `/publicar`).
   Confirme que o link abre com `https://` e cadeado antes de usar — link quebrado ou `http://` não vai para cliente.
4. Escreva o e-mail seguindo a skill `proposta-email` na íntegra (se o agente `copy-engine` estiver disponível, delegue a escrita a ele passando a skill como regra e os dados reais do lead — a checklist anti-spam do passo abaixo continua valendo sobre o texto dele), usando os dados reais do lead: elogio baseado nas avaliações do Google, o defeito específico apontado na prospecção e — como ÚNICO link — a capa do passo 3. NUNCA mencione preço.
5. **Checklist anti-spam (bloqueante)**: valide o e-mail contra a checklist da skill `proposta-email` (1 link, sem palavras-gatilho, sem anexo, assunto-pergunta ≤ 60 caracteres, primeira linha personalizada). Reescreva até passar em todos os itens.
6. Envio conforme o modo do config:
   - **rascunho** (padrão): crie o rascunho pelo conector do Gmail e informe que está pronto para revisão na caixa de rascunhos.
   - **enviar direto**: se o conector do Gmail não oferecer envio direto, use o Claude in Chrome no Gmail web para enviar, ou crie o rascunho e avise o usuário.
7. Atualize `leads.md` e o banco do dashboard: status `proposta` + data de envio.

## Saída

Resuma: quantas propostas criadas/enviadas e para quem, com o link da capa de cada uma. Lembre o usuário: `/respostas` verifica quem respondeu (dá pra agendar diário) e `/followup` cuida de quem está 3+ dias sem responder.
