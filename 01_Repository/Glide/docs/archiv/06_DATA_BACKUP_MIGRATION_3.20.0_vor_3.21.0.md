# Daten, Backups und Migration – Glide 3.20.0

Stand 13.09.2026 · Aufgabenformat 15 · Änderungsverlauf in 3.19

Aufgabenformat **14**, Einstellungen **2**, Vorlagenformat **2**. Die UI nennt Erinnerungen jetzt Benachrichtigungen; gespeicherte Felder und APIs wie `reminder`, `reminder_attention`, Zustellbelege und Aufschub bleiben unverändert. Neuer additiver boolescher Einstellungswert: `sidebar_visible`, Standard `true`. Design bleibt im bisherigen Feld `theme`.

Vor dem ersten Speichern von Aufgaben vor Format 14 entsteht die unrotierte unveränderte Originalkopie `backups/liste_vor_format14_<Zeitstempel>.json`. Bei Fehler wird nicht gespeichert. Formate 4–14 und Legacy 2 bleiben lesbar. Glide 3.13 und ältere Versionen können Format 14 nicht lesen. Für einen Rückwechsel die alte Sicherung in einer separaten Ablage verwenden; sie enthält keine späteren Änderungen.

| Ablage | Inhalt | Transport |
|---|---|---|
| `liste_speicher.json` | Ordner, Listen, Aufgaben, Labels, Wiederholungen, Benachrichtigungen, Papierkorb | Aufgabenbackup |
| `settings.json` | Theme, Profil, Anzeige, Historien, `reminder_attention`, `sidebar_visible` | Datenordnerkopie |
| `vorlagen.json` | System-/eigene Vorlagen | `.glidetemplates` oder Datenordnerkopie |
| `attachments/`, `backups/` | Lokale Anhänge und Sicherungen | referenzierte Anhänge in Aufgabenbackup; vollständige Datenordnerkopie |
| `glide.lock` | Temporäre Belegung | nicht kopieren |
| `datenordner.json` | Gerätebezogener Ablagezeiger | nicht im Aufgabenbackup |

Ein `.glidebackup` ist ein ZIP aus `data.json` und referenzierten Anhängen. Vollrestore ersetzt erst nach Validierung und Sicherung. Additiver Import erzeugt neue IDs und erhält den bisherigen Bestand. Teilbackups umfassen vollständige Zweige einschließlich leerer Unterordner. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden weiter geprüft. Einstellungen und separater Vorlagenkatalog sind nicht Teil eines Aufgabenbackups.

Die frei wählbare Ablage liegt außerhalb des Programms. `GLIDE_DATA_DIR` hat für Tests Vorrang; andernfalls gelten Plattformstandard und optional `datenordner.json`. Ein Datenordnerwechsel kopiert in ein leeres Ziel oder öffnet einen vorhandenen Bestand; die Quelle bleibt erhalten. Erkannte Fremdbelegung verhindert Speichern. Die Sperre ersetzt keinen verteilten Synchronisationsdienst.

