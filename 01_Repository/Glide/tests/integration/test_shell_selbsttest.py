# SPDX-License-Identifier: MPL-2.0
"""Selbsttest der Glide Shell (Shell-Paket 11): läuft aus einer Kopie und erkennt eine kaputte Kopie.

Der Test kopiert `src/glide/glide_shell` in ein leeres Temporärverzeichnis und
startet dort `python -m glide_shell.selftest` in eigenem Prozess:
- vollständige Kopie: Exitcode 0, jede Prüfung `ok`, Zusammenfassung „13/13“;
- Gegenprobe mit verändertem `window_geometry.parse`: Exitcode 1 und genau
  diese Prüfung `FAIL`, die übrigen bleiben `ok` – auch unter `python -O`;
- Übernahme mit `scripts/pflege/shell_uebernehmen.py`: die Prüfung `manifest`
  bestätigt die Kopie; eine nachträglich veränderte Datei oder ein zusätzliches
  Modul macht genau `manifest` rot (Prüfung der Kopie ohne Glide-Checkout).

Aufruf: python3 -B tests/integration/test_shell_selbsttest.py
"""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
PAKET = REPO / "src" / "glide" / "glide_shell"
WERKZEUG = REPO / "scripts" / "pflege" / "shell_uebernehmen.py"
ZEITLIMIT = 120


