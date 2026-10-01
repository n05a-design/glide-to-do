# Startkontext – Glide 3.8.0

Stand 12.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Kanonischer Code: `src/glide/app.pyw`. Startbare Kopie:
`../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.8.0.pyw` ab Repository;
der vollständige Ressourcenordner gehört dazu. Der Workspace ist kein Git-Checkout.

Zuerst `AGENTS.md`, [Erinnerungen](31_ERINNERUNGEN_3.8.0.md),
[Datenvertrag](06_DATA_BACKUP_MIGRATION.md), [QA](07_QA_BERICHT.md) und
[Übergabe](09_PROJECT_HANDOFF.md) lesen. Tests nur mit isoliertem `GLIDE_DATA_DIR`.

Erster Funktionsausbau: gespeicherte lokale Erinnerungen, Aufschub, Bestätigung,
Serienbezug und gemeinsame Übersicht. Hinweise erscheinen innerhalb der laufenden
App und heben zusätzlich den Eintrag in Taskleiste bzw. Dock hervor – einmal je
Prüflauf, abschaltbar. Systembenachrichtigungen und Ausführung bei beendetem
Programm fehlen; beides setzt eine registrierte, installierte Anwendung voraus
([Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).
Bestehende Funktionen aus 3.7, Vorlagen, Mac-Menüs und dynamische Kacheln bleiben erhalten.

Weitere Wünsche: Reiteransicht und Pinnwand für dieselben Objekte. Keine neue
Projektmappe, keine parallele Statusablage. Genaue Reiterebene noch offen.
