from __future__ import annotations

import re
import sys
from pathlib import Path

from pypdf import PdfReader


reader = PdfReader(str(Path(sys.argv[1])))
pattern = re.compile(r"(?i)(?:v?\d+\.\d+(?:\.\d+)?|datenformat(?:-version)?\s*:?\s*\d+|dokumentversion\s*\d+(?:\.\d+)+)")
for page_number, page in enumerate(reader.pages, 1):
    text = re.sub(r"\s+", " ", page.extract_text() or "").strip()
    for match in pattern.finditer(text):
        start = max(0, match.start() - 90)
        end = min(len(text), match.end() + 120)
        print(f"Seite {page_number}: {text[start:end]}")
