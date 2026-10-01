from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw


source = Path(sys.argv[1])
output = Path(sys.argv[2])
output.mkdir(parents=True, exist_ok=True)
paths = sorted(source.glob("page-*.png"))


def make_sheet(kind: str, crop_height: int) -> None:
    width = 800
    label_width = 90
    scale = (width - label_width) / 1600
    strip_h = round(crop_height * scale)
    gap = 8
    sheet = Image.new("RGB", (width, len(paths) * (strip_h + gap) + gap), "#d0d0d0")
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(paths, 1):
        with Image.open(path) as page:
            page = page.convert("RGB")
            if kind == "top":
                strip = page.crop((0, 0, page.width, crop_height))
            else:
                strip = page.crop((0, page.height - crop_height, page.width, page.height))
            strip = strip.resize((width - label_width, strip_h), Image.Resampling.LANCZOS)
        y = gap + (i - 1) * (strip_h + gap)
        draw.text((8, y + 5), f"Seite {i}", fill="black")
        sheet.paste(strip, (label_width, y))
    sheet.save(output / f"{kind}-strips.png", optimize=True)


make_sheet("top", 220)
make_sheet("bottom", 180)
