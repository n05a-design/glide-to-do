"""Paketierung (Vorstufe, 26.09.2026): Kennungen, Windows-Anmeldung, macOS-Entwicklungsbundle.

- Die Kennungen stehen genau einmal im Code (`APP_BUNDLE_ID`, `APP_USER_MODEL_ID`)
  und stimmen mit dem Produktregister überein.
- Das Windows-Skript liest die AppUserModelID aus app.pyw, statt sie zu
  wiederholen; außerhalb von Windows tut die Anmeldung nichts.
- Unter macOS baut `packaging/macos/baue_app.py` ein vollständiges Bundle mit
  gültiger Ad-hoc-Signatur. Gestartet wird es hier nicht: Ein Start gehört
  mit einem getrennten Datenordner in die Sichtprüfung.
"""
import importlib.machinery
import importlib.util
import os
import plistlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-paketierung-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_paketierung", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    assert mod.APP_BUNDLE_ID == "de.shaye.glide", mod.APP_BUNDLE_ID
    assert mod.APP_USER_MODEL_ID == "Shaye.Glide", mod.APP_USER_MODEL_ID
    register = (REPO / "docs/decisions/PRODUCT_IDENTITY.md").read_text(encoding="utf-8")
    assert "de.shaye.glide" in register and "Shaye.Glide" in register, "Produktregister nennt die Kennungen"
    if not mod.IS_WINDOWS:
        assert mod.set_windows_app_user_model_id() is False

    skript = (REPO / "packaging/windows/verknuepfung_anlegen.ps1").read_bytes()
    assert skript.startswith(b"\xef\xbb\xbf"), "PowerShell 5 braucht UTF-8 mit BOM"
    text = skript.decode("utf-8-sig")
    assert "\r\n" in text and "Shaye.Glide" not in text.split("param(")[1], "Kennung nur aus app.pyw lesen"
    muster = re.search(r"-Pattern '(.+?)'", text).group(1)
    quelle = (REPO / "src/glide/app.pyw").read_text(encoding="utf-8")
    treffer = re.search(muster, quelle, re.MULTILINE)
    assert treffer and treffer.group(1) == "Shaye.Glide", "Das Skript findet die Kennung in app.pyw"

    # Programmsymbole aus dem Logo-Master (packaging/baue_symbole.py).
    ico = (REPO / "assets/icons/glide.ico").read_bytes()
    assert ico[:4] == b"\x00\x00\x01\x00" and int.from_bytes(ico[4:6], "little") == 7, "sieben Größen im ICO"
    for name in ("glide_macos_1024.png", "glide_512.png"):
        assert (REPO / "assets/icons" / name).read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", name
    assert "assets\\icons\\glide.ico" in text, "Verknüpfung nimmt das Glide-Symbol"

    gebaut = "übersprungen (kein macOS)"
    if sys.platform == "darwin" and (Path(sys.base_prefix) / "Resources/Python.app").is_dir():
        ziel = Path(ordner) / "bundle"
        lauf = subprocess.run([sys.executable, str(REPO / "packaging/macos/baue_app.py"), "--ziel", str(ziel)],
                              capture_output=True, text=True, timeout=300)
        assert lauf.returncode == 0, lauf.stderr[-2000:]
        app = ziel / "Glide.app"
        with open(app / "Contents/Info.plist", "rb") as datei:
            info = plistlib.load(datei)
        assert info["CFBundleIdentifier"] == mod.APP_BUNDLE_ID
        assert info["CFBundleShortVersionString"] == mod.APP_VERSION
        for teil in ("MacOS/Glide", "MacOS/glide-python", "Resources/Glide.icns",
                     "Resources/glide/app.pyw", "Resources/glide/drawing.py",
                     "Resources/glide/drawing_image.py", "Resources/glide/backdrop.py",
                     "Resources/glide/glide_start.py", "Resources/glide/page_markdown.py",
                     "Resources/glide/image_preview.py", "Resources/glide/vendor/tkinterdnd2/__init__.py",
                     "Resources/glide/resources/fonts/PixelifySans-Regular.ttf",
                     # Seit 29.09.2026: Logo-Modul und Master für Kopfzeile und Symbol.
                     "Resources/glide/logo.py", "Resources/glide/resources/logo/glide-logo.svg",
                     "Resources/glide/resources/logo/glide-app-icon.svg"):
            assert (app / "Contents" / teil).exists(), teil
        assert not (app / "Contents/Resources/glide/resources/templates/archiv").exists(), "Archiv gehört nicht ins Paket"
        assert os.access(app / "Contents/MacOS/Glide", os.X_OK)
        # Das Programmsymbol ist das Glide-Symbol, kein Platzhalter mehr.
        assert (app / "Contents/Resources/Glide.icns").stat().st_size > 20000
        assert not (ziel / "Glide_Platzhaltersymbol.png").exists()
        pruefung = subprocess.run(["codesign", "--verify", "--deep", str(app)], capture_output=True, text=True)
        assert pruefung.returncode == 0, pruefung.stderr
        gebaut = f"Bundle gebaut und gültig signiert ({mod.APP_BUNDLE_ID})"

print(f"test_paketierung330: OK; Kennungen {mod.APP_BUNDLE_ID} / {mod.APP_USER_MODEL_ID}, Windows-Skript, {gebaut}.")
