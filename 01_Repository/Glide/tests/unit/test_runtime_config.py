# SPDX-License-Identifier: MPL-2.0
"""Prüfungen für die kontrollierte Laufzeitkonfiguration und Pfadentkopplung (WA-49 / WA-39)."""
from pathlib import Path
import ntpath
import os
import posixpath
import sys
import tempfile
import types
import unittest
from unittest import mock

SOURCE = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(SOURCE))
import glide_start
import runtime_config as rc


class RuntimeConfigTests(unittest.TestCase):
    def test_paths_are_resolved_without_filesystem_side_effects(self):
        with tempfile.TemporaryDirectory(prefix="glide-test-pure-") as non_existent_parent:
            target = os.path.join(non_existent_parent, "does_not_exist_yet")
            self.assertFalse(os.path.exists(target))

            paths = rc.resolve_paths(data_dir=target)
            self.assertEqual(paths.base_dir, os.path.abspath(target))
            self.assertEqual(paths.save_file, os.path.join(paths.base_dir, "liste_speicher.json"))
            self.assertEqual(paths.settings_file, os.path.join(paths.base_dir, "settings.json"))
            self.assertEqual(paths.backup_dir, os.path.join(paths.base_dir, "backups"))
            self.assertEqual(paths.attachments_dir, os.path.join(paths.base_dir, "attachments"))
            self.assertEqual(paths.lock_file, os.path.join(paths.base_dir, "glide.lock"))
            self.assertEqual(paths.error_log_file, os.path.join(paths.base_dir, "fehlerprotokoll.txt"))

            # Reine Auflösung darf KEINE Verzeichnisse auf der Festplatte anlegen!
            self.assertFalse(os.path.exists(target))
            self.assertFalse(os.path.exists(paths.backup_dir))
            self.assertFalse(os.path.exists(paths.attachments_dir))

    def test_ensure_dirs_creates_required_directories_on_demand(self):
        with tempfile.TemporaryDirectory(prefix="glide-test-ensure-") as non_existent_parent:
            target = os.path.join(non_existent_parent, "explicit_target")
            paths = rc.resolve_paths(data_dir=target)
            self.assertFalse(os.path.exists(target))

            paths.ensure_dirs()
            self.assertTrue(os.path.isdir(paths.base_dir))
            self.assertTrue(os.path.isdir(paths.backup_dir))
            self.assertTrue(os.path.isdir(paths.attachments_dir))

    def test_environment_override_precedence(self):
        with tempfile.TemporaryDirectory(prefix="glide-test-env-") as env_dir:
            env = {"GLIDE_DATA_DIR": env_dir}
            paths = rc.resolve_paths(env=env)
            self.assertEqual(paths.base_dir, os.path.abspath(env_dir))

            # Expliziter Parameter schlägt Umgebungsvariable
            with tempfile.TemporaryDirectory(prefix="glide-test-explicit-") as explicit_dir:
                paths2 = rc.resolve_paths(data_dir=explicit_dir, env=env)
                self.assertEqual(paths2.base_dir, os.path.abspath(explicit_dir))

    def test_runtime_config_metadata(self):
        with tempfile.TemporaryDirectory(prefix="glide-test-cfg-") as tmp:
            env = {"GLIDE_TEST_MODE": "1"}
            config = rc.RuntimeConfig.create(data_dir=tmp, read_only=True, env=env)
            self.assertEqual(config.paths.base_dir, os.path.abspath(tmp))
            self.assertTrue(config.read_only)
            self.assertTrue(config.test_mode)
            self.assertEqual(config.app_name, "Glide")


def function_source(text, name):
    """Quelltext einer Modulfunktion, ohne das Modul zu importieren."""
    lines = text.splitlines()
    starts = [index for index, line in enumerate(lines) if line.startswith(f"def {name}(")]
    if len(starts) != 1:
        raise AssertionError(f"{name}: {len(starts)} Definitionen statt einer")
    end = starts[0] + 1
    while end < len(lines) and (not lines[end].strip() or lines[end][0] in " \t"):
        end += 1
    return "\n".join(lines[starts[0]:end]) + "\n"


def simulated(platform, home, environ):
    """Ersatz für `os` und `sys` einer Plattform; die echte Umgebung bleibt unberührt."""
    windows = platform == "win32"
    flavour = ntpath if windows else posixpath
    path = types.SimpleNamespace(
        join=flavour.join, abspath=flavour.abspath,
        expanduser=lambda value: home + value[1:] if value.startswith("~") else value)
    return (types.SimpleNamespace(name="nt" if windows else "posix", environ=dict(environ), path=path),
            types.SimpleNamespace(platform=platform, pycache_prefix=None))


