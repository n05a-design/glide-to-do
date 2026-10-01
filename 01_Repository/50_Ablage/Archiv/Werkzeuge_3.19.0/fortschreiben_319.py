#!/usr/bin/env python3
"""Doku-Kette der Arbeitsablage von 3.18.0 auf 3.19.0 fortschreiben.

Läuft im Wurzelordner „Glide ToDo". Erst Archivkopien, dann gezielte
Ersetzungen – jede mit Zählprüfung, damit eine nicht mehr passende Erwartung
sichtbar abbricht statt stillschweigend nichts zu treffen.
"""
import shutil
import sys
from pathlib import Path

R = Path("01_Repository/Glide")
DOCS = R / "docs"
FEHLER = []


def bearbeite(pfad, paare):
    p = Path(pfad)
    text = p.read_text(encoding="utf-8")
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"{pfad}: {text.count(alt)} Treffer für {alt[:70]!r}")
            continue
        text = text.replace(alt, neu)
    p.write_text(text, encoding="utf-8")
    print("fortgeschrieben:", pfad)


def archiviere():
    namen = ["00_INDEX", "01_PRODUCT_CONSTRAINTS", "02_ARCHITECTURE", "03_STARTKONTEXT",
             "05_QA_TESTPLAN", "06_DATA_BACKUP_MIGRATION", "07_QA_BERICHT",
             "09_PROJECT_HANDOFF", "10_RELEASE_CHECKLIST", "11_BESTANDSANALYSE",
             "12_ABSCHLUSSBERICHT", "25_FEATURE_ABGLEICH_3.7.0", "27_VORLAGEN_PRAXISANLEITUNG"]
    (DOCS / "archiv").mkdir(exist_ok=True)
    (DOCS / "decisions" / "archiv").mkdir(parents=True, exist_ok=True)
    for name in namen:
        shutil.copy2(DOCS / f"{name}.md", DOCS / "archiv" / f"{name}_3.18.0_vor_3.19.0.md")
    shutil.copy2(DOCS / "decisions" / "PRODUCT_IDENTITY.md",
                 DOCS / "decisions" / "archiv" / "PRODUCT_IDENTITY_3.18.0_vor_3.19.0.md")
    shutil.copy2(R / "CHANGELOG.md", DOCS / "archiv" / "CHANGELOG_3.18.0_vor_3.19.0.md")
    shutil.copy2(R / "README.md", DOCS / "archiv" / "README_3.18.0_vor_3.19.0.md")
    shutil.copy2("README.md", DOCS / "archiv" / "README_root_3.18.0_vor_3.19.0.md")
    A = Path("00_Arbeitsvorbereitung")
    for quelle, ziel in (
        (A / "README.md", A / "Archiv" / "README_3.18.0_vor_3.19.0.md"),
        (A / "Glide_Funktionsvorschlaege_2026-09-11.md",
         A / "Archiv" / "Glide_Funktionsvorschlaege_2026-09-11_3.18.0_vor_3.19.0.md"),
        (A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md",
         A / "Archiv" / "Glide_Weitergabe_neuer_Chat_2026-09-11_3.18.0_vor_3.19.0.md"),
        (A / "Notizen" / "Technische_Fakten_3.18.0.md",
         A / "Notizen" / "Archiv" / "Technische_Fakten_3.18.0.md"),
        (A / "Checklisten" / "Manuelle_Pruefung_3.18.0.md",
         A / "Checklisten" / "Archiv" / "Manuelle_Pruefung_3.18.0.md"),
        (A / "Entscheidungen" / "Offene_Entscheidungen_3.18.0.md",
         A / "Entscheidungen" / "Archiv" / "Offene_Entscheidungen_3.18.0.md"),
        (Path("10_Dokumentation") / "Vorlagen_Praxisanleitung_3.18.0.md",
         Path("10_Dokumentation") / "Archiv" / "Vorlagen_Praxisanleitung_3.18.0.md"),
        (Path("40_Store_Material") / "Produktdatenblatt_3.18.0.md",
         Path("40_Store_Material") / "Archiv" / "Produktdatenblatt_3.18.0.md"),
    ):
        if Path(quelle).is_file():
            Path(ziel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(quelle, ziel)
    for d in ("05_Probelisten_Testdaten", "07_Python-Versionen", "10_Dokumentation", "40_Store_Material"):
        Path(d, "Archiv").mkdir(parents=True, exist_ok=True)
        shutil.copy2(Path(d, "README.md"), Path(d, "Archiv", "README_3.18.0_vor_3.19.0.md"))
    print("Vorfassungen archiviert")


def index():
    p = DOCS / "00_INDEX.md"
    text = p.read_text(encoding="utf-8")
    paare = [
        ("Aktueller Entwicklungsstand: 3.18.0 / Format 14. [CSV-Import mit Spaltenzuordnung](42_CSV_IMPORT_3.18.0.md).",
         "Aktueller Entwicklungsstand: 3.19.0 / Format 15. [Dauerhafter Änderungsverlauf](43_AENDERUNGSVERLAUF_3.19.0.md)."),
        ("Stand 13.09.2026 · Glide 3.18.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagenformat 2",
         "Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagenformat 2"),
        ("- [CSV-Import mit Spaltenzuordnung 3.18.0](42_CSV_IMPORT_3.18.0.md)\n- [QA-Bericht 3.18.0](07_QA_BERICHT.md)\n"
         "- [Daten, Backups und Migration 3.18.0](06_DATA_BACKUP_MIGRATION.md)\n"
         "- [Projektübergabe 3.18.0](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste 3.18.0](10_RELEASE_CHECKLIST.md)",
         "- [Dauerhafter Änderungsverlauf 3.19.0](43_AENDERUNGSVERLAUF_3.19.0.md)\n- [QA-Bericht 3.19.0](07_QA_BERICHT.md)\n"
         "- [Daten, Backups und Migration 3.19.0](06_DATA_BACKUP_MIGRATION.md)\n"
         "- [Projektübergabe 3.19.0](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste 3.19.0](10_RELEASE_CHECKLIST.md)\n"
         "- [CSV-Import mit Spaltenzuordnung 3.18.0](42_CSV_IMPORT_3.18.0.md)"),
        ("3.18-Dokumenten oben und in der Funktionsübersicht.", "3.19-Dokumenten oben und in der Funktionsübersicht."),
        ("- [42_CSV_IMPORT_3.18.0.md](<42_CSV_IMPORT_3.18.0.md>)",
         "- [42_CSV_IMPORT_3.18.0.md](<42_CSV_IMPORT_3.18.0.md>)\n- [43_AENDERUNGSVERLAUF_3.19.0.md](<43_AENDERUNGSVERLAUF_3.19.0.md>)"),
        ("- [07_QA_BERICHT_3.18.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.18.0_vor_Pruefnachtrag.md)",
         "- [07_QA_BERICHT_3.18.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.18.0_vor_Pruefnachtrag.md)\n"
         "- [07_QA_BERICHT_3.19.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.19.0_vor_Pruefnachtrag.md)"),
    ]
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"00_INDEX.md: {text.count(alt)} Treffer für {alt[:70]!r}")
            continue
        text = text.replace(alt, neu)
    namen = ["00_INDEX", "01_PRODUCT_CONSTRAINTS", "02_ARCHITECTURE", "03_STARTKONTEXT",
             "05_QA_TESTPLAN", "06_DATA_BACKUP_MIGRATION", "07_QA_BERICHT", "09_PROJECT_HANDOFF",
             "10_RELEASE_CHECKLIST", "11_BESTANDSANALYSE", "12_ABSCHLUSSBERICHT",
             "25_FEATURE_ABGLEICH_3.7.0", "27_VORLAGEN_PRAXISANLEITUNG"]
    zeilen = ["", "## Ergänzte Archivnachweise 3.18 vor 3.19", ""]
    zeilen += [f"- [{name}_3.18.0_vor_3.19.0](archiv/{name}_3.18.0_vor_3.19.0.md)" for name in namen]
    zeilen += [
        "- [CHANGELOG_3.18.0_vor_3.19.0](archiv/CHANGELOG_3.18.0_vor_3.19.0.md)",
        "- [README_3.18.0_vor_3.19.0](archiv/README_3.18.0_vor_3.19.0.md)",
        "- [README_root_3.18.0_vor_3.19.0](archiv/README_root_3.18.0_vor_3.19.0.md)",
        "- [PRODUCT_IDENTITY_3.18.0_vor_3.19.0](decisions/archiv/PRODUCT_IDENTITY_3.18.0_vor_3.19.0.md)",
    ]
    text = text.rstrip("\n") + "\n" + "\n".join(zeilen) + "\n"
    p.write_text(text, encoding="utf-8")
    print("fortgeschrieben: 00_INDEX.md")


