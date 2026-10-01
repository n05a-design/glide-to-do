# Daten, Backups und Migration – Glide

Stand 01.10.2026 · Glide 3.32.3 · Aufgabenformat 20

## Format 20: Beziehungen, Zeit, Pixelsymbole, Archiv, kleine Zeichnungen

Der aktuelle Schreiber verwendet Aufgabenformat **20**. Es bündelt alle
bestandsändernden Pakete des Modernisierungskatalogs (E-02).

**Punkte:**

- `links` – bis 50 Kennungen;
- `blocked_by` – bis 50 Kennungen, kreisfrei; Kreise löst das Laden auf;
- `planned_time` – `HH:MM`, nur mit Bearbeitungstag;
- `time_spent_minutes` – 0 bis 1 000 000;
- `done_at` – beim Abhaken gesetzt, beim Wiederöffnen geleert.

**Listen und Ordner:**

- `icon` – Zeichendokument 16 × 16;
- `archived`, `archived_at`.

**Zeichnungen:** Flächen mit 16, 32 oder 64 Zellen tragen
`drawing.format_version` 2. 128 bleibt Version 1 und damit für 3.29 lesbar,
solange der Bestand kein Format 20 trägt.

**Listen- und Ordnerarten in Format 20:**

- `list_kind`: `tasks`, `note`, `drawing`, `page` (Seite, seit 26.09.2026)
  und `gallery` (Galerie, seit 27.09.2026). „Seite“ und „Galerie“ kamen
  additiv in das noch unveröffentlichte Format 20.
- `folder_kind`: `standard` (Ordner), `library` (Bibliothek) und `journal`
  (Notizbuch).
- **Regel seit 29.09.2026:** Jede weitere Listen- oder Ordnerart hebt die
  Formatnummer. Nur so erkennt eine ältere Fassung den Bestand als neuer
  und öffnet ihn schreibgeschützt, statt ihn zu überschreiben.

**Automatische Sicherungen** (`backups/liste_backup_*.json`, seit 29.09.2026):

- Eine Sicherung entsteht nur, wenn sich der Inhalt seit der neuesten
  Sicherung geändert hat (SHA-256-Vergleich). Der Fünf-Minuten-Takt und
  jedes Speichern nach mindestens zwei Minuten prüfen das. Bis dahin legte
  der Takt auch ohne Änderung Kopien an. Nach 50 Minuten Ruhe waren dann alle
  zehn Sicherungen gleich, und ältere Stände waren gelöscht.
- **Aufbewahrung:**
  - die zehn neuesten immer;
  - weitere, solange sie jünger als 30 Minuten sind;
  - höchstens 40.
  - Zusätzlich je Kalendertag der letzte Stand, 14 Tage lang.
- Vorsicherungen einer Umstellung (`liste_vor_format*`, `liste_unlesbar_*`,
  `liste_vor_titelkuerzung_*`) und `vor_import_*.glidebackup` werden nie
  rotiert.

**Migration und Rückfall:**

- Vor dem ersten Speichern einer älteren Datei entsteht bytegenau und
  unrotiert `backups/liste_vor_format20_<Zeitstempel>.json`. Scheitert sie,
  bleibt die Originaldatei unverändert.
- **Glide 3.29 und älter nach der Umstellung nicht mehr starten.** Sie melden
  „Speicherdatei beschädigt oder ungültig“, beginnen mit einem leeren Bestand
  und überschreiben die Format-20-Datei bei der ersten Eingabe. Nachgewiesen
  am 25.09.2026 mit einer Kopie eines echten Bestands. Zurück zu 3.29 führt
  nur die Vorsicherung – in einer getrennten Ablage und ohne spätere
  Änderungen.
- Nicht nur 3.29: Auch die Zwischenstände von 3.30 vor dem 26. bzw.
  27.09.2026 kennen die Listenarten „Seite“ und „Galerie“ nicht. Sie
  behandeln einen Bestand mit einer Seite oder Galerie als unlesbar und
  beginnen leer. Alte Fassungen deshalb nur mit einer getrennten Ablage
  (`GLIDE_DATA_DIR`) starten.
