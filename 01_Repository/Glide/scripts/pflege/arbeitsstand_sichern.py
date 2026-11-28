# SPDX-License-Identifier: MPL-2.0
"""Sichert einen nicht committeten Arbeitsstand vollständig und stellt ihn prüfbar wieder her.

Aufruf (aus einem beliebigen Ordner der Arbeitskopie):

    python3 -B scripts/pflege/arbeitsstand_sichern.py sichern <Zielordner> [--name <Kennung>]
    python3 -B scripts/pflege/arbeitsstand_sichern.py pruefen <Sicherungsordner>
    python3 -B scripts/pflege/arbeitsstand_sichern.py wiederherstellen <Sicherungsordner> <Leerer Ordner>

Eine Sicherung enthält:

- `aenderungen.patch`: `git diff --binary HEAD` – Änderungen, Löschungen,
  Umbenennungen und Binärdateien der versionierten Dateien gegenüber dem
  Ausgangscommit (gestagte und ungestagte zusammen).
- `unversioniert/`: Kopie jeder neuen, nicht durch `.gitignore` ausgeschlossenen
  Datei. Ausgeschlossene Dateien (Rohprotokolle, Nutzerdaten, Builds) werden
  bewusst nicht übernommen; Dateien, deren Name auf ein Geheimnis deutet
  (`.env`, Schlüssel, Zertifikate, Tokens), verweigert das Werkzeug.
- `MANIFEST.json`: Ausgangscommit, Branch, Zeitpunkt, Git-Status je Pfad und
  SHA-256 jeder geänderten oder neuen Datei im Arbeitsstand sowie der
  Sicherungsdateien selbst.

`pruefen` vergleicht die Sicherungsdateien mit dem Manifest. `wiederherstellen`
klont das Repository der aktuellen Arbeitskopie ohne Hardlinks in einen leeren
Ordner, checkt den Ausgangscommit losgelöst aus, wendet den Patch an, kopiert
die unversionierten Dateien und vergleicht danach jede Datei mit dem Manifest.
Der Zielordner muss außerhalb der Arbeitskopie liegen. `sichern` prüft vorab den
freien Speicher (Bedarf plus Reserve `--reserve-mb`, Standard 1024), schreibt in
einen Zwischenordner `.<Kennung>.unvollstaendig`, vergleicht ihn mit dem Manifest
und benennt ihn erst danach um; bei jedem Fehler bleibt keine halbe Sicherung
stehen, und es wird kein Erfolg gemeldet. Das Werkzeug ändert die
Arbeitskopie nie und legt weder Commits noch Branches noch Stashes an.

Exitcodes: 0 in Ordnung, 1 Abweichung, 2 Bedienfehler, 3 verweigerte Datei, 4 zu wenig Speicher.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

MANIFEST = "MANIFEST.json"
PATCH = "aenderungen.patch"
UNVERSIONIERT = "unversioniert"
FORMAT = 1
GEHEIMNIS = re.compile(
    r"(^|/)(\.env(\..*)?|.*\.(pem|key|p12|pfx|keychain|mobileprovision)|id_rsa.*|.*token.*\.txt|credentials.*)$",
    re.IGNORECASE)


class SicherungsFehler(Exception):
    def __init__(self, text, code=1):
        super().__init__(text)
        self.code = code


def _git(root, *argumente, text=True):
    ergebnis = subprocess.run(["git", "-C", str(root), *argumente], capture_output=True,
                              text=text, check=False, **({"encoding": "utf-8"} if text else {}))
    if ergebnis.returncode != 0:
        fehler = ergebnis.stderr if text else ergebnis.stderr.decode("utf-8", "replace")
        raise SicherungsFehler(f"git {' '.join(argumente)}: {fehler.strip()}", 2)
    return ergebnis.stdout


def repo_root(start="."):
    return pathlib.Path(_git(pathlib.Path(start).resolve(), "rev-parse", "--show-toplevel").strip())


def sha(pfad):
    h = hashlib.sha256()
    with open(pfad, "rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def status_eintraege(root):
    """Git-Status je Pfad (porcelain v1, -z, ohne ignorierte Dateien)."""
    roh = _git(root, "-c", "core.quotepath=false", "status", "--porcelain=v1", "-z", "--untracked-files=all")
    teile = roh.split("\0")
    eintraege, i = [], 0
    while i < len(teile):
        satz = teile[i]
        i += 1
        if not satz:
            continue
        code, pfad = satz[:2], satz[3:]
        alt = None
        if code[0] in "RC":
            alt = teile[i]
            i += 1
        eintraege.append({"status": code, "pfad": pfad, **({"vorher": alt} if alt else {})})
    return eintraege


def bedarf(root, eintraege):
    """Geschätzter Platzbedarf einer Sicherung in Byte (Patch-Obergrenze plus neue Dateien)."""
    summe = 0
    for e in eintraege:
        pfad = pathlib.Path(root) / e["pfad"]
        if pfad.is_file():
            summe += pfad.stat().st_size * (1 if e["status"] == "??" else 2)
    return summe + (1 << 20)


def sichern(root, ziel, name=None, reserve_mb=1024):
    """Schreibt die Sicherung in einen Zwischenordner, prüft sie und benennt sie erst dann um."""
    root = pathlib.Path(root).resolve()
    ziel = pathlib.Path(ziel).resolve()
    if ziel == root or root in ziel.parents:
        raise SicherungsFehler("Zielordner liegt in der Arbeitskopie", 2)
    kennung = name or _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    ordner = ziel / kennung
    if ordner.exists():
        raise SicherungsFehler(f"{ordner} existiert bereits", 2)
    eintraege = status_eintraege(root)
    neu = [e["pfad"] for e in eintraege if e["status"] == "??"]
    verweigert = [p for p in neu if GEHEIMNIS.search(p)]
    if verweigert:
        raise SicherungsFehler("mögliche Geheimnisse nicht gesichert: " + ", ".join(verweigert), 3)
    ziel.mkdir(parents=True, exist_ok=True)
    noetig = bedarf(root, eintraege) + reserve_mb * (1 << 20)
    frei = shutil.disk_usage(ziel).free
    if frei < noetig:
        raise SicherungsFehler(f"zu wenig Speicher in {ziel}: frei {frei >> 20} MB, nötig {noetig >> 20} MB "
                               f"(einschließlich {reserve_mb} MB Reserve)", 4)
    endgueltig, ordner = ordner, ziel / f".{kennung}.unvollstaendig"
    if ordner.exists():
        shutil.rmtree(ordner)
    try:
        manifest = _schreiben(root, ordner, eintraege, neu)
        _, fehler = pruefen(ordner)
        if fehler:
            raise SicherungsFehler("Prüfung nach dem Schreiben: " + "; ".join(fehler))
        ordner.rename(endgueltig)
    except BaseException:
        shutil.rmtree(ordner, ignore_errors=True)
        raise
    return endgueltig, manifest


def _schreiben(root, ordner, eintraege, neu):
    ordner.mkdir(parents=True)
    patch = _git(root, "diff", "--binary", "HEAD", text=False)
    (ordner / PATCH).write_bytes(patch)
    for pfad in neu:
        quelle = root / pfad
        kopie = ordner / UNVERSIONIERT / pfad
        kopie.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(quelle, kopie)
    dateien = {}
    for e in eintraege:
        pfad = root / e["pfad"]
        dateien[e["pfad"]] = {"status": e["status"], **({"vorher": e["vorher"]} if "vorher" in e else {}),
                              "sha256": sha(pfad) if pfad.is_file() else None}
    sicherung = {PATCH: sha(ordner / PATCH)}
    for pfad in neu:
        sicherung[f"{UNVERSIONIERT}/{pfad}"] = sha(ordner / UNVERSIONIERT / pfad)
    manifest = {
        "format": FORMAT,
        "erstellt": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "ausgangscommit": _git(root, "rev-parse", "HEAD").strip(),
        "branch": _git(root, "rev-parse", "--abbrev-ref", "HEAD").strip(),
        "dateien": dateien,
        "sicherung": sicherung,
        # Abdruck des ganzen Arbeitsbaums (Teil 05B): Die Arbeitskopie mischt CRLF
        # und LF; ein frischer Klon setzt Zeilenenden nach `core.autocrlf`. Ohne
        # Abdruck wären nur geänderte Dateien bytegenau prüfbar.
        "baum": baum_abdruck(root),
    }
    (ordner / MANIFEST).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


CRLF, LF = bytes((13, 10)), bytes((10,))


def baum_abdruck(root):
    """SHA-256 und Zeilenendeform jeder versionierten Datei im Arbeitsbaum."""
    namen = _git(root, "-c", "core.quotepath=false", "ls-files", "-z", text=False).split(b"\0")
    abdruck = {}
    for roh in namen:
        if not roh:
            continue
        name = roh.decode("utf-8")
        pfad = root / name
        if not pfad.is_file() or pfad.is_symlink():
            continue
        inhalt = pfad.read_bytes()
        abdruck[name] = {"sha256": hashlib.sha256(inhalt).hexdigest(),
                         "crlf": CRLF in inhalt}
    return abdruck


def zeilenenden_angleichen(ziel, abdruck):
    """Zeilenenden der Quelle herstellen; ändert nur, wenn danach die Prüfsumme stimmt."""
    for name, eintrag in abdruck.items():
        datei = ziel / name
        if not datei.is_file() or sha(datei) == eintrag["sha256"]:
            continue
        lf = datei.read_bytes().replace(CRLF, LF)
        umgestellt = lf.replace(LF, CRLF) if eintrag["crlf"] else lf
        if hashlib.sha256(umgestellt).hexdigest() == eintrag["sha256"]:
            datei.write_bytes(umgestellt)


def manifest_lesen(ordner):
    pfad = pathlib.Path(ordner) / MANIFEST
    if not pfad.is_file():
        raise SicherungsFehler(f"{pfad} fehlt", 2)
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    if daten.get("format") != FORMAT:
        raise SicherungsFehler(f"unbekanntes Manifestformat {daten.get('format')!r}", 2)
    return daten


def pruefen(ordner):
    ordner = pathlib.Path(ordner)
    manifest = manifest_lesen(ordner)
    fehler = []
    for name, erwartet in manifest["sicherung"].items():
        pfad = ordner / name
        if not pfad.is_file():
            fehler.append(f"fehlt: {name}")
        elif sha(pfad) != erwartet:
            fehler.append(f"verändert: {name}")
    return manifest, fehler


def wiederherstellen(ordner, ziel, quelle_repo="."):
    manifest, fehler = pruefen(ordner)
    if fehler:
        raise SicherungsFehler("Sicherung beschädigt: " + "; ".join(fehler))
    ordner = pathlib.Path(ordner).resolve()
    ziel = pathlib.Path(ziel).resolve()
    if ziel.exists() and any(ziel.iterdir()):
        raise SicherungsFehler(f"{ziel} ist nicht leer", 2)
    root = repo_root(quelle_repo)
    # Ohne Zeilenendkonvertierung klonen: Der Klon enthält dann genau die
    # Blob-Bytes; die tatsächlichen Zeilenenden der Quelle setzt der Abdruck.
    subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--no-hardlinks", "--no-checkout",
                    "--config", "core.autocrlf=false", "--config", "core.eol=lf", str(root), str(ziel)], check=True)
    _git(ziel, "checkout", "-q", "--detach", manifest["ausgangscommit"])
    if (ordner / PATCH).stat().st_size:
        _git(ziel, "apply", "--binary", "--whitespace=nowarn", str(ordner / PATCH))
    quelle_neu = ordner / UNVERSIONIERT
    if quelle_neu.is_dir():
        for datei in quelle_neu.rglob("*"):
            if datei.is_file():
                rel = datei.relative_to(quelle_neu)
                (ziel / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(datei, ziel / rel)
    abdruck = manifest.get("baum") or {}
    zeilenenden_angleichen(ziel, abdruck)
    abweichungen = []
    for name, eintrag in abdruck.items():
        datei = ziel / name
        if name in manifest["dateien"]:
            continue  # unten mit dem Änderungsmanifest geprüft
        if not datei.is_file():
            abweichungen.append(f"fehlt: {name}")
        elif sha(datei) != eintrag["sha256"]:
            abweichungen.append(f"abweichend (Bytes): {name}")
    zeilenenden_angleichen(ziel, {pfad: {"sha256": e["sha256"], "crlf": abdruck.get(pfad, {}).get("crlf", False)}
                                  for pfad, e in manifest["dateien"].items() if e["sha256"]})
    for pfad, eintrag in manifest["dateien"].items():
        datei = ziel / pfad
        if eintrag["sha256"] is None:
            if datei.exists():
                abweichungen.append(f"sollte fehlen: {pfad}")
        elif not datei.is_file():
            abweichungen.append(f"fehlt: {pfad}")
        elif sha(datei) != eintrag["sha256"]:
            abweichungen.append(f"abweichend: {pfad}")
    return manifest, abweichungen


def main(argv=None):
    parser = argparse.ArgumentParser(description="Nicht committeten Arbeitsstand sichern, prüfen, wiederherstellen")
    unter = parser.add_subparsers(dest="befehl", required=True)
    s = unter.add_parser("sichern")
    s.add_argument("ziel")
    s.add_argument("--name")
    s.add_argument("--reserve-mb", type=int, default=1024)
    p = unter.add_parser("pruefen")
    p.add_argument("sicherung")
    w = unter.add_parser("wiederherstellen")
    w.add_argument("sicherung")
    w.add_argument("ziel")
    args = parser.parse_args(argv)
    try:
        if args.befehl == "sichern":
            ordner, manifest = sichern(repo_root(), args.ziel, args.name, args.reserve_mb)
            neu = sum(1 for e in manifest["dateien"].values() if e["status"] == "??")
            print(f"Gesichert: {ordner} · Ausgangscommit {manifest['ausgangscommit'][:12]} · "
                  f"{len(manifest['dateien']) - neu} versionierte Änderungen, {neu} neue Dateien")
            return 0
        if args.befehl == "pruefen":
            manifest, fehler = pruefen(args.sicherung)
            for zeile in fehler:
                print(zeile)
            print("Sicherung vollständig" if not fehler else f"{len(fehler)} Abweichung(en)")
            return 1 if fehler else 0
        manifest, abweichungen = wiederherstellen(args.sicherung, args.ziel)
        for zeile in abweichungen:
            print(zeile)
        print(f"Wiederhergestellt in {args.ziel}: {len(manifest['dateien'])} Dateien, "
              + ("alle SHA-256 gleich" if not abweichungen else f"{len(abweichungen)} Abweichung(en)"))
        return 1 if abweichungen else 0
    except SicherungsFehler as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return fehler.code


if __name__ == "__main__":
    sys.exit(main())
