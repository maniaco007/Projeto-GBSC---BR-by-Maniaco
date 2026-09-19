#!/usr/bin/env python3
"""
Gera OLEDIconAnimations.cpp a partir de um manifesto de icones animados para
o protetor de tela do menu OLED (SSD1306 128x64).

Cada entrada do manifesto vira um IconAnimation (ver OLEDIconAnimations.h),
associado ao mesmo icone escolhido no seletor de icone da webui (o "iconId"
tem que bater com o id do simbolo "gbs-slot-icon-<id>" em
public/src/index.html.tpl / SLOT_ICON_COUNT em public/src/index.ts).

Uso:
    python3 scripts/make_icon_animation.py [--manifest assets_in/icons/animations_manifest.json]

Formato do manifesto (JSON, lista de objetos):
    {
      "iconId": 9,
      "name": "gamecube",
      "source": "assets_in/icons/gamecube_40.png",
      "size": 32,
      "threshold": 128,
      "invert": false,
      // Uma das duas opcoes abaixo:
      "synthBounceFrames": 4,      // gera uma animacao simples subindo/descendo
      "synthBounceAmplitude": 3,   // a partir de uma imagem estatica (px)
      // OU, se "source" for um .gif animado com varios quadros, os quadros
      // sao extraidos diretamente dele (nao precisa de synthBounce*).
    }

Depois de editar o manifesto, rode o script de novo e recompile - nenhum
outro arquivo precisa ser tocado (o .cpp gerado e incluido automaticamente
pelo build_src_filter do platformio.ini).
"""

import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageSequence

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = REPO_ROOT / "assets_in" / "icons" / "animations_manifest.json"
OUTPUT_CPP = REPO_ROOT / "OLEDIconAnimations.cpp"


def otsu_threshold(gray_img: Image.Image) -> int:
    """Otsu's method: picks the threshold that best separates the pixel
    histogram into two classes (ink vs background)."""
    hist = np.array(gray_img.histogram(), dtype=np.float64)
    total = hist.sum()
    if total == 0:
        return 128
    sum_all = np.dot(np.arange(256), hist)
    sum_bg, weight_bg, best_between, best_thresh = 0.0, 0.0, -1.0, 128
    for t in range(256):
        weight_bg += hist[t]
        if weight_bg == 0:
            continue
        weight_fg = total - weight_bg
        if weight_fg == 0:
            break
        sum_bg += t * hist[t]
        mean_bg = sum_bg / weight_bg
        mean_fg = (sum_all - sum_bg) / weight_fg
        between = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2
        if between > best_between:
            best_between = between
            best_thresh = t
    return best_thresh


def auto_threshold(gray_img: Image.Image) -> int:
    """Otsu's threshold, with a fallback to a percentile-based pick when
    Otsu still leaves the image almost entirely black or almost entirely
    white (common for logos/line-art with thin strokes or soft gradients),
    so every icon ends up with a recognizable ~15-55% ink coverage on the
    1-bit OLED instead of degenerating into a blank or solid square."""
    arr = np.array(gray_img, dtype=np.uint8)
    t = otsu_threshold(gray_img)
    ink_ratio = (arr < t).mean()
    if ink_ratio < 0.08 or ink_ratio > 0.55:
        target = 30
        t = int(np.percentile(arr, target))
        t = max(40, min(230, t))
    return t


