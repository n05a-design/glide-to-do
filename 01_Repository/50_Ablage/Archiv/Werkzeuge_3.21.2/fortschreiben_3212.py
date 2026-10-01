#!/usr/bin/env python3
"""Schreibt die Glide-Dokumentenkette von 3.21.1 auf 3.21.2 fort.

3.21.2 ist ein Daten- und Dokumentationsstand: kein Anwendungscode ausser der
Versionsangabe. Der Beispielbestand deckt die Funktionen seit 3.14 erstmals
testbar ab, ueberholte Angaben in READMEs sind richtiggestellt, und der
QA-Bericht traegt das Ergebnis des abgenommenen 3.21.1-Laufs.

Aufruf im Ordner "Glide ToDo":

    python3 fortschreiben_3212.py <Werkzeugordner> --probe    # nur zeigen
    python3 fortschreiben_3212.py <Werkzeugordner>            # schreiben

Grundsaetze: Jede Datei wird als Ganzes berechnet und nur geschrieben, wenn alle
Pflichtstellen zutreffen; sonst bricht der Lauf ab und aendert nichts weiter.
Vorfassungen gehen vorher ins archiv/ desselben Ordners. Es wird nichts
geloescht.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ALT, NEU = "3.21.1", "3.21.2"
REPO_TEIL = "01_Repository/Glide"

# Allgemeine Versionsangaben. Die Schreibweisen mit Fettschrift und mit
# vorangestelltem Trenner fehlten bis 3.21.1 – deshalb blieben Wurzel-README,
# Repository-README und 10_Dokumentation auf 3.21.0 stehen.
TOKENS = (
    ("Glide 3.21.1 ·", "Glide 3.21.2 ·"),
    ("· Glide 3.21.1", "· Glide 3.21.2"),
    ("**3.21.1**", "**3.21.2**"),
    ("**3.21.1 vom", "**3.21.2 vom"),
    ("Entwicklungsstand 3.21.1", "Entwicklungsstand 3.21.2"),
    ("Entwicklungsstand: **3.21.1", "Entwicklungsstand: **3.21.2"),
    ("v3.21.1.pyw", "v3.21.2.pyw"),
    ("Stand 3.21.1", "Stand 3.21.2"),
    ("Releaseplanung 3.21.1", "Releaseplanung 3.21.2"),
    ("glide_releaseplanung_3.21.1.glidebackup", "glide_releaseplanung_3.21.2.glidebackup"),
    ("--protokoll tests/qa-3.21.1/abschluss", "--protokoll tests/qa-3.21.2/abschluss"),
    ("Maßgeblich sind tests/qa-3.21.1/abschluss", "Maßgeblich sind tests/qa-3.21.2/abschluss"),
    ("– Glide 3.21.1", "– Glide 3.21.2"),
    ("3.21.1 ·", "3.21.2 ·"),
    ("Technische_Fakten_3.21.1.md", "Technische_Fakten_3.21.2.md"),
    ("Manuelle_Pruefung_3.21.1.md", "Manuelle_Pruefung_3.21.2.md"),
    ("Offene_Entscheidungen_3.21.1.md", "Offene_Entscheidungen_3.21.2.md"),
    ("Vorlagen_Praxisanleitung_3.21.1.md", "Vorlagen_Praxisanleitung_3.21.2.md"),
    ("Produktdatenblatt_3.21.1.md", "Produktdatenblatt_3.21.2.md"),
)

# Bedienvertraege tragen die Version, unter der die Funktion entstand.
# QA-Bericht, Weitergabe und der Probelisten-README bekommen eigene Funktionen.
GESCHUETZT = ("45_KALENDERIMPORT_3.21.0.md", "44_KALENDERAUSGABE_3.20.0.md",
              "07_QA_BERICHT.md", "Glide_Weitergabe_neuer_Chat_2026-09-11.md")
NUR_EIGEN = ("05_Probelisten_Testdaten/README.md",)

UMBENENNEN = (
    ("10_Dokumentation/Vorlagen_Praxisanleitung_3.21.1.md",
     "10_Dokumentation/Vorlagen_Praxisanleitung_3.21.2.md"),
    ("40_Store_Material/Produktdatenblatt_3.21.1.md",
     "40_Store_Material/Produktdatenblatt_3.21.2.md"),
)

STAND = f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"

# Gezielte Richtigstellungen. (pflicht, alt, neu) – eine Pflichtstelle, die
# fehlt, bricht den Lauf ab; optionale Stellen werden uebersprungen.
README_REGELN: dict[str, tuple] = {
    f"{REPO_TEIL}/packaging/README.md": (
        (True, "# Paketierung Glide 3.14.0", f"# Paketierung Glide {NEU}\n\n{STAND}"),
    ),
    f"{REPO_TEIL}/src/glide/README.md": (
        (True, "# Anwendungskern Glide 3.14.0", f"# Anwendungskern Glide {NEU}\n\n{STAND}"),
    ),
    f"{REPO_TEIL}/tests/README.md": (
        (True, "# Prüfungen für Glide 3.14.0", f"# Prüfungen für Glide {NEU}"),
        (True, "Stand 13.09.2026. Alle Tests setzen",
         f"Stand 14.09.2026 · Aufgabenformat 15 · 25 Suiten. Alle Tests setzen"),
        (True, "--protokoll tests/qa-3.14.0/abschluss",
         f"--protokoll tests/qa-{NEU}/abschluss"),
    ),
    f"{REPO_TEIL}/tests/fixtures/README.md": (
        (True, "Aktueller Aufgabenstand: **Glide 3.14.0 / Format 14**. `current_v14` enthält",
         f"Aktueller Aufgabenstand: **Glide {NEU} / Format 15**. `current_v15` enthält"),
    ),
    f"{REPO_TEIL}/tests/tools/README.md": (
        (True, "# Prüfwerkzeuge für Glide 3.14.0",
         f"# Prüfwerkzeuge für Glide {NEU}\n\n{STAND}\n\n"
         "Prüfläufe verwenden `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt: In UTC "
         "ist jeder Zeitzonenfehler unsichtbar, weil der Versatz null ist."),
    ),
    f"{REPO_TEIL}/assets/README.md": (
        (True, "# Assets", f"# Assets\n\n{STAND}"),
    ),
    "30_Release_Exports/README.md": (
        (True, "# Glide 3.14.0 – Release_Exports", f"# Glide {NEU} – Release_Exports"),
        (True, "Stand: 13.09.2026 · Aufgabenformat 15",
         "Stand: 14.09.2026 · Aufgabenformat 15"),
        (True, "[Glide 3.14.0](../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.14.0.pyw)",
         f"[Glide {NEU}](../07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw)"),
    ),
    "40_Store_Material/README.md": (
        # Linktext und Ziel liefen auseinander: Der Text sagte 3.21.0, das Ziel
        # war schon die 3.21.1-Datei. Beides wird gemeinsam gesetzt.
        # Nur der Linktext: Das Ziel hat der Tokendurchgang vorher schon
        # gesetzt, und genau daran scheiterte die Regel im Probelauf.
        (True, "[Produktdatenblatt 3.21.0]", f"[Produktdatenblatt {NEU}]"),
        (True, "# Store-Material", f"# Store-Material\n\n{STAND}"),
    ),
    "20_Grafik_Master/README.md": (
        (True, "# Grafik-Master", f"# Grafik-Master\n\n{STAND}"),
    ),
    "50_Ablage/README.md": (
        (True, "# 50_Ablage", f"# 50_Ablage\n\n{STAND}"),
    ),
    "50_Ablage/Screenshots/README.md": (
        (True, "# Screenshots", f"# Screenshots\n\n{STAND}"),
    ),
    "90_Testdaten_Extern/README.md": (
        (True, "# Externe und manuelle Testdaten",
         f"# Externe und manuelle Testdaten\n\n{STAND}"),
    ),
    "50_Ablage/QA/Dokumentation/README.md": (
        # Behauptete einen ueberholten Stand als den aktuellen.
        (True, "Stand der Dokumentationspflege: 13.09.2026 · aktueller Glide-Stand 3.13.0 · Datenformat 13",
         f"Stand der Dokumentationspflege: 14.09.2026 · aktueller Glide-Stand {NEU} · Aufgabenformat 15. "
         "Die hier abgelegten Renderläufe sind historisch und werden nicht nachgezogen; "
         "ihre Versionsangaben gelten für den jeweiligen Lauf."),
    ),
    "50_Ablage/QA/Dokumentation/Renderlaeufe/README.md": (
        (True, "Stand: 04.09.2026 · aktuelle Dokumentversion 3.2.0 · Datenformat 10",
         f"Historischer Lauf vom 04.09.2026 · Dokumentversion 3.2.0 · Datenformat 10. "
         f"Aktueller Glide-Stand ist {NEU} mit Aufgabenformat 15; dieser Ordner wird "
         "bewusst nicht nachgezogen."),
    ),
}


def ablage_wurzel() -> Path:
    for kandidat in (Path.cwd(), *Path.cwd().parents):
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    raise SystemExit("Kein Ablageordner gefunden: im Ordner \"Glide ToDo\" starten.")


SAMMELARCHIV = f"50_Ablage/Archiv/Vorfassungen_vor_{NEU}"


def vorhandenes_archiv(ordner: Path) -> Path | None:
    """Archivordner desselben Ordners in seiner echten Schreibung, falls da."""
    if ordner.is_dir():
        for eintrag in sorted(ordner.iterdir()):
            if eintrag.is_dir() and eintrag.name.lower() == "archiv":
                return eintrag
    return None


class Lauf:
    def __init__(self, wurzel: Path, probe: bool):
        self.wurzel, self.probe = wurzel, probe
        self.geschrieben: list[str] = []
        self.archiviert: list[str] = []
        self.verschoben: list[str] = []
        self.fehler: list[str] = []
        self.schon_archiviert: set[Path] = set()

    def kurz(self, pfad: Path) -> str:
        try:
            return str(pfad.relative_to(self.wurzel))
        except ValueError:
            return str(pfad)

    def archivieren(self, datei: Path) -> None:
        if datei.name == "CHANGELOG.md":
            return  # traegt seine Geschichte selbst
        if datei.resolve() in self.schon_archiviert:
            return
        stem = datei.stem
        rumpf = stem if re.search(r"_\d+\.\d+\.\d+$", stem) else f"{stem}_{ALT}"
        eigenes = vorhandenes_archiv(datei.parent)
        if eigenes is not None:
            # Wo schon ein Archiv steht, bleibt die Geschichte beim Dokument.
            ziel = eigenes / f"{rumpf}_vor_{NEU}{datei.suffix}"
        else:
            # Sonst in ein Sammelarchiv, statt ein Dutzend neue archiv/-Ordner
            # fuer je eine kleine README-Vorfassung anzulegen. Der Pfad steckt
            # im Namen, damit die Herkunft eindeutig bleibt.
            rel = datei.relative_to(self.wurzel).parent.as_posix()
            vorsatz = (rel.replace("/", "__") + "__") if rel not in ("", ".") else ""
            ziel = self.wurzel / SAMMELARCHIV / f"{vorsatz}{rumpf}_vor_{NEU}{datei.suffix}"
        if ziel.exists():
            return
        if not self.probe:
            ziel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(datei, ziel)
        self.archiviert.append(self.kurz(ziel) + ("   (Probe)" if self.probe else ""))

    def schreiben(self, datei: Path, neu: str, alt: str) -> None:
        if neu == alt:
            return
        self.archivieren(datei)
        if not self.probe:
            datei.write_text(neu, encoding="utf-8")
        self.geschrieben.append(self.kurz(datei) + ("   (Probe)" if self.probe else ""))


def tokens_auf_text(text: str) -> str:
    for muster, ersatz in TOKENS:
        text = text.replace(muster, ersatz)
    return text


def aktuelle_dokumente(wurzel: Path):
    for pfad in sorted(wurzel.rglob("*.md")):
        rel = pfad.relative_to(wurzel)
        if any(t.lower().startswith("archiv") for t in rel.parts):
            continue
        if pfad.name in GESCHUETZT or rel.as_posix() in NUR_EIGEN:
            continue
        if re.fullmatch(r"(Technische_Fakten|Manuelle_Pruefung|Offene_Entscheidungen)"
                        r"_\d+\.\d+\.\d+\.md", pfad.name):
            continue
        yield pfad


def umbenennen(lauf: Lauf) -> None:
    for alt_rel, neu_rel in UMBENENNEN:
        a, n = lauf.wurzel / alt_rel, lauf.wurzel / neu_rel
        if n.is_file() and not a.is_file():
            continue
        if not a.is_file():
            lauf.fehler.append(f"Zum Umbenennen fehlt {alt_rel}")
            continue
        archiv = (vorhandenes_archiv(a.parent) or (a.parent / "Archiv")) / a.name
        if not lauf.probe:
            archiv.parent.mkdir(parents=True, exist_ok=True)
            if not archiv.exists():
                shutil.copy2(a, archiv)
            shutil.move(str(a), str(n))
        lauf.verschoben.append(f"{alt_rel} -> {neu_rel}" + ("   (Probe)" if lauf.probe else ""))
        lauf.archiviert.append(lauf.kurz(archiv) + ("   (Probe)" if lauf.probe else ""))
        lauf.schon_archiviert.add(n.resolve())


def tokens_fortschreiben(lauf: Lauf) -> None:
    for pfad in aktuelle_dokumente(lauf.wurzel):
        alt = pfad.read_text(encoding="utf-8")
        lauf.schreiben(pfad, tokens_auf_text(alt), alt)


def readmes_richtigstellen(lauf: Lauf) -> None:
    """Stellen, die kein Token trifft: Titelzeilen, Fettschrift, falsche Stände."""
    for rel, regeln in README_REGELN.items():
        datei = lauf.wurzel / rel
        if not datei.is_file():
            lauf.fehler.append(f"README fehlt: {rel}")
            continue
        alt = datei.read_text(encoding="utf-8")
        neu = alt
        for pflicht, muster, ersatz in regeln:
            # Ergebnis zuerst pruefen: Sonst haengt ein zweiter Lauf die
            # Standzeile ein zweites Mal an eine Titelzeile, die ja bestehen
            # bleibt. Der Probelauf hat genau das gezeigt.
            if ersatz in neu:
                continue
            if muster in neu:
                neu = neu.replace(muster, ersatz, 1)
            elif pflicht:
                lauf.fehler.append(f"{rel}: Pflichtstelle fehlt – {muster[:64]!r}")
        lauf.schreiben(datei, neu, alt)


def probelisten_readme(lauf: Lauf, quelle: Path) -> None:
    src = quelle / "probelisten_README.md"
    if not src.is_file():
        lauf.fehler.append("Im Werkzeugordner fehlt probelisten_README.md")
        return
    datei = lauf.wurzel / "05_Probelisten_Testdaten/README.md"
    alt = datei.read_text(encoding="utf-8") if datei.is_file() else ""
    lauf.schreiben(datei, src.read_text(encoding="utf-8"), alt)


def changelog(lauf: Lauf, eintrag: Path) -> None:
    datei = lauf.wurzel / REPO_TEIL / "CHANGELOG.md"
    alt = datei.read_text(encoding="utf-8")
    if f"## {NEU} " in alt:
        print(f"CHANGELOG: {NEU} steht schon drin")
        return
    kopf = "# Änderungsverlauf\n"
    if not alt.startswith(kopf):
        lauf.fehler.append("CHANGELOG.md beginnt nicht mit der erwarteten Überschrift")
        return
    text = eintrag.read_text(encoding="utf-8").strip() + "\n"
    lauf.schreiben(datei, kopf + "\n" + text + "\n" + alt[len(kopf):].lstrip("\n"), alt)


QA_ANKER = f"Für {ALT} sind alle fünfundzwanzig Suiten"

QA_ALTE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf zu 3.21.1 auf macOS steht aus: "
    "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.1/abschluss`. "
    "Sein Ergebnis wird hier ergänzt."
)
QA_NEUE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf bestand auf macOS mit Python 3.14.5 am 14.09.2026 um "
    "13:34 mit **Exitcode 0**: [Abschlusslauf 3.21.1](../tests/qa-3.21.1/abschluss/ergebnis.json). "
    "Sechsunddreißig Schritte wurden ausgeführt, übersprungen blieben allein die "
    "plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Automatisiert ist 3.21.1 "
    "damit abgenommen – einschließlich Beispiel- und Releaseabgleich, der seit 3.19 nie grün "
    "werden konnte."
)

QA_NEUER_ABSATZ = """Für 3.21.2 sind alle fünfundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb, `TZ=Europe/Berlin`) mit Exitcode 0 gelaufen. 3.21.2 ändert keinen Anwendungscode außer der Versionsangabe; geprüft wird deshalb vor allem der erweiterte Beispielbestand. Er enthielt bis 3.21.1 **keine einzige Erinnerung**, obwohl die Vorlagenanleitung das Gegenteil behauptete, führte nur einen Bearbeitungstag und einen geschätzten Aufwand und kannte von den sechs Wiederholungsarten nur zwei – Tagesplanung, Tageskapazität und der Kalenderrundlauf ließen sich damit nicht sinnvoll ausprobieren. Die neue Liste „Kalender, Erinnerungen und Tagesplanung" bringt sechs Punkte auf einem Bearbeitungstag mit 270 Minuten Gesamtaufwand, beide Erinnerungsarten und alle sechs Wiederholungsarten, darunter die Wochentagsregel mit Enddatum – genau den Fall, der bis 3.21.0 beim Rundlauf um einen Tag verrutschte. Der Bestand wächst von 149 auf 166 Punkte; alle Zusicherungen der Suiten sind Untergrenzen und blieben unverändert. Beispiel- und Releaseabgleich wurden gegen eine unabhängige Zweiterzeugung nachgestellt und fallen gleich aus. Der maßgebliche macOS-Lauf steht aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.2/abschluss`. Sein Ergebnis wird hier ergänzt.

