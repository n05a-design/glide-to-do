# Glide – kompakte Weitergabe an einen neuen Chat

Stand 13.09.2026 · Entwicklungsstand 3.11.0 · Aufgabenformat 13

Die priorisierten Reiter und die erste Pinnwand sind umgesetzt. Aufgaben, Long-Tasks und Gruppen lassen sich als Reiter öffnen. Pinnwände zeigen Punkte aus Listen/Ordnern; Karten können gefiltert, geordnet oder frei angeordnet werden. Reiter schließen und Karten abheften ändern nur die Ansicht. Dieselben Aufgabenobjekte, IDs, Termine, Wiederholungen und Anhänge bleiben erhalten.

Kanonisch: `01_Repository/Glide/src/glide/app.pyw`. Startbare Kopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.11.0.pyw` mit vollständigen Ressourcen. Python/Tk, lokal ohne Konto oder neue Laufzeitabhängigkeit.

[Bedienung 3.11](../01_Repository/Glide/docs/34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md) · [Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) · [Aktueller Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Der 3.9-Bestand mit einheitlichen eingebetteten Dropdowns, App-Aktionen, kompaktem Kopf, Einstellungen und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen erscheinen bei laufender App, optional mit Dock-/Taskleistenaufmerksamkeit. Echte Systemzustellung hängt an installierter Registrierung und Signierung. Kein Autostart-Hilfsprozess. [Entscheidung](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Vor Änderungen `AGENTS.md` lesen, aktuelle Tests ausführen und alle App-Importe mit temporärem `GLIDE_DATA_DIR` isolieren. Aufgabenmutationen über `item_change`, Container über `sidebar_change`, Struktur über `guarded_structural_change`, Dialoge über `run_modal`. Symbole aus `ICONS`. Dokumentvorfassungen archivieren.

Nächste Ideen: Schnellerfassung und gespeicherte Filter; größere Pinnwandoptionen separat planen. Keine zusätzliche Projektmappe oder parallele Statusablage. [Vorschläge und Einordnung](Glide_Funktionsvorschlaege_2026-09-11.md).
