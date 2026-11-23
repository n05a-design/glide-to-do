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
import json
import os
import pathlib
import shutil
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

def expect(condition, message="Prüfung fehlgeschlagen"):
    if not condition:
        raise AssertionError(message)

def run_isolated_verification():
    def create_test_root():
        root = tk.Tk()
        root.withdraw()
        return root

    def no_glide_in_runtime(_root):
        forbidden = [m for m in sys.modules if m == "glide" or (m.startswith("glide.") and not m.startswith("glide.glide_shell"))]
        if forbidden:
            return ("Architekturfehler", f"Unzulässige Glide-Kopplung: {forbidden}")
        return None

    host = app_host.AppHost(
        tk_factory=create_test_root,
        preflight=(no_glide_in_runtime,),
        show_error=lambda title, msg, **kw: sys.stderr.write(f"{title}: {msg}\n"),
    )
    app = host.run(lambda r: ReferenceHostApp(r, lang="de", dark=True), mainloop=False)
    root = app.root
    try:
        root.update()

        # 1. Start & Theme
        expect(app.palette["bg"] == THEME["dark"]["bg"], "Theme-Hintergrund stimmt nicht mit Palette überein")
        expect(app.counter == 0, "Zähler muss initial 0 sein")
        expect("Zähler: 0" in app.label.cget("text"), "Labeltext muss Zähler: 0 enthalten")

        # 2. Fachlogik & Undo/Redo
        app.do_increment()
        root.update()
        expect(app.counter == 1, "Zähler nach Inkrement muss 1 sein")
        expect("Zähler: 1" in app.label.cget("text"), "Labeltext muss Zähler: 1 enthalten")

        app.undo()
        root.update()
        expect(app.counter == 0, "Zähler nach Undo muss 0 sein")
        expect("Zähler: 0" in app.label.cget("text"), "Labeltext muss Zähler: 0 enthalten")

        app.redo()
        root.update()
        expect(app.counter == 1, "Zähler nach Redo muss 1 sein")

        # 3. Dialog & Focus
        root.after(50, lambda: [app.root.winfo_children()[-1].destroy()])
        app.open_dialog()
        expect(app.dialog_shown is True, "Dialog wurde nicht geöffnet")

        # 4. Timer & Cleanup
        app.request_close()
        expect(len(app.scope.pending()) == 0, f"Offene Timer nach Schließen: {app.scope.pending()}")
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

    def run_host_script(self, code_file, *extra_args):
        """Führt ein Skript in isolierter Umgebung ohne Glide im PYTHONPATH aus (optional mit Flags wie -O)."""
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        env.pop("PYTHONPATH", None)
        sub = subprocess.run([sys.executable, "-B", *extra_args, str(code_file)],
                             capture_output=True, text=True, cwd=self.proj_dir, env=env, timeout=60)
        return sub.returncode, sub.stdout, sub.stderr

    def test_referenzhost_laeuft_isoliert_und_erfuellt_vertraege(self):
        for args in ((), ("-O",)):
            code, stdout, stderr = self.run_host_script(self.host_file, *args)
            self.assertEqual(code, 0, f"Referenzhost mit Flag {args} fehlgeschlagen (Exit {code}):\nSTDOUT: {stdout}\nSTDERR: {stderr}")
            self.assertIn("VERIFIED_ISOLATED_HOST_OK", stdout)

    def test_unzulässige_glide_abhaengigkeit_wird_erkannt_und_schlaegt_fehl(self):
        # 1. Fall A: Echter Architekturverstoß – Glide ist im Modulsuchpfad physisch vorhanden,
        #    aber der Laufzeit-Architekturwächter im AppHost erkennt den Import von Glide-Fachlogik
        #    und verweigert den Start vor Aufbau der Anwendung.
        bad_code_coupling = (
            "import sys, pathlib\n"
            f"sys.path.insert(0, {str(REPO / 'src')!r})\n"
            "import glide.glide_start\n"  # Echter Glide-Fachlogikimport!
            + HOST_CODE
        )
        bad_file_a = self.proj_dir / "bad_host_coupling.py"
        bad_file_a.write_text(bad_code_coupling, encoding="utf-8")

        code_a, stdout_a, stderr_a = self.run_host_script(bad_file_a)
        self.assertEqual(code_a, 1, f"Architekturverstoß hätte mit Exitcode 1 abbrechen müssen:\nSTDOUT: {stdout_a}\nSTDERR: {stderr_a}")
        self.assertTrue("Architekturfehler" in stderr_a or "Unzulässige Glide-Kopplung" in stderr_a,
                        f"Erwartete Architekturfehlermeldung in STDERR, erhalten:\n{stderr_a}")

        # 2. Fall B: Fehlender Import ohne Quellpfad
        bad_code_missing = "import glide.version\n" + HOST_CODE
        bad_file_b = self.proj_dir / "bad_host_missing.py"
        bad_file_b.write_text(bad_code_missing, encoding="utf-8")

        code_b, stdout_b, stderr_b = self.run_host_script(bad_file_b)
        self.assertNotEqual(code_b, 0, "Host mit unzulässiger Glide-Abhängigkeit hätte fehlschlagen müssen!")
        self.assertTrue("ModuleNotFoundError" in stderr_b or "No module named 'glide'" in stderr_b or "ImportError" in stderr_b,
                        f"Unerwarteter Fehler: {stderr_b}")

    def test_consumer_upgrade_und_erhalt_der_hostdateien(self):
        # 1. Ausgangszustand: Host verwendet echten historischen Git-Stand von Shell 0.5.0 (Commit 3c91e0c8)
        host_050_code = r'''# -*- coding: utf-8 -*-
import sys
import tkinter as tk
from glide_shell import modal_session, motion, redo_history, system_appearance, window_geometry, window_lifetime

def expect(cond, msg="Prüfung fehlgeschlagen"):
    if not cond:
        raise AssertionError(msg)

root = tk.Tk()
root.withdraw()
try:
    scope = window_lifetime.scope_for(root)
    transitions = motion.Transitions(scope.after, scope.cancel)
    redo = redo_history.RedoHistory(limit=10)
    cw, ch, cx, cy = window_geometry.clamp(400, 300, 50, 50, 1920, 1080, (320, 200))
    root.geometry(window_geometry.format_geometry(cw, ch, cx, cy))
    palette = system_appearance.resolve({"light": {"bg": "#ffffff"}, "dark": {"bg": "#1e1e1e"}}, True, {"bg": "#ffffff"})
    root.configure(bg=palette["bg"])
    expect(palette["bg"] == "#1e1e1e", "Theme mismatch")
    scope.close()
    print("VERIFIED_050_HOST_OK")
finally:
    try:
        root.destroy()
    except Exception:
        pass
'''
        # Projekt leeren und echten Quellstand 0.5.0 aus Git via --commit holen
        shutil.rmtree(self.proj_dir)
        self.proj_dir.mkdir(parents=True, exist_ok=True)
        cmd_checkout_050 = [sys.executable, "-B", str(WERKZEUG), "--commit", "3c91e0c8", str(self.proj_dir)]
        lauf_050 = subprocess.run(cmd_checkout_050, capture_output=True, text=True, timeout=60)
        self.assertEqual(lauf_050.returncode, 0, f"Checkout 0.5.0 fehlgeschlagen:\n{lauf_050.stdout}\n{lauf_050.stderr}")

        shell_dir = self.proj_dir / "glide_shell"
        manifest_file = shell_dir / "SHELL_MANIFEST.json"
        manifest_050 = json.loads(manifest_file.read_text(encoding="utf-8"))
        self.assertEqual(manifest_050["shell_version"], "0.5.0")
        self.assertEqual(len(manifest_050["dateien"]), 17)

        # Host-eigene Dateien anlegen
        host_data_file = self.proj_dir / "host_data.json"
        host_data_file.write_text('{"db_version": 1, "custom_setting": 42}', encoding="utf-8")
        host_050_file = self.proj_dir / "host_050.py"
        host_050_file.write_text(host_050_code, encoding="utf-8")

        # Host mit echtem Stand 0.5.0 ausführen
        code_050, stdout_050, stderr_050 = self.run_host_script(host_050_file)
        self.assertEqual(code_050, 0, f"Host mit echtem Stand 0.5.0 sollte laufen:\n{stderr_050}")
        self.assertIn("VERIFIED_050_HOST_OK", stdout_050)

        # 2. Reguläres Upgrade auf neuesten Shell-Stand (0.6.2) durchführen
        cmd_upgrade = [sys.executable, "-B", str(WERKZEUG), "--unsauber-erlauben", str(self.proj_dir)]
        lauf_up = subprocess.run(cmd_upgrade, capture_output=True, text=True, timeout=60)
        self.assertEqual(lauf_up.returncode, 0, f"Upgrade fehlgeschlagen:\n{lauf_up.stdout}\n{lauf_up.stderr}")

        # 3. Nach dem Upgrade prüfen:
        # a) Host-Dateien sind byte-identisch unversehrt
        self.assertTrue(host_data_file.is_file())
        self.assertEqual(host_data_file.read_text(encoding="utf-8"), '{"db_version": 1, "custom_setting": 42}')
        # b) Manifest ist aktualisiert auf 0.6.2 und umfasst neue Module
        new_manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        self.assertEqual(new_manifest["shell_version"], "0.6.2")
        self.assertIn("app_host.py", new_manifest["dateien"])
        self.assertIn("command_history.py", new_manifest["dateien"])
        # c) Host-Anwendungen laufen: 0.5.0-Host und neuer 0.6.2-Host (auch mit -O)
        code_old_after, stdout_old_after, stderr_old_after = self.run_host_script(host_050_file)
        self.assertEqual(code_old_after, 0, f"0.5.0-Host nach Upgrade fehlgeschlagen:\n{stderr_old_after}")
        self.assertIn("VERIFIED_050_HOST_OK", stdout_old_after)

        self.host_file.write_text(HOST_CODE, encoding="utf-8")
        for args in ((), ("-O",)):
            code_after, stdout_after, stderr_after = self.run_host_script(self.host_file, *args)
            self.assertEqual(code_after, 0, f"Host nach Upgrade fehlgeschlagen mit Flag {args}:\n{stderr_after}")
            self.assertIn("VERIFIED_ISOLATED_HOST_OK", stdout_after)

    def test_consumer_upgrade_rollback_bei_fehler(self):
        host_data_file = self.proj_dir / "host_data.json"
        host_data_file.write_text('{"state": "safe"}', encoding="utf-8")
        shell_dir = self.proj_dir / "glide_shell"
        init_file = shell_dir / "__init__.py"
        init_before = init_file.read_bytes()
        manifest_file = shell_dir / "SHELL_MANIFEST.json"
        manifest_before = manifest_file.read_bytes()

        inject_script = (
            "import sys, pathlib\n"
            f"sys.path.insert(0, {str(REPO / 'scripts' / 'pflege')!r})\n"
            "import shell_uebernehmen as ueb\n"
            "original = ueb.schreiben_atomar\n"
            "def broken_schreiben(ziel, inhalt):\n"
            "    if ziel.name.endswith('.py') and ziel.name != '__init__.py':\n"
            "        raise IOError('Künstlicher Abbruch mitten im Kopieren')\n"
            "    return original(ziel, inhalt)\n"
            "ueb.schreiben_atomar = broken_schreiben\n"
            f"code, meldungen = ueb.uebernehmen(pathlib.Path({str(shell_dir)!r}), ersetzen=True)\n"
            "print('CODE:', code)\n"
            "for m in meldungen: print('MSG:', m)\n"
        )
        sub = subprocess.run([sys.executable, "-B", "-c", inject_script],
                             capture_output=True, text=True, cwd=self.proj_dir, timeout=60)
        self.assertIn("CODE: 1", sub.stdout)
        self.assertIn("Rollback ausgeführt", sub.stdout)

        # Verifikation: Zustand ist exakt wie vor dem Abbruch
        self.assertEqual(init_file.read_bytes(), init_before)
        self.assertEqual(manifest_file.read_bytes(), manifest_before)
        self.assertEqual(host_data_file.read_text(encoding="utf-8"), '{"state": "safe"}')

        # Referenzhost läuft weiterhin stabil
        code, stdout, stderr = self.run_host_script(self.host_file)
        self.assertEqual(code, 0, f"Host nach Rollback muss voll lauffähig sein:\n{stderr}")
        self.assertIn("VERIFIED_ISOLATED_HOST_OK", stdout)


if __name__ == "__main__":
    unittest.main()
