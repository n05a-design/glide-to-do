# SPDX-License-Identifier: MPL-2.0
"""Lokaler, eindeutig identifizierter Framework-Checkpoint (E01, Glide Ecosystem).

Übernimmt `glide_shell` und `glide_bento` mit dem vorhandenen Übernahmewerkzeug
(`shell_uebernehmen.py --mit-bento`) in einen Ordner außerhalb der
Arbeitskopie und legt daneben `CHECKPOINT.json` mit:

- Shell- und Bento-Version, Glide-Systemversion, App-Version,
- Ausgangscommit und Prüfsumme der lokalen, noch nicht committeten
  Framework-Abweichungen (`git diff HEAD` der Frameworkordner plus
  unversionierte Dateien darin) – ein uncommitteter Stand ist so nicht nur
  über HEAD identifiziert,
- Dateimanifest (Pfad, Größe, SHA-256) aller Checkpoint-Dateien,
- Snapshot-Kennung = SHA-256 über Commit, Abweichungsprüfsumme und Manifest,
- öffentliche Schnittstellen je Modul (Klassen und Funktionen ohne `_`),
- Kompatibilitätsangaben (Shell-Mindestversion von Bento, `SHELL_COMPAT_SINCE`),
- bekannte Einschränkungen.

Der Checkpoint enthält keine Nutzerdaten, Sicherungen, Berichte oder
Referenzbilder; nur Framework-Quellen, ihre Verträge und den Lizenztext.
`--pruefen <Ordner>` berechnet Manifest und Kennung neu und vergleicht.

    python3 -B scripts/pflege/framework_checkpoint.py <Zielordner>
    python3 -B scripts/pflege/framework_checkpoint.py --pruefen <Zielordner>
"""
from __future__ import annotations

import argparse
import ast
import datetime as _dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
SRC = REPO / "src" / "glide"
FRAMEWORKS = ("glide_shell", "glide_bento")
NAME = "CHECKPOINT.json"
EINSCHRAENKUNGEN = [
    "Lokaler Entwicklungscheckpoint, keine Veröffentlichung und kein Commit; Quelle ist ein uncommitteter Arbeitsbaum.",
    "Geprüft unter Windows 11 mit Tk 9 und künstlichen Daten; macOS und Linux nativ offen.",
    "Shell vor 1.0: öffentliche Schnittstellen können sich in E02 noch kompatibel erweitern.",
]


def sha(pfad):
    return hashlib.sha256(pathlib.Path(pfad).read_bytes()).hexdigest()


def git(*args, text=True):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True, text=text).stdout


def konstante(datei, name):
    for knoten in ast.parse(datei.read_text(encoding="utf-8")).body:
        if isinstance(knoten, ast.Assign) and any(isinstance(z, ast.Name) and z.id == name for z in knoten.targets):
            if isinstance(knoten.value, ast.Constant):
                return knoten.value.value
    return None


def abweichung():
    """Prüfsumme der lokalen Framework-Abweichungen gegenüber HEAD (versioniert und neu)."""
    pfade = [f"src/glide/{f}" for f in FRAMEWORKS]  # relativ zu `git -C REPO`
    diff = git("diff", "--binary", "HEAD", "--", *pfade, text=False)
    neu = [z for z in git("ls-files", "--others", "--exclude-standard", "--", *pfade).splitlines() if z]
    h = hashlib.sha256(diff)
    for name in sorted(neu):
        h.update(name.encode("utf-8"))
        h.update(bytes.fromhex(sha(REPO / name)))
    return h.hexdigest(), bool(diff) or bool(neu), sorted(neu)


def schnittstellen(paket):
    ergebnis = {}
    for datei in sorted(paket.glob("*.py")):
        baum = ast.parse(datei.read_text(encoding="utf-8"))
        namen = [k.name for k in baum.body if isinstance(k, (ast.ClassDef, ast.FunctionDef)) and not k.name.startswith("_")]
        if namen:
            ergebnis[f"{paket.name}.{datei.stem}"] = namen
    return ergebnis


def manifest(ziel):
    eintraege = []
    for datei in sorted(p for p in ziel.rglob("*") if p.is_file() and p.name != NAME):
        eintraege.append({"path": datei.relative_to(ziel).as_posix(), "size": datei.stat().st_size, "sha256": sha(datei)})
    return eintraege


def kennung(commit, abw, eintraege):
    h = hashlib.sha256(f"{commit}\n{abw}\n".encode("utf-8"))
    for e in eintraege:
        h.update(f"{e['path']}\t{e['sha256']}\n".encode("utf-8"))
    return h.hexdigest()


