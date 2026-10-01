# Produkt- und Identitätsregister

Stand 30.09.2026 · App-Version 3.31.0 · Datenformat 20

Der obere Block ist durch den Quellcode belegt und muss nicht mehr entschieden
werden. Der untere Block enthält Geschäfts- und Rechtsentscheidungen. Offene
Werte dürfen nicht durch Vermutungen in Build- oder Store-Konfigurationen
ersetzt werden.

## Technisch belegt

| Feld | Stand | Beleg im Code |
|---|---|---|
| Produktname | Glide | `APP_NAME` |
| Langname | Glide – Aufgaben und Listen | `APP_PRODUCT_NAME` |
| App-Version | 3.31.0 | `APP_VERSION`, `VERSION` |
| Datenformat | 20 | `DATA_SCHEMA_VERSION` |
| Unterstützte Backup-Formate | 4 bis 20 | `MIN_PORTABLE_BACKUP_SCHEMA_VERSION`, `DATA_SCHEMA_VERSION` |
| Laufzeit | Python 3.14 mit Tk 9 als Grundlage (27.09.2026); Tk 8.6 bleibt lauffähig, ohne Systemmitteilung und SVG-Vorschau. Sonst nur Standardbibliothek | Importliste in `app.pyw` |
| Mitgelieferte Bibliothek | tkinterdnd2 0.6.3 (MIT) mit tkDnD für das Ziehen aus Finder/Explorer; optional, lädt beim ersten Gebrauch | `src/glide/vendor`, [Entscheidung](ABHAENGIGKEIT_TKDND.md) |
| Prüflaufzeit | maßgeblich macOS mit Python 3.14.5 und Tk 9.0.3; der letzte vollständige Windows-Lauf war 3.26 (Python 3.13). Ergebnisse im QA-Bericht | `docs/07_QA_BERICHT.md` |
| Netzwerkzugriff | kein automatischer Datentransfer; bewusst angeklickte Links öffnen den Browser | lokale Datenhaltung, `webbrowser` |
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
| Automatische Sicherungen | unter `backups/`, nur bei geändertem Inhalt: die zehn neuesten, jüngere als 30 Minuten, höchstens 40; dazu je Tag der letzte Stand für 14 Tage (29.09.2026) | `MIN_BACKUPS`, `BACKUP_MAX_AGE_MINUTES`, `MAX_BACKUPS`, `BACKUP_DAILY_DAYS`, `write_backup_copy` |
| Oberflächensprache | Deutsch, einsprachig | Beschriftungen im Code |
| Oberflächensymbole | zentrale Textzeichen-Tabelle; Legacy-Emoji nur beim Parsen alter Eingaben | `ICONS`, Symbolprüfung |
| Logo und Programmsymbol | SVG-Master aus `20_Grafik_Master` (Glide-Blau `#0185E1`); in der Oberfläche in der Akzentfarbe, als Programmsymbol in Blau; Paketsymbole in `assets/icons` (29.09.2026) | `logo.py`, `resources/logo`, `packaging/baue_symbole.py` |
| Übernahme aus Altordnern | keine – der Datenordner ist der Datenordner | `get_app_data_dir()` |
| Rückgängig-Tiefe | 20 Schritte | `MAX_UNDO_STEPS` |
| Max. Papierkorbeinträge | 200 | `MAX_TRASH_ENTRIES` |
| Max. Ordnerverschachtelung | 5 Ebenen | `MAX_FOLDER_DEPTH` |
| Materialoptik | abschaltbare getönte Flächen, Kanten und optionaler DWM-Aufruf | `active_theme`, `RoundedContainer` |
| Mitgelieferte Schriften | DejaVu Sans TTF (vier Schnitte) und Pixelify Sans TTF (Regular, Bold; SIL OFL 1.1, nur Überschriften im Design „Pixel“), private Registrierung | `register_private_fonts`, `app_font`, `pixel_heading_family`, `resources/fonts/provenance.json` |
| macOS Bundle Identifier | `de.shaye.glide` (Inhaberentscheidung 26.09.2026) | `APP_BUNDLE_ID`, `packaging/macos/baue_app.py` |
| Windows AppUserModelID | `Shaye.Glide` (Inhaberentscheidung 26.09.2026) | `APP_USER_MODEL_ID`, `set_windows_app_user_model_id`, `packaging/windows/verknuepfung_anlegen.ps1` |
| Beispielbestand zum Einlesen | aktuelles Format-20-Fixture unter `tests/fixtures/beispiele/`, feste Referenz `current_v20` | `pruefen.py`, `test_features330.py` |

