#!/usr/bin/env python3
"""Schreibt die Glide-Dokumentenkette von 3.21.3 auf 3.21.4 fort.

3.21.4 ist ein Korrekturstand: kein Anwendungscode ausser der Versionsangabe.
Er behebt, was ein vollstaendiger Durchgang durch alle 93 aktiven Dokumente
gefunden hat - darunter zwoelf sachlich falsche Aussagen ueber den
Anwendungscode, fuenf ueberholte Formatstufen, acht falsche Verweise und vier
eigene Zaehlfehler aus 3.21.3.

Aufruf im Ordner "Glide ToDo":

    python3 fortschreiben_3214.py <Werkzeugordner> --probe    # nur zeigen
    python3 fortschreiben_3214.py <Werkzeugordner>            # schreiben

Grundsaetze: Jede Datei wird als Ganzes im Puffer berechnet; geschrieben wird
erst am Ende und nur, wenn alle Pflichtstellen zutreffen. Vorfassungen gehen
vorher ins archiv/ desselben Ordners. Es wird nichts geloescht.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ALT, NEU = "3.21.3", "3.21.4"
DATUM = "14.09.2026"
REPO_TEIL = "01_Repository/Glide"
STAND = f"Stand {DATUM} · Glide {NEU} · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2"

# Versionsdurchgang. Der Lookaround verhindert nur Treffer innerhalb einer
# laengeren Nummer; Dateinamen wie v3.21.3.pyw sollen ausdruecklich mitgehen.
VERSIONSPASS = re.compile(r"(?<![\d.])" + re.escape(ALT) + r"(?!\d)")

# Belegstellen: Wortlaute, die den 3.21.3-Stand dokumentieren und bleiben
# muessen. Sie werden vor dem Durchgang durch Platzhalter ersetzt.
BELEGE = (
    f"_vor_{ALT}",              # jede Archivfassung
    f"_{ALT}_vor_",
    f"vor {ALT}",               # Abschnittstitel im Dokumentationsindex
    f"{ALT} vor {NEU}",         # Abschnittstitel, den dieser Lauf selbst anlegt
    f"Werkzeuge_{ALT}",
    f"qa-{ALT}/abschluss/ergebnis.json",
    f"Abschlusslauf {ALT}",
    f"Für {ALT} sind alle",
    f"seit {ALT}",              # „seit 3.21.3 `standpruefung.py`“
    f"Neu in {ALT}",
    f"Datenregeln von {ALT}",
    f"**{ALT}** ergänzt",       # Abschnitt der Projektübergabe
    f"bis {ALT}",               # „Bis 3.21.3 stand hier …“
)

GESCHUETZT = ("CHANGELOG.md", "07_QA_BERICHT.md",
              "Glide_Weitergabe_neuer_Chat_2026-09-11.md")

# Mit dem Quellstand ausgeliefert (SHA-256-Abgleich in ablegen_3214.py).
# tests/tools/README.md und src/glide/README.md kommen mit 3.21.4 dazu: Beide
# trugen Angaben, die bei jedem Stand haetten mitgehen muessen und es nicht
# taten - „Achtzehn Suiten“, „Format 14“, „Datenformat 13“.
AUSGELIEFERT = (f"{REPO_TEIL}/tests/README.md",
                f"{REPO_TEIL}/tests/fixtures/README.md",
                f"{REPO_TEIL}/tests/tools/README.md",
                f"{REPO_TEIL}/src/glide/README.md")

ERSETZEN = {
    "05_Probelisten_Testdaten/README.md": "probelisten_README.md",
    "00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.21.4.md": "Technische_Fakten_3.21.4.md",
    "00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.21.4.md": "Manuelle_Pruefung_3.21.4.md",
    "00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_3.21.4.md": "Offene_Entscheidungen_3.21.4.md",
}

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

# Wortlaut fuer die Formatstufe: steht als DATA_SCHEMA_VERSION im Code und
# wird ab 3.21.4 von standpruefung.py gegen ihn geprueft.
FORMATBEREICH = "die Formate 4 bis 15 (`MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis `DATA_SCHEMA_VERSION`)"

# --------------------------------------------------------------------------
# Gezielte Richtigstellungen. (pflicht, alt, neu). Die Regeln laufen NACH dem
# Versionsdurchgang auf demselben Puffer.
# --------------------------------------------------------------------------
REGELN: dict[str, tuple] = {
    # ============================ A. Falsche Aussagen ueber den Code ======
    # Gegen src/glide/app.pyw in 3.21.3 geprueft.
    f"{REPO_TEIL}/docs/43_AENDERUNGSVERLAUF_3.19.0.md": (
        # SAVE_FILE heisst liste_speicher.json; `glide_liste.json` gibt es
        # nirgends im Code und in keinem anderen Dokument.
        (True, "`glide_liste.json` erhält das Feld `history`",
         "`liste_speicher.json` erhält das Feld `history`"),
        # Im selben Satz wechselte die Menge von 400 auf 412.
        (True, "Wer 400 Zeilen aus einer CSV-Datei importiert, will keine 400 "
               "Verlaufseinträge.",
         "Wer 412 Zeilen aus einer CSV-Datei importiert, will keine 412 "
         "Verlaufseinträge."),
    ),
    f"{REPO_TEIL}/docs/45_KALENDERIMPORT_3.21.0.md": (
        # Der ICS-Import kennt nur MAX_ICS_IMPORT_EVENTS und
        # MAX_ICS_IMPORT_BYTES - keine Zeilenobergrenze. Der Wortlaut stammt
        # aus dem CSV-Vertrag, wo Zeilen und Spalten wirklich begrenzt sind.
        (True, "10. Zeilen-, Größen- und Terminobergrenze brechen vor jeder "
               "Bestandsänderung ab.",
         "10. Termin- und Größenobergrenze brechen vor jeder Bestandsänderung ab; "
         "eine Zeilenobergrenze hat der ICS-Import nicht."),
        # Ein VEVENT hat keinen Erledigt-Zustand: STATUS kennt dort nur
        # TENTATIVE, CONFIRMED und CANCELLED. Der Code prueft ausschliesslich
        # CANCELLED, und VTODO ist ausdrücklich ausgeschlossen.
        (True, "geschätzten Aufwand übernehmen und erledigte beziehungsweise abgesagte Termine\n"
               "  überspringen.",
         "geschätzten Aufwand übernehmen und abgesagte Termine (`STATUS:CANCELLED`)\n"
         "  überspringen."),
        (True, "7. Die vier übernehmbaren Termine der RRULE-Tabelle erscheinen als "
               "Wiederholung, nicht\n   abbildbare Regeln werden verworfen und gezählt.",
         "7. Die vier übernehmbaren `FREQ`-Werte erscheinen – mit `INTERVAL` bei "
         "täglichen\n   und `BYDAY` bei wöchentlichen Regeln – als Glide-Wiederholung; "
         "nicht\n   abbildbare Regeln werden verworfen und gezählt."),
    ),
    f"{REPO_TEIL}/docs/44_KALENDERAUSGABE_3.20.0.md": (
        # Ein Planungstermin entsteht unabhaengig von der Faelligkeit: Die
        # Ausgabe ruft ics_event_lines(item, quelle, "planned", options) fuer
        # jeden Punkt auf, auch wenn der Faelligkeitstermin leer blieb. Nach
        # dem alten Wortlaut fiele genau der geplante, aber terminlose Punkt
        # heraus - der Fall, fuer den die Option gedacht ist.
        (True, "Grundlage ist die **Fälligkeit**: Ohne Fälligkeit gibt es keinen Termin – "
               "eine Aufgabe ohne\nDatum hat im Kalender keinen Platz. Aus jedem fälligen "
               "Punkt entsteht ein `VEVENT`:",
         "Grundlage des Fälligkeitstermins ist die **Fälligkeit**: Ohne Fälligkeit "
         "entsteht kein\nFälligkeitstermin. Aus jedem fälligen Punkt entsteht ein "
         "`VEVENT`; ein Punkt ohne\nFälligkeit, aber mit Bearbeitungstag erscheint bei "
         "zugeschalteter Option als\nPlanungstermin:"),
        (True, "Ausnahmeregeln. Punkte ohne Fälligkeit erscheinen nicht. Gruppen und "
               "Überschriften",
         "Ausnahmeregeln. Punkte ohne Fälligkeit erscheinen nur als Planungstermin, und "
         "nur\nwenn sie einen Bearbeitungstag tragen und die Option zugeschaltet ist. "
         "Gruppen und Überschriften"),
        # `DI` ist kein zulaessiges BYDAY-Token. ICS_WEEKDAYS im Code enthaelt
        # ausschliesslich MO, TU, WE, TH, FR, SA, SU.
        (True, "| an bestimmten Wochentagen | `FREQ=WEEKLY;BYDAY=MO,DI…` als "
               "`MO,TU,WE,TH,FR,SA,SU` |",
         "| an bestimmten Wochentagen | `FREQ=WEEKLY;BYDAY=MO,WE` – Glides Wochentage "
         "werden auf `MO,TU,WE,TH,FR,SA,SU` abgebildet |"),
        # SEQUENCE steht im Code fest auf 0 und steigt nie. Die Identitaet
        # traegt allein die stabile UID; ein Kalender erkennt daran denselben
        # Termin, eine neue Fassung erkennt er daran nicht.
        (True, "**aktualisiert** seine Termine statt sie zu verdoppeln, weil `UID` und "
               "`SEQUENCE` dem\nKalender sagen, dass es derselbe Termin in neuer Fassung ist.",
         "**aktualisiert** seine Termine statt sie zu verdoppeln, weil die `UID` dem "
         "Kalender\nsagt, dass es derselbe Termin ist. `SEQUENCE` steht dabei fest auf "
         "`0` und steigt\nnicht mit – Glide zeigt einem Kalender also nicht an, dass eine "
         "neue Fassung\nvorliegt; ob er den Termin ersetzt, entscheidet er selbst."),
    ),
    f"{REPO_TEIL}/docs/41_DRUCK_UND_PDF_3.17.0.md": (
        # Die mitgelieferten TTF-Dateien werden nur prozesslokal registriert
        # (FR_PRIVATE unter Windows, Prozessumfang unter macOS). Das
        # Anzeigeprogramm der Druckdatei sieht sie nicht, und die Datei enthaelt
        # ausdruecklich keine Web-Schrift.
        (True, "Die Schriftwahl beginnt bei der\nmitgelieferten DejaVu Sans und fällt auf "
               "Systemschriften zurück.",
         "Die Schriftliste beginnt bei DejaVu Sans,\nsofern sie im System installiert "
         "ist, und fällt auf Systemschriften zurück. Die\nmitgelieferten Schnitte werden "
         "nur prozesslokal für Glides eigene Oberfläche\nregistriert; das Anzeigeprogramm "
         "der Druckdatei sieht sie nicht."),
    ),
    # ============================ B. Ueberholte Formatstufen ==============
    "01_Repository/Glide/SECURITY.md": (
        (True, "akzeptiert die Formate 4 bis 12 (`MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis "
               "`DATA_SCHEMA_VERSION`)",
         "akzeptiert " + FORMATBEREICH),
    ),
    f"{REPO_TEIL}/docs/06_DATA_BACKUP_MIGRATION.md": (
        (True, "Formate 4–14 und Legacy 2 bleiben lesbar. Glide 3.13 und ältere Versionen "
               "können Format 14 nicht lesen.",
         "Formate 4–15 und Legacy 2 bleiben lesbar. Glide 3.13 und ältere Versionen "
         "können Format 14 nicht lesen, Glide 3.18 und ältere nicht Format 15."),
    ),
    f"{REPO_TEIL}/docs/decisions/PRODUCT_IDENTITY.md": (
        (True, "| App-Version | 3.14.0 | `APP_VERSION`, `VERSION` |",
         f"| App-Version | {NEU} | `APP_VERSION`, `VERSION` |"),
        (True, "| Datenformat | 13 | `DATA_SCHEMA_VERSION` |",
         "| Datenformat | 15 | `DATA_SCHEMA_VERSION` |"),
        (True, "| Unterstützte Backup-Formate | 4 bis 13 | "
               "`MIN_PORTABLE_BACKUP_SCHEMA_VERSION`, `DATA_SCHEMA_VERSION` |",
         "| Unterstützte Backup-Formate | 4 bis 15 | "
         "`MIN_PORTABLE_BACKUP_SCHEMA_VERSION`, `DATA_SCHEMA_VERSION` |"),
        (True, "| Beispielbestand zum Einlesen | aktuelles Format-13-Fixture unter "
               "`tests/fixtures/beispiele/` | `pruefen.py`, `test_release36.py` |",
         "| Beispielbestand zum Einlesen | aktuelles Format-15-Fixture unter "
         "`tests/fixtures/beispiele/`, feste Referenz `current_v15` | `pruefen.py`, "
         "`test_release36.py` |"),
        # Erinnerungen kamen mit Format 13 (3.8.0), nicht mit 14.
        (True, "Format 14: lokale Erinnerungen mit Originalsicherung.",
         "Format 13: lokale Erinnerungen mit Originalsicherung."),
        (True, "Aufgabenformat 14 bleibt unverändert; Aufgabenbackups transportieren "
               "diese Ansichten nicht.",
         "Aufgabenformat 13 bleibt unverändert; Aufgabenbackups transportieren "
         "diese Ansichten nicht."),
        (True, "Die Einstellungen bleiben Format 2, Aufgabenformat 14 ergänzt "
               "Bearbeitungstag und geschätzten Aufwand.",
         "Die Einstellungen bleiben Format 2; das Aufgabenformat bleibt bis 3.13 bei 13, "
         "erst 3.14 ergänzt mit Format 14 Bearbeitungstag und geschätzten Aufwand."),
    ),
    f"{REPO_TEIL}/docs/27_VORLAGEN_PRAXISANLEITUNG.md": (
        (True, "Aktuelle Teilpayloads verwenden Format 14 und benötigen Glide ab 3.14.",
         "Aktuelle Teilpayloads verwenden Aufgabenformat 15 und benötigen Glide ab 3.19; "
         "das Vorlagenformat selbst bleibt 2."),
    ),
    # ============================ C. Gegenwart in historischen Dokumenten =
    f"{REPO_TEIL}/docs/08_CODE_BEFUND.md": (
        (True, "Dieses Dokument beschreibt den aktuellen lokalen Python-/Tk-Quellstand.",
         "Dieses Dokument beschreibt den damaligen Quellstand von 3.7.0."),
    ),
    f"{REPO_TEIL}/docs/25_FEATURE_ABGLEICH_3.7.0.md": (
        (True, "den geprüften 3.13-Stand mit siebzehn Testsuiten nach; für 3.14.0 mit "
               "achtzehn",
         "damals den geprüften 3.13-Stand mit siebzehn Testsuiten nach; der Lauf zu "
         "3.14.0 mit achtzehn"),
    ),
    f"{REPO_TEIL}/docs/12_ABSCHLUSSBERICHT.md": (
        (True, "Nächste Schritte: native Abnahme der ersten Stufe, danach Entwurf der",
         "Nächste Schritte damals – Reiteransicht und Pinnwand sind seit 3.10.0 "
         "umgesetzt: native Abnahme der ersten Stufe, danach Entwurf der"),
    ),
    f"{REPO_TEIL}/docs/28_ABLAGEPRUEFUNG_2026-09-11.md": (
        (True, "- In `05_Probelisten_Testdaten` liegen inzwischen die aktuellen "
               "Aufgabenbackups",
         "- In `05_Probelisten_Testdaten` lagen damals die Aufgabenbackups"),
    ),
    f"{REPO_TEIL}/docs/30_DOKUMENTATIONSABGLEICH_2026-09-12.md": (
        (True, "Die Chatweitergabe und das aktuelle Produktdatenblatt verweisen inzwischen "
               "auf",
         "Die Chatweitergabe und das Produktdatenblatt verwiesen damals auf"),
    ),
    f"{REPO_TEIL}/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md": (
        (True, "2. Reiteransicht angehen, wie in der Reihenfolge vorgesehen; sie hängt an",
         "2. Reiteransicht – **umgesetzt in 3.10.0**; sie hing an"),
    ),
    "50_Ablage/QA/Dokumentation/README.md": (
        (True, "Die aktuelle App-Prüfung liegt unter `01_Repository/Glide/tests/qa-3.13.0/`.",
         "Die laufende App-Prüfung weist der "
         "[QA-Bericht](../../../01_Repository/Glide/docs/07_QA_BERICHT.md) nach; der "
         "Protokollordner trägt jeweils die geprüfte Version."),
        (True, "Der aktuelle Word-Bericht 3.7 ist inhaltlich erstellt. Seine Layoutprüfung ist",
         "Der damalige Word-Bericht 3.7 war inhaltlich erstellt; seine Layoutprüfung war"),
        (True, "Dokumentprüfungen und werden nicht nachträglich auf 3.13 umetikettiert.",
         "Dokumentprüfungen und werden nicht nachträglich auf den jeweils aktuellen "
         "Stand umetikettiert."),
    ),
    # ============================ D. Verweise und Widersprueche ===========
    "40_Store_Material/Apple/Store_Angaben_Apple.md": (
        (True, "Ausformulierbare Texte: [Produktdatenblatt](../README.md).",
         f"Ausformulierbare Texte: [Produktdatenblatt](../Produktdatenblatt_{NEU}.md)."),
        # 3.14.0 trägt Aufgabenformat 14; die Paarung mit Format 13 stammt aus
        # einem falschen Literal im Releaseerzeuger und ist unmöglich.
        (True, "auf Grundlage von Glide 3.14.0 / Datenformat 13 erhoben.",
         "auf Grundlage von Glide 3.14.0 / Aufgabenformat 14 erhoben."),
    ),
    "40_Store_Material/Microsoft/Store_Angaben_Microsoft.md": (
        (True, "| Texte/Features | [Produktdatenblatt](../README.md) |",
         f"| Texte/Features | [Produktdatenblatt](../Produktdatenblatt_{NEU}.md) |"),
        (True, "auf Grundlage von Glide 3.14.0 / Datenformat 13 erhoben.",
         "auf Grundlage von Glide 3.14.0 / Aufgabenformat 14 erhoben."),
    ),
    "20_Grafik_Master/README.md": (
        (True, "Store-Assets stehen im [aktuellen Produktdatenblatt]"
               "(../40_Store_Material/README.md)",
         "Store-Assets stehen in den Store-Angaben für "
         "[Apple](../40_Store_Material/Apple/Store_Angaben_Apple.md) und "
         "[Microsoft](../40_Store_Material/Microsoft/Store_Angaben_Microsoft.md)"),
    ),
    "30_Release_Exports/README.md": (
        (True, "[Bedienung und Änderungen](../01_Repository/Glide/docs/"
               "36_TABELLENANSICHT_3.13.0.md).",
         "[Jüngste Bedienergänzung](../01_Repository/Glide/docs/"
         "45_KALENDERIMPORT_3.21.0.md) · [Tabellenansicht 3.13]"
         "(../01_Repository/Glide/docs/36_TABELLENANSICHT_3.13.0.md)."),
        (True, "Die 3.13-Arbeitskopie ergänzt die Tabellenansicht mit listenspezifischen "
               "Spalten",
         "Die aktuelle Arbeitskopie führt den Funktionsbestand bis zum Kalenderimport "
         "aus ICS"),
    ),
    "07_Python-Versionen/README.md": (
        (True, "Neu: Die Tabellenansicht zeigt Aufgaben kompakt in wählbaren Spalten je "
               "Liste.",
         "Seit 3.13: Die Tabellenansicht zeigt Aufgaben kompakt in wählbaren Spalten je "
         "Liste."),
    ),
    "50_Ablage/README.md": (
        (True, "- `10_Dokumentation` enthält die aktuelle Word-Arbeitsgrundlage und ihre "
               "historischen Fassungen.",
         "- `10_Dokumentation` enthält die aktuelle Markdown-Dokumentation; die früheren "
         "Word-Berichte liegen dort im `Archiv/`."),
        (True, "Für den Nachweis genügt der",
         "Renderläufe bleiben vollständig erhalten, auch identische Zwischenstände; "
         "gelöscht wurde keiner. Für den Nachweis genügt beim Lesen der"),
    ),
    "00_Arbeitsvorbereitung/README.md": (
        (True, "[Aktuelle Funktionsübersicht](Glide_Funktionsvorschlaege_2026-09-11.md) ·",
         "[Funktionsvorschläge und Prioritäten](Glide_Funktionsvorschlaege_2026-09-11.md) ·"),
    ),
    "10_Dokumentation/README.md": (
        (True, "[Aktuelle Funktionsübersicht](../00_Arbeitsvorbereitung/"
               "Glide_Funktionsvorschlaege_2026-09-11.md) ·",
         "[Funktionsvorschläge und Prioritäten](../00_Arbeitsvorbereitung/"
         "Glide_Funktionsvorschlaege_2026-09-11.md) ·"),
    ),
    "00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md": (
        (True, "| Dauerhafter Änderungsverlauf | Änderungen und frühere Werte gezielt "
               "nachvollziehen; ergänzt das vorhandene Rückgängig innerhalb einer "
               "Sitzung. |",
         "| Dauerhafter Änderungsverlauf | **Umgesetzt in 3.19.0:** Änderungen und "
         "frühere Werte gezielt nachvollziehen; ergänzt das vorhandene Rückgängig "
         "innerhalb einer Sitzung. [Bedienvertrag]"
         "(../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md). |"),
    ),
    # ============================ E. Produktdatenblatt ====================
    f"40_Store_Material/Produktdatenblatt_{NEU}.md": (
        (True, "| Ansichten | Liste, kompakte Tabellenansicht mit wählbaren Spalten, "
               "„Mein Tag“, Tagesplanung mit Aufwandssumme und Tageskapazität, Reiter "
               "und Pinnwand |",
         "| Ansichten | Liste, kompakte Tabellenansicht mit wählbaren Spalten, "
         "„Mein Tag“, Tagesplanung mit Aufwandssumme und Tageskapazität, Reiter, "
         "Pinnwand und Startseite mit Ordner- und Listenkacheln |"),
        (True, f"Der maßgebliche Lauf zu 3.21.2 bestand am {DATUM}",
         f"Der maßgebliche Lauf zu {NEU} bestand am {DATUM}"),
        (True, "auf macOS mit Python 3.14.5 mit Exitcode 0: 25 Suiten, statische Analysen "
               "sowie\nBeispiel- und Releaseabgleich.",
         "auf macOS mit Python 3.14.5 mit Exitcode 0: 25 Suiten, drei Analysen sowie\n"
         "Beispiel- und Releaseabgleich."),
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


def unterschiede(kurz: str, alt: str, neu: str) -> list[str]:
    """Geänderte Zeilen im Wortlaut. Ein verfälschtes Zitat fällt nur auf,
    wenn man es liest: „Glide 3.21.1 · Aufgabenformat 15“ wurde in 3.21.2 von
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
        # Der Durchgang hob „Bis 3.21.2 stand derselbe Satz dreimal darin“ und
        # „Der maßgebliche 3.21.2-Lauf“ auf die neue Version - und hätte damit
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



