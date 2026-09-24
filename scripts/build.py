#!/usr/bin/env python3
"""Gera public/index.html a partir da lista de ofertas abaixo.

Para trocar preço, incluir ou tirar uma peça: edite PRODUTOS e rode
    python3 scripts/build.py
O percentual de desconto, a economia e a mensagem do WhatsApp são calculados aqui.
"""
from html import escape
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
PUBLIC = RAIZ / "public"

WHATSAPP = "5561992146833"

# Desconto da campanha ("até 70% OFF"), usado no título, no topo e na etiqueta do hero.
# Os cards mostram o percentual real de cada peça.
DESCONTO_CAMPANHA = 70

# nome, detalhe, categoria, preço de, preço por, "cada"?, destaques, arquivo da foto, largura x altura da foto
PRODUTOS = [
    ("Sofá em couro natural", "2,80 m", "Sofás", 31180, 9900, False,
     ["Couro natural", "Materiais nobres", "Conforto absoluto"], "sofa-couro-280", (900, 680)),
    ("Sofá Living", "2,10 m", "Sofás", 12900, 5900, False,
     ["Design autoral", "Materiais nobres", "Conforto absoluto"], "sofa-living-210", (900, 785)),
    ("Sofá orgânico", "em couro natural", "Sofás", 22900, 11900, False,
     ["Design autoral", "Materiais nobres", "Conforto absoluto"], "sofa-organico-couro", (900, 715)),
    ("Sofá Living", "3,00 m", "Sofás", 19900, 6900, False,
     ["Tecido de alta qualidade", "Design exclusivo", "Conforto absoluto"], "sofa-living-300", (900, 700)),
    ("Banco / Recamier", "design atemporal", "Outras peças", 6900, 2900, False,
     ["Couro natural", "Acabamento premium", "Estilo atemporal"], "banco-recamier", (900, 720)),
    ("Sofá automatizado", "couro natural · 2,90 m", "Sofás", 44900, 19990, False,
     ["Couro natural", "Sistema automatizado", "Conforto superior"], "sofa-automatizado-couro", (900, 770)),
    ("Poltrona", "linho e madeira natural", "Poltronas", 6900, 2900, False,
     ["Linho de alta qualidade", "Madeira natural", "Design exclusivo"], "poltrona-linho-madeira", (1000, 803)),
    ("Sofá retrátil", "sem caixa · 2,50 m", "Sofás", 22900, 11500, False,
     ["Tecido de alta qualidade", "Conforto superior", "Design exclusivo"], "sofa-retratil", (1000, 682)),
    ("Poltronas", "tecido e madeira natural", "Poltronas", 15900, 5990, True,
     ["Tecido de alta qualidade", "Madeira natural", "Design exclusivo"], "poltronas-tecido-madeira", (1000, 830)),
    ("Sofá Living", "couro natural · 2,15 m", "Sofás", 21790, 6900, False,
     ["Couro natural", "Design exclusivo", "Conforto em alto nível"], "sofa-living-couro-215", (1000, 782)),
    ("Sofá Living Long Chaise", "3,60 m", "Sofás", 29170, 17900, False,
     ["Tecido de alta qualidade", "Design exclusivo", "Conforto superior"], "sofa-long-chaise", (900, 690)),
    ("Poltrona assinada", "Dirce Ayaco", "Poltronas", 22999, 8500, False,
     ["Peça assinada", "Design exclusivo", "Acabamento premium"], "poltrona-dirce-ayaco", (1000, 911)),
    ("Aparador", "madeira natural · 2,00 m", "Outras peças", 12999, 4900, True,
     ["Madeira natural", "Design exclusivo", "Acabamento premium"], "aparador-madeira", (900, 820)),
    ("Poltrona giratória", "em linho", "Poltronas", 6999, 3200, True,
     ["Linho de alta qualidade", "Base giratória", "Design exclusivo"], "poltrona-giratoria", (1000, 760)),
    ("Poltrona reclinável", "couro natural · automatizada", "Poltronas", 22750, 8500, True,
     ["Couro natural", "Sistema automatizado", "Design exclusivo"], "poltrona-reclinavel-couro", (900, 955)),
    ("Poltrona assinada", "Studio Uultis", "Poltronas", 24999, 10900, True,
     ["Madeira natural", "Design exclusivo", "Conforto premium"], "poltrona-studio-uultis", (1000, 687)),
    ("Mesa quadrada", "base em madeira · tampo laqueado · 1,50 m · cadeiras não inclusas", "Mesas", 18999, 6990, False,
     ["Base em madeira", "Tampo laqueado", "Design exclusivo"], "mesa-quadrada", (1086, 970)),
    ("Mesa de jantar assinada", "Studio Esse · 2,40 x 1,20 m", "Mesas", 25999, 12500, True,
     ["Madeira natural", "Tampo laqueado", "Design exclusivo"], "mesa-jantar-studio-esse", (900, 647)),
]

