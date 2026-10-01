# Glide – kompakte Weitergabe an einen neuen Chat

Stand 13.09.2026 · Entwicklungsstand 3.12.0 · Aufgabenformat 13

Die priorisierten Reiter, die erste Pinnwand, Schnellerfassung/Filter und die bewusste Tagesauswahl „Mein Tag“ sind umgesetzt. „Mein Tag“ stellt Aufgaben aus mehreren Listen für den aktuellen Tag zusammen, ohne Fälligkeiten zu verändern; die Auswahl liegt als persönliche Einstellung vor und wird am Tageswechsel geleert. Alle Ansichten zeigen dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.12.0.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

[Bedienung 3.12](../01_Repository/Glide/docs/35_MEIN_TAG_3.12.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren.

Nächste Idee: Tabellenansicht für kompakte Mehrfachbearbeitung bewerten; größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md).
