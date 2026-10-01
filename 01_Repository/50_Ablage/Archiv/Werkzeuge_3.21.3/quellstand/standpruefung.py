#!/usr/bin/env python3
"""Prüft die Standangaben aller aktiven Markdown-Dokumente gegen VERSION.

Warum es dieses Werkzeug gibt: Sieben Dokumente standen zwei Versionssprünge
lang auf 3.21.0 – Repository-README, Dokumentationsindex, Bestandsanalyse,
Abschlussbericht, Feature-Abgleich, `10_Dokumentation/README.md` und das
Produktdatenblatt. Niemand hat es gesehen, weil die Fortschreibung eine
Tokenliste benutzt und eine Schreibweise, die dort fehlt, einfach stehen
bleibt. Ein Banner „Aktueller Entwicklungsstand: …", das von Hand gepflegt
werden muss, rottet zwangsläufig. Der Prüfstand hat das bis 3.21.2 nicht
bemerkt, weil er Dokumente nur auf Indexeintrag und erreichbare Links prüft,
nie auf Aktualität ihrer Aussage.

Geprüft wird mit fünf Regeln. Grundlage ist die Unterscheidung zwischen
**fortgeschriebenen** und **festgeschriebenen** Dokumenten:

* Festgeschrieben ist ein Dokument, dessen Dateiname eine Version oder ein
  Datum trägt, dessen Pfad einen Versionsordner enthält oder dessen Titel das
  Wort „historisch" führt. Es beschreibt einen abgeschlossenen Stand und wird
  bewusst nicht nachgezogen.
* Alles andere ist fortgeschrieben und muss den aktuellen Stand nennen.

Regeln:

R1  Ein fortgeschriebenes Dokument trägt mindestens eine Standangabe, die die
    Version aus `VERSION` nennt. Das erzwingt, dass Datum und Version an
    derselben Stelle stehen und beim Fortschreiben beide mitgehen.
R2  Nennt eine Standangabe eine andere Version, muss derselbe Satz auch die
    aktuelle nennen. So bleibt Herkunft erlaubt („erhoben auf Grundlage von
    3.14.0"), eine allein stehende überholte Angabe nicht.
R3  Kein Dokument – auch kein festgeschriebenes – behauptet einen aktuellen
    Stand mit einer anderen Version. Diese Regel trifft genau die gerotteten
    Banner. Wer in einem historischen Dokument auf den aktuellen Stand
    verweisen will, verweist ohne Nummer auf Index und QA-Bericht.
R4  Trägt der Dateiname eine Version, darf eine Standangabe keine andere
    Version nennen als diese oder die aktuelle.
R5  Der Titel eines versionsbenannten Dokuments nennt keine ältere Version als
    der Dateiname – es sei denn, er nennt auch die eigene. Genau so stand
    „# Glide Produktdatenblatt 3.21.0" in `Produktdatenblatt_3.21.2.md`.

Bewertet wird jeweils der **Satz**, nicht die Zeile: Eine Zeile kann eine
Standangabe und daneben einen historischen Hinweis tragen.

Aufruf:

    python3 tests/tools/standpruefung.py            # Repo und, wenn da, Ablage
    python3 tests/tools/standpruefung.py --wurzel .  # nur diesen Baum

Exitcode 0, wenn alle Regeln zutreffen, sonst 1 mit Fundstellen. Nur
Standardbibliothek, keine Schreibzugriffe.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[2]
REPO_TEIL = "01_Repository/Glide"

# Zeilen, die einen Stand behaupten. Absichtlich eng: „Prüfstand: 3.15.0 bis
# 3.18.0 …" nennt viele Versionen zu Recht und beginnt nicht mit „Stand".
STANDZEILE = re.compile(
    r"(^\s*(>\s*)?(\*\*)?(Stand|Arbeitsstand)\b"
    r"|Entwicklungsstand"
    r"|Aufgabenstand"
    r"|aktueller\s+Glide-Stand"
    r"|Stand der Dokumentationspflege)",
    re.I,
)

# Eine Zeile kann eine Standangabe und daneben einen historischen Hinweis
# tragen: „Historischer Lauf … Dokumentversion 3.2.0 … Aktueller Glide-Stand
# ist 3.21.3". Bewertet wird deshalb der Satz, nicht die Zeile. Getrennt wird
# an Satzzeichen vor einem Großbuchstaben; Versionsnummern enthalten Punkte,
# aber nie ein Leerzeichen danach.
SATZGRENZE = re.compile(r"(?<=[.!?])\s+(?=[»„*\[(A-ZÄÖÜ])")

# Behauptungen über den *aktuellen* Stand. Nur diese Formen, damit ein Satz
# wie „umgesetzt in 3.10.0" nicht als Aktualitätsaussage gilt.
AKTUELL = re.compile(
    r"(Aktueller\s+(interner\s+)?Entwicklungsstand"
    r"|Aktueller\s+Aufgabenstand"
    r"|aktueller\s+Glide-Stand"
    r"|Der\s+aktuelle\s+[^.]{0,60}?\bist\s+Glide"
    r"|Der\s+liegt\s+bei\s+Glide"
    r"|Der\s+aktuelle\s+Bestand\s+ist"
    r"|Der\s+aktuelle\s+Stand\s+ist)",
    re.I,
)

VERSION_MUSTER = re.compile(r"(?<![\w.])(\d+\.\d+(?:\.\d+)?)(?![\w.])")

# Zitate und Codespannen sind Belegstellen, keine Aussagen. Der
# Änderungsverlauf zitiert die gerotteten Banner wörtlich („Aktueller
# Entwicklungsstand: …" auf 3.14.0) – ohne diesen Vorfilter meldete die Prüfung
# genau den Satz, der den Fehler dokumentiert. Dieselbe Falle hat in 3.21.2 ein
# Tokendurchgang gestellt, der ein historisches Zitat auf die neue Version hob.
ZITATE = re.compile(r"„[^“”\"]{0,400}[“”\"]|`[^`]{0,400}`|\"[^\"]{0,400}\"")

# Versionsähnliche Angaben, die keine Glide-Version sind. Ohne diese Vorfilter
# stolpert die Prüfung über „Python 3.14.5" im QA-Bericht.
FREMDE_ANGABEN = re.compile(
    r"(Python|Tk|Tcl|macOS|Windows|Electron|Node)\s*/?\s*\d+(\.\d+)*"
    r"|(Aufgaben|Daten|Vorlagen|Einstellungs|Dokument)?[Ff]ormat\s+\d+"
    r"|Einstellungen\s+\d+"
    r"|Vorlagen\s+\d+"
    r"|Regel\s+\d+"
    r"|\d{1,2}\.\d{1,2}\.\d{4}",  # Datumsangaben
    re.I,
)

# Ordnernamen, die einen abgeschlossenen Stand tragen: tests/qa-3.6.0,
# Bestandsanalyse_3.2.0, Screenshots/3.5.0, Renderlaeufe/3.2.0_2026-09-04.
VERSIONSORDNER = re.compile(r"(^|[-_/])\d+\.\d+\.\d+([-_]|$)")

# Fortgeschrieben, obwohl der Dateiname ein Datum trägt: Beide Dokumente sind
# ausdrücklich die je eine aktive Fassung und werden jede Version gepflegt.
# Der Name stammt aus dem Tag ihrer Anlage und bleibt, damit Verweise halten.
GEPFLEGT = (
    "00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md",
    "00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md",
)

# Festgeschrieben, obwohl weder Name noch Titel das zeigen. Jeder Eintrag ist
# eine Entscheidung: Der Reiterentwurf beschreibt den Bedienvertrag von 3.10.0
# und wurde durch 33_REITER_UND_PINNWAND_3.10.0.md abgelöst.
FESTGESCHRIEBEN = (
    "01_Repository/Glide/docs/32_REITERANSICHT.md",
)

# Dateien ohne Standaussage. Arbeitsregeln und Änderungsverlauf tragen ihren
# Stand in der Sache selbst: AGENTS.md gilt versionsunabhängig, CHANGELOG.md
# beginnt mit dem Eintrag der aktuellen Version.
OHNE_STAND = ("AGENTS.md", "CHANGELOG.md", "LIESMICH.md",
              "LICENSE.md", "SECURITY.md")


def aussage(text: str) -> str:
    """Die Zeile ohne Zitate und Codespannen – nur was sie selbst behauptet."""
    return ZITATE.sub(" ", text)


def saetze(zeile: str) -> list[str]:
    """Die Sätze einer Zeile, Zitate und Codespannen bereits entfernt."""
    return [teil for teil in SATZGRENZE.split(aussage(zeile)) if teil.strip()]


def versionen(text: str) -> list[str]:
    """Glide-Versionen einer Zeile; Fremdangaben und Daten fallen vorher weg."""
    return VERSION_MUSTER.findall(FREMDE_ANGABEN.sub(" ", aussage(text)))


def als_tupel(wert: str) -> tuple[int, ...]:
    teile = tuple(int(t) for t in wert.split("."))
    return teile + (0,) * (3 - len(teile))


def ablagewurzel(repo: Path) -> Path | None:
    """Der Ordner „Glide ToDo", wenn das Repository darin liegt."""
    for kandidat in repo.parents:
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    return None