# Onde a foto fica melhor enquadrada no card 4:3 (padrão: centro)
ENQUADRAMENTO = {
    "poltrona-reclinavel-couro": "50% 70%",
    "poltrona-dirce-ayaco": "50% 45%",
    "aparador-madeira": "50% 40%",
    "mesa-quadrada": "50% 15%",
}


def brl(valor):
    """Moeda no padrão pt-BR: 31180 -> R$ 31.180 (centavos só quando existem)."""
    inteiro = f"{int(valor):,}".replace(",", ".")
    centavos = round((valor - int(valor)) * 100)
    return f"R$ {inteiro}" + (f",{centavos:02d}" if centavos else "")


def wa(texto):
    return f"https://wa.me/{WHATSAPP}?text={quote(texto)}"


def srcset(foto, largura):
    grande = min(largura, 960)
    return f"assets/{foto}-480.webp 480w, assets/{foto}-960.webp {grande}w"


def card(p, indice):
    nome, detalhe, categoria, de, por, cada, destaques, foto, (w, h) = p
    pct = round((de - por) / de * 100)
    economia = de - por
    titulo = f"{nome} {detalhe}"
    unidade = " cada" if cada else ""
    msg = (f"Olá! Vi na página de Natal da WJ Design o {titulo} por {brl(por).replace(chr(160), ' ')}"
           f"{unidade} e quero saber se ainda está disponível.")
    carregamento = 'loading="eager"' if indice < 2 else 'loading="lazy"'
    pos = ENQUADRAMENTO.get(foto)
    estilo = f' style="object-position:{pos}"' if pos else ""
    chips = "".join(f"<li>{escape(d)}</li>" for d in destaques)
    return f"""
        <li class="card" data-cat="{escape(categoria)}" data-reveal>
          <div class="card-media">
            <img src="assets/{foto}-480.webp" srcset="{srcset(foto, w)}"
                 sizes="(min-width: 1100px) 340px, (min-width: 640px) 45vw, 92vw"
                 width="{w}" height="{h}" {carregamento} decoding="async"{estilo}
                 alt="{escape(titulo)} da WJ Design">
            <span class="tag tag-sm" aria-hidden="true"><b>-{pct}%</b></span>
          </div>
          <div class="card-body">
            <p class="card-cat">{escape(categoria)}</p>
            <h3 class="card-title">{escape(nome)} <span>{escape(detalhe)}</span></h3>
            <p class="price">
              <span class="price-de">de <s>{brl(de)}</s></span>
              <span class="price-por">{brl(por)}<small>{unidade}</small></span>
              <span class="price-save">Você economiza {brl(economia)}{unidade} · {pct}% OFF</span>
            </p>
            <ul class="chips">{chips}</ul>
            <a class="btn btn-card" href="{wa(msg)}" target="_blank" rel="noopener"
               data-wa="card" data-product="{escape(titulo)}">
              {ICONE_WA}<span>Quero esta peça</span>
            </a>
          </div>
        </li>"""


ICONE_WA = ('<svg class="i-wa" viewBox="0 0 32 32" width="20" height="20" aria-hidden="true" focusable="false">'
            '<use href="#i-wa"/></svg>')