def bestandsdokumente():
    bearbeite(DOCS / "01_PRODUCT_CONSTRAINTS.md", [
        ("# Produktgrenzen – Glide 3.18.0", "# Produktgrenzen – Glide 3.19.0"),
        ("3.18 ergänzt den CSV-Import mit Spaltenzuordnung:",
         "3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15. "
         "Protokolliert wird der Aufgabenbestand – nicht Einstellungen, Vorlagen, Reiter, "
         "Pinnwände oder gespeicherte Filter. Kein Wiederherstellen alter Werte aus dem "
         "Protokoll, keine alten Feldinhalte, keine Verlaufsansicht am einzelnen Punkt, kein "
         "Benutzer- oder Gerätebezug, keine Synchronisierung; Obergrenze 4000 Einträge, "
         "abschaltbar. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "3.18 ergänzt den CSV-Import mit Spaltenzuordnung:"),
    ])
    bearbeite(DOCS / "02_ARCHITECTURE.md", [
        ("# Architektur – Glide 3.18.0", "# Architektur – Glide 3.19.0"),
        ("3.18 ergänzt `read_csv_table`",
         "3.19 ergänzt `history_snapshot`, `history_events`, `group_history_events`, "
         "`record_history_events`, `update_history`, `reset_history_baseline`, "
         "`normalize_history_entries`, `filtered_history`, `clear_history`, "
         "`history_entry_line`, `show_history_dialog` und `ensure_schema15_backup`. Der "
         "Verlauf entsteht in `update_history` innerhalb von `save_items` aus dem Vergleich "
         "zweier Vergleichsstände – eine Stelle für alle Änderungswege. `normalize_lists_data` "
         "legt den gelesenen Verlauf in `_loaded_history` ab, damit ein fremdes Archiv den "
         "laufenden Bestand nicht überschreibt. Neues Datenfeld `history` im Aufgabenformat 15, "
         "keine neue Laufzeitabhängigkeit. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "3.18 ergänzt `read_csv_table`"),
    ])
    bearbeite(DOCS / "03_STARTKONTEXT.md", [
        ("# Startkontext – Glide 3.18.0", "# Startkontext – Glide 3.19.0"),
        ("Glide-Aufgaben-und-Listen_v3.18.0.pyw", "Glide-Aufgaben-und-Listen_v3.19.0.pyw"),
        ("und der CSV-Import mit Spaltenzuordnung in 3.18. Spätere Ideen sind ein dauerhafter Änderungsverlauf und benutzerdefinierte Felder.",
         "der CSV-Import mit Spaltenzuordnung in 3.18 und der dauerhafte Änderungsverlauf in 3.19. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten."),
        ("3.18 ergänzt den CSV-Import mit Spaltenzuordnung; er legt ausschließlich neue Punkte an, "
         "überschreibt nichts und ist mit Rückgängig vollständig zurücknehmbar. "
         "[Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).",
         "3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15; der "
         "Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "3.18 ergänzt den CSV-Import mit Spaltenzuordnung; er legt ausschließlich neue Punkte an, "
         "überschreibt nichts und ist mit Rückgängig vollständig zurücknehmbar. "
         "[Bedienung 3.18](42_CSV_IMPORT_3.18.0.md)."),
    ])
    bearbeite(DOCS / "05_QA_TESTPLAN.md", [
        ("# Prüfplan – Glide 3.18.0", "# Prüfplan – Glide 3.19.0"),
        ("Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.18.0/abschluss`. Zweiundzwanzig Suiten,",
         "Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss`. Dreiundzwanzig Suiten,"),
        ("`test_features318.py` prüft den Rundlauf",
         "`test_features319.py` prüft die Migration von Format 14 samt unveränderter "
         "Originalkopie, jeden erfassten Vorgang einzeln, die Feldliste bei Änderungen, "
         "Erledigen und Wiederöffnen, Verschieben zwischen Elternpunkt, Liste und Ordner, die "
         "drei Papierkorbvorgänge, Sammeleinträge an der Schwelle, die Obergrenze von 4000 "
         "Einträgen, den Rundlauf über Komplett- und Teilbackup, defekte und fremde "
         "Verlaufsfelder, die abschaltbare Erfassung, das Leeren, Suche und Filter sowie den "
         "Dialog in beiden Themes bei 780×640. Die Fixtureprüfung kennt die Formatstufen "
         "(14 für 3.14.0 bis 3.18.0, darüber 15); neu ist "
         "`tests/fixtures/current_v15/reference_v15.json`. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "`test_features318.py` prüft den Rundlauf"),
    ])
    bearbeite(DOCS / "06_DATA_BACKUP_MIGRATION.md", [
        ("# Daten, Backups und Migration – Glide 3.18.0", "# Daten, Backups und Migration – Glide 3.19.0"),
        ("3.18 ergänzt den CSV-Import.",
         "3.19 hebt das Aufgabenformat auf **15** und ergänzt das Feld `history` neben den "
         "Aufgabenfeldern. Ein Bestand im Format 14 oder älter wird beim ersten Speichern "
         "gehoben und erhält ein leeres Protokoll; vorher entsteht die unveränderte Kopie "
         "`liste_vor_format15_<Zeitstempel>.json` im Backup-Ordner. Ein defektes oder fremdes "
         "`history`-Feld wird beim Laden verworfen, ohne die Aufgaben zu berühren. "
         "Komplettbackup und App-Backup führen den Verlauf mit, ein Teilbackup als Auszug "
         "nicht; portable Backups werden weiterhin ab Format 4 gelesen, ein Format-15-Backup "
         "ist für ältere Fassungen erwartungsgemäß nicht lesbar. Rückgängig stellt den Bestand "
         "wieder her und lässt das Protokoll stehen. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n3.18 ergänzt den CSV-Import."),
    ])
    bearbeite(DOCS / "09_PROJECT_HANDOFF.md", [
        ("# Projektübergabe – Glide 3.18.0", "# Projektübergabe – Glide 3.19.0"),
        ("Glide-Aufgaben-und-Listen_v3.18.0.pyw", "Glide-Aufgaben-und-Listen_v3.19.0.pyw"),
        ("3.18 ist das zuletzt umgesetzte Funktionspaket: der CSV-Import mit Spaltenzuordnung.",
         "3.19 ist das zuletzt umgesetzte Funktionspaket: der dauerhafte Änderungsverlauf mit "
         "Aufgabenformat 15. Bei Änderungen besonders prüfen: dass `update_history` in jedem "
         "Speicherweg läuft und den Vergleichsstand nachführt (auch bei abgeschalteter "
         "Protokollierung), dass `normalize_lists_data` den gelesenen Verlauf nur in "
         "`_loaded_history` ablegt – sonst überschreibt ein fremdes Archiv das laufende "
         "Protokoll –, dass gelöschte Container ihre Punkte nicht einzeln melden, dass "
         "Sammeleinträge und Obergrenze greifen und dass ein defektes `history`-Feld verworfen "
         "wird, ohne die Aufgaben zu berühren. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "3.18 brachte den CSV-Import mit Spaltenzuordnung."),
    ])
    bearbeite(DOCS / "10_RELEASE_CHECKLIST.md", [
        ("# Release-Checkliste – Glide 3.18.0", "# Release-Checkliste – Glide 3.19.0"),
        ("- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.18.0 abstimmen.",
         "- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.19.0 abstimmen.\n"
         "- Formatsprung beachten: Aufgabenformat 15, Referenz-Fixture `current_v15`, "
         "Formatstufen in der Fixtureprüfung."),
        ("Für 3.18 zusätzlich den CSV-Import abnehmen:",
         "Für 3.19 zusätzlich den Änderungsverlauf abnehmen: vor der ersten Nutzung eine "
         "Sicherung anlegen und nach dem ersten Speichern die Datei "
         "`liste_vor_format15_*.json` im Backup-Ordner prüfen, einen Arbeitstag protokollieren "
         "lassen und die Einträge gegen das tatsächliche Vorgehen halten, Massenvorgänge auf "
         "Sammeleinträge prüfen, Filter und TXT-Ausgabe durchgehen, Protokollierung ab- und "
         "wieder einschalten, Verlauf leeren und den Bestand danach kontrollieren. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).\n\n"
         "Für 3.18 zusätzlich den CSV-Import abnehmen:"),
    ])
    for name in ("11_BESTANDSANALYSE.md", "12_ABSCHLUSSBERICHT.md", "25_FEATURE_ABGLEICH_3.7.0.md"):
        bearbeite(DOCS / name, [
            ("Aktueller Entwicklungsstand: **3.18.0 / Aufgabenformat 14** mit CSV-Import mit Spaltenzuordnung. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md), [QA](07_QA_BERICHT.md).",
             "Aktueller Entwicklungsstand: **3.19.0 / Aufgabenformat 15** mit dauerhaftem Änderungsverlauf. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md), [QA](07_QA_BERICHT.md)."),
        ])
    bearbeite(DOCS / "11_BESTANDSANALYSE.md", [("Glide 3.18.0; maßgeblich sind", "Glide 3.19.0; maßgeblich sind")])
    bearbeite(DOCS / "12_ABSCHLUSSBERICHT.md", [
        ("Arbeitsstand ist Glide 3.18.0;", "Arbeitsstand ist Glide 3.19.0;"),
        ("[CSV-Import mit Spaltenzuordnung](42_CSV_IMPORT_3.18.0.md).",
         "[Dauerhafter Änderungsverlauf](43_AENDERUNGSVERLAUF_3.19.0.md)."),
        ("- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.18.0.pyw)",
         "- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw)"),
    ])
    bearbeite(DOCS / "27_VORLAGEN_PRAXISANLEITUNG.md", [
        ("Stand 13.09.2026 · Glide 3.18.0 · Aufgabenformat 14 · Vorlagenformat 2",
         "Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(DOCS / "decisions" / "PRODUCT_IDENTITY.md", [
        ("Stand 13.09.2026 · App-Version 3.18.0 · Datenformat 14",
         "Stand 13.09.2026 · App-Version 3.19.0 · Datenformat 15"),
    ])
    bearbeite(DOCS / "07_QA_BERICHT.md", [
        ("# QA-Bericht – Glide 3.18.0", "# QA-Bericht – Glide 3.19.0"),
        ("Für 3.18 bestand der Gesamtlauf",
         "Für 3.19 sind alle dreiundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, "
         "Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter "
         "Xvfb) mit Exitcode 0 gelaufen. Die neue "
         "[Verlaufssuite](../tests/integration/test_features319.py) prüft Migration samt "
         "Originalkopie, alle erfassten Vorgänge, Feldlisten, Verschieben, die drei "
         "Papierkorbvorgänge, Sammeleinträge, Obergrenze, Backup-Rundlauf, defekte "
         "Verlaufsfelder, abschaltbare Erfassung, Leeren, Filter und den Dialog in beiden "
         "Themes. Angepasst wurden die Formaterwartungen in sechs Bestandssuiten, die "
         "Formatstufen der Fixtureprüfung und der Bestandsvergleich in `test_features318.py`, "
         "der das Protokoll ausnimmt – Rückgängig stellt den Bestand her, nicht den Verlauf. "
         "Zwei Befunde der Bestandssuiten sind behoben: ein Namensschatten im "
         "Einstellungsdialog und das Überschreiben des laufenden Protokolls beim Lesen eines "
         "fremden Archivs. Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht "
         "noch aus: `python3 tests/tools/pruefen.py --modus voll --protokoll "
         "tests/qa-3.19.0/abschluss`. Sein Ergebnis wird hier ergänzt.\n\n"
         "Für 3.18 bestand der Gesamtlauf"),
    ])


def changelog(eintrag_pfad):
    p = R / "CHANGELOG.md"
    text = p.read_text(encoding="utf-8")
    eintrag = Path(eintrag_pfad).read_text(encoding="utf-8").strip() + "\n\n"
    anker = "## 3.18.0 – 13.09.2026"
    if text.count(anker) != 1:
        FEHLER.append(f"CHANGELOG.md: {text.count(anker)} Treffer für den 3.18-Anker")
        return
    p.write_text(text.replace(anker, eintrag + anker, 1), encoding="utf-8")
    print("CHANGELOG: 3.19.0 eingetragen")


def readmes():
    NEU = ("Neu in 3.19: dauerhafter Änderungsverlauf. Anlegen, Ändern, Erledigen, Verschieben, "
           "Umbenennen, Papierkorb, Wiederherstellen und endgültiges Entfernen bleiben mit "
           "Zeitpunkt, Objekt, Liste und geänderten Feldern nachlesbar – über Programmstarts "
           "hinweg.")
    bearbeite(R / "README.md", [
        ("Aktueller interner Entwicklungsstand: **3.18.0** · 13.09.2026",
         "Aktueller interner Entwicklungsstand: **3.19.0** · 13.09.2026"),
        ("07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.18.0.pyw",
         "07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw"),
        ("--protokoll tests/qa-3.18.0/abschluss`", "--protokoll tests/qa-3.19.0/abschluss`"),
        ("[Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](docs/40_APP_BACKUP_3.16.0.md) · [Bedienung 3.15](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) · [Bedienung 3.14](docs/37_PLANUNG_UND_AUFWAND_3.14.0.md)",
         "[Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](docs/40_APP_BACKUP_3.16.0.md) · [Bedienung 3.15](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md)"),
    ])
    bearbeite("README.md", [
        ("Neu in 3.18: CSV-Import mit Spaltenzuordnung. Glide erkennt Trennzeichen und Kodierung, "
         "ordnet jede Spalte einem Feld zu und zeigt vor der Übernahme eine Vorschau; eine mit "
         "„Als CSV“ geschriebene Liste ist vollständig zurücklesbar. "
         "[Bedienung und Datenregeln](01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).",
         NEU + " [Bedienung und Datenregeln](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)."),
        ("Aktueller Entwicklungsstand: **3.18.0 vom 13.09.2026**: CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe,",
         "Aktueller Entwicklungsstand: **3.19.0 vom 13.09.2026**: dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung, Druck- und PDF-Ausgabe,"),
        ("[CSV-Import mit Spaltenzuordnung 3.18](01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·",
         "[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·\n"
         "[CSV-Import mit Spaltenzuordnung 3.18](01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·"),
    ])
    A = Path("00_Arbeitsvorbereitung")
    bearbeite(A / "README.md", [
        ("Stand 13.09.2026. [Aktueller Ausbau: CSV-Import mit Spaltenzuordnung 3.18.0](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).",
         "Stand 13.09.2026. [Aktueller Ausbau: Dauerhafter Änderungsverlauf 3.19.0](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)."),
        ("- [Manuelle Prüfung des 3.18-Stands](Checklisten/Manuelle_Pruefung_3.18.0.md)",
         "- [Manuelle Prüfung des 3.19-Stands](Checklisten/Manuelle_Pruefung_3.19.0.md)"),
        ("- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_3.18.0.md)",
         "- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_3.19.0.md)"),
        ("- [Bedienvertrag 3.18.0: CSV-Import mit Spaltenzuordnung, umgesetzt](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md)",
         "- [Bedienvertrag 3.19.0: Dauerhafter Änderungsverlauf, umgesetzt](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)\n"
         "- [Bedienvertrag 3.18.0: CSV-Import mit Spaltenzuordnung, umgesetzt](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md)"),
        ("- [Technische Fakten 3.18](Notizen/Technische_Fakten_3.18.0.md)",
         "- [Technische Fakten 3.19](Notizen/Technische_Fakten_3.19.0.md)"),
        ("[CSV-Import mit Spaltenzuordnung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·",
         "[Dauerhafter Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·\n"
         "[CSV-Import mit Spaltenzuordnung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·"),
    ])
    bearbeite(Path("10_Dokumentation") / "README.md", [
        ("Stand 13.09.2026 · Glide 3.18.0", "Stand 13.09.2026 · Glide 3.19.0"),
        ("- [CSV importieren](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md)",
         "- [Änderungsverlauf](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)\n"
         "- [CSV importieren](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md)"),
        ("- [Bedienung der Praxisvorlagen 3.18](Vorlagen_Praxisanleitung_3.18.0.md)",
         "- [Bedienung der Praxisvorlagen 3.19](Vorlagen_Praxisanleitung_3.19.0.md)"),
        ("[CSV importieren 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·",
         "[Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·\n"
         "[CSV importieren 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·"),
    ])
    bearbeite(Path("40_Store_Material") / "README.md", [
        ("[Produktdatenblatt 3.18.0](Produktdatenblatt_3.18.0.md) enthält den aktuellen Entwicklungsnachtrag.",
         "[Produktdatenblatt 3.19.0](Produktdatenblatt_3.19.0.md) enthält den aktuellen Entwicklungsnachtrag."),
    ])
    bearbeite(Path("05_Probelisten_Testdaten") / "README.md", [
        ("Stand 13.09.2026 · Glide 3.18.0 · Aufgabenformat 14 · Vorlagenformat 2",
         "Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(Path("07_Python-Versionen") / "README.md", [
        ("Glide 3.18.0 · Entwicklungsstand 13.09.2026 · Aufgabenformat 14 · Vorlagenformat 2",
         "Glide 3.19.0 · Entwicklungsstand 13.09.2026 · Aufgabenformat 15 · Vorlagenformat 2"),
        ("[Glide-Aufgaben-und-Listen_v3.18.0.pyw](Glide-Aufgaben-und-Listen_v3.18.0.pyw) ist die aktuelle Arbeitskopie",
         "[Glide-Aufgaben-und-Listen_v3.19.0.pyw](Glide-Aufgaben-und-Listen_v3.19.0.pyw) ist die aktuelle Arbeitskopie"),
        ("[Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)",
         "[Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)"),
    ])


def weitergabe():
    A = Path("00_Arbeitsvorbereitung")
    bearbeite(A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md", [
        ("Neu in 3.18: CSV-Import mit Spaltenzuordnung. Trennzeichen und Kodierung werden erkannt und "
         "sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine Vorschau zeigt das "
         "Ergebnis vor der Übernahme; eine mit „Als CSV“ geschriebene Liste ist vollständig "
         "zurücklesbar. [Bedienung und Datenregeln](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md).",
         "Neu in 3.19: dauerhafter Änderungsverlauf mit Aufgabenformat 15. Anlegen, Ändern, "
         "Erledigen, Verschieben, Umbenennen, Papierkorb, Wiederherstellen und endgültiges "
         "Entfernen bleiben mit Zeitpunkt, Objekt, Liste und geänderten Feldern nachlesbar; der "
         "Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. "
         "[Bedienung und Datenregeln](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)."),
        ("Stand 13.09.2026 · Entwicklungsstand 3.18.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2",
         "Stand 13.09.2026 · Entwicklungsstand 3.19.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"),
        ("die Druck- und PDF-Ausgabe sowie der CSV-Import mit Spaltenzuordnung.",
         "die Druck- und PDF-Ausgabe, der CSV-Import mit Spaltenzuordnung sowie der dauerhafte Änderungsverlauf."),
        ("`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.18.0.pyw`",
         "`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw`"),
        ("3.18.0 ist ebenfalls abgenommen (zweiundzwanzig Suiten, macOS/Python 3.14.5, Exitcode 0, `tests/qa-3.18.0/abschluss/ergebnis.json`).",
         "3.18.0 ist ebenfalls abgenommen (zweiundzwanzig Suiten, macOS/Python 3.14.5, Exitcode 0, "
         "`tests/qa-3.18.0/abschluss/ergebnis.json`). Für 3.19.0 sind alle dreiundzwanzig Suiten "
         "in einer Linux-Vorabumgebung mit Exitcode 0 gelaufen; der maßgebliche macOS-Lauf steht "
         "noch aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss`."),
        ("[Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md) · [Bedienung 3.15](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) ·",
         "[Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md) ·"),
        ("Datenregeln von 3.18:",
         "Datenregeln von 3.19: `history` liegt neben den Aufgabenfeldern; Format 14 wird beim "
         "ersten Speichern auf 15 gehoben, vorher entsteht `liste_vor_format15_*`. Der Verlauf "
         "entsteht in `update_history` beim Speichern aus dem Vergleich zweier Stände; "
         "`normalize_lists_data` legt einen gelesenen Verlauf nur in `_loaded_history` ab, damit "
         "ein fremdes Archiv das laufende Protokoll nicht überschreibt. Obergrenze 4000 Einträge, "
         "Sammeleinträge ab 25 gleichartigen Ereignissen, abschaltbar über `history_enabled`. "
         "Rückgängig nimmt den Bestand zurück, nicht das Protokoll.\n\nDatenregeln von 3.18:"),
        ("Nächste offene Ideen: dauerhafter Änderungsverlauf (der erste Punkt, der wieder ein neues "
         "Datenformat braucht) und benutzerdefinierte Felder.",
         "Nächste offene Ideen: benutzerdefinierte Felder und darauf aufbauende eigene Ansichten."),
    ])
    bearbeite(A / "Glide_Funktionsvorschlaege_2026-09-11.md", [
        ("13. CSV-Import mit Spaltenzuordnung – **umgesetzt in 3.18.0**;",
         "14. Dauerhafter Änderungsverlauf – **umgesetzt in 3.19.0** mit Aufgabenformat 15; "
         "Migration, alle erfassten Vorgänge, Sammeleinträge, Obergrenze, Backups, defekte "
         "Verlaufsfelder, Abschaltung, Leeren, Filter und Dialog sind automatisiert geprüft. "
         "[Bedienvertrag](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md). Nächste "
         "offene Ausbaustufen: benutzerdefinierte Felder und eigene Ansichten je Feld.\n"
         "13. CSV-Import mit Spaltenzuordnung – **umgesetzt in 3.18.0**;"),
    ])


def abgeleitet(quelle):
    A = Path("00_Arbeitsvorbereitung")
    for name, ziel in (("Technische_Fakten_3.19.0.md", A / "Notizen"),
                       ("Manuelle_Pruefung_3.19.0.md", A / "Checklisten"),
                       ("Offene_Entscheidungen_3.19.0.md", A / "Entscheidungen")):
        shutil.copy2(Path(quelle) / name, ziel / name)
        print("abgelegt:", ziel / name)
    # Vorlagenanleitung und Produktdatenblatt aus der Vorfassung ableiten.
    vorlage = Path("10_Dokumentation/Archiv/Vorlagen_Praxisanleitung_3.18.0.md")
    text = vorlage.read_text(encoding="utf-8").replace(
        "Stand 13.09.2026 · Glide 3.18.0 · Aufgabenformat 14 · Vorlagenformat 2",
        "Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2")
    Path("10_Dokumentation/Vorlagen_Praxisanleitung_3.19.0.md").write_text(text, encoding="utf-8")
    blatt = Path("40_Store_Material/Archiv/Produktdatenblatt_3.18.0.md")
    text = blatt.read_text(encoding="utf-8")
    ersetzungen = [
        ("# Glide Produktdatenblatt 3.18.0", "# Glide Produktdatenblatt 3.19.0"),
        ("Aufgabenformat 14", "Aufgabenformat 15"),
        ("Der 3.18-Stand ist lokal geprüft: 22 Testsuiten", "Der 3.19-Stand ist lokal geprüft: 23 Testsuiten"),
        ("[Aktuelle Bedienung](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·",
         "[Aktuelle Bedienung](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·"),
    ]
    for alt, neu in ersetzungen:
        if text.count(alt) != 1:
            FEHLER.append(f"Produktdatenblatt: {text.count(alt)} Treffer für {alt[:60]!r}")
            continue
        text = text.replace(alt, neu)
    anker = "| Austausch |"
    if anker in text:
        zeile_alt = [z for z in text.splitlines() if z.startswith(anker)][0]
        zeile_neu = zeile_alt.replace("portable Backups", "dauerhafter Änderungsverlauf, portable Backups")
        text = text.replace(zeile_alt, zeile_neu)
    Path("40_Store_Material/Produktdatenblatt_3.19.0.md").write_text(text, encoding="utf-8")
    print("abgeleitet: Vorlagenanleitung und Produktdatenblatt 3.19.0")


if __name__ == "__main__":
    quelle = sys.argv[1] if len(sys.argv) > 1 else "/tmp/glide319_docs"
    archiviere()
    index()
    bestandsdokumente()
    changelog(Path(quelle) / "changelog_319.md")
    readmes()
    weitergabe()
    abgeleitet(Path(quelle) / "abgeleitet")
    print()
    if FEHLER:
        print("NICHT ANGEWENDET – bitte prüfen:")
        for zeile in FEHLER:
            print(" -", zeile)
        sys.exit(1)
    print("Doku-Kette vollständig auf 3.19.0 fortgeschrieben")
