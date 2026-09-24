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

## Ajustes no fim do `template.html`

- `GTM_ID`: contêiner do Google Tag Manager. Vazio = sem medição.
- `CUPOM`: valor e código do desconto do pop-up de saída.

Eventos enviados ao `dataLayer`: `whatsapp_click` (com `wa_local` e `produto`), `popup_saida_exibido`, `filtro_ofertas`. Use `whatsapp_click` como conversão no Google Ads.

## Publicar (Cloudflare Pages)

- **Projeto:** `wjdesign-natal`, na conta Cloudflare da Moletto, conectado a este repositório. Diretório de saída: `public`, sem comando de build.
- **Todo push em `main` publica sozinho.** Outras branches geram um deploy de prévia.
- **Endereço:** https://wjdesign-natal.pages.dev
- **Domínio:** `natal.wjmoveis.com`. O DNS do wjmoveis.com fica no Wix: registro CNAME `natal` → `wjdesign-natal.pages.dev`.

## Regras de Google Ads respeitadas

- O pop-up de saída não mexe no botão voltar e aparece só uma vez por sessão.
- `noindex`: a página fica fora da busca orgânica, mas o robô do Google Ads (AdsBot) continua avaliando a página.
- Não há `robots.txt` bloqueando o AdsBot.
