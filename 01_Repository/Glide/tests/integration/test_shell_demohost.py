# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 6 (D95): Der Demonstrationshost läuft nur mit `glide_shell` und `tkinter`.

Der Test kopiert ausschließlich den Ordner `src/glide/glide_shell` in ein leeres
Temporärverzeichnis und startet den Host dort in einem eigenen Prozess. Ein
Folgeprojekt, das nur dieses Paket übernimmt, bekommt damit dasselbe Ergebnis:
- `glide_shell` kommt aus der Kopie, kein Modul aus `src/glide` wird geladen;
- Menüleiste mit Aktionskennungen, Uhr im eigenen `AfterScope`, Bedienelement;
- der modale Dialog aus `create_dialog` hält den Griff, folgt der Hostfarbe und
  gibt ihn frei;
- nach dem Schließen ist kein Zeitgeber des Hosts mehr offen.

Aufruf: python3 -B tests/integration/test_shell_demohost.py
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

KIND = r'''
import sys, tkinter as tk
sys.path[:] = [p for p in sys.path if "src" + __import__("os").sep + "glide" not in p]
ordner = sys.argv[1]
sys.path.insert(0, ordner)
import glide_shell
from glide_shell import demo, window_lifetime
assert glide_shell.__file__.startswith(ordner), glide_shell.__file__
assert glide_shell.SHELL_VERSION.count(".") == 2, glide_shell.SHELL_VERSION
root = tk.Tk()
root.geometry("420x240+40+40")
host = demo.DemoHost(root, colors={"bg": "#FAFAF0"})
root.update()
ids = [m._glide_action_ids for m in host.menus]
assert {"open_dialog", "quit"} <= {a for d in ids for a in d.values()}, ids
assert host.clock.cget("text").count(":") == 2, host.clock.cget("text")
assert len(host.scope.pending()) == 1, host.scope.pending()
host.seconds.set(False); host.tick(); root.update()
assert host.clock.cget("text").count(":") == 1, host.clock.cget("text")
assert len(host.scope.pending()) == 1, "Uhr plant genau einen Folgelauf"
gesehen = {}
def im_dialog():
    dialog = [w for w in root.winfo_children() if isinstance(w, tk.Toplevel)][-1]
    gesehen.update(titel=dialog.title(), grab=root.grab_current() is dialog,
                   bg=dialog.cget("background"), besitzer=str(dialog.transient()))
    dialog.event_generate("<Escape>")
    dialog.destroy()
root.after(200, im_dialog)
host.open_dialog()
assert gesehen.get("titel") == "Example dialog", gesehen
assert gesehen.get("grab") is True and gesehen.get("bg") == "#FAFAF0", gesehen
assert gesehen.get("besitzer") == str(root), gesehen
assert root.grab_current() is None and host.dialogs_opened == 1
fremd = sorted(n for n, m in sys.modules.items()
               if getattr(m, "__file__", None) and "src" + __import__("os").sep + "glide" in m.__file__
               and not m.__file__.startswith(ordner))
assert not fremd, fremd
scope = host.scope
host.close()
assert scope.closed and not scope.jobs, scope.jobs
print("DEMOHOST OK")
'''


def main():
    with tempfile.TemporaryDirectory(prefix="glide-shell-demo-") as ordner:
        shutil.copytree(PAKET, pathlib.Path(ordner) / "glide_shell", ignore=shutil.ignore_patterns("__pycache__"))
        umgebung = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        lauf = subprocess.run([sys.executable, "-B", "-c", KIND, ordner], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=umgebung, cwd=ordner, timeout=ZEITLIMIT)
    ausgabe = (lauf.stdout + lauf.stderr).strip()
    if lauf.returncode != 0 or "DEMOHOST OK" not in lauf.stdout:
        print(ausgabe)
        print("Shell-Demohost: ROT")
        return 1
    print("Shell-Demohost: OK (nur glide_shell und tkinter, Menü, Uhr im AfterScope, modaler Dialog, Abbau ohne offene Zeitgeber)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
