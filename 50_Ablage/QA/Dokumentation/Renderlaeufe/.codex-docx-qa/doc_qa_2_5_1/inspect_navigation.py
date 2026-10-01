from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


path = Path(sys.argv[1])
ns = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}
with zipfile.ZipFile(path) as zf:
    document = ET.fromstring(zf.read("word/document.xml"))
    rels_root = ET.fromstring(zf.read("word/_rels/document.xml.rels"))

rels = {}
for rel in rels_root.findall("pr:Relationship", ns):
    rels[rel.attrib["Id"]] = {
        "target": rel.attrib.get("Target"),
        "mode": rel.attrib.get("TargetMode"),
        "type": rel.attrib.get("Type", "").rsplit("/", 1)[-1],
    }

hyperlinks = []
for h in document.findall(".//w:hyperlink", ns):
    text = "".join(t.text or "" for t in h.findall(".//w:t", ns))
    rid = h.attrib.get(f"{{{ns['r']}}}id")
    hyperlinks.append(
        {
            "text": text,
            "anchor": h.attrib.get(f"{{{ns['w']}}}anchor"),
            "relationship": rels.get(rid) if rid else None,
        }
    )

bookmarks = [
    {
        "name": b.attrib.get(f"{{{ns['w']}}}name"),
        "id": b.attrib.get(f"{{{ns['w']}}}id"),
    }
    for b in document.findall(".//w:bookmarkStart", ns)
]

fields = []
for instr in document.findall(".//w:instrText", ns):
    if instr.text and instr.text.strip():
        fields.append(instr.text.strip())

print(json.dumps({"hyperlinks": hyperlinks, "bookmarks": bookmarks, "fields": fields}, ensure_ascii=False, indent=2))
