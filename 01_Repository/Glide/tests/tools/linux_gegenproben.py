#!/usr/bin/env python3
"""Kalibrierte UI-Erwartungen gegen echte Defekte in isolierten App-Kopien.

Keine Produktionsdatei wird verändert. Jede Mutation muss an ihrer passenden
Beobachtung scheitern, ein Importfehler oder Timeout gilt nicht als Gegenprobe.
"""
from __future__ import annotations
import argparse
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
CASES = (
    ("ueberlauf", "test_mindestgroesse330.py",
     '("header_overflow_button", minimal and not pending, (0, 0))',
     '("header_overflow_button", False, (0, 0))', 'assert app.header_overflow_button.winfo_ismapped()'),
    ("reihenfolge", "test_rueckmeldung330.py",
     'for knopf, rand in soll:\n                knopf.pack(side="right", padx=rand)',
     'for knopf, rand in reversed(soll):\n                knopf.pack(side="right", padx=rand)',
     'assert reihenfolge() == erwartet'),
    ("svg-fähigkeit", "test_befunde330.py",
     'if not self.previews.reads_svg(self.root):\n                raise glide_drawing.DrawingFormatError("SVG braucht Tk 9 (Python 3.14).")',
     'if True:\n                return path', 'SVG ohne SVG-Leser muss verständlich abgelehnt werden'),
    ("scrollen", "test_tempo330.py",
     'def _on_mousewheel(self, event, widget, precise=False):\n        self.note_scrolling()',
     'def _on_mousewheel(self, event, widget, precise=False):\n        return "break"\n        self.note_scrolling()',
     'Scrollereignisse bewegen die lange Prüfansicht nicht'),
    ("datum", "test_planen33313.py",
     'day = value[0]\n        else:', 'day = self.plan_day()\n        else:',
     'assert fresh(a["id"])["planned_date"] == chosen'),
    ("hintergrundvorschau", "test_hintergrund330.py",
     'def hintergrund_sichtbar(*_args):\n            if not backdrop_dirty[0]',
     'def hintergrund_sichtbar(*_args):\n            return\n            if not backdrop_dirty[0]',
     'assert gesehen.get("kacheln") == 6'),
    ("dialogabschluss", "test_fenster330.py",
     'dialog._glide_chrome_jobs = set()\n            dialog.withdraw()\n            dialog._glide_modal_finished.set(True)',
     'dialog._glide_chrome_jobs = set()\n            dialog._glide_modal_finished.set(True)',
     'Esc schließt nicht'),
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protokoll", type=Path, required=True)
    parser.add_argument("--fall", choices=[case[0] for case in CASES])
    parser.add_argument("--basis-ergebnis", type=Path,
                        help="Vollprüfung derselben unveränderten Prüfkandidatenkopie")
    args = parser.parse_args()
    args.protokoll.mkdir(parents=True, exist_ok=True)
    results = []
    basis = (json.loads(args.basis_ergebnis.read_text(encoding="utf-8"))
             if args.basis_ergebnis else None)
    # Die SVG-Gegenprobe gilt gezielt für einen Prüfstand ohne SVG-Leser.
    # Unter Tk 9 wird stattdessen die positive Konvertierungsanforderung rot.
    for name, suite, old, new, observation in CASES:
        if args.fall and name != args.fall:
            continue
        if basis is not None and not any(step["schritt"] == Path(suite).stem and step["status"] == "ausgeführt"
                                         for step in basis["schritte"]):
            results.append({"fall": name, "suite": suite, "gegenprobe_rot": False,
                            "grund": "Positive Basis dieser Suite nicht grün; keine Defekt-Gegenprobe behaupten"})
            continue
        with tempfile.TemporaryDirectory(prefix="glide-linux-defekt-") as folder:
            clone = Path(folder) / "Glide"
            for directory in ("src/glide", "tests/fixtures"):
                shutil.copytree(REPO / directory, clone / directory,
                                ignore=shutil.ignore_patterns("__pycache__", "archiv"))
            target = clone / "tests/integration" / suite
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(REPO / "tests/integration" / suite, target)
            # Einzelne Suiten verwenden weitere Prüfhelfer relativ zum Repo.
            shutil.copytree(REPO / "tests/tools", clone / "tests/tools",
                            ignore=shutil.ignore_patterns("__pycache__"))
            app = clone / "src/glide/app.pyw"
            source = app.read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise ValueError(f"Mutation {name} ist nicht mehr eindeutig")
            source = source.replace(old, new)
            ast.parse(source)
            env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
            command = [sys.executable, "-B", str(target)]
            if sys.platform.startswith("linux") and not env.get("DISPLAY"):
                command = ["xvfb-run", "-a", "--server-args=-screen 0 1400x1100x24", *command]
            if basis is None:
                positive = subprocess.run(command, cwd=clone, env=env, capture_output=True,
                                          text=True, encoding="utf-8", errors="replace", timeout=900)
                (args.protokoll / f"{name}-positiv.log").write_text(positive.stdout + positive.stderr, encoding="utf-8")
                if positive.returncode:
                    results.append({"fall": name, "suite": suite, "gegenprobe_rot": False,
                                    "grund": "Positive Basis dieser Suite nicht grün"})
                    continue
            app.write_text(source, encoding="utf-8")
            run = subprocess.run(command, cwd=clone, env=env, capture_output=True,
                                 text=True, encoding="utf-8", errors="replace", timeout=900)
            output = run.stdout + run.stderr
            (args.protokoll / f"{name}.log").write_text(output, encoding="utf-8")
            matched = observation in output
            if name == "svg-fähigkeit" and 'assert svg.endswith(".png")' in output:
                matched = True
            ok = run.returncode != 0 and 'AssertionError' in output and matched
            results.append({"fall": name, "suite": suite, "exitcode": run.returncode,
                            "erwartete_beobachtung": observation, "gegenprobe_rot": ok})
            print(f"{name}: {'passend rot' if ok else 'NICHT BELEGT'}", flush=True)
    (args.protokoll / "ergebnis.json").write_text(json.dumps(
        {"plattform": sys.platform, "gegenproben": results}, ensure_ascii=False, indent=2) + "\n")
    return 0 if all(result["gegenprobe_rot"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
