# Produkt- und Identitätsregister

Stand 04.09.2026 · App-Version 3.3.0 · Datenformat 10

Der obere Block ist durch den Quellcode belegt und muss nicht mehr entschieden
werden. Der untere Block enthält Geschäfts- und Rechtsentscheidungen. Offene
Werte dürfen nicht durch Vermutungen in Build- oder Store-Konfigurationen
ersetzt werden.

## Technisch belegt

| Feld | Stand | Beleg im Code |
|---|---|---|
| Produktname | Glide | `APP_NAME` |
| Langname | Glide – Aufgaben und Listen | `APP_PRODUCT_NAME` |
| App-Version | 3.2.0 | `APP_VERSION`, `VERSION` |
| Datenformat | 10 | `DATA_SCHEMA_VERSION` |
| Unterstützte Backup-Formate | 4 bis 10 | `MIN_PORTABLE_BACKUP_SCHEMA_VERSION`, `DATA_SCHEMA_VERSION` |
| Laufzeit | Python 3 mit Tk/Tcl, sonst nur Standardbibliothek | Importliste in `app.pyw` |
| Prüflaufzeit | Windows: Python 3.12.12 / Tk 8.6.17; zuvor dokumentiert Linux/Xvfb | aktuelles Ergebnis in `../07_QA_BERICHT.md` |
| Netzwerkzugriff | keiner | kein Socket-, HTTP- oder URL-Import |
| Benutzerkonto | keines | keine Auth-Pfade |
| Telemetrie | keine | keine Analytics-Aufrufe |
| Nutzerdaten Windows | `%APPDATA%\Glide\` | `get_app_data_dir()` |
| Nutzerdaten macOS | `~/Library/Application Support/Glide/` | `get_app_data_dir()` |
| Nutzerdaten Linux | `$XDG_DATA_HOME/Glide/` bzw. `~/.local/share/Glide/` | `get_app_data_dir()` |
| Testisolierung | `GLIDE_DATA_DIR` überschreibt den Datenordner | `get_app_data_dir()` |
| Dateiendung Backup | `.glidebackup` (ZIP mit `data.json` + `attachments/`) | `write_complete_backup()` |
| Austauschformate | TXT, Markdown, CSV (Semikolon, UTF-8-BOM) | Exportfunktionen |
| Größenlimit je Anhang | 512 MiB je Datei | `MAX_BACKUP_ATTACHMENT_BYTES` |
| Entpackte Backup-Grenzen | 2 GiB gesamt, 32 MiB Daten-JSON | `MAX_BACKUP_TOTAL_BYTES`, `MAX_BACKUP_DATA_BYTES` |
| Technisches Validierungslimit | 200.000 Punkte; keine Performancezusage | `MAX_BACKUP_ITEMS` |
| Lade-/Normalisierungsgrenze der Punkttiefe | 100; vor UI-Mutationen noch nicht durchgehend eingehalten | `MAX_ITEM_DEPTH`; offene Lücke in `../11_BESTANDSANALYSE.md` |
| Automatische Sicherungen | letzte 40 JSON-Stände unter `backups/` | `MAX_BACKUPS` |
| Oberflächensprache | Deutsch, einsprachig | Beschriftungen im Code |
| Fenstermindestgröße | 860 × 700 px | `minsize()` |
| Hell-/Dunkelmodus | vorhanden, Zustand wird gespeichert | `THEMES`, `settings.json` |
| Oberflächensymbole | `ICONS` nutzt Textzeichen; drei Emoji-Ausnahmen außerhalb der Tabelle sind offen | `ICONS`, `GROUP_MARKER`, `IMPORTANCE_MARKERS[3]`, `description_suffix`; siehe Produktgrenzen |
| Übernahme aus Altordnern | keine – der Datenordner ist der Datenordner | seit 3.2.0 entfernt |
| Rückgängig-Tiefe | 20 Schritte | `MAX_UNDO_STEPS` |
| Max. Papierkorbeinträge | 200 | `MAX_TRASH_ENTRIES` |
| Max. Ordnerverschachtelung | 5 Ebenen | `MAX_FOLDER_DEPTH` |
| Beispielbestand zum Einlesen | 10 Listen, 5 Ordner, 140 Punkte | `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` |

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
| macOS Mindestversion | offen | folgt aus Build-Laufzeit und Tests auf Zielgeräten |
| macOS Architektur | offen; Universal 2 erst nach Machbarkeits- und Buildprüfung | Inhaber |
| Sicherheitskontakt | offen | Inhaber |
| Markenprüfung „Glide“ | offen | Fachanwalt, nicht durch Recherche ersetzbar |

Der Name „Glide“ wird von mehreren Anbietern in der Software genutzt. Vor einer
öffentlichen Veröffentlichung ist eine professionelle Marken- und
Namensrecherche erforderlich; eine eigene Suche ersetzt sie nicht.

## Pflege dieser Datei

`AGENTS.md` nennt dieses Register als verbindliche Quelle für Build- und
Store-Konfigurationen. Ein falscher Wert hier wird also weitergereicht, nicht
nur gelesen.

Der übergebene Kontext meldete einen veralteten Wert 9. Beim aktuellen
Abgleich enthielt diese Datei bereits korrekt **10**. Der tatsächliche Dateistand
hat Vorrang vor älteren Übergaben. Deshalb: Bei jeder Versionserhöhung
die Werte im oberen Block gegen den Quelltext prüfen, nicht gegen die
Erinnerung. Der Belegpfad steht in jeder Zeile.
