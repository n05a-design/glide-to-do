# SPDX-License-Identifier: MPL-2.0
"""Übernimmt das Paket `glide_shell` in ein Folgeprojekt und prüft bestehende Kopien (D95).

Aufruf (Ziel ist der Quellordner des Folgeprojekts, in dem `glide_shell/` liegen soll):

    python3 -B scripts/pflege/shell_uebernehmen.py <Ziel>             # anlegen oder aktualisieren
    python3 -B scripts/pflege/shell_uebernehmen.py --pruefen <Ziel>   # nur prüfen, nichts schreiben
    python3 -B scripts/pflege/shell_uebernehmen.py --ersetzen <Ziel>  # lokale Änderungen überschreiben

Das Werkzeug kopiert alle `*.py` und die Anleitungen `README.md`/`README.de.md`
aus `src/glide/glide_shell` nach
`<Ziel>/glide_shell` und schreibt daneben `SHELL_MANIFEST.json` mit
`SHELL_VERSION`, Glide-Systemversion, Quell-Commit (falls bekannt), ob das
Paket diesem Commit entspricht (`quelle_unveraendert`), und SHA-256 jeder Datei. Beim Aktualisieren gilt:

- Stimmt die Kopie mit ihrem eigenen Manifest überein, wird sie ersetzt.
  Dateien, die das alte Manifest nennt und die es in der Quelle nicht mehr
  gibt, werden entfernt; Dateien ohne Manifesteintrag bleiben stehen.
- Weicht eine Datei von ihrem Manifest ab oder fehlt das Manifest bei einem
  nicht leeren Ordner, bricht das Werkzeug mit Exitcode 2 ab; `--ersetzen`
  überschreibt dann bewusst.

`--pruefen` meldet je Datei `aktuell`, `veraltet` (unverändert, aber älter
als die Quelle), `verändert` (abweichend vom eigenen Manifest), `fehlt` oder
`neu in der Quelle`; Exitcode 0 nur, wenn alles aktuell ist.

Exitcodes: 0 in Ordnung, 1 Prüfung mit Abweichung, 2 Übernahme verweigert.
"""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
QUELLE = REPO / "src" / "glide" / "glide_shell"
PAKET = "glide_shell"
MANIFEST = "SHELL_MANIFEST.json"
# Quelltext und die Anleitung für Folgeprojekte (README.md, README.de.md).
ANTEILE = (".py", ".md")


def sha(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def shell_version(ordner=QUELLE):
    baum = ast.parse((ordner / "__init__.py").read_text(encoding="utf-8"))
    for knoten in baum.body:
        if (isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant)
                and any(getattr(z, "id", None) == "SHELL_VERSION" for z in knoten.targets)):
            return knoten.value.value
    raise SystemExit("SHELL_VERSION fehlt in glide_shell/__init__.py")


def quell_commit():
    try:
        lauf = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True,
                              text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return (lauf.stdout.strip() or None) if lauf.returncode == 0 else None