def erstellen(ziel):
    ziel = pathlib.Path(ziel).resolve()
    if ziel == REPO or REPO in ziel.parents or REPO.parents[1] in ziel.parents:
        raise SystemExit("Zielordner muss außerhalb der Arbeitskopie liegen")
    if ziel.exists() and any(ziel.iterdir()):
        raise SystemExit(f"{ziel} ist nicht leer")
    quelle = ziel / "src"
    quelle.mkdir(parents=True)
    lauf = subprocess.run([sys.executable, "-B", str(REPO / "scripts/pflege/shell_uebernehmen.py"), "--mit-bento",
                           "--unsauber-erlauben", str(quelle)], capture_output=True, text=True)
    if lauf.returncode != 0:
        shutil.rmtree(ziel, ignore_errors=True)
        raise SystemExit("Übernahme fehlgeschlagen:\n" + lauf.stdout[-2000:] + lauf.stderr[-2000:])
    commit = git("rev-parse", "HEAD").strip()
    abw, lokal, neu = abweichung()
    eintraege = manifest(ziel)
    shell_version = konstante(SRC / "glide_shell/__init__.py", "SHELL_VERSION")
    daten = {
        "format": "glide-framework-checkpoint", "version": 1,
        "created": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "shell_version": shell_version,
        "shell_compat_since": konstante(SRC / "glide_shell/__init__.py", "SHELL_COMPAT_SINCE"),
        "bento_version": konstante(SRC / "glide_bento/__init__.py", "BENTO_VERSION"),
        "bento_shell_min_version": konstante(SRC / "glide_bento/__init__.py", "SHELL_MIN_VERSION"),
        "glide_system_version": (REPO / "GLIDE_SYSTEM_VERSION").read_text(encoding="utf-8").strip(),
        "glide_app_version": (REPO / "VERSION").read_text(encoding="utf-8").strip(),
        "source_commit": commit,
        "source_has_local_changes": lokal,
        "local_changes_sha256": abw,
        "local_new_files": [n.split("src/glide/", 1)[-1] for n in neu],
        "files": eintraege,
        "public_interfaces": {**schnittstellen(SRC / "glide_shell"), **schnittstellen(SRC / "glide_bento")},
        "contracts": ["src/glide_shell/DESIGN_RICHTLINIEN.md", "src/glide_shell/KI_MIGRATION_BESTEHENDE_ANWENDUNG.md",
                      "src/glide_shell/AI_MIGRATION_EXISTING_APPS.md"],
        "known_limitations": EINSCHRAENKUNGEN,
    }
    daten["snapshot_id"] = kennung(commit, abw, eintraege)
    (ziel / NAME).write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return daten


def pruefen(ziel):
    ziel = pathlib.Path(ziel)
    daten = json.loads((ziel / NAME).read_text(encoding="utf-8"))
    eintraege = manifest(ziel)
    fehler = []
    if eintraege != daten["files"]:
        alt = {e["path"]: e["sha256"] for e in daten["files"]}
        neu = {e["path"]: e["sha256"] for e in eintraege}
        fehler += [f"abweichend: {p}" for p in sorted(set(alt) | set(neu)) if alt.get(p) != neu.get(p)]
    if kennung(daten["source_commit"], daten["local_changes_sha256"], eintraege) != daten["snapshot_id"]:
        fehler.append("Snapshot-Kennung stimmt nicht")
    return daten, fehler


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ziel")
    parser.add_argument("--pruefen", action="store_true")
    args = parser.parse_args(argv)
    if args.pruefen:
        daten, fehler = pruefen(args.ziel)
        for f in fehler:
            print(f)
        print(f"Checkpoint {daten['snapshot_id'][:16]} · Shell {daten['shell_version']} · Bento {daten['bento_version']} · "
              + ("unverändert" if not fehler else f"{len(fehler)} Abweichung(en)"))
        return 1 if fehler else 0
    daten = erstellen(args.ziel)
    print(f"Checkpoint {daten['snapshot_id'][:16]} · Shell {daten['shell_version']} · Bento {daten['bento_version']} · "
          f"Commit {daten['source_commit'][:12]} · lokale Framework-Abweichungen: {'ja' if daten['source_has_local_changes'] else 'nein'} · "
          f"{len(daten['files'])} Dateien")
    return 0


if __name__ == "__main__":
    sys.exit(main())
