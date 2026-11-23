# SPDX-License-Identifier: MPL-2.0
"""Übernimmt das Paket `glide_shell` in ein Folgeprojekt und prüft bestehende Kopien (D95).

Aufruf (Ziel ist der Quellordner des Folgeprojekts, in dem `glide_shell/` liegen soll):

    python3 -B scripts/pflege/shell_uebernehmen.py <Ziel>                   # anlegen oder aktualisieren
    python3 -B scripts/pflege/shell_uebernehmen.py --commit <Rev> <Ziel>    # reproduzierbar aus einem Commit
    python3 -B scripts/pflege/shell_uebernehmen.py --pruefen <Ziel>         # nur prüfen, nichts schreiben
    python3 -B scripts/pflege/shell_uebernehmen.py --ersetzen <Ziel>        # lokale Änderungen überschreiben

Das Werkzeug kopiert alle `*.py` und `*.md` aus `src/glide/glide_shell` sowie
den vollständigen Lizenztext `LICENSE` (MPL-2.0) aus der Repository-Wurzel nach
`<Ziel>/glide_shell` und schreibt daneben `SHELL_MANIFEST.json` mit
`SHELL_VERSION`, Glide-Systemversion, Quell-Commit, ob die Quelle diesem Commit
entspricht (`quelle_unveraendert`), Lizenz und SHA-256 jeder Datei.

Quelle:

- Ohne `--commit` dient die Arbeitskopie als Quelle. Ist sie im Shell-Ordner
  oder beim Lizenztext lokal verändert (auch unversionierte Dateien), verweigert
  das Werkzeug die Übernahme mit Exitcode 3; `--unsauber-erlauben` übernimmt
  bewusst und vermerkt `quelle_unveraendert: false`.
- Mit `--commit <Rev>` liest das Werkzeug genau die versionierten Dateien dieses
  Commits aus Git, unabhängig von der Arbeitskopie (reproduzierbare Übernahme).

Ziel:

- Stimmt die Kopie mit ihrem eigenen, gültigen Manifest überein, wird sie
  ersetzt. Dateien, die das alte Manifest nennt und die es in der Quelle nicht
  mehr gibt, werden entfernt; Dateien ohne Manifesteintrag bleiben stehen.
  Liefert die Shell neu eine Datei, die es in der Kopie schon ohne
  Manifesteintrag und mit anderem Inhalt gibt, bricht das Werkzeug ab.
- Weicht eine Datei von ihrem Manifest ab, ist das Manifest ungültig oder fehlt
  es bei einem nicht leeren Ordner, bricht das Werkzeug ab; `--ersetzen`
  überschreibt dann bewusst.

`--pruefen` meldet je Datei `aktuell`, `veraltet` (unverändert, aber älter
als die Quelle), `verändert` (abweichend vom eigenen Manifest), `fehlt`,
`neu in der Quelle`, `nicht mehr in der Quelle` oder `zusätzlich` (ein Modul
ohne Manifesteintrag, das als `glide_shell.<name>` importierbar wäre) sowie
Verstöße gegen das Manifestschema; Exitcode 0 nur, wenn alles aktuell ist.
Ohne Glide-Checkout prüft das Folgeprojekt seine Kopie mit
`python -m glide_shell.selftest` (Prüfung `manifest`).

Exitcodes: 0 in Ordnung, 1 Prüfung mit Abweichung, 2 Übernahme verweigert
(Konflikt im Ziel), 3 Quelle unbrauchbar (fehlt, beschädigt, lokal verändert
ohne Zustimmung oder Commit unbekannt).
"""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
QUELLE = REPO / "src" / "glide" / "glide_shell"
LIZENZ = REPO.parents[1] / "LICENSE"
PAKET = "glide_shell"
MANIFEST = "SHELL_MANIFEST.json"
LIZENZDATEI = "LICENSE"
# Quelltext und die Anleitungen für Folgeprojekte; dazu der Lizenztext.
ANTEILE = (".py", ".md")
SEMVER = re.compile(r"\d+\.\d+\.\d+")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
OK, ABWEICHUNG, VERWEIGERT, QUELLFEHLER = 0, 1, 2, 3


class QuellFehler(Exception):
    """Die Quelle ist nicht nutzbar (Exitcode 3)."""


def sha(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def sha_bytes(inhalt):
    return hashlib.sha256(inhalt).hexdigest()


def version_aus_text(text):
    """SHELL_VERSION aus dem Quelltext von `__init__.py`; None, wenn sie fehlt oder kein SemVer ist."""
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return None
    for knoten in baum.body:
        if (isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant)
                and any(getattr(z, "id", None) == "SHELL_VERSION" for z in knoten.targets)):
            wert = knoten.value.value
            return wert if isinstance(wert, str) and SEMVER.fullmatch(wert) else None
    return None


