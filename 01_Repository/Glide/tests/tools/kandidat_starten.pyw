#!/usr/bin/env python3
"""Öffnet den Quellstand (`src/glide`) mit dem Showcase in einem eigenen Prüfordner.

Für Sicht- und Bedienabnahmen eines noch nicht gelieferten Kandidaten (seit
25.10.2026, D55). Der Showcase-Starter in `05_Probelisten_Testdaten` nimmt die
gelieferte Fassung aus `07_Python-Versionen`; dieser Starter nimmt
`01_Repository/Glide/src/glide/app.pyw`.

Daten: `<Benutzerordner>/GlidePruefung/kandidat_showcase` – außerhalb des
Projektordners und damit außerhalb von OneDrive, getrennt von den echten Daten
(`GLIDE_DATA_DIR`). Beim ersten Start lädt er das Showcase-App-Backup; weitere
Starts behalten den Prüfstand. `--neu` (aus einer Konsole) beginnt mit frischem
Showcase; der alte Prüfordner wird dabei umbenannt, nicht gelöscht.
"""
import importlib.machinery
import importlib.util
import os
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ABLAGE = REPO.parents[1]


def pruefordner(heim=None):
    return Path(heim or Path.home()) / "GlidePruefung" / "kandidat_showcase"


def showcase_backup(ablage=ABLAGE, repo=REPO):
    """Aktiver Showcase, sonst die Fixture im Quellbaum."""
    for pfad in (ablage / "05_Probelisten_Testdaten/Showcase/Glide-Showcase_App.glideapp",
                 repo / "tests/fixtures/showcase/Glide-Showcase_App.glideapp"):
        if pfad.is_file():
            return pfad
    return None


def neu_beginnen(ordner, jetzt=None):
    """Bestehenden Prüfordner beiseitelegen; liefert den neuen Namen oder None."""
    if not ordner.exists():
        return None
    ziel = ordner.with_name(ordner.name + "_" + (jetzt or datetime.now()).strftime("%Y%m%d-%H%M%S"))
    ordner.rename(ziel)
    return ziel


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    app_pfad = REPO / "src/glide/app.pyw"
    backup = showcase_backup()
    if not app_pfad.is_file() or backup is None:
        raise SystemExit("Quellstand oder Showcase fehlt; den Starter im Projektordner belassen.")
    daten = pruefordner()
    if "--neu" in argv:
        neu_beginnen(daten)
    daten.mkdir(parents=True, exist_ok=True)
    erster_start = not (daten / "liste_speicher.json").exists()
    os.environ["GLIDE_DATA_DIR"] = str(daten)
    os.environ.pop("GLIDE_TEST_MODE", None)
    sys.path.insert(0, str(app_pfad.parent))
    loader = importlib.machinery.SourceFileLoader("glide_kandidat_start", str(app_pfad))
    modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = modul
    loader.exec_module(modul)
    modul.set_windows_app_user_model_id()
    root = modul.tk.Tk()
    app = modul.ListApp(root)
    if erster_start:
        geladen = app.restore_app_backup(str(backup), sections={
            "tasks": True, "settings": True, "templates": True, "activity": True}, show_success=False)
        if not geladen:
            app.show_error("Prüfstand", "Der Showcase konnte nicht geladen werden.")
            root.destroy()
            return 1
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
