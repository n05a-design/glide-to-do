# Speicherstatus und Sicherungsreserve – WA-40/WA-47

25.10.2026 · lokaler Quellkandidat auf Glide 3.44.0 / Aufgabenformat 26 · keine Lieferung

**Auftrag:** „Anschließend weiter mit der Feature Umsetzung“. Begrenztes nächstes Paket aus der technischen Folge in [Plan §21.12/§21.13](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2113-fünftes-umsetzungspaket-speicherstatus-und-sicherungsreserve). Die offene menschliche D55-Abnahme bleibt getrennt. Kein Versionswechsel, Commit/Push, Anbieter, Formatwechsel oder Lieferauftrag.

## Umgesetzt

- **Speicherstatus:** Datei › Sicherung › Speicherstatus …, auch in der Aktionssuche. Aufgaben-, Einstellungs-, Vorlagen- und Sicherungsfehler bleiben getrennt. Ein nicht modaler Textknopf am unteren Fensterrand erscheint nur bei einem Problem oder knapper Reserve; ein erfolgreicher anderer Speicherweg verdeckt den Fehler nicht.
- **Erneut speichern:** offene Editoreingaben übernehmen; Aufgaben/Sicherung und Einstellungen erneut versuchen, offene Vorlagen bei Bedarf ebenfalls. Nur tatsächlicher Erfolg löscht den passenden Fehler. Der scrollbare Dialog zeigt den aktualisierten Zustand; sein Fuß bleibt bei 480 × 360 frei.
- **Stille Fehler:** Autosave, Einstellungen und Vorlagen melden Probleme über den Status und das vorhandene Fehlerprotokoll. Der neue Statusweg zählt wiederholte gleiche Fehler und protokolliert sie beim ersten Auftreten bzw. bei geändertem Text. Vorhandene Meldungen zu Folgefehlern bleiben erhalten.
- **Größenbudget:** 32 MiB je JSON-Datei, wie die bestehende Grenze der Sicherungsdaten. Vorabprüfung plus begrenztes Lesen für Aufgaben, Einstellungen und Vorlagen samt den bisherigen direkten JSON-Dateilesern; auch die Formatvorsicherung prüft vor Hash/Parse. Atomare Schreibvorgänge prüfen neue Kodierung und vorhandenes Ziel. UTF-8 und Windows-Zeilenenden sind in der Bytezahl enthalten.
- **Geschützter Start:** zu große Aufgaben nur schreibgeschützt, zu große Einstellungen/Vorlagen für diesen Start gegen Schreiben gesperrt. Originaldateien bleiben unverändert; kein automatisches Entfernen oder Verkleinern. Nach externer Prüfung ist ein Neustart nötig. Retry umgeht keine Schranke.
- **Reserve:** ab 80 % von 32 MiB für die Summe der drei gespeicherten JSON-Dateien. Diese Summe ist ausdrücklich eine Frühwarnung; die tatsächliche App-Backupgröße wird weiterhin beim Export geprüft. Ein Import mit fehlgeschlagener Vorab-Sicherung bleibt ohne Bestandsänderung.

