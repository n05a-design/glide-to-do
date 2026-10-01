#!/usr/bin/env python3
"""Doku-Kette der Arbeitsablage von 3.19.0 auf 3.20.0 fortschreiben.

Läuft im Wurzelordner „Glide ToDo". Erst Archivkopien, dann gezielte
Ersetzungen – jede mit Zählprüfung, damit eine nicht mehr passende Erwartung
sichtbar abbricht statt stillschweigend nichts zu treffen. Das Aufgabenformat
bleibt 15; 3.20 ist reine Ausgabe.
"""
import shutil
import sys
from pathlib import Path

R = Path("01_Repository/Glide")
DOCS = R / "docs"
A = Path("00_Arbeitsvorbereitung")
FEHLER = []
NAMEN = ["00_INDEX", "01_PRODUCT_CONSTRAINTS", "02_ARCHITECTURE", "03_STARTKONTEXT",
         "05_QA_TESTPLAN", "06_DATA_BACKUP_MIGRATION", "07_QA_BERICHT", "09_PROJECT_HANDOFF",
         "10_RELEASE_CHECKLIST", "11_BESTANDSANALYSE", "12_ABSCHLUSSBERICHT",
         "25_FEATURE_ABGLEICH_3.7.0", "27_VORLAGEN_PRAXISANLEITUNG"]