def quelle_unveraendert():
    """True, wenn `glide_shell` dem Quell-Commit entspricht; None ohne Git."""
    try:
        lauf = subprocess.run(["git", "-C", str(REPO), "status", "--porcelain", "--", str(QUELLE)],
                              capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return not lauf.stdout.strip() if lauf.returncode == 0 else None


def quelldateien():
    return {p.name: sha(p) for p in sorted(QUELLE.iterdir()) if p.is_file() and p.suffix in ANTEILE}


def manifest_lesen(ordner):
    pfad = ordner / MANIFEST
    if not pfad.is_file():
        return None
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    dateien = daten.get("dateien")
    return daten if isinstance(dateien, dict) else None


def schreiben_atomar(ziel, inhalt):
    fd, temp = tempfile.mkstemp(dir=ziel.parent, prefix="." + ziel.name + ".")
    try:
        with os.fdopen(fd, "wb") as datei:
            datei.write(inhalt)
        os.replace(temp, ziel)
    except BaseException:
        pathlib.Path(temp).unlink(missing_ok=True)
        raise


def lokale_abweichungen(ordner, manifest):
    """Dateien der Kopie, die nicht mehr ihrem eigenen Manifest entsprechen."""
    abweichend = []
    for name, wert in sorted(manifest["dateien"].items()):
        pfad = ordner / name
        if not pfad.is_file():
            abweichend.append((name, "fehlt"))
        elif sha(pfad) != wert:
            abweichend.append((name, "verändert"))
    return abweichend


def pruefen(ordner):
    quelle = quelldateien()
    manifest = manifest_lesen(ordner)
    eigen = manifest["dateien"] if manifest else {}
    zeilen = []
    for name in sorted(set(quelle) | set(eigen)):
        pfad = ordner / name
        if name not in quelle:
            zeilen.append((name, "nicht mehr in der Quelle"))
        elif not pfad.is_file():
            zeilen.append((name, "fehlt" if name in eigen else "neu in der Quelle"))
        elif sha(pfad) == quelle[name]:
            zeilen.append((name, "aktuell"))
        elif name in eigen and sha(pfad) == eigen[name]:
            zeilen.append((name, "veraltet"))
        else:
            zeilen.append((name, "verändert"))
    return manifest, zeilen


def uebernehmen(ordner, ersetzen=False):
    ordner.mkdir(parents=True, exist_ok=True)
    manifest = manifest_lesen(ordner)
    vorhanden = sorted(p.name for p in ordner.iterdir() if p.name not in (MANIFEST, "__pycache__"))
    if manifest is None and vorhanden and not ersetzen:
        return 2, [f"{ordner}: Ordner ist nicht leer und hat kein {MANIFEST} – mit --ersetzen bewusst überschreiben"]
    if manifest is not None and not ersetzen:
        abweichend = lokale_abweichungen(ordner, manifest)
        if abweichend:
            return 2, [f"{name}: {art} gegenüber {MANIFEST} – mit --ersetzen bewusst überschreiben"
                       for name, art in abweichend]
    quelle = quelldateien()
    meldungen = []
    for name in quelle:
        schreiben_atomar(ordner / name, (QUELLE / name).read_bytes())
    for name in sorted(set(manifest["dateien"]) - set(quelle)) if manifest else ():
        (ordner / name).unlink(missing_ok=True)
        meldungen.append(f"{name}: entfernt (nicht mehr Teil der Shell)")
    fremd = sorted(n for n in vorhanden if n not in quelle and not (manifest and n in manifest["dateien"]))
    meldungen.extend(f"{name}: bleibt stehen (kein Teil der Shell)" for name in fremd)
    daten = {
        "paket": PAKET,
        "shell_version": shell_version(),
        "glide_system_version": (REPO / "GLIDE_SYSTEM_VERSION").read_text(encoding="utf-8").strip(),
        "quell_commit": quell_commit(),
        "quelle_unveraendert": quelle_unveraendert(),
        "lizenz": "MPL-2.0",
        "dateien": quelle,
    }
    schreiben_atomar(ordner / MANIFEST, (json.dumps(daten, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    for name, art in pruefen(ordner)[1]:
        if art != "aktuell":
            return 1, meldungen + [f"{name}: {art} nach dem Kopieren"]
    meldungen.append(f"glide_shell {daten['shell_version']} mit {len(quelle)} Dateien nach {ordner}")
    return 0, meldungen


def zielordner(text):
    ziel = pathlib.Path(text).expanduser().resolve()
    ordner = ziel if ziel.name == PAKET else ziel / PAKET
    quelle = QUELLE.resolve()
    if ordner == quelle or quelle in ordner.parents or (REPO / "src").resolve() in ordner.parents:
        raise SystemExit("Ziel liegt im Glide-Quellbaum; Folgeprojekte übernehmen die Shell in ihren eigenen Ordner")
    return ordner


def main(argv=None):
    parser = argparse.ArgumentParser(description="glide_shell in ein Folgeprojekt übernehmen oder eine Kopie prüfen")
    parser.add_argument("ziel", help="Quellordner des Folgeprojekts (oder dessen glide_shell-Ordner)")
    gruppe = parser.add_mutually_exclusive_group()
    gruppe.add_argument("--pruefen", action="store_true", help="nur prüfen, nichts schreiben")
    gruppe.add_argument("--ersetzen", action="store_true", help="lokale Änderungen bewusst überschreiben")
    args = parser.parse_args(argv)
    ordner = zielordner(args.ziel)
    if args.pruefen:
        if not ordner.is_dir():
            print(f"{ordner}: keine Kopie vorhanden")
            return 1
        manifest, zeilen = pruefen(ordner)
        stand = manifest.get("shell_version") if manifest else "ohne Manifest"
        print(f"Kopie {stand}, Quelle {shell_version()}")
        for name, art in zeilen:
            print(f"  {name}: {art}")
        return 0 if manifest and all(art == "aktuell" for _, art in zeilen) else 1
    code, meldungen = uebernehmen(ordner, ersetzen=args.ersetzen)
    for zeile in meldungen:
        print(zeile)
    return code


if __name__ == "__main__":
    sys.exit(main())