# ------------------------------------------------------------------ Weitergabe
WEITERGABE_KOPF = (
    f"Neu in {NEU}: Ein vollständiger Durchgang durch alle 93 aktiven Dokumente hat "
    "zwölf sachlich falsche Aussagen über den Anwendungscode gefunden – darunter einen "
    "erfundenen Dateinamen, eine Grenze, die es nicht gibt, ein ungültiges "
    "`BYDAY`-Beispiel und die Zusage, die Kalenderausgabe zeige einem Kalender eine "
    "neue Fassung an (`SEQUENCE` steht fest auf `0`). Alle behoben. Die Standprüfung "
    "prüft jetzt auch die Formatstufen gegen `DATA_SCHEMA_VERSION`. Anwendungscode "
    "unverändert. [Prüfungen und Umfang](../01_Repository/Glide/tests/README.md)."
)

WEITERGABE_PRUEFSTAND = (
    "Prüfstand: 3.15.0 bis 3.18.0, **3.21.1**, **3.21.2** und **3.21.3** sind "
    "automatisiert abgenommen (macOS/Python 3.14.5, Exitcode 0). Der 3.21.3-Lauf vom "
    "14.09.2026 um 20:45 umfasst **neununddreißig Schritte, siebenunddreißig "
    "ausgeführt**: `tests/qa-3.21.3/abschluss/ergebnis.json`; übersprungen blieben allein "
    "die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Der Lauf zu "
    "3.21.0 war fehlgeschlagen (Exitcode 1, drei Schritte) – zwei Zeitzonenfehler im "
    "ICS-Rundlauf und ein Fehler im Fixture-Abgleich, der seit 3.19 nie grün werden "
    "konnte; beide Ursachen sind in 3.21.1 behoben, der Beleg bleibt als "
    "`tests/qa-3.21.0/abschluss`. Für 3.19.0 und 3.20.0 wurden keine eigenen macOS-Läufe "
    f"nachgeholt; sie sind im 3.21.1-Lauf enthalten. Für {NEU} sind alle fünfundzwanzig "
    "Suiten und die drei Analysen in der Linux-Vorabumgebung unter `TZ=Europe/Berlin` "
    "mit Exitcode 0 gelaufen – ausgenommen der Dokumentationsindex, weil die Dokumente "
    "dort nicht mitkopiert sind. Der maßgebliche macOS-Lauf steht aus: `python3 "
    f"tests/tools/pruefen.py --modus voll --protokoll tests/qa-{NEU}/abschluss`. Offen "
    "bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, "
    "Screenreader, Langzeitbetrieb, Installer und Signierung."
)