class BytecodePathAgreementTests(unittest.TestCase):
    """Die drei Auflösungen des Bytecode-Ordners liefern denselben Pfad (WA-49).

    `glide_start.cache_ordner`, `bytecode_cache_dir` in `app.pyw` und
    `runtime_config.resolve_default_cache_dir` plus „bytecode“ stehen bewusst
    nebeneinander: Jeder Einstieg muss den Ordner kennen, bevor er sein erstes
    eigenes Modul importiert – sonst entstünde `__pycache__` neben den Quellen.
    Statt sie zusammenzulegen, hält dieser Test sie gleich. Die Funktion der
    App wird aus dem Quelltext gelöst; der Test bleibt ohne Tk.
    """

    @classmethod
    def setUpClass(cls):
        text = (SOURCE / "app.pyw").read_text(encoding="utf-8")
        cls.app_function = compile(function_source(text, "bytecode_cache_dir"), "app.pyw", "exec")

    def resolutions(self, platform, home, environ):
        fake_os, fake_sys = simulated(platform, home, environ)
        with mock.patch.object(glide_start, "os", fake_os), mock.patch.object(glide_start, "sys", fake_sys):
            starter = glide_start.cache_ordner()
        namespace = {"os": fake_os, "sys": fake_sys}
        exec(self.app_function, namespace)
        app = namespace["bytecode_cache_dir"]()
        with mock.patch.object(rc, "os", fake_os), mock.patch.object(rc, "IS_MACOS", platform == "darwin"), \
                mock.patch.object(rc, "IS_WINDOWS", platform == "win32"):
            config = fake_os.path.join(rc.resolve_default_cache_dir(), "bytecode")
        return starter, app, config

    def test_same_path_on_each_platform(self):
        mac, windows, linux = "/Users/nutzer", "C:\\Users\\nutzer", "/home/nutzer"
        local = windows + "\\AppData\\Local"
        cases = (
            ("darwin", mac, {}, mac + "/Library/Caches/Glide/bytecode"),
            # macOS folgt weder der Windows- noch der XDG-Angabe.
            ("darwin", mac, {"LOCALAPPDATA": "/fremd", "XDG_CACHE_HOME": "/fremd"}, mac + "/Library/Caches/Glide/bytecode"),
            ("win32", windows, {"LOCALAPPDATA": local}, local + "\\Glide\\Cache\\bytecode"),
            ("win32", windows, {}, windows + "\\Glide\\Cache\\bytecode"),
            ("win32", windows, {"LOCALAPPDATA": ""}, windows + "\\Glide\\Cache\\bytecode"),
            ("linux", linux, {"XDG_CACHE_HOME": "/var/cache/nutzer"}, "/var/cache/nutzer/glide/bytecode"),
            ("linux", linux, {}, linux + "/.cache/glide/bytecode"),
            ("linux", linux, {"XDG_CACHE_HOME": ""}, linux + "/.cache/glide/bytecode"),
        )
        for platform, home, environ, expected in cases:
            with self.subTest(platform=platform, environ=environ):
                self.assertEqual(self.resolutions(platform, home, environ), (expected,) * 3)

    def test_cache_override_moves_the_path_object_but_not_the_bytecode(self):
        # `GLIDE_CACHE_DIR` steuert `RuntimePaths.cache_dir`; die Bytecode-Auflösungen kennen es nicht.
        override = os.path.join(tempfile.gettempdir(), "glide-cache-nicht-angelegt")
        data = os.path.join(tempfile.gettempdir(), "glide-daten-nicht-angelegt")
        self.assertEqual(rc.resolve_paths(data_dir=data, env={"GLIDE_CACHE_DIR": override}).cache_dir,
                         os.path.abspath(override))
        self.assertEqual(self.resolutions("linux", "/home/nutzer", {"GLIDE_CACHE_DIR": "/anderswo"}),
                         ("/home/nutzer/.cache/glide/bytecode",) * 3)
        self.assertFalse(os.path.exists(override) or os.path.exists(data))

    def test_relative_cache_home_is_absolute_only_in_runtime_config(self):
        # Bestehender Unterschied: Die Startkopien übernehmen eine relative Angabe unverändert,
        # `runtime_config` löst sie gegen das Arbeitsverzeichnis auf.
        starter, app, config = self.resolutions("linux", "/home/nutzer", {"XDG_CACHE_HOME": "cache"})
        self.assertEqual((starter, app), ("cache/glide/bytecode",) * 2)
        self.assertEqual(config, posixpath.join(posixpath.abspath("cache/glide"), "bytecode"))

    def test_function_source_requires_exactly_one_definition(self):
        self.assertEqual(function_source("x = 1\ndef f():\n    return 1\n\ny = 2\n", "f"), "def f():\n    return 1\n\n")
        for text in ("x = 1\n", "def f():\n    pass\ndef f():\n    pass\n"):
            with self.assertRaises(AssertionError):
                function_source(text, "f")


if __name__ == "__main__":
    unittest.main()
