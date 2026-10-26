"""Lokale Paketstartprobe ohne ACL-Sperre; kein Hosted-CI-Isolationsnachweis."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paket", type=Path, required=True)
    parser.add_argument("--bericht", type=Path, required=True)
    args = parser.parse_args()
    package = args.paket.resolve()
    executable = package / "Glide.exe"
    if not executable.is_file():
        raise SystemExit("Glide.exe fehlt")
    report = args.bericht.resolve()
    if report.exists():
        raise SystemExit("Für jede Startprobe einen neuen Bericht wählen")
    report.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="glide-package-local-") as work:
        env = dict(os.environ, PATH=str(Path(os.environ["SystemRoot"]) / "System32"),
                   GLIDE_DATA_DIR=str(Path(work) / "data"), GLIDE_TEST_MODE="1", PYTHONUTF8="1")
        for name in ("PYTHONHOME", "PYTHONPATH", "TCL_LIBRARY", "TK_LIBRARY"):
            env.pop(name, None)
        result = subprocess.run([str(executable), "--paket-pruefen", str(report)],
                                cwd=work, env=env, capture_output=True, timeout=180)
    proof = json.loads(report.read_text(encoding="utf-8")) if report.is_file() else {}
    checks = ("eigenstaendiger_pruefstart", "daten_isoliert", "anlegen_abhaken_undo",
              "logo_geladen", "dateilesen", "app_backup_rundlauf")
    ok = (result.returncode == 0 and proof.get("exitcode") == 0
          and proof.get("app_version") == "3.45.0"
          and all(proof.get(name) for name in checks)
          and not proof.get("externe_python_suchpfade") and not proof.get("callbackfehler"))
    summary = {"ok": bool(ok), "scope": "lokale Windows-Startprobe ohne ACL-Sperre",
               "process_exitcode": result.returncode, "strict_acl_isolation_tested": False,
               "executable_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
               "report": report.name, "stdout": result.stdout.decode("utf-8", errors="replace"),
               "stderr": result.stderr.decode("utf-8", errors="replace")}
    report.with_name(report.stem + "_aufruf.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key not in ("stdout", "stderr")}))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
