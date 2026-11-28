# SPDX-License-Identifier: MPL-2.0
"""Eigene Symbole in Glide (Ecosystem E03), ohne Tk.

Begleitdatei `symbol_library.json` (Format `glide-symbol-library`, Version 1)
im Datenordner, geschrieben über `local_json_store` wie der KI-Arbeitsbereich:
Eine unlesbare oder neuere Datei bleibt unverändert und schreibgeschützt.
Das Aufgabenformat ändert sich nicht: Ein gewähltes Symbol wird wie bisher als
16-×-16-Pixeldokument in das `icon`-Feld einer Liste oder eines Ordners
kopiert. Löschen eines Symbols aus der Bibliothek ändert deshalb keine Seite;
`references` nennt die Seiten, die dasselbe Bild tragen.

Importierte PNG- und SVG-Dateien werden nicht gespeichert, nur das daraus
erzeugte Pixeldokument, die Prüfsumme der Quelle und ihr Typ. Die Begleitdatei
gehört zur vollständigen App-Sicherung (Abschnitt `symbol_library`).
"""
from __future__ import annotations

import hashlib
import time
import uuid

import local_json_store

FORMAT = "glide-symbol-library"
VERSION = 1
FILE_NAME = "symbol_library.json"
MAX_SYMBOLS = 2000
MAX_LABEL = 60
CATEGORY_DEFAULT = "Eigene Symbole"


def icon_key(icon):
    """Inhaltsschlüssel eines Pixeldokuments (gleiches Bild ⇒ gleicher Schlüssel)."""
    if not isinstance(icon, dict):
        return None
    rows = "".join(icon.get("rows") or [])
    palette = "".join(icon.get("palette") or [])
    return hashlib.sha256((rows + "|" + palette).encode("utf-8")).hexdigest()


class Library:
    def __init__(self, payload=None):
        payload = payload if isinstance(payload, dict) else {}
        self.symbols = {}
        for sid, eintrag in (payload.get("symbols") or {}).items():
            if isinstance(sid, str) and isinstance(eintrag, dict) and isinstance(eintrag.get("icon"), dict):
                self.symbols[sid] = eintrag
        zustand = payload.get("state") if isinstance(payload.get("state"), dict) else {}
        self.favorites = [i for i in zustand.get("favorites") or [] if isinstance(i, str)]
        self.recent = [i for i in zustand.get("recent") or [] if isinstance(i, str)][:24]

    def to_payload(self):
        return {"format": FORMAT, "version": VERSION, "symbols": self.symbols,
                "state": {"favorites": self.favorites, "recent": self.recent}}

    def add(self, label, icon, source_kind, source_sha256=None, category=CATEGORY_DEFAULT):
        """Neues Symbol; ein bereits vorhandenes gleiches Bild wird nicht doppelt angelegt."""
        if len(self.symbols) >= MAX_SYMBOLS:
            raise ValueError("Symbolbibliothek ist voll")
        schluessel = icon_key(icon)
        for sid, eintrag in self.symbols.items():
            if icon_key(eintrag["icon"]) == schluessel:
                return sid, False
        sid = uuid.uuid4().hex
        self.symbols[sid] = {"label": (str(label).strip() or "Symbol")[:MAX_LABEL], "category": (str(category).strip() or CATEGORY_DEFAULT)[:MAX_LABEL],
                             "icon": icon, "source_kind": source_kind, "source_sha256": source_sha256,
                             "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        return sid, True

    def rename(self, sid, label=None, category=None):
        eintrag = self.symbols[sid]
        if label is not None and str(label).strip():
            eintrag["label"] = str(label).strip()[:MAX_LABEL]
        if category is not None and str(category).strip():
            eintrag["category"] = str(category).strip()[:MAX_LABEL]

    def remove(self, sid):
        self.symbols.pop(sid, None)
        for liste in (self.favorites, self.recent):
            while sid in liste:
                liste.remove(sid)

    def references(self, sid, holders):
        """Listen/Ordner, deren Symbol dasselbe Bild zeigt (Kopie, keine Verknüpfung)."""
        schluessel = icon_key(self.symbols.get(sid, {}).get("icon"))
        return [h for h in holders if isinstance(h, dict) and schluessel and icon_key(h.get("icon")) == schluessel]

    def problems(self):
        """Integritätsbefunde: fehlerhafte Einträge, verwaiste Favoriten."""
        befunde = [f"{sid}: ohne Zeilen" for sid, e in self.symbols.items() if not (e.get("icon") or {}).get("rows")]
        befunde += [f"Favorit {sid} fehlt" for sid in self.favorites if sid not in self.symbols]
        return befunde


def load(path):
    zustand = local_json_store.read(path, FORMAT, VERSION, quarantine=False)
    return Library(zustand.payload), zustand


def save(path, library):
    local_json_store.write_atomic(path, library.to_payload())
