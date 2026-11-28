# SPDX-License-Identifier: MPL-2.0
"""E01: Framework-Checkpoint erzeugen und in einem neutralen Host prüfen.

Der Checkpoint entsteht außerhalb der Arbeitskopie. Geprüft werden: Manifest
und Snapshot-Kennung (`framework_checkpoint.py --pruefen`), Manifest des
Übernahmewerkzeugs (`shell_uebernehmen.py --pruefen --mit-bento`),
Startfähigkeit und Versionen aus der Kopie, Shell- und Bento-Selbsttest aus
der Kopie, Import-Isolation (kein Glide-Fachmodul geladen), Konformität eines
fremden Hosts und der Bento-Referenzhost mit eigenen Themen. Alle Läufe in
eigenen Prozessen mit `-I` (keine Umgebungs- oder Arbeitsordnerpfade).
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]


def lauf(*args, cwd=None):
    ergebnis = subprocess.run([sys.executable, "-B", *args], capture_output=True, text=True, cwd=cwd, timeout=600)
    return ergebnis.returncode, ergebnis.stdout + ergebnis.stderr


def im_host(src, code, cwd):
    """Python isoliert (-I) mit nur dem Checkpoint im Suchpfad."""
    return lauf("-I", "-c", f"import sys; sys.path.insert(0, {str(src)!r}); " + code, cwd=cwd)


with tempfile.TemporaryDirectory(prefix="glide-ckpt-", ignore_cleanup_errors=True) as tmp:
    tmp = Path(tmp)
    ziel = tmp / "checkpoint"
    rc, out = lauf(str(REPO / "scripts/pflege/framework_checkpoint.py"), str(ziel))
    assert rc == 0, out
    daten = json.loads((ziel / "CHECKPOINT.json").read_text(encoding="utf-8"))
    src = ziel / "src"
    rc, out = lauf(str(REPO / "scripts/pflege/framework_checkpoint.py"), "--pruefen", str(ziel))
    assert rc == 0 and "unverändert" in out, out
    rc, out = lauf(str(REPO / "scripts/pflege/shell_uebernehmen.py"), "--pruefen", "--mit-bento", str(src))
    assert rc == 0, out
    # Keine Glide-Fachmodule, Berichte, Bilder oder Benutzerpfade im Checkpoint.
    namen = {e["path"] for e in daten["files"]}
    assert all(n.startswith(("src/glide_shell/", "src/glide_bento/")) or n.endswith(("MANIFEST.json", "LICENSE")) for n in namen), namen
    assert not any(n.endswith((".png", ".jpg", ".log", ".glidebackup", ".glideapp")) for n in namen)
    for e in daten["files"]:
        inhalt = (ziel / e["path"]).read_bytes()
        assert b"C:\\Users\\" not in inhalt and b"/Users/" not in inhalt.replace(b"/Users/<", b""), e["path"]
    host = tmp / "neutraler_host"
    host.mkdir()
    rc, out = im_host(src, "import glide_shell, glide_bento; "
                           "assert not any(m in sys.modules for m in ('app','ui_design','i18n','planning','ai_workspace')), sorted(sys.modules); "
                           "print(glide_shell.SHELL_VERSION, glide_bento.BENTO_VERSION)", host)
    assert rc == 0 and out.split() == [daten["shell_version"], daten["bento_version"]], out
    for modul, erwartet in (("glide_shell.selftest", "13/13"), ("glide_bento.selftest", "16/16")):
        rc, out = im_host(src, f"import runpy; runpy.run_module({modul!r}, run_name='__main__')", host)
        assert rc == 0 and erwartet in out, (modul, out[-1500:])
    # Fremder Host: eigenes Hauptmodul mit Shell und Bento, Konformität.
    shutil.copytree(src / "glide_shell", host / "glide_shell")
    shutil.copytree(src / "glide_bento", host / "glide_bento")
    (host / "main.py").write_text("import glide_shell.app_host\nimport glide_bento\n", encoding="utf-8")
    rc, out = im_host(src, f"from glide_shell import conformance; sys.exit(conformance.main([{str(host)!r}]))", host)
    assert rc == 0 and "conform" in out, out
    rc, out = im_host(src, f"exec(compile(open({str(REPO / 'tests/fixtures/bento_referenzhost/host.py')!r}, encoding='utf-8').read(), 'host.py', 'exec'))", host)
    assert rc == 0, out[-2000:]
    print(f"test_framework_checkpoint: OK – Checkpoint {daten['snapshot_id'][:16]} (Shell {daten['shell_version']}, "
          f"Bento {daten['bento_version']}, {len(daten['files'])} Dateien); Manifest, Übernahmeprüfung, Selbsttests, "
          "Import-Isolation, Konformität und Referenzhost aus der Kopie bestanden (Windows-Tk)")
