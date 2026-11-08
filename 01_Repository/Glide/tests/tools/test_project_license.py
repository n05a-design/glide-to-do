"""Neue Pakete führen MPL-Original und einen eindeutigen Quellbezug mit."""
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[2] / "packaging/paket"
sys.path.insert(0, str(TOOLS))
from project_license import stage_project_license


class ProjectLicenseTests(unittest.TestCase):
    def fixture(self, root):
        repo = root / "01_Repository/Glide"
        (repo / "src/glide").mkdir(parents=True)
        (repo / "src/glide/app.pyw").write_text('APP_VERSION = "3.50.6"\n')
        (root / "LICENSE").write_bytes((TOOLS.parents[3] / "LICENSE").read_bytes())
        (repo / "LICENSE.md").write_text("Mozilla Public License 2.0 (MPL-2.0)\n")
        def git(*args):
            return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.STDOUT).decode().strip()
        git("init", "-q")
        git("add", ".")
        git("-c", "user.name=License Test", "-c", "user.email=test@example.invalid",
            "commit", "-qm", "fixture")
        return repo, git("rev-parse", "HEAD")

    def test_exact_license_bytes_hashes_and_commit_source_survive_staging(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            repo, revision = self.fixture(root)
            record = stage_project_license(repo, root / "package", repo / "src/glide")
            self.assertEqual(record["version"], "MPL-2.0")
            self.assertTrue(record["source"].endswith("/tree/" + revision))
            self.assertEqual((root / "package/Glide-MPL-2.0.txt").read_bytes(), (root / "LICENSE").read_bytes())
            notice = (root / "package/Glide-Quellcode.txt").read_text(encoding="utf-8")
            self.assertIn("/archive/" + revision + ".zip", notice)
            for name, digest in record["files"].items():
                self.assertEqual(hashlib.sha256((root / "package" / name).read_bytes()).hexdigest(), digest)

    def test_modified_untracked_or_foreign_sources_cannot_claim_an_old_commit(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            repo, _ = self.fixture(root)
            with self.assertRaisesRegex(ValueError, "Repository-Quellbaum"):
                stage_project_license(repo, root / "package", root / "other")
            added = repo / "src/glide/new.py"
            added.write_text("# new source\n")
            with self.assertRaisesRegex(ValueError, "Git-Commit"):
                stage_project_license(repo, root / "package")
            added.unlink()
            (repo / "src/glide/app.pyw").write_text("# changed source\n")
            with self.assertRaisesRegex(ValueError, "Git-Commit"):
                stage_project_license(repo, root / "package")


if __name__ == "__main__":
    unittest.main()
