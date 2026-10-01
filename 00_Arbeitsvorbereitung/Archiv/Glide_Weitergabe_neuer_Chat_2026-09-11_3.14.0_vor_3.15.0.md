# Glide – kompakte Weitergabe an einen neuen Chat

Neu in 3.14: freiwilliger Bearbeitungstag und geschätzter Aufwand in Minuten, getrennt von Fälligkeit und „Mein Tag“. Beide Angaben stehen in Punktdetails, Mehrfachbearbeitung, Tabelle und Reitern und werden in Backups und Vorlagen mitgeführt. [Bedienung und Datenregeln](../01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md).

Stand 13.09.2026 · Entwicklungsstand 3.14.0 · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner `00_Arbeitsvorbereitung` der Arbeitsablage.

Die priorisierten Reiter, die erste Pinnwand, Schnellerfassung/Filter, „Mein Tag“ und die Tabellenansicht sind umgesetzt. Die Tabelle stellt Aufgaben flach dar, übernimmt Filter und Punktaktionen und speichert die sichtbaren Spalten je Liste in den persönlichen Einstellungen. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.14.0.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

Prüfstand: Der Vollmodus-Lauf vom 13.09.2026 bestand mit Exitcode 0 – achtzehn Suiten, zwei statische Analysen, Beispiel- und Releaseabgleich. Automatisiert ist 3.14.0 damit abgenommen. Offen bleiben die native Sichtabnahme auf macOS und Windows, DPI-/Mehrmonitorprofile, Screenreader, Langzeitbetrieb, Installer und Signierung. Alle aktiven Dokumente sind am 13.09.2026 auf diesen Stand abgeglichen ([Protokoll](../01_Repository/Glide/docs/38_DOKUMENTATIONSABGLEICH_2026-09-13.md)).

[Bedienung 3.14](../01_Repository/Glide/docs/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [Bedienung 3.13](../01_Repository/Glide/docs/36_TABELLENANSICHT_3.13.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren.

Bearbeitungstag und Aufwand sind in 3.14 umgesetzt. Nächste offene Idee: vollständiges App-Backup mit Inhaltsvorschau; größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md).