- Ab 3.30 gilt beim Öffnen (Startprüfung, ergänzt am 29.09.2026):
  - Ein Bestand aus einer **neueren** Version öffnet schreibgeschützt. Glide
    zeigt einen leeren Bestand, speichert nichts und nennt den Grund. Eine
    **unbekannte Listenart** gilt ebenso als neuer.
  - Ein **älteres** Format wird gleich beim Start umgestellt, mit den
    bytegenauen Vorsicherungen `liste_vor_format<N>_*.json` und einem
    Hinweis. Bis zum 29.09.2026 geschah das erst bei der ersten Eingabe.
  - Zwischendateien eines abgebrochenen Schreibvorgangs
    (`.glide-json-*.tmp`, älter als zehn Minuten) räumt der Start auf.
  - Eine **unlesbare** Datei wird zuerst als
    `backups/liste_unlesbar_<Zeitstempel>.json` gesichert; erst danach darf
    ein leerer Bestand sie ersetzen. Gelingt die Kopie nicht, bleibt die
    Sitzung schreibgeschützt.
  - `data_format_written` in den Einstellungen merkt das zuletzt hier
    geschriebene Format, sobald der Bestand echten Inhalt hat. Ist die Datei
    älter, warnt Glide: Eine ältere Version hat gespeichert oder jemand hat
    eine ältere Datei hineinkopiert. Frühere Stände holt Datei › Sicherung ›
    „Komplettbackup laden …“ aus dem Backup-Ordner.
- Formate 4–20 und Legacy 2 bleiben lesbar.

**Transportwege:**

- Kopieren, Duplizieren und additiver Import vergeben neue Kennungen und
  ziehen `links` und `blocked_by` nach.
- Aufgaben-, Teil- und App-Backup, Vorlagen, Papierkorb und Austausch führen
  alle Felder mit.
- Benannte Zwischenstände einer Zeichnung sind Anhänge (MIME
  `application/vnd.glide.drawing-snapshot+json`) und reisen mit den Anhängen.

**Einstellungen:** Das Format bleibt 2; alle neuen Schlüssel sind additiv,
fehlende Werte ergeben das Verhalten von 3.29.

**Pinnwandabschnitt `pinboards`:** Ebenfalls additiv; er reist wie seit 3.24
in App- und Komplettbackup. Neu sind:

- Spaltenboard, Karteninhalt und Kartenfarbe;
- Bereiche (neue Kennungen beim additiven Import);
- Verbindungen mit Beschriftung, Strichart und Farbe;
- Zeichnungskarten `page:<Seitenkennung>`;
- Hintergrund.

Eine ältere Fassung liest die Pinnwand als freie Fläche.

Referenz-Fixture: `tests/fixtures/current_v20/reference_v20.json`.
Vollständiger Vertrag: [Modernisierung 3.30](66_MODERNISIERUNG_3.30.0.md),
Abschnitte 3 bis 5.

## Format 19: Zeichnungsseiten

Seit 3.29.0 (heute gilt Format 20, siehe oben) verwendet Glide Aufgabenformat **19**. `list_kind` kennt die
Werte `tasks`, `note` und `drawing` (zentrale Registrierung `LIST_KINDS`). Nur
Zeichnungsseiten tragen zusätzlich `drawing` – das kanonische Zellmodell
`glide.drawing` Version 1 mit 128 Hexzeilen und höchstens 256 Farben – und
`drawing_reference` (`null` oder Verweis auf einen PNG-Anhang derselben Liste
mit Rahmenwerten). Ansichtszustände wie Zoom, Werkzeug oder Raster werden nicht
gespeichert.