Fachlogik Tk-frei in `storage_health.py`, vorhandener `SaveResult`-/Bool-Vertrag und Mutationseinstiege erhalten. Keine neue Laufzeitabhängigkeit oder Einstellung. [Verhalten](../../../docs/20_FUNKTIONEN.md#speicherstatus-und-sicherungsreserve-wa-40wa-47-lokaler-kandidat), [Datenvertrag](../../../docs/06_DATA_BACKUP_MIGRATION.md#größenbudget-und-speicherstatus-lokaler-kandidat).

## Quelle und gezielte Prüfung

Vorherige App `155d1a9b318f652fae6b0ad944dd4c1ddd3928c1d4c64bad76e797fa2c3f97f0`; Paket-App `2c274277d55b883e95dfa7b2d1b550e22e1764c81bd96ebb05319ec7993babf3`. Modul- und Prüfwerkzeughashes: [Quellmanifest](quellmanifest.json); [Zusammenfassung](ergebnis.json). Die vorhandene Speicherergebnisprüfung war vor Produktionsänderungen grün ([Baseline](baseline_speicherergebnis.json)).

Windows 11, Python 3.14.7 / Tk 9.0.4. Alle Appimporte mit frischem temporärem `GLIDE_DATA_DIR`, künstlichen Daten und UTF-8-Ausgabe. Kein Eingriff in den echten Nutzerdatenordner; keine Computer-Use-Bedienung nach dem vorherigen Esc-Stopp.

| Prüfung | Ergebnis / Beleg |
|---|---|
| Neue Fachlogik | 8 Unit-Tests: Bytegrenze/Unicode, Wachstum nach stat, kein Lesen oberhalb Grenze, ungültiges JSON, Fehlerzählung/Deduplizierung, getrennte Erholung, 80-%-Reserve, Windows-Zeilenenden |
| Bestehende Fachverträge | 14 Formatvorsicherungs-, 16 Speichervergleichs/-ergebnis- und 6 Aktionskatalogtests grün; Formatsicherungen weiter bytegenau und je Dateistand nur ein Parse |
| Neue Pflichtsuite | [4/4 grün](test_speicherstatus.json): echter Autosave-Fehler, alte Dateibytes bis Retry, Statusdialog und echter Retry-Knopf, getrennte Nebendateien/Sicherung, Größenüberschreitung beim Start für alle drei Dateien, atomare UTF-8-Grenze, Reserve im Kompaktmodus 480 × 560, Importabbruch vor Mutation |
| Bestehende Bereichsregression | [Ladephasen](laden.json) und [Speicherergebnis](speicherergebnis.json) grün; [Kompaktansichten](kompakt_ansichten.json) mit 108 Knopfprüfungen und vollständiger Menüauswahl grün |
| Statisch | Syntax der berührten Dateien, Tk-Freiheit und höchstens 50 Zeilen je Funktion im neuen Fachmodul, Diff-Prüfung grün; neue Suite in `pruefen.py` registriert |

Die drei bestehenden Regressionsberichte stammen vom Stand vor dem letzten reinen Docstring-Nachtrag zum Autosave; die abschließende neue 4/4-Suite stimmt einschließlich Modul- und Testhashes mit dem dokumentierten Quellstand überein.

Die roten Entwicklungsstände bleiben erhalten: [erster Vorlauf](test_speicherstatus_vorlauf.json) fand einen falschen UI-Adapter (`configure(text=…)` statt `RoundedButton.set_text`), [zweiter Vorlauf](test_speicherstatus_vorlauf2.json) fand die fehlenden CRLF-Bytes der Windows-Schreibgrenze und eine um einen Bruchteil zu kleine 80-%-Prüfvorgabe. Beides korrigiert; [grüner Zwischenstand](test_speicherstatus_zwischenstand.json) und finaler 4/4-Lauf sind getrennt. Beim Nachziehen der Formatvorsicherung musste deren Parse-Zähler vom bisherigen `json.load` auf den neuen begrenzten Leser umgestellt werden; abschließend alle 14 Fälle grün.

## Grenzen

Dies ist eine gezielte Paketprüfung, kein neuer eingefrorener Voll-/CI-/Liefernachweis. Die früheren 13/13-D55- und Windows-Vollprüfungen behalten ihre damaligen Quellstände. Native Menschen-/Screenreader-/DPI-/Mehrmonitorabnahme und Mac bleiben offen. Die zuvor beobachtete native Kürzelgrenze aus D55 wird durch dieses Paket nicht als abgenommen ausgegeben. Größenproben verwenden begrenzte künstliche Dateien und gepatchte kleine Grenzwerte; die neue Formatvorsicherungsprobe weist zusätzlich eine echte Datei oberhalb 32 MiB vor Hash und Parse ab. Keine erneute 26.420-Punkte-Speicherlast-/Leistungsmessung oder Behauptung zur Ursache von WA-41.
