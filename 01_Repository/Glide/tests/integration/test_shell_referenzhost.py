# SPDX-License-Identifier: MPL-2.0
"""T337: End-to-End-Referenzhost für unabhängige Folgeprojekte (Phase 5).

Dieser Test verifiziert:
1. Eine mit `shell_uebernehmen.py` übernommene Kopie der Glide Shell läuft isoliert
   in einem fremden Projektverzeichnis ohne Zugriff auf den Glide-Quellbaum.
2. Der Referenzhost implementiert die geforderten Host-Funktionen:
   - Import ausschließlich aus `glide_shell` (und Tkinter/Stdlib).
   - Start und Lebenszyklussteuerung über `AppHost`.
   - Host-eigene Fachlogik und eigene DE/EN-Texte.
   - Eigene Theme-Werte (Hell/Dunkel via `system_appearance`).
   - Modaler Dialog via `modal_session`.
   - Rückgängig/Wiederholen via `CommandHistory` und Befehlsobjekt.
   - Zeitgeber und Übergänge im eigenen `AfterScope` (`motion.Transitions`).
   - Schließweg und sauberer Event-/Timer-Abbau.
3. Schnittstellenwächter: Eine absichtlich hinzugefügte unzulässige Abhängigkeit
   zu Glide (z. B. Import von `glide.version` oder `glide.ui_design`) wird im
   Host-Test zuverlässig erkannt und schlägt fehl.

Aufruf: python3 -B tests/integration/test_shell_referenzhost.py
"""
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[2]
WERKZEUG = REPO / "scripts" / "pflege" / "shell_uebernehmen.py"

HOST_CODE = r'''# -*- coding: utf-8 -*-
import json
import sys
import tkinter as tk
from glide_shell import app_host, command_history, desktop_adapter, modal_session, motion, system_appearance, window_geometry, window_lifetime

# Eigene Theme-Werte des Hosts (Dunkel / Hell)
THEME = {
    "light": {"bg": "#FFFFFF", "fg": "#111111", "card": "#F5F5F5", "accent": "#0066CC"},
    "dark": {"bg": "#1E1E1E", "fg": "#F0F0F0", "card": "#2D2D2D", "accent": "#3399FF"},
}

LOCALES = {
    "de": {
        "title": "Referenz-Host",
        "count": "Zähler: {count}",
        "increment": "Erhöhen",
        "dialog": "Dialog öffnen",
        "dialog_title": "Bestätigung",
        "dialog_msg": "Modaler Dialog des Referenzhosts.",
        "dialog_close": "Schließen",
        "undo": "Rückgängig",
        "redo": "Wiederholen",
    },
    "en": {
        "title": "Reference Host",
        "count": "Count: {count}",
        "increment": "Increment",
        "dialog": "Open Dialog",
        "dialog_title": "Confirmation",
        "dialog_msg": "Modal dialog of reference host.",
        "dialog_close": "Close",
        "undo": "Undo",
        "redo": "Redo",
    }
}

class IncrementCommand(command_history.Command):
    def __init__(self, host):
        self.host = host
    def execute(self):
        self.host.counter += 1
        self.host.update_display()
    def undo(self):
        self.host.counter -= 1
        self.host.update_display()

class ReferenceHostApp:
    def __init__(self, root, lang="de", dark=False):
        self.root = root
        self.lang = lang
        self.texts = LOCALES[lang]
        self.palette = system_appearance.resolve(THEME, dark, THEME["light"])
        self.counter = 0
        self.dialog_shown = False

        self.scope = window_lifetime.scope_for(root)
        self.history = command_history.CommandHistory(limit=20)
        self.transitions = motion.Transitions(self.scope.after, self.scope.cancel)

        # Fenstergeometrie
        cw, ch, cx, cy = window_geometry.clamp(400, 300, 50, 50, 1920, 1080, (320, 200))
        root.geometry(window_geometry.format_geometry(cw, ch, cx, cy))
        root.title(self.texts["title"])
        root.configure(bg=self.palette["bg"])

        # Layout
        self.card = tk.Frame(root, bg=self.palette["card"], padx=10, pady=10)
        self.card.pack(padx=20, pady=20, fill="both", expand=True)

        self.label = tk.Label(self.card, text="", bg=self.palette["card"], fg=self.palette["fg"])
        self.label.pack(pady=5)

        self.btn_inc = tk.Button(self.card, text=self.texts["increment"], command=self.do_increment)
        self.btn_inc.pack(pady=5)

        self.btn_dlg = tk.Button(self.card, text=self.texts["dialog"], command=self.open_dialog)
        self.btn_dlg.pack(pady=5)

        # Menü und Kürzel
        self.platform = app_host.platform_of(root.tk.call("tk", "windowingsystem"))
        menubar = desktop_adapter.build_menu_tree(root, [
            ("Edit", [
                (self.texts["undo"], self.undo, desktop_adapter.format_accelerator("Z"), "undo"),
                (self.texts["redo"], self.redo, desktop_adapter.format_redo_accelerator(), "redo"),
            ])
        ])
        app_host.attach_menubar(root, menubar)
        app_host.install_close(root, self.request_close, self.platform, scope=self.scope)

        self.update_display()

    def update_display(self):
        self.label.configure(text=self.texts["count"].format(count=self.counter))

    def do_increment(self):
        self.history.execute(IncrementCommand(self))
        # Kurzer visueller Übergang
        self.transitions.start("pulse", lambda f: None, duration_ms=100)

    def undo(self):
        self.history.undo()

    def redo(self):
        self.history.redo_step()

    def open_dialog(self):
        dlg = modal_session.create_dialog(self.root, self.texts["dialog_title"], background=self.palette["bg"])
        lbl = tk.Label(dlg, text=self.texts["dialog_msg"], bg=self.palette["bg"], fg=self.palette["fg"])
        lbl.pack(padx=20, pady=20)
        btn = tk.Button(dlg, text=self.texts["dialog_close"], command=dlg.destroy)
        btn.pack(pady=10)
        self.dialog_shown = True
        modal_session.run_modal(self.root, dlg)

    def request_close(self):
        self.transitions.close()
        self.scope.close()
        self.root.destroy()

def run_isolated_verification():
    root = tk.Tk()
    root.withdraw()
    try:
        app = ReferenceHostApp(root, lang="de", dark=True)
        root.update()

        # 1. Start & Theme
        assert app.palette["bg"] == THEME["dark"]["bg"]
        assert app.counter == 0
        assert "Zähler: 0" in app.label.cget("text")

        # 2. Fachlogik & Undo/Redo
        app.do_increment()
        root.update()
        assert app.counter == 1
        assert "Zähler: 1" in app.label.cget("text")

        app.undo()
        root.update()
        assert app.counter == 0
        assert "Zähler: 0" in app.label.cget("text")

        app.redo()
        root.update()
        assert app.counter == 1

        # 3. Dialog & Focus
        root.after(50, lambda: [app.root.winfo_children()[-1].destroy()])
        app.open_dialog()
        assert app.dialog_shown is True

        # 4. Timer & Cleanup
        app.request_close()
        assert len(app.scope.pending()) == 0, f"Offene Timer nach Schließen: {app.scope.pending()}"
        print("VERIFIED_ISOLATED_HOST_OK")
    finally:
        try:
            root.destroy()
        except Exception:
            pass

if __name__ == "__main__":
    run_isolated_verification()
'''