def lauf(ordner, *schalter):
    umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    umgebung.pop("PYTHONPATH", None)
    ergebnis = subprocess.run([sys.executable, "-B", *schalter, "-m", "glide_shell.selftest"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=umgebung, cwd=ordner, timeout=ZEITLIMIT)
    return ergebnis.returncode, ergebnis.stdout + ergebnis.stderr


def kopie(ziel):
    shutil.copytree(PAKET, pathlib.Path(ziel) / "glide_shell", ignore=shutil.ignore_patterns("__pycache__"))
    return pathlib.Path(ziel) / "glide_shell"


def uebernahme(ziel):
    subprocess.run([sys.executable, "-B", str(WERKZEUG), "--unsauber-erlauben", str(ziel)], check=True,
                   capture_output=True, timeout=ZEITLIMIT)
    return pathlib.Path(ziel) / "glide_shell"


def manifestfaelle(fehler):
    with tempfile.TemporaryDirectory(prefix="glide-shell-selbst-") as ordner:
        paket = uebernahme(ordner)
        code, text = lauf(ordner)
        if code != 0 or "ok   manifest:" not in text or "13/13 checks passed" not in text:
            fehler.append(f"übernommene Kopie: Exit {code}\n{text}")

        # Gegenprobe: manipulierte Datei
        datei = paket / "motion.py"
        datei.write_text(datei.read_text(encoding="utf-8") + "\n# manipuliert\n", encoding="utf-8")
        (paket / "fremd.py").write_text("x = 1\n", encoding="utf-8")
        code, text = lauf(ordner)
        rot = [z for z in text.splitlines() if z.startswith("FAIL")]
        if code != 1 or len(rot) != 1 or "manifest" not in rot[0] or "motion.py: modified" not in rot[0]:
            fehler.append(f"manipulierte Kopie: Exit {code}, erwartet genau manifest rot\n{text}")
        datei.write_bytes((PAKET / "motion.py").read_bytes())

        # Gegenprobe: zusätzliches Modul
        code, text = lauf(ordner)
        if code != 1 or "modules without manifest entry: ['fremd.py']" not in text:
            fehler.append(f"zusätzliches Modul: Exit {code}\n{text}")
        (paket / "fremd.py").unlink()

        # Gegenprobe: zusätzliches importierbares Unterpaket
        sub = paket / "unterpaket"
        sub.mkdir(exist_ok=True)
        (sub / "__init__.py").write_text("# subpackage\n", encoding="utf-8")
        code, text = lauf(ordner)
        if code != 1 or "modules without manifest entry: ['unterpaket']" not in text:
            fehler.append(f"zusätzliches Unterpaket: Exit {code}\n{text}")
        shutil.rmtree(sub, ignore_errors=True)

        # Gegenprobe: gelöschtes Manifest in übernommener Kopie
        manifest_pfad = paket / "SHELL_MANIFEST.json"
        manifest_inhalt = manifest_pfad.read_bytes()
        manifest_pfad.unlink()
        code, text = lauf(ordner)
        if code != 1 or "manifest: SHELL_MANIFEST.json is missing in consumer copy" not in text:
            fehler.append(f"gelöschtes Manifest: Exit {code}, erwartet Ablehnung wegen fehlendem Manifest\n{text}")

        # Gegenprobe: vorgetäuschter Quellbaum (nur einzelne Glide-Dateien vorhanden)
        fake_app = pathlib.Path(ordner) / "app.pyw"
        fake_app.write_text("# fake\n", encoding="utf-8")
        code, text = lauf(ordner)
        if code != 1 or "manifest: SHELL_MANIFEST.json is missing in consumer copy" not in text:
            fehler.append(f"vorgetäuschter Quellbaum: Exit {code}, erwartet Ablehnung trotz fake app.pyw\n{text}")
        fake_app.unlink()

        manifest_pfad.write_bytes(manifest_inhalt)

        # Gegenprobe: Symlink statt Datei
        (paket / "motion.py").unlink()
        try:
            (paket / "motion.py").symlink_to(PAKET / "motion.py")
            code, text = lauf(ordner)
            if code != 1 or "symlinks are forbidden" not in text:
                fehler.append(f"Symlink statt Shell-Datei: Exit {code}\n{text}")
            (paket / "motion.py").unlink()
            (paket / "motion.py").write_bytes((PAKET / "motion.py").read_bytes())
        except OSError:
            pass


def main():
    fehler = []
    # 1. Quellbaum-Selbsttest direkt in src/glide
    code_quelle, text_quelle = lauf(REPO / "src" / "glide")
    if code_quelle != 0 or "ok   manifest: source tree without manifest" not in text_quelle or "13/13 checks passed" not in text_quelle:
        fehler.append(f"Glide-Quellbaum: Exit {code_quelle}\n{text_quelle}")

    # 2. Manifest-Fälle und Gegenproben
    manifestfaelle(fehler)

    # 3. Vollständige übernommene Kopie
    with tempfile.TemporaryDirectory(prefix="glide-shell-selbst-") as ordner:
        uebernahme(ordner)
        code, text = lauf(ordner)
        zeilen = [z for z in text.splitlines() if z.startswith(("ok ", "FAIL"))]
        if code != 0 or len(zeilen) != 13 or any(z.startswith("FAIL") for z in zeilen) or "13/13 checks passed" not in text:
            fehler.append(f"vollständige Kopie: Exit {code}\n{text}")

    # 4. Gegenprobe Geometrie mit und ohne -O
    with tempfile.TemporaryDirectory(prefix="glide-shell-selbst-") as ordner:
        paket = uebernahme(ordner)
        datei = paket / "window_geometry.py"
        quelle = datei.read_text(encoding="utf-8")
        alt = "    return width, height, int(match.group(4)), int(match.group(6))"
        if alt not in quelle:
            fehler.append("Gegenprobe: Ersetzungsstelle in window_geometry.parse fehlt")
        else:
            datei.write_text(quelle.replace(alt, "    return width, height, None, None"), encoding="utf-8")
            # Manifest aktualisieren, damit genau die Auswirkung auf window_geometry isoliert geprüft wird
            manifest_pfad = paket / "SHELL_MANIFEST.json"
            manifest_daten = json.loads(manifest_pfad.read_text(encoding="utf-8"))
            manifest_daten["dateien"]["window_geometry.py"] = hashlib.sha256(datei.read_bytes()).hexdigest()
            manifest_pfad.write_text(json.dumps(manifest_daten, indent=2), encoding="utf-8")
            for schalter in ((), ("-O",)):
                code, text = lauf(ordner, *schalter)
                rot = [z for z in text.splitlines() if z.startswith("FAIL")]
                if code != 1 or len(rot) != 1 or "window_geometry" not in rot[0] or "12/13 checks passed" not in text:
                    fehler.append(f"Gegenprobe {' '.join(schalter) or 'ohne -O'}: Exit {code}, "
                                  f"erwartet genau window_geometry rot\n{text}")
    if fehler:
        print("\n".join(fehler))
        print("Shell-Selbsttest: ROT")
        return 1
    print("Shell-Selbsttest: OK (Kopie 13/13, Gegenproben erkennen kaputte Geometrie auch mit -O, gelöschte Manifeste sowie manipulierte und ergänzte Dateien/Unterpakete)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
