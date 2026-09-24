# WJ Design · Landing de Natal (Google Ads)

Página de vendas da campanha de Natal da WJ Design, feita para receber tráfego do Google Ads. Toda ação leva ao WhatsApp da loja (61 99214-6833) com a mensagem pronta.

## Estrutura

| Caminho | O que é |
|---|---|
| `public/index.html` | A página. Gerada pelo script, não edite à mão |
| `public/assets/` | Fotos sem texto, em WebP (480 px e 960 px), e a imagem de compartilhamento |
| `public/_headers` | Cabeçalhos de segurança e cache (Cloudflare Pages) |
| `scripts/template.html` | Layout, textos, CSS e JS da página |
| `scripts/build.py` | Lista de ofertas (preços e fotos). Gera o `index.html` |

## Trocar preço, incluir ou tirar peça

1. Edite a lista `PRODUTOS` em `scripts/build.py`.
2. Rode `python3 scripts/build.py`.

O percentual de desconto, a economia, a ordem (maior desconto primeiro), e os contadores dos filtros são recalculados. O "até 70% OFF" da campanha fica em `DESCONTO_CAMPANHA`, no mesmo arquivo.

## Medição (Google Tag Manager)

O contêiner **GTM-55HF7G4X** está instalado no `<head>`, com o `<noscript>` logo após o `<body>`.

Eventos enviados ao `dataLayer`:
- `whatsapp_click`, com `wa_local` (topo, hero, card, flutuante, popup-saida…) e `produto`. Use como conversão do Google Ads.
- `popup_saida_exibido`, com `origem` (mouse ou rolagem).
- `filtro_ofertas`, com `filtro`.

## Pop-up de saída

É só um aviso de urgência, sem desconto: "Espere! Essas peças não voltam", com os dias que faltam para o Natal e um botão para o WhatsApp.

## Publicar (Cloudflare Pages)

- **Projeto:** `wjdesign-natal`, na conta Cloudflare da Moletto, conectado a este repositório. Diretório de saída: `public`, sem comando de build.
- **Todo push em `main` publica sozinho.** Outras branches geram um deploy de prévia.
- **Endereço:** https://wjdesign-natal.pages.dev
- **Domínio:** `natal.wjmoveis.com`. O DNS do wjmoveis.com fica no Wix: registro CNAME `natal` → `wjdesign-natal.pages.dev`.

## Regras de Google Ads respeitadas

- A pop-up de saída não mexe no botão voltar e aparece só uma vez por sessão.
- `noindex`: a página fica fora da busca orgânica, mas o robô do Google Ads (AdsBot) continua avaliando a página.
- Não há `robots.txt` bloqueando o AdsBot.

## Configuração do GTM pronta para importar

`gtm/wj-gtm-conversao-whatsapp.json` tem a tag do Google, o vinculador de conversões, o acionador `whatsapp_click` e a conversão "Clique no WhatsApp". No GTM: Administrador → Importar contêiner → escolher o arquivo → espaço de trabalho existente → **Mesclar** (renomear conflitos). O ID (`16658250321`) e o rótulo (`sgyaCIGYhYQdENH0ooc-`) da conversão "Clique no WhatsApp" já vêm preenchidos. Teste em Visualizar e clique em Enviar.

## Proteção contra cópia

- `functions/_middleware.js`: bloqueia programas de cópia de sites (HTTrack, wget, scrapers) na página; robôs do Google, WhatsApp e redes sociais continuam liberados. Roda só no HTML (`public/_routes.json`).
- Script no fim do `template.html`: se a página for publicada em outro domínio, o visitante é mandado para `natal.wjmoveis.com`. Para usar outro domínio oficial, inclua na lista `ok`.
- `_headers`: impede que a página seja exibida dentro de outro site (iframe) e pede para buscadores não guardarem cópia.
- Fotos sem menu "salvar imagem" e sem arrastar; aviso de direitos autorais no rodapé.