def shell_version(ordner=QUELLE):
    pfad = ordner / "__init__.py"
    wert = version_aus_text(pfad.read_text(encoding="utf-8")) if pfad.is_file() else None
    if wert is None:
        raise QuellFehler(f"{pfad}: SHELL_VERSION fehlt oder ist kein SemVer")
    return wert


def _git(*argumente, text=True):
    try:
        return subprocess.run(["git", "-C", str(REPO), *argumente], capture_output=True, text=text, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None


def quell_commit():
    lauf = _git("rev-parse", "HEAD")
    return (lauf.stdout.strip() or None) if lauf and lauf.returncode == 0 else None


def quelle_unveraendert():
    """True, wenn `glide_shell` und der Lizenztext dem Quell-Commit entsprechen; None ohne Git."""
    lauf = _git("status", "--porcelain", "--untracked-files=all", "--", str(QUELLE), str(LIZENZ))
    return not lauf.stdout.strip() if lauf and lauf.returncode == 0 else None


def _quelle_arbeitskopie(unsauber_erlauben):
    if not (QUELLE / "__init__.py").is_file():
        raise QuellFehler(f"{QUELLE}: Shell-Quelle fehlt")
    if not LIZENZ.is_file():
        raise QuellFehler(f"{LIZENZ}: Lizenztext fehlt")
    unveraendert = quelle_unveraendert()
    if unveraendert is False and not unsauber_erlauben:
        raise QuellFehler(f"{QUELLE}: lokal verändert gegenüber dem Commit – committen, mit --commit "
                          "aus einem Commit übernehmen oder mit --unsauber-erlauben bewusst übernehmen")
    dateien = {p.name: p.read_bytes() for p in sorted(QUELLE.iterdir()) if p.is_file() and p.suffix in ANTEILE}
    dateien[LIZENZDATEI] = LIZENZ.read_bytes()
    system = REPO / "GLIDE_SYSTEM_VERSION"
    return {"dateien": dateien, "commit": quell_commit(), "unveraendert": unveraendert,
            "system": system.read_text(encoding="utf-8").strip() if system.is_file() else None}


def _git_datei(commit, pfad):
    lauf = _git("show", f"{commit}:{pfad}", text=False)
    if not lauf or lauf.returncode != 0:
        raise QuellFehler(f"{commit[:12]}:{pfad} fehlt im Commit")
    return lauf.stdout


def _quelle_commit(rev):
    lauf = _git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if not lauf or lauf.returncode != 0 or not lauf.stdout.strip():
        raise QuellFehler(f"{rev}: Commit unbekannt")
    commit = lauf.stdout.strip()
    praefix = _git("rev-parse", "--show-prefix").stdout.strip()
    ordner = f"{praefix}src/glide/glide_shell/"
    liste = _git("ls-tree", "--full-tree", "--name-only", commit, ordner)
    namen = [pathlib.PurePosixPath(z).name for z in liste.stdout.splitlines()] if liste.returncode == 0 else []
    namen = sorted(n for n in namen if pathlib.PurePosixPath(n).suffix in ANTEILE)
    if "__init__.py" not in namen:
        raise QuellFehler(f"{commit[:12]}: Shell-Quelle fehlt im Commit")
    dateien = {n: _git_datei(commit, ordner + n) for n in namen}
    dateien[LIZENZDATEI] = _git_datei(commit, LIZENZDATEI)
    system = _git_datei(commit, f"{praefix}GLIDE_SYSTEM_VERSION").decode("utf-8").strip()
    return {"dateien": dateien, "commit": commit, "unveraendert": True, "system": system}


def quelle_lesen(commit=None, unsauber_erlauben=False):
    """Liefert die zu übernehmende Quelle; QuellFehler, wenn sie fehlt, beschädigt oder unsauber ist."""
    quelle = _quelle_commit(commit) if commit else _quelle_arbeitskopie(unsauber_erlauben)
    try:
        version = version_aus_text(quelle["dateien"]["__init__.py"].decode("utf-8"))
    except UnicodeDecodeError:
        version = None
    if version is None:
        raise QuellFehler("__init__.py der Quelle: SHELL_VERSION fehlt oder ist kein SemVer")
    quelle["version"] = version
    quelle["hashes"] = {name: sha_bytes(inhalt) for name, inhalt in quelle["dateien"].items()}
    return quelle


def quelldateien():
    """SHA-256 der Shell-Dateien der Arbeitskopie (ohne Sauberkeitsprüfung)."""
    return quelle_lesen(unsauber_erlauben=True)["hashes"]


def manifest_fehler(daten, ordner=None):
    """Verstöße gegen das Manifestschema; leer, wenn das Manifest gültig und in sich stimmig ist."""
    if not isinstance(daten, dict):
        return ["kein JSON-Objekt"]
    fehler = []
    dateien = daten.get("dateien")
    if daten.get("paket") != PAKET:
        fehler.append(f"paket ist nicht {PAKET}")
    if daten.get("lizenz") != "MPL-2.0":
        fehler.append("lizenz ist nicht MPL-2.0")
    if not (isinstance(daten.get("shell_version"), str) and SEMVER.fullmatch(daten["shell_version"])):
        fehler.append("shell_version fehlt oder ist kein SemVer")
    commit = daten.get("quell_commit")
    if commit is not None and not (isinstance(commit, str) and HEX40.fullmatch(commit)):
        fehler.append("quell_commit ist kein Commit-Hash")
    if not isinstance(dateien, dict) or "__init__.py" not in dateien:
        return fehler + ["dateien fehlt oder nennt kein __init__.py"]
    for name, wert in sorted(dateien.items()):
        if (not isinstance(name, str) or name in ("", ".", "..") or "/" in name or "\\" in name or
                name == MANIFEST or name.startswith(".") or ".." in name or os.path.basename(name) != name):
            fehler.append(f"unzulässiger Dateiname {name!r}")
        elif not (isinstance(wert, str) and HEX64.fullmatch(wert)):
            fehler.append(f"{name}: kein SHA-256")
        elif ordner is not None and (ordner / name).is_symlink():
            fehler.append(f"{name}: symbolischer Link ist unzulässig")
    if ordner is not None and (ordner / MANIFEST).is_symlink():
        fehler.append(f"{MANIFEST}: symbolischer Link ist unzulässig")
    if ordner is not None and not fehler and (ordner / "__init__.py").is_file():
        version = version_aus_text((ordner / "__init__.py").read_text(encoding="utf-8", errors="replace"))
        if version != daten["shell_version"]:
            fehler.append(f"shell_version {daten['shell_version']} widerspricht __init__.py ({version})")
    return fehler


def manifest_lesen(ordner):
    """(Manifest, Fehlerliste); (None, []) ohne Manifest."""
    pfad = ordner / MANIFEST
    if not pfad.is_file():
        return None, []
    if pfad.is_symlink():
        return {}, [f"{MANIFEST}: symbolischer Link ist unzulässig"]
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}, ["nicht lesbar"]
    return daten, manifest_fehler(daten, ordner)


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
        if pfad.is_symlink():
            abweichend.append((name, "symbolischer Link"))
        elif not pfad.is_file():
            abweichend.append((name, "fehlt"))
        elif sha(pfad) != wert:
            abweichend.append((name, "verändert"))
    return abweichend