Vor dem ersten Speichern einer älteren Datei entsteht die bytegenaue,
unrotierte Sicherung `backups/liste_vor_format19_<Zeitstempel>.json`. Scheitert
sie, bleibt die Originaldatei unverändert. Formate 4–20 und Legacy 2 bleiben
lesbar. Eine unbekannte Listenart in einer Format-19-Datei, ein ungültiges
Zellmodell oder Punkte in einer Zeichnung werden vor jeder Bestandsänderung
abgelehnt; ältere Formate werden wie bisher gelesen. Glide 3.28 und älter
können Format 19 nicht öffnen.

Aufgabenbackup, Teilbackup, App-Backup, Austausch (ohne Datei), Vorlagen,
Papierkorb, Wiederherstellung und Duplizieren führen Zellmodell und
Referenzverweis mit; das Referenz-PNG reist als referenzierter Anhang. Beim
additiven Import folgt der Verweis der neu vergebenen Anhangskennung. Der
Änderungsverlauf enthält nur den SHA-256 des Zellmodells. Vollständiger
Vertrag: [Zeichnungsseite 3.29](65_ZEICHNUNGSSEITE_3.29.0.md).

## Format 18: Tagebuch

Aufgabenformat **18** führte Tagebuch-Metadaten ein. Ordner tragen
`folder_kind` (`standard` oder `journal`). Jede Liste trägt das normalisierte
Wörterbuch `journal` mit `favorite`, `mood`, `location`, `moment_date` und
`prompt`. Die erlaubten Stimmungen sind fest begrenzt; Ort und Impuls werden
gekürzt, ein Momentdatum muss ISO-Datum sein. Fehlende Felder älterer Dateien
werden additiv ergänzt und verändern Aufgaben sowie Rich-Text-Inhalt nicht.

Vor dem ersten Speichern einer älteren Datei entsteht die bytegenaue,
unrotierte Sicherung `backups/liste_vor_format18_<Zeitstempel>.json`. Scheitert
die Sicherung, wird die Originaldatei nicht überschrieben. Formate 4–20 und das
historische Format 2 bleiben importierbar; ältere Glide-Versionen dürfen eine
Format-18-Datei nicht schreibend öffnen.

Aufgabenbackup, App-Backup, Austausch, Papierkorb, Wiederherstellung und
Duplizieren bewahren Ordnerart und Tagebuch-Metadaten. Persönliche Gismo-Werte
bleiben dagegen in `settings.json` und sind nicht Teil eines Aufgabenbackups.
Der vollständige Bedienvertrag steht in
[Tagebuch und UI 3.28](59_TAGEBUCH_UND_UI_3.28.0.md).

## Format 17: Notizlisten

Format 17 führte Notizlisten ein. Einstellungen und Vorlagen behalten ihre Formatnummer **2**.

Jede Liste enthält `list_kind` (`tasks` oder `note`) und `rich_note` mit `text`, `spans` und `links`. Ein Formatierungsbereich besteht aus `tag`, `start` und `end`; die Grenzen sind Python-Zeichenpositionen im gespeicherten Text, keine Tk-Indizes. Damit bleiben Umlaute und Zeichen außerhalb der BMP über einen Neustart erhalten. Fehlende Felder alter Listen ergeben eine Aufgabenliste mit leerem Notizdokument. Der Wechsel zurück zur Aufgabenliste bewahrt die Notiz.

Die Validierung begrenzt ein Dokument auf 1.000.000 Zeichen und 10.000 Bereiche. Links sind explizite HTTP-, HTTPS- oder mailto-Verweise. Die Anwendung öffnet sie erst nach einer Benutzeraktion. Format-Tags werden nicht als Suchtext verwendet.

Vor der ersten Format-17-Speicherung entstand die bytegenaue, unrotierte Sicherung `backups/liste_vor_format17_<Zeitstempel>.json`. Ältere Backups bleiben importierbar; ältere Glide-Versionen können neue Format-17-Dateien nicht lesen. Ein Rückwechsel braucht deshalb die Originalsicherung in einem getrennten Datenordner; spätere Änderungen fehlen darin.

