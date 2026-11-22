#!/usr/bin/env python3
"""Öffnet die geprüfte Demo in ihrem eigenen, dauerhaft bearbeitbaren Bestand.

Opens the verified demo in its own, permanently editable data folder. Liegt der
Starter im Ordner `en`, startet die englische Fassung (meldet sich auf Englisch).
"""
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import re
import subprocess
import sys


def main():
    here = Path(__file__).resolve().parent
    englisch = here.name == "en"
    tx = (lambda de, en: en) if englisch else (lambda de, en: de)
    base = next((p for p in here.parents if (p/"01_Repository/Glide/VERSION").is_file()), None)
    if base is None:
        raise SystemExit(tx("Die Glide-Projektablage wurde nicht gefunden. Den Starter in der Ablage belassen.",
                             "The Glide project folder was not found. Keep the starter inside it."))
    version = (base/"01_Repository/Glide/VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(tx("Ungültige Glide-Version in der Projektablage.", "Invalid Glide version in the project folder."))
    runtime = base/"07_Python-Versionen"/f"Glide-Aufgaben-und-Listen_v{version}.pyw"
    if not runtime.is_file():
        raise SystemExit(tx(f"Die abgeglichene Glide-Fassung {version} fehlt in 07_Python-Versionen.",
                             f"The matching Glide version {version} is missing in 07_Python-Versionen."))
    backup = here/"Glide-Showcase_App.glideapp"
    if not backup.is_file():
        raise SystemExit(tx("Glide-Showcase_App.glideapp fehlt neben dem Starter.",
                             "Glide-Showcase_App.glideapp is missing next to the starter."))
    data = here/tx("Arbeitsstand-Stadtlicht", "Workspace-City-Light")
    restore_only = "--nur-wiederherstellen" in sys.argv[1:]
    first_start = not (data/"liste_speicher.json").exists()
    if first_start and not restore_only:
        # Die Sicherung trägt die Oberflächensprache. ListApp liest sie beim
        # Aufbau; deshalb stellt ein eigener Prozess zuerst den Bestand her
        # (ein zweites Tk() im selben Prozess ist unter macOS nicht stabil).
        lauf = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--nur-wiederherstellen"])
        if lauf.returncode:
            return lauf.returncode
        first_start = False
    os.environ["GLIDE_DATA_DIR"] = str(data)
    os.environ.pop("GLIDE_TEST_MODE", None)
    sys.path.insert(0, str(runtime.parent))
    loader = importlib.machinery.SourceFileLoader("glide_showcase_start", str(runtime))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    mod.set_windows_app_user_model_id()
    root = mod.tk.Tk()
    if restore_only:
        root.withdraw()
    app = mod.ListApp(root)
    if first_start:
        restored = app.restore_app_backup(str(backup), sections={
            "tasks":True, "settings":True, "templates":True, "activity":True}, show_success=False)
        if not restored:
            app.show_error("Showcase", tx("Die Basis konnte nicht geladen werden. Den getrennten Arbeitsstand prüfen.",
                                          "The base could not be loaded. Check the separate workspace."))
            root.destroy()
            return 1
    if restore_only:
        root.destroy()
        return 0
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
