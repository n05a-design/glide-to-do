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

Geprüft wird mit vierzehn Regeln. Grundlage ist die Unterscheidung zwischen
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
R6  Nennt eine Standangabe eine Formatstufe („Aufgabenformat 15", „Datenformat
    15", „Format 15"), muss es die aus `DATA_SCHEMA_VERSION` sein.
R7  Ein Formatbereich („Formate 4 bis 15", „Formate 4–15") muss von
    `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis `DATA_SCHEMA_VERSION` reichen.
R8  Eine Tabellenzeile, deren erste Spalte „Datenformat", „Aufgabenformat" oder
    „… Backup-Formate" heißt, nennt die aktuellen Werte.

R9  Ein aktives Dokument wiederholt keine als überholt bekannte Aussage
    (`UEBERHOLT`, je mit Grund und richtiger Aussage). Anlass: Die Prüfung vom
    28.09.2026 fand neun solche Stellen, die keine Regel erkannte – etwa „letzte
    40 JSON-Stände“ oder einen Link „Warum es keine Systembenachrichtigung
    gibt“, obwohl es sie seit dem 27.09.2026 gibt.
R10 Jede Moduldatei neben `app.pyw` steht in allen Dokumenten und Skripten, die
    die Module aufzählen (`MODULLISTEN`). Anlass: `30_Release_Exports/README.md`
    nannte nur zwei von sechs Modulen, und das macOS-Bundle hätte ein neues
    Modul ohne Fehlermeldung weggelassen. Die README in `07_Python-Versionen`
    folgt seit 09.10.2026 den Modulen dieses Ordners, nicht dem Quellbaum.
R11 Jeder relative Link eines aktiven Dokuments führt zu einer vorhandenen
    Datei. Anlass: das Aufräumen leerer Ordner am 29.09.2026.
R12 Ein fortgeschriebener Titel behauptet keinen älteren Glide-Stand.
R13 Der erste Vollprüfungsaufruf eines fortgeschriebenen Dokuments verwendet
    in seinem Protokollpfad die aktuelle Version oder einen Platzhalter.
    Spätere historische Beispielaufrufe bleiben erlaubt.
R14 Nennt eine fortgeschriebene Standzeile die Zahl der Integrationssuiten,
    stimmt sie mit SUITEN im Prüfstand überein. Historische Laufzahlen bleiben
    als Belege erlaubt.

R6 bis R8 kamen mit 3.21.4 dazu, R9 bis R11 am 29.09.2026. Anlass: Fünf fortgeschriebene Dokumente
trugen eine überholte Formatstufe – `SECURITY.md` „Formate 4 bis 12",
`06_DATA_BACKUP_MIGRATION.md` „Formate 4–14", `decisions/PRODUCT_IDENTITY.md`
gleich vier Werte auf Format 13 und App-Version 3.14.0, `src/glide/README.md`
„Datenformat 13". Die Formatstufe steht im Code; sie lässt sich also prüfen,
statt sie in jedem Dokument von Hand zu pflegen.

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
import ast
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[2]
REPO_TEIL = "01_Repository/Glide"
APP = REPO / "src/glide/app.pyw"

# Formatangaben in einer Standzeile oder Tabellenzeile.
FORMATSTUFE = re.compile(
    r"\b(?:Aufgaben|Daten|Dokument)?[Ff]ormat\s+(\d+)\b")
FORMATBEREICH = re.compile(
    r"[Ff]ormate?\s+(\d+)\s*(?:bis|–|-)\s*(\d+)")
# Tabellenzeile, deren erste Spalte eine Formatangabe benennt.
FORMATZEILE = re.compile(
    r"^\|\s*(?:Unterstützte\s+)?(?:Backup-)?(?:Aufgaben|Daten)?[Ff]ormate?\s*\|")
VERSIONSZEILE = re.compile(r"^\|\s*App-Version\s*\|")

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
# Vollständige datierte Ablageabbilder sind keine zweite aktive Arbeitsgrundlage.
# Ein Zwischenstand kann unvollständige Nachweise enthalten; nichts nachschreiben.
ZWISCHENSTAND = re.compile(r"Glide_\d+\.\d+\.\d+_Zwischenstand_\d{4}-\d{2}-\d{2}")

# Fortgeschrieben, obwohl der Dateiname ein Datum oder eine Version trägt.
# Seit dem Aufräumen vom 03.10.2026 tragen die gepflegten Dokumente
# (Übergabe, Entwicklungsplan, Markt und Vorbilder, manuelle Prüfliste) kein
# Datum mehr im Namen; die Liste bleibt für künftige Ausnahmen.
GEPFLEGT: tuple[str, ...] = ()

# Zusätzliche festgeschriebene Einzeldateien außerhalb klar datierter Pfade.
# Der frühere Reiterentwurf ist seit der Existenzprüfung vom 24.09.2026 im
# Archiv und benötigt deshalb keine aktive Sonderbehandlung mehr.
FESTGESCHRIEBEN: tuple[str, ...] = ()

# Dateien ohne Standaussage. Arbeitsregeln und Änderungsverlauf tragen ihren
# Stand in der Sache selbst: AGENTS.md gilt versionsunabhängig, CHANGELOG.md
# beginnt mit dem Eintrag der aktuellen Version.
OHNE_STAND = ("AGENTS.md", "CHANGELOG.md", "LIESMICH.md",
              "LICENSE.md", "SECURITY.md")

# R9: Aussagen, die nachweislich überholt sind (Prüfung vom 28.09.2026 und
# später). Jede Zeile: Muster, Grund. Geprüft werden alle aktiven Dokumente
# außer reiner Geschichte (CHANGELOG) und festgeschriebenen Belegen – ein
# datiertes Protokoll darf wiedergeben, was damals galt.
UEBERHOLT: tuple[tuple[str, str], ...] = (
    (r"Warum es keine Systembenachrichtigung gibt",
     "Systemmitteilungen gibt es seit 27.09.2026 als Option"),
    (r"zwei aktuelle Beispielbackups",
     "es sind drei, einschließlich „Rundgang“"),
    (r"letzte[n]? 40 JSON-Stände",
     "seit 29.09.2026: Sicherung nur bei Änderung, dazu je Tag der letzte Stand für 14 Tage"),
    (r"Ziehen aus (?:dem )?Finder (?:oder|bzw\.) (?:dem )?Explorer bräuchte",
     "seit 27.09.2026 über tkinterdnd2"),
    (r"leere(?:n)? (?:Windows-)?Python-(?:3\.13-)?Umgebung",
     ".venv stammt von GitHub Copilot und bleibt für spätere Arbeit"),
    (r"(?:echte )?Logo liegt nur als Affinity-Datei",
     "Logo liegt seit 29.09.2026 als SVG und PNG in 20_Grafik_Master"),
    (r"Pixel-„G“ als Platzhalter",
     "das Programmsymbol kommt seit 29.09.2026 aus dem Logo-Master"),
    (r"Prüflaufzeit[^|\n]*Python 3\.13",
     "maßgeblich ist Python 3.14 mit Tk 9"),
)

# R10: Wer die Module neben `app.pyw` aufzählt, nennt alle. Die Moduldateien
# ergeben sich aus `src/glide/*.py` (ohne die isolierte Bedienprobe).
MODULLISTEN = (
    "docs/02_ARCHITECTURE.md",
    "src/glide/README.md",
    "packaging/README.md",
    "packaging/macos/baue_app.py",
)
MODULLISTEN_ABLAGE = ("07_Python-Versionen/README.md",)

# Reine Geschichte: Jeder Eintrag beschreibt den Stand seiner Version. Ein
# Formatbereich wie „Formate 2 bis 9" war damals richtig und darf nicht
# nachgezogen werden – dieselbe Überlegung wie beim Zitatschutz.
NUR_GESCHICHTE = ("CHANGELOG.md",)


def aussage(text: str) -> str:
    """Die Zeile ohne Zitate und Codespannen – nur was sie selbst behauptet."""
    return ZITATE.sub(" ", text)


def saetze(zeile: str) -> list[str]:
    """Die Sätze einer Zeile, Zitate und Codespannen bereits entfernt."""
    return [teil for teil in SATZGRENZE.split(aussage(zeile)) if teil.strip()]


def versionen(text: str) -> list[str]:
    """Glide-Versionen einer Zeile; Fremdangaben und Daten fallen vorher weg."""
    return VERSION_MUSTER.findall(FREMDE_ANGABEN.sub(" ", aussage(text)))


def app_konstanten() -> dict[str, int]:
    """`DATA_SCHEMA_VERSION` und `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` aus dem
    Anwendungscode. Über den Syntaxbaum gelesen, damit die Prüfung die App
    nicht importieren muss – ein Import würde Tk starten und den echten
    Nutzerdatenordner anfassen."""
    werte: dict[str, int] = {}
    if not APP.is_file():
        return werte
    baum = ast.parse(APP.read_text(encoding="utf-8-sig"), filename=str(APP))
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant) \
                and isinstance(knoten.value.value, int):
            for ziel in knoten.targets:
                if isinstance(ziel, ast.Name) and ziel.id in (
                        "DATA_SCHEMA_VERSION", "MIN_PORTABLE_BACKUP_SCHEMA_VERSION"):
                    werte.setdefault(ziel.id, knoten.value.value)
    return werte


def als_tupel(wert: str) -> tuple[int, ...]:
    teile = tuple(int(t) for t in wert.split("."))
    return teile + (0,) * (3 - len(teile))


def suite_anzahl() -> int:
    """SUITEN statisch lesen; kein App-/Tk-Import und keine Nutzerdaten."""
    pfad = REPO / "tests/tools/pruefen.py"
    baum = ast.parse(pfad.read_text(encoding="utf-8-sig"), filename=str(pfad))
    for knoten in baum.body:
        if isinstance(knoten, ast.Assign) and any(
                isinstance(ziel, ast.Name) and ziel.id == "SUITEN"
                for ziel in knoten.targets):
            return len(ast.literal_eval(knoten.value))
    raise ValueError("SUITEN fehlt im Prüfstand")


def ablagewurzel(repo: Path) -> Path | None:
    """Der Ordner „Glide ToDo", wenn das Repository darin liegt."""
    for kandidat in repo.parents:
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    return None


def dokumente(wurzel: Path):
    for pfad in sorted(wurzel.rglob("*.md")):
        teile = pfad.relative_to(wurzel).parts
        # Verschachtelte Git-Checkouts haben einen eigenen Stand und Auftrag.
        # .git ist im Worktree eine Datei, im eigenständigen Checkout ein Ordner.
        if any((parent / ".git").exists() for parent in pfad.parents
               if parent != wurzel and parent.is_relative_to(wurzel)):
            continue
        if any(t.lower().startswith("archiv") for t in teile):
            continue
        if any(ZWISCHENSTAND.fullmatch(t) for t in teile[:-1]):
            continue
        # Mit „_Z“ markierte der Inhaber bis 03.10.2026, was er selbst löschen
        # wollte (Ordner `Name_Z`, Dateien `Name_Z.md`); seitdem wird gelöscht.
        if any(t.endswith("_Z") for t in teile[:-1]) or pfad.stem.endswith("_Z"):
            continue
        if ("__pycache__" in teile or "node_modules" in teile
                or ".venv" in teile or "venv" in teile):
            continue
        # Werkzeugordner eines Versionssprungs sind Quellmaterial und wandern
        # nach dem Lauf ins Ablagearchiv; ihre Texte beschreiben den Sprung,
        # nicht den Stand der Ablage.
        if any(t.startswith("Werkzeuge_") for t in teile):
            continue
        # Unveränderte Nutzeraufträge sind Eingangsbelege, keine gepflegten
        # Produktdokumente. Ihre ursprünglichen Standangaben bleiben erhalten.
        if any(re.fullmatch(r"\d+\.\d+ Änderungen-Prompt", t) for t in teile):
            continue
        yield pfad


class Befund:
    def __init__(self, version: str, formate: dict[str, int] | None = None,
                 suiten: int | None = None):
        self.version = version
        formate = formate or {}
        self.format_aktuell = formate.get("DATA_SCHEMA_VERSION")
        self.format_niedrigst = formate.get("MIN_PORTABLE_BACKUP_SCHEMA_VERSION")
        self.suiten = suiten
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

    if not fest:
        formate_pruefen(befund, kurz, zeilen, standzeilen)
    # R9 auch für Verträge der laufenden Version („…_3.30.0.md“): Sie werden
    # fortgeschrieben, solange die Version gilt. Datierte Belege bleiben frei.
    lebend = not fest or (name_version and als_tupel(name_version) == als_tupel(befund.version)
                          and not hat_datum)
    if lebend and name not in NUR_GESCHICHTE:
        ueberholt_pruefen(befund, kurz, text)

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

    einstieg_pruefen(befund, kurz, titel, text)

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
        if befund.suiten is not None:
            for zahl in re.findall(r"\b(\d+)\s+(?:Integrations)?[Ss]uiten\b", zeile):
                if int(zahl) != befund.suiten:
                    befund.melden(kurz, nr, f"Standzeile nennt {zahl} Suiten, "
                                            f"SUITEN enthält {befund.suiten} (R14)")


def einstieg_pruefen(befund: Befund, kurz: str, titel: str, text: str) -> None:
    """R12/R13: gepflegte Einstiege auch innerhalb von Codebeispielen prüfen.

    Die erste Vollprüfungsanweisung ist der Einstieg; spätere Befehle dürfen
    historische Vergleichsläufe beschreiben. Versionsplatzhalter bleiben frei.
    Historische Dokumente rufen diese Funktion ausdrücklich nicht auf.
    """
    titelwerte = versionen(titel)
    if not any(als_tupel(w) == als_tupel(befund.version) for w in titelwerte):
        for wert in titelwerte:
            if als_tupel(wert) < als_tupel(befund.version):
                nr = text.splitlines().index(titel) + 1
                befund.melden(kurz, nr, f"fortgeschriebener Titel nennt {wert}, "
                                        f"aktuell ist {befund.version} (R12)")
    # Raw-Text: Zitat-/Codespannenschutz wäre hier falsch, weil ausführbare
    # Befehle gerade in Code stehen. Der Zeilenumbruch einer Anweisung zählt.
    befehl = re.search(r"--modus\s+voll\s+--protokoll\s+([^\s`]+)", text)
    if befehl:
        version = re.search(r"(?:^|[/\\])qa-(\d+\.\d+\.\d+)(?=[/\\]|$)",
                            befehl.group(1))
        if version and als_tupel(version.group(1)) != als_tupel(befund.version):
            nr = text.count("\n", 0, befehl.start()) + 1
            befund.melden(kurz, nr, f"erster Vollprüfungsaufruf verwendet "
                                    f"qa-{version.group(1)}, aktuell ist "
                                    f"{befund.version} (R13)")


def formate_pruefen(befund: Befund, kurz: str, zeilen: list[str],
                    standzeilen: list[tuple[int, str, list[str]]]) -> None:
    """R6 bis R8: Formatangaben gegen den Anwendungscode.

    Die Formatstufe ist keine Meinung – sie steht als `DATA_SCHEMA_VERSION` im
    Code. Fünf fortgeschriebene Dokumente trugen bis 3.21.3 eine überholte
    Stufe, eines davon der Sicherheitshinweis („Formate 4 bis 12"), der die
    Konstante ausdrücklich zitiert.
    """
    aktuell = befund.format_aktuell
    niedrigst = befund.format_niedrigst
    if not aktuell or Path(kurz).name in NUR_GESCHICHTE:
        return

    nummern = {nr for nr, _satz, _werte in standzeilen}
    for nr, satz, _werte in standzeilen:
        # R6: Formatstufe in einer Standangabe.
        for wert in FORMATSTUFE.findall(aussage(satz)):
            if int(wert) != aktuell:
                befund.melden(kurz, nr, f"Standangabe nennt Format {wert}, aktuell ist "
                                        f"{aktuell} (R6)")

    for nr, zeile in enumerate(zeilen, 1):
        rein = aussage(zeile)
        # R7: Formatbereich – überall, nicht nur in Standzeilen.
        for tief, hoch in FORMATBEREICH.findall(rein):
            if niedrigst and (int(tief) != niedrigst or int(hoch) != aktuell):
                befund.melden(kurz, nr, f"Formatbereich {tief} bis {hoch}; lesbar sind "
                                        f"{niedrigst} bis {aktuell} (R7)")
        # R8: Tabellenzeile, deren erste Spalte eine Formatangabe benennt.
        if FORMATZEILE.match(zeile) and nr not in nummern:
            werte = [int(w) for w in re.findall(r"\b(\d+)\b", zeile)]
            if werte and not FORMATBEREICH.search(rein) and aktuell not in werte:
                befund.melden(kurz, nr, f"Tabellenzeile nennt Format "
                                        f"{', '.join(str(w) for w in werte)}, aktuell "
                                        f"ist {aktuell} (R8)")
        if VERSIONSZEILE.match(zeile):
            werte = versionen(zeile)
            if werte and not any(als_tupel(w) == als_tupel(befund.version) for w in werte):
                befund.melden(kurz, nr, f"Tabellenzeile App-Version nennt "
                                        f"{', '.join(werte)}, aktuell ist "
                                        f"{befund.version} (R8)")


def ueberholt_pruefen(befund: Befund, kurz: str, text: str) -> None:
    """R9: bekannte überholte Aussagen – außerhalb von Zitaten und Codespannen.

    Eine Aussage darf über einen Zeilenumbruch laufen: Jedes Leerzeichen im
    Muster steht für beliebigen Leerraum.
    """
    rein = "\n".join(aussage(zeile) for zeile in text.splitlines())
    for muster, grund in UEBERHOLT:
        for treffer in re.finditer(muster.replace(" ", r"\s+"), rein):
            nr = rein.count("\n", 0, treffer.start()) + 1
            fund = " ".join(treffer.group(0).split())
            befund.melden(kurz, nr, f"überholte Aussage „{fund}“ – {grund} (R9)")


LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def links_pruefen(befund: Befund, wurzel: Path, pfad: Path, text: str) -> None:
    """R11: relative Links führen zu vorhandenen Dateien (Codeblöcke ausgenommen)."""
    from urllib.parse import unquote
    ohne_code = re.sub(r"```.*?```", "", text, flags=re.S)
    kurz = pfad.relative_to(wurzel).as_posix()
    for nr, zeile in enumerate(ohne_code.splitlines(), 1):
        for ziel in LINK.findall(zeile):
            if re.match(r"^[a-z][a-z0-9+.-]*:", ziel) or ziel.startswith("#"):
                continue
            ziel = unquote(ziel.split("#")[0]).strip("<>")
            if ziel and not (pfad.parent / ziel).exists():
                befund.melden(kurz, nr, f"Link auf {ziel} führt ins Leere (R11)")


def modulnamen(ordner: Path) -> list[str]:
    """Moduldateien eines Ordners neben der Hauptdatei (ohne die isolierte Bedienprobe)."""
    return sorted(pfad.name for pfad in ordner.glob("*.py") if pfad.name != "drawing_prototype.py")


def fehlende_module(text: str, module: list[str]) -> list[str]:
    """Module, die eine Aufzählung nicht nennt; der Schnellstart heißt in 07 `Schnellstart.pyw`."""
    fehlend = []
    for modul in module:
        namen = (modul, "Schnellstart.pyw") if modul == "glide_start.py" else (modul,)
        if not any(name in text for name in namen):
            fehlend.append(modul)
    return fehlend


def module_pruefen(befund: Befund, wurzeln: list[Path]) -> None:
    """R10: Jede Moduldatei steht in jeder Modulliste.

    Die Listen im Repository folgen `src/glide`. Die README in
    `07_Python-Versionen` beschreibt dagegen den gelieferten Ordner und folgt
    dessen Modulen: Zwischen Prüfkandidat und Auslieferung darf der Quellbaum
    ein Modul mehr haben (die CI meldet das unter „Lieferstand“).
    """
    module = modulnamen(REPO / "src/glide")
    ablage = ablagewurzel(REPO)
    listen = [(REPO / name, f"{REPO_TEIL}/{name}", module) for name in MODULLISTEN]
    if ablage is not None:
        for name in MODULLISTEN_ABLAGE:
            listen.append((ablage / name, name, modulnamen((ablage / name).parent)))
    for pfad, kurz, erwartet in listen:
        if not pfad.is_file():
            continue
        for modul in fehlende_module(pfad.read_text(encoding="utf-8-sig"), erwartet):
            befund.melden(kurz, 1, f"Modul {modul} fehlt in der Aufzählung (R10)")


def lauf(wurzeln: list[Path], version: str) -> Befund:
    befund = Befund(version, app_konstanten(), suite_anzahl())
    gesehen: set[Path] = set()
    for wurzel in wurzeln:
        for pfad in dokumente(wurzel):
            if pfad.resolve() in gesehen:
                continue
            gesehen.add(pfad.resolve())
            kurz = pfad.relative_to(wurzel).as_posix()
            text = pfad.read_text(encoding="utf-8-sig")
            datei_pruefen(befund, kurz, text)
            teile = pfad.relative_to(wurzel).parts
            # Belege (QA-Läufe) zitieren Pfade ihres Tages.
            if not any(t.startswith("qa-") for t in teile):
                links_pruefen(befund, wurzel, pfad, text)
    module_pruefen(befund, wurzeln)
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
