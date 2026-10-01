# Produkt- und Identitätsregister

Stand 14.09.2026 · App-Version 3.21.0 · Datenformat 15

Der obere Block ist durch den Quellcode belegt und muss nicht mehr entschieden
werden. Der untere Block enthält Geschäfts- und Rechtsentscheidungen. Offene
Werte dürfen nicht durch Vermutungen in Build- oder Store-Konfigurationen
ersetzt werden.

## Technisch belegt

| Feld | Stand | Beleg im Code |
|---|---|---|
| Produktname | Glide | `APP_NAME` |
| Langname | Glide – Aufgaben und Listen | `APP_PRODUCT_NAME` |
| App-Version | 3.14.0 | `APP_VERSION`, `VERSION` |
| Datenformat | 13 | `DATA_SCHEMA_VERSION` |
| Unterstützte Backup-Formate | 4 bis 13 | `MIN_PORTABLE_BACKUP_SCHEMA_VERSION`, `DATA_SCHEMA_VERSION` |
| Laufzeit | Python 3 mit Tk/Tcl, sonst nur Standardbibliothek | Importliste in `app.pyw` |
| Prüflaufzeit | macOS / Python 3.14.5; aktueller Windows-Lauf offen | `docs/07_QA_BERICHT.md` |
| Netzwerkzugriff | keiner | kein Socket-, HTTP- oder URL-Import |
| Benutzerkonto | keines | keine Auth-Pfade |
| Telemetrie | keine | keine Analytics-Aufrufe |
| Nutzerdaten Windows | `%APPDATA%\\Glide\\` bzw. gewählter Datenordner | `get_app_data_dir()`, `change_data_folder()` |
| Nutzerdaten macOS | `~/Library/Application Support/Glide/` bzw. gewählter Datenordner | `get_app_data_dir()` |
| Nutzerdaten Linux | `$XDG_DATA_HOME/Glide/` bzw. `~/.local/share/Glide/` | `get_app_data_dir()` |
| Testisolierung | `GLIDE_DATA_DIR` überschreibt den Datenordner | `get_app_data_dir()` |
| Dateiendung Backup | `.glidebackup` (ZIP mit `data.json` + `attachments/`) | `write_complete_backup()` |
| Austauschformate | TXT, Markdown, CSV (Semikolon, UTF-8-BOM) | Exportfunktionen |
| Größenlimit je Anhang | 512 MiB je Datei | `MAX_BACKUP_ATTACHMENT_BYTES` |
| Entpackte Backup-Grenzen | 2 GiB gesamt, 32 MiB Daten-JSON | `MAX_BACKUP_TOTAL_BYTES`, `MAX_BACKUP_DATA_BYTES` |
| Technisches Validierungslimit | 200.000 Punkte; keine Performancezusage | `MAX_BACKUP_ITEMS` |
| Lade-/Mutationsgrenze der Punkttiefe | 100; vor tiefenerhöhenden UI-Mutationen geprüft | `MAX_ITEM_DEPTH`, `make_subitem` |
| Automatische Sicherungen | letzte 40 JSON-Stände unter `backups/` | `MAX_BACKUPS` |
| Oberflächensprache | Deutsch, einsprachig | Beschriftungen im Code |
| Oberflächensymbole | zentrale Textzeichen-Tabelle; Legacy-Emoji nur beim Parsen alter Eingaben | `ICONS`, Symbolprüfung |
| Übernahme aus Altordnern | keine – der Datenordner ist der Datenordner | `get_app_data_dir()` |
| Rückgängig-Tiefe | 20 Schritte | `MAX_UNDO_STEPS` |
| Max. Papierkorbeinträge | 200 | `MAX_TRASH_ENTRIES` |
| Max. Ordnerverschachtelung | 5 Ebenen | `MAX_FOLDER_DEPTH` |
| Materialoptik | abschaltbare getönte Flächen, Kanten und optionaler DWM-Aufruf | `active_theme`, `RoundedContainer` |
| Mitgelieferte Schrift | DejaVu Sans TTF, vier Schnitte, private Registrierung | `register_private_fonts`, `app_font` |
| Beispielbestand zum Einlesen | aktuelles Format-13-Fixture unter `tests/fixtures/beispiele/` | `pruefen.py`, `test_release36.py` |

## Offen – Entscheidung oder Plattformabnahme erforderlich

