# Startkontext – Glide 3.21.2

Stand 13.09.2026 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Kanonisch: `src/glide/app.pyw`. Startbare Kopie: `../../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.21.2.pyw` mit vollständigen Ressourcen. Kein Git-Checkout.

Zuerst `AGENTS.md`, [Bedienung 3.10](33_REITER_UND_PINNWAND_3.10.0.md), [Datenvertrag](06_DATA_BACKUP_MIGRATION.md), [QA](07_QA_BERICHT.md) und [Übergabe](09_PROJECT_HANDOFF.md) lesen. Alle Tests setzen vor App-Import ein temporäres `GLIDE_DATA_DIR`.

3.11 setzt Schnellerfassung und gespeicherte Filter um. 3.12 ergänzt „Mein Tag“; 3.13 ergänzt die Tabellenansicht mit flacher Darstellung und listenspezifischer Spaltenauswahl. Alle drei Ansichten referenzieren dieselben Punkte. Aufgabenformat ist jetzt 14.

Der 3.9-Bestand mit eingebetteten Dropdowns, App-Aktionen, Einstellungszahnrad und ausblendbarer Seitenleiste bleibt erhalten. Benachrichtigungen funktionieren bei laufender App. Systemzustellung bleibt an Paketierung und Signierung gebunden; kein Autostart-Hilfsprozess. [Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Bearbeitungstag und Aufwand sind in 3.14 umgesetzt, Tagesplanung und Tageskapazität in 3.15, das vollständige App-Backup mit Inhaltsvorschau in 3.16 die Druck-/PDF-Ausgabe in 3.17 der CSV-Import mit Spaltenzuordnung in 3.18 der dauerhafte Änderungsverlauf in 3.19 die Kalenderausgabe als ICS in 3.20 und der Kalenderimport in 3.21. Spätere Ideen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten. Keine zusätzliche Projektmappe oder parallele Statusablage. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md) · [Vorschläge](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md).

3.21 ergänzt den Kalenderimport; er legt ausschließlich neue Punkte an, überschreibt nichts und ist mit Rückgängig vollständig zurücknehmbar. Aufgabenformat 15 bleibt unverändert. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

3.20 ergänzt die Kalenderausgabe als ICS; sie liest nur vorhandene Objekte und verändert nichts. Aufgabenformat 15 bleibt unverändert. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).

3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15; der Verlauf entsteht beim Speichern aus dem Vergleich zweier Stände und ist abschaltbar. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 ergänzt den CSV-Import mit Spaltenzuordnung; er legt ausschließlich neue Punkte an, überschreibt nichts und ist mit Rückgängig vollständig zurücknehmbar. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt die Druck- und PDF-Ausgabe; sie liest nur vorhandene Objekte und verändert nichts. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt das vollständige App-Backup mit Inhaltsvorschau; Aufgabenformat 14 bleibt unverändert. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

3.15 ergänzt die Ansicht „Tagesplanung" und die Einstellung „Tageskapazität"; gerechnet wird ausschließlich aus vorhandenen Feldern. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

3.14 ergänzt freiwilligen Bearbeitungstag und Aufwand. Aufgabenformat 14 sichert ältere Daten vor dem ersten Speichern; Backups, Vorlagen und Exporte führen beide Angaben mit. Persönliche Ansichten bleiben in Einstellungen. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).