Historischer vollständiger [Zustellvertrag Format 13](31_ERINNERUNGEN_3.8.0.md) gilt technisch weiter. Aktuelle [Bedienung](32_UI_UND_BEDIENUNG_3.9.0.md) und [QA](07_QA_BERICHT.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt `today_plan`; 3.13 ergänzt `table_columns` für die listenspezifische Tabellenansicht. Diese Werte sind persönliche Einstellungen, werden beim Laden bereinigt und sind kein Bestandteil eines Aufgabenbackups. Seit 3.14 führen Aufgabenformat 14, Backups und Vorlagen zusätzlich Bearbeitungstag und geschätzten Aufwand mit. [Bedienung 3.13](36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](35_MEIN_TAG_3.12.0.md).

3.20 ergänzt die Kalenderausgabe. Sie schreibt ausschließlich ICS-Dateien an ein gewähltes Ziel, atomar über eine Temporärdatei; Nutzdatendateien sind als Ziel ausgeschlossen. Aufgabenformat 15, Einstellungen und Vorlagen bleiben unberührt, und es entsteht kein Verlaufseintrag – eine Ausgabe ist keine Änderung. [Bedienung 3.20](44_KALENDERAUSGABE_3.20.0.md).

3.19 hebt das Aufgabenformat auf **15** und ergänzt das Feld `history` neben den Aufgabenfeldern. Ein Bestand im Format 14 oder älter wird beim ersten Speichern gehoben und erhält ein leeres Protokoll; vorher entsteht die unveränderte Kopie `liste_vor_format15_<Zeitstempel>.json` im Backup-Ordner. Ein defektes oder fremdes `history`-Feld wird beim Laden verworfen, ohne die Aufgaben zu berühren. Komplettbackup und App-Backup führen den Verlauf mit, ein Teilbackup als Auszug nicht; portable Backups werden weiterhin ab Format 4 gelesen, ein Format-15-Backup ist für ältere Fassungen erwartungsgemäß nicht lesbar. Rückgängig stellt den Bestand wieder her und lässt das Protokoll stehen. [Bedienung 3.19](43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 ergänzt den CSV-Import. Er liest eine gewählte Datei, schreibt selbst keine Datei und legt keine eigene Datenhaltung an; die entstehenden Punkte gehen durch `new_item` und damit durch dieselbe Prüfung wie handangelegte Punkte. Aufgabenformat 14, Einstellungen und Vorlagen bleiben unberührt, bestehende Punkte werden nie überschrieben, und der Vorgang ist ein einzelner Rückgängig-Schritt einschließlich der dabei angelegten Labels. [Bedienung 3.18](42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt die Druckausgabe. Sie schreibt ausschließlich HTML-Dateien an ein gewähltes Ziel oder in den temporären Ordner, atomar über eine Temporärdatei; Nutzdatendateien sind als Ziel ausgeschlossen. Aufgabenformat 14, Einstellungen und Vorlagen bleiben unberührt. [Bedienung 3.17](41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt das vollständige App-Backup. Das Archiv ist dasselbe ZIP wie ein Komplettbackup; im JSON steht zusätzlich der Abschnitt `app_backup` mit `format_version`, `settings` (ohne Tageshistorien, mit `theme`), `templates` und `activity`. Aufgabenformat 14 bleibt unverändert, und weil der Abschnitt neben den Aufgabenfeldern liegt, bleibt die Datei für ältere Fassungen ein gültiges Aufgabenbackup. Vor dem Ersetzen entstehen `vor_import_*.glidebackup`, `settings_vor_restore_*.json` und `vorlagen_vor_restore_*.json`. Ansichtsverweise werden nur zusammen mit den Aufgaben desselben Archivs übernommen. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

3.15 ergänzt die persönliche Einstellung `daily_capacity_minutes` (ganze Minuten 0–1440, Vorgabe 0 = kein Vergleich). Ein fehlender, beschädigter oder fremder Wert führt auf 0 zurück. Der betrachtete Planungstag wird nicht gespeichert, Tagesbilanzen werden nicht abgelegt: Jede Summe entsteht bei der Anzeige aus dem aktuellen Bestand. Aufgabenformat 14 bleibt unverändert; Aufgabenbackups enthalten weder Kapazität noch Ansichtszustand. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

3.14 ergänzt `planned_date` (ISO-Datum oder `null`) und `estimated_minutes` (ganze Minuten 1–60000 oder `null`) in jedem Punkt. Fehlende ältere Angaben werden leer ergänzt. Ungültige Werte werden vor einem Import abgewiesen. Beide Angaben sind unabhängig von Fälligkeit und Tagesauswahl. Gruppen und Überschriften tragen keine Planung. [Vollständige Regeln einschließlich Wiederholungen, Vorlagen und Export](37_PLANUNG_UND_AUFWAND_3.14.0.md).