| Feld | Stand | Wer entscheidet |
|---|---|---|
| Publisher / Herausgebername | offen | Inhaber |
| Copyright-Zeile | offen | Inhaber |
| Support-E-Mail | mailme@shaye.de | Inhaber |
| Website | Shaye.de | Inhaber |
| Datenschutz-URL | offen | Inhaber, für beide Stores Pflicht |
| Lizenzmodell | offen | Inhaber, rechtlich prüfen lassen |
| Preis / Monetarisierung | offen | Inhaber |
| Windows-Zielarchitektur | offen, Empfehlung x64 | Inhaber |
| Windows AppUserModelID | offen | folgt aus Publisher + Produktname |
| Inno Setup AppId | offen, einmalige GUID | einmalig erzeugen, danach nie ändern |
| macOS Bundle Identifier | offen, Form `de.<domain>.glide` | folgt aus eigener Domain |
| macOS Mindestversion | offen | folgt aus Build-Laufzeit und Tests auf Zielgeräten |
| macOS Architektur | offen; Universal 2 erst nach Machbarkeits- und Buildprüfung | Inhaber |
| Sicherheitskontakt | offen | Inhaber |
| Markenprüfung „Glide“ | offen | Fachanwalt, nicht durch Recherche ersetzbar |

Echter selektiver Desktop-Blur, Synchronisationsdienst und
Konfliktzusammenführung sind Architekturentscheidungen außerhalb des lokalen
Tk-3.7-Funktionsstands; ihre Bewertung steht in den aktuellen 3.7-Berichten.

Der Name „Glide“ wird von mehreren Anbietern in der Software genutzt. Vor einer
öffentlichen Veröffentlichung ist eine professionelle Marken- und
Namensrecherche erforderlich; eine eigene Suche ersetzt sie nicht.

## Pflege dieser Datei

`AGENTS.md` nennt dieses Register als verbindliche Quelle für Build- und
Store-Konfigurationen. Bei jeder Versionserhöhung sind Version, Datenformat,
Backupgrenzen, Pfade und Plattformnachweise gegen den Quelltext und den
aktuellen QA-Lauf zu prüfen. Historische Fassungen liegen unter
`docs/decisions/archiv/`.

Format 12 ergänzt Anhänge an Listen und Ordnern. Vor dem ersten Überschreiben älterer lokaler Daten entsteht eine unrotierte Originalkopie. [Änderungen und aktueller Nachweis](../24_VERSION_3.7.0.md).

Format 14: lokale Erinnerungen mit Originalsicherung. [Vertrag](../31_ERINNERUNGEN_3.8.0.md).

Eine Systembenachrichtigung mit Glide-Namen verlangt eine feste AppUserModelID
beziehungsweise einen festen Bundle-Identifikator; beide sind hier festzulegen,
sobald die Paketierung ansteht. [Entscheidung](SYSTEMBENACHRICHTIGUNGEN.md).

3.9 ergänzt die additive Einstellung `sidebar_visible` und vereinheitlicht Dropdowns als eingebettete Frames ohne zusätzliche Fenster/Grabs. Keine Formatänderung. [UI-Vertrag](../32_UI_UND_BEDIENUNG_3.9.0.md).

3.10 ergänzt Reiter und Pinnwände als Ansichten vorhandener Punktobjekte. `ItemWorkspace` normalisiert und prüft `open_tabs`, `active_tab` und `pinboards` in den Einstellungen. Aufgabenformat 14 bleibt unverändert; Aufgabenbackups transportieren diese Ansichten nicht. Bearbeitungen laufen durch `item_change`, modale Auswahl durch `run_modal`. [Bedienung und Grenzen](../33_REITER_UND_PINNWAND_3.10.0.md).

3.11 ergänzt die app-interne Schnellerfassung mit deutscher Fristvorschau und gespeicherte Filter; 3.12 ergänzt „Mein Tag“; 3.13 ergänzt die flache Tabellenansicht. `SavedFilters`, `today_plan` und `table_columns` halten nur Kriterien, IDs beziehungsweise Spaltennamen; Aufgabenobjekte werden nicht kopiert. Die Einstellungen bleiben Format 2, Aufgabenformat 14 ergänzt Bearbeitungstag und geschätzten Aufwand. [Bedienung 3.13](../36_TABELLENANSICHT_3.13.0.md).
