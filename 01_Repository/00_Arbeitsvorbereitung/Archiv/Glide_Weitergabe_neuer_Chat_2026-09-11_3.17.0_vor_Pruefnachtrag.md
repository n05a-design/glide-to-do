# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.17: Druck- und PDF-Ausgabe für Tageszettel, Liste oder Ordner, Tagesplanung und Checkliste zum Abhaken. Glide erzeugt eine eigenständige HTML-Druckansicht und öffnet sie im Standardprogramm; dessen Druckdialog liefert Papier oder PDF. [Bedienung und Datenregeln](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md).

Stand 13.09.2026 · Entwicklungsstand 3.17.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner `00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“, die Tabellenansicht mit listenspezifischen Spalten, Bearbeitungstag und Aufwand, die Tagesplanung mit Tageskapazität das vollständige App-Backup mit Inhaltsvorschau sowie die Druck- und PDF-Ausgabe. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.17.0.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand: 3.15.0 ist automatisiert abgenommen (macOS/Python 3.14.5, Exitcode 0, neunzehn Suiten, `tests/qa-3.15.0/abschluss/ergebnis.json`). 3.16.0 ist ebenfalls abgenommen (zwanzig Suiten, `tests/qa-3.16.0/abschluss/ergebnis.json`). Für 3.17.0 sind alle einundzwanzig Suiten in einer Linux-Vorabumgebung mit Exitcode 0 gelaufen; der maßgebliche macOS-Lauf steht noch aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.17.0/abschluss`. Offen bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und Signierung.

[Bedienung 3.17](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md) · [Bedienung 3.16](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md) · [Bedienung 3.15](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) · [Bedienung 3.14](../01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Datenregeln von 3.17: Die Druckausgabe liest nur vorhandene Objekte, schreibt ausschließlich HTML an ein gewähltes Ziel oder in den temporären Ordner und verändert weder Aufgaben noch Einstellungen; Nutzdatendateien sind als Ziel ausgeschlossen, die Obergrenze liegt bei 2000 Punkten.

Datenregeln von 3.16: Das App-Backup ist dasselbe ZIP wie ein Komplettbackup, ergänzt um den JSON-Abschnitt `app_backup` (`settings` ohne Tageshistorien, `templates`, `activity`). Ältere Fassungen lesen die Datei weiterhin als Aufgabenbackup. Aufgaben laufen beim Wiederherstellen durch `import_full_backup`; vor dem Ersetzen entstehen `vor_import_*.glidebackup`, `settings_vor_restore_*.json` und `vorlagen_vor_restore_*.json`. Ansichtsverweise werden nur zusammen mit den Aufgaben desselben Archivs übernommen.

Datenregeln von 3.15: `planning_summary` ist die einzige Rechenstelle für alle Aufwandssummen; gezählt werden nur Aufgaben und Long-Tasks, Punkte ohne Schätzung getrennt, erledigte bleiben in der Summe. Die Tageskapazität liegt additiv als `daily_capacity_minutes` (0–1440, Vorgabe 0 = kein Vergleich) in den Einstellungen, der betrachtete Tag nur im Laufzeitzustand. Aufgabenformat 14 bleibt unverändert; Backups enthalten weder Kapazität noch Ansichtszustand.

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren.

Nächste offene Ideen: dauerhafter Änderungsverlauf, CSV-Import mit Spaltenzuordnung und benutzerdefinierte Felder. Größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md).
