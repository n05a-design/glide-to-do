#!/usr/bin/env python3
"""Schreibt die Glide-Dokumentenkette von 3.21.0 auf 3.21.1 fort.

3.21.1 ist eine Fehlerbehebung: kein neues Bedienelement, kein Formatsprung.
Die Kette braucht deshalb vor allem Versionsangaben, einen CHANGELOG-Eintrag,
einen ehrlichen Abschnitt im QA-Bericht (der 3.21.0-Lauf ist fehlgeschlagen)
und die korrigierte Zeitform-Aussage in den beiden Kalenderdokumenten.

Aufruf im Ordner "Glide ToDo":

    python3 fortschreiben_3211.py <Werkzeugordner> --probe    # nur zeigen
    python3 fortschreiben_3211.py <Werkzeugordner>            # schreiben

Der Werkzeugordner enthaelt changelog_3211.md und abgeleitet/.

Grundsaetze: Jede Datei wird als Ganzes berechnet und nur geschrieben, wenn
alle Erwartungen an sie zutreffen. Vorfassungen werden vorher ins archiv/ des
gleichen Ordners kopiert. Es wird nichts geloescht.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ALT, NEU = "3.21.0", "3.21.1"
REPO_TEIL = "01_Repository/Glide"

# Reihenfolge ist bedeutsam: Die spezifischen Muster zuerst, damit das
# allgemeine „3.21.0 ·" nicht schon ersetzte Stellen erneut trifft.
TOKENS = (
    ("Glide 3.21.0 ·", "Glide 3.21.1 ·"),
    ("Entwicklungsstand 3.21.0", "Entwicklungsstand 3.21.1"),
    ("v3.21.0.pyw", "v3.21.1.pyw"),
    ("Stand 3.21.0", "Stand 3.21.1"),
    ("Releaseplanung 3.21.0", "Releaseplanung 3.21.1"),
    ("glide_releaseplanung_3.21.0.glidebackup", "glide_releaseplanung_3.21.1.glidebackup"),
    # Nur der Verweis auf den MASSGEBLICHEN Lauf wandert mit. Ein pauschales
    # „qa-3.21.0 -> qa-3.21.1" hatte im Probelauf genau die Belegstellen
    # zerschrieben, die den fehlgeschlagenen 3.21.0-Lauf absichtlich nennen.
    ("--protokoll tests/qa-3.21.0/abschluss", "--protokoll tests/qa-3.21.1/abschluss"),
    ("Maßgeblich sind tests/qa-3.21.0/abschluss", "Maßgeblich sind tests/qa-3.21.1/abschluss"),
    ("– Glide 3.21.0", "– Glide 3.21.1"),
    ("3.21.0 ·", "3.21.1 ·"),
    ("Vorlagen_Praxisanleitung_3.21.0.md", "Vorlagen_Praxisanleitung_3.21.1.md"),
    ("Produktdatenblatt_3.21.0.md", "Produktdatenblatt_3.21.1.md"),
)

# Diese Dateinamen bleiben, wie sie sind: Bedienvertraege tragen die Version,
# unter der die Funktion entstanden ist. Der QA-Bericht und die Weitergabe
# werden von ihren eigenen Funktionen behandelt – sie bekommen dort erst die
# Tokens und dann ihren neuen Text, damit der Durchgang die eingesetzten
# Belegstellen nicht wieder ueberschreibt.
GESCHUETZT = ("45_KALENDERIMPORT_3.21.0.md", "44_KALENDERAUSGABE_3.20.0.md",
              "07_QA_BERICHT.md", "Glide_Weitergabe_neuer_Chat_2026-09-11.md")

# Versionsbenannte abgeleitete Dokumente: umbenennen statt fortschreiben.
UMBENENNEN = (
    ("10_Dokumentation/Vorlagen_Praxisanleitung_3.21.0.md",
     "10_Dokumentation/Vorlagen_Praxisanleitung_3.21.1.md"),
    ("40_Store_Material/Produktdatenblatt_3.21.0.md",
     "40_Store_Material/Produktdatenblatt_3.21.1.md"),
)

# Der QA-Bericht ist ein flaches Dokument: Titelzeile, dann ein Absatz je
# Version in absteigender Reihenfolge („Für 3.21 …", „Für 3.20 …"). Der neue
# Absatz kommt vor den bisher obersten.
QA_ANKER = "Für 3.21 sind alle fünfundzwanzig Suiten"

# Die bisherige 3.21-Passage behauptet, der macOS-Lauf stehe aus. Er lief –
# und scheiterte. Diese Stelle wird ersetzt, bevor die Tokens greifen.
QA_ALTE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht noch aus: "
    "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.0/abschluss`. "
    "Sein Ergebnis wird hier ergänzt."
)
QA_NEUE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 lief am 14.09.2026 um 11:55 "
    "und **scheiterte mit Exitcode 1**: "
    "[Abschlusslauf 3.21.0](../tests/qa-3.21.0/abschluss/ergebnis.json). Von achtunddreißig "
    "Schritten waren dreiunddreißig ausgeführt, drei fehlgeschlagen – `test_features321`, "
    "Beispieldaten-Abgleich und Release-Abgleich – und zwei übersprungen. Automatisiert ist "
    "3.21.0 damit **nicht** abgenommen; Ursachen und Behebung stehen im Absatz zu 3.21.1."
)

QA_NEUER_ABSATZ = """Für 3.21.1 sind alle fünfundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb) mit Exitcode 0 gelaufen – erstmals unter `TZ=Europe/Berlin` statt UTC. 3.21.1 behebt die drei Fehlschläge des 3.21.0-Laufs, die auf zwei echte Defekte zurückgingen. Erstens die Zeitform von `UNTIL`: Die Kalenderausgabe schrieb das Ende einer Wiederholung als UTC-Zeitpunkt (`…T235959Z`), obwohl `DTSTART` in schwebender Ortszeit beziehungsweise als reines Datum steht. Der Import rechnete folgerichtig in Ortszeit um und landete östlich von Greenwich einen Tag zu spät, westlich einen Tag zu früh – das Enddatum überlebte den Rundlauf nur in der Zeitzone UTC. Dieselbe Verschiebung traf jede fremde Datei, weil Glide auch dort das `UNTIL` als Zeitpunkt statt als Datumsgrenze las. Behoben: Die Ausgabe trägt dieselbe Zeitform wie `DTSTART`, das Lesen nimmt über `parse_ics_until` den Kalendertag ohne Umrechnung. Zweitens die Verlaufszeiten im Fixture-Abgleich: `inhalt_normalisieren` in `pruefen.py` blendete `exported_at`, `deleted_at` und `added_at` aus, nicht aber das Feld `at` der Verlaufseinträge aus 3.19. Der Verlauf entsteht beim Speichern und trägt den echten Zeitpunkt, zwei Erzeugungen im Abstand von Sekunden lieferten also unterschiedliche Werte – „Beispieldaten-Abgleich" und „Release-Abgleich" konnten seit 3.19 **nie** gleich ausfallen. Weil beide Schritte erst ab `--modus voll` laufen und es für 3.19.0 und 3.20.0 keinen macOS-Lauf gab, blieb das bis jetzt unentdeckt. Die Verlaufszeiten bleiben nun genauso draußen wie `exported_at`; Art, Aktion, Ziel, Liste und Anzahl werden weiterhin verglichen.

