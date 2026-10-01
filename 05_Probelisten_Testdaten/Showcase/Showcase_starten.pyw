#!/usr/bin/env python3
"""Öffnet die geprüfte Demo in ihrem eigenen, dauerhaft bearbeitbaren Bestand."""
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import re
import sys


def main():
    here = Path(__file__).resolve().parent
    base = next((p for p in here.parents if (p/"01_Repository/Glide/VERSION").is_file()), None)
    if base is None:
        raise SystemExit("Die Glide-Projektablage wurde nicht gefunden. Den Starter in der Ablage belassen.")
    version = (base/"01_Repository/Glide/VERSION").read_text().strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit("Ungültige Glide-Version in der Projektablage.")
    runtime = base/"07_Python-Versionen"/f"Glide-Aufgaben-und-Listen_v{version}.pyw"
    if not runtime.is_file():
        raise SystemExit(f"Die abgeglichene Glide-Fassung {version} fehlt in 07_Python-Versionen.")
    backup = here/"Glide-Showcase_App.glideapp"
    if not backup.is_file():
        raise SystemExit("Glide-Showcase_App.glideapp fehlt neben dem Starter.")
    data = here/"Arbeitsstand"
    first_start = not (data/"liste_speicher.json").exists()
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
    app = mod.ListApp(root)
    if first_start:
        restored = app.restore_app_backup(str(backup), sections={
            "tasks":True, "settings":True, "templates":True, "activity":True}, show_success=False)
        if not restored:
            app.show_error("Showcase", "Die Basis konnte nicht geladen werden. Den getrennten Arbeitsstand prüfen.")
            root.destroy()
            return 1
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