def fremde_kollisionen(ordner, manifest, quelle):
    """Eigene Dateien ohne Manifesteintrag, die eine neue Shell-Datei gleichen Namens überschreiben würde."""
    return [name for name in sorted(quelle) if name not in manifest["dateien"]
            and (ordner / name).is_file() and sha(ordner / name) != quelle[name]]


def zusaetzliche_module(ordner, bekannt):
    """Module im Paketordner ohne Eintrag, die als `glide_shell.<name>` importierbar wären."""
    return sorted(p.name for p in ordner.iterdir()
                  if p.name not in bekannt and (p.suffix == ".py" or (p.is_dir() and (p / "__init__.py").is_file())))


def pruefen(ordner, quelle=None):
    """(Manifest, Zeilen) der Kopie gegenüber der Quelle; Manifestfehler stehen als Zeilen `SHELL_MANIFEST.json`."""
    quelle = quelle if quelle is not None else quelldateien()
    manifest, fehler = manifest_lesen(ordner)
    eigen = manifest["dateien"] if manifest and not fehler else {}
    zeilen = [(MANIFEST, f"ungültig: {f}") for f in fehler]
    for name in sorted(set(quelle) | set(eigen)):
        pfad = ordner / name
        if pfad.is_symlink():
            zeilen.append((name, "symbolischer Link (unzulässig)"))
        elif name not in quelle:
            zeilen.append((name, "nicht mehr in der Quelle"))
        elif not pfad.is_file():
            zeilen.append((name, "fehlt" if name in eigen else "neu in der Quelle"))
        elif sha(pfad) == quelle[name]:
            zeilen.append((name, "aktuell"))
        elif name in eigen and sha(pfad) == eigen[name]:
            zeilen.append((name, "veraltet"))
        else:
            zeilen.append((name, "verändert"))
    zeilen.extend((name, "zusätzlich, ohne Manifesteintrag als Modul importierbar")
                  for name in zusaetzliche_module(ordner, set(quelle) | set(eigen) | {"__pycache__"}))
    return (manifest if not fehler else None), zeilen


