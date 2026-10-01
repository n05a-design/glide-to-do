# Produkt- und Identitätsregister

Stand 03.09.2026 · App-Version 2.11.0 · Datenformat 10

Der obere Block ist durch den Quellcode belegt und muss nicht mehr entschieden
werden. Der untere Block enthält Geschäfts- und Rechtsentscheidungen. Offene
Werte dürfen nicht durch Vermutungen in Build- oder Store-Konfigurationen
ersetzt werden.

## Technisch belegt

| Feld | Stand | Beleg im Code |
|---|---|---|
| Produktname | Glide | `APP_NAME` |
| Langname | Glide – Aufgaben und Listen | `APP_PRODUCT_NAME` |
| App-Version | 2.11.0 | `APP_VERSION`, `VERSION` |
| Datenformat | 9 | `DATA_SCHEMA_VERSION` |
| Unterstützte Backup-Formate | 4, 5, 6, 7 | `MIN_PORTABLE_BACKUP_SCHEMA_VERSION` |
| Laufzeit | Python 3 mit Tk/Tcl, sonst nur Standardbibliothek | Importliste in `app.pyw` |
| Getestete Laufzeit | Python 3.12 / Tk 8.6 | Integrationstestlauf |
| Netzwerkzugriff | keiner | kein Socket-, HTTP- oder URL-Import |
| Benutzerkonto | keines | keine Auth-Pfade |
| Telemetrie | keine | keine Analytics-Aufrufe |
| Nutzerdaten Windows | `%APPDATA%\Glide\` | `get_app_data_dir()` |
| Nutzerdaten macOS | `~/Library/Application Support/Glide/` | `get_app_data_dir()` |
| Nutzerdaten Linux | `$XDG_DATA_HOME/Glide/` bzw. `~/.local/share/Glide/` | `get_app_data_dir()` |
| Testisolierung | `GLIDE_DATA_DIR` überschreibt den Datenordner | `get_app_data_dir()` |
| Dateiendung Backup | `.glidebackup` (ZIP mit `data.json` + `attachments/`) | `write_complete_backup()` |
| Austauschformate | TXT, Markdown, CSV (Semikolon, UTF-8-BOM) | Exportfunktionen |
| Max. Anhangsgröße | 512 MB je Datei | `MAX_BACKUP_ATTACHMENT_BYTES` |
| Max. Backupgröße | 2 GB gesamt, 32 MB Daten-JSON | `MAX_BACKUP_TOTAL_BYTES`, `MAX_BACKUP_DATA_BYTES` |
| Max. Aufgabenzahl je Bestand | 200.000 | `MAX_BACKUP_ITEMS` |
| Max. Verschachtelung | 100 Ebenen | `MAX_ITEM_DEPTH` |
| Automatische Sicherungen | letzte 40 JSON-Stände unter `backups/` | `MAX_BACKUPS` |
| Oberflächensprache | Deutsch, einsprachig | Beschriftungen im Code |
| Fenstermindestgröße | 860 × 700 px | `minsize()` |
| Hell-/Dunkelmodus | vorhanden, Zustand wird gespeichert | `THEMES`, `settings.json` |

## Offen – Entscheidung erforderlich

| Feld | Stand | Wer entscheidet |
|---|---|---|
| Publisher / Herausgebername | offen | Inhaber |
| Copyright-Zeile | offen | Inhaber |
| Support-E-Mail | offen | Inhaber |
| Website | offen | Inhaber |
| Datenschutz-URL | offen | Inhaber, für beide Stores Pflicht |
| Lizenzmodell | offen | Inhaber, rechtlich prüfen lassen |
| Preis / Monetarisierung | offen | Inhaber |
| Windows-Zielarchitektur | offen, Empfehlung x64 | Inhaber |
| Windows AppUserModelID | offen | folgt aus Publisher + Produktname |
| Inno Setup AppId | offen, einmalige GUID | einmalig erzeugen, danach nie ändern |
| macOS Bundle Identifier | offen, Form `de.<domain>.glide` | folgt aus eigener Domain |
| macOS Mindestversion | offen, Empfehlung macOS 12 | folgt aus Testgeräten |
| macOS Architektur | offen, Empfehlung Universal 2 | Inhaber |
| Sicherheitskontakt | offen | Inhaber |
| Markenprüfung „Glide“ | offen | Fachanwalt, nicht durch Recherche ersetzbar |

Der Name „Glide“ wird von mehreren Anbietern in der Software genutzt. Vor einer
öffentlichen Veröffentlichung ist eine professionelle Marken- und
Namensrecherche erforderlich; eine eigene Suche ersetzt sie nicht.