WEITERGABE_EINSCHUB = (
    f"Datenregeln von {NEU}: Kein Formatsprung, kein neues Feld, keine Änderung am "
    "Anwendungscode. `standpruefung.py` prüft zusätzlich die **Formatstufen**: Eine "
    "Formatangabe in einer Standzeile muss `DATA_SCHEMA_VERSION` entsprechen (R6), ein "
    "Formatbereich muss von `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis dorthin reichen "
    "(R7), und eine Tabellenzeile „Datenformat“ oder „App-Version“ nennt die aktuellen Werte "
    "(R8). Die Werte liest das Werkzeug über den Syntaxbaum aus `app.pyw` – ein Import "
    "würde Tk starten und den echten Nutzerdatenordner anfassen. Der Änderungsverlauf "
    "ist von der Formatprüfung ausgenommen: Dort war „Formate 2 bis 9“ damals richtig. "
    "`tests/tools/README.md` und `src/glide/README.md` werden seit 3.21.4 mit dem "
    "Quellstand ausgeliefert, zusammen mit den beiden Testberichten aus 3.21.3.\n\n"
)

WEITERGABE_FALLE = (
    "- **Eine Zahl im Zweck einer Werkzeugtabelle rottet.** `tests/tools/README.md` "
    "beschrieb den Vollprüflauf als \u201eAchtzehn Suiten\u201c, den Beispielerzeuger "
    "als \u201eFormat 14\u201c und die Releaseplanung als \u201efür 3.14\u201c \u2013 "
    "drei Angaben, die bei jedem Stand hätten mitgehen müssen. Zwecke ohne Zahl "
    "formulieren und die Zahl im Quelltext an eine Konstante binden.\n"
    "- **Eine Formatstufe gehört nicht in Prosa.** Fünf Dokumente trugen eine überholte: "
    "`SECURITY.md` \u201eFormate 4 bis 12\u201c, `06_DATA_BACKUP_MIGRATION.md` "
    "\u201eFormate 4\u201315\u201c, `PRODUCT_IDENTITY.md` vier Werte auf Format 13 "
    "und App-Version 3.14.0. Seit 3.21.4 prüft `standpruefung.py` das gegen den Code.\n"
    "- **Ein Linktext muss halten, was er verspricht.** An vier Stellen zeigte "
    "\u201eProduktdatenblatt\u201c auf den Ordner-README, an zwei Stellen hieß eine "
    "Vorschlagsliste \u201eAktuelle Funktionsübersicht\u201c. Ein Linktext, der etwas "
    "anderes verspricht als sein Ziel, führt jeden externen Agenten in die Irre.\n"
    "- **Ein historisches Dokument darf keine Gegenwart behaupten.** Sieben solche Sätze "
    "standen in Dokumenten, die als historisch gekennzeichnet sind \u2013 vom "
    "\u201eaktuellen Quellstand\u201c bis zu \u201eNächste Schritte: \u2026 "
    "Reiteransicht\u201c, die seit 3.10.0 umgesetzt ist. Präteritum verwenden oder die "
    "Umsetzung benennen.\n"
)

