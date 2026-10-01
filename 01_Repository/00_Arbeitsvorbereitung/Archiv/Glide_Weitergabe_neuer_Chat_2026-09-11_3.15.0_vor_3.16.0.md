# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.15: Die Ansicht „Tagesplanung“ zeigt alle Aufgaben mit Bearbeitungstag an einem wählbaren Tag und stellt ihren geschätzten Aufwand einer selbst gesetzten Tageskapazität gegenüber. Summen erscheinen auch in „Mein Tag“, in der Tabelle und auf der Startseite. Keine Zeiterfassung und keine automatische Terminverteilung. [Bedienung und Datenregeln](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

Stand 13.09.2026 · Entwicklungsstand 3.15.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner `00_Arbeitsvorbereitung` der Arbeitsablage.

Umgesetzt sind Erinnerungen mit Dock-/Taskleistenaufmerksamkeit, Reiter und Pinnwand, Schnellerfassung und gespeicherte Filter, „Mein Tag“, die Tabellenansicht mit listenspezifischen Spalten, Bearbeitungstag und Aufwand sowie die Tagesplanung mit Tageskapazität. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.15.0.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand: 3.15.0 ist automatisiert abgenommen – Gesamtlauf auf macOS/Python 3.14.5 vom 13.09.2026 mit Exitcode 0, neunzehn Suiten, zwei statische Analysen, Beispiel- und Releaseabgleich (`tests/qa-3.15.0/abschluss/ergebnis.json`). Offen bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und Signierung.

[Bedienung 3.15](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) · [Bedienung 3.14](../01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Datenregeln von 3.15: `planning_summary` ist die einzige Rechenstelle für alle Aufwandssummen; gezählt werden nur Aufgaben und Long-Tasks, Punkte ohne Schätzung getrennt, erledigte bleiben in der Summe. Die Tageskapazität liegt additiv als `daily_capacity_minutes` (0–1440, Vorgabe 0 = kein Vergleich) in den Einstellungen, der betrachtete Tag nur im Laufzeitzustand. Aufgabenformat 14 bleibt unverändert; Backups enthalten weder Kapazität noch Ansichtszustand.

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren.

Nächste offene Idee: vollständiges App-Backup mit Inhaltsvorschau; danach dauerhafter Änderungsverlauf und Druck/PDF. Größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md).