Aufgabenbackups und Glide-Austauschdateien erhalten den strukturierten Notizinhalt. TXT und Markdown enthalten den Notiztext, bewahren aber nicht alle Formatierungsbereiche. Der App-Verlauf bleibt Teil des Aufgabenbestands und enthält höchstens 15 Einträge aus den letzten 15 Tagen; er ersetzt kein Undo.

## Vorherige Formaterweiterungen

Format 16 ergänzte bei unveränderten Einstellungen **2** und Vorlagenformat **2** am Punkt das additive Feld `checklist`: eine Liste kurzer Schritte mit Text und Zustand. Fehlt das Feld, trägt der Punkt keine Checkliste; Format-15-Dateien bleiben unverändert gültig. Die UI nennt Erinnerungen jetzt Benachrichtigungen; gespeicherte Felder und APIs wie `reminder`, `reminder_attention`, Zustellbelege und Aufschub bleiben unverändert. Neuer additiver boolescher Einstellungswert seit 3.22: `sidebar_visible`, Standard `true`.

**3.23.0 ändert kein Datenformat.** Aufgabenformat bleibt 16, Einstellungen 2, Vorlagen 2; es entsteht keine Formatsicherung und kein Rückwechselproblem. Hinzu kommen ausschließlich additive Einstellungswerte:

| Wert | Inhalt | Standard | Verhalten bei fehlendem Wert |
|---|---|---|---|
| `design` | Gewähltes Design aus `DESIGNS` | `glass_dark` | wird beim Laden aus `theme`, `color_mode` und `glass_mode` abgeleitet |
| `list_detail_mode` | Anzeigemodus der Listenansicht | `standard` | `standard` |
| `board_focus` je Pinnwand | Fokusmodus der Arbeitsfläche | `false` | `false` |
| `connections` je Pinnwand | Verbindungen zwischen Karten | `[]` | leere Liste |
| `table_column_widths` je Ansicht | gespeicherte Spaltenbreiten | – | berechnete Breite |

Die Designmigration ist verlustfrei und in beide Richtungen verträglich: Beim Laden entsteht `design` aus den bisherigen Feldern `theme`, `color_mode` und `glass_mode`; beim Speichern werden diese drei Felder als abgeleitete Spiegelwerte mitgeschrieben. Eine Einstellungsdatei aus 3.23.0 bleibt deshalb für 3.22.0 lesbar, und ein gespeicherter Dopamin- oder Glasmodus geht bei keinem Wechsel verloren. Unbekannte Designschlüssel fallen auf `DESIGN_DEFAULT` zurück, ohne die übrige Datei zu verwerfen.

Pinnwandverbindungen werden weiterhin in `settings.json` gespeichert. Aktuelle portable Backups übernehmen die zugehörigen Pinnwände zusätzlich und ordnen ihre Verweise beim Import neu zu; die ältere Aussage, Verbindungen seien grundsätzlich nicht enthalten, gilt dafür nicht mehr. Verweise auf entfernte Karten werden beim Normalisieren verworfen; die Obergrenze liegt bei `MAX_CONNECTIONS` = 200 je Pinnwand.

Das Austauschformat `.glideexchange` ist ein **Transportformat, kein Speicherformat**. Es ersetzt weder Aufgabenbackup noch Datenordnerkopie: Import erzeugt neue Objekte oder trifft vorhandene über stabile IDs, verändert aber nie die Ablagestruktur der Nutzdaten. Grenzen vor dem Schreiben und Lesen: 12 MB, 5000 Punkte, Verschachtelungstiefe 12. Details: [Austauschformat](52_AUSTAUSCHFORMAT_3.23.0.md).

