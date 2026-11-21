# SPDX-License-Identifier: MPL-2.0
"""Selbsttest der Glide Shell (Shell-Paket 11): läuft aus einer Kopie und erkennt eine kaputte Kopie.

Der Test kopiert `src/glide/glide_shell` in ein leeres Temporärverzeichnis und
startet dort `python -m glide_shell.selftest` in eigenem Prozess:
- vollständige Kopie: Exitcode 0, jede Prüfung `ok`, Zusammenfassung „7/7“;
- Gegenprobe mit verändertem `window_geometry.parse`: Exitcode 1 und genau
  diese Prüfung `FAIL`, die übrigen bleiben `ok`.

Aufruf: python3 -B tests/integration/test_shell_selbsttest.py
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
PAKET = REPO / "src" / "glide" / "glide_shell"
ZEITLIMIT = 120


def lauf(ordner):
    umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    umgebung.pop("PYTHONPATH", None)
    ergebnis = subprocess.run([sys.executable, "-B", "-m", "glide_shell.selftest"], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=umgebung, cwd=ordner, timeout=ZEITLIMIT)
    return ergebnis.returncode, ergebnis.stdout + ergebnis.stderr


def kopie(ziel):
    shutil.copytree(PAKET, pathlib.Path(ziel) / "glide_shell", ignore=shutil.ignore_patterns("__pycache__"))
    return pathlib.Path(ziel) / "glide_shell"


def main():
    fehler = []
    with tempfile.TemporaryDirectory(prefix="glide-shell-selbst-") as ordner:
        kopie(ordner)
        code, text = lauf(ordner)
        zeilen = [z for z in text.splitlines() if z.startswith(("ok ", "FAIL"))]
        if code != 0 or len(zeilen) != 7 or any(z.startswith("FAIL") for z in zeilen) or "7/7 checks passed" not in text:
            fehler.append(f"vollständige Kopie: Exit {code}\n{text}")
    with tempfile.TemporaryDirectory(prefix="glide-shell-selbst-") as ordner:
        paket = kopie(ordner)
        datei = paket / "window_geometry.py"
        quelle = datei.read_text(encoding="utf-8")
        alt = "    return width, height, int(match.group(4)), int(match.group(6))"
        if alt not in quelle:
            fehler.append("Gegenprobe: Ersetzungsstelle in window_geometry.parse fehlt")
        else:
            datei.write_text(quelle.replace(alt, "    return width, height, None, None"), encoding="utf-8")
            code, text = lauf(ordner)
            rot = [z for z in text.splitlines() if z.startswith("FAIL")]
            if code != 1 or len(rot) != 1 or "window_geometry" not in rot[0] or "6/7 checks passed" not in text:
                fehler.append(f"Gegenprobe: Exit {code}, erwartet genau window_geometry rot\n{text}")
    if fehler:
        print("\n".join(fehler))
        print("Shell-Selbsttest: ROT")
        return 1
    print("Shell-Selbsttest: OK (Kopie 7/7, Gegenprobe erkennt kaputte Geometrie)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