Dass die Vorabumgebung den Zeitzonenfehler nicht fand, liegt an ihrer Zone: In **UTC** ist jeder Zeitzonenfehler unsichtbar, weil der Versatz null ist – `…T235959Z` bleibt dort der 31.01. Der Prüfstand setzt deshalb `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt, und `test_features321.py` prüft das Enddatum in vier Zonen von `America/New_York` bis `Pacific/Kiritimati`, in allen drei Schreibweisen. Ein gesetztes `TZ` bleibt unangetastet, damit sich jede Zone gezielt nachstellen lässt. Der maßgebliche Abschlusslauf zu 3.21.1 auf macOS steht aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.1/abschluss`. Sein Ergebnis wird hier ergänzt.

"""

WEITERGABE_KOPF = (
    "Neu in 3.21.1: Fehlerbehebung im Kalenderrundlauf. Das Enddatum einer Wiederholung "
    "überlebte „exportieren, importieren“ bisher nur in der Zeitzone UTC – die Ausgabe "
    "schrieb `UNTIL` als UTC-Zeitpunkt, obwohl `DTSTART` in Ortszeit steht. Jetzt trägt "
    "`UNTIL` dieselbe Zeitform, und fremde Angaben werden als Datumsgrenze gelesen statt "
    "umgerechnet. "
    "[Bedienung und Datenregeln](../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md)."
)

WEITERGABE_PRUEFSTAND = (
    "Prüfstand: 3.15.0 bis 3.18.0 sind automatisiert abgenommen (macOS/Python 3.14.5, "
    "Exitcode 0; `tests/qa-3.15.0/abschluss/ergebnis.json` bis "
    "`tests/qa-3.18.0/abschluss/ergebnis.json`). Der Lauf zu **3.21.0 ist fehlgeschlagen** "
    "(Exitcode 1, drei Schritte): zwei Zeitzonenfehler im ICS-Rundlauf und ein Fehler im "
    "Fixture-Abgleich des Prüfstands, der seit 3.19 nie grün werden konnte. Beide Ursachen "
    "sind in 3.21.1 behoben, der Beleg bleibt als `tests/qa-3.21.0/abschluss`. Für 3.21.1 "
    "sind alle fünfundzwanzig Suiten in der Linux-Vorabumgebung mit Exitcode 0 gelaufen, "
    "erstmals unter `TZ=Europe/Berlin` statt UTC; der maßgebliche macOS-Lauf steht aus: "
    "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.1/abschluss`. "
    "Für 3.19.0 und 3.20.0 wurden keine eigenen macOS-Läufe nachgeholt; sie sind in 3.21.1 "
    "enthalten. Offen bleiben die native Sichtabnahme auf macOS und Windows, DPI-/"
    "Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und Signierung."
)

ICS_ZEITFORM = """
## Zeitform des Wiederholungsendes