WEITERGABE_ABLAGEWEG = (
    "8. Nach dem Prüflauf das Ergebnis in QA-Bericht, Weitergabe und Technische Fakten "
    "**derselben** Version eintragen. Bis 3.21.2 stand es immer erst in den Dokumenten "
    "der nächsten Version – dadurch behauptete jeder Stand, sein eigener Prüflauf stehe "
    "noch aus."
)

# --------------------------------------------------------------- QA-Bericht
QA_ALTE_ZUSAGE = (
    "Der maßgebliche macOS-Lauf steht aus: `python3 tests/tools/pruefen.py --modus voll "
    f"--protokoll tests/qa-{ALT}/abschluss`. Sein Ergebnis wird hier ergänzt."
)
QA_NEUE_ZUSAGE = (
    "Der maßgebliche Abschlusslauf bestand auf macOS mit Python 3.14.5 am 14.09.2026 um "
    f"20:45 mit **Exitcode 0**: [Abschlusslauf {ALT}](../tests/qa-{ALT}/abschluss/ergebnis.json). "
    "Von neununddreißig Schritten wurden siebenunddreißig ausgeführt; übersprungen "
    "blieben allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. "
    f"Automatisiert ist {ALT} damit abgenommen – einschließlich der neuen Standprüfung, "
    "die 93 aktive Dokumente ohne Befund durchlief."
)