def dokumente(wurzel: Path):
    for pfad in sorted(wurzel.rglob("*.md")):
        teile = pfad.relative_to(wurzel).parts
        if any(t.lower().startswith("archiv") for t in teile):
            continue
        if "__pycache__" in teile or "node_modules" in teile:
            continue
        # Werkzeugordner eines Versionssprungs sind Quellmaterial und wandern
        # nach dem Lauf ins Ablagearchiv; ihre Texte beschreiben den Sprung,
        # nicht den Stand der Ablage.
        if any(t.startswith("Werkzeuge_") for t in teile):
            continue
        yield pfad


class Befund:
    def __init__(self, version: str):
        self.version = version
        self.fehler: list[str] = []
        self.fortgeschrieben = 0
        self.festgeschrieben = 0
        self.ohne_stand = 0
        self._gemeldet: set[tuple[str, int]] = set()

    def melden(self, kurz: str, zeile: int, text: str) -> None:
        """Je Zeile nur der erste Befund: Eine überholte Standzeile verstößt
        oft gegen mehrere Regeln gleichzeitig, und drei Meldungen zur selben
        Stelle verdecken die übrigen Fundstellen."""
        if (kurz, zeile) in self._gemeldet:
            return
        self._gemeldet.add((kurz, zeile))
        self.fehler.append(f"{kurz}:{zeile}: {text}")