"""


def qa_bericht(lauf: Lauf) -> None:
    datei = lauf.wurzel / REPO_TEIL / "docs/07_QA_BERICHT.md"
    alt = datei.read_text(encoding="utf-8")
    if f"Für {NEU} sind alle" in alt:
        print(f"QA-Bericht: Absatz {NEU} steht schon drin")
        return
    if QA_ALTE_ZUSAGE not in alt:
        lauf.fehler.append(
            "07_QA_BERICHT.md: die Zusage zum ausstehenden 3.21.1-Lauf steht nicht im "
            "erwarteten Wortlaut"
        )
        return
    neu = alt.replace(QA_ALTE_ZUSAGE, QA_NEUE_ZUSAGE, 1)
    if QA_ANKER not in neu:
        lauf.fehler.append(f"07_QA_BERICHT.md: Anker \"{QA_ANKER}\" fehlt")
        return
    neu = neu.replace(QA_ANKER, QA_NEUER_ABSATZ + QA_ANKER, 1)
    neu = neu.replace(f"# QA-Bericht – Glide {ALT}", f"# QA-Bericht – Glide {NEU}", 1)
    lauf.schreiben(datei, tokens_auf_text(neu), alt)


WEITERGABE_KOPF = (
    f"Neu in {NEU}: Der mitgelieferte Beispielbestand deckt die Funktionen seit 3.14 erstmals "
    "testbar ab. Er enthielt keine einzige Erinnerung, führte nur einen Bearbeitungstag und "
    "einen Aufwand und kannte von sechs Wiederholungsarten zwei. Die neue Liste „Kalender, "
    "Erinnerungen und Tagesplanung“ bringt sechs Punkte auf einem Bearbeitungstag mit 270 "
    "Minuten, beide Erinnerungsarten und alle sechs Wiederholungsarten. Anwendungscode "
    "unverändert. "
    "[Probedaten und Prüfwege](../05_Probelisten_Testdaten/README.md)."
)

WEITERGABE_PRUEFSTAND = (
    "Prüfstand: 3.15.0 bis 3.18.0 und **3.21.1** sind automatisiert abgenommen (macOS/Python "
    "3.14.5, Exitcode 0). Der 3.21.1-Lauf vom 14.09.2026 umfasst sechsunddreißig Schritte "
    "einschließlich Beispiel- und Releaseabgleich: `tests/qa-3.21.1/abschluss/ergebnis.json`. "
    "Der Lauf zu 3.21.0 war fehlgeschlagen (Exitcode 1, drei Schritte) – zwei Zeitzonenfehler "
    "im ICS-Rundlauf und ein Fehler im Fixture-Abgleich, der seit 3.19 nie grün werden konnte; "
    "beide Ursachen sind in 3.21.1 behoben, der Beleg bleibt als `tests/qa-3.21.0/abschluss`. "
    "Für 3.19.0 und 3.20.0 wurden keine eigenen macOS-Läufe nachgeholt; sie sind in 3.21.1 "
    "enthalten. Für 3.21.2 sind alle fünfundzwanzig Suiten in der Linux-Vorabumgebung unter "
    "`TZ=Europe/Berlin` mit Exitcode 0 gelaufen; der maßgebliche macOS-Lauf steht aus: "
    "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.2/abschluss`. Offen "
    "bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, "
    "Screenreader, Langzeitbetrieb, Installer und Signierung."
)

WEITERGABE_EINSCHUB = (
    f"Datenregeln von {NEU}: Kein Formatsprung, kein neues Feld, keine Änderung am "
    "Anwendungscode. Der Beispielbestand wächst von 149 auf 166 Punkte und von 11 auf 12 "
    "Listen; alle Zusicherungen der Suiten sind Untergrenzen und bleiben gültig. "
    "`tests/tools/releasedaten.py` bindet seine Standangaben an `APP_VERSION` und die neue "
    "Modulkonstante `DATA_SCHEMA_VERSION`; bis 3.21.1 hing an jedem Codebeleg unverändert "
    "„Stand: 3.14.0 / Datenformat 13“, sieben Versionen überholt. Die Probedateien in "
    "`05_Probelisten_Testdaten` sind die Nutzerkopien der Repo-Bestände und tragen jetzt "
    "denselben Stand; acht überholte Fassungen liegen im Archiv.\n\n"
)


def weitergabe(lauf: Lauf) -> None:
    datei = lauf.wurzel / "00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md"
    alt = datei.read_text(encoding="utf-8")
    if f"Neu in {NEU}:" in alt:
        print(f"Weitergabe: steht schon auf {NEU}")
        return
    neu = tokens_auf_text(alt)

    zeilen = neu.split("\n")
    titel = next((k for k, z in enumerate(zeilen) if z.startswith("# ")), None)
    if titel is None:
        lauf.fehler.append("Weitergabe: keine Titelzeile")
        return
    start = next((k for k in range(titel + 1, len(zeilen)) if zeilen[k].strip()), None)
    if start is None or not zeilen[start].startswith("Neu in "):
        lauf.fehler.append("Weitergabe: Vorspann beginnt nicht mit \"Neu in \"")
        return
    ende = start
    while ende < len(zeilen) and zeilen[ende].strip():
        ende += 1
    zeilen[start:ende] = [WEITERGABE_KOPF]
    neu = "\n".join(zeilen)

    muster = re.compile(r"(?ms)^Prüfstand:.*?(?=\n\s*\n)")
    if not muster.search(neu):
        lauf.fehler.append("Weitergabe: Prüfstandsabsatz nicht gefunden")
        return
    neu = muster.sub(lambda _m: WEITERGABE_PRUEFSTAND, neu, count=1)

    anker = f"Datenregeln von {ALT}:"
    if anker not in neu:
        lauf.fehler.append(f"Weitergabe: Anker \"{anker}\" fehlt")
        return
    if f"Datenregeln von {NEU}:" not in neu:
        neu = neu.replace(anker, WEITERGABE_EINSCHUB + anker, 1)

    lauf.schreiben(datei, neu, alt)


def abgeleitete(lauf: Lauf, quelle: Path) -> None:
    ziele = {
        f"Technische_Fakten_{NEU}.md": "00_Arbeitsvorbereitung/Notizen",
        f"Manuelle_Pruefung_{NEU}.md": "00_Arbeitsvorbereitung/Checklisten",
        f"Offene_Entscheidungen_{NEU}.md": "00_Arbeitsvorbereitung/Entscheidungen",
    }
    for name, ordner in ziele.items():
        src = quelle / name
        if not src.is_file():
            lauf.fehler.append(f"Im Werkzeugordner fehlt abgeleitet/{name}")
            continue
        ziel = lauf.wurzel / ordner / name
        if ziel.is_file() and ziel.read_bytes() == src.read_bytes():
            continue
        if not lauf.probe:
            ziel.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, ziel)
        lauf.geschrieben.append(lauf.kurz(ziel) + ("   (Probe)" if lauf.probe else ""))
        vorher = ziel.parent / name.replace(NEU, ALT)
        if vorher.is_file():
            archiv = (vorhandenes_archiv(vorher.parent) or (vorher.parent / "Archiv")) / vorher.name
            if not archiv.exists():
                if not lauf.probe:
                    archiv.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(vorher), str(archiv))
                lauf.verschoben.append(f"{lauf.kurz(vorher)} -> {lauf.kurz(archiv)}"
                                       + ("   (Probe)" if lauf.probe else ""))


def index_ergaenzen(lauf: Lauf) -> None:
    datei = lauf.wurzel / REPO_TEIL / "docs/00_INDEX.md"
    alt = datei.read_text(encoding="utf-8")
    docs = lauf.wurzel / REPO_TEIL / "docs"
    fehlen = []
    for pfad in sorted(docs.rglob("*.md")):
        rel = pfad.relative_to(docs).as_posix()
        if rel == "00_INDEX.md":
            continue
        if pfad.name not in alt and rel not in alt:
            fehlen.append(rel)
    if not fehlen:
        print("Index: alle docs-Dateien eingetragen")
        return
    lauf.schreiben(datei, alt.rstrip("\n") + "\n"
                   + "".join(f"- [{r}](<{r}>)\n" for r in fehlen), alt)
    for r in fehlen:
        print(f"Index ergänzt: {r}")


def main() -> int:
    p = argparse.ArgumentParser(description=f"Doku-Kette von {ALT} auf {NEU}")
    p.add_argument("quelle", nargs="?", default=f"50_Ablage/Werkzeuge_{NEU}")
    p.add_argument("--probe", action="store_true", help="nur zeigen, nichts schreiben")
    args = p.parse_args()

    wurzel = ablage_wurzel()
    quelle = Path(args.quelle)
    if not quelle.is_absolute():
        quelle = wurzel / quelle
    if not quelle.is_dir():
        raise SystemExit(f"Werkzeugordner fehlt: {quelle}")

    lauf = Lauf(wurzel, args.probe)
    print(f"Ablageordner: {wurzel}")
    print(f"Modus: {'PROBE – es wird nichts geschrieben' if args.probe else 'schreiben'}\n")

    umbenennen(lauf)
    tokens_fortschreiben(lauf)
    readmes_richtigstellen(lauf)
    probelisten_readme(lauf, quelle)
    changelog(lauf, quelle / "changelog_3212.md")
    qa_bericht(lauf)
    weitergabe(lauf)
    abgeleitete(lauf, quelle / "abgeleitet")
    index_ergaenzen(lauf)

    def liste(titel: str, werte: list[str]) -> None:
        print(f"\n{titel} ({len(werte)})")
        for wert in werte:
            print(f"  {wert}")

    liste("Fortgeschrieben", lauf.geschrieben)
    liste("Vorfassungen archiviert", lauf.archiviert)
    liste("Umbenannt oder verschoben", lauf.verschoben)

    if lauf.fehler:
        liste("NICHT ERLEDIGT", lauf.fehler)
        print("\nAbgebrochen: Die genannten Stellen passen nicht zur Erwartung.")
        return 1
    if args.probe:
        print("\nProbe beendet. Ohne --probe erneut aufrufen, um zu schreiben.")
        return 0
    version = (wurzel / REPO_TEIL / "VERSION").read_text(encoding="utf-8").strip()
    print(f"\nVERSION im Repository: {version}")
    print(f"Doku-Kette auf {NEU} fortgeschrieben")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