Vor dem ersten Speichern von Aufgaben vor Format 14 entsteht die unrotierte unveränderte Originalkopie `backups/liste_vor_format14_<Zeitstempel>.json`. Bei Fehler wird nicht gespeichert. Formate 4–20 und Legacy 2 bleiben lesbar. Glide 3.13 und ältere Versionen können Format 14 nicht lesen, Glide 3.18 und ältere nicht Format 15, Glide 3.21 und ältere nicht Format 16. Vor dem ersten Speichern in Format 16 entsteht `backups/liste_vor_format16_<Zeitstempel>.json`. Für einen Rückwechsel die alte Sicherung in einer separaten Ablage verwenden; sie enthält keine späteren Änderungen.

| Ablage | Inhalt | Transport |
|---|---|---|
| `liste_speicher.json` | Ordner, Listen, Aufgaben, Labels, Wiederholungen, Benachrichtigungen, Papierkorb und Änderungsverlauf | Aufgabenbackup |
| `settings.json` | Design, Profil, Anzeige, Historien, `reminder_attention`, `sidebar_visible`, Anzeigemodus, Spaltenbreiten, Pinnwandverbindungen | Datenordnerkopie |
| `vorlagen.json` | System-/eigene Vorlagen | `.glidetemplates` oder Datenordnerkopie |
| `attachments/`, `backups/` | Lokale Anhänge und Sicherungen | referenzierte Anhänge in Aufgabenbackup; vollständige Datenordnerkopie |
| `glide.lock` | Temporäre Belegung | nicht kopieren |
| `datenordner.json` | Gerätebezogener Ablagezeiger | nicht im Aufgabenbackup |

Ein `.glidebackup` ist ein ZIP aus `data.json` und referenzierten Anhängen. Vollrestore ersetzt erst nach Validierung und Sicherung. Additiver Import erzeugt neue IDs und erhält den bisherigen Bestand. Teilbackups umfassen vollständige Zweige einschließlich leerer Unterordner. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden weiter geprüft. Einstellungen und separater Vorlagenkatalog sind nicht Teil eines Aufgabenbackups.

Die frei wählbare Ablage liegt außerhalb des Programms. `GLIDE_DATA_DIR` hat für Tests Vorrang; andernfalls gelten Plattformstandard und optional `datenordner.json`. Ein Datenordnerwechsel kopiert in ein leeres Ziel oder öffnet einen vorhandenen Bestand; die Quelle bleibt erhalten. Erkannte Fremdbelegung verhindert Speichern. Die Sperre ersetzt keinen verteilten Synchronisationsdienst.

Historischer vollständiger [Zustellvertrag Format 13](archiv/31_ERINNERUNGEN_3.8.0.md) gilt technisch weiter. Aktuelle [Bedienung](archiv/32_UI_UND_BEDIENUNG_3.9.0.md) und [QA](07_QA_BERICHT.md).

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt `today_plan`; 3.13 ergänzt `table_columns` für die listenspezifische Tabellenansicht. Diese Werte sind persönliche Einstellungen, werden beim Laden bereinigt und sind kein Bestandteil eines Aufgabenbackups. Seit 3.14 führen Aufgabenformat 14, Backups und Vorlagen zusätzlich Bearbeitungstag und geschätzten Aufwand mit. [Bedienung 3.13](archiv/36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](archiv/35_MEIN_TAG_3.12.0.md).

3.21 ergänzt den Kalenderimport. Er liest eine gewählte Datei, schreibt selbst keine Datei und legt keine eigene Datenhaltung an; Punkte entstehen über `new_item` und damit durch dieselbe Prüfung wie handangelegte. Aufgabenformat 15 bleibt unverändert, bestehende Punkte werden nie überschrieben, und der Vorgang ist ein einzelner Rückgängig-Schritt einschließlich der dabei angelegten Labels. Eigene UIDs werden erkannt und übersprungen, damit der Rundlauf mit der Ausgabe aus 3.20 keine Kopien anlegt. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

