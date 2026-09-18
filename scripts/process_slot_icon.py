#!/usr/bin/env python3
"""
Converte um favicon/badge de console (PNG com fundo branco, logo + texto
abaixo) num icone pronto para o seletor de presets da webui: recorta so o
selo do logo (descarta o texto), remove a borda/fundo branco (transparencia)
e redimensiona para 40x40.

Uso:
    python3 scripts/process_slot_icon.py caminho/para/favicon.png --box x0,y0,x1,y1 [--out nome.png]

O --box e o retangulo (em pixels da imagem original) contendo so o selo do
logo, sem a legenda de texto abaixo nem a borda/sombra externa. Descubra os
valores inspecionando a imagem (ex.: Read/zoom) antes de rodar.
"""

import argparse
from pathlib import Path

from PIL import Image

OUT_SIZE = 40


def process(src_path: Path, out_path: Path, box: tuple[int, int, int, int]):
    img = Image.open(src_path).convert("RGB")
    crop = img.crop(box).resize((OUT_SIZE, OUT_SIZE), Image.LANCZOS)
    crop = crop.convert("RGBA")
    px = crop.load()
    for y in range(OUT_SIZE):
        for x in range(OUT_SIZE):
            r, g, b, a = px[x, y]
            if r > 235 and g > 235 and b > 235:
                px[x, y] = (r, g, b, 0)

    crop.save(out_path, optimize=True)
    print(f"{src_path.name}: recorte {box} -> {out_path} ({out_path.stat().st_size} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--box", required=True, help="x0,y0,x1,y1")
    ap.add_argument("--out")
    args = ap.parse_args()

    src = Path(args.image)
    out = Path(args.out) if args.out else src.with_name(src.stem + "_40.png")
    box = tuple(int(v) for v in args.box.split(","))
    process(src, out, box)


if __name__ == "__main__":
    main()
