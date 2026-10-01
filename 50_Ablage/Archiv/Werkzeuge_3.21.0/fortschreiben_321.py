#!/usr/bin/env python3
"""Doku-Kette der Arbeitsablage von 3.20.0 auf 3.21.0 fortschreiben.

Läuft im Wurzelordner „Glide ToDo". Das Aufgabenformat bleibt 15; 3.21 liest
Kalenderdateien. Jede Ersetzung wird gezählt – eine nicht mehr passende
Erwartung bricht sichtbar ab, statt stillschweigend nichts zu treffen.
"""
import shutil
import sys
from pathlib import Path

R = Path("01_Repository/Glide")
DOCS = R / "docs"
A = Path("00_Arbeitsvorbereitung")
ALT, NEU = "3.20.0", "3.21.0"
KURZ_ALT, KURZ_NEU = "3.20", "3.21"
VERTRAG = "45_KALENDERIMPORT_3.21.0.md"
VORVERTRAG = "44_KALENDERAUSGABE_3.20.0.md"
TITEL = "Kalenderimport aus ICS"
VOR_TITEL = "Kalenderausgabe als ICS"
FEHLER = []
NAMEN = ["00_INDEX", "01_PRODUCT_CONSTRAINTS", "02_ARCHITECTURE", "03_STARTKONTEXT",
         "05_QA_TESTPLAN", "06_DATA_BACKUP_MIGRATION", "07_QA_BERICHT", "09_PROJECT_HANDOFF",
         "10_RELEASE_CHECKLIST", "11_BESTANDSANALYSE", "12_ABSCHLUSSBERICHT",
         "25_FEATURE_ABGLEICH_3.7.0", "27_VORLAGEN_PRAXISANLEITUNG"]