NEU_SATZ = ("Neu in 3.20: Kalenderausgabe als ICS. Fälligkeiten werden als Kalenderdatei "
            "geschrieben, die Apple Kalender, Outlook, Thunderbird und Google Kalender einlesen – "
            "mit Ganztags- und Uhrzeitterminen, Wiederholungen als RRULE und Erinnerungen als "
            "Alarm, ohne Konto und ohne Synchronisierung.")


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
    for name in NAMEN:
        shutil.copy2(DOCS / f"{name}.md", DOCS / "archiv" / f"{name}_3.19.0_vor_3.20.0.md")
    shutil.copy2(DOCS / "decisions" / "PRODUCT_IDENTITY.md",
                 DOCS / "decisions" / "archiv" / "PRODUCT_IDENTITY_3.19.0_vor_3.20.0.md")
    shutil.copy2(R / "CHANGELOG.md", DOCS / "archiv" / "CHANGELOG_3.19.0_vor_3.20.0.md")
    shutil.copy2(R / "README.md", DOCS / "archiv" / "README_3.19.0_vor_3.20.0.md")
    shutil.copy2("README.md", DOCS / "archiv" / "README_root_3.19.0_vor_3.20.0.md")
    for quelle, ziel in (
        (A / "README.md", A / "Archiv" / "README_3.19.0_vor_3.20.0.md"),
        (A / "Glide_Funktionsvorschlaege_2026-09-11.md",
         A / "Archiv" / "Glide_Funktionsvorschlaege_2026-09-11_3.19.0_vor_3.20.0.md"),
        (A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md",
         A / "Archiv" / "Glide_Weitergabe_neuer_Chat_2026-09-11_3.19.0_vor_3.20.0.md"),
        (A / "Notizen" / "Technische_Fakten_3.19.0.md",
         A / "Notizen" / "Archiv" / "Technische_Fakten_3.19.0.md"),
        (A / "Checklisten" / "Manuelle_Pruefung_3.19.0.md",
         A / "Checklisten" / "Archiv" / "Manuelle_Pruefung_3.19.0.md"),
        (A / "Entscheidungen" / "Offene_Entscheidungen_3.19.0.md",
         A / "Entscheidungen" / "Archiv" / "Offene_Entscheidungen_3.19.0.md"),
        (Path("10_Dokumentation/Vorlagen_Praxisanleitung_3.19.0.md"),
         Path("10_Dokumentation/Archiv/Vorlagen_Praxisanleitung_3.19.0.md")),
        (Path("40_Store_Material/Produktdatenblatt_3.19.0.md"),
         Path("40_Store_Material/Archiv/Produktdatenblatt_3.19.0.md")),
    ):
        if Path(quelle).is_file():
            Path(ziel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(quelle, ziel)
    for d in ("05_Probelisten_Testdaten", "07_Python-Versionen", "10_Dokumentation", "40_Store_Material"):
        shutil.copy2(Path(d, "README.md"), Path(d, "Archiv", "README_3.19.0_vor_3.20.0.md"))
    print("Vorfassungen archiviert")


def index():
    p = DOCS / "00_INDEX.md"
    text = p.read_text(encoding="utf-8")
    paare = [
        ("Aktueller Entwicklungsstand: 3.19.0 / Format 15. [Dauerhafter Änderungsverlauf](43_AENDERUNGSVERLAUF_3.19.0.md).",
         "Aktueller Entwicklungsstand: 3.20.0 / Format 15. [Kalenderausgabe als ICS](44_KALENDERAUSGABE_3.20.0.md)."),
        ("Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagenformat 2",
         "Stand 14.09.2026 · Glide 3.20.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagenformat 2"),
        ("- [Dauerhafter Änderungsverlauf 3.19.0](43_AENDERUNGSVERLAUF_3.19.0.md)\n- [QA-Bericht 3.19.0](07_QA_BERICHT.md)\n"
         "- [Daten, Backups und Migration 3.19.0](06_DATA_BACKUP_MIGRATION.md)\n"
         "- [Projektübergabe 3.19.0](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste 3.19.0](10_RELEASE_CHECKLIST.md)",
         "- [Kalenderausgabe als ICS 3.20.0](44_KALENDERAUSGABE_3.20.0.md)\n- [QA-Bericht 3.20.0](07_QA_BERICHT.md)\n"
         "- [Daten, Backups und Migration 3.20.0](06_DATA_BACKUP_MIGRATION.md)\n"
         "- [Projektübergabe 3.20.0](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste 3.20.0](10_RELEASE_CHECKLIST.md)\n"
         "- [Dauerhafter Änderungsverlauf 3.19.0](43_AENDERUNGSVERLAUF_3.19.0.md)"),
        ("3.19-Dokumenten oben und in der Funktionsübersicht.", "3.20-Dokumenten oben und in der Funktionsübersicht."),
        ("- [43_AENDERUNGSVERLAUF_3.19.0.md](<43_AENDERUNGSVERLAUF_3.19.0.md>)",
         "- [43_AENDERUNGSVERLAUF_3.19.0.md](<43_AENDERUNGSVERLAUF_3.19.0.md>)\n"
         "- [44_KALENDERAUSGABE_3.20.0.md](<44_KALENDERAUSGABE_3.20.0.md>)"),
        ("- [07_QA_BERICHT_3.19.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.19.0_vor_Pruefnachtrag.md)",
         "- [07_QA_BERICHT_3.19.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.19.0_vor_Pruefnachtrag.md)\n"
         "- [07_QA_BERICHT_3.20.0_vor_Pruefnachtrag](archiv/07_QA_BERICHT_3.20.0_vor_Pruefnachtrag.md)"),
    ]
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"00_INDEX.md: {text.count(alt)} Treffer für {alt[:70]!r}")
            continue
        text = text.replace(alt, neu)
    zeilen = ["", "## Ergänzte Archivnachweise 3.19 vor 3.20", ""]
    zeilen += [f"- [{name}_3.19.0_vor_3.20.0](archiv/{name}_3.19.0_vor_3.20.0.md)" for name in NAMEN]
    zeilen += [
        "- [CHANGELOG_3.19.0_vor_3.20.0](archiv/CHANGELOG_3.19.0_vor_3.20.0.md)",
        "- [README_3.19.0_vor_3.20.0](archiv/README_3.19.0_vor_3.20.0.md)",
        "- [README_root_3.19.0_vor_3.20.0](archiv/README_root_3.19.0_vor_3.20.0.md)",
        "- [PRODUCT_IDENTITY_3.19.0_vor_3.20.0](decisions/archiv/PRODUCT_IDENTITY_3.19.0_vor_3.20.0.md)",
    ]
    p.write_text(text.rstrip("\n") + "\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
    print("fortgeschrieben: 00_INDEX.md")


def bestandsdokumente():
    bearbeite(DOCS / "01_PRODUCT_CONSTRAINTS.md", [
        ("# Produktgrenzen – Glide 3.19.0", "# Produktgrenzen – Glide 3.20.0"),
        ("3.19 ergänzt den dauerhaften Änderungsverlauf",
         "3.20 ergänzt die Kalenderausgabe als ICS-Datei: eine Ausgabe, keine Anbindung. Keine "
         "Synchronisierung und kein Rückweg aus dem Kalender, kein Konto, kein Netzzugriff, keine "
         "automatische Neuausgabe; keine VTODO-Ausgabe, keine Teilnehmer, Orte oder "
         "Ausnahmetermine, keine mitgelieferte Zeitzonentabelle. Punkte ohne Fälligkeit erscheinen "
         "nicht, ab 2000 Terminen endet die Ausgabe. "
         "[Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "3.19 ergänzt den dauerhaften Änderungsverlauf"),
    ])
    bearbeite(DOCS / "02_ARCHITECTURE.md", [
        ("# Architektur – Glide 3.19.0", "# Architektur – Glide 3.20.0"),
        ("3.19 ergänzt `history_snapshot`",
         "3.20 ergänzt `build_ics_document`, `ics_sources`, `ics_event_lines`, `ics_alarm_lines`, "
         "`ics_repeat_rule`, `write_ics_document`, `escape_ics_text`, `fold_ics_line`, "
         "`ics_utc_stamp`, `ics_local_stamp` und `show_calendar_export_dialog`. Die Mengen kommen "
         "aus `print_document_sections` – dieselbe Datengrundlage wie der Druck, damit Ausgabe und "
         "Ansicht nicht auseinanderlaufen. Die Ausgabe ist rein lesend: kein neues Datenfeld, kein "
         "Verlaufseintrag, keine neue Laufzeitabhängigkeit. "
         "[Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n3.19 ergänzt `history_snapshot`"),
    ])
    bearbeite(DOCS / "03_STARTKONTEXT.md", [
        ("# Startkontext – Glide 3.19.0", "# Startkontext – Glide 3.20.0"),
        ("Glide-Aufgaben-und-Listen_v3.19.0.pyw", "Glide-Aufgaben-und-Listen_v3.20.0.pyw"),
        ("und der dauerhafte Änderungsverlauf in 3.19. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten.",
         "der dauerhafte Änderungsverlauf in 3.19 und die Kalenderausgabe als ICS in 3.20. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten."),
        ("3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15; der "
         "Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).",
         "3.20 ergänzt die Kalenderausgabe als ICS; sie liest nur vorhandene Objekte und verändert "
         "nichts. Aufgabenformat 15 bleibt unverändert. "
         "[Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15; der "
         "Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. "
         "[Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md)."),
    ])
    bearbeite(DOCS / "05_QA_TESTPLAN.md", [
        ("# Prüfplan – Glide 3.19.0", "# Prüfplan – Glide 3.20.0"),
        ("Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss`. Dreiundzwanzig Suiten,",
         "Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.20.0/abschluss`. Vierundzwanzig Suiten,"),
        ("`test_features319.py` prüft die Migration",
         "`test_features320.py` prüft den Aufbau aller vier Umfänge, Ganztags- und "
         "Uhrzeittermine, die Dauerregeln, jede der sechs Optionen einzeln, alle sechs "
         "Wiederholungsarten samt Enddatum, beide Erinnerungsarten, Escaping und Zeilenfaltung "
         "einschließlich Rückfaltung, stabile UIDs über zwei Ausgaben, übersprungene Punkte ohne "
         "Fälligkeit, die Obergrenze von 2000 Terminen, atomares Schreiben samt abgewiesener "
         "Nutzdatendatei, die Unveränderlichkeit von Bestand und Verlauf sowie den Dialog in "
         "beiden Themes. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "`test_features319.py` prüft die Migration"),
    ])
    bearbeite(DOCS / "06_DATA_BACKUP_MIGRATION.md", [
        ("# Daten, Backups und Migration – Glide 3.19.0", "# Daten, Backups und Migration – Glide 3.20.0"),
        ("3.19 hebt das Aufgabenformat auf **15**",
         "3.20 ergänzt die Kalenderausgabe. Sie schreibt ausschließlich ICS-Dateien an ein "
         "gewähltes Ziel, atomar über eine Temporärdatei; Nutzdatendateien sind als Ziel "
         "ausgeschlossen. Aufgabenformat 15, Einstellungen und Vorlagen bleiben unberührt, und es "
         "entsteht kein Verlaufseintrag – eine Ausgabe ist keine Änderung. "
         "[Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "3.19 hebt das Aufgabenformat auf **15**"),
    ])
    bearbeite(DOCS / "09_PROJECT_HANDOFF.md", [
        ("# Projektübergabe – Glide 3.19.0", "# Projektübergabe – Glide 3.20.0"),
        ("Glide-Aufgaben-und-Listen_v3.19.0.pyw", "Glide-Aufgaben-und-Listen_v3.20.0.pyw"),
        ("3.19 ist das zuletzt umgesetzte Funktionspaket: der dauerhafte Änderungsverlauf mit "
         "Aufgabenformat 15.",
         "3.20 ist das zuletzt umgesetzte Funktionspaket: die Kalenderausgabe als ICS. Bei "
         "Änderungen besonders prüfen: dass jede Ausgabezeile durch `fold_ics_line` läuft (die "
         "Faltung zählt Oktette, nicht Zeichen), dass jeder Textwert durch `escape_ics_text` geht, "
         "dass Ganztagstermine ihr `DTEND` am Folgetag tragen, dass die UID je Punkt stabil bleibt "
         "und Bearbeitungstage eine eigene tragen, und dass die Ausgabe weder Bestand noch "
         "Änderungsverlauf berührt. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "3.19 brachte den dauerhaften Änderungsverlauf mit Aufgabenformat 15."),
    ])
    bearbeite(DOCS / "10_RELEASE_CHECKLIST.md", [
        ("# Release-Checkliste – Glide 3.19.0", "# Release-Checkliste – Glide 3.20.0"),
        ("- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.19.0 abstimmen.",
         "- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf 3.20.0 abstimmen."),
        ("Für 3.19 zusätzlich den Änderungsverlauf abnehmen:",
         "Für 3.20 zusätzlich die Kalenderausgabe abnehmen: je eine Datei in Apple Kalender, "
         "Outlook und Thunderbird einlesen, Ganztags- und Uhrzeittermine, Dauer, Priorität, "
         "Kategorien und Alarme im Kalender prüfen, eine Serie über mehrere Wochen ansehen, "
         "dieselbe Datei ein zweites Mal einlesen und prüfen, dass Termine aktualisiert und nicht "
         "verdoppelt werden. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).\n\n"
         "Für 3.19 zusätzlich den Änderungsverlauf abnehmen:"),
    ])
    for name in ("11_BESTANDSANALYSE.md", "12_ABSCHLUSSBERICHT.md", "25_FEATURE_ABGLEICH_3.7.0.md"):
        bearbeite(DOCS / name, [
            ("Aktueller Entwicklungsstand: **3.19.0 / Aufgabenformat 15** mit dauerhaftem Änderungsverlauf. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md), [QA](07_QA_BERICHT.md).",
             "Aktueller Entwicklungsstand: **3.20.0 / Aufgabenformat 15** mit Kalenderausgabe als ICS. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md), [QA](07_QA_BERICHT.md)."),
        ])
    bearbeite(DOCS / "11_BESTANDSANALYSE.md", [("Glide 3.19.0; maßgeblich sind", "Glide 3.20.0; maßgeblich sind")])
    bearbeite(DOCS / "12_ABSCHLUSSBERICHT.md", [
        ("Arbeitsstand ist Glide 3.19.0;", "Arbeitsstand ist Glide 3.20.0;"),
        ("[Dauerhafter Änderungsverlauf](43_AENDERUNGSVERLAUF_3.19.0.md).",
         "[Kalenderausgabe als ICS](44_KALENDERAUSGABE_3.20.0.md)."),
        ("- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw)",
         "- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.20.0.pyw)"),
    ])
    bearbeite(DOCS / "27_VORLAGEN_PRAXISANLEITUNG.md", [
        ("Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2",
         "Stand 14.09.2026 · Glide 3.20.0 · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(DOCS / "decisions" / "PRODUCT_IDENTITY.md", [
        ("Stand 13.09.2026 · App-Version 3.19.0 · Datenformat 15",
         "Stand 14.09.2026 · App-Version 3.20.0 · Datenformat 15"),
    ])
    bearbeite(DOCS / "07_QA_BERICHT.md", [
        ("# QA-Bericht – Glide 3.19.0", "# QA-Bericht – Glide 3.20.0"),
        ("Für 3.19 sind alle dreiundzwanzig Suiten",
         "Für 3.20 sind alle vierundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, "
         "Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter "
         "Xvfb) mit Exitcode 0 gelaufen. Die neue "
         "[Kalendersuite](../tests/integration/test_features320.py) prüft alle vier Umfänge, "
         "Termintypen und Dauerregeln, jede Option, alle Wiederholungsarten, beide "
         "Erinnerungsarten, Escaping und Faltung, stabile UIDs, Obergrenze, Dateischreibung und "
         "den Dialog in beiden Themes. Bestandssuiten mussten nicht angepasst werden: 3.20 ändert "
         "kein Datenfeld. Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht noch "
         "aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.20.0/abschluss`. "
         "Sein Ergebnis wird hier ergänzt.\n\nFür 3.19 sind alle dreiundzwanzig Suiten"),
    ])


def changelog(eintrag_pfad):
    p = R / "CHANGELOG.md"
    text = p.read_text(encoding="utf-8")
    eintrag = Path(eintrag_pfad).read_text(encoding="utf-8").strip() + "\n\n"
    anker = "## 3.19.0 – 13.09.2026"
    if text.count(anker) != 1:
        FEHLER.append(f"CHANGELOG.md: {text.count(anker)} Treffer für den 3.19-Anker")
        return
    p.write_text(text.replace(anker, eintrag + anker, 1), encoding="utf-8")
    print("CHANGELOG: 3.20.0 eingetragen")


def readmes():
    bearbeite(R / "README.md", [
        ("Aktueller interner Entwicklungsstand: **3.19.0** · 13.09.2026",
         "Aktueller interner Entwicklungsstand: **3.20.0** · 14.09.2026"),
        ("07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw",
         "07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.20.0.pyw"),
        ("--protokoll tests/qa-3.19.0/abschluss`", "--protokoll tests/qa-3.20.0/abschluss`"),
        ("[Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](docs/40_APP_BACKUP_3.16.0.md) · [Bedienung 3.15](docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md)",
         "[Bedienung 3.20](docs/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](docs/40_APP_BACKUP_3.16.0.md)"),
    ])
    bearbeite("README.md", [
        ("Neu in 3.19: dauerhafter Änderungsverlauf. Anlegen, Ändern, Erledigen, Verschieben, "
         "Umbenennen, Papierkorb, Wiederherstellen und endgültiges Entfernen bleiben mit "
         "Zeitpunkt, Objekt, Liste und geänderten Feldern nachlesbar – über Programmstarts "
         "hinweg. [Bedienung und Datenregeln](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md).",
         NEU_SATZ + " [Bedienung und Datenregeln](01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)."),
        ("Aktueller Entwicklungsstand: **3.19.0 vom 13.09.2026**: dauerhafter Änderungsverlauf,",
         "Aktueller Entwicklungsstand: **3.20.0 vom 14.09.2026**: Kalenderausgabe als ICS, dauerhafter Änderungsverlauf,"),
        ("[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·",
         "[Kalenderausgabe als ICS 3.20](01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) ·\n"
         "[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·"),
    ])
    bearbeite(A / "README.md", [
        ("Stand 13.09.2026. [Aktueller Ausbau: Dauerhafter Änderungsverlauf 3.19.0](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md).",
         "Stand 14.09.2026. [Aktueller Ausbau: Kalenderausgabe als ICS 3.20.0](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)."),
        ("- [Manuelle Prüfung des 3.19-Stands](Checklisten/Manuelle_Pruefung_3.19.0.md)",
         "- [Manuelle Prüfung des 3.20-Stands](Checklisten/Manuelle_Pruefung_3.20.0.md)"),
        ("- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_3.19.0.md)",
         "- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_3.20.0.md)"),
        ("- [Bedienvertrag 3.19.0: Dauerhafter Änderungsverlauf, umgesetzt](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)",
         "- [Bedienvertrag 3.20.0: Kalenderausgabe als ICS, umgesetzt](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)\n"
         "- [Bedienvertrag 3.19.0: Dauerhafter Änderungsverlauf, umgesetzt](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)"),
        ("- [Technische Fakten 3.19](Notizen/Technische_Fakten_3.19.0.md)",
         "- [Technische Fakten 3.20](Notizen/Technische_Fakten_3.20.0.md)"),
        ("[Dauerhafter Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·",
         "[Kalenderausgabe als ICS 3.20](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) ·\n"
         "[Dauerhafter Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·"),
    ])
    bearbeite(Path("10_Dokumentation/README.md"), [
        ("Stand 13.09.2026 · Glide 3.19.0", "Stand 14.09.2026 · Glide 3.20.0"),
        ("- [Änderungsverlauf](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)",
         "- [Kalenderdatei schreiben](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)\n"
         "- [Änderungsverlauf](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md)"),
        ("- [Bedienung der Praxisvorlagen 3.19](Vorlagen_Praxisanleitung_3.19.0.md)",
         "- [Bedienung der Praxisvorlagen 3.20](Vorlagen_Praxisanleitung_3.20.0.md)"),
        ("[Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·",
         "[Kalenderausgabe 3.20](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) ·\n"
         "[Änderungsverlauf 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·"),
    ])
    bearbeite(Path("40_Store_Material/README.md"), [
        ("[Produktdatenblatt 3.19.0](Produktdatenblatt_3.19.0.md) enthält den aktuellen Entwicklungsnachtrag.",
         "[Produktdatenblatt 3.20.0](Produktdatenblatt_3.20.0.md) enthält den aktuellen Entwicklungsnachtrag."),
    ])
    bearbeite(Path("05_Probelisten_Testdaten/README.md"), [
        ("Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2",
         "Stand 14.09.2026 · Glide 3.20.0 · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(Path("07_Python-Versionen/README.md"), [
        ("Glide 3.19.0 · Entwicklungsstand 13.09.2026 · Aufgabenformat 15 · Vorlagenformat 2",
         "Glide 3.20.0 · Entwicklungsstand 14.09.2026 · Aufgabenformat 15 · Vorlagenformat 2"),
        ("[Glide-Aufgaben-und-Listen_v3.19.0.pyw](Glide-Aufgaben-und-Listen_v3.19.0.pyw) ist die aktuelle Arbeitskopie",
         "[Glide-Aufgaben-und-Listen_v3.20.0.pyw](Glide-Aufgaben-und-Listen_v3.20.0.pyw) ist die aktuelle Arbeitskopie"),
        ("[Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)",
         "[Bedienung 3.20](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)"),
    ])


def weitergabe():
    bearbeite(A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md", [
        ("Neu in 3.19: dauerhafter Änderungsverlauf mit Aufgabenformat 15. Anlegen, Ändern, "
         "Erledigen, Verschieben, Umbenennen, Papierkorb, Wiederherstellen und endgültiges "
         "Entfernen bleiben mit Zeitpunkt, Objekt, Liste und geänderten Feldern nachlesbar; der "
         "Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. "
         "[Bedienung und Datenregeln](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md).",
         NEU_SATZ + " [Bedienung und Datenregeln](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)."),
        ("Stand 13.09.2026 · Entwicklungsstand 3.19.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2",
         "Stand 14.09.2026 · Entwicklungsstand 3.20.0 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"),
        ("der CSV-Import mit Spaltenzuordnung sowie der dauerhafte Änderungsverlauf.",
         "der CSV-Import mit Spaltenzuordnung, der dauerhafte Änderungsverlauf sowie die Kalenderausgabe als ICS."),
        ("`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.19.0.pyw`",
         "`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.20.0.pyw`"),
        ("Für 3.19.0 sind alle dreiundzwanzig Suiten in einer Linux-Vorabumgebung mit Exitcode 0 gelaufen; der maßgebliche macOS-Lauf steht noch aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss`.",
         "Für 3.19.0 und 3.20.0 sind alle Suiten (dreiundzwanzig bzw. vierundzwanzig) in einer "
         "Linux-Vorabumgebung mit Exitcode 0 gelaufen; die maßgeblichen macOS-Läufe stehen noch "
         "aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss` "
         "und `… --protokoll tests/qa-3.20.0/abschluss`."),
        ("[Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md) ·",
         "[Bedienung 3.20](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) · [Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) ·"),
        ("Datenregeln von 3.19:",
         "Datenregeln von 3.20: Die Kalenderausgabe ist rein lesend – sie schreibt nur ICS-Dateien "
         "an ein gewähltes Ziel (atomar, Nutzdatendateien ausgeschlossen), verändert weder Bestand "
         "noch Einstellungen und erzeugt keinen Verlaufseintrag. Termine stehen in schwebender "
         "Ortszeit, nur `DTSTAMP` und feste Alarme in UTC; die UID je Punkt ist stabil, damit "
         "erneutes Einlesen aktualisiert statt verdoppelt. Obergrenze 2000 Termine.\n\n"
         "Datenregeln von 3.19:"),
        ("Nächste offene Ideen: Kalenderausgabe als ICS, benutzerdefinierte Felder und darauf aufbauende eigene Ansichten.",
         "Nächste offene Ideen: benutzerdefinierte Felder und darauf aufbauende eigene Ansichten; "
         "ein Kalenderimport (ICS lesen) wäre das Gegenstück zur Ausgabe aus 3.20."),
    ])
    bearbeite(A / "Glide_Funktionsvorschlaege_2026-09-11.md", [
        ("14. Dauerhafter Änderungsverlauf – **umgesetzt in 3.19.0** mit Aufgabenformat 15;",
         "15. Kalenderausgabe als ICS – **umgesetzt in 3.20.0**; vier Umfänge, Termintypen, "
         "Dauerregeln, Optionen, Wiederholungen, Alarme, Format, stabile UIDs, Grenzen und Dialog "
         "sind automatisiert geprüft. "
         "[Bedienvertrag](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md). Nächste "
         "offene Ausbaustufen: benutzerdefinierte Felder, eigene Ansichten je Feld und ein "
         "Kalenderimport.\n"
         "14. Dauerhafter Änderungsverlauf – **umgesetzt in 3.19.0** mit Aufgabenformat 15;"),
        ("| Import und Integrationen | CSV mit Spaltenzuordnung ist in 3.18.0 umgesetzt; offen bleiben Kalenderdateien und später gezielte Mail-/Kalenderschnittstellen.",
         "| Import und Integrationen | CSV mit Spaltenzuordnung ist in 3.18.0 umgesetzt, die Kalenderausgabe als ICS in 3.20.0; offen bleiben der Kalenderimport und später gezielte Mail-/Kalenderschnittstellen."),
    ])


def abgeleitet(quelle):
    for name, ziel in (("Technische_Fakten_3.20.0.md", A / "Notizen"),
                       ("Manuelle_Pruefung_3.20.0.md", A / "Checklisten"),
                       ("Offene_Entscheidungen_3.20.0.md", A / "Entscheidungen")):
        shutil.copy2(Path(quelle) / name, ziel / name)
        print("abgelegt:", ziel / name)
    vorlage = Path("10_Dokumentation/Archiv/Vorlagen_Praxisanleitung_3.19.0.md")
    text = vorlage.read_text(encoding="utf-8").replace(
        "Stand 13.09.2026 · Glide 3.19.0 · Aufgabenformat 15 · Vorlagenformat 2",
        "Stand 14.09.2026 · Glide 3.20.0 · Aufgabenformat 15 · Vorlagenformat 2")
    Path("10_Dokumentation/Vorlagen_Praxisanleitung_3.20.0.md").write_text(text, encoding="utf-8")
    blatt = Path("40_Store_Material/Archiv/Produktdatenblatt_3.19.0.md")
    text = blatt.read_text(encoding="utf-8")
    paare = [
        ("# Glide Produktdatenblatt 3.19.0", "# Glide Produktdatenblatt 3.20.0"),
        ("Der 3.19-Stand ist lokal geprüft: 23 Testsuiten", "Der 3.20-Stand ist lokal geprüft: 24 Testsuiten"),
        ("[Aktuelle Bedienung](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) ·",
         "[Aktuelle Bedienung](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md) ·"),
    ]
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"Produktdatenblatt: {text.count(alt)} Treffer für {alt[:60]!r}")
            continue
        text = text.replace(alt, neu)
    zeilen = text.splitlines()
    for index, zeile in enumerate(zeilen):
        if zeile.startswith("| Austausch |") and "Kalenderausgabe" not in zeile:
            zeilen[index] = zeile.replace("portable Backups", "Kalenderausgabe als ICS, portable Backups")
            break
    text = "\n".join(zeilen) + ("\n" if text.endswith("\n") else "")
    for alt, neu in (("Neu in 3.19: dauerhafter Änderungsverlauf", "Neu in 3.20: Kalenderausgabe als ICS"),):
        if alt in text:
            # Der Einleitungssatz wird vollständig ersetzt, nicht nur der Anfang.
            anfang = text.index(alt)
            ende = text.index("\n\n", anfang)
            text = text[:anfang] + NEU_SATZ + " [Bedienung und Datenregeln](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md)." + text[ende:]
    Path("40_Store_Material/Produktdatenblatt_3.20.0.md").write_text(text, encoding="utf-8")
    print("abgeleitet: Vorlagenanleitung und Produktdatenblatt 3.20.0")


if __name__ == "__main__":
    quelle = sys.argv[1] if len(sys.argv) > 1 else "50_Ablage/Werkzeuge_3.20.0"
    archiviere()
    index()
    bestandsdokumente()
    changelog(Path(quelle) / "changelog_320.md")
    readmes()
    weitergabe()
    abgeleitet(Path(quelle) / "abgeleitet")
    print()
    if FEHLER:
        print("NICHT ANGEWENDET – bitte prüfen:")
        for zeile in FEHLER:
            print(" -", zeile)
        sys.exit(1)
    print("Doku-Kette vollständig auf 3.20.0 fortgeschrieben")