def datei_pruefen(befund: Befund, kurz: str, text: str) -> None:
    zeilen = text.splitlines()
    name = Path(kurz).name
    titel = next((z for z in zeilen if z.startswith("# ")), "")

    # Version im Dateinamen; der Rumpf ohne Suffix, damit „3.21.2.md" zählt.
    treffer = re.search(r"(\d+\.\d+\.\d+)", Path(kurz).stem)
    name_version = treffer.group(1) if treffer else None
    hat_datum = bool(re.search(r"\d{4}-\d{2}-\d{2}", Path(kurz).stem))
    ordner_fest = any(VERSIONSORDNER.search(t) for t in Path(kurz).parts[:-1])
    titel_historisch = "historisch" in titel.lower()

    fest = bool(name_version or hat_datum or ordner_fest or titel_historisch
                or kurz in FESTGESCHRIEBEN)
    if kurz in GEPFLEGT:
        fest = False
    if fest:
        befund.festgeschrieben += 1
    elif name in OHNE_STAND:
        befund.ohne_stand += 1
    else:
        befund.fortgeschrieben += 1

    standzeilen: list[tuple[int, str, list[str]]] = []
    for nr, zeile in enumerate(zeilen, 1):
        for satz in saetze(zeile):
            if STANDZEILE.search(satz):
                standzeilen.append((nr, satz, versionen(satz)))

            # R3 gilt für jedes Dokument: Eine Aussage über den aktuellen Stand
            # darf keine andere Version nennen.
            if AKTUELL.search(satz):
                for wert in versionen(satz):
                    if als_tupel(wert) != als_tupel(befund.version):
                        befund.melden(kurz, nr, f"nennt {wert} als aktuellen Stand, "
                                                f"aktuell ist {befund.version} (R3)")

    if fest:
        # R4: Der Dateiname gibt den Stand vor.
        if name_version:
            erlaubt = {als_tupel(name_version), als_tupel(befund.version)}
            for nr, _satz, werte in standzeilen:
                # Wie bei R2 bleibt Herkunft erlaubt, solange die eigene oder
                # die aktuelle Version im selben Satz steht.
                if any(als_tupel(w) in erlaubt for w in werte):
                    continue
                for wert in werte:
                    if als_tupel(wert) not in erlaubt:
                        befund.melden(kurz, nr, f"Standangabe nennt {wert}; der Dateiname "
                                                f"sagt {name_version} (R4)")
            # R5: Der Titel nennt keine ältere Version als der Dateiname –
            # es sei denn, er nennt auch die eigene. „2.7.1 – Feinschliff nach
            # der Sichtprüfung von 2.7.0" ist in Ordnung; „Produktdatenblatt
            # 3.21.0" in einer Datei _3.21.2 nicht.
            titelwerte = versionen(titel)
            eigen = any(als_tupel(w) == als_tupel(name_version) for w in titelwerte)
            if not eigen:
                for wert in titelwerte:
                    if als_tupel(wert) < als_tupel(name_version):
                        befund.melden(kurz, 1, f"Titel nennt {wert}, der Dateiname "
                                               f"{name_version} (R5)")
        return

    if name in OHNE_STAND:
        return

    # R1: mindestens eine Standzeile mit der aktuellen Version.
    passend = [nr for nr, _z, werte in standzeilen
               if any(als_tupel(w) == als_tupel(befund.version) for w in werte)]
    if not passend:
        if not standzeilen:
            befund.melden(kurz, 1, f"keine Standangabe; erwartet wird eine Zeile mit "
                                   f"Glide {befund.version} (R1)")
        else:
            nr, zeile, _werte = standzeilen[0]
            befund.melden(kurz, nr, f"Standangabe nennt {befund.version} nicht: "
                                    f"{zeile.strip()[:90]!r} (R1)")

    # R2: Eine überholte Angabe ist nur als Herkunft neben der aktuellen erlaubt.
    for nr, zeile, werte in standzeilen:
        fremd = [w for w in werte if als_tupel(w) != als_tupel(befund.version)]
        eigen = any(als_tupel(w) == als_tupel(befund.version) for w in werte)
        if fremd and not eigen:
            befund.melden(kurz, nr, f"Standangabe nennt nur {', '.join(fremd)}, "
                                    f"nicht {befund.version} (R2)")


