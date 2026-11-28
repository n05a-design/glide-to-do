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
- bekannte Einschränkungen,
- seit E02: die Übernahmewerkzeuge (`tools/`), den Schnittstellenvergleich zur
  Fassung der Folgeprojekte (`interface_changes`, Standard Shell 0.6.2 aus
  `7dcd8dc0`) und – mit `--ergebnisse DATEI` – die Prüfergebnisse des Laufs.

Der Checkpoint enthält keine Nutzerdaten, Sicherungen, Berichte oder
Referenzbilder; nur Framework-Quellen, ihre Verträge und den Lizenztext.
`--pruefen <Ordner>` berechnet Manifest und Kennung neu und vergleicht.

    python3 -B scripts/pflege/framework_checkpoint.py <Zielordner>
    python3 -B scripts/pflege/framework_checkpoint.py --pruefen <Zielordner>
    python3 -B scripts/pflege/framework_checkpoint.py <Ziel> --basis 7dcd8dc0 --ergebnisse pruefung.json
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
    "Lokaler Entwicklungscheckpoint, keine Veröffentlichung; Quelle kann ein uncommitteter Arbeitsbaum sein (siehe source_has_local_changes).",
    "Geprüft unter Windows 11 mit Tk 9 und künstlichen Daten; macOS und Linux nativ offen.",
    "Shell vor 1.0: öffentliche Schnittstellen können sich bis zur Stabilisierung nach E03 noch kompatibel erweitern.",
    "In Glide produktiv: SearchField, Softwarekatalog/Weitere Programme, Symbolauswahl, begrenzter Symbol-Cache, Bento-Diagramme der Projektübersicht; "
    "nur Galerie/Referenzhosts: ShellButton, Tooltip, Toolbar, WorkspaceHost, ThemeProvider, TaskQueue und die meisten Bento-Kompositionen.",
    "Leistung: gemessen nur in Glide und neutralen Hosts unter Windows; kein Nachweis für STEPS oder Chess & Chains.",
]
WERKZEUGE = ("scripts/pflege/shell_uebernehmen.py", "scripts/pflege/framework_checkpoint.py")
BASIS = "7dcd8dc0"  # Shell 0.6.2 der Folgeprojekte (laut SHELL_MANIFEST.json von STEPS und Chess & Chains, E03 neu geprüft)


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


def _api(text):
    ergebnis = {}
    for knoten in ast.parse(text).body:
        if isinstance(knoten, (ast.FunctionDef, ast.ClassDef)) and not knoten.name.startswith("_"):
            if isinstance(knoten, ast.ClassDef):
                for teil in knoten.body:
                    if isinstance(teil, ast.FunctionDef) and (not teil.name.startswith("_") or teil.name == "__init__"):
                        a = teil.args
                        ergebnis[f"{knoten.name}.{teil.name}"] = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
                ergebnis.setdefault(knoten.name, [])
            else:
                a = knoten.args
                ergebnis[knoten.name] = [x.arg for x in a.posonlyargs + a.args + a.kwonlyargs]
    return ergebnis


def schnittstellen_vergleich(basis):
    """Neue, entfernte und geänderte öffentliche Namen der Shell gegenüber Commit `basis`."""
    ergebnis = {"base_commit": None, "base_shell_version": None, "added_modules": [], "removed_modules": [],
                "added": [], "removed": [], "changed": []}
    try:
        commit = git("rev-parse", basis).strip()
        namen = git("ls-tree", "--name-only", commit, "src/glide/glide_shell/").split()
    except subprocess.CalledProcessError:
        ergebnis["error"] = f"commit {basis} not available"
        return ergebnis
    alt = {}
    for name in namen:
        if name.endswith(".py"):
            alt[pathlib.PurePosixPath(name).stem] = _api(git("show", f"{commit}:./{name}"))
    if "__init__" in alt:
        kopf = git("show", f"{commit}:./src/glide/glide_shell/__init__.py")
        for knoten in ast.parse(kopf).body:
            if isinstance(knoten, ast.Assign) and any(getattr(z, "id", "") == "SHELL_VERSION" for z in knoten.targets):
                ergebnis["base_shell_version"] = knoten.value.value
    neu = {d.stem: _api(d.read_text(encoding="utf-8")) for d in sorted((SRC / "glide_shell").glob("*.py"))}
    ergebnis["base_commit"] = commit
    ergebnis["added_modules"] = sorted(set(neu) - set(alt))
    ergebnis["removed_modules"] = sorted(set(alt) - set(neu))
    for modul in sorted(set(alt) & set(neu)):
        for name, parameter in alt[modul].items():
            if name not in neu[modul]:
                ergebnis["removed"].append(f"{modul}.{name}")
            elif neu[modul][name][:len(parameter)] != parameter:
                ergebnis["changed"].append(f"{modul}.{name}: {parameter} -> {neu[modul][name]}")
        ergebnis["added"] += [f"{modul}.{n}" for n in sorted(set(neu[modul]) - set(alt[modul]))]
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


def erstellen(ziel, basis=BASIS, ergebnisse=None):
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
    werkzeuge = ziel / "tools"
    werkzeuge.mkdir()
    for rel in WERKZEUGE:
        shutil.copy2(REPO / rel, werkzeuge / pathlib.Path(rel).name)
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
                      "src/glide_shell/AI_MIGRATION_EXISTING_APPS.md", "src/glide_shell/AKTUALISIERUNG.md",
                      "src/glide_shell/UPDATING.md", "src/glide_bento/BENTO_DESIGN_CONTRACT.md"],
        "tools": [f"tools/{pathlib.Path(rel).name}" for rel in WERKZEUGE],
        "compatibility": {"shell_compat_since": konstante(SRC / "glide_shell/__init__.py", "SHELL_COMPAT_SINCE"),
                          "bento_requires_shell": konstante(SRC / "glide_bento/__init__.py", "SHELL_MIN_VERSION"),
                          "data_formats_changed": False},
        "interface_changes": schnittstellen_vergleich(basis) if basis else None,
        "verification": json.loads(pathlib.Path(ergebnisse).read_text(encoding="utf-8")) if ergebnisse else None,
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
    parser.add_argument("--basis", default=BASIS, help="Commit der Shell-Fassung der Folgeprojekte für den Schnittstellenvergleich")
    parser.add_argument("--ergebnisse", help="JSON-Datei mit Prüfergebnissen, die in CHECKPOINT.json aufgenommen werden")
    args = parser.parse_args(argv)
    if args.pruefen:
        daten, fehler = pruefen(args.ziel)
        for f in fehler:
            print(f)
        print(f"Checkpoint {daten['snapshot_id'][:16]} · Shell {daten['shell_version']} · Bento {daten['bento_version']} · "
              + ("unverändert" if not fehler else f"{len(fehler)} Abweichung(en)"))
        return 1 if fehler else 0
    daten = erstellen(args.ziel, args.basis, args.ergebnisse)
    print(f"Checkpoint {daten['snapshot_id'][:16]} · Shell {daten['shell_version']} · Bento {daten['bento_version']} · "
          f"Commit {daten['source_commit'][:12]} · lokale Framework-Abweichungen: {'ja' if daten['source_has_local_changes'] else 'nein'} · "
          f"{len(daten['files'])} Dateien")
    return 0


if __name__ == "__main__":
    sys.exit(main())
