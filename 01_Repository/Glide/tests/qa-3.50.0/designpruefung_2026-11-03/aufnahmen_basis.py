"""Gemeinsamer Lader der Aufnahmewerkzeuge: app.pyw mit isoliertem GLIDE_DATA_DIR (nie echte Daten)."""
import os, sys, tempfile, importlib.machinery, importlib.util, subprocess, pathlib, traceback
# Repository-Wurzel aus der Lage dieser Datei; GLIDE_REPO überschreibt (andere Prüfkopie).
REPO = (pathlib.Path(os.environ['GLIDE_REPO']) / '01_Repository/Glide') if os.environ.get('GLIDE_REPO') else pathlib.Path(__file__).resolve().parents[3]
APP = REPO/'src/glide/app.pyw'
SHOWCASE = REPO/'tests/fixtures/showcase/Glide-Showcase_App.glideapp'
def load(tmp):
    os.environ['GLIDE_DATA_DIR'] = str(pathlib.Path(tmp)/'Glide')
    os.environ['GLIDE_TEST_MODE'] = '1'
    sys.path.insert(0, str(APP.parent))
    loader = importlib.machinery.SourceFileLoader('glide_app', str(APP))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules['glide_app'] = mod
    loader.exec_module(mod)
    return mod
