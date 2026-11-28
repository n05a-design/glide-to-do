# SPDX-License-Identifier: MPL-2.0
"""Dauerhafte Eingabeentwürfe der Inline-Erfassung, ohne Tk (Teil 05).

Entwürfe sind keine Aufgaben: Sie liegen in einer eigenen lokalen Datei
neben den Einstellungen, nie in der Speicherdatei. Ein Entwurf gehört genau
einem Ziel (Speicherdatei, Listen-ID). Leere Texte werden nicht gespeichert;
verworfene und übernommene Entwürfe werden entfernt. Der Schreibweg ist
atomar (temporäre Datei im selben Ordner, fsync, os.replace); eine kaputte
oder fremde Datei wird nie überschrieben, sondern beiseitegelegt.
"""
import json
import os
import time

import local_json_store

FORMAT = "glide-input-drafts"
VERSION = 1
FILE_NAME = "input_drafts.json"
MAX_TEXT = 4000
MAX_DRAFTS = 200
MAX_BYTES = 2 * 1024 * 1024


def _valid_key(save_file, list_id):
    return isinstance(save_file, str) and save_file and isinstance(list_id, str) and list_id


class DraftStore:
    """Lädt tolerant, schreibt nur bei Änderung und nur vollständig."""

    def __init__(self, path, clock=time.time):
        self.path = os.fspath(path)
        self._clock = clock
        self._drafts = {}
        self._dirty = False
        self.load_problem = None
        self._load()

    def _load(self):
        try:
            size = os.path.getsize(self.path)
        except OSError:
            return
        try:
            if size > MAX_BYTES:
                raise ValueError("zu groß")
            with open(self.path, "r", encoding="utf-8") as source:
                payload = json.load(source)
            if not isinstance(payload, dict) or payload.get("format") != FORMAT:
                raise ValueError("fremdes Format")
            version = payload.get("version")
            if type(version) is not int or version < 1:
                raise ValueError("ungültige Version")
            if version > VERSION:
                # Neuere Entwurfsdatei: lesen, was verständlich ist, aber nicht
                # überschreiben, damit die neuere Glide-Fassung nichts verliert.
                self.load_problem = "newer"
            for entry in payload.get("drafts", ())[:MAX_DRAFTS]:
                if not isinstance(entry, dict):
                    continue
                key = (entry.get("save_file"), entry.get("list_id"))
                text = entry.get("text")
                updated = entry.get("updated")
                if not isinstance(updated, (int, float)) or isinstance(updated, bool):
                    updated = 0.0
                if _valid_key(*key) and isinstance(text, str) and text.strip():
                    self._drafts[key] = (text[:MAX_TEXT], float(updated))
        except (OSError, ValueError, TypeError, UnicodeDecodeError) as exc:
            self._drafts = {}
            self.load_problem = f"unreadable: {exc}"
            self._quarantine()

    def _quarantine(self):
        stamp = time.strftime("%Y%m%d_%H%M%S")
        try:
            os.replace(self.path, f"{self.path}.unlesbar_{stamp}")
        except OSError:
            pass

    @property
    def writable(self):
        return self.load_problem != "newer"

    def get(self, save_file, list_id):
        entry = self._drafts.get((save_file, list_id))
        return entry[0] if entry else ""

    def items(self):
        return {key: value[0] for key, value in self._drafts.items()}

    def set(self, save_file, list_id, text):
        if not _valid_key(save_file, list_id):
            return
        key = (save_file, list_id)
        if not isinstance(text, str) or not text.strip():
            self.discard(save_file, list_id)
            return
        text = text[:MAX_TEXT]
        if self._drafts.get(key, (None,))[0] == text:
            return
        self._drafts[key] = (text, self._clock())
        if len(self._drafts) > MAX_DRAFTS:
            oldest = sorted(self._drafts, key=lambda k: self._drafts[k][1])
            for stale in oldest[:len(self._drafts) - MAX_DRAFTS]:
                del self._drafts[stale]
        self._dirty = True

    def discard(self, save_file, list_id):
        if self._drafts.pop((save_file, list_id), None) is not None:
            self._dirty = True

    def prune(self, save_file, existing_list_ids):
        """Entwürfe gelöschter Listen derselben Speicherdatei entfernen."""
        existing = set(existing_list_ids)
        for key in [k for k in self._drafts if k[0] == save_file and k[1] not in existing]:
            del self._drafts[key]
            self._dirty = True

    @property
    def dirty(self):
        return self._dirty

    def flush(self):
        """True bei Erfolg oder nichts zu tun; wirft OSError bei Schreibfehlern."""
        if not self._dirty:
            return True
        if not self.writable:
            return False
        payload = {"format": FORMAT, "version": VERSION, "drafts": [
            {"save_file": key[0], "list_id": key[1], "text": text, "updated": updated}
            for key, (text, updated) in sorted(self._drafts.items())]}
        local_json_store.write_atomic(self.path, payload)
        self._dirty = False
        return True
