# E03 – Chess & Chains: Shared Framework Integration (Arbeitsauftrag)

Stand 28.11.2026 (E02) · Glide 1.0.3 · Aufgabenformat 27 · Framework-Checkpoint `35018623631ab6ad` · Shell 0.10.0 / Bento 0.3.0

Separat einsetzbarer Auftrag für den Entwicklungsagenten von Chess & Chains (https://github.com/n05a-design/chess-and-chains). Er wird erst nach Freigabe durch den Inhaber übergeben. Dieser Glide-Auftrag hat Chess & Chains nicht verändert.

## 1. Ziel

Die vorhandene Schach-Fachlogik läuft innerhalb derselben gemeinsamen Shell-Architektur. Geeignete Bento-Komponenten werden produktiv verwendet. Schachregeln, Engines und Analyse bleiben in Chess & Chains.

## 2. Bekannter Ausgangsstand (öffentlich gelesen am 28.11.2026, ungeprüft)

- `chess_and_chains.__version__` 0.3.0, letzter Commit `6dcd12f1` auf `main`, Python ≥ 3.11.
- `src/glide_shell` 0.6.2 aus Glide-System V1.86 mit unverändertem Manifest; kein `glide_bento`.
- Der tatsächliche Funktionsbestand (Brett, Partieverwaltung, Analyse, Eröffnungen, Varianten, Training, Statistiken, Engines) ist **vom Chess-&-Chains-Agenten zu prüfen**, bevor etwas geändert wird.

## 3. Framework-Checkpoint (verbindlich)

Übernommen wird ausschließlich aus dem Checkpoint **`35018623631ab6ad`** (vollständige Kennung `35018623631ab6ad52415ffc4d8604b80428c33235aee99bb745e36b074a7856`): Glide Shell **0.10.0** (kompatibel seit 0.6.2), Glide Bento **0.3.0**, Glide-System V1.97. Der Checkpoint liegt beim Inhaber unter `%USERPROFILE%\gq\e02\checkpoint` und wird dem Agenten als Ordner übergeben; er enthält `CHECKPOINT.json` (Kennung, Quellcommit, Manifest mit SHA-256, öffentliche Schnittstellen, Schnittstellenvergleich zu 0.6.2, Kompatibilität, Prüfergebnisse, bekannte Einschränkungen), `src/glide_shell`, `src/glide_bento` und `tools/`.

1. Checkpoint prüfen: `python3 -B <checkpoint>/tools/framework_checkpoint.py --pruefen <checkpoint>` muss „unverändert“ melden.
2. Vorab prüfen, ohne zu schreiben: `python3 -B <checkpoint>/tools/shell_uebernehmen.py --pruefen --mit-bento <projekt>/<quellordner>`. Unter „Host-Vertrag“ steht jeder Import eines Namens, den Shell 0.10.0 nicht hat.
3. Aktualisieren mit Sicherung außerhalb des Projekts: `python3 -B <checkpoint>/tools/shell_uebernehmen.py --mit-bento --unsauber-erlauben --sicherung <sicherungsordner> <projekt>/<quellordner>`. `--unsauber-erlauben` ist nötig, weil der Checkpoint aus einem noch nicht committeten Glide-Stand stammt (im Manifest vermerkt). Das Manifest der Kopie nennt danach `framework_snapshot`.
4. Rückkehr: `python3 -B <checkpoint>/tools/shell_uebernehmen.py --zurueck <sicherung> <projekt>/<quellordner>` stellt Shell 0.6.2 bytegenau wieder her.
5. Den Ablauf und die Kompatibilitätsgrenzen beschreibt `src/glide_shell/AKTUALISIERUNG.md` im Checkpoint. Belegt ist die Aktualisierung an einem künstlichen 0.6.2-Host, nicht an diesem Projekt.

Nie aus einem Glide-Arbeitsbaum übernehmen. Verwaltete Framework-Kopien werden im Projekt nicht dauerhaft verändert.

## 4. Verbindliche Arbeitsweise

1. Bestandsprüfung vor jeder Änderung; Arbeitsstand sichern.
2. Shell 0.6.2 → 0.10.0 nach Abschnitt 3 anheben; Selbsttests 16/16 (Shell und Bento) und Konformität grün.
3. Shell als Anwendungsfundament: `AppHost` mit geordnetem Beenden, `workspaces` für Brett, Partien, Training und Analyse, `color_roles.ThemeProvider` mit eigener Markenfarbe, `settings_registry`, `controls`, Dialoge, Fensterlebensdauer, Plattformadapter, Pfade; konkurrierende allgemeine Mechanismen kontrolliert ablösen.
4. Bento für Statistik-, Trainings- und Partieübersichten; Brettdarstellung und Zugberechnung bleiben Fachlogik.
5. Datensicherheit: Partien und Datenbanken nie still migrieren; Sicherung vor Formatänderungen.
6. Regressionstests (Regeln, Engine-Anbindung, PGN o. Ä.) vor und nach der Integration.
7. Versionsfortschreibung von Chess & Chains nach eigenem Vertrag.
8. Fehlende allgemeine Komponenten über den Rückmeldevertrag an Glide melden.

## 5. Rückmeldevertrag

Wie im STEPS-Auftrag; Vorlage im [Entwicklungsplan §4.8](../Glide_Entwicklungsplan.md#48-glide-ecosystem-e01e08-ab-28112026).

## 6. Abnahme

Start und Bedienung, Konformität und Selbsttests aus der Kopie grün, Fachregressionen grün, gemeldete Framework-Anforderungen, Kompatibilitätszeile für die Matrix in Glide.
