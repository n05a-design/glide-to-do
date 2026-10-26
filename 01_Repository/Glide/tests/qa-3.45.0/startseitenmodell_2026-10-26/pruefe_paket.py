"""Gezielte WA-39-Paketprüfung; keine Vollprüfung und kein Lieferabgleich."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def main():
    commands = [
        ["-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_home_dashboard.py", "-v"],
        ["-m", "unittest", "discover", "-s", "tests/unit", "-p", "test_home_tiles.py", "-v"],
        ["tests/integration/test_startseite3332.py"],
        *[["tests/integration/test_uiux_paket.py", "--fall", case,
           "--report", str(HERE / f"{case}.json")] for case in ("b01", "b02", "b04")],
        ["tests/tools/standpruefung.py"],
    ]
    result = {"scope": "gezielte Paketprüfung WA-39/WA-36", "steps": [], "ok": True}
    with tempfile.TemporaryDirectory(prefix="glide-home-package-") as directory:
        env = dict(os.environ, PYTHONUTF8="1", GLIDE_DATA_DIR=directory, GLIDE_TEST_MODE="1")
        for command in commands:
            run = subprocess.run([sys.executable, "-B", *command], cwd=REPO,
                                 env=env, capture_output=True, text=True, encoding="utf-8", timeout=180)
            result["steps"].append({"command": command, "exitcode": run.returncode,
                                    "stdout": run.stdout, "stderr": run.stderr})
            result["ok"] = result["ok"] and run.returncode == 0
            print(f"{'OK' if run.returncode == 0 else 'ROT'}: {' '.join(command)}", flush=True)
    changed = ["src/glide/app.pyw", "src/glide/home_dashboard.py", "tests/unit/test_home_dashboard.py",
               "tests/integration/test_startseite3332.py", "scripts/pflege/abgleich_07.py",
               "packaging/macos/baue_app.py"]
    for relative in changed:
        ast.parse((REPO / relative).read_text(encoding="utf-8-sig"), filename=relative)
    diff = subprocess.run(["git", "diff", "--check"], cwd=REPO, capture_output=True, text=True)
    result["diff_check"] = {"exitcode": diff.returncode, "output": diff.stdout + diff.stderr}
    result["ok"] = result["ok"] and diff.returncode == 0
    app_tree = ast.parse((REPO / "src/glide/app.pyw").read_text(encoding="utf-8-sig"))
    app_class = next(node for node in app_tree.body if isinstance(node, ast.ClassDef) and node.name == "ListApp")
    source = {"version": (REPO / "VERSION").read_text().strip(), "schema": 26,
              "app_lines": len((REPO / "src/glide/app.pyw").read_text(encoding="utf-8-sig").splitlines()),
              "listapp_lines": app_class.end_lineno - app_class.lineno + 1,
              "listapp_methods": sum(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) for node in app_class.body),
              "sha256": {relative: hashlib.sha256((REPO / relative).read_bytes()).hexdigest() for relative in changed},
              "runtime_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                 for path in sorted((REPO / "src/glide").glob("*.py*")) if path.is_file()}}
    (HERE / "pruefung.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (HERE / "quellstand.json").write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
