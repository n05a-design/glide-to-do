# SPDX-License-Identifier: MPL-2.0
"""Prüfungen für die kontrollierte Laufzeitkonfiguration und Pfadentkopplung (WA-49 / WA-39)."""
from pathlib import Path
import os
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
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


if __name__ == "__main__":
    unittest.main()