def to_xbm_bytes(img: Image.Image) -> bytes:
    """img must be mode '1'. Same packing as scripts/make_boot_logo.py:
    LSB-first per byte, row-padded to byte boundary, bit=1 means the source
    pixel was black (drawn/lit on the OLED)."""
    w, h = img.size
    row_bytes = (w + 7) // 8
    data = bytearray(row_bytes * h)
    px = img.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == 0:
                data[y * row_bytes + (x // 8)] |= 1 << (x % 8)
    return bytes(data)


def prepare_frame_gray(src: Image.Image, size: int, y_offset: int = 0) -> Image.Image:
    """Resize (keeping aspect ratio) onto a size x size white canvas, offset
    vertically by y_offset px. Returns the grayscale composite, before
    thresholding to 1-bit.

    A thin dark outline is drawn around the artwork's silhouette (from its
    alpha channel) before compositing, so icons whose ink color happens to
    be close to white (e.g. a white game controller) still leave a visible
    silhouette on a 1-bit display instead of disappearing into the white
    background."""
    frame = src.convert("RGBA")
    ratio = min(size / frame.width, size / frame.height)
    new_w = max(1, round(frame.width * ratio))
    new_h = max(1, round(frame.height * ratio))
    resized = frame.resize((new_w, new_h), Image.LANCZOS)
    x = (size - new_w) // 2
    y = (size - new_h) // 2 + y_offset

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    layer.paste(resized, (x, y), resized)
    alpha = layer.split()[-1]
    dilated = alpha.filter(ImageFilter.MaxFilter(5))
    ring = np.clip(np.array(dilated, dtype=np.int16) - np.array(alpha, dtype=np.int16), 0, 255).astype(np.uint8)

    canvas_rgba = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    if ring.any():
        outline = Image.new("RGBA", (size, size), (0, 0, 0, 255))
        canvas_rgba.paste(outline, (0, 0), Image.fromarray(ring, mode="L"))
    canvas_rgba.alpha_composite(layer)
    return canvas_rgba.convert("L")


def prepare_frame(src: Image.Image, size: int, threshold: int, invert: bool, y_offset: int = 0) -> Image.Image:
    """Resize+offset (see prepare_frame_gray), then threshold to 1-bit."""
    gray = prepare_frame_gray(src, size, y_offset)
    bw = gray.point(lambda p: 255 if p >= threshold else 0, mode="L").convert("1")
    if invert:
        bw = bw.point(lambda p: 255 - p)
    return bw


def format_c_array(data: bytes) -> str:
    lines = []
    for i in range(0, len(data), 12):
        chunk = data[i:i + 12]
        lines.append("    " + ", ".join(f"0x{b:02x}" for b in chunk) + ",")
    return "\n".join(lines)


def build_frames(entry: dict) -> list:
    source = REPO_ROOT / entry["source"]
    size = int(entry.get("size", 32))
    invert = bool(entry.get("invert", False))
    img = Image.open(source)

    threshold = entry.get("threshold", "auto")
    if threshold == "auto":
        # Compute once from the neutral (no y-offset) frame and reuse it for
        # every frame of this icon, so a bounce animation doesn't flicker
        # between different ink coverages frame to frame.
        base_gray = prepare_frame_gray(img, size)
        threshold = auto_threshold(base_gray)
    else:
        threshold = int(threshold)

    frames_bw = []
    if getattr(img, "is_animated", False):
        for page in ImageSequence.Iterator(img):
            frames_bw.append(prepare_frame(page, size, threshold, invert))
    elif entry.get("synthBounceFrames"):
        n = int(entry["synthBounceFrames"])
        amp = int(entry.get("synthBounceAmplitude", 3))
        for i in range(n):
            # simple up/down bounce derived from one static image, so the
            # animation pipeline can be tested/shipped before real
            # per-console frame art exists
            phase = (2 * abs((i % n) - (n - 1) / 2)) / (n - 1) if n > 1 else 0
            offset = round(-amp + phase * 2 * amp)
            frames_bw.append(prepare_frame(img, size, threshold, invert, y_offset=offset))
    else:
        frames_bw.append(prepare_frame(img, size, threshold, invert))

    return frames_bw, size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    args = ap.parse_args()

    manifest_path = Path(args.manifest)
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))

    cpp_parts = [
        "// GENERATED by scripts/make_icon_animation.py from",
        f"// {manifest_path.relative_to(REPO_ROOT)} -- do not hand-edit, edit the",
        "// manifest and rerun the script instead.",
        '#include "OLEDIconAnimations.h"',
        "",
    ]
    table_rows = []

    for entry in entries:
        icon_id = int(entry["iconId"])
        name = entry["name"]
        frames_bw, size = build_frames(entry)

        frame_var_names = []
        for i, frame in enumerate(frames_bw):
            var = f"icon_{name}_frame{i}"
            frame_var_names.append(var)
            xbm_bytes = to_xbm_bytes(frame)
            cpp_parts.append(f"static const uint8_t {var}[] PROGMEM = {{")
            cpp_parts.append(format_c_array(xbm_bytes))
            cpp_parts.append("};")
        frames_array_var = f"icon_{name}_frames"
        cpp_parts.append(f"static const uint8_t *const {frames_array_var}[] = {{{', '.join(frame_var_names)}}};")
        cpp_parts.append("")

        table_rows.append(
            f"    {{ {icon_id}, {len(frame_var_names)}, {size}, {size}, {frames_array_var} }},"
        )
        print(f"OK: {name} (icon {icon_id}), {len(frame_var_names)} quadro(s) {size}x{size}")

    cpp_parts.append("const IconAnimation ICON_ANIMATIONS[] = {")
    cpp_parts.extend(table_rows)
    cpp_parts.append("};")
    cpp_parts.append("const uint8_t ICON_ANIMATIONS_COUNT = sizeof(ICON_ANIMATIONS) / sizeof(ICON_ANIMATIONS[0]);")
    cpp_parts.append("")
    cpp_parts.append("const IconAnimation *findIconAnimation(uint8_t iconId)")
    cpp_parts.append("{")
    cpp_parts.append("    for (uint8_t i = 0; i < ICON_ANIMATIONS_COUNT; ++i) {")
    cpp_parts.append("        if (ICON_ANIMATIONS[i].iconId == iconId) {")
    cpp_parts.append("            return &ICON_ANIMATIONS[i];")
    cpp_parts.append("        }")
    cpp_parts.append("    }")
    cpp_parts.append("    return nullptr;")
    cpp_parts.append("}")
    cpp_parts.append("")

    OUTPUT_CPP.write_text("\n".join(cpp_parts), encoding="utf-8")
    print(f"OK: {OUTPUT_CPP.relative_to(REPO_ROOT)} gerado com {len(entries)} icone(s)")


if __name__ == "__main__":
    main()