QA_ANKER = f"Für {ALT} sind alle fünfundzwanzig Suiten"

QA_NEUER_ABSATZ = f"""Für {NEU} sind alle fünfundzwanzig Suiten, die drei Analysen sowie Vorlagen-, Beispiel- und Releasedaten in einer Linux-Vorabumgebung (Python 3.12.3, Tk 8.6 unter Xvfb, `TZ=Europe/Berlin`) mit Exitcode 0 gelaufen; ausgenommen blieb dort allein der Dokumentationsindex, weil die Dokumente in der Arbeitskopie nicht mitliegen. {NEU} ändert keinen Anwendungscode außer der Versionsangabe. Es ist ein Korrekturstand: Ein vollständiger Durchgang durch **alle 93 aktiven Dokumente** hat Befunde ergeben, die keine maschinelle Prüfung finden konnte. Zwölf davon sind sachlich falsche Aussagen über den Anwendungscode, gegen `src/glide/app.pyw` geprüft – der Änderungsverlauf nannte die Nutzdatendatei `glide_liste.json` statt `liste_speicher.json`; der ICS-Import führte eine Zeilenobergrenze, die es nicht gibt, und behauptete, erledigte Termine zu überspringen, obwohl ein `VEVENT` keinen Erledigt-Zustand kennt; die Kalenderausgabe schloss Punkte ohne Fälligkeit aus, obwohl ein Bearbeitungstag auch ohne Fälligkeit einen Planungstermin erzeugt, zeigte `BYDAY=MO,DI` als Ausgabe, obwohl `DI` kein zulässiges Token ist, und stützte die Aktualisierung im Kalender auf `SEQUENCE`, das im Code fest auf `0` steht; die Druckausgabe versprach die mitgelieferte DejaVu Sans, die nur prozesslokal registriert ist und dem Anzeigeprogramm deshalb nicht zur Verfügung steht. Fünf Dokumente trugen eine überholte Formatstufe, acht Verweise zeigten auf ein anderes Ziel als ihr Linktext, und sieben als historisch gekennzeichnete Dokumente behaupteten eine Gegenwart. Vier Zählfehler aus 3.21.3 sind ebenfalls berichtigt. Neu sind die Regeln R6 bis R8 der Standprüfung: Formatstufe, Formatbereich und Formattabellenzeilen gehen gegen `DATA_SCHEMA_VERSION` und `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` aus dem Anwendungscode – drei der fünf Formatbefunde hätte das mechanisch gefunden. Der maßgebliche macOS-Lauf steht aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-{NEU}/abschluss`. Sein Ergebnis wird hier ergänzt.

"""


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
        lauf.fehler.append(f"07_QA_BERICHT.md: die Zusage zum ausstehenden {ALT}-Lauf "
                           "steht nicht im erwarteten Wortlaut")
        return
    neu = neu.replace(QA_ALTE_ZUSAGE, QA_NEUE_ZUSAGE, 1)
    if QA_ANKER not in neu:
        lauf.fehler.append(f"07_QA_BERICHT.md: Anker \"{QA_ANKER}\" fehlt")
        return
    neu = neu.replace(QA_ANKER, QA_NEUER_ABSATZ + QA_ANKER, 1)
    neu = neu.replace(f"# QA-Bericht – Glide {ALT}", f"# QA-Bericht – Glide {NEU}", 1)
    neu = neu.replace(f"Stand {DATUM} · Glide {ALT} · macOS · Python 3.14.5",
                      f"Stand {DATUM} · Glide {NEU} · macOS · Python 3.14.5", 1)
    lauf.setze(rel, neu)


