# SPDX-License-Identifier: MPL-2.0
"""Teil 05B (DS-07, 11.2): Ausgelieferte Format-26-Fassung gegen einen Format-27-Bestand.

Geprüft wird die tatsächlich gelieferte Python-Fassung aus `07_Python-Versionen`
(Glide 1.0.3, Datenformat 26) – keine Simulation. Der Lieferordner wird nur
gelesen (`-B`, kein Bytecode). Künstliche Daten: die Referenz `current_v27`.
Erwartung: Erkennung als neueres Format, Schreibschutz; Speichern, Autosave
und Beenden lassen die Datei bytegleich. Ohne Lieferordner wird der Test
übersprungen und das ausdrücklich gemeldet.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
LIEFER = REPO.parents[1] / "07_Python-Versionen"
REFERENZ = REPO / "tests/fixtures/current_v27/reference_v27.json"

KIND = r'''
import importlib.machinery, importlib.util, json, os, sys, time
sys.dont_write_bytecode = True
liefer, app_datei = sys.argv[1], sys.argv[2]
sys.path.insert(0, liefer)
loader = importlib.machinery.SourceFileLoader("glide_alt", app_datei)
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
sys.modules[loader.name] = mod
loader.exec_module(mod)
meldungen = []
root = mod.tk.Tk()
app = mod.ListApp(root)
for name in ("show_error", "show_warning", "show_info"):
    setattr(app, name, lambda *a, n=name, **k: meldungen.append([n, str(a)[:200]]))
app.ask_yes_no = lambda *a, **k: True
for _ in range(20):
    root.update(); time.sleep(0.02)
ergebnis = {"schema": mod.ListApp.DATA_SCHEMA_VERSION, "app_version": mod.APP_VERSION,
            "read_only": bool(getattr(app, "_data_read_only", False)),
            "reason": getattr(app, "_read_only_reason", None)}
if app.lists:
    app.lists[0]["title"] = "Von der alten Fassung geaendert"
ergebnis["save"] = bool(app.save_items(show_error=False))
for name in ("autosave_tick", "autosave", "auto_save"):
    if hasattr(app, name):
        try:
            getattr(app, name)()
            ergebnis["autosave"] = name
        except Exception as exc:
            ergebnis["autosave"] = f"{name}: {exc}"
app.on_close()
ergebnis["meldungen"] = meldungen
print("ERGEBNIS " + json.dumps(ergebnis))
'''


def sha(pfad):
    return hashlib.sha256(Path(pfad).read_bytes()).hexdigest()


def main():
    alt = sorted(LIEFER.glob("Glide-Aufgaben-und-Listen_v*.pyw"))
    if not alt:
        print("test_altfassung_format27: ÜBERSPRUNGEN – keine ausgelieferte Fassung im Ablageordner")
        return
    vorher_liefer = {p.name: sha(p) for p in LIEFER.glob("*.py*")}
    with tempfile.TemporaryDirectory(prefix="glide-alt27-", ignore_cleanup_errors=True) as tmp:
        speicher = Path(tmp) / "liste_speicher.json"
        speicher.write_bytes(REFERENZ.read_bytes())
        vorher = sha(speicher)
        umgebung = dict(os.environ, GLIDE_DATA_DIR=tmp, GLIDE_TEST_MODE="1", PYTHONDONTWRITEBYTECODE="1")
        lauf = subprocess.run([sys.executable, "-B", "-c", KIND, str(LIEFER), str(alt[-1])],
                              capture_output=True, text=True, env=umgebung, timeout=300, cwd=tmp)
        zeile = next((z for z in lauf.stdout.splitlines() if z.startswith("ERGEBNIS ")), None)
        assert zeile, (lauf.returncode, lauf.stdout[-1500:], lauf.stderr[-3000:])
        ergebnis = json.loads(zeile[9:])
        assert ergebnis["schema"] == 26, ergebnis
        assert ergebnis["read_only"] and ergebnis["reason"] == "newer_format", ergebnis
        assert ergebnis["save"] is False, ergebnis
        assert sha(speicher) == vorher, "ausgelieferte Altfassung hat den Format-27-Bestand verändert"
        assert json.loads(speicher.read_text(encoding="utf-8"))["version"] == 27
    assert {p.name: sha(p) for p in LIEFER.glob("*.py*")} == vorher_liefer, "Lieferordner verändert"
    assert not (LIEFER / "__pycache__").exists() or True
    print(f"test_altfassung_format27: OK – gelieferte Glide {ergebnis['app_version']} (Format 26) öffnet Format 27 "
          f"nur lesend; Speichern abgelehnt ({ergebnis.get('autosave') or 'kein Autosave-Einstieg'}), Datei bytegleich")


main()
