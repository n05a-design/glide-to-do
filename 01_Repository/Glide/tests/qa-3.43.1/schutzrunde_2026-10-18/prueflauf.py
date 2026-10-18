"""Gezielte Nachprüfung der Schutzrunde, keine Vollprüfung oder Lieferung."""
import argparse
import ast
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

QA = Path(__file__).resolve().parent
REPO = QA.parents[2]
APP = REPO / "src/glide/app.pyw"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    rows, owners = [], []
    class Calls(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            owners.append(node.name)
            self.generic_visit(node)
            owners.pop()

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute) and node.func.attr in {
                "flush_rich_note", "flush_drawing_editor", "editor_switch_allowed",
                "require_editor_flush", "output_editor_ready", "prepare_inspector_switch",
                "guarded_structural_change", "rollback_to_undo_depth"}:
                rows.append({"aufrufer": ".".join(owners), "zeile": node.lineno,
                             "aufruf": ast.unparse(node)})
            self.generic_visit(node)
    Calls().visit(ast.parse(APP.read_text(encoding="utf-8")))
    (QA / "aufrufer.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("gruppe", choices=("bereiche", "gegenprobe", "units", "grundstufe", "schutz"))
    parser.add_argument("--basis", type=Path)
    args = parser.parse_args()
    inventory()
    integration = REPO / "tests/integration"
    if args.gruppe == "bereiche":
        jobs = [
            ("schutzrunde", [str(integration / "test_schutzrunde.py"), "--report", str(QA / "pflichtsuite.json")]),
            ("wiederholen", [str(integration / "test_wiederholen.py"), "--report", str(QA / "wiederholen.json")]),
            ("datenintegritaet", [str(integration / "test_datenintegritaet.py")]),
            ("editorabbau", [str(integration / "test_editor3338.py")]),
            ("vorlagen", [str(integration / "test_template_workflows.py")]),
            ("notion_restore", [str(integration / "test_import3410.py"), "--report", str(QA / "notion_restore.json")]),
            ("seiten", [str(integration / "test_seiten33318.py")]),
        ]
    elif args.gruppe == "schutz":
        jobs = [("schutzrunde", [str(integration / "test_schutzrunde.py"), "--report", str(QA / "pflichtsuite.json")])]
    elif args.gruppe == "gegenprobe":
        if args.basis is None:
            parser.error("--basis muss die aus 9ec474b extrahierte app.pyw nennen")
        jobs = [("gegenprobe_9ec474b", [str(integration / "test_schutzrunde.py"), "--app", str(args.basis),
                                      "--report", str(QA / "gegenprobe_9ec474b.json")])]
    elif args.gruppe == "units":
        jobs = [("units", ["-m", "unittest", "discover", "-s", "tests/unit"]),
                ("werkzeuge", ["-m", "unittest", "discover", "-s", "tests/tools", "-p", "test_*.py"])]
    else:
        # Die vorhandene CI-Grundstufe prüft ihren festgelegten Umfang; der
        # abweichende Lieferstand bleibt ohne --lieferstand-streng ein Hinweis.
        jobs = [("grundstufe", ["tests/tools/ci_grundstufe.py", "--protokoll", str(QA / "ci")])]
    result = {"datum": datetime.now().isoformat(timespec="seconds"), "gruppe": args.gruppe,
              "plattform": sys.platform, "python": sys.version.split()[0], "app_sha256": digest(APP),
              "test_sha256": digest(integration / "test_schutzrunde.py"), "pruefungen": []}
    for name, command in jobs:
        print("START " + name, flush=True)
        started = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="glide-schutz-check-") as temporary:
            env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                       GLIDE_DATA_DIR=temporary, GLIDE_TEST_MODE="1")
            try:
                run = subprocess.run([sys.executable, "-B", *command], cwd=REPO, env=env,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     encoding="utf-8", errors="replace", timeout=900)
                output, code = run.stdout, run.returncode
            except subprocess.TimeoutExpired as exc:
                output, code = str(exc), -1
        (QA / (name + ".log")).write_text(output, encoding="utf-8")
        row = {"name": name, "exitcode": code, "sekunden": round(time.monotonic() - started, 2),
               "protokoll": name + ".log"}
        result["pruefungen"].append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        result["quelle_unveraendert"] = digest(APP) == result["app_sha256"]
        (QA / (args.gruppe + ".json")).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(r["exitcode"] == 0 for r in result["pruefungen"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