def projektuebergabe(lauf: Lauf) -> None:
    """Eigener Abschnitt je Folgestand. Ohne ihn stünde 3.21.4 nirgends in dem
    Dokument, das ein externer Agent als erstes liest."""
    rel = f"{REPO_TEIL}/docs/09_PROJECT_HANDOFF.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    if f"**{NEU}**" in alt:
        lauf.hinweise.append(f"Projektübergabe: Abschnitt {NEU} steht schon drin")
        return
    anker = "## Bestand aus den Vorgängerständen"
    if anker not in alt:
        lauf.fehler.append(f"09_PROJECT_HANDOFF.md: Anker {anker!r} fehlt")
        return
    absatz = (
        f"**{NEU}** ist ein Korrekturstand aus einem vollständigen Durchgang durch alle "
        "93 aktiven Dokumente: zwölf sachlich falsche Aussagen über den Anwendungscode, "
        "fünf überholte Formatstufen, acht falsche Verweise und sieben "
        "Gegenwartsbehauptungen in historischen Dokumenten. Für die Technik am "
        "wichtigsten: Die Kalenderausgabe erzeugt aus einem Bearbeitungstag **auch ohne "
        "Fälligkeit** einen Planungstermin – der Bedienvertrag schloss das aus –, und "
        "`SEQUENCE` steht fest auf `0`, die Termin-Identität trägt allein die stabile "
        "`UID`. `standpruefung.py` prüft seit diesem Stand auch Formatstufen gegen "
        "`DATA_SCHEMA_VERSION`. Bei Änderungen besonders prüfen: dass eine Formatstufe "
        "nicht als Literal in Prosa wandert, sondern aus dem Code kommt. Anwendungscode "
        f"unverändert. [Prüfungen und Umfang](../tests/README.md).\n\n"
    )
    lauf.setze(rel, alt.replace(anker, absatz + anker, 1))