## Offen – Entscheidung oder Plattformabnahme erforderlich

| Feld | Stand | Wer entscheidet |
|---|---|---|
| Publisher / Herausgebername | Tim von Trostorff | Entwicklungsauftrag 3.26.0 |
| Copyright-Zeile | offen | Inhaber |
| Support-E-Mail | mailme@shaye.de | Inhaber |
| Website | Shaye.de | Inhaber |
| Datenschutz-URL | offen | Inhaber, für beide Stores Pflicht |
| Lizenzmodell | Entwurf: kostenlose private, nicht kommerzielle Nutzung; siehe LIZENZENTWURF_3.26.0.md | Veröffentlichung der Bedingungen noch offen |
| Preis / Monetarisierung | Private Nutzung kostenlos; kommerzielle Nutzung nicht durch den Entwurf erlaubt | Entwicklungsauftrag 3.26.0 |
| Vertriebsweg | zuerst Direktvertrieb (Website, Developer-ID-Signatur und Notarisierung, Windows-Installer); Stores später – entschieden 27.09.2026 | Inhaber |
| Windows-Zielarchitektur | x64 – entschieden 27.09.2026 | Inhaber |
| Inno Setup AppId | offen, einmalige GUID | einmalig erzeugen, danach nie ändern |
| macOS Mindestversion | offen | folgt aus Build-Laufzeit und Tests auf Zielgeräten |
| macOS Architektur | arm64 (Apple Silicon) – entschieden 27.09.2026; Universal 2 nur, wenn Intel-Macs gebraucht werden | Inhaber |
| Sicherheitskontakt | offen | Inhaber |
| Markenprüfung „Glide“ | offen | Fachanwalt, nicht durch Recherche ersetzbar |

Für Copyright, Datenschutz-URL, Sicherheitskontakt, Inno-AppId und
macOS-Mindestversion liegen seit dem 27.09.2026
[Vorschläge zur Bestätigung](../../../../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md)
bereit. Sie gelten erst nach der Bestätigung durch den Inhaber.

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

Format 12 ergänzt Anhänge an Listen und Ordnern. Vor dem ersten Überschreiben älterer lokaler Daten entsteht eine unrotierte Originalkopie. [Änderungen und aktueller Nachweis](../archiv/24_VERSION_3.7.0.md).

Format 13: lokale Erinnerungen mit Originalsicherung. [Vertrag](../archiv/31_ERINNERUNGEN_3.8.0.md).

Eine Systembenachrichtigung mit Glide-Namen verlangt eine feste AppUserModelID
beziehungsweise einen festen Bundle-Identifikator. Beide sind seit dem
26.09.2026 festgelegt und ändern sich nie mehr. Siehe
[Entscheidung](SYSTEMBENACHRICHTIGUNGEN.md) und
[Paketierung](../../packaging/README.md).

3.9 ergänzt die additive Einstellung `sidebar_visible` und vereinheitlicht Dropdowns als eingebettete Frames ohne zusätzliche Fenster/Grabs. Keine Formatänderung. [UI-Vertrag](../archiv/32_UI_UND_BEDIENUNG_3.9.0.md).

3.10 ergänzt Reiter und Pinnwände als Ansichten vorhandener Punktobjekte. `ItemWorkspace` normalisiert und prüft `open_tabs`, `active_tab` und `pinboards` in den Einstellungen. Aufgabenformat 13 bleibt unverändert; Aufgabenbackups transportieren diese Ansichten nicht. Bearbeitungen laufen durch `item_change`, modale Auswahl durch `run_modal`. [Bedienung und Grenzen](../archiv/33_REITER_UND_PINNWAND_3.10.0.md).

3.11 ergänzt die app-interne Schnellerfassung mit deutscher Fristvorschau und gespeicherte Filter; 3.12 ergänzt „Mein Tag“; 3.13 ergänzt die flache Tabellenansicht. `SavedFilters`, `today_plan` und `table_columns` halten nur Kriterien, IDs beziehungsweise Spaltennamen; Aufgabenobjekte werden nicht kopiert. Die Einstellungen bleiben Format 2; das Aufgabenformat bleibt bis 3.13 bei 13, erst 3.14 ergänzt mit Format 14 Bearbeitungstag und geschätzten Aufwand. [Bedienung 3.13](../archiv/36_TABELLENANSICHT_3.13.0.md).