# Desenho do ícone, incluído uma vez no <body> e reaproveitado por todos os botões
SPRITE_WA = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
             '<symbol id="i-wa" viewBox="0 0 32 32">'
            '<path fill="currentColor" d="M16.04 3C8.86 3 3.03 8.82 3.03 16c0 2.3.6 4.54 1.74 6.51L3 29l6.66-1.74A12.95 '
            '12.95 0 0 0 16.04 29C23.2 29 29 23.18 29 16S23.2 3 16.04 3Zm0 23.63c-2 0-3.95-.54-5.66-1.55l-.4-.24-3.95 '
            '1.03 1.05-3.85-.26-.4A10.6 10.6 0 0 1 5.4 16c0-5.87 4.77-10.64 10.65-10.64 5.86 0 10.63 4.77 10.63 10.64 0 '
            '5.87-4.77 10.63-10.64 10.63Zm5.84-7.96c-.32-.16-1.89-.93-2.18-1.04-.3-.1-.5-.16-.72.16-.21.32-.82 1.04-1.01 '
            '1.25-.18.21-.37.24-.69.08-.32-.16-1.35-.5-2.57-1.59-.95-.85-1.59-1.9-1.78-2.21-.18-.32-.02-.5.14-.65.14-.14.32'
            '-.37.48-.56.16-.18.21-.32.32-.53.1-.21.05-.4-.03-.56-.08-.16-.72-1.73-.98-2.37-.26-.62-.52-.54-.72-.55h-.61c'
            '-.21 0-.56.08-.85.4-.29.32-1.12 1.09-1.12 2.66 0 1.57 1.14 3.09 1.3 3.3.16.21 2.25 3.43 5.44 4.81.76.33 1.35.52 '
            '1.81.67.76.24 1.46.2 2 .12.61-.09 1.89-.77 2.15-1.52.27-.74.27-1.38.19-1.52-.08-.13-.29-.21-.61-.37Z"/></symbol></svg>')


def main():
    produtos = sorted(PRODUTOS, key=lambda p: (p[3] - p[4]) / p[3], reverse=True)
    cards = "".join(card(p, i) for i, p in enumerate(produtos))
    maior = max(round((p[3] - p[4]) / p[3] * 100) for p in PRODUTOS)
    contagem = {c: sum(1 for p in PRODUTOS if p[2] == c) for c in ("Sofás", "Poltronas", "Mesas", "Outras peças")}

    html = (RAIZ / "scripts" / "template.html").read_text(encoding="utf-8")
    trocas = {
        "{{CARDS}}": cards,
        "{{TOTAL}}": str(len(PRODUTOS)),
        "{{N_SOFAS}}": str(contagem["Sofás"]),
        "{{N_POLTRONAS}}": str(contagem["Poltronas"]),
        "{{N_MESAS}}": str(contagem["Mesas"]),
        "{{N_OUTRAS}}": str(contagem["Outras peças"]),
        "{{DESCONTO_CAMPANHA}}": str(DESCONTO_CAMPANHA),
        "{{WHATSAPP}}": WHATSAPP,
        "{{ICONE_WA}}": ICONE_WA,
        "{{SPRITE_WA}}": SPRITE_WA,
        "{{WA_GERAL}}": wa("Olá! Vi a campanha de Natal da WJ Design e quero ajuda para escolher uma peça."),
        "{{WA_SOB_MEDIDA}}": wa("Olá! Vi a campanha de Natal da WJ Design e quero falar sobre um móvel sob medida."),
        "{{WA_POPUP}}": wa("Olá! Vi as ofertas de Natal da WJ Design e quero saber quais peças ainda estão disponíveis."),
        "{{WA_LOJA}}": wa("Olá! Vi a campanha de Natal da WJ Design e quero visitar uma das lojas. Onde está a peça que eu gostei?"),
    }
    for chave, valor in trocas.items():
        html = html.replace(chave, valor)
    assert "{{" not in html, "placeholder sem valor no template"
    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    print(f"public/index.html gerado com {len(PRODUTOS)} ofertas (campanha: até {DESCONTO_CAMPANHA}% OFF; maior desconto de peça: {maior}%)")


if __name__ == "__main__":
    main()
