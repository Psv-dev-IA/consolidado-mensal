#!/usr/bin/env python3
"""
Extrai a paleta de cores da logo anexada pelo consultor.

Uso:
    python extrair_cores.py /mnt/user-data/uploads/logo.png

Devolve um JSON com as variáveis CSS prontas para colar no template:
  --cor-principal, --cor-secundaria, --cor-texto, --cor-negativo, --cor-linha

Aceita .png, .jpg, .jpeg, .webp, .gif e .svg.

Como ele decide:
  - Descarta fundo transparente, branco, preto e cinzas sem saturação.
  - Ordena as cores restantes por área ocupada na imagem.
  - A cor principal é a mais presente que tenha contraste suficiente para
    receber texto branco em cima. Se a mais presente for clara demais, ela
    é escurecida até passar no contraste, preservando o matiz.
  - A secundária é uma versão bem clara da principal, para fundo de quadro.
  - O negativo usa o vermelho padrão, a não ser que a marca já seja vermelha,
    caso em que ele escurece para não se confundir com a principal.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

NEGATIVO_PADRAO = "#B3261E"
NEUTRO = {
    "--cor-principal": "#1A1A1A",
    "--cor-secundaria": "#F5F5F5",
    "--cor-texto": "#1A1A1A",
    "--cor-negativo": NEGATIVO_PADRAO,
    "--cor-linha": "#DDDDDD",
}


def hex_de(rgb):
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, int(c))) for c in rgb])


def rgb_de(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminancia(rgb):
    def canal(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(a, b):
    la, lb = luminancia(a), luminancia(b)
    claro, escuro = max(la, lb), min(la, lb)
    return (claro + 0.05) / (escuro + 0.05)


def saturacao(rgb):
    mx, mn = max(rgb), min(rgb)
    return 0 if mx == 0 else (mx - mn) / mx


def escurecer(rgb, fator):
    return tuple(c * fator for c in rgb)


def clarear(rgb, fator):
    return tuple(c + (255 - c) * fator for c in rgb)


def util(rgb):
    """Cor que serve como cor de marca: nem branca, nem preta, nem cinza morto."""
    lum = luminancia(rgb)
    if lum > 0.92:
        return False
    if lum < 0.015:
        return False
    if saturacao(rgb) < 0.12 and not (0.02 < lum < 0.30):
        return False
    return True


def cores_svg(caminho):
    texto = Path(caminho).read_text(errors="ignore")
    achados = re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", texto)
    contagem = Counter(h.upper() for h in achados)
    return [(rgb_de(h), n) for h, n in contagem.most_common() if util(rgb_de(h))]


def cores_bitmap(caminho):
    from PIL import Image

    img = Image.open(caminho)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        fundo = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(fundo, img)
    img = img.convert("RGB")
    img.thumbnail((200, 200))
    reduzida = img.quantize(colors=24, method=2).convert("RGB")

    pares = reduzida.getcolors(maxcolors=1 << 16) or []
    pares.sort(key=lambda p: p[0], reverse=True)
    return [(rgb, n) for n, rgb in pares if util(rgb)]


def montar_paleta(candidatas):
    if not candidatas:
        return dict(NEUTRO), "logo sem cor aproveitável, paleta neutra aplicada"

    principal = candidatas[0][0]
    ajuste = ""

    # Texto branco precisa ler em cima da cor principal, que é usada no
    # cabeçalho da tabela. 4.5 é o piso de contraste para texto normal.
    tentativas = 0
    while contraste(principal, (255, 255, 255)) < 4.5 and tentativas < 12:
        principal = escurecer(principal, 0.88)
        tentativas += 1
    if tentativas:
        ajuste = "cor principal escurecida para o texto branco ler no cabeçalho da tabela"

    secundaria = clarear(principal, 0.93)
    linha = clarear(principal, 0.78)

    # Texto do corpo: quase preto, com um toque do matiz da marca.
    texto = escurecer(principal, 0.22)
    if luminancia(texto) > 0.12:
        texto = (26, 26, 26)

    negativo = rgb_de(NEGATIVO_PADRAO)
    if contraste(negativo, principal) < 1.6:
        negativo = escurecer(negativo, 0.72)

    return {
        "--cor-principal": hex_de(principal),
        "--cor-secundaria": hex_de(secundaria),
        "--cor-texto": hex_de(texto),
        "--cor-negativo": hex_de(negativo),
        "--cor-linha": hex_de(linha),
    }, ajuste


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"erro": "informe o caminho da logo"}, ensure_ascii=False))
        sys.exit(1)

    caminho = Path(sys.argv[1])
    if not caminho.exists():
        print(json.dumps({"erro": f"arquivo não encontrado: {caminho}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        if caminho.suffix.lower() == ".svg":
            candidatas = cores_svg(caminho)
        else:
            candidatas = cores_bitmap(caminho)
    except Exception as e:  # noqa: BLE001
        print(json.dumps(
            {"paleta": NEUTRO, "observacao": f"não consegui ler a logo ({e}), paleta neutra aplicada"},
            ensure_ascii=False, indent=2))
        return

    paleta, ajuste = montar_paleta(candidatas)
    saida = {
        "arquivo": caminho.name,
        "paleta": paleta,
        "cores_encontradas": [hex_de(rgb) for rgb, _ in candidatas[:6]],
    }
    if ajuste:
        saida["observacao"] = ajuste
    print(json.dumps(saida, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