# ------------------------------------------------------- Änderungsverlauf
# Vier Zahlen im 3.21.3-Eintrag waren falsch, und die einzige inhaltliche
# Korrektur dieses Stands fehlte darin. Ein Änderungsverlauf, der einen Stand
# falsch beschreibt, ist schlimmer als einer, der ihn knapp beschreibt: Er wird
# von jedem späteren Leser als Beleg genommen.
CHANGELOG_KORREKTUR = (
    (True, "Neu dokumentiert: Die **neunzehn versionierten Releaseplanungen**",
     "Neu dokumentiert: Die **zwanzig versionierten Releaseplanungen**"),
    (True, "In `07_Python-Versionen` lagen **neun \u00fcberholte startbare Fassungen** "
           "(3.14.0 bis 3.21.2)",
     "In `07_Python-Versionen` lagen **zehn \u00fcberholte startbare Fassungen** "
     "(3.14.0 bis 3.21.2)"),
    (True, "Alle sechs Dokumente tragen jetzt denselben Satz \u00fcber die durchgehende "
           "Grundlage",
     "Wurzel-README, Repository-README, Projekt\u00fcbergabe und Weitergabe tragen "
     "jetzt denselben Satz \u00fcber die durchgehende Grundlage; Produktdatenblatt und "
     "Probelisten-README f\u00fchren ihre eigene Funktionstabelle"),
    (True, "- Anwendungscode unver\u00e4ndert: keine \u00c4nderung an "
           "`src/glide/app.pyw` au\u00dfer der Versionsangabe. Aufgabenformat bleibt 15, "
           "Einstellungen 2, Vorlagen 2. Unver\u00e4ndert 25 Suiten; die Analysen "
           "wachsen von zwei auf drei, der Vollpr\u00fcflauf von achtunddrei\u00dfig "
           "auf neununddrei\u00dfig Schritte. Keine neue Laufzeitabh\u00e4ngigkeit.",
     "- `tests/tools/beispieldaten.py` legte die Liste \u201eKalender, Erinnerungen und "
     "Tagesplanung\u201c mit `color=\"due_soon\"` an. Der Wert steht nicht in "
     "`LIST_COLOR_KEYS`; die App verwirft eine unbekannte Farbe still, die Liste hatte "
     "deshalb seit 3.21.2 **keine Farbe**. Der Fixture-Abgleich kann das nicht finden "
     "\u2013 die Neuerzeugung verwirft denselben Wert genauso. Jetzt `import` (Braun), "
     "und der `Builder` bricht bei unbekannter Farbe ab.\n"
     "- Anwendungscode unver\u00e4ndert: keine \u00c4nderung an `src/glide/app.pyw` "
     "au\u00dfer der Versionsangabe. Aufgabenformat bleibt 15, Einstellungen 2, "
     "Vorlagen 2. Unver\u00e4ndert 25 Suiten; die Analysen wachsen von zwei auf drei, "
     "der Vollpr\u00fcflauf von achtunddrei\u00dfig auf neununddrei\u00dfig Schritte. "
     "Keine neue Laufzeitabh\u00e4ngigkeit."),
)


