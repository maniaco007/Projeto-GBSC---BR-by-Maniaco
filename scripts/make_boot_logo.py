#!/usr/bin/env python3
"""
Converte uma imagem (PNG/JPG/etc) no logo de boot exibido no menu OLED
(SSD1306 128x64), gerando images.h e images/gbsicon.xbm.

Uso:
    python3 scripts/make_boot_logo.py caminho/para/logo.png [--width 84] [--height 63] [--threshold 128] [--invert]

O logo é redimensionado mantendo proporção, convertido para 1-bit
(preto e branco) e centralizado num canvas 128x64 antes de virar XBM.
Depois de rodar, o boot screen do menu OLED (drawXbm em gbs-control.ino)
usa o novo bitmap automaticamente - não precisa editar mais nada.
"""

import argparse
from pathlib import Path

from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
PANEL_W, PANEL_H = 128, 64


def to_xbm_bytes(img: Image.Image) -> bytes:
    """img must be mode '1' (1-bit). Returns packed XBM byte rows, LSB first per byte, row-padded to byte boundary."""
    w, h = img.size
    row_bytes = (w + 7) // 8
    data = bytearray(row_bytes * h)
    px = img.load()
    for y in range(h):
        for x in range(w):
            # XBM: bit set = black pixel (0 in PIL mode '1' after our thresholding below)
            if px[x, y] == 0:
                data[y * row_bytes + (x // 8)] |= 1 << (x % 8)
    return bytes(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image", help="Caminho da imagem de origem")
    ap.add_argument("--width", type=int, default=84, help="Largura máxima do logo (default 84, igual ao usado pelo fork do Tales)")
    ap.add_argument("--height", type=int, default=63, help="Altura máxima do logo (default 63)")
    ap.add_argument("--threshold", type=int, default=128, help="Limiar 0-255 para converter em preto/branco")
    ap.add_argument("--invert", action="store_true", help="Inverte preto/branco (use se o logo aparecer com as cores trocadas no OLED)")
    args = ap.parse_args()

    src = Image.open(args.image).convert("RGBA")
    # Composita sobre um fundo branco opaco antes de converter para tons de
    # cinza (mesma ideia de prepare_frame_gray em scripts/make_icon_animation.py):
    # sem isso, um PNG com fundo transparente cujo RGB por baixo for preto
    # (padrão comum de exportação) vira cinza 0 e o logo sai como uma caixa
    # sólida acesa no OLED em vez de silhueta transparente/apagada.
    background = Image.new("RGBA", src.size, (255, 255, 255, 255))
    background.alpha_composite(src)
    src = background.convert("L")

    # redimensiona mantendo proporção dentro de width x height
    ratio = min(args.width / src.width, args.height / src.height)
    new_w = max(1, round(src.width * ratio))
    new_h = max(1, round(src.height * ratio))
    resized = src.resize((new_w, new_h), Image.LANCZOS)

    bw = resized.point(lambda p: 255 if p >= args.threshold else 0, mode="L").convert("1")
    if args.invert:
        bw = bw.point(lambda p: 255 - p)

    # Não centralizamos no bitmap: gbs-control.ino já centraliza o logo na
    # tela 128x64 em tempo de execução com base em gbsicon_width/height.
    final = bw
    xbm_bytes = to_xbm_bytes(final)
    w, h = final.size

    def format_c_array(data: bytes) -> str:
        lines = []
        for i in range(0, len(data), 12):
            chunk = data[i:i + 12]
            lines.append("    " + ", ".join(f"0x{b:02x}" for b in chunk) + ",")
        return "\n".join(lines)

    header = (
        f"#define gbsicon_width {w}\n"
        f"#define gbsicon_height {h}\n"
        f"static unsigned char gbsicon_bits[] = {{\n"
        f"{format_c_array(xbm_bytes)}\n"
        f"}};\n"
    )

    (REPO_ROOT / "images.h").write_text(header)

    xbm = (
        f"#define gbsicon_width {w}\n"
        f"#define gbsicon_height {h}\n"
        f"static unsigned char gbsicon_bits[] = {{\n"
        f"{format_c_array(xbm_bytes)}\n"
        f"}};\n"
    )
    (REPO_ROOT / "images" / "gbsicon.xbm").write_text(xbm)

    print(f"OK: logo {w}x{h} gravado em images.h e images/gbsicon.xbm")


if __name__ == "__main__":
    main()
