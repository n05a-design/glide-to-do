from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageOps


PDF = Path(sys.argv[1])
ORIGINAL_DIR = Path(sys.argv[2])
OUT_DIR = Path(sys.argv[3])
OUT_DIR.mkdir(parents=True, exist_ok=True)

doc = pdfium.PdfDocument(PDF)
comparisons = []
hi_paths: list[Path] = []

for index in range(len(doc)):
    number = index + 1
    page = doc[index]
    width_pt, height_pt = page.get_size()

    original_path = ORIGINAL_DIR / f"page-{number:02d}.png"
    with Image.open(original_path) as original_image:
        original = original_image.convert("RGB")
        target_w, target_h = original.size

    exact_scale = target_w / width_pt
    exact = page.render(scale=exact_scale, rev_byteorder=True).to_pil().convert("RGB")
    if exact.size != (target_w, target_h):
        exact = exact.resize((target_w, target_h), Image.Resampling.LANCZOS)

    a = np.asarray(original.convert("L"), dtype=np.float32) / 255.0
    b = np.asarray(exact.convert("L"), dtype=np.float32) / 255.0
    mae = float(np.mean(np.abs(a - b)))
    corr = float(np.corrcoef(a.ravel(), b.ravel())[0, 1])
    foreground_a = a < 0.97
    foreground_b = b < 0.97
    intersection = int(np.logical_and(foreground_a, foreground_b).sum())
    union = int(np.logical_or(foreground_a, foreground_b).sum())
    iou = intersection / union if union else 1.0

    hi_scale = 1600 / width_pt
    high = page.render(scale=hi_scale, rev_byteorder=True).to_pil().convert("RGB")
    high_path = OUT_DIR / f"page-{number:02d}.png"
    high.save(high_path, optimize=True)
    hi_paths.append(high_path)

    comparisons.append(
        {
            "page": number,
            "pdf_points": [round(width_pt, 3), round(height_pt, 3)],
            "original_pixels": [target_w, target_h],
            "rerender_pixels": list(high.size),
            "grayscale_mae": round(mae, 6),
            "pixel_correlation": round(corr, 6),
            "foreground_iou": round(iou, 6),
        }
    )

thumb_w = 320
thumb_h = round(thumb_w * 1287 / 910)
gap = 20
label_h = 28
for sheet_index, start in enumerate(range(0, len(hi_paths), 6), 1):
    selected = hi_paths[start : start + 6]
    canvas = Image.new("RGB", (3 * thumb_w + 4 * gap, 2 * (thumb_h + label_h) + 3 * gap), "#d7d7d7")
    draw = ImageDraw.Draw(canvas)
    for slot, path in enumerate(selected):
        row, col = divmod(slot, 3)
        x = gap + col * (thumb_w + gap)
        y = gap + row * (thumb_h + label_h + gap)
        with Image.open(path) as image:
            thumb = ImageOps.contain(image.convert("RGB"), (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x, y + label_h))
        draw.text((x + 4, y + 4), f"Seite {start + slot + 1}", fill="black")
    canvas.save(OUT_DIR / f"contact-{sheet_index}.png", optimize=True)

print(
    json.dumps(
        {
            "pdf_pages": len(doc),
            "high_resolution_output": str(OUT_DIR),
            "comparisons": comparisons,
        },
        ensure_ascii=False,
        indent=2,
    )
)