`UNTIL` trägt dieselbe Zeitform wie `DTSTART`: bei einem Uhrzeittermin schwebende
Ortszeit ohne „Z" (`UNTIL=20270131T235959`), bei einem Ganztagstermin ein reines Datum
(`UNTIL=20270131`). So verlangt es RFC 5545, und nur so überlebt das Enddatum den
Rundlauf in jeder Zeitzone. Bis 3.21.0 stand dort ein UTC-Zeitpunkt; beim Wiedereinlesen
verschob sich das Enddatum östlich von Greenwich um einen Tag.

Beim Lesen gilt die Umkehrung: `UNTIL` ist die Obergrenze einer Terminreihe, kein
Zeitpunkt, den jemand abliest. Glide nimmt deshalb den Kalendertag der Angabe, ohne
Zeitzonenumrechnung – auch bei einem fremden `…T235959Z`, das praktisch jedes
Kalenderprogramm so schreibt. `DTSTART` und Erinnerungen werden weiterhin umgerechnet;
dort ist der Zeitpunkt die Aussage.
"""


def ablage_wurzel() -> Path:
    for kandidat in (Path.cwd(), *Path.cwd().parents):
        if (kandidat / REPO_TEIL / "VERSION").is_file():
            return kandidat
    raise SystemExit(
        "Kein Ablageordner gefunden: Dieses Skript im Ordner \"Glide ToDo\" starten."
    )


def archivordner(datei: Path) -> Path:
    """archiv/ oder Archiv/ desselben Ordners – je nachdem, was schon da ist."""
    for eintrag in sorted(datei.parent.iterdir()) if datei.parent.is_dir() else []:
        if eintrag.is_dir() and eintrag.name.lower() == "archiv":
            return eintrag
    return datei.parent / "archiv"


class Lauf:
    def __init__(self, wurzel: Path, probe: bool):
        self.wurzel = wurzel
        self.probe = probe
        self.geschrieben: list[str] = []
        self.archiviert: list[str] = []
        self.umbenannt: list[str] = []
        self.schon_archiviert: set = set()
        self.fehler: list[str] = []

    def kurz(self, pfad: Path) -> str:
        try:
            return str(pfad.relative_to(self.wurzel))
        except ValueError:
            return str(pfad)

    def archivieren(self, datei: Path) -> None:
        # Der CHANGELOG wird nur oben ergaenzt und traegt seine Geschichte
        # selbst; eine Vorfassung waere eine Verdopplung und braeuchte einen
        # neuen archiv/-Ordner in der Repositoriumswurzel.
        if datei.name == "CHANGELOG.md":
            return
        if datei.resolve() in self.schon_archiviert:
            return
        # Traegt der Name schon eine Version, nicht noch eine anhaengen:
        # aus „Produktdatenblatt_3.21.0" wird „…_3.21.0_vor_3.21.1", nicht
        # „…_3.21.0_3.21.0_vor_3.21.1".
        stem = datei.stem
        rumpf = stem if re.search(r"_\d+\.\d+\.\d+$", stem) else f"{stem}_{ALT}"
        ziel = archivordner(datei) / f"{rumpf}_vor_{NEU}{datei.suffix}"
        if ziel.exists():
            return
        if self.probe:
            self.archiviert.append(self.kurz(ziel) + "   (Probe)")
            return
        ziel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(datei, ziel)
        self.archiviert.append(self.kurz(ziel))

    def schreiben(self, datei: Path, neu: str, alt: str) -> None:
        if neu == alt:
            return
        self.archivieren(datei)
        if not self.probe:
            datei.write_text(neu, encoding="utf-8")
        self.geschrieben.append(self.kurz(datei) + ("   (Probe)" if self.probe else ""))


def aktuelle_dokumente(wurzel: Path):
    for pfad in sorted(wurzel.rglob("*.md")):
        teile = pfad.relative_to(wurzel).parts
        if any(t.lower().startswith("archiv") for t in teile):
            continue
        if pfad.name in GESCHUETZT:
            continue
        yield pfad


def tokens_fortschreiben(lauf: Lauf) -> int:
    """Versionsangaben in allen aktuellen Dokumenten."""
    betroffen = 0
    for pfad in aktuelle_dokumente(lauf.wurzel):
        alt = pfad.read_text(encoding="utf-8")
        neu = alt
        for muster, ersatz in TOKENS:
            neu = neu.replace(muster, ersatz)
        if neu != alt:
            lauf.schreiben(pfad, neu, alt)
            betroffen += 1
    return betroffen


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
    neu = kopf + "\n" + text + "\n" + alt[len(kopf):].lstrip("\n")
    lauf.schreiben(datei, neu, alt)


def tokens_auf_text(text: str) -> str:
    for muster, ersatz in TOKENS:
        text = text.replace(muster, ersatz)
    return text


def qa_bericht(lauf: Lauf) -> None:
    datei = lauf.wurzel / REPO_TEIL / "docs/07_QA_BERICHT.md"
    alt = datei.read_text(encoding="utf-8")
    if f"Für {NEU} sind alle" in alt:
        print(f"QA-Bericht: Absatz {NEU} steht schon drin")
        return

    # 1. Die überholte Zusage zum 3.21.0-Lauf richtigstellen – VOR den Tokens,
    #    weil sie den Protokollpfad in der Zusage sonst schon umgeschrieben
    #    hätten und die Stelle nicht mehr zu finden wäre.
    if QA_ALTE_ZUSAGE not in alt:
        lauf.fehler.append(
            "07_QA_BERICHT.md: die Zusage \"Abschlusslauf … steht noch aus\" zu 3.21.0 "
            "steht nicht im erwarteten Wortlaut"
        )
        return
    neu = alt.replace(QA_ALTE_ZUSAGE, QA_NEUE_ZUSAGE, 1)

    # 2. Neuen Absatz vor den bisher obersten Versionsabsatz setzen.
    if QA_ANKER not in neu:
        lauf.fehler.append(f"07_QA_BERICHT.md: Anker \"{QA_ANKER}\" fehlt")
        return
    neu = neu.replace(QA_ANKER, QA_NEUER_ABSATZ + QA_ANKER, 1)

    # 3. Titelzeile und übrige Versionsangaben.
    neu = neu.replace(f"# QA-Bericht – Glide {ALT}", f"# QA-Bericht – Glide {NEU}", 1)
    neu = tokens_auf_text(neu)
    lauf.schreiben(datei, neu, alt)


def weitergabe(lauf: Lauf) -> None:
    datei = lauf.wurzel / "00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md"
    alt = datei.read_text(encoding="utf-8")
    if f"Neu in {NEU}:" in alt:
        print(f"Weitergabe: steht schon auf {NEU}")
        return
    # Erst die Versionsangaben, dann der neue Text – wie beim QA-Bericht,
    # damit die Belegstelle zum fehlgeschlagenen Lauf erhalten bleibt.
    neu = tokens_auf_text(alt)

    # 1. Vorspann: der erste Absatz nach der Titelzeile.
    zeilen = neu.split("\n")
    titel = next((k for k, z in enumerate(zeilen) if z.startswith("# ")), None)
    if titel is None:
        lauf.fehler.append("Weitergabe: keine Titelzeile gefunden")
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

    # 2. Prüfstandsabsatz: vom Wort „Prüfstand:" bis zur naechsten Leerzeile.
    muster = re.compile(r"(?ms)^Prüfstand:.*?(?=\n\s*\n)")
    if not muster.search(neu):
        lauf.fehler.append("Weitergabe: Prüfstandsabsatz nicht gefunden")
        return
    neu = muster.sub(lambda _m: WEITERGABE_PRUEFSTAND, neu, count=1)

    # 3. Datenregeln der Behebung ergaenzen, direkt vor den 3.20-Regeln.
    einschub = (
        "Datenregeln von 3.21.1: Kein Formatsprung, kein neues Feld. `UNTIL` trägt in der "
        "Kalenderausgabe dieselbe Zeitform wie `DTSTART` – ohne „Z“ beim Uhrzeittermin, als "
        "Datum beim Ganztagstermin. Beim Lesen nimmt `parse_ics_until` den Kalendertag der "
        "Angabe ohne Zeitzonenumrechnung, weil `UNTIL` eine Datumsgrenze ist und kein "
        "Zeitpunkt. Im Prüfstand bleiben die Verlaufszeiten (`history[].at`) aus dem "
        "Fixture-Abgleich heraus, genauso wie `exported_at`; Suiten laufen ohne eigene "
        "Vorgabe unter `TZ=Europe/Berlin`.\n\n"
    )
    anker = "Datenregeln von 3.20:"
    if anker not in neu:
        lauf.fehler.append("Weitergabe: Anker \"Datenregeln von 3.20:\" fehlt")
        return
    if "Datenregeln von 3.21.1:" not in neu:
        neu = neu.replace(anker, einschub + anker, 1)

    lauf.schreiben(datei, neu, alt)


def kalenderdokumente(lauf: Lauf) -> None:
    """Zeitform-Abschnitt in Ausgabe- und Importvertrag ergaenzen."""
    for name in ("docs/44_KALENDERAUSGABE_3.20.0.md", "docs/45_KALENDERIMPORT_3.21.0.md"):
        datei = lauf.wurzel / REPO_TEIL / name
        if not datei.is_file():
            lauf.fehler.append(f"{name} fehlt")
            continue
        alt = datei.read_text(encoding="utf-8")
        if "## Zeitform des Wiederholungsendes" in alt:
            continue
        # Vor dem Abschnitt „Grenzen" einsetzen, sonst vor „Abnahmekriterien",
        # sonst am Ende. Die Reihenfolge haelt die Dokumente vergleichbar.
        stelle = None
        for anker in ("\n## Grenzen", "\n## Abnahmekriterien", "\n## Prüfung"):
            if anker in alt:
                stelle = alt.index(anker)
                break
        neu = (alt[:stelle] + "\n" + ICS_ZEITFORM.strip() + "\n" + alt[stelle:]) if stelle is not None \
            else alt.rstrip("\n") + "\n\n" + ICS_ZEITFORM.strip() + "\n"
        lauf.schreiben(datei, neu, alt)


def abgeleitete(lauf: Lauf, quelle: Path) -> None:
    """Technische Fakten, Manuelle Pruefung, Offene Entscheidungen ablegen."""
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
        # Vorfassung der Vorversion beiseitelegen
        vorher = ziel.parent / name.replace(NEU, ALT)
        if vorher.is_file():
            archiv = archivordner(vorher) / vorher.name
            if not archiv.exists():
                if not lauf.probe:
                    archiv.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(vorher), str(archiv))
                lauf.umbenannt.append(f"{lauf.kurz(vorher)} -> {lauf.kurz(archiv)}"
                                      + ("   (Probe)" if lauf.probe else ""))


def umbenennen(lauf: Lauf) -> None:
    for alt_rel, neu_rel in UMBENENNEN:
        alt_pfad, neu_pfad = lauf.wurzel / alt_rel, lauf.wurzel / neu_rel
        if neu_pfad.is_file() and not alt_pfad.is_file():
            continue
        if not alt_pfad.is_file():
            lauf.fehler.append(f"Zum Umbenennen fehlt {alt_rel}")
            continue
        # Die Vorfassung bleibt unter ihrem eigenen Versionsnamen im Archiv;
        # sie IST der 3.21.0-Stand, ein Zusatz waere ueberfluessig.
        archiv = archivordner(alt_pfad) / alt_pfad.name
        if not lauf.probe:
            archiv.parent.mkdir(parents=True, exist_ok=True)
            if not archiv.exists():
                shutil.copy2(alt_pfad, archiv)
            shutil.move(str(alt_pfad), str(neu_pfad))
        lauf.umbenannt.append(f"{alt_rel} -> {neu_rel}" + ("   (Probe)" if lauf.probe else ""))
        lauf.archiviert.append(lauf.kurz(archiv) + ("   (Probe)" if lauf.probe else ""))
        # Die Vorfassung liegt schon im Archiv. Der folgende Tokendurchgang
        # darf keine zweite, sinnlos benannte Kopie anlegen.
        lauf.schon_archiviert.add(neu_pfad.resolve())


def index_ergaenzen(lauf: Lauf) -> None:
    """Neu archivierte docs-Dateien im Index nachtragen.

    pruefen.py verlangt, dass jede Datei unter docs/ – Archiv eingeschlossen –
    im Index steht. Eingetragen wird am Ende des Archivabschnitts.
    """
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
    zeilen = "".join(f"- [{rel}](<{rel}>)\n" for rel in fehlen)
    neu = alt.rstrip("\n") + "\n" + zeilen
    lauf.schreiben(datei, neu, alt)
    for rel in fehlen:
        print(f"Index ergänzt: {rel}")


def main() -> int:
    p = argparse.ArgumentParser(description=f"Doku-Kette von {ALT} auf {NEU}")
    p.add_argument("quelle", nargs="?", default=f"50_Ablage/Werkzeuge_{NEU}",
                   help="Ordner mit changelog_3211.md und abgeleitet/")
    p.add_argument("--probe", action="store_true",
                   help="nur zeigen, was geändert würde; nichts schreiben")
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
    changelog(lauf, quelle / "changelog_3211.md")
    qa_bericht(lauf)
    weitergabe(lauf)
    kalenderdokumente(lauf)
    abgeleitete(lauf, quelle / "abgeleitet")
    index_ergaenzen(lauf)

    def liste(titel: str, werte: list[str]) -> None:
        print(f"\n{titel} ({len(werte)})")
        for wert in werte:
            print(f"  {wert}")

    liste("Fortgeschrieben", lauf.geschrieben)
    liste("Vorfassungen archiviert", lauf.archiviert)
    liste("Umbenannt oder verschoben", lauf.umbenannt)

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
