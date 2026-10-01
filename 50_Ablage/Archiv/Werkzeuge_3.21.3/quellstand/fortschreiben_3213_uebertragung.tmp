#!/usr/bin/env python3
"""Schreibt die Glide-Dokumentenkette von 3.21.2 auf 3.21.3 fort.

3.21.3 ist ein Dokumentations- und Prüfstandsstand: kein Anwendungscode ausser
der Versionsangabe. Neu ist `tests/tools/standpruefung.py` als dritte Analyse.
Behoben sind die gerotteten Standangaben (sieben Dokumente standen auf 3.21.0),
sechs von Hand gepflegte Banner in historischen Dokumenten, die dreifache
Aussage im PROJECT_HANDOFF und die Luecken in den Funktionsuebersichten.

Aufruf im Ordner "Glide ToDo":

    python3 fortschreiben_3213.py <Werkzeugordner> --probe    # nur zeigen
    python3 fortschreiben_3213.py <Werkzeugordner>            # schreiben

Grundsaetze: Jede Datei wird als Ganzes berechnet und nur geschrieben, wenn alle
Pflichtstellen zutreffen; sonst bricht der Lauf ab und aendert nichts weiter.
Vorfassungen gehen vorher ins archiv/ desselben Ordners. Es wird nichts
geloescht.

Anders als bis 3.21.2: Der Versionsdurchgang ist ein Regexdurchgang mit
geschuetzten Belegstellen, keine Tokenliste. Eine Tokenliste kennt nur die
Schreibweisen, an die jemand gedacht hat - genau daran blieben Wurzel-README,
Repository-README, Dokumentationsindex und vier weitere Dokumente stehen. Der
Probelauf zeigt jede geaenderte Zeile im Wortlaut, damit ein verfaelschtes Zitat
auffaellt, bevor es geschrieben wird.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ALT, NEU = "3.21.2", "3.21.3"
DATUM = "14.09.2026"
REPO_TEIL = "01_Repository/Glide"
STAND = f"Stand {DATUM} · Glide {NEU} · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"

# Ein Wortlaut fuer alle Uebersichten. Die Funktionslisten waren lueckenhaft:
# Der Repository-README nannte zwoelf vorhandene Funktionen nicht, der
# PROJECT_HANDOFF fuenf, der Wurzel-README vier. Wer die Liste an sechs Stellen
# eigenstaendig pflegt, bekommt sechs verschiedene Staende.
GRUNDLAGE = (
    "Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion: "
    "verschachtelte Listen und Ordner, Aufgaben, Long-Tasks, Gruppen, "
    "Überschriften und Unterpunkte, Notizen, Fälligkeit mit Uhrzeit, "
    "Wichtigkeit, sechs Wiederholungsarten, Erinnerungen innerhalb der "
    "laufenden App, Labels, Farben, Beschreibungen und lokale Anhänge an "
    "Punkten, Listen und Ordnern, Kalenderansicht, Suche und Offen-Filter, "
    "Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb, 16 Praxisvorlagen mit "
    "eigenem Katalog zum Bearbeiten, Importieren und Exportieren, TXT-, CSV- "
    "und Markdown-Austausch, portable Aufgabenbackups sowie Hell- und "
    "Dunkelmodus mit Akzentfarbe und drei Schriftgrößen."
)

# Verweis ohne Nummer. Genau so muss ein historisches Dokument auf den
# aktuellen Stand zeigen, damit die Angabe nicht mit der naechsten Version
# falsch wird.
HISTORISCH = ("Dieses Dokument ist ein abgeschlossener Nachweis und wird nicht "
              "nachgezogen. Der aktuelle Stand steht im "
              "[Dokumentationsindex](00_INDEX.md) und im "
              "[QA-Bericht](07_QA_BERICHT.md).")

# Versionsdurchgang. Der Lookaround verhindert nur Treffer innerhalb einer
# laengeren Nummer; Dateinamen wie v3.21.2.pyw sollen ausdruecklich mitgehen.
VERSIONSPASS = re.compile(r"(?<![\d.])" + re.escape(ALT) + r"(?!\d)")

# Belegstellen: Wortlaute, die den 3.21.2-Stand dokumentieren und bleiben
# muessen. Sie werden vor dem Durchgang durch Platzhalter ersetzt und danach
# zurueckgesetzt - eine pauschale Ersetzung haette in 3.21.1 die Stellen
# zerschrieben, die den fehlgeschlagenen Lauf dokumentieren.
BELEGE = (
    f"_vor_{ALT}",          # jede Archivfassung: README_3.21.1_vor_3.21.2.md
    f"_{ALT}_vor_",         # 07_QA_BERICHT_3.21.2_vor_3.21.3.md
    f"vor {ALT}",           # Abschnittstitel im Dokumentationsindex
    f"Werkzeuge_{ALT}",     # Werkzeugordner im Ablagearchiv
    f"qa-{ALT}/abschluss/ergebnis.json",   # Beleg eines abgeschlossenen Laufs
    f"Abschlusslauf {ALT}",
    f"seit {ALT}",          # „deckt diese Funktionen seit 3.21.2 testbar ab"
    f"Neu in {ALT}",        # Aufmacher der Vorlagenanleitung: historisch richtig
    f"Datenregeln von {ALT}",   # je Stand ein eigener Abschnitt der Weitergabe
    f"Für {ALT} sind alle",
    f"Lauf zu {ALT}",       # Nachweis im Produktdatenblatt
    f"{ALT} vor {NEU}",     # Abschnittstitel, den dieser Lauf selbst anlegt
)

# Eigene Funktionen statt Durchgang. CHANGELOG.md ist reine Geschichte; der
# QA-Bericht und die Weitergabe fuehren je Version einen eigenen Abschnitt.
GESCHUETZT = ("CHANGELOG.md", "07_QA_BERICHT.md",
              "Glide_Weitergabe_neuer_Chat_2026-09-11.md")

# Dateien, die mit dem Quellstand ausgeliefert werden (SHA-256-Abgleich in
# ablegen_3213.py). Sie duerfen hier nicht angefasst werden, sonst laufen
# Auslieferung und Fortschreibung auseinander.
AUSGELIEFERT = (f"{REPO_TEIL}/tests/README.md",
                f"{REPO_TEIL}/tests/fixtures/README.md")

# Dateien, die vollstaendig aus dem Werkzeugordner ersetzt werden. Der
# PROJECT_HANDOFF wird neu geordnet statt geflickt: Er behauptete an drei
# Stellen gleichzeitig, 3.15, 3.16 und 3.21 seien das zuletzt umgesetzte
# Funktionspaket, und nannte laengst umgesetzte Funktionen als offene Ideen.
ERSETZEN = {
    f"{REPO_TEIL}/docs/09_PROJECT_HANDOFF.md": "09_PROJECT_HANDOFF.md",
    "05_Probelisten_Testdaten/README.md": "probelisten_README.md",
    "00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.21.3.md": "Technische_Fakten_3.21.3.md",
    "00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.21.3.md": "Manuelle_Pruefung_3.21.3.md",
    "00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.21.3.md": "Offene_Entscheidungen_3.21.3.md",
}

# Vorgaengerfassungen der versionsbenannten Notizen: ins Archiv desselben
# Ordners, wie es dort seit 3.21.0 gehalten wird.
NOTIZEN_ARCHIV = (
    f"00_Arbeitsvorbereitung/Notizen/Technische_Fakten_{ALT}.md",
    f"00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_{ALT}.md",
    f"00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_{ALT}.md",
)

UMBENENNEN = (
    (f"10_Dokumentation/Vorlagen_Praxisanleitung_{ALT}.md",
     f"10_Dokumentation/Vorlagen_Praxisanleitung_{NEU}.md"),
    (f"40_Store_Material/Produktdatenblatt_{ALT}.md",
     f"40_Store_Material/Produktdatenblatt_{NEU}.md"),
)

# --------------------------------------------------------------------------
# Gezielte Richtigstellungen. (pflicht, alt, neu) - eine fehlende Pflichtstelle
# bricht den Lauf ab. Die Regeln laufen NACH dem Versionsdurchgang, die
# Suchtexte tragen deshalb schon die neue Version.
# --------------------------------------------------------------------------
REGELN: dict[str, tuple] = {
    # ---------------------------------------------------------------- Wurzel
    "README.md": (
        # Funktionsluecken: Anhaenge, Hell/Dunkel, Papierkorb, Punktarten.
        (True,
         "Der mitgelieferte Beispielbestand deckt diese Funktionen seit 3.21.2 testbar ab: "
         "[Probedaten und Prüfwege](05_Probelisten_Testdaten/README.md).",
         "Der mitgelieferte Beispielbestand deckt diese Funktionen seit 3.21.2 testbar ab: "
         "[Probedaten und Prüfwege](05_Probelisten_Testdaten/README.md).\n\n"
         + GRUNDLAGE),
    ),
    # ------------------------------------------------------------ Repository
    f"{REPO_TEIL}/README.md": (
        # Der Aufmacher stand auf 3.15, sechs Funktionen spaeter.
        (True,
         "Neu in 3.15: Die Ansicht „Tagesplanung“ zeigt alle Aufgaben mit Bearbeitungstag "
         "an einem wählbaren Tag und stellt ihren geschätzten Aufwand einer selbst "
         "gesetzten Tageskapazität gegenüber. Summen erscheinen auch in „Mein Tag“, in der "
         "Tabelle und auf der Startseite. Keine Zeiterfassung und keine automatische "
         "Terminverteilung. [Bedienung und Datenregeln](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).",
         "Neu in 3.21: Kalenderimport aus ICS. Termine einer Kalenderdatei werden Aufgaben "
         "mit Fälligkeit – mit Dauer als Aufwand, Kategorien als Labels, abbildbaren "
         "Wiederholungen und Erinnerungen, mit Vorschau vor der Übernahme und einem "
         "Rückgängig-Schritt. [Bedienung und Datenregeln](docs/45_KALENDERIMPORT_3.21.0.md)."),
        # Stand auf 3.21.0, zwei Versionssprünge alt.
        (True,
         f"Aktueller interner Entwicklungsstand: **3.21.0** · {DATUM}",
         f"Aktueller interner Entwicklungsstand: **{NEU}** · {DATUM} · Aufgabenformat 15 · "
         "Einstellungen 2 · Vorlagen 2"),
        # „Neu: Die Tabellenansicht …" nannte zwölf vorhandene Funktionen nicht.
        (True,
         "Neu: Die Tabellenansicht zeigt Aufgaben einer Liste kompakt in wählbaren Spalten; "
         "Such-, Offen- und Bearbeitungsaktionen bleiben mit der Listenansicht verbunden. "
         "Dazu kommen „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau und "
         "gespeicherte Filter. Alle Ansichten bearbeiten dieselben Objekte.",
         "Funktionsbestand: Kalenderimport und Kalenderausgabe als ICS, dauerhafter "
         "Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe, "
         "vollständiges App-Backup mit Inhaltsvorschau, Tagesplanung mit Tageskapazität, "
         "Bearbeitungstag und geschätzter Aufwand, Tabellenansicht mit listenspezifischen "
         "Spalten, „Mein Tag“, Schnellerfassung mit deutscher Fristvorschau, gespeicherte "
         "Filter, Reiter und Pinnwände. Alle Ansichten bearbeiten dieselben Objekte.\n\n"
         + GRUNDLAGE),
        (True,
         "Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll "
         f"tests/qa-{NEU}/abschluss`. Alle Tests verwenden isolierte Datenordner.",
         "Prüfung: `python3 tests/tools/pruefen.py --modus voll --protokoll "
         f"tests/qa-{NEU}/abschluss` – 25 Suiten, drei Analysen, Beispiel- und "
         "Releaseabgleich. Alle Tests verwenden isolierte Datenordner."),
    ),
    # -------------------------------------------------- Dokumentationsindex
    f"{REPO_TEIL}/docs/00_INDEX.md": (
        # Das Banner trug die Version doppelt und rottete: Zeile 5 stand
        # richtig, Zeile 3 auf 3.21.0.
        (True,
         "Aktueller Entwicklungsstand: 3.21.0 / Format 15. "
         "[Kalenderimport aus ICS](45_KALENDERIMPORT_3.21.0.md).",
         "Jüngste Bedienergänzung: [Kalenderimport aus ICS](45_KALENDERIMPORT_3.21.0.md). "
         "Der Stand steht in der Zeile darunter und nur dort."),
        # Versionen in Linktexten fortgeschriebener Dokumente rotten. Der
        # QA-Bericht stand hier als „3.21.0", während er bei 3.21.2 lag.
        (True, "- [QA-Bericht 3.21.0](07_QA_BERICHT.md)",
         "- [QA-Bericht](07_QA_BERICHT.md)"),
        (True, "- [Daten, Backups und Migration 3.21.0](06_DATA_BACKUP_MIGRATION.md)",
         "- [Daten, Backups und Migration](06_DATA_BACKUP_MIGRATION.md)"),
        (True, "- [Projektübergabe 3.21.0](09_PROJECT_HANDOFF.md)",
         "- [Projektübergabe](09_PROJECT_HANDOFF.md)"),
        (True, "- [Release-Checkliste 3.21.0](10_RELEASE_CHECKLIST.md)",
         "- [Release-Checkliste](10_RELEASE_CHECKLIST.md)"),
    ),
    # --------------------------------------- Standzeilen ohne Versionsangabe
    # Diese sechs Dokumente werden fortgeschrieben, nannten in der Standzeile
    # aber keine Version. Ein externer Agent konnte nicht erkennen, welchen
    # Stand sie beschreiben - und die Fortschreibung hatte keinen Anker.
    f"{REPO_TEIL}/docs/01_PRODUCT_CONSTRAINTS.md": (
        (True, "Stand 13.09.2026 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2",
         STAND),
    ),
    f"{REPO_TEIL}/docs/02_ARCHITECTURE.md": (
        (True, "Stand 13.09.2026 · Aufgabenformat 15",
         f"Stand {DATUM} · Glide {NEU} · Aufgabenformat 15"),
    ),
    f"{REPO_TEIL}/docs/03_STARTKONTEXT.md": (
        (True, "Stand 13.09.2026 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2",
         STAND),
    ),
    f"{REPO_TEIL}/docs/05_QA_TESTPLAN.md": (
        (True, "Stand 13.09.2026 · alle App-Tests mit isoliertem `GLIDE_DATA_DIR`",
         f"Stand {DATUM} · Glide {NEU} · alle App-Tests mit isoliertem `GLIDE_DATA_DIR`"),
        # „statische Analysen" nannte die Standpruefung nicht mit.
        (True, "Fünfundzwanzig Suiten, Syntax, Versions-/Dokument-/Fixtureprüfung, "
               "statische Analysen sowie reproduzierte Beispiel- und Releasedaten.",
         "Fünfundzwanzig Suiten, Syntax-, Versions-, Dokument- und Fixtureprüfung, die "
         "drei Analysen – statische Analyse, Erreichbarkeit und seit 3.21.3 die "
         "Standprüfung der Dokumente – sowie reproduzierte Beispiel- und Releasedaten. "
         "Neununddreißig Schritte im Vollmodus."),
    ),
    f"{REPO_TEIL}/docs/06_DATA_BACKUP_MIGRATION.md": (
        (True, "Stand 13.09.2026 · Aufgabenformat 15 · Änderungsverlauf in 3.19",
         f"Stand {DATUM} · Glide {NEU} · Aufgabenformat 15 · Änderungsverlauf in 3.19"),
    ),
    f"{REPO_TEIL}/docs/10_RELEASE_CHECKLIST.md": (
        (True, "Stand 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 15",
         f"Stand {DATUM} · Glide {NEU} · interner Entwicklungsstand · Aufgabenformat 15"),
        # Eine Checkliste mit fester Versionsnummer veraltet bei jedem Stand.
        # Sie stand auf 3.21.0, zwei Spruenge alt.
        (True, "- Version, App-Konstante, Hauptsuite, Changelog und aktuelle "
               "Release-Fixtures auf 3.21.0 abstimmen.",
         "- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures "
         "auf die Version aus `VERSION` abstimmen – keine Nummer in diese Zeile "
         "schreiben, sie veraltet sonst bei jedem Stand."),
        (True, "- Einundzwanzig Suiten plus Syntax, Dokumentverweise, Daten-Fixtures, "
               "zwei Analysen und Reproduktion vollständig prüfen.",
         "- Fünfundzwanzig Suiten plus Syntax, Versions- und Dokumentprüfung, "
         "Daten-Fixtures, die drei Analysen und die Reproduktion vollständig prüfen: "
         "neununddreißig Schritte im Vollmodus, von denen regelmäßig nur "
         "Screenshot-Erzeugung und Sichtprüfung übersprungen bleiben."),
    ),
    # ------------------------------------- Banner in historischen Dokumenten
    f"{REPO_TEIL}/docs/08_CODE_BEFUND.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.14.0 / Aufgabenformat 14** mit Bearbeitungstag "
         "und Aufwand. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md), "
         "[QA](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen "
         "älteren Stand.",
         HISTORISCH + " Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand."),
        (True,
         "Der dokumentierte Befund stammt aus dem 3.7-Abgleich. Der aktuelle kumulative\n"
         "Stand ist Glide 3.13.0; dafür gelten [Architektur](02_ARCHITECTURE.md),\n"
         "[QA-Bericht](07_QA_BERICHT.md) und [Tabellenansicht](36_TABELLENANSICHT_3.13.0.md).",
         "Der dokumentierte Befund stammt aus dem 3.7-Abgleich. Für den heutigen Bestand\n"
         "gelten [Architektur](02_ARCHITECTURE.md), [Startkontext](03_STARTKONTEXT.md) und\n"
         "der [QA-Bericht](07_QA_BERICHT.md)."),
    ),
    f"{REPO_TEIL}/docs/11_BESTANDSANALYSE.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.21.0 / Aufgabenformat 15** mit Kalenderimport "
         "aus ICS. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md), [QA](07_QA_BERICHT.md). "
         "Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.",
         HISTORISCH + " Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand."),
        (True,
         "Diese datierte Analyse bleibt als Nachweis erhalten. Der aktuelle Bestand ist\n"
         "Glide 3.21.0; maßgeblich sind [Startkontext](03_STARTKONTEXT.md),\n"
         "[Projektübergabe](09_PROJECT_HANDOFF.md) und [QA-Bericht](07_QA_BERICHT.md).",
         "Diese datierte Analyse bleibt als Nachweis erhalten. Für den heutigen Bestand\n"
         "sind [Startkontext](03_STARTKONTEXT.md), [Projektübergabe](09_PROJECT_HANDOFF.md)\n"
         "und [QA-Bericht](07_QA_BERICHT.md) maßgeblich."),
    ),
    f"{REPO_TEIL}/docs/12_ABSCHLUSSBERICHT.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.21.0 / Aufgabenformat 15** mit Kalenderimport "
         "aus ICS. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md), [QA](07_QA_BERICHT.md). "
         "Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.",
         HISTORISCH + " Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand."),
        (True,
         "Dieser Bericht dokumentiert den damaligen Erinnerungsstand. Der aktuelle\n"
         "Arbeitsstand ist Glide 3.21.0; der aktuelle Prüfstand steht im\n"
         "[QA-Bericht](07_QA_BERICHT.md), die jüngste Bedienergänzung in\n"
         "[Kalenderimport aus ICS](45_KALENDERIMPORT_3.21.0.md).",
         "Dieser Bericht dokumentiert den damaligen Erinnerungsstand. Der heutige\n"
         "Prüfstand steht im [QA-Bericht](07_QA_BERICHT.md), die jüngste Bedienergänzung\n"
         "in [Kalenderimport aus ICS](45_KALENDERIMPORT_3.21.0.md)."),
    ),
    f"{REPO_TEIL}/docs/25_FEATURE_ABGLEICH_3.7.0.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.21.0 / Aufgabenformat 15** mit Kalenderimport "
         "aus ICS. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md), [QA](07_QA_BERICHT.md). "
         "Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.",
         HISTORISCH + " Die folgende Matrix gehört zum Stand von 3.7."),
        (True,
         "Dieses Dokument beschreibt die historische 3.7-Matrix. Der aktuelle Ausbau bis\n"
         "3.14 steht in der [Funktionsübersicht](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md),\n"
         "der [Tabellenansicht](36_TABELLENANSICHT_3.13.0.md) und den aktuellen technischen\n"
         "Dokumenten.",
         "Dieses Dokument beschreibt die historische 3.7-Matrix. Der heutige Ausbau steht\n"
         "in der [Funktionsübersicht](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md)\n"
         "und in der [Projektübergabe](09_PROJECT_HANDOFF.md)."),
    ),
    f"{REPO_TEIL}/docs/28_ABLAGEPRUEFUNG_2026-09-11.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.14.0 / Aufgabenformat 14** mit Bearbeitungstag "
         "und Aufwand. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md), "
         "[QA](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen "
         "älteren Stand.",
         HISTORISCH),
        (True,
         "Dieser datierte Abgleich beschreibt die damalige 3.7-Ablage. Der aktuelle\n"
         "Arbeitsstand ist Glide 3.13.0; maßgeblich sind der [Dokumentationsindex](00_INDEX.md),\n"
         "die [3.13-Bedienung](36_TABELLENANSICHT_3.13.0.md) und der [aktuelle QA-Bericht](07_QA_BERICHT.md).",
         "Dieser datierte Abgleich beschreibt die damalige 3.7-Ablage. Für den heutigen\n"
         "Stand sind der [Dokumentationsindex](00_INDEX.md) und der\n"
         "[QA-Bericht](07_QA_BERICHT.md) maßgeblich."),
    ),
    f"{REPO_TEIL}/docs/30_DOKUMENTATIONSABGLEICH_2026-09-12.md": (
        (True,
         "Aktueller Entwicklungsstand: **3.14.0 / Aufgabenformat 14** mit Bearbeitungstag "
         "und Aufwand. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md), "
         "[QA](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen "
         "älteren Stand.",
         HISTORISCH),
    ),
    # ----------------------------------- Reiterentwurf und Entscheidungssatz
    f"{REPO_TEIL}/docs/32_REITERANSICHT.md": (
        (True, "Stand: 13.09.2026 · **Umgesetzt in 3.10.0** ·\n"
               "Aufgabenformat bleibt 13, Einstellungen bleiben Format 2.",
         "Abgeschlossener Entwurf · **umgesetzt in 3.10.0**, damals ohne Formatsprung\n"
         "(Aufgabenformat 13, Einstellungen 2). Der ausgeführte Bedienvertrag steht in\n"
         "[Reiter und Pinnwand 3.10.0](33_REITER_UND_PINNWAND_3.10.0.md), der heutige\n"
         "Stand im [Dokumentationsindex](00_INDEX.md)."),
        (True, "# Reiteransicht für Listenelemente – Bedienvertrag",
         "# Reiteransicht für Listenelemente – historischer Entwurf 3.10.0"),
    ),
    f"{REPO_TEIL}/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md": (
        (True, "Stand: 12.09.2026 · Ausgangspunkt: Glide 3.8.0, erste lokale Erinnerungsstufe.",
         f"Stand: {DATUM} · Glide {NEU}, Entscheidung unverändert gültig · Ausgangspunkt: "
         "Glide 3.8.0, erste lokale Erinnerungsstufe."),
    ),
    # Entscheidungsvermerk ohne jede Standangabe: Ein Leser konnte nicht
    # erkennen, ob die Entscheidung noch gilt.
    f"{REPO_TEIL}/docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md": (
        (True, "# Gruppe, Ordner oder Zwischenüberschrift?\n",
         "# Gruppe, Ordner oder Zwischenüberschrift?\n\n"
         f"Stand: {DATUM} · Glide {NEU} · Entscheidung unverändert gültig.\n"),
    ),
    # --------------------------------------------------------- Release-Exports
    "30_Release_Exports/README.md": (
        (True, "Stand: 14.09.2026 · Aufgabenformat 15 · unveröffentlichter Entwicklungsstand",
         f"Stand: {DATUM} · Glide {NEU} · Aufgabenformat 15 · unveröffentlichter "
         "Entwicklungsstand"),
    ),
    # ------------------------------------------------------- Funktionsliste
    "00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md": (
        (True, "Stand: 13.09.2026 · Aktueller Entwicklungsstand: Glide 3.17.0",
         f"Stand: {DATUM} · Glide {NEU} · Aufgabenformat 15"),
        (True,
         "In 3.14 folgen Bearbeitungstag und Aufwand, in 3.15 die Tagesplanung mit "
         "Tageskapazität in 3.16 das vollständige App-Backup und in 3.17 die Druck- und "
         "PDF-Ausgabe. Weitere Stufen und Ideen bleiben offen.",
         "In 3.14 folgten Bearbeitungstag und Aufwand, in 3.15 die Tagesplanung mit "
         "Tageskapazität, in 3.16 das vollständige App-Backup, in 3.17 die Druck- und "
         "PDF-Ausgabe, in 3.18 der CSV-Import mit Spaltenzuordnung, in 3.19 der dauerhafte "
         "Änderungsverlauf mit Aufgabenformat 15, in 3.20 die Kalenderausgabe als ICS und "
         "in 3.21 der Kalenderimport aus ICS. Offen sind benutzerdefinierte Felder und "
         "darauf aufbauende eigene Ansichten; eine echte Kalendersynchronisierung bleibt "
         "bewusst außen vor."),
    ),
    "00_Arbeitsvorbereitung/README.md": (
        (True,
         "Stand 14.09.2026. [Aktueller Ausbau: Kalenderimport aus ICS 3.21.0]"
         "(../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md).",
         f"{STAND}. Jüngste Bedienergänzung: [Kalenderimport aus ICS]"
         "(../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md)."),
    ),
    # ------------------------------------------------------ 10_Dokumentation
    "10_Dokumentation/README.md": (
        (True, "Stand 14.09.2026 · Glide 3.21.0", STAND),
    ),
    # ------------------------------------------------------------ Storeangaben
    "40_Store_Material/Apple/Store_Angaben_Apple.md": (
        (True,
         "Arbeitsstand: 13.09.2026 · Quellenabruf: 04.09.2026 · erhoben auf Grundlage von "
         "Glide 3.14.0 / Datenformat 13.",
         f"Arbeitsstand: {DATUM} · Glide {NEU} · Quellenabruf: 04.09.2026. Die "
         "Store-Vorgaben unten sind auf Grundlage von Glide 3.14.0 / Datenformat 13 "
         "erhoben."),
    ),
    "40_Store_Material/Microsoft/Store_Angaben_Microsoft.md": (
        (True,
         "Arbeitsstand: 13.09.2026 · Quellenabruf: 04.09.2026 · erhoben auf Grundlage von "
         "Glide 3.14.0 / Datenformat 13.",
         f"Arbeitsstand: {DATUM} · Glide {NEU} · Quellenabruf: 04.09.2026. Die "
         "Store-Vorgaben unten sind auf Grundlage von Glide 3.14.0 / Datenformat 13 "
         "erhoben."),
    ),
    # ----------------------------------------------------- Startbare Fassungen
    "07_Python-Versionen/README.md": (
        (True, "Vorherige startbare Versionen bleiben erhalten.",
         "Vorherige startbare Fassungen liegen im Unterordner `Archiv`. Seit 3.14 war das "
         "nicht nachgezogen worden; mit diesem Stand ist es erledigt, und nur die "
         "aktuelle Fassung liegt aktiv im Ordner."),
        (True,
         "Neu in 3.18: CSV-Import mit Spaltenzuordnung. Trennzeichen und Kodierung werden "
         "erkannt und sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine "
         "Vorschau zeigt das Ergebnis vor der Übernahme; eine mit „Als CSV“ geschriebene "
         "Liste ist vollständig zurücklesbar. [Bedienung und Datenregeln]"
         "(../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).",
         "Neu in 3.21: Kalenderimport aus ICS. [Bedienung und Datenregeln]"
         "(../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md)."),
    ),
    # ---------------------------------------------------- Produktdatenblatt
    f"40_Store_Material/Produktdatenblatt_{NEU}.md": (
        (True, "# Glide Produktdatenblatt 3.21.0", f"# Glide Produktdatenblatt {NEU}"),
        (True,
         "Neu in 3.18: CSV-Import mit Spaltenzuordnung. Trennzeichen und Kodierung werden "
         "erkannt und sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine "
         "Vorschau zeigt das Ergebnis vor der Übernahme; eine mit „Als CSV“ geschriebene "
         "Liste ist vollständig zurücklesbar. [Bedienung und Datenregeln]"
         "(../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).",
         "Neu in 3.21: Kalenderimport aus ICS. Termine einer Kalenderdatei werden Aufgaben "
         "mit Fälligkeit – mit Dauer als Aufwand, Kategorien als Labels, abbildbaren "
         "Wiederholungen und Erinnerungen, mit Vorschau vor der Übernahme und einem "
         "Rückgängig-Schritt. [Bedienung und Datenregeln]"
         "(../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md)."),
        (True, "Stand: 13.09.2026 · lokaler Entwicklungsstand · Aufgabenformat 15 ·",
         f"Stand: {DATUM} · Glide {NEU} · lokaler Entwicklungsstand · Aufgabenformat 15 ·"),
        # Schnellerfassung fehlte in der Bedienzeile.
        (True,
         "| Bedienung | Suche, Offen-Filter, gespeicherte Filter, Mehrfachauswahl, Ziehen, "
         "Rückgängig und Papierkorb |",
         "| Bedienung | Suche, Offen-Filter, gespeicherte Filter, Schnellerfassung mit "
         "deutscher Fristvorschau, Mehrfachauswahl, Ziehen, Rückgängig und Papierkorb |"),
        # Die Aussage war unbelegt: Zum Zeitpunkt des Satzes gab es den
        # macOS-Lauf noch nicht, und sie blieb stehen, als er vorlag.
        (True,
         f"Der 3.21-Stand ist lokal geprüft: 25 Testsuiten, statische Analysen sowie\n"
         "Beispiel- und Releaseabgleiche sind in einer Vorabumgebung erfolgreich; der\n"
         "abschließende macOS-Lauf wird im QA-Bericht nachgewiesen.",
         "Der 3.21-Stand ist lokal geprüft. Der maßgebliche Lauf zu 3.21.2 bestand am "
         f"{DATUM}\n"
         "auf macOS mit Python 3.14.5 mit Exitcode 0: 25 Suiten, statische Analysen sowie\n"
         "Beispiel- und Releaseabgleich. Der Nachweis je Stand steht im QA-Bericht."),
    ),
    # ------------------------------------------------ Vorlagen-Praxisanleitung
    f"10_Dokumentation/Vorlagen_Praxisanleitung_{NEU}.md": (
        (False, f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Vorlagenformat 2",
         f"Stand {DATUM} · Glide {NEU} · Aufgabenformat 15 · Vorlagenformat 2"),
    ),
}

# ------------------------------------------------------------------ Weitergabe
WEITERGABE_KOPF = (
    f"Neu in {NEU}: Der Prüfstand prüft die Dokumentation jetzt auch inhaltlich. "
    "`tests/tools/standpruefung.py` vergleicht jede aktive Standangabe der Ablage mit "
    "`VERSION`; historische Dokumente dürfen keinen aktuellen Stand behaupten. Anlass: "
    "Sieben Dokumente standen zwei Versionssprünge lang auf 3.21.0, ohne dass eine "
    "Prüfung das finden konnte. Anwendungscode unverändert. "
    "[Prüfungen und Umfang](../01_Repository/Glide/tests/README.md)."
)

WEITERGABE_UMGESETZT = (
    "Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und "
    "Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“, die Tabellenansicht "
    "mit listenspezifischen Spalten, Bearbeitungstag und Aufwand, die Tagesplanung mit "
    "Tageskapazität, das vollständige App-Backup mit Inhaltsvorschau, die Druck- und "
    "PDF-Ausgabe, der CSV-Import mit Spaltenzuordnung, der dauerhafte Änderungsverlauf "
    "sowie Kalenderausgabe und Kalenderimport als ICS. Alle Ansichten zeigen dieselben "
    "Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.\n\n" + GRUNDLAGE
)

WEITERGABE_PRUEFSTAND = (
    "Prüfstand: 3.15.0 bis 3.18.0, **3.21.1** und **3.21.2** sind automatisiert "
    "abgenommen (macOS/Python 3.14.5, Exitcode 0). Der 3.21.2-Lauf vom 14.09.2026 um "
    "15:04 umfasst sechsunddreißig von achtunddreißig Schritten einschließlich Beispiel- "
    "und Releaseabgleich: `tests/qa-3.21.2/abschluss/ergebnis.json`; übersprungen blieben "
    "allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Der Lauf zu "
    "3.21.0 war fehlgeschlagen (Exitcode 1, drei Schritte) – zwei Zeitzonenfehler im "
    "ICS-Rundlauf und ein Fehler im Fixture-Abgleich, der seit 3.19 nie grün werden "
    "konnte; beide Ursachen sind in 3.21.1 behoben, der Beleg bleibt als "
    "`tests/qa-3.21.0/abschluss`. Für 3.19.0 und 3.20.0 wurden keine eigenen macOS-Läufe "
    f"nachgeholt; sie sind im 3.21.1-Lauf enthalten. Für {NEU} sind alle fünfundzwanzig "
    "Suiten und die drei Analysen in der Linux-Vorabumgebung unter `TZ=Europe/Berlin` mit "
    "Exitcode 0 gelaufen – ausgenommen der Dokumentationsindex, weil die Dokumente dort "
    "nicht mitkopiert sind. Der maßgebliche macOS-Lauf steht aus: `python3 "
    f"tests/tools/pruefen.py --modus voll --protokoll tests/qa-{NEU}/abschluss`. Offen "
    "bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, "
    "Screenreader, Langzeitbetrieb, Installer und Signierung."
)

WEITERGABE_EINSCHUB = (
    f"Datenregeln von {NEU}: Kein Formatsprung, kein neues Feld, keine Änderung am "
    "Anwendungscode. Neu ist `tests/tools/standpruefung.py` als dritte Analyse: Ein "
    "Dokument mit Version oder Datum im Dateinamen, in einem Versionsordner oder mit "
    "„historisch“ im Titel gilt als **festgeschrieben** und darf keinen aktuellen Stand "
    "behaupten; jedes andere aktive Dokument muss eine Standzeile mit der Version aus "
    "`VERSION` tragen. Zitate und Codespannen sind ausgenommen, sonst meldet die Prüfung "
    "den Satz, der den Fehler dokumentiert. `tests/README.md` und "
    "`tests/fixtures/README.md` werden seit 3.21.3 mit dem Quellstand ausgeliefert und "
    "gehen damit über den SHA-256-Abgleich statt über Fortschreibungsregeln.\n\n"
)

WEITERGABE_FALLE = (
    "- **Ein von Hand gepflegtes Banner „Aktueller Entwicklungsstand“ rottet.** Sechs "
    "historische Dokumente trugen eines; drei standen auf 3.14.0, drei auf 3.21.0. "
    "Historische Dokumente verweisen ohne Nummer auf Index und QA-Bericht, dann kann die "
    "Angabe nicht falsch werden. Die Version steht in genau einer Zeile je Dokument, und "
    "`tests/tools/standpruefung.py` prüft das.\n"
    "- **Versionen in Linktexten fortgeschriebener Dokumente rotten genauso.** Im Index "
    "stand „QA-Bericht 3.21.0“, während der Bericht bei 3.21.2 lag. Linktext ohne Nummer, "
    "wenn das Ziel fortgeschrieben wird.\n"
    "- **Die neunzehn versionierten Releaseplanungen in `tests/fixtures/beispiele` "
    "gehören nicht ins Archiv.** Die Fixtureprüfung erwartet bei versioniertem Dateinamen "
    "genau dessen Version; die Reihe ist der Migrationsnachweis. Nur die unversionierten "
    "Bestände werden ersetzt und ihre Vorfassung archiviert.\n"
)


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


def unterschiede(kurz: str, alt: str, neu: str) -> list[str]:
    """Geänderte Zeilen im Wortlaut. Ein verfälschtes Zitat fällt nur auf,
    wenn man es liest: „Glide 3.21.1 · Aufgabenformat 15" wurde in 3.21.2 von
    einem Tokendurchgang angehoben und der Satz damit sinnlos."""
    a, b = alt.splitlines(), neu.splitlines()
    aus: list[str] = []
    for nr, (x, y) in enumerate(zip(a, b), 1):
        if x != y:
            aus.append(f"  {kurz}:{nr}\n      alt: {x.strip()[:200]}"
                       f"\n      neu: {y.strip()[:200]}")
    if len(a) != len(b):
        aus.append(f"  {kurz}: Zeilenzahl {len(a)} -> {len(b)}")
    return aus


def versionspass(text: str) -> str:
    """Regexdurchgang mit geschützten Belegstellen."""
    platzhalter = {}
    for nr, beleg in enumerate(BELEGE):
        marke = f"\x00BELEG{nr}\x00"
        if beleg in text:
            platzhalter[marke] = beleg
            text = text.replace(beleg, marke)
    text = VERSIONSPASS.sub(NEU, text)
    for marke, beleg in platzhalter.items():
        text = text.replace(marke, beleg)
    return text


class Lauf:
    """Führt jede Datei als Textpuffer und schreibt erst am Ende.

    Bis 3.21.2 las jeder Schritt die Datei erneut von der Platte. Im Probelauf
    stand dort noch der alte Text, weil nichts geschrieben wurde – eine Regel,
    deren Suchtext erst durch den Versionsdurchgang entsteht, schlug im
    Probelauf fehl und im Schreiblauf nicht. Ein Probelauf, der anders rechnet
    als der Schreiblauf, ist wertlos. Deshalb ein Puffer je Pfad: Durchgang,
    Regeln und Sonderfunktionen arbeiten in beiden Läufen auf demselben Text,
    und die Platte wird erst in `abschluss()` angefasst.
    """

    def __init__(self, wurzel: Path, probe: bool):
        self.wurzel, self.probe = wurzel, probe
        self.puffer: dict[str, str] = {}        # Pfad -> aktueller Text
        self.ausgang: dict[str, str] = {}       # Pfad -> Text beim Einlesen
        self.umzug: list[tuple[str, str]] = []  # (alt, neu) für Umbenennungen
        self.fehler: list[str] = []
        self.hinweise: list[str] = []

    def pfad(self, rel: str) -> Path:
        return self.wurzel / rel

    def lese(self, rel: str) -> str | None:
        """Text aus dem Puffer, sonst von der Platte; None, wenn es ihn nicht
        gibt."""
        if rel in self.puffer:
            return self.puffer[rel]
        datei = self.pfad(rel)
        if not datei.is_file():
            return None
        text = datei.read_text(encoding="utf-8")
        self.puffer[rel] = text
        self.ausgang[rel] = text
        return text

    def setze(self, rel: str, neu: str) -> None:
        """Neuen Text übernehmen. Geschrieben wird erst in `abschluss()`."""
        alt = self.lese(rel)
        if alt is None:
            self.ausgang.setdefault(rel, "")
        self.puffer[rel] = neu

    def geaendert(self) -> list[str]:
        return [rel for rel, text in sorted(self.puffer.items())
                if text != self.ausgang.get(rel, "")]

    # -- Archivierung ----------------------------------------------------
    def archivziel(self, rel: str) -> str | None:
        """Wohin die Vorfassung gehört, als Pfad unter der Ablagewurzel.

        Wo schon ein Archivordner steht, bleibt die Geschichte beim Dokument.
        Sonst in ein Sammelarchiv, statt für je eine kleine README-Vorfassung
        ein Dutzend neue archiv/-Ordner anzulegen; der Pfad steckt dann im
        Namen, damit die Herkunft eindeutig bleibt.
        """
        datei = self.pfad(rel)
        if datei.name == "CHANGELOG.md":
            return None            # trägt seine Geschichte selbst
        stem, suffix = datei.stem, datei.suffix
        rumpf = stem if re.search(r"_\d+\.\d+\.\d+$", stem) else f"{stem}_{ALT}"
        eigenes = vorhandenes_archiv(datei.parent)
        if eigenes is not None:
            return f"{eigenes.relative_to(self.wurzel).as_posix()}/{rumpf}_vor_{NEU}{suffix}"
        ordner = Path(rel).parent.as_posix()
        vorsatz = (ordner.replace("/", "__") + "__") if ordner not in ("", ".") else ""
        return f"{SAMMELARCHIV}/{vorsatz}{rumpf}_vor_{NEU}{suffix}"

    def docs_archiv(self) -> list[str]:
        """Archivfassungen unter docs/, relativ zu docs/ – für die Indexpflicht.

        Der 3.21.2-Nachtrag hat einen solchen Eintrag vergessen und den
        Prüfstand fehlschlagen lassen; deshalb sammelt der Lauf sie selbst.
        """
        marke = f"{REPO_TEIL}/docs/"
        aus = []
        for rel in self.geaendert():
            if not rel.startswith(marke):
                continue
            ziel = self.archivziel(rel)
            if ziel and ziel.startswith(marke):
                aus.append(ziel[len(marke):])
        for alt_rel, _neu_rel in self.umzug:
            if alt_rel.startswith(marke):
                datei = self.pfad(alt_rel)
                eigenes = vorhandenes_archiv(datei.parent) or (datei.parent / "Archiv")
                ziel = f"{eigenes.relative_to(self.wurzel).as_posix()}/{datei.name}"
                if ziel.startswith(marke):
                    aus.append(ziel[len(marke):])
        return sorted(set(aus))

    # -- Schreiben -------------------------------------------------------
    def abschluss(self) -> tuple[list[str], list[str], list[str], list[str]]:
        """Umbenennen, archivieren, schreiben. Im Probelauf wird nur gemeldet."""
        verschoben, archiviert, geschrieben, zeilen = [], [], [], []
        vermerk = "   (Probe)" if self.probe else ""

        for alt_rel, neu_rel in self.umzug:
            a, n = self.pfad(alt_rel), self.pfad(neu_rel)
            archiv = (vorhandenes_archiv(a.parent) or (a.parent / "Archiv")) / a.name
            if not self.probe:
                archiv.parent.mkdir(parents=True, exist_ok=True)
                if not archiv.exists():
                    shutil.copy2(a, archiv)
                shutil.move(str(a), str(n))
                if a.exists():
                    raise SystemExit(f"Quelle liegt nach dem Umbenennen noch da: {a}")
            verschoben.append(f"{alt_rel} -> {neu_rel}{vermerk}")
            archiviert.append(f"{archiv.relative_to(self.wurzel).as_posix()}{vermerk}")

        for rel in self.geaendert():
            alt, neu = self.ausgang.get(rel, ""), self.puffer[rel]
            umgezogen = any(rel == n for _a, n in self.umzug)
            if alt and not umgezogen:
                ziel_rel = self.archivziel(rel)
                if ziel_rel:
                    ziel = self.pfad(ziel_rel)
                    if not ziel.exists():
                        if not self.probe:
                            ziel.parent.mkdir(parents=True, exist_ok=True)
                            ziel.write_text(alt, encoding="utf-8")
                        archiviert.append(f"{ziel_rel}{vermerk}")
            if not self.probe:
                datei = self.pfad(rel)
                datei.parent.mkdir(parents=True, exist_ok=True)
                datei.write_text(neu, encoding="utf-8")
            geschrieben.append(f"{rel}{vermerk}")
            zeilen.extend(unterschiede(rel, alt, neu))
        return verschoben, archiviert, geschrieben, zeilen


def aktuelle_dokumente(lauf: Lauf) -> list[str]:
    """Aktive Dokumente, die den Versionsdurchgang bekommen – als Pfade."""
    umgezogen = {a for a, _n in lauf.umzug}
    neue = {n for _a, n in lauf.umzug}
    aus: list[str] = []
    for datei in sorted(lauf.wurzel.rglob("*.md")):
        rel = datei.relative_to(lauf.wurzel).as_posix()
        if rel in umgezogen:
            continue
        aus.append(rel)
    aus.extend(neue)
    ergebnis = []
    for rel in sorted(set(aus)):
        teile = Path(rel).parts
        if any(t.lower().startswith("archiv") for t in teile):
            continue
        # Der Werkzeugordner dieses Sprungs ist Quellmaterial, kein Dokument
        # der Ablage. Der Probelauf hat gezeigt, was ohne diese Zeile passiert:
        # Der Durchgang hob „Bis 3.21.2 stand derselbe Satz dreimal darin" und
        # „Der maßgebliche 3.21.2-Lauf" auf die neue Version - und hätte damit
        # genau die historischen Aussagen zerschrieben, die diesen Stand
        # begründen. Ein zweiter Lauf hätte den falschen Text dann in den
        # Änderungsverlauf des Repositorys übernommen.
        if any(t.startswith("Werkzeuge_") for t in teile):
            continue
        if Path(rel).name in GESCHUETZT:
            continue
        if rel in ERSETZEN or rel in AUSGELIEFERT:
            continue
        # Versionsbenannte Notizen beschreiben je einen Stand und gehen nicht
        # mit; die 3.21.3-Fassungen kommen aus dem Werkzeugordner.
        if re.fullmatch(r"(Technische_Fakten|Manuelle_Pruefung|Offene_Entscheidungen)"
                        r"_\d+\.\d+\.\d+\.md", Path(rel).name):
            continue
        ergebnis.append(rel)
    return ergebnis


def umbenennen(lauf: Lauf) -> None:
    for alt_rel, neu_rel in UMBENENNEN:
        a, n = lauf.pfad(alt_rel), lauf.pfad(neu_rel)
        if n.is_file() and not a.is_file():
            continue                      # zweiter Lauf
        if not a.is_file():
            lauf.fehler.append(f"Zum Umbenennen fehlt {alt_rel}")
            continue
        inhalt = a.read_text(encoding="utf-8")
        lauf.umzug.append((alt_rel, neu_rel))
        lauf.puffer[neu_rel] = inhalt
        lauf.ausgang[neu_rel] = inhalt


def notizen_ersetzen(lauf: Lauf, quelle: Path) -> None:
    """Die drei versionsbenannten Notizen: Vorfassung ins Archiv, neue Fassung
    aus dem Werkzeugordner."""
    for alt_rel in NOTIZEN_ARCHIV:
        a = lauf.pfad(alt_rel)
        if not a.is_file():
            lauf.hinweise.append(f"Vorfassung schon verschoben: {alt_rel}")
            continue
        archiv = (vorhandenes_archiv(a.parent) or (a.parent / "Archiv")) / a.name
        if archiv.exists():
            continue
        lauf.umzug.append((alt_rel, archiv.relative_to(lauf.wurzel).as_posix()))

    for ziel_rel, name in ERSETZEN.items():
        src = quelle / name
        if not src.is_file():
            lauf.fehler.append(f"Im Werkzeugordner fehlt {name}")
            continue
        lauf.setze(ziel_rel, src.read_text(encoding="utf-8"))


def dokumente_fortschreiben(lauf: Lauf) -> None:
    for rel in aktuelle_dokumente(lauf):
        alt = lauf.lese(rel)
        if alt is None:
            continue
        lauf.setze(rel, versionspass(alt))


def regeln_anwenden(lauf: Lauf) -> None:
    for rel, regeln in REGELN.items():
        alt = lauf.lese(rel)
        if alt is None:
            lauf.fehler.append(f"Datei fehlt: {rel}")
            continue
        neu = alt
        for pflicht, muster, ersatz in regeln:
            # Ergebnis zuerst prüfen: Sonst hängt ein zweiter Lauf denselben
            # Zusatz ein zweites Mal an eine Zeile, die ja bestehen bleibt.
            if ersatz in neu:
                continue
            if muster in neu:
                neu = neu.replace(muster, ersatz, 1)
            elif pflicht:
                lauf.fehler.append(f"{rel}: Pflichtstelle fehlt – {muster[:72]!r}")
        lauf.setze(rel, neu)


def index_ergaenzen(lauf: Lauf) -> None:
    """Archivfassungen unter docs/ in den Index aufnehmen. Der Prüfstand
    verlangt das, und ein fehlender Eintrag lässt ihn zu Recht fehlschlagen."""
    rel = f"{REPO_TEIL}/docs/00_INDEX.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    titel = f"## Ergänzte Archivnachweise {ALT} vor {NEU}"
    fehlend = [p for p in lauf.docs_archiv()
               if f"({p})" not in alt and f"<{p}>" not in alt]
    if not fehlend:
        lauf.hinweise.append("Dokumentationsindex: keine neuen Archivnachweise")
        return
    eintraege = "\n".join(f"- [{p}](<{p}>)" for p in fehlend)
    if titel in alt:
        neu = alt.rstrip("\n") + "\n" + eintraege + "\n"
    else:
        neu = alt.rstrip("\n") + "\n\n" + titel + "\n\n" + eintraege + "\n"
    lauf.setze(rel, neu)
    lauf.hinweise.append(f"Dokumentationsindex: {len(fehlend)} Archivnachweise ergänzt")


def changelog(lauf: Lauf, eintrag: Path) -> None:
    rel = f"{REPO_TEIL}/CHANGELOG.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    if f"## {NEU} " in alt:
        lauf.hinweise.append(f"CHANGELOG: {NEU} steht schon drin")
        return
    kopf = "# Änderungsverlauf\n"
    if not alt.startswith(kopf):
        lauf.fehler.append("CHANGELOG.md beginnt nicht mit der erwarteten Überschrift")
        return
    if not eintrag.is_file():
        lauf.fehler.append(f"Im Werkzeugordner fehlt {eintrag.name}")
        return
    text = eintrag.read_text(encoding="utf-8").strip() + "\n"
    lauf.setze(rel, kopf + "\n" + text + "\n" + alt[len(kopf):].lstrip("\n"))


# --------------------------------------------------------------- QA-Bericht
QA_ALTE_ZUSAGE = (
    "Der maßgebliche macOS-Lauf steht aus: `python3 tests/tools/pruefen.py --modus voll "
    "--protokoll tests/qa-3.21.2/abschluss`. Sein Ergebnis wird hier ergänzt."
)
QA_NEUE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf bestand auf macOS mit Python 3.14.5 am 14.09.2026 um "
    "15:04 mit **Exitcode 0**: [Abschlusslauf 3.21.2](../tests/qa-3.21.2/abschluss/ergebnis.json). "
    "Sechsunddreißig von achtunddreißig Schritten wurden ausgeführt, übersprungen blieben "
    "allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. "
    "Automatisiert ist 3.21.2 damit abgenommen."
)

QA_ANKER = "Für 3.21.2 sind alle fünfundzwanzig Suiten"

QA_NEUER_ABSATZ = f"""Für {NEU} sind alle fünfundzwanzig Suiten, die drei Analysen sowie Vorlagen-, Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb, `TZ=Europe/Berlin`) mit Exitcode 0 gelaufen; ausgenommen blieb dort allein der Dokumentationsindex, weil die Dokumente in der Arbeitskopie nicht mitliegen. {NEU} ändert keinen Anwendungscode außer der Versionsangabe. Neu ist die dritte Analyse `tests/tools/standpruefung.py`: Sie vergleicht jede aktive Standangabe der Ablage mit `VERSION` und verlangt, dass festgeschriebene Dokumente – Version oder Datum im Dateinamen, Versionsordner im Pfad oder „historisch“ im Titel – keinen aktuellen Stand behaupten. Anlass war ein Befund, den dieser Prüfstand bis 3.21.2 nicht finden konnte: **Sieben Dokumente standen zwei Versionssprünge lang auf 3.21.0** – Repository-README, Dokumentationsindex, Bestandsanalyse, Abschlussbericht, Feature-Abgleich, `10_Dokumentation/README.md` und das Produktdatenblatt. Die Dokumentprüfung bestand aus Indexeintrag und erreichbaren Linkzielen; ein Dokument kann beides erfüllen und dennoch inhaltlich überholt sein. Sechs historische Dokumente trugen zusätzlich ein von Hand gepflegtes Banner „Aktueller Entwicklungsstand“ – drei auf 3.14.0, drei auf 3.21.0. Sie verweisen jetzt ohne Nummer auf Index und QA-Bericht. Der Vollprüflauf wächst damit von achtunddreißig auf neununddreißig Schritte. Der maßgebliche macOS-Lauf steht aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-{NEU}/abschluss`. Sein Ergebnis wird hier ergänzt.

"""

# 3.19.0 und 3.20.0 haben keinen eigenen macOS-Lauf. Das stand nur in der
# Weitergabe; im Bericht las sich beides wie ein offener Rest.
QA_NACHTRAEGE = (
    ("Für 3.20 sind alle vierundzwanzig Suiten",
     "Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht noch aus: "
     "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.20.0/abschluss`. "
     "Sein Ergebnis wird hier ergänzt.",
     "Ein eigener macOS-Lauf zu 3.20.0 wurde nicht nachgeholt; der Stand ist im "
     "abgenommenen 3.21.1-Lauf enthalten, der denselben Code mit zwei behobenen "
     "Zeitzonenfehlern prüft."),
    ("Für 3.19 sind alle dreiundzwanzig Suiten",
     "Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht noch aus: "
     "`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss`. "
     "Sein Ergebnis wird hier ergänzt.",
     "Ein eigener macOS-Lauf zu 3.19.0 wurde nicht nachgeholt; der Stand ist im "
     "abgenommenen 3.21.1-Lauf enthalten."),
)


