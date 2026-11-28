# SPDX-License-Identifier: MPL-2.0
"""E02: kontrollierte Aktualisierung einer vorhandenen Framework-Kopie (T376).

Ein künstliches Folgeprojekt erhält zuerst Shell 0.6.2 aus dem Commit, mit dem
STEPS und Chess & Chains laut E01 arbeiten (`793596f1`). Geprüft wird der Weg
auf den aktuellen Stand mit `shell_uebernehmen.py`:

1. Host-Modul im 0.6.2-Stil (nur damals öffentliche Namen) besteht die Regel
   `host-api` gegen die neue Shell; die Aktualisierung mit `--sicherung` legt
   eine geprüfte Sicherung an, schreibt Shell und Bento, Host-Dateien bleiben
   bytegleich, Konformität und Selbsttests der neuen Kopie sind grün.
2. Ein Host, der einen Namen importiert, den die Shell nicht hat, wird ohne
   `--ersetzen` abgewiesen; nichts wird geschrieben.
3. Herabstufung (ältere Quelle über neuere Kopie) wird abgewiesen.
4. Fehlende und manipulierte Dateien meldet `--pruefen`.
5. `--zurueck` stellt den 0.6.2-Stand bytegenau wieder her; eine veränderte
   Sicherung wird abgewiesen, ohne etwas zu schreiben.
6. Eine Bento-Kopie neben einer zu alten Shell wird nicht angelegt.

Nur künstliche Daten, eigene Prozesse, Temp außerhalb der Arbeitskopie.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
WERKZEUG = REPO / "scripts/pflege/shell_uebernehmen.py"
ALT = "793596f1"  # Shell 0.6.2 (V1.86), Stand der Folgeprojekte laut E01


def lauf(*args, cwd=None):
    e = subprocess.run([sys.executable, "-B", str(WERKZEUG), *args], capture_output=True, text=True, timeout=600, cwd=cwd)
    return e.returncode, e.stdout + e.stderr


def py(code, cwd):
    e = subprocess.run([sys.executable, "-B", "-I", "-c", "import sys; sys.path.insert(0, '.'); " + code],
                       capture_output=True, text=True, timeout=600, cwd=cwd)
    return e.returncode, e.stdout + e.stderr


def hashes(ordner):
    return {p.relative_to(ordner).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ordner.rglob("*")) if p.is_file() and "__pycache__" not in p.parts}


def haupt():
    with tempfile.TemporaryDirectory(prefix="glide-akt-", ignore_cleanup_errors=True) as tmp:
        tmp = Path(tmp)
        projekt = tmp / "folgeprojekt"
        src = projekt / "src"
        src.mkdir(parents=True)
        (projekt / "pyproject.toml").write_text("[project]\nname = 'probe'\n", encoding="utf-8")
        host = src / "probe_app.py"
        host.write_text("from glide_shell.app_host import AppHost, primary_shortcuts\n"
                        "from glide_shell import modal_session, window_lifetime\n"
                        "from glide_shell.custom_controls import GlideCheckbutton\n", encoding="utf-8")
        eigen = src / "fachlogik.py"
        eigen.write_text("TONLEITER = ('c', 'd', 'e')\n", encoding="utf-8")
        fach_vorher = hashes(src.parent)

        # Ausgangsstand 0.6.2 aus dem Commit der Folgeprojekte
        rc, out = lauf("--commit", ALT, str(src))
        assert rc == 0, out
        alt_manifest = json.loads((src / "glide_shell/SHELL_MANIFEST.json").read_text(encoding="utf-8"))
        assert alt_manifest["shell_version"] == "0.6.2", alt_manifest["shell_version"]
        stand_062 = hashes(src / "glide_shell")

        # 6. Bento verlangt Shell >= 0.7.0: neben 0.6.2 nicht anlegen
        rc, out = lauf("--commit", ALT, "--mit-bento", "--ersetzen", str(src))
        assert rc != 0 and not (src / "glide_bento").exists(), out
        import importlib.util
        spec = importlib.util.spec_from_file_location("_werkzeug", WERKZEUG)
        werkzeug = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(werkzeug)
        bento = werkzeug.bento_quelle_lesen()
        ok, text = werkzeug.bento_kompatibel(src / "glide_shell", bento["shell_min"])
        assert not ok and "0.6.2" in text, text
        code, meldungen = werkzeug.bento_uebernehmen(src / "glide_shell", bento)
        assert code == werkzeug.QUELLFEHLER and not (src / "glide_bento").exists(), meldungen

        # 2. Host mit einem Namen, den die Shell nicht hat
        falsch = src / "falsch.py"
        falsch.write_text("from glide_shell.app_host import AppHost, gibt_es_nicht\n", encoding="utf-8")
        rc, out = lauf("--mit-bento", "--unsauber-erlauben", str(src))
        assert rc == 2 and "gibt_es_nicht" in out, out
        assert hashes(src / "glide_shell") == stand_062, "abgewiesene Übernahme hat geschrieben"
        falsch.unlink()

        # 1. Aktualisierung mit Sicherung
        sicherungen = tmp / "sicherungen"
        rc, out = lauf("--mit-bento", "--unsauber-erlauben", "--sicherung", str(sicherungen), str(src))
        assert rc == 0, out
        neu = json.loads((src / "glide_shell/SHELL_MANIFEST.json").read_text(encoding="utf-8"))
        sys.path.insert(0, str(REPO / "src/glide"))
        import glide_shell
        assert neu["shell_version"] == glide_shell.SHELL_VERSION, neu["shell_version"]
        assert (src / "glide_bento/BENTO_MANIFEST.json").is_file()
        sicherung = next(sicherungen.iterdir())
        assert hashes(sicherung / "glide_shell") == stand_062
        assert {k: v for k, v in hashes(src.parent).items() if not k.startswith("src/glide_")} == fach_vorher, \
            "Host-Fachdateien verändert"
        rc, out = py("from glide_shell import conformance; sys.exit(conformance.main(['.']))", src)
        assert rc == 0 and "conform" in out, out
        for modul, erwartet in (("glide_shell.selftest", "16/16"), ("glide_bento.selftest", "16/16")):
            rc, out = py(f"import runpy; runpy.run_module({modul!r}, run_name='__main__')", src)
            assert rc == 0 and erwartet in out, (modul, out[-1200:])

        # 3. Herabstufung
        rc, out = lauf("--commit", ALT, str(src))
        assert rc == 2 and "Herabstufung" in out, out

        # 4. fehlende und manipulierte Dateien
        (src / "glide_shell/motion.py").unlink()
        with open(src / "glide_shell/text_fit.py", "a", encoding="utf-8") as datei:
            datei.write("\n# lokal\n")
        rc, out = lauf("--pruefen", "--mit-bento", str(src))
        assert rc == 1 and "motion.py: fehlt" in out and "text_fit.py: verändert" in out, out

        # 5. Rückkehr; zuerst eine manipulierte Sicherung
        kaputt = tmp / "kaputt"
        shutil.copytree(sicherung, kaputt)
        with open(kaputt / "glide_shell/compat.py" if (kaputt / "glide_shell/compat.py").exists()
                  else kaputt / "glide_shell/motion.py", "a", encoding="utf-8") as datei:
            datei.write("\n# manipuliert\n")
        vorher = hashes(src / "glide_shell")
        rc, out = lauf("--zurueck", str(kaputt), str(src))
        assert rc == 2 and "beschädigt" in out and hashes(src / "glide_shell") == vorher, out
        rc, out = lauf("--zurueck", str(sicherung), str(src))
        assert rc == 0, out
        assert hashes(src / "glide_shell") == stand_062, "Rückkehr nicht bytegenau"
        rc, out = py("import glide_shell; print(glide_shell.SHELL_VERSION)", src)
        assert rc == 0 and out.strip() == "0.6.2", out
    print(f"test_framework_aktualisierung: OK – 0.6.2 ({ALT}) → {glide_shell.SHELL_VERSION} mit Sicherung, "
          "Host-Vertrag, Herabstufung, fehlende/manipulierte Dateien, Rückkehr bytegenau, Bento-Kompatibilität")


haupt()