class ReferenzHostIntegrationTest(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory(prefix="glide-shell-refhost-")
        self.test_dir = pathlib.Path(self._temp.name)
        self.proj_dir = self.test_dir / "my_project"
        self.proj_dir.mkdir(parents=True, exist_ok=True)

        # 1. Shell mit offiziellem Werkzeug übernehmen
        cmd = [sys.executable, "-B", str(WERKZEUG), "--unsauber-erlauben", str(self.proj_dir)]
        lauf = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        self.assertEqual(lauf.returncode, 0, f"Übernahme fehlgeschlagen:\n{lauf.stdout}\n{lauf.stderr}")
        self.assertTrue((self.proj_dir / "glide_shell" / "__init__.py").is_file())

        # 2. Host-Code platzieren
        self.host_file = self.proj_dir / "host_app.py"
        self.host_file.write_text(HOST_CODE, encoding="utf-8")

    def tearDown(self):
        self._temp.cleanup()

    def run_host_script(self, code_file):
        """Führt ein Skript in isolierter Umgebung ohne Glide im PYTHONPATH aus."""
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        env.pop("PYTHONPATH", None)
        sub = subprocess.run([sys.executable, "-B", str(code_file)],
                             capture_output=True, text=True, cwd=self.proj_dir, env=env, timeout=60)
        return sub.returncode, sub.stdout, sub.stderr

    def test_referenzhost_laeuft_isoliert_und_erfuellt_vertraege(self):
        code, stdout, stderr = self.run_host_script(self.host_file)
        self.assertEqual(code, 0, f"Referenzhost fehlgeschlagen (Exit {code}):\nSTDOUT: {stdout}\nSTDERR: {stderr}")
        self.assertIn("VERIFIED_ISOLATED_HOST_OK", stdout)

    def test_unzulässige_glide_abhaengigkeit_wird_erkannt_und_schlaegt_fehl(self):
        # Wir fügen absichtlich einen verbotenen Glide-Import hinzu
        bad_code = "import glide.version\n" + HOST_CODE
        bad_file = self.proj_dir / "bad_host.py"
        bad_file.write_text(bad_code, encoding="utf-8")

        code, stdout, stderr = self.run_host_script(bad_file)
        self.assertNotEqual(code, 0, "Host mit unzulässiger Glide-Abhängigkeit hätte fehlschlagen müssen!")
        self.assertTrue("ModuleNotFoundError" in stderr or "No module named 'glide'" in stderr or "ImportError" in stderr,
                        f"Unerwarteter Fehler: {stderr}")


if __name__ == "__main__":
    unittest.main()
