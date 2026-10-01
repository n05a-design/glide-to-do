# Glide – kompakte Weitergabe an einen neuen Chat

Stand 12.09.2026 · Entwicklungsstand 3.8.0 · Aufgabenformat 13

Der Nutzer hat am 12.09.2026 den Beginn der Umsetzung der Funktionsvorschläge
beauftragt. Die erste priorisierte Stufe **lokale Erinnerungen** ist umgesetzt:
feste/relative Zeitpunkte, Aufschub, Bestätigung, Serienbezug, verpasste Termine
und gemeinsame Übersicht. Hinweise erscheinen innerhalb der laufenden App.
Am selben Tag kam Stufe A der Zustellung dazu: Eine neu zugestellte Erinnerung
hebt den Eintrag in Taskleiste bzw. Dock hervor – einmal je Prüflauf, erst nach
gespeichertem Zustellbeleg, abschaltbar, ohne Fokusdiebstahl. Beide vollständigen
Prüfläufe sind grün (Exitcode 0, je zwölf Suiten und zwei Analysen); automatisiert
ist 3.8.0 damit abgenommen. Offen bleibt die manuelle Sichtabnahme auf macOS und
Windows, für Stufe A insbesondere die tatsächliche Wirkung von Dock und Taskleiste.

Kanonischer Code: `01_Repository/Glide/src/glide/app.pyw`.
Startbare Arbeitskopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.8.0.pyw`
mit vollständigem Ressourcenordner. Python/Tk, lokal ohne Konto/Internet.

[Technische Übergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) ·
[Erinnerungsvertrag](../01_Repository/Glide/docs/31_ERINNERUNGEN_3.8.0.md) ·
[Prüfstand und Grenzen](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Abschlussbericht 3.8.0](../01_Repository/Glide/docs/12_ABSCHLUSSBERICHT.md).

Bestehender 3.7-Funktionsumfang einschließlich Vorlageneditor, Mac-Auswahlfeldern
und dynamischen Ordner-/Listenkacheln bleibt erhalten. Aufgabenformat 13 ergänzt
Erinnerungen; Einstellungen und Vorlagen bleiben Format 2. Vor Überschreiben
älterer Daten wird eine unrotierte bytegleiche Originalkopie gesichert.

Nächste Prioritäten: Erinnerungen samt Stufe A nativ abnehmen, anschließend
Reiteransicht und Pinnwand für dieselben Objekte. Die Reiterebene ist noch offen –
ob einzelne Punkte oder Gruppen die Reiter bilden, ist zu entscheiden.
Echte Systembenachrichtigungen setzen eine registrierte, installierte Anwendung
voraus und gehören zum Installer, nicht zum Anwendungscode; ein Hilfsprozess mit
Autostart ist ausgeschlossen. Begründung und Stufen in der
[Entscheidung zu Systembenachrichtigungen](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md). Keine parallele Statusverwaltung, zusätzliche
Ablagefächer oder Projektmappe als neue Datenstruktur.

Vor Änderungen `01_Repository/Glide/AGENTS.md` lesen, Ausgangstests ausführen,
Nutzdatenpfade prüfen und ausschließlich isoliertes `GLIDE_DATA_DIR` verwenden.
`item_change`, `sidebar_change`, `guarded_structural_change` und `run_modal`
weiterverwenden; Symbole aus `ICONS`. Keine neue Laufzeitabhängigkeit ohne
dokumentierte Entscheidung. Dokumentvorfassungen vor Änderung archivieren.
Arbeitskopie und Ressourcen konsistent halten. OneDrive ist externe
Dateisynchronisation und kein sicherer gleichzeitiger Mehrbenutzerbetrieb.

Weitere Ideen: [Funktionsvorschläge](Glide_Funktionsvorschlaege_2026-09-11.md).
Die Vorgängerfassung mit dem vollständigen 3.7-Stand liegt im lokalen Archiv.
