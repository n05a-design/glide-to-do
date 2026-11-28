# E03 – Chess & Chains: Shared Framework Integration (Arbeitsauftrag)

Stand 28.11.2026 · Glide 1.0.3 · Aufgabenformat 27 · Framework-Checkpoint Shell 0.9.1 / Bento 0.3.0

Separat einsetzbarer Auftrag für den Entwicklungsagenten von Chess & Chains (https://github.com/n05a-design/chess-and-chains). Er wird erst nach Freigabe durch den Inhaber übergeben. Dieser Glide-Auftrag hat Chess & Chains nicht verändert.

## 1. Ziel

Die vorhandene Schach-Fachlogik läuft innerhalb derselben gemeinsamen Shell-Architektur. Geeignete Bento-Komponenten werden produktiv verwendet. Schachregeln, Engines und Analyse bleiben in Chess & Chains.

## 2. Bekannter Ausgangsstand (öffentlich gelesen am 28.11.2026, ungeprüft)

- `chess_and_chains.__version__` 0.3.0, letzter Commit `6dcd12f1` auf `main`, Python ≥ 3.11.
- `src/glide_shell` 0.6.2 aus Glide-System V1.86 mit unverändertem Manifest; kein `glide_bento`.
- Der tatsächliche Funktionsbestand (Brett, Partieverwaltung, Analyse, Eröffnungen, Varianten, Training, Statistiken, Engines) ist **vom Chess-&-Chains-Agenten zu prüfen**, bevor etwas geändert wird.

## 3. Framework-Checkpoint

Wie bei STEPS: Übernahme nur aus einem Checkpoint mit `snapshot_id` und Manifest (`framework_checkpoint.py`, `shell_uebernehmen.py --mit-bento`), keine dauerhaften lokalen Änderungen an den Framework-Kopien.

## 4. Verbindliche Arbeitsweise

1. Bestandsprüfung vor jeder Änderung; Arbeitsstand sichern.
2. Shell 0.6.2 → Checkpoint-Stand, Manifest- und Konformitätsprüfung grün.
3. Shell als Anwendungsfundament (Host, Dialoge, Fensterlebensdauer, Plattformadapter, Pfade, Theme-Provider); konkurrierende allgemeine Mechanismen kontrolliert ablösen.
4. Bento für Statistik-, Trainings- und Partieübersichten; Brettdarstellung und Zugberechnung bleiben Fachlogik.
5. Datensicherheit: Partien und Datenbanken nie still migrieren; Sicherung vor Formatänderungen.
6. Regressionstests (Regeln, Engine-Anbindung, PGN o. Ä.) vor und nach der Integration.
7. Versionsfortschreibung von Chess & Chains nach eigenem Vertrag.
8. Fehlende allgemeine Komponenten über den Rückmeldevertrag an Glide melden.

## 5. Rückmeldevertrag

Wie im STEPS-Auftrag; Vorlage im [Entwicklungsplan §4.8](../Glide_Entwicklungsplan.md#48-glide-ecosystem-e01e08-ab-28112026).

## 6. Abnahme

Start und Bedienung, Konformität und Selbsttests aus der Kopie grün, Fachregressionen grün, gemeldete Framework-Anforderungen, Kompatibilitätszeile für die Matrix in Glide.