3.20 ergänzt die Kalenderausgabe. Sie schreibt ausschließlich ICS-Dateien an ein gewähltes Ziel, atomar über eine Temporärdatei; Nutzdatendateien sind als Ziel ausgeschlossen. Aufgabenformat 15, Einstellungen und Vorlagen bleiben unberührt, und es entsteht kein Verlaufseintrag – eine Ausgabe ist keine Änderung. [Bedienung 3.20](archiv/44_KALENDERAUSGABE_3.20.0.md).

3.19 hebt das Aufgabenformat auf **15** und ergänzt das Feld `history` neben den Aufgabenfeldern. Ein Bestand im Format 14 oder älter wird beim ersten Speichern gehoben und erhält ein leeres Protokoll; vorher entsteht die unveränderte Kopie `liste_vor_format15_<Zeitstempel>.json` im Backup-Ordner. Ein defektes oder fremdes `history`-Feld wird beim Laden verworfen, ohne die Aufgaben zu berühren. Komplettbackup und App-Backup führen den Verlauf mit, ein Teilbackup als Auszug nicht; portable Backups werden weiterhin ab Format 4 gelesen, ein Format-15-Backup ist für ältere Fassungen erwartungsgemäß nicht lesbar. Rückgängig stellt den Bestand wieder her und lässt das Protokoll stehen. [Bedienung 3.19](archiv/43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 ergänzt den CSV-Import. Er liest eine gewählte Datei, schreibt selbst keine Datei und legt keine eigene Datenhaltung an; die entstehenden Punkte gehen durch `new_item` und damit durch dieselbe Prüfung wie handangelegte Punkte. Aufgabenformat 14, Einstellungen und Vorlagen bleiben unberührt, bestehende Punkte werden nie überschrieben, und der Vorgang ist ein einzelner Rückgängig-Schritt einschließlich der dabei angelegten Labels. [Bedienung 3.18](archiv/42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt die Druckausgabe. Sie schreibt ausschließlich HTML-Dateien an ein gewähltes Ziel oder in den temporären Ordner, atomar über eine Temporärdatei; Nutzdatendateien sind als Ziel ausgeschlossen. Aufgabenformat 14, Einstellungen und Vorlagen bleiben unberührt. [Bedienung 3.17](archiv/41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt das vollständige App-Backup. Das Archiv ist dasselbe ZIP wie ein Komplettbackup; im JSON steht zusätzlich der Abschnitt `app_backup` mit `format_version`, `settings` (ohne Tageshistorien, mit `theme`), `templates` und `activity`. Aufgabenformat 14 bleibt unverändert, und weil der Abschnitt neben den Aufgabenfeldern liegt, bleibt die Datei für ältere Fassungen ein gültiges Aufgabenbackup. Vor dem Ersetzen entstehen `vor_import_*.glidebackup`, `settings_vor_restore_*.json` und `vorlagen_vor_restore_*.json`. Ansichtsverweise werden nur zusammen mit den Aufgaben desselben Archivs übernommen. [Bedienung 3.16](archiv/40_APP_BACKUP_3.16.0.md).

3.15 ergänzt die persönliche Einstellung `daily_capacity_minutes` (ganze Minuten 0–1440, Vorgabe 0 = kein Vergleich). Ein fehlender, beschädigter oder fremder Wert führt auf 0 zurück. Der betrachtete Planungstag wird nicht gespeichert, Tagesbilanzen werden nicht abgelegt: Jede Summe entsteht bei der Anzeige aus dem aktuellen Bestand. Aufgabenformat 14 bleibt unverändert; Aufgabenbackups enthalten weder Kapazität noch Ansichtszustand. [Bedienung 3.15](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

3.14 ergänzt `planned_date` (ISO-Datum oder `null`) und `estimated_minutes` (ganze Minuten 1–60000 oder `null`) in jedem Punkt. Fehlende ältere Angaben werden leer ergänzt. Ungültige Werte werden vor einem Import abgewiesen. Beide Angaben sind unabhängig von Fälligkeit und Tagesauswahl. Gruppen und Überschriften tragen keine Planung. [Vollständige Regeln einschließlich Wiederholungen, Vorlagen und Export](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md).