def qa_bericht(lauf: Lauf) -> None:
    rel = f"{REPO_TEIL}/docs/07_QA_BERICHT.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    if f"Für {NEU} sind alle" in alt:
        lauf.hinweise.append(f"QA-Bericht: Absatz {NEU} steht schon drin")
        return
    neu = alt
    if QA_ALTE_ZUSAGE not in neu:
        lauf.fehler.append("07_QA_BERICHT.md: die Zusage zum ausstehenden 3.21.2-Lauf steht "
                           "nicht im erwarteten Wortlaut")
        return
    neu = neu.replace(QA_ALTE_ZUSAGE, QA_NEUE_ZUSAGE, 1)
    if QA_ANKER not in neu:
        lauf.fehler.append(f"07_QA_BERICHT.md: Anker \"{QA_ANKER}\" fehlt")
        return
    neu = neu.replace(QA_ANKER, QA_NEUER_ABSATZ + QA_ANKER, 1)
    for _anker, muster, ersatz in QA_NACHTRAEGE:
        if ersatz in neu:
            continue
        if muster not in neu:
            lauf.fehler.append(f"07_QA_BERICHT.md: Nachtragsstelle fehlt – {muster[:60]!r}")
            continue
        neu = neu.replace(muster, ersatz, 1)
    neu = neu.replace(f"# QA-Bericht – Glide {ALT}", f"# QA-Bericht – Glide {NEU}", 1)
    neu = neu.replace("Stand 13.09.2026 · macOS · Python 3.14.5",
                      f"Stand {DATUM} · Glide {NEU} · macOS · Python 3.14.5", 1)
    lauf.setze(rel, neu)