def _verweigern(ordner, manifest, fehler, quelle):
    """Gründe, die Übernahme ohne `--ersetzen` abzulehnen; leer, wenn sie gefahrlos ist."""
    vorhanden = [p.name for p in ordner.iterdir() if p.name not in (MANIFEST, "__pycache__")]
    hinweis = " – mit --ersetzen bewusst überschreiben"
    symlinks = [p.name for p in ordner.iterdir() if p.is_symlink()]
    if symlinks:
        return [f"{name}: symbolischer Link im Zielordner (unzulässig){hinweis}" for name in sorted(symlinks)]
    if manifest is None:
        return [f"{ordner}: Ordner ist nicht leer und hat kein {MANIFEST}{hinweis}"] if vorhanden else []
    if fehler:
        return [f"{MANIFEST}: ungültig ({f}){hinweis}" for f in fehler]
    gruende = [f"{name}: {art} gegenüber {MANIFEST}{hinweis}" for name, art in lokale_abweichungen(ordner, manifest)]
    gruende += [f"{name}: eigene Datei ohne Manifesteintrag, die Shell liefert jetzt dieselbe Datei{hinweis}"
                for name in fremde_kollisionen(ordner, manifest, quelle)]
    return gruende


def uebernehmen(ordner, ersetzen=False, quelle=None):
    quelle = quelle if quelle is not None else quelle_lesen(unsauber_erlauben=True)
    ordner_existierte = ordner.exists()
    ordner.mkdir(parents=True, exist_ok=True)
    manifest, fehler = manifest_lesen(ordner)
    if not ersetzen:
        gruende = _verweigern(ordner, manifest, fehler, quelle["hashes"])
        if gruende:
            if not ordner_existierte and not any(ordner.iterdir()):
                ordner.rmdir()
            return VERWEIGERT, gruende

    # Vorbereitung Rollback-Sicherung des bestehenden Zustands
    backup_temp = tempfile.TemporaryDirectory(prefix="glide-shell-backup-")
    backup_ordner = pathlib.Path(backup_temp.name)
    try:
        for item in ordner.iterdir():
            if item.name == "__pycache__":
                continue
            ziel_backup = backup_ordner / item.name
            if item.is_symlink():
                ziel_backup.symlink_to(os.readlink(item))
            elif item.is_file():
                shutil.copy2(item, ziel_backup)
            elif item.is_dir():
                shutil.copytree(item, ziel_backup, symlinks=True)

        alt = manifest["dateien"] if manifest and not fehler else {}
        vorhanden = sorted(p.name for p in ordner.iterdir() if p.name not in (MANIFEST, "__pycache__"))
        meldungen = []

        # Schritt 1: Quell-Dateien schreiben
        for name, inhalt in quelle["dateien"].items():
            schreiben_atomar(ordner / name, inhalt)

        # Schritt 2: Veraltete Shell-Dateien entfernen
        for name in sorted(set(alt) - set(quelle["dateien"])):
            (ordner / name).unlink(missing_ok=True)
            meldungen.append(f"{name}: entfernt (nicht mehr Teil der Shell)")

        # Schritt 3: Fremde Dateien beibehalten
        fremd = sorted(n for n in vorhanden if n not in quelle["dateien"] and n not in alt)
        meldungen.extend(f"{name}: bleibt stehen (kein Teil der Shell)" for name in fremd)

        # Schritt 4: Manifest schreiben
        daten = {"paket": PAKET, "shell_version": quelle["version"], "glide_system_version": quelle["system"],
                 "quell_commit": quelle["commit"], "quelle_unveraendert": quelle["unveraendert"],
                 "lizenz": "MPL-2.0", "dateien": quelle["hashes"]}
        schreiben_atomar(ordner / MANIFEST, (json.dumps(daten, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

        # Schritt 5: Verifizierung des Ergebnisses
        abw = [f"{name}: {art} nach dem Kopieren" for name, art in pruefen(ordner, quelle["hashes"])[1] if art != "aktuell"]
        if abw:
            raise RuntimeError("; ".join(abw))

        herkunft = (quelle["commit"] or "ohne Git")[:12] + ("" if quelle["unveraendert"] is not False else " + lokale Änderungen")
        meldungen.append(f"glide_shell {quelle['version']} ({herkunft}) mit {len(quelle['dateien'])} Dateien nach {ordner}")
        return OK, meldungen

    except BaseException as fehler_kopie:
        # Rollback: Zustand exakt wiederherstellen
        try:
            if not ordner_existierte:
                shutil.rmtree(ordner, ignore_errors=True)
            else:
                backup_namen = {p.name for p in backup_ordner.iterdir()}
                for item in list(ordner.iterdir()):
                    if item.name == "__pycache__":
                        continue
                    if item.name not in backup_namen:
                        if item.is_dir() and not item.is_symlink():
                            shutil.rmtree(item, ignore_errors=True)
                        else:
                            item.unlink(missing_ok=True)
                for item in backup_ordner.iterdir():
                    ziel_item = ordner / item.name
                    if item.is_symlink():
                        ziel_item.unlink(missing_ok=True)
                        ziel_item.symlink_to(os.readlink(item))
                    elif item.is_file():
                        shutil.copy2(item, ziel_item)
                    elif item.is_dir():
                        if ziel_item.exists():
                            shutil.rmtree(ziel_item, ignore_errors=True)
                        shutil.copytree(item, ziel_item, symlinks=True)
        except Exception as fehler_rollback:
            return ABWEICHUNG, [f"Fehler bei Übernahme ({fehler_kopie}) und Rollback fehlgeschlagen ({fehler_rollback})"]

        if isinstance(fehler_kopie, (KeyboardInterrupt, SystemExit)):
            raise fehler_kopie
        return ABWEICHUNG, [f"Übernahme fehlgeschlagen ({fehler_kopie}) – Rollback ausgeführt (Zustand wiederhergestellt)"]

    finally:
        backup_temp.cleanup()


def zielordner(text):
    ziel = pathlib.Path(text).expanduser().resolve()
    ordner = ziel if ziel.name == PAKET else ziel / PAKET
    quelle = QUELLE.resolve()
    if ordner == quelle or quelle in ordner.parents or (REPO / "src").resolve() in ordner.parents:
        return None
    return ordner


def _pruefen_ausgeben(ordner, quelle):
    if not ordner.is_dir():
        print(f"{ordner}: keine Kopie vorhanden")
        return ABWEICHUNG
    manifest, zeilen = pruefen(ordner, quelle["hashes"])
    stand = manifest.get("shell_version") if manifest else "ohne gültiges Manifest"
    print(f"Kopie {stand}, Quelle {quelle['version']} ({(quelle['commit'] or 'ohne Git')[:12]})")
    for name, art in zeilen:
        print(f"  {name}: {art}")
    return OK if manifest and all(art == "aktuell" for _, art in zeilen) else ABWEICHUNG


def main(argv=None):
    parser = argparse.ArgumentParser(description="glide_shell in ein Folgeprojekt übernehmen oder eine Kopie prüfen")
    parser.add_argument("ziel", help="Quellordner des Folgeprojekts (oder dessen glide_shell-Ordner)")
    gruppe = parser.add_mutually_exclusive_group()
    gruppe.add_argument("--pruefen", action="store_true", help="nur prüfen, nichts schreiben")
    gruppe.add_argument("--ersetzen", action="store_true", help="lokale Änderungen bewusst überschreiben")
    parser.add_argument("--commit", metavar="REV", help="Shell aus diesem Commit statt aus der Arbeitskopie lesen")
    parser.add_argument("--unsauber-erlauben", action="store_true",
                        help="lokal veränderte Shell-Quelle bewusst übernehmen (im Manifest vermerkt)")
    args = parser.parse_args(argv)
    ordner = zielordner(args.ziel)
    if ordner is None:
        print("Ziel liegt im Glide-Quellbaum; Folgeprojekte übernehmen die Shell in ihren eigenen Ordner")
        return VERWEIGERT
    try:
        quelle = quelle_lesen(args.commit, args.unsauber_erlauben or args.pruefen)
    except QuellFehler as fehler:
        print(f"Quelle unbrauchbar: {fehler}")
        return QUELLFEHLER
    if args.pruefen:
        return _pruefen_ausgeben(ordner, quelle)
    code, meldungen = uebernehmen(ordner, ersetzen=args.ersetzen, quelle=quelle)
    for zeile in meldungen:
        print(zeile)
    return code


if __name__ == "__main__":
    sys.exit(main())