NEU_SATZ = ("Neu in 3.21: Kalenderimport aus ICS. Termine einer Kalenderdatei werden Aufgaben "
            "mit Fälligkeit – mit Dauer als Aufwand, Kategorien als Labels, abbildbaren "
            "Wiederholungen und Erinnerungen, mit Vorschau vor der Übernahme und einem "
            "Rückgängig-Schritt.")


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
        shutil.copy2(DOCS / f"{name}.md", DOCS / "archiv" / f"{name}_{ALT}_vor_{NEU}.md")
    shutil.copy2(DOCS / "decisions" / "PRODUCT_IDENTITY.md",
                 DOCS / "decisions" / "archiv" / f"PRODUCT_IDENTITY_{ALT}_vor_{NEU}.md")
    shutil.copy2(R / "CHANGELOG.md", DOCS / "archiv" / f"CHANGELOG_{ALT}_vor_{NEU}.md")
    shutil.copy2(R / "README.md", DOCS / "archiv" / f"README_{ALT}_vor_{NEU}.md")
    shutil.copy2("README.md", DOCS / "archiv" / f"README_root_{ALT}_vor_{NEU}.md")
    for quelle, ziel in (
        (A / "README.md", A / "Archiv" / f"README_{ALT}_vor_{NEU}.md"),
        (A / "Glide_Funktionsvorschlaege_2026-09-11.md",
         A / "Archiv" / f"Glide_Funktionsvorschlaege_2026-09-11_{ALT}_vor_{NEU}.md"),
        (A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md",
         A / "Archiv" / f"Glide_Weitergabe_neuer_Chat_2026-09-11_{ALT}_vor_{NEU}.md"),
        (A / "Notizen" / f"Technische_Fakten_{ALT}.md", A / "Notizen" / "Archiv" / f"Technische_Fakten_{ALT}.md"),
        (A / "Checklisten" / f"Manuelle_Pruefung_{ALT}.md", A / "Checklisten" / "Archiv" / f"Manuelle_Pruefung_{ALT}.md"),
        (A / "Entscheidungen" / f"Offene_Entscheidungen_{ALT}.md",
         A / "Entscheidungen" / "Archiv" / f"Offene_Entscheidungen_{ALT}.md"),
        (Path(f"10_Dokumentation/Vorlagen_Praxisanleitung_{ALT}.md"),
         Path(f"10_Dokumentation/Archiv/Vorlagen_Praxisanleitung_{ALT}.md")),
        (Path(f"40_Store_Material/Produktdatenblatt_{ALT}.md"),
         Path(f"40_Store_Material/Archiv/Produktdatenblatt_{ALT}.md")),
    ):
        if Path(quelle).is_file():
            Path(ziel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(quelle, ziel)
    for d in ("05_Probelisten_Testdaten", "07_Python-Versionen", "10_Dokumentation", "40_Store_Material"):
        shutil.copy2(Path(d, "README.md"), Path(d, "Archiv", f"README_{ALT}_vor_{NEU}.md"))
    print("Vorfassungen archiviert")


def index():
    p = DOCS / "00_INDEX.md"
    text = p.read_text(encoding="utf-8")
    paare = [
        (f"Aktueller Entwicklungsstand: {ALT} / Format 15. [{VOR_TITEL}]({VORVERTRAG}).",
         f"Aktueller Entwicklungsstand: {NEU} / Format 15. [{TITEL}]({VERTRAG})."),
        (f"Stand 14.09.2026 · Glide {ALT} · Aufgabenformat 15 · Einstellungen 2 · Vorlagenformat 2",
         f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Einstellungen 2 · Vorlagenformat 2"),
        (f"- [{VOR_TITEL} {ALT}]({VORVERTRAG})\n- [QA-Bericht {ALT}](07_QA_BERICHT.md)\n"
         f"- [Daten, Backups und Migration {ALT}](06_DATA_BACKUP_MIGRATION.md)\n"
         f"- [Projektübergabe {ALT}](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste {ALT}](10_RELEASE_CHECKLIST.md)",
         f"- [{TITEL} {NEU}]({VERTRAG})\n- [QA-Bericht {NEU}](07_QA_BERICHT.md)\n"
         f"- [Daten, Backups und Migration {NEU}](06_DATA_BACKUP_MIGRATION.md)\n"
         f"- [Projektübergabe {NEU}](09_PROJECT_HANDOFF.md)\n- [Release-Checkliste {NEU}](10_RELEASE_CHECKLIST.md)\n"
         f"- [{VOR_TITEL} {ALT}]({VORVERTRAG})"),
        (f"{KURZ_ALT}-Dokumenten oben und in der Funktionsübersicht.",
         f"{KURZ_NEU}-Dokumenten oben und in der Funktionsübersicht."),
        (f"- [{VORVERTRAG}](<{VORVERTRAG}>)",
         f"- [{VORVERTRAG}](<{VORVERTRAG}>)\n- [{VERTRAG}](<{VERTRAG}>)"),
        (f"- [07_QA_BERICHT_{ALT}_vor_Pruefnachtrag](archiv/07_QA_BERICHT_{ALT}_vor_Pruefnachtrag.md)",
         f"- [07_QA_BERICHT_{ALT}_vor_Pruefnachtrag](archiv/07_QA_BERICHT_{ALT}_vor_Pruefnachtrag.md)\n"
         f"- [07_QA_BERICHT_{NEU}_vor_Pruefnachtrag](archiv/07_QA_BERICHT_{NEU}_vor_Pruefnachtrag.md)"),
    ]
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"00_INDEX.md: {text.count(alt)} Treffer für {alt[:70]!r}")
            continue
        text = text.replace(alt, neu)
    zeilen = ["", f"## Ergänzte Archivnachweise {KURZ_ALT} vor {KURZ_NEU}", ""]
    zeilen += [f"- [{name}_{ALT}_vor_{NEU}](archiv/{name}_{ALT}_vor_{NEU}.md)" for name in NAMEN]
    zeilen += [
        f"- [CHANGELOG_{ALT}_vor_{NEU}](archiv/CHANGELOG_{ALT}_vor_{NEU}.md)",
        f"- [README_{ALT}_vor_{NEU}](archiv/README_{ALT}_vor_{NEU}.md)",
        f"- [README_root_{ALT}_vor_{NEU}](archiv/README_root_{ALT}_vor_{NEU}.md)",
        f"- [PRODUCT_IDENTITY_{ALT}_vor_{NEU}](decisions/archiv/PRODUCT_IDENTITY_{ALT}_vor_{NEU}.md)",
    ]
    p.write_text(text.rstrip("\n") + "\n" + "\n".join(zeilen) + "\n", encoding="utf-8")
    print("fortgeschrieben: 00_INDEX.md")


def bestandsdokumente():
    bearbeite(DOCS / "01_PRODUCT_CONSTRAINTS.md", [
        (f"# Produktgrenzen – Glide {ALT}", f"# Produktgrenzen – Glide {NEU}"),
        (f"{KURZ_ALT} ergänzt die Kalenderausgabe als ICS-Datei:",
         f"{KURZ_NEU} ergänzt den Kalenderimport: Glide liest eine ICS-Datei, die man ihm gibt – "
         "keine Synchronisierung, kein Abonnement, kein Netzzugriff und kein Abgleich, der "
         "vorhandene Punkte aktualisiert. Keine Teilnehmer, Anhänge oder Ausnahmetermine, keine "
         "VTODO-Einträge, keine Zeitzonendefinitionen aus der Datei. Nicht abbildbare "
         "Wiederholungsregeln und Erinnerungen werden verworfen und gezählt statt still "
         "vereinfacht; Grenzen sind 2000 Termine und 12 MB je Datei. "
         f"[Bedienung {KURZ_NEU}]({VERTRAG}).\n\n{KURZ_ALT} ergänzt die Kalenderausgabe als ICS-Datei:"),
    ])
    bearbeite(DOCS / "02_ARCHITECTURE.md", [
        (f"# Architektur – Glide {ALT}", f"# Architektur – Glide {NEU}"),
        (f"{KURZ_ALT} ergänzt `build_ics_document`",
         f"{KURZ_NEU} ergänzt `read_ics_file`, `unfold_ics_lines`, `parse_ics_property`, "
         "`parse_ics_events`, `parse_ics_moment`, `parse_ics_duration`, `unescape_ics_text`, "
         "`ics_repeat_from_rule`, `ics_importance_from_priority`, `ics_events_to_items`, "
         "`ics_preview_text`, `import_ics_events`, `known_glide_item_ids` und "
         "`show_ics_import_dialog`. Der Parser arbeitet ohne Fremdbibliothek: Entfalten, "
         "Eigenschaften mit Parametern, VEVENT- und VALARM-Blöcke. Punkte entstehen "
         "ausschließlich über `new_item`, die Übernahme läuft als ein `snapshot_undo`-Schritt. "
         "Kein neues Datenfeld, keine neue Laufzeitabhängigkeit – `zoneinfo` ist "
         "Standardbibliothek und wird nur genutzt, wenn das System die Zeitzonendatenbank "
         f"mitbringt. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n{KURZ_ALT} ergänzt `build_ics_document`"),
    ])
    bearbeite(DOCS / "03_STARTKONTEXT.md", [
        (f"# Startkontext – Glide {ALT}", f"# Startkontext – Glide {NEU}"),
        (f"Glide-Aufgaben-und-Listen_v{ALT}.pyw", f"Glide-Aufgaben-und-Listen_v{NEU}.pyw"),
        ("und die Kalenderausgabe als ICS in 3.20. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten.",
         "die Kalenderausgabe als ICS in 3.20 und der Kalenderimport in 3.21. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten."),
        (f"{KURZ_ALT} ergänzt die Kalenderausgabe als ICS; sie liest nur vorhandene Objekte und verändert "
         f"nichts. Aufgabenformat 15 bleibt unverändert. "
         f"[Bedienung {KURZ_ALT}]({VORVERTRAG}).",
         f"{KURZ_NEU} ergänzt den Kalenderimport; er legt ausschließlich neue Punkte an, überschreibt "
         "nichts und ist mit Rückgängig vollständig zurücknehmbar. Aufgabenformat 15 bleibt "
         f"unverändert. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n"
         f"{KURZ_ALT} ergänzt die Kalenderausgabe als ICS; sie liest nur vorhandene Objekte und verändert "
         f"nichts. Aufgabenformat 15 bleibt unverändert. [Bedienung {KURZ_ALT}]({VORVERTRAG})."),
    ])
    bearbeite(DOCS / "05_QA_TESTPLAN.md", [
        (f"# Prüfplan – Glide {ALT}", f"# Prüfplan – Glide {NEU}"),
        (f"Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-{ALT}/abschluss`. Vierundzwanzig Suiten,",
         f"Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-{NEU}/abschluss`. Fünfundzwanzig Suiten,"),
        ("`test_features320.py` prüft den Aufbau",
         "`test_features321.py` prüft den Rundlauf über die eigene Ausgabe samt "
         "Duplikaterkennung, fremde Dateien mit gefalteten Zeilen, Escaping, BOM und "
         "LF-Zeilenenden, Ortszeit, UTC und TZID einschließlich unbekannter Zone, Ganztags- und "
         "Mehrtagestermine, beide Dauerangaben, alle abbildbaren und sechs nicht abbildbare "
         "Wiederholungsregeln, vier Erinnerungsfälle, alle Übersprungsgründe, den Zeitraumfilter, "
         "die Grenzen, beide Importziele, Rückgängig mit Labelrücknahme und den Dialog in beiden "
         f"Themes. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n`test_features320.py` prüft den Aufbau"),
    ])
    bearbeite(DOCS / "06_DATA_BACKUP_MIGRATION.md", [
        (f"# Daten, Backups und Migration – Glide {ALT}", f"# Daten, Backups und Migration – Glide {NEU}"),
        (f"{KURZ_ALT} ergänzt die Kalenderausgabe.",
         f"{KURZ_NEU} ergänzt den Kalenderimport. Er liest eine gewählte Datei, schreibt selbst "
         "keine Datei und legt keine eigene Datenhaltung an; Punkte entstehen über `new_item` und "
         "damit durch dieselbe Prüfung wie handangelegte. Aufgabenformat 15 bleibt unverändert, "
         "bestehende Punkte werden nie überschrieben, und der Vorgang ist ein einzelner "
         "Rückgängig-Schritt einschließlich der dabei angelegten Labels. Eigene UIDs werden "
         "erkannt und übersprungen, damit der Rundlauf mit der Ausgabe aus 3.20 keine Kopien "
         f"anlegt. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n{KURZ_ALT} ergänzt die Kalenderausgabe."),
    ])
    bearbeite(DOCS / "09_PROJECT_HANDOFF.md", [
        (f"# Projektübergabe – Glide {ALT}", f"# Projektübergabe – Glide {NEU}"),
        (f"Glide-Aufgaben-und-Listen_v{ALT}.pyw", f"Glide-Aufgaben-und-Listen_v{NEU}.pyw"),
        (f"{KURZ_ALT} ist das zuletzt umgesetzte Funktionspaket: die Kalenderausgabe als ICS.",
         f"{KURZ_NEU} ist das zuletzt umgesetzte Funktionspaket: der Kalenderimport aus ICS. Bei "
         "Änderungen besonders prüfen: dass `unfold_ics_lines` gefaltete Zeilen vor dem Zerlegen "
         "zusammenfügt, dass `parse_ics_property` Doppelpunkte in Anführungszeichen überliest, "
         "dass `ics_repeat_from_rule` streng bleibt und Unabbildbares verwirft statt vereinfacht, "
         "dass eigene UIDs weiterhin als Duplikat gelten und dass ein fehlgeschlagener Import "
         f"Labelbestand und Rückgängig-Stapel exakt zurücksetzt. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n"
         f"{KURZ_ALT} brachte die Kalenderausgabe als ICS."),
    ])
    bearbeite(DOCS / "10_RELEASE_CHECKLIST.md", [
        (f"# Release-Checkliste – Glide {ALT}", f"# Release-Checkliste – Glide {NEU}"),
        (f"- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf {ALT} abstimmen.",
         f"- Version, App-Konstante, Hauptsuite, Changelog und aktuelle Release-Fixtures auf {NEU} abstimmen."),
        (f"Für {KURZ_ALT} zusätzlich die Kalenderausgabe abnehmen:",
         f"Für {KURZ_NEU} zusätzlich den Kalenderimport abnehmen: je eine Datei aus Apple Kalender, "
         "Outlook und einem Webkalender einlesen, eine Einladung mit Teilnehmern (die Angaben "
         "fehlen erwartungsgemäß), eine Serie und einen Termin mit Alarm; den Rundlauf mit der "
         "eigenen Ausgabe prüfen (keine Kopien) und den Bericht mit den Übersprungsgründen gegen "
         f"die Datei halten. [Bedienung {KURZ_NEU}]({VERTRAG}).\n\n"
         f"Für {KURZ_ALT} zusätzlich die Kalenderausgabe abnehmen:"),
    ])
    for name in ("11_BESTANDSANALYSE.md", "12_ABSCHLUSSBERICHT.md", "25_FEATURE_ABGLEICH_3.7.0.md"):
        bearbeite(DOCS / name, [
            (f"Aktueller Entwicklungsstand: **{ALT} / Aufgabenformat 15** mit {VOR_TITEL}. [Bedienung {KURZ_ALT}]({VORVERTRAG}), [QA](07_QA_BERICHT.md).",
             f"Aktueller Entwicklungsstand: **{NEU} / Aufgabenformat 15** mit {TITEL}. [Bedienung {KURZ_NEU}]({VERTRAG}), [QA](07_QA_BERICHT.md)."),
        ])
    bearbeite(DOCS / "11_BESTANDSANALYSE.md", [(f"Glide {ALT}; maßgeblich sind", f"Glide {NEU}; maßgeblich sind")])
    bearbeite(DOCS / "12_ABSCHLUSSBERICHT.md", [
        (f"Arbeitsstand ist Glide {ALT};", f"Arbeitsstand ist Glide {NEU};"),
        (f"[{VOR_TITEL}]({VORVERTRAG}).", f"[{TITEL}]({VERTRAG})."),
        (f"- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v{ALT}.pyw)",
         f"- [Aktuelle startbare Arbeitskopie](../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw)"),
    ])
    bearbeite(DOCS / "27_VORLAGEN_PRAXISANLEITUNG.md", [
        (f"Stand 14.09.2026 · Glide {ALT} · Aufgabenformat 15 · Vorlagenformat 2",
         f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(DOCS / "decisions" / "PRODUCT_IDENTITY.md", [
        (f"Stand 14.09.2026 · App-Version {ALT} · Datenformat 15",
         f"Stand 14.09.2026 · App-Version {NEU} · Datenformat 15"),
    ])
    bearbeite(DOCS / "07_QA_BERICHT.md", [
        (f"# QA-Bericht – Glide {ALT}", f"# QA-Bericht – Glide {NEU}"),
        (f"Für {KURZ_ALT} sind alle vierundzwanzig Suiten",
         f"Für {KURZ_NEU} sind alle fünfundzwanzig Suiten, beide statischen Analysen sowie "
         "Vorlagen-, Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 "
         "unter Xvfb) mit Exitcode 0 gelaufen. Die neue "
         "[Importsuite](../tests/integration/test_features321.py) prüft den Rundlauf samt "
         "Duplikaterkennung, den Parser, Zeitzonen, Dauerangaben, abbildbare und nicht abbildbare "
         "Wiederholungsregeln, vier Erinnerungsfälle, alle Übersprungsgründe, Zeitraumfilter, "
         "Grenzen, beide Importziele, Rückgängig und den Dialog. Bestandssuiten mussten nicht "
         f"angepasst werden: {KURZ_NEU} ändert kein Datenfeld. Der maßgebliche Abschlusslauf auf "
         "macOS mit Python 3.14.5 steht noch aus: `python3 tests/tools/pruefen.py --modus voll "
         f"--protokoll tests/qa-{NEU}/abschluss`. Sein Ergebnis wird hier ergänzt.\n\n"
         f"Für {KURZ_ALT} sind alle vierundzwanzig Suiten"),
    ])


def changelog(eintrag_pfad):
    p = R / "CHANGELOG.md"
    text = p.read_text(encoding="utf-8")
    eintrag = Path(eintrag_pfad).read_text(encoding="utf-8").strip() + "\n\n"
    anker = f"## {ALT} – 14.09.2026"
    if text.count(anker) != 1:
        FEHLER.append(f"CHANGELOG.md: {text.count(anker)} Treffer für den {KURZ_ALT}-Anker")
        return
    p.write_text(text.replace(anker, eintrag + anker, 1), encoding="utf-8")
    print(f"CHANGELOG: {NEU} eingetragen")


def readmes():
    bearbeite(R / "README.md", [
        (f"Aktueller interner Entwicklungsstand: **{ALT}** · 14.09.2026",
         f"Aktueller interner Entwicklungsstand: **{NEU}** · 14.09.2026"),
        (f"07_Python-Versionen/Glide-Aufgaben-und-Listen_v{ALT}.pyw",
         f"07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw"),
        (f"--protokoll tests/qa-{ALT}/abschluss`", f"--protokoll tests/qa-{NEU}/abschluss`"),
        (f"[Bedienung {KURZ_ALT}](docs/{VORVERTRAG}) · [Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](docs/40_APP_BACKUP_3.16.0.md)",
         f"[Bedienung {KURZ_NEU}](docs/{VERTRAG}) · [Bedienung {KURZ_ALT}](docs/{VORVERTRAG}) · [Bedienung 3.19](docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](docs/41_DRUCK_UND_PDF_3.17.0.md)"),
    ])
    p = Path("README.md")
    text = p.read_text(encoding="utf-8")
    anfang = text.find("Neu in 3.20:")
    if anfang < 0:
        FEHLER.append("README.md: Einleitungssatz „Neu in 3.20:" + "\" nicht gefunden")
    else:
        ende = text.index("\n\n", anfang)
        text = text[:anfang] + NEU_SATZ + f" [Bedienung und Datenregeln](01_Repository/Glide/docs/{VERTRAG})." + text[ende:]
        p.write_text(text, encoding="utf-8")
    bearbeite("README.md", [
        (f"Aktueller Entwicklungsstand: **{ALT} vom 14.09.2026**: {VOR_TITEL},",
         f"Aktueller Entwicklungsstand: **{NEU} vom 14.09.2026**: {TITEL}, {VOR_TITEL},"),
        (f"[{VOR_TITEL} {KURZ_ALT}](01_Repository/Glide/docs/{VORVERTRAG}) ·",
         f"[{TITEL} {KURZ_NEU}](01_Repository/Glide/docs/{VERTRAG}) ·\n"
         f"[{VOR_TITEL} {KURZ_ALT}](01_Repository/Glide/docs/{VORVERTRAG}) ·"),
    ])
    bearbeite(A / "README.md", [
        (f"Stand 14.09.2026. [Aktueller Ausbau: {VOR_TITEL} {ALT}](../01_Repository/Glide/docs/{VORVERTRAG}).",
         f"Stand 14.09.2026. [Aktueller Ausbau: {TITEL} {NEU}](../01_Repository/Glide/docs/{VERTRAG})."),
        (f"- [Manuelle Prüfung des {KURZ_ALT}-Stands](Checklisten/Manuelle_Pruefung_{ALT}.md)",
         f"- [Manuelle Prüfung des {KURZ_NEU}-Stands](Checklisten/Manuelle_Pruefung_{NEU}.md)"),
        (f"- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_{ALT}.md)",
         f"- [Offene Inhaberentscheidungen](Entscheidungen/Offene_Entscheidungen_{NEU}.md)"),
        (f"- [Bedienvertrag {ALT}: {VOR_TITEL}, umgesetzt](../01_Repository/Glide/docs/{VORVERTRAG})",
         f"- [Bedienvertrag {NEU}: {TITEL}, umgesetzt](../01_Repository/Glide/docs/{VERTRAG})\n"
         f"- [Bedienvertrag {ALT}: {VOR_TITEL}, umgesetzt](../01_Repository/Glide/docs/{VORVERTRAG})"),
        (f"- [Technische Fakten {KURZ_ALT}](Notizen/Technische_Fakten_{ALT}.md)",
         f"- [Technische Fakten {KURZ_NEU}](Notizen/Technische_Fakten_{NEU}.md)"),
        (f"[{VOR_TITEL} {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) ·",
         f"[{TITEL} {KURZ_NEU}](../01_Repository/Glide/docs/{VERTRAG}) ·\n"
         f"[{VOR_TITEL} {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) ·"),
    ])
    bearbeite(Path("10_Dokumentation/README.md"), [
        (f"Stand 14.09.2026 · Glide {ALT}", f"Stand 14.09.2026 · Glide {NEU}"),
        (f"- [Kalenderdatei schreiben](../01_Repository/Glide/docs/{VORVERTRAG})",
         f"- [Kalenderdatei lesen](../01_Repository/Glide/docs/{VERTRAG})\n"
         f"- [Kalenderdatei schreiben](../01_Repository/Glide/docs/{VORVERTRAG})"),
        (f"- [Bedienung der Praxisvorlagen {KURZ_ALT}](Vorlagen_Praxisanleitung_{ALT}.md)",
         f"- [Bedienung der Praxisvorlagen {KURZ_NEU}](Vorlagen_Praxisanleitung_{NEU}.md)"),
        (f"[Kalenderausgabe {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) ·",
         f"[Kalenderimport {KURZ_NEU}](../01_Repository/Glide/docs/{VERTRAG}) ·\n"
         f"[Kalenderausgabe {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) ·"),
    ])
    bearbeite(Path("40_Store_Material/README.md"), [
        (f"[Produktdatenblatt {ALT}](Produktdatenblatt_{ALT}.md) enthält den aktuellen Entwicklungsnachtrag.",
         f"[Produktdatenblatt {NEU}](Produktdatenblatt_{NEU}.md) enthält den aktuellen Entwicklungsnachtrag."),
    ])
    bearbeite(Path("05_Probelisten_Testdaten/README.md"), [
        (f"Stand 14.09.2026 · Glide {ALT} · Aufgabenformat 15 · Vorlagenformat 2",
         f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Vorlagenformat 2"),
    ])
    bearbeite(Path("07_Python-Versionen/README.md"), [
        (f"Glide {ALT} · Entwicklungsstand 14.09.2026 · Aufgabenformat 15 · Vorlagenformat 2",
         f"Glide {NEU} · Entwicklungsstand 14.09.2026 · Aufgabenformat 15 · Vorlagenformat 2"),
        (f"[Glide-Aufgaben-und-Listen_v{ALT}.pyw](Glide-Aufgaben-und-Listen_v{ALT}.pyw) ist die aktuelle Arbeitskopie",
         f"[Glide-Aufgaben-und-Listen_v{NEU}.pyw](Glide-Aufgaben-und-Listen_v{NEU}.pyw) ist die aktuelle Arbeitskopie"),
        (f"[Bedienung {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)",
         f"[Bedienung {KURZ_NEU}](../01_Repository/Glide/docs/{VERTRAG}) · [Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md)"),
    ])
    # Der Einleitungssatz der Python-Ablage wird vollständig ersetzt.
    p = Path("07_Python-Versionen/README.md")
    text = p.read_text(encoding="utf-8")
    anfang = text.find("Neu in 3.20:")
    if anfang >= 0:
        ende = text.index("\n\n", anfang)
        text = text[:anfang] + NEU_SATZ + f" [Bedienung und Datenregeln](../01_Repository/Glide/docs/{VERTRAG})." + text[ende:]
        p.write_text(text, encoding="utf-8")
        print("Einleitungssatz 07_Python-Versionen ersetzt")


def weitergabe():
    p = A / "Glide_Weitergabe_neuer_Chat_2026-09-11.md"
    text = p.read_text(encoding="utf-8")
    anfang = text.find("Neu in 3.20:")
    if anfang < 0:
        FEHLER.append("Weitergabe: Einleitungssatz nicht gefunden")
    else:
        ende = text.index("\n\n", anfang)
        text = text[:anfang] + NEU_SATZ + f" [Bedienung und Datenregeln](../01_Repository/Glide/docs/{VERTRAG})." + text[ende:]
        p.write_text(text, encoding="utf-8")
    bearbeite(p, [
        (f"Stand 14.09.2026 · Entwicklungsstand {ALT} · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2",
         f"Stand 14.09.2026 · Entwicklungsstand {NEU} · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"),
        ("der dauerhafte Änderungsverlauf sowie die Kalenderausgabe als ICS.",
         "der dauerhafte Änderungsverlauf sowie Kalenderausgabe und Kalenderimport als ICS."),
        (f"`07_Python-Versionen/Glide-Aufgaben-und-Listen_v{ALT}.pyw`",
         f"`07_Python-Versionen/Glide-Aufgaben-und-Listen_v{NEU}.pyw`"),
        ("Für 3.19.0 und 3.20.0 sind alle Suiten (dreiundzwanzig bzw. vierundzwanzig) in einer "
         "Linux-Vorabumgebung mit Exitcode 0 gelaufen; die maßgeblichen macOS-Läufe stehen noch "
         "aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.19.0/abschluss` "
         "und `… --protokoll tests/qa-3.20.0/abschluss`.",
         "Für 3.19.0 bis 3.21.0 sind alle Suiten (dreiundzwanzig bis fünfundzwanzig) in einer "
         "Linux-Vorabumgebung mit Exitcode 0 gelaufen; die maßgeblichen macOS-Läufe stehen noch "
         "aus, zuletzt `python3 tests/tools/pruefen.py --modus voll --protokoll "
         "tests/qa-3.21.0/abschluss`."),
        (f"[Bedienung {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) · [Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) · [Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) ·",
         f"[Bedienung {KURZ_NEU}](../01_Repository/Glide/docs/{VERTRAG}) · [Bedienung {KURZ_ALT}](../01_Repository/Glide/docs/{VORVERTRAG}) · [Bedienung 3.19](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md) · [Bedienung 3.18](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md) ·"),
        (f"Datenregeln von {KURZ_ALT}:",
         f"Datenregeln von {KURZ_NEU}: Der Kalenderimport liest eine gewählte Datei und schreibt "
         "selbst keine. Punkte entstehen über `new_item`, Labels über `ensure_label_by_name`; "
         "bestehende Punkte werden nie überschrieben. Eigene UIDs gelten als Duplikat und werden "
         "übersprungen; nicht abbildbare Wiederholungsregeln und Erinnerungen werden verworfen und "
         "gezählt. Grenzen: 2000 Termine, 12 MB je Datei. Ein Import ist ein Rückgängig-Schritt "
         f"einschließlich neuer Labels.\n\nDatenregeln von {KURZ_ALT}:"),
        ("Nächste offene Ideen: benutzerdefinierte Felder, darauf aufbauende eigene Ansichten und "
         "ein Kalenderimport als Gegenstück zur Ausgabe aus 3.20.",
         "Nächste offene Ideen: benutzerdefinierte Felder und darauf aufbauende eigene Ansichten; "
         "eine echte Kalendersynchronisierung bleibt bewusst außen vor."),
    ])
    bearbeite(A / "Glide_Funktionsvorschlaege_2026-09-11.md", [
        (f"15. {VOR_TITEL} – **umgesetzt in {ALT}**;",
         f"16. {TITEL} – **umgesetzt in {NEU}**; Rundlauf mit Duplikaterkennung, Parser, "
         "Zeitzonen, Dauerangaben, Wiederholungsregeln, Erinnerungen, Übersprungsgründe, "
         "Zeitraumfilter, Grenzen, Ziele, Rückgängig und Dialog sind automatisiert geprüft. "
         f"[Bedienvertrag](../01_Repository/Glide/docs/{VERTRAG}). Nächste offene Ausbaustufen: "
         "benutzerdefinierte Felder und eigene Ansichten je Feld.\n"
         f"15. {VOR_TITEL} – **umgesetzt in {ALT}**;"),
        ("offen bleiben der Kalenderimport und später gezielte Mail-/Kalenderschnittstellen.",
         "der Kalenderimport in 3.21.0; offen bleiben eine echte Kalendersynchronisierung und später gezielte Mailschnittstellen."),
    ])


def abgeleitet(quelle):
    for name, ziel in ((f"Technische_Fakten_{NEU}.md", A / "Notizen"),
                       (f"Manuelle_Pruefung_{NEU}.md", A / "Checklisten"),
                       (f"Offene_Entscheidungen_{NEU}.md", A / "Entscheidungen")):
        shutil.copy2(Path(quelle) / name, ziel / name)
        print("abgelegt:", ziel / name)
    vorlage = Path(f"10_Dokumentation/Archiv/Vorlagen_Praxisanleitung_{ALT}.md")
    text = vorlage.read_text(encoding="utf-8").replace(
        f"Stand 14.09.2026 · Glide {ALT} · Aufgabenformat 15 · Vorlagenformat 2",
        f"Stand 14.09.2026 · Glide {NEU} · Aufgabenformat 15 · Vorlagenformat 2")
    Path(f"10_Dokumentation/Vorlagen_Praxisanleitung_{NEU}.md").write_text(text, encoding="utf-8")
    blatt = Path(f"40_Store_Material/Archiv/Produktdatenblatt_{ALT}.md")
    text = blatt.read_text(encoding="utf-8")
    paare = [
        (f"# Glide Produktdatenblatt {ALT}", f"# Glide Produktdatenblatt {NEU}"),
        (f"Der {KURZ_ALT}-Stand ist lokal geprüft: 24 Testsuiten",
         f"Der {KURZ_NEU}-Stand ist lokal geprüft: 25 Testsuiten"),
        (f"[Aktuelle Bedienung](../01_Repository/Glide/docs/{VORVERTRAG}) ·",
         f"[Aktuelle Bedienung](../01_Repository/Glide/docs/{VERTRAG}) ·"),
    ]
    for alt, neu in paare:
        if text.count(alt) != 1:
            FEHLER.append(f"Produktdatenblatt: {text.count(alt)} Treffer für {alt[:60]!r}")
            continue
        text = text.replace(alt, neu)
    zeilen = text.splitlines()
    for index, zeile in enumerate(zeilen):
        if zeile.startswith("| Austausch |") and "Kalenderimport" not in zeile:
            zeilen[index] = zeile.replace("Kalenderausgabe als ICS", "Kalenderausgabe und -import als ICS")
            break
    text = "\n".join(zeilen) + ("\n" if text.endswith("\n") else "")
    anfang = text.find("Neu in 3.20:")
    if anfang >= 0:
        ende = text.index("\n\n", anfang)
        text = text[:anfang] + NEU_SATZ + f" [Bedienung und Datenregeln](../01_Repository/Glide/docs/{VERTRAG})." + text[ende:]
    Path(f"40_Store_Material/Produktdatenblatt_{NEU}.md").write_text(text, encoding="utf-8")
    print(f"abgeleitet: Vorlagenanleitung und Produktdatenblatt {NEU}")


if __name__ == "__main__":
    quelle = sys.argv[1] if len(sys.argv) > 1 else f"50_Ablage/Werkzeuge_{NEU}"
    archiviere()
    index()
    bestandsdokumente()
    changelog(Path(quelle) / "changelog_321.md")
    readmes()
    weitergabe()
    abgeleitet(Path(quelle) / "abgeleitet")
    print()
    if FEHLER:
        print("NICHT ANGEWENDET – bitte prüfen:")
        for zeile in FEHLER:
            print(" -", zeile)
        sys.exit(1)
    print(f"Doku-Kette vollständig auf {NEU} fortgeschrieben")