def lauf(wurzeln: list[Path], version: str) -> Befund:
    befund = Befund(version)
    gesehen: set[Path] = set()
    for wurzel in wurzeln:
        for pfad in dokumente(wurzel):
            if pfad.resolve() in gesehen:
                continue
            gesehen.add(pfad.resolve())
            kurz = pfad.relative_to(wurzel).as_posix()
            datei_pruefen(befund, kurz, pfad.read_text(encoding="utf-8-sig"))
    return befund


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wurzel", type=Path, action="append",
                        help="Nur diesen Baum prüfen; mehrfach angebbar")
    args = parser.parse_args()

    version = (REPO / "VERSION").read_text(encoding="utf-8-sig").strip()
    if args.wurzel:
        wurzeln = [w.expanduser().resolve() for w in args.wurzel]
        umfang = "vorgegebene Bäume"
    else:
        ablage = ablagewurzel(REPO)
        wurzeln = [ablage] if ablage else [REPO]
        umfang = "Ablage einschließlich Repository" if ablage else "nur Repository"

    for wurzel in wurzeln:
        if not wurzel.is_dir():
            print(f"Kein Ordner: {wurzel}", file=sys.stderr)
            return 1

    befund = lauf(wurzeln, version)
    gesamt = befund.fortgeschrieben + befund.festgeschrieben + befund.ohne_stand
    print(f"Standprüfung gegen VERSION {version} · {umfang} · {gesamt} aktive Dokumente "
          f"({befund.fortgeschrieben} fortgeschrieben, {befund.festgeschrieben} "
          f"festgeschrieben, {befund.ohne_stand} ohne Standaussage)")
    if befund.fehler:
        print(f"BEFUNDE ({len(befund.fehler)})")
        for zeile in befund.fehler:
            print(f"- {zeile}")
        return 1
    print("Alle Standangaben passen zur Version; kein historisches Dokument "
          "behauptet einen aktuellen Stand.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