def changelog_korrektur(lauf: Lauf) -> None:
    rel = f"{REPO_TEIL}/CHANGELOG.md"
    alt = lauf.lese(rel)
    if alt is None:
        lauf.fehler.append(f"Datei fehlt: {rel}")
        return
    neu = alt
    for pflicht, muster, ersatz in CHANGELOG_KORREKTUR:
        if ersatz in neu:
            continue
        if muster in neu:
            neu = neu.replace(muster, ersatz, 1)
        elif pflicht:
            lauf.fehler.append(f"CHANGELOG.md: Korrekturstelle fehlt – {muster[:70]!r}")
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

    anfang = neu.find("Prüfstand: 3.15.0 bis 3.18.0")
    if anfang < 0:
        lauf.fehler.append("Weitergabe: Prüfstandsabsatz fehlt")
        return
    ende = neu.find("\n\n", anfang)
    neu = neu[:anfang] + WEITERGABE_PRUEFSTAND + neu[ende:]

    anker = f"Datenregeln von {ALT}:"
    if anker not in neu:
        lauf.fehler.append(f"Weitergabe: Anker {anker!r} fehlt")
        return
    neu = neu.replace(anker, WEITERGABE_EINSCHUB + anker, 1)

    falle_anker = "- **Ein von Hand gepflegtes Banner"
    if falle_anker not in neu:
        lauf.fehler.append("Weitergabe: Fallenliste fehlt")
        return
    neu = neu.replace(falle_anker, WEITERGABE_FALLE + falle_anker, 1)

    schritt7 = "7. Diese Weitergabe fortschreiben und als Projektdokument hochladen."
    if WEITERGABE_ABLAGEWEG not in neu:
        if schritt7 not in neu:
            lauf.fehler.append("Weitergabe: Schritt 7 des Ablagewegs fehlt")
            return
        neu = neu.replace(schritt7, schritt7 + "\n" + WEITERGABE_ABLAGEWEG, 1)

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
    projektuebergabe(lauf)
    changelog_korrektur(lauf)
    weitergabe(lauf)
    changelog(lauf, quelle / "changelog_3214.md")
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
