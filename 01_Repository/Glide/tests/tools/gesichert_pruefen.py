"""Allgemeiner lokaler Voll-/Laststarter mit unveränderlicher Prüfkopie.

    python -B tests/tools/gesichert_pruefen.py --art voll --timeout 900
    python -B tests/tools/gesichert_pruefen.py --art speicherlast --timeout 900

Kein Netz, keine Nutzerdaten, keine automatische Wiederholung roter Fälle.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from pruefablauf import Pruefablauf, einfrieren


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--art", choices=("voll", "speicherlast", "dauerlauf", "leistung"), default="voll")
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--arbeitsablage", type=Path)
    parser.add_argument("--minuten", type=float, default=10)
    parser.add_argument("--aufgaben", type=int, default=4000)
    args = parser.parse_args()
    if args.timeout <= 0 or args.minuten <= 0 or args.aufgaben <= 0:
        parser.error("Zeitlimits und Bestandsgröße müssen positiv sein")
    repo = Path(__file__).resolve().parents[2]
    frozen, root = einfrieren(repo, args.arbeitsablage)
    guard = Pruefablauf(frozen, args.arbeitsablage)
    if args.art == "voll":
        command = [sys.executable, "-B", str(frozen / "tests/tools/pruefen.py"),
                   "--modus", "voll", "--protokoll", str(root / "protokoll"),
                   "--timeout", str(args.timeout), "--arbeitsablage", str(guard.root.parent)]
    elif args.art == "speicherlast":
        command = [sys.executable, "-B", str(frozen / "tests/integration/test_speicherlast330.py")]
    else:
        script = "dauerlauf.py" if args.art == "dauerlauf" else "leistungspruefung.py"
        command = [sys.executable, "-B", str(frozen / "tests/tools" / script), "--ziel", str(root / "messung.json")]
        if args.art == "dauerlauf":
            command += ["--minuten", str(args.minuten), "--aufgaben", str(args.aufgaben)]
    print(f"Eingefrorene Prüfkopie: {frozen}\nNachweise: {root}\nProzesswächter: {guard.root}", flush=True)
    # Vollprüfung hat ein Limit pro Fall. Der äußere Prozess benötigt ein
    # unabhängiges großzügiges Gesamtbudget; keine Testfälle werden verkürzt.
    timeout = args.timeout * 200 if args.art == "voll" else args.timeout
    try:
        result = guard.command(args.art, command, timeout=timeout, environment=os.environ, cwd=frozen)
    except (OSError, subprocess.TimeoutExpired):
        return 1
    exitcode = result.returncode if result is not None and not guard.stopped else 1
    (root / "abschluss.json").write_text(json.dumps({"exitcode": exitcode,
        "art": args.art, "pruefablauf": str(guard.root / "pruefablauf.json"),
        "release_ready": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exitcode {exitcode}; Rohlogs und Prüfdaten bleiben unter {guard.root}", flush=True)
    return exitcode


if __name__ == "__main__":
    raise SystemExit(main())