def weitergabe(lauf: Lauf) -> None:
    rel = "00_Arbeitsvorbereitung/Glide_Weitergabe_neuer_Chat_2026-09-11.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    if f"Neu in {NEU}:" in alt:
        lauf.hinweise.append(f"Weitergabe: steht schon auf {NEU}")
        return
    neu = versionspass(alt)

    zeilen = neu.split("\n")
    titel = next((k for k, z in enumerate(zeilen) if z.startswith("# ")), None)
    if titel is None:
        lauf.fehler.append("Weitergabe: keine Titelzeile")
        return
    start = next((k for k in range(titel + 1, len(zeilen)) if zeilen[k].strip()), None)
    if start is None or not zeilen[start].startswith("Neu in "):
        lauf.fehler.append("Weitergabe: erste Absatzzeile beginnt nicht mit \"Neu in \"")
        return
    zeilen[start] = WEITERGABE_KOPF
    neu = "\n".join(zeilen)

    # Funktionsliste: ganzer Absatz.
    anfang = neu.find("Umgesetzt sind Erinnerungen mit Dock-")
    if anfang < 0:
        lauf.fehler.append("Weitergabe: Absatz \"Umgesetzt sind …\" fehlt")
        return
    ende = neu.find("\n\n", anfang)
    neu = neu[:anfang] + WEITERGABE_UMGESETZT + neu[ende:]

    # Prüfstandsabsatz: ganzer Absatz.
    anfang = neu.find("Prüfstand: 3.15.0 bis 3.18.0")
    if anfang < 0:
        lauf.fehler.append("Weitergabe: Prüfstandsabsatz fehlt")
        return
    ende = neu.find("\n\n", anfang)
    neu = neu[:anfang] + WEITERGABE_PRUEFSTAND + neu[ende:]

    # Datenregeln: neuer Abschnitt vor dem bisherigen obersten.
    anker = f"Datenregeln von {ALT}:"
    if anker not in neu:
        lauf.fehler.append(f"Weitergabe: Anker {anker!r} fehlt")
        return
    neu = neu.replace(anker, WEITERGABE_EINSCHUB + anker, 1)

    # Fallen: drei neue Punkte vor den bestehenden ersten.
    falle_anker = "- **Prüfläufe nie in UTC.**"
    if falle_anker not in neu:
        lauf.fehler.append("Weitergabe: Fallenliste fehlt")
        return
    neu = neu.replace(falle_anker, WEITERGABE_FALLE + falle_anker, 1)

    # Ablageweg: der Prüfschritt gehört in die Endkontrolle.
    alt_schritt = ("6. Endkontrolle: `pruefen.py --modus schnell`, ablageweite Linkprüfung, "
                   "Restsuche nach der Vorversion, Werkzeugordner nach `50_Ablage/Archiv`.")
    neu_schritt = ("6. Endkontrolle: `pruefen.py --modus schnell`, "
                   "`tests/tools/standpruefung.py`, ablageweite Linkprüfung, Restsuche nach "
                   "der Vorversion, Werkzeugordner nach `50_Ablage/Archiv`.")
    if neu_schritt not in neu:
        if alt_schritt not in neu:
            lauf.fehler.append("Weitergabe: Schritt 6 des Ablagewegs fehlt")
            return
        neu = neu.replace(alt_schritt, neu_schritt, 1)

    lauf.setze(rel, neu)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("quelle", type=Path, help="Werkzeugordner mit den Textbausteinen")
    parser.add_argument("--probe", action="store_true", help="nur zeigen, nichts schreiben")
    args = parser.parse_args()

    wurzel = ablage_wurzel()
    quelle = args.quelle.expanduser().resolve()
    if not quelle.is_dir():
        raise SystemExit(f"Werkzeugordner fehlt: {quelle}")

    lauf = Lauf(wurzel, args.probe)
    umbenennen(lauf)
    notizen_ersetzen(lauf, quelle)
    dokumente_fortschreiben(lauf)
    regeln_anwenden(lauf)
    qa_bericht(lauf)
    weitergabe(lauf)
    changelog(lauf, quelle / "changelog_3213.md")
    index_ergaenzen(lauf)      # zuletzt: braucht alle Archivfassungen

    # Erst jetzt wird die Platte angefasst - und im Probelauf gar nicht. Bis
    # dahin hat jeder Schritt auf demselben Puffer gerechnet, Probe wie Lauf.
    if lauf.fehler:
        print(f"\nFortschreibung {ALT} -> {NEU}: ABGEBROCHEN, nichts geschrieben")
        print(f"\nFEHLER ({len(lauf.fehler)}):")
        for fehler in lauf.fehler:
            print(f"  {fehler}")
        return 1
    verschoben, archiviert, geschrieben, zeilen = lauf.abschluss()

    print(f"\nFortschreibung {ALT} -> {NEU}" + ("   (PROBELAUF)" if args.probe else ""))
    for titel, werte in (("Umbenannt/verschoben", verschoben),
                         ("Archiviert", archiviert),
                         ("Geschrieben", geschrieben)):
        print(f"\n{titel} ({len(werte)}):")
        for wert in werte:
            print(f"  {wert}")
    if lauf.hinweise:
        print(f"\nHinweise ({len(lauf.hinweise)}):")
        for hinweis in lauf.hinweise:
            print(f"  {hinweis}")
    if zeilen:
        print(f"\nGeänderte Zeilen im Wortlaut ({len(zeilen)}):")
        for zeile in zeilen:
            print(zeile)
    print("\nAlle Pflichtstellen getroffen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
