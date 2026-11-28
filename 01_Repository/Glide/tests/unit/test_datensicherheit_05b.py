# SPDX-License-Identifier: MPL-2.0
"""Teil 05B ohne Tk: Anhangsintegrität, Begleitdateien, Lesepositionen, Sperre, Statusdatei."""
import datetime as dt
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src" / "glide"))

import attachment_integrity
import chapters
import data_lock
import data_safety
import local_json_store
import view_positions


def gueltig(storage):
    if not isinstance(storage, str) or not storage.startswith("attachments/") or ".." in storage or "/" in storage[12:]:
        raise ValueError("ungültig")
    return storage


class Anhangsintegritaet(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        (self.dir / "attachments").mkdir()
        (self.dir / "attachments" / "a.bin").write_bytes(b"x" * 10)
        (self.dir / "attachments" / "leer.bin").write_bytes(b"")
        (self.dir / "attachments" / "waise.bin").write_bytes(b"y")

    def tearDown(self):
        self.tmp.cleanup()

    def test_befunde_ohne_aenderung(self):
        refs = [("Liste", {"storage": "attachments/a.bin"}), ("Aufgabe", {"storage": "attachments/a.bin"}),
                ("Seite", {"storage": "attachments/fehlt.bin"}), ("Notiz", {"storage": "attachments/leer.bin"}),
                ("Böse", {"storage": "attachments/../settings.json"}), ("Kaputt", "kein dict")]
        vorher = sorted(os.listdir(self.dir / "attachments"))
        bericht = attachment_integrity.check(refs, str(self.dir), gueltig)
        self.assertEqual(sorted(os.listdir(self.dir / "attachments")), vorher, "Prüfung darf nichts löschen")
        self.assertEqual([m["storage"] for m in bericht.missing], ["attachments/fehlt.bin"])
        self.assertEqual([m["storage"] for m in bericht.empty], ["attachments/leer.bin"])
        self.assertEqual(len(bericht.invalid), 2)
        self.assertEqual(bericht.shared, {"attachments/a.bin": 2})
        self.assertEqual(bericht.unreferenced, ["attachments/waise.bin"])
        self.assertEqual((bericht.files, bericht.bytes), (3, 11))
        self.assertFalse(bericht.ok)
        self.assertTrue(json.dumps(bericht.as_dict()))

    def test_sauberer_bestand(self):
        bericht = attachment_integrity.check([("L", {"storage": "attachments/a.bin"})], str(self.dir), gueltig)
        self.assertTrue(bericht.ok)


class Begleitdateien(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "x.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rundlauf_neuer_und_kaputt(self):
        local_json_store.write_atomic(self.path, {"format": "f", "version": 1, "a": 1})
        self.assertEqual(local_json_store.read(self.path, "f", 1).payload["a"], 1)
        local_json_store.write_atomic(self.path, {"format": "f", "version": 2})
        self.assertFalse(local_json_store.read(self.path, "f", 1).writable)
        Path(self.path).write_text("{", encoding="utf-8")
        zustand = local_json_store.read(self.path, "f", 1)
        self.assertIsNone(zustand.payload)
        self.assertFalse(os.path.exists(self.path))

    def test_abbruch_erhaelt_vorherigen_stand(self):
        local_json_store.write_atomic(self.path, {"format": "f", "version": 1, "a": 1})
        with mock.patch("local_json_store.os.replace", side_effect=OSError("Abbruch")):
            with self.assertRaises(OSError):
                local_json_store.write_atomic(self.path, {"format": "f", "version": 1, "a": 2})
        self.assertEqual(json.loads(Path(self.path).read_text(encoding="utf-8"))["a"], 1)
        self.assertEqual([n for n in os.listdir(self.tmp.name) if n.endswith(".tmp")], [])


class Lesepositionen(unittest.TestCase):
    A, B = "a" * 32, "b" * 32

    def doc(self, vorspann=""):
        text = vorspann + "Eins\nText eins\nZwei\nText zwei lang\n"
        s = len(vorspann)
        d = {"text": text, "spans": [{"tag": "h1", "start": s, "end": s + 5}, {"tag": "h1", "start": s + 15, "end": s + 20}],
             "links": {}}
        ids = iter([self.A, self.B])
        return chapters.ensure_anchors(d, new_id=lambda: next(ids))[0]

    def test_anker_ueberlebt_eingefuegten_text_davor(self):
        kap = chapters.outline(self.doc())
        anker, abstand = view_positions.anchor_point(kap, 18)
        self.assertEqual((anker, abstand), (self.B, 3))
        neu = chapters.outline(self.doc(vorspann="Neuer Absatz\n\n"))
        self.assertEqual(view_positions.resolve_point(neu, anker, abstand, 18, 999), 14 + 15 + 3)

    def test_geloeschtes_kapitel_faellt_auf_versatz_zurueck(self):
        self.assertEqual(view_positions.resolve_point([], self.B, 3, 18, 10), 10)
        self.assertIsNone(view_positions.resolve_point([], None, None, "x", 10))

    def test_datei_rundlauf_trennt_speicherdateien(self):
        p = view_positions.ViewPositions()
        p.remember(("page", "S1"), top=5, anchor=self.A, anchor_delta=2, bogus="weg")
        p.remember(("list", "L1", "list"), row="r1", fraction=0.4)
        nutzlast = view_positions.to_payload(p, "a.json", {"entries": [{"save_file": "b.json", "key": ["page", "X"], "position": {"top": 1}}]})
        q = view_positions.ViewPositions()
        view_positions.load_payload(q, nutzlast, "a.json")
        self.assertEqual(q.recall(("page", "S1")), {"top": 5, "anchor": self.A, "anchor_delta": 2})
        self.assertEqual(q.recall(("list", "L1", "list")), {"row": "r1", "fraction": 0.4})
        self.assertIsNone(q.recall(("page", "X")))
        self.assertTrue(any(e["save_file"] == "b.json" for e in nutzlast["entries"]))


class Sperre(unittest.TestCase):
    def test_veraltete_fremdsperre_ist_nicht_frei(self):
        jetzt = dt.datetime(2026, 11, 28, 12, tzinfo=dt.timezone.utc)
        alt = {"host": "ANDERER", "pid": 1, "token": "t", "started_at": "2026-11-20T08:00:00+00:00",
               "refreshed_at": "2026-11-20T08:00:00+00:00"}
        self.assertTrue(data_lock.stale_foreign(alt, host="HIER", now=jetzt, max_age_seconds=8 * 3600))
        frisch = dict(alt, refreshed_at="2026-11-28T11:59:00+00:00")
        self.assertFalse(data_lock.stale_foreign(frisch, host="HIER", now=jetzt, max_age_seconds=8 * 3600))
        self.assertFalse(data_lock.stale_foreign(alt, host="ANDERER", now=jetzt, max_age_seconds=8 * 3600))
        self.assertIn("ANDERER", data_lock.stale_question("ANDERER", "gestern"))


class Statusdatei(unittest.TestCase):
    def test_ergebnisse_je_speicherdatei_und_schnellwerte(self):
        with tempfile.TemporaryDirectory() as tmp:
            pfad = os.path.join(tmp, data_safety.FILE_NAME)
            a = data_safety.StatusFile(pfad, "a.json")
            self.assertIsNone(a.get("integrity"))
            a.record("integrity", {"ok": True})
            self.assertTrue(data_safety.StatusFile(pfad, "a.json").get("integrity")["ok"])
            self.assertIsNone(data_safety.StatusFile(pfad, "b.json").get("integrity"))
            Path(tmp, "s.glideapp").write_bytes(b"12345")
            Path(tmp, "liste_backup_1.json").write_bytes(b"1")
            snap = data_safety.snapshot(base_dir=tmp, save_file=os.path.join(tmp, "fehlt.json"), backup_dir=tmp,
                                        attachments_dir=os.path.join(tmp, "attachments"), schema_version=27,
                                        dirty=False, read_only_reason=None, lock_held=True)
            self.assertEqual(snap["full_backups"].count, 1)
            self.assertEqual(snap["data"].newest, None)
            self.assertEqual(data_safety.human_bytes(2048), "2.0 KB")


if __name__ == "__main__":
    unittest.main()
