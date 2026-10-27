# Daten, Backups und Migration – Glide

Stand 27.10.2026 · Glide 3.47.0 · Aufgabenformat 26 · Einstellungen 2 · Vorlagen 2 · Austauschformat 2 (Erstellen 1 lesbar, Änderungsvorschläge 2)

**3.44.0 (22.10.2026):** Aufgabenformat 26 (FP-02), FP-01 und die Schutzrunde WA-27–WA-30 sowie die neuen obersten Einstellungsnamespaces von FP-03/FP-04 sind als Python-Fassung geliefert. Die früher nachgestellten Grenzen A32/A33/A34/A35/A36 haben gezielte Schutzprüfungen und Gegenproben ([Schutznachweis](../tests/qa-3.43.1/schutzrunde_2026-10-18/README.md)); die historische Analyse beschreibt den Zustand davor. Eigenständige Pakete (3.42.0) lesen Format 26 nur schreibgeschützt; Mac-Bundle/Pakete 3.44.0 und native Abnahmen bleiben offen ([Prüf- und Lieferstand](07_QA_BERICHT.md)).

Verbindlicher Datenvertrag. Am 03.10.2026 um das Austauschformat (bisher Vertrag 52) ergänzt und um die Verweise auf gelöschte Einzelverträge bereinigt; die Vorfassungen trägt Git. Formate 4–26 und Legacy 2 bleiben lesbar.

## Ablage

| Datei | Inhalt | Transport |
|---|---|---|
| `liste_speicher.json` | Ordner, Listen, Aufgaben, Labels, Wiederholungen, Erinnerungen, Papierkorb, Änderungsverlauf | Aufgabenbackup |
| `settings.json` | Design, Profil, Anzeige, Startseite, Pinnwände (`pinboards`), Bereichszuordnung, Historien | App-Backup oder Datenordnerkopie |
| `vorlagen.json` | System- und eigene Vorlagen | `.glidetemplates`, App-Backup |
| `attachments/` | lokale Kopien der Anhänge | referenzierte Anhänge im Backup |
| `backups/` | automatische Sicherungen und Vorsicherungen | Datenordnerkopie |
| `window.conf`, `glide.lock`, `datenordner.json` | Fenster, Belegung, gerätebezogener Ablagezeiger | nicht übertragen |

- Der Datenordner liegt außerhalb des Programms. `GLIDE_DATA_DIR` hat Vorrang (Tests), sonst Plattformstandard und optional `datenordner.json`. Ein Wechsel kopiert in ein leeres Ziel oder öffnet einen vorhandenen Bestand; die Quelle bleibt.
- `glide.lock` verhindert gleichzeitiges Schreiben zweier Instanzen; erkannte Fremdbelegung verhindert Speichern – der Aufgabendatei ebenso wie von Einstellungen, Fenstergröße und Vorlagen. Eine beschädigte oder unlesbare Sperre öffnet schreibgeschützt; die Warnung beim Start bietet an, sie bewusst zu übernehmen. Eine verschwundene Sperre legt Glide beim nächsten Schreiben neu an (Schutzrunde WA-30). Die Sperre ersetzt keinen Synchronisationsdienst. Die lokale OS-Sperre auf `glide.lock.acquire` schützt auch die Übernahme verwaister Sperren; sie ist kein verteilter Konsens zwischen Rechnern.
- Gespeichert wird sofort und atomar (Temporärdatei, `replace_with_retry`; unter Windows bis 1,5 s Warten bei Dateisperren). Liegengebliebene `.glide-json-*.tmp`, älter als zehn Minuten, räumt der Start auf.

## Größenbudget und Speicherstatus (lokaler Kandidat)

WA-40/WA-47, Quellkandidat 25.10.2026, noch keine Lieferung: Das gemeinsame JSON-Budget beträgt **32 MiB** wie die bestehende Grenze für `data.json` in vollständigen Sicherungen. Aufgaben, Einstellungen, Vorlagen, ihre Import-/Startleser und die Formatvorsicherung prüfen die Dateigröße vor dem JSON-Parse. Der begrenzte Leseweg prüft zusätzlich die tatsächlich gelesenen Bytes; Wachstum nach der ersten Dateiprüfung wird abgefangen. UTF-8 und vorhandene BOM werden gelesen; der Schreiber zählt UTF-8 einschließlich der Windows-Zeilenenden. Alte Dateibytes, atomarer Austausch, Formatsicherungen und deren Cache bleiben erhalten.

Eine Überschreitung der Hauptdatei führt zu einem leeren, ausdrücklich schreibgeschützten Start mit Speicherhinweis; die Originaldatei wird weder als beschädigt umkopiert noch überschrieben. Bei zu großen Einstellungen oder Vorlagen verwendet die Oberfläche ihre Vorgaben, schützt aber die betroffene Datei bis zum Neustart gegen Schreiben. Auch eine nach dem Laden gewachsene Zieldatei wird vom atomaren Schreiber geschützt. Eine zu große neue Kodierung ersetzt keine bestehende Datei. Ein Retry hebt weder Größen- noch Sperrschranken auf.

Der Speicherstatus hält Aufgaben-, Einstellungs-, Vorlagen- und Sicherungsfehler getrennt im Arbeitsspeicher; Erfolg löscht nur den passenden Fehler. Fehlgeschlagene stille Speicherungen werden protokolliert und mit einem nicht modalen Hinweis zugänglich. Die Reserveanzeige verwendet die Summe der drei gespeicherten JSON-Dateien als Frühwarnung ab 80 % des Budgets. Die tatsächlichen Sicherungsbytes bleiben beim Export maßgeblich; Anhänge haben weiterhin ihre eigenen Archivgrenzen. Ein Import ohne erfolgreiche Vorab-Sicherung ändert den Bestand nicht. Keine neue Formatnummer, Einstellung oder Laufzeitabhängigkeit. [Verhalten](20_FUNKTIONEN.md#speicherstatus-und-sicherungsreserve-wa-40wa-47-lokaler-kandidat), [Prüfgrenzen und Belege](../tests/qa-3.44.0/speicherstatus_2026-10-25/README.md).

## Format 26 (FP-02, seit 3.44.0)

Das FP-02-Paket führt Format 26 ein; geliefert mit 3.44.0. Neue Rhythmusformen speichern `repeat = {"art": "serie", "rrule": "…", "start": "JJJJ-MM-TT", "ende": null}`. Erlaubt sind Wochen mit mehreren Tagen, Monats-/Jahresintervalle (1–365), monatliche Position 1–5 oder letzte, letzter Monatstag und letzter Werktag (Mo–Fr, ohne Feiertage). Die sechs bisherigen Arten und ihre Felder bleiben ohne aktivierte Zusätze unverändert.

Alle Arten können optional `bezug: "erledigt"`, `pausiert: true` und `rest: 1..10000` tragen. Fehlende Werte bedeuten Fälligkeitsbezug, laufende Serie und unbegrenzte Anzahl. `rest` zählt das aktuelle Vorkommen mit. Eine Erledigung oder ein übersprungener Termin verbraucht ein Vorkommen; bei verpassten Terminen wird jedes übersprungene Vorkommen gezählt. Beim letzten Erledigen bleibt die Aufgabe abgeschlossen und verliert wie beim bisherigen Serienende ihre Regel. Pausierte Regeln erzeugen weder beim Erledigen noch beim Überspringen einen Folgetermin; die aktuelle Aufgabe und ihre Erinnerung bleiben erhalten. Beim Wiederaufnehmen wird kein Abschluss nachgebucht.

Bei Erledigungsbezug wird ab dem tatsächlichen Erledigungstag neu gerechnet und der Anker entsprechend fortgeschrieben; Überspringen bleibt im Terminraster. Neue Intervallserien lassen fehlende Datumstage aus; die alten Monats-/Jahresarten behalten ihre Klemmregel. Die Vorschau ist begrenzt und rein lesend. Bei Erledigungsbezug nennt sie ausdrücklich ihre Annahme: heute erledigt, danach pünktliche Erledigung.

Vor dem ersten Überschreiben einer älteren Datei entsteht die bytegleiche unrotierte `liste_vor_format26_*.json`. Ein Kopierfehler verhindert das Schreiben. Neue Rhythmusformen und Steuerfelder werden unter älteren Formatnummern sowie in unversionierten Altlisten abgewiesen. Der unveränderte frühere Leser 3.43.1 (Speicherstufe 25, jetzt im 07-Archiv) zeigt für den neuen Bestand seinen bestehenden leeren Schreibschutzmodus und speichert nichts. Format 26 wurde vor dem Phasenabschluss vervollständigt und erst mit 3.44.0 ausgeliefert. Beispiel-, Rundgang- und Showcase-Fixtures wurden beim Versionswechsel wie üblich neu erzeugt und tragen Format 26; die versionierten Altfixtures `current_v<N>` bleiben unverändert. `current_v26/reference_v26.json` enthält Rhythmus und Steuerfelder.

TXT beschreibt und liest Rhythmus, Bezug, Pause und Restanzahl. ICS übernimmt statische Reihen einschließlich Intervall, Monatsposition und wirksamer Anzahl bzw. Enddatum. COUNT und UNTIL werden niemals gemeinsam ausgegeben; bei zwei Grenzen wird die tatsächlich mögliche Anzahl berechnet. Die Folge wird beim Import erhalten, einschließlich echter RFC-Monats-/Schalttagreihen, die die alte Fassung noch abweisen musste. Pausierte, vom Erledigungstag abhängige oder nicht zu DTSTART passende Regeln werden nicht als statische Kalenderserie angenähert: Beschreibung und sichtbarer Hinweis benennen die Grenze. CSV bleibt hinsichtlich vollständiger Serien begrenzt. Die vollständige Glide-Sicherung enthält sämtliche Felder und bleibt der verlustfreie Rückweg. Einstellungen 2, Vorlagen 2 und Austauschformat 2 bleiben unverändert. [Prüfnachweis](../tests/qa-3.43.1/wiederholungsregeln_2026-10-21/README.md).

## Format 25

Seit 3.41.0 tragen aus Notion übernommene Seiten `notion_source` (Version 1): `key` (`notion:` mit 32 Hexzeichen aus dem Dateinamen oder `path:` mit SHA-256 des Archivpfads), `target_id` (die Glide-Seite), `source_hash` (Inhalt der Quelle), `local_hash` (übernommener Glide-Stand) und `source_path` (relativer Archivpfad ohne `..`, Laufwerk oder Steuerzeichen). Ordner für Unterseiten tragen `notion_source_key`. Jede Quelle gehört zu genau einer lebenden Seite; Kopien und Duplikate erhalten keine Zuordnung, Papierkorb und Wiederherstellung behalten sie. Unbekannte oder widersprüchliche Zuordnungen werden abgewiesen.

Vor dem ersten Format-25-Schreiben wird die alte Datei unverändert nach `liste_vor_format25_*.json` kopiert; ein Kopierfehler verhindert das Schreiben. Die unveränderte 3.40.0 (Format 24) öffnet Format 25 schreibgeschützt. Ein Bestand mit Format 24 darf keine Zuordnungsfelder tragen. Der Referenzbestand `tests/fixtures/current_v25/reference_v25.json` enthält eine zugeordnete Seite und einen Ordner. Seitenwiederherstellung und Notion-Import legen vor der Übernahme eine vollständige Sicherung `vor_seitenrestore_*.glidebackup` bzw. eine Vorsicherung an. Migrations-, Altleser- und Schreibproben in `test_import3410.py`.

## Format 24

Seit 3.40.0 tragen Zeichnungsseiten `animation` im Dokumentformat `glide.animation` Version 1: quadratische Fläche 16/32/64/128, gemeinsame `duration_ms` und 1–120 Bilder (`frames`) mit eindeutiger stabiler `id`, `drawing` und optionaler eigener `duration_ms`. Dauern sind ganze 20–60.000 ms; alle Bilder haben dieselbe Fläche. Das vorhandene Feld `drawing` enthält das erste Bild als statische Vorschau; ein Widerspruch oder eine beschädigte Folge wird abgewiesen und nie durch eine leere Zeichnung ersetzt.

Alte Zeichnungen werden verlustfrei zu einem Bild. Kopie, Papierkorb, Rückgängig/Wiederholen, Verlauf, Sicherungen, Vorlagen und normalisierte Bestände erhalten die vollständige Folge; Bildcache und Startseite erkennen auch Änderungen an späteren Bildern und Dauern. Der Zeichenverlauf bleibt je Bild getrennt, ein Struktur-Rückgängig holt die ganze Folge zurück. Zwischenstandsanhänge enthalten eine vollständige `glide.animation`; bisherige `glide.drawing`-Anhänge bleiben lesbar. Austausch-Erstellen 2 bewahrt Bildfolgen, Erstellen 1 bleibt lesbar; Änderungsvorschläge bleiben Version 2.

Vor dem ersten Format-24-Schreiben wird die alte Datei unverändert nach `liste_vor_format24_*.json` kopiert. Ein Kopierfehler verhindert das Schreiben; der ursprüngliche Bestand bleibt bytegleich. Die unveränderte 3.39.1 (Format 23) öffnet Format 24 schreibgeschützt. Der Referenzbestand `tests/fixtures/current_v24/reference_v24.json` enthält eine Bildfolge mit drei Bildern, gemeinsamer und eigener Dauer; historische Referenzen und alte Releaseplanungen behalten ihre Formatnummer. Einstellungen 2 und Vorlagenhülle 2 bleiben, enthaltene neue Aufgabenbackups tragen Format 24. Migrations-, Altleser- und Dateischreibproben in `test_animation3400.py`.

## Format 23

Seit 3.33.18 tragen Seiten optional `live_lists` (höchstens 20 eindeutige `glide://list/<id>`-Ziele) und `cover`. Die Live-Liste ist eine abgeleitete Ansicht der Originalaufgaben samt Unteraufgaben; sie erzeugt keine Kopien und kann nicht rekursiv andere Live-Listen erweitern. Fehlende und gelöschte Ziele behalten ihre Kennung. Archivierte Quelllisten, auch unter archivierten Ordnern, bleiben sichtbar und werden nicht verändert.

Ein Titelbild ist `{"kind":"image","attachment":"<id>"}` für einen lokalen Anhang derselben Seite oder `{"kind":"drawing","document":<glide.drawing>}` für eine unabhängige Pixelzeichnung. Keine externen Bild-URLs. Ungültige Werte werden abgewiesen; ein fehlender Bildanhang zeigt einen Platzhalter. Die Anhangskennung folgt beim Import genau einmal ihrer neuen Kennung, Live-Listen folgen der gemeinsamen Containerzuordnung. Papierkorb, Wiederherstellung, Kopie, Sicherung und Undo erhalten beide Felder; der Vergleich für Verlauf/Aktivität berücksichtigt Änderungen.

Vor dem ersten Schreiben von Format 23 wird die alte Datei bytegenau nach `liste_vor_format23_*.json` kopiert. Ein Kopierfehler verhindert das Überschreiben. Die unveränderte 3.33.17 (Format 22) erkennt den neuen Bestand und öffnet schreibgeschützt; Start- und Speicherprobe prüfen dieselben Dateibytes. Referenz-Fixture: `tests/fixtures/current_v23/reference_v23.json`. Einstellungen 2 und Vorlagenformat 2 bleiben erhalten; enthaltene Vorlagen-Backups tragen Format 23.

## Format 22

Seit 3.33.17 erweitert Format 22 den Bestand um typisierte lokale Beziehungen. Listen und Aufgaben tragen optional `references`, höchstens 200 eindeutige lokale URLs `glide://list/<id>` oder `glide://item/<id>`. Kennungen sind URL-kodiert; die Namensräume bleiben getrennt. Notiz-/Seitentext verwendet dieselben Ziele in den vorhandenen `rich_note.links` und aktiven Linkspannen. Ungültige Typen, URLs oder Mengen werden beim Laden/Import abgewiesen; fehlende Ziele bleiben als gültige Kennungen erhalten. Rückverweise sind eine abgeleitete Sicht.

Vor dem ersten Schreiben entsteht eine bytegenaue `liste_vor_format22_*.json`-Kopie. Kopierfehler verhindert das Überschreiben. Die unveränderte Vorversion 3.33.16 (Format 21) erkennt Format 22 und öffnet schreibgeschützt; eine tatsächliche Start-/Speicherprobe prüft unveränderte Dateibytes. Die Wochenplanung verwendet vorhandene Felder `planned_date`, `planned_time` und `estimated_minutes`; Einstellungen, Vorlagen und Austausch bleiben unverändert. Referenz: `tests/fixtures/current_v22/reference_v22.json`.

Additiver Import und Vorlagenkopie remappen enthaltene Listen- und Aufgabenkennungen getrennt, auch in Textlinks; externe Ziele bleiben unverändert. Listen-/Aufgabenkopien und Papierkorbwiederherstellung erhalten die Beziehungen, Undo/Redo kann die Objekte ersetzen; der Graph wird dann neu berechnet. Markdown importiert/exportiert interne Links mit denselben URLs.

## Format 21

Seit 3.33.15 schützt Format 21 Aufgaben im Notiztext und Textverweise. `item:<id>` bindet eine Heimatzeile; `taskref:<id>` verweist auf eine Aufgabe mit derselben Kennung an einem anderen Heimatort. Die Heimat bleibt ausschließlich in `lists[].items`/`children`. Beim Übernehmen in eine Aufgabenliste wechseln die zugehörigen Heimatmarken zu Textverweisen. Mehrere Verweiszeilen kopieren keine Aufgabe. Papierkorb- und fehlende Ziele behalten ihre Kennung; Laden erzeugt keinen Ersatzpunkt. Nur das Rückgängigmachen einer tatsächlich entfernten Heimatzeile stellt deren Aufgabe wieder her.

Der bestehende Startmigrationsweg schreibt den Bestand erst nach erfolgreicher bytegenauer `liste_vor_format21_*.json`-Sicherung. Scheitert die Kopie, bleibt die alte Datei unverändert. 3.33.14 erkennt den neueren Bestand und sperrt Schreiben. Referenz-Fixture: `tests/fixtures/current_v21/reference_v21.json`. Einstellungen bleiben Format 2; gespeicherte Filter ergänzen additiv `source` (`all`/`pages`). Allgemeine Dokumentverweise G08/G30 verwenden seit 3.33.17 die eigene Formatstufe 22.

## Format 20

Aufgabenformat **20** (seit 3.30.0) bündelt alle bestandsändernden Pakete des Modernisierungskatalogs (E-02).

**Punkte:** `links` (bis 50 Kennungen); `blocked_by` (bis 50, kreisfrei, Kreise löst das Laden auf); `planned_time` (`HH:MM`, nur mit Bearbeitungstag); `time_spent_minutes` (0–1.000.000); `done_at` (beim Abhaken gesetzt, beim Wiederöffnen geleert). Dazu aus früheren Stufen: `due`, `due_time`, `planned_date`, `estimated_minutes` (1–60.000), `importance`, `labels`, `color`, `kind` (`task`, `long`, `group`, `heading`), `checklist` (`{id, text, done}`), `repeat`, `reminder`, `attachments`, `children`.

**Listen und Ordner:** `icon` (Zeichendokument 16 × 16), `archived`, `archived_at`, `recurring_checklist` (nur Aufgabenlisten).

| Feld | Werte |
|---|---|
| `list_kind` | `tasks`, `note`, `drawing`, `page`, `gallery` |
| `folder_kind` | `standard` (Ordner), `library` (Buch), `journal` (Notizbuch); Unbekanntes wird `standard` |
| `rich_note` | `text`, `spans` (`tag`, `start`, `end` als Python-Zeichenpositionen), `links`; Seiten zusätzlich `images` (`{"img:<kennung>": {attachment, mode, width}}`, `mode` `left`/`right`/`center`, Breite 24–4.000 px) und Aufgabenmarken `item:<id>`. Höchstens 1.000.000 Zeichen und 10.000 Bereiche |
| `journal` | `favorite`, `mood` (feste Auswahl), `location`, `moment_date` (ISO), `prompt` |
| `drawing` | Zellmodell `glide.drawing`, Kodierung `hex8-row-v1`, höchstens 256 Farben; Flächen mit 16/32/64 Zellen tragen `format_version` 2, 128 Zellen Version 1 |
| `drawing_reference` | `null` oder Verweis auf einen PNG-Anhang derselben Liste mit Rahmenwerten |

**Regel seit 29.09.2026:** Jede weitere Listen- oder Ordnerart hebt die Formatnummer. Nur so erkennt eine ältere Fassung den Bestand als neuer und öffnet ihn schreibgeschützt, statt ihn zu überschreiben. Format 21 ist seit 3.33.15 für Aufgaben-Textverweise angehoben; spätere inkompatible Inhalte benötigen erneut eine Formatstufe.

Referenz-Fixture: `tests/fixtures/current_v20/reference_v20.json`.

## Formatstufen

| Format | Seit | Ergänzt | Ältere Fassungen |
|---|---|---|---|
| 2 (Legacy), 4–9 | 2.x–2.10 | Grundbestand; 5 Aufgabenfarbe, 6 `kind` (`task`, `group`), 7 `labels` und `trash` | – |
| 10 | 2.11.0 | `due_time`, Papierkorbart `item` | ältere verwerfen Papierkorbeinträge, daher neue Nummer |
| 11 | 3.5.0 | Wiederholungen | – |
| 12 | 3.7.0 | Anhänge an Listen und Ordnern | – |
| 13 | 3.8.0 | Erinnerungen mit Zustellbeleg und Aufschub | – |
| 14 | 3.14.0 | `planned_date`, `estimated_minutes` | ≤ 3.13 können es nicht lesen |
| 15 | 3.19.0 | `history` (Änderungsverlauf, höchstens 15 Einträge und 15 Tage) | ≤ 3.18 |
| 16 | 3.22.0 | `checklist` | ≤ 3.21 |
| 17 | 3.26.0 | `list_kind` (`tasks`, `note`), `rich_note` | ≤ 3.25 |
| 18 | 3.28.0 | `folder_kind`, `journal` | ≤ 3.27 |
| 19 | 3.29.0 | `list_kind` `drawing`, `drawing`, `drawing_reference` | ≤ 3.28 |
| 20 | 3.30.0 | Beziehungen, Zeit, Pixelsymbole, Archiv, Seiten, Galerien, kleine Zeichnungen | ≤ 3.29 und Zwischenstände von 3.30 vor dem 27.09.2026 |
| 21 | 3.33.15 | Aufgaben im Notiztext, stabile Textverweise `taskref:<id>` und Heimatwechsel | 3.33.14 und ältere Format-20-Leser öffnen schreibgeschützt |
| 22 | 3.33.17 | Typisierte lokale Listen-/Aufgabenbeziehungen und Textlinks, abgeleitete Rückverweise | 3.33.16 und ältere Format-21-Leser öffnen schreibgeschützt |
| 23 | 3.33.18 | Live-Listen und Titelbilder in Seiten | 3.33.17 und ältere Format-22-Leser öffnen schreibgeschützt |
| 24 | 3.40.0 | Vollständige Pixelbildfolgen mit Bildkennungen und Dauern | 3.39.1 und ältere Format-23-Leser öffnen schreibgeschützt |
| 25 | 3.41.0 | Notion-Quellenzuordnungen an Seiten und Ordnern | 3.40.0 und ältere Format-24-Leser öffnen schreibgeschützt |

**Glide 3.29 und älter nach der Umstellung nicht mehr starten.** Sie halten einen Format-20-Bestand für beschädigt, beginnen leer und überschreiben ihn bei der ersten Eingabe (nachgewiesen am 25.09.2026 mit einer Kopie eines echten Bestands). Alte Fassungen nur mit getrennter Ablage (`GLIDE_DATA_DIR`) starten.

## Migration und Startprüfung

- **Windows-Dateistand:** Gleich große Überschreibungen können dieselben Dateizeiten behalten. Der Formatcache berücksichtigt daher den vollständigen SHA-256-Inhalt; ein geänderter Formatwert wird auch ohne Metadatenänderung neu gelesen. Unveränderter Inhalt braucht keinen erneuten JSON-Parse.
- **Älteres Format:** wird beim Start umgestellt (`migrate_on_start`), vorher bytegenau und unrotiert gesichert als `backups/liste_vor_format<N>_<Zeitstempel>.json` (`schema_backups.py`). Scheitert die Sicherung, bleibt die Originaldatei unverändert und es wird nicht gespeichert; der nächste Versuch sichert erneut.
- **Neueres Format oder unbekannte Listenart** (`NewerDataError`): öffnet schreibgeschützt mit leerem Bestand und Grund; nichts wird gespeichert.
- **Unlesbare Datei:** erst Kopie `backups/liste_unlesbar_<Zeitstempel>.json`, dann darf ein leerer Bestand sie ersetzen; gelingt die Kopie nicht, bleibt die Sitzung schreibgeschützt.
- **`data_format_written`** merkt das zuletzt geschriebene Format; ist die Datei älter, warnt Glide (eine ältere Version hat gespeichert oder eine ältere Datei wurde hineinkopiert).
- **Titelkürzung:** Container-Titel über 40 Zeichen werden beim Laden gekürzt; vorher `backups/liste_vor_titelkuerzung_<Zeitstempel>.json`. Scheitert die Sicherung, bleiben die Titel.
- Ein beschädigtes Einzelfeld (Checkliste, Verlauf, Ordnerart) fällt auf seinen leeren Wert zurück, statt die Datei unlesbar zu machen.

## Automatische Sicherungen

- `backups/liste_backup_*.json` entsteht nur bei geändertem Inhalt (SHA-256 gegen die neueste Sicherung), geprüft im Fünf-Minuten-Takt und bei jedem Speichern nach mindestens zwei Minuten.
- Aufbewahrung: die zehn neuesten immer, weitere jünger als 30 Minuten, höchstens 40; zusätzlich je Kalendertag der letzte Stand für 14 Tage (`BACKUP_DAILY_DAYS`, zählt nicht gegen die 40).
- Nie rotiert: `liste_vor_format*`, `liste_unlesbar_*`, `liste_vor_titelkuerzung_*`, `vor_import_*.glidebackup`, `vor_vorschlag_*.glidebackup` (3.35.0), `settings_vor_restore_*.json`, `vorlagen_vor_restore_*.json`.

## Backups und Transportwege

- **`.glidebackup`** ist ein ZIP aus `data.json` und den referenzierten Anhängen. Archivpfade, Größen, Symlinks, doppelte Namen und Kompressionsverhältnisse werden geprüft. Portable Backups werden ab Format 4 gelesen.
- **Größengrenzen:** `data.json` höchstens 32 MiB (`MAX_BACKUP_DATA_BYTES`), lese- und schreibseitig gleich geprüft; Anhänge je 512 MiB, zusammen 2 GiB, höchstens 4.096 Einträge. `data.json` hat dieselbe Kodierung wie `liste_speicher.json`, die Grenze gilt deshalb praktisch auch für den Bestand: Darüber scheitern vollständige Sicherungen, App-Backups und die Vorab-Sicherung vor Importen, ohne vorherige Warnung. Die Speicherlastsuite (26.420 Punkte) schreibt 28,5 MB. Die Hauptdatei selbst, die Einstellungen und Vorlagen werden ohne Vorabgrenze vollständig gelesen; der Vorlagenimport prüft vorab nur 4 GiB. Gemeinsames Budget mit Frühwarnung: WA-47 im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#212-ergänztes-aufgabenregister-und-gemeinsame-komponenten).
- **Komplettbackup laden** ersetzt erst nach Validierung und Sicherung (`vor_import_*.glidebackup`). **Teilbackup / Listen und Ordner hinzufügen** importiert additiv mit neuen Kennungen, vollständige Zweige einschließlich leerer Unterordner; Verweise (`links`, `blocked_by`, `references`, interne Textlinks, `item:<id>`, Bildanhänge, Zeichnungsreferenzen) ziehen nach.
- **App-Backup** = Komplettbackup plus Abschnitt `app_backup` (`format_version`, `settings` ohne Tageshistorien, `templates`, `activity`); für ältere Fassungen bleibt es ein gültiges Aufgabenbackup. Wiederherstellen mit Inhaltsvorschau und wählbaren Bereichen. Pinnwände reisen mit und werden beim Import neu zugeordnet.
- **`.glidepage`:** Teilbackup nur mit Seiten und Büchern (`"content": "pages"`); eine Datei mit Listen weist der Seitenimport ab.
- **Vorlagenkatalog** `.glidetemplates` (Vorlagenformat 2) mit portablen Anhängen.
- Benannte Zwischenstände einer Zeichnung sind Anhänge (MIME `application/vnd.glide.drawing-snapshot+json`, höchstens 10).
- **Ausgaben** (Druck-HTML, ICS, CSV, Markdown) schreiben atomar an ein gewähltes Ziel; Nutzdatendateien sind als Ziel ausgeschlossen. Sie erzeugen keinen Verlaufseintrag.
- **Importe** (CSV, ICS, Markdown, Austausch) lesen nur die gewählte Datei, erzeugen Punkte über `new_item` und sind ein Rückgängig-Schritt einschließlich neuer Labels; bestehende Punkte werden nie überschrieben. Einzige Ausnahme ist der geprüfte Änderungsvorschlag (Stufe 2 des Austauschformats).
- **Sicherungen vergleichen** (3.35.0, F-03): Datei › Sicherung › „Sicherungen vergleichen …“ liest zwei Stände – den aktuellen Bestand, eine automatische Sicherung oder eine gewählte `.glidebackup`/`.json` – mit den Grenzen des Imports und zeigt Listen und Aufgaben neu, entfernt, verschoben und geändert mit Feldern (`backup_diff.py`, Tk-frei). Nur lesend: keine Datei wird geschrieben, nichts wiederhergestellt. Eigene ICS-UIDs werden erkannt, damit der Rundlauf keine Kopien anlegt.

## Einstellungen

**FP-03 Stufe 1 (3.44.0):** `saved_view_conditions_v1` enthält Definitionen je Filter-ID auf oberster Einstellungsebene. `saved_filters` behält ausschließlich seine bisherigen Felder; `_view` ist nur der vorübergehende Dialog-/API-Transport und wird nicht dort gespeichert. Lesen und App-Sichern erhalten unbekannte Bedingungen bestehender Filter; die neue Auswertung behandelt sie sichtbar als ungültig. Verwaiste Definitionen gelöschter Filter werden entfernt. Die vollständige App-Sicherung führt den Schlüssel mit; ohne zugehörigen Aufgabenteil wird er wie `saved_filters` verworfen. Alte Fassungen erhalten den obersten Schlüssel, wenden aber nur ihre alten Bedingungen an und können deshalb mehr Treffer zeigen. FP-03 selbst änderte die Formate nicht; der nachfolgende FP-02-Schnitt verwendet inzwischen Aufgabenformat 26 und unverändert Einstellungen 2.

**FP-03 Stufe 2 (3.44.0):** `saved_view_layouts_v1` speichert je Filter-ID `display` (`list`, `table`, `columns`), `group`, `sort`, `direction`, geordnete `columns`, `widths` (60–1.200 px), `collapsed`, `hide_empty` und `only_open`. `_layout` ist nur Dialog-/API-Transport und wird vor dem Schreiben aus `saved_filters` entfernt. Unbekannte oder ungültige Darstellung bleibt unverändert erhalten, liefert eine sichtbare Meldung und eine lesbare Liste als Rückweg; der Dialog verlangt die Bestätigung zum Ersetzen. Verwaiste Definitionen werden zusammen mit dem Filter gelöscht. App-Sicherungen erhalten den Schlüssel, ohne zugehörigen Aufgabenteil wird er wie `saved_filters` verworfen. Die ausgelieferte ältere 3.43.1 erhält ihn auf oberster Ebene, verwendet aber ihre alte Listenansicht. Aufgabenformat 26 und Einstellungen 2 bleiben; keine Aufgabe und keine ID werden durch eine Darstellung kopiert.

**FP-04 (3.44.0):** `page_pinboards_v1` ist ein eigener oberster Schlüssel für Seiten-/Notizkarten (`page:<ID>`), ihre Positionen, Reihenfolge und berührten Kanten je Pinnwand sowie einen Grundzustand, falls die ältere Fassung die leere Pinnwand entfernt. Im Arbeitsspeicher verwendet Glide weiterhin die gemeinsame Pinnwand. Beim Schreiben trennt `pinboard_pages.persist` die neuen Karten von den bestehenden Aufgaben-/Zeichnungskarten in `pinboards`; beim Lesen führt `restore` sie vor der bekannten Normalisierung zusammen. Dabei gibt es keine zusätzliche Obergrenze für die Zahl der Pinnwand-Kontexte; die bestehenden Grenzen je Pinnwand bleiben erhalten. Der Persistenzrundlauf ist mit 1.001 Kontexten geprüft. Eine ausgelieferte 3.43.1 kann dadurch den unverstandenen obersten Schlüssel unverändert zurückschreiben. Das ist der Altleserschutz für FP-04; die allgemeinere Toleranz unbekannter Unterfelder aus WA-09 ist damit nicht pauschal umgesetzt. FP-04 selbst änderte die Formate nicht; inzwischen gilt durch FP-02 Aufgabenformat 26 bei unverändert Einstellungen 2. App-Sicherungen führen denselben Schlüssel; ohne zugehörigen Aufgabenteil wird er wie die bisherigen aufgabenbezogenen Ansichten verworfen. Objekt-Undo hält den Seitenkartenanteil mit fest, damit Archivieren/Löschen rücknehmbar bleibt.

**FP-07 Stufe 1 (3.44.0):** Die lesbare Gesamtausgabe schreibt ausschließlich in einen neuen externen Zielordner. `INVENTAR.json` (eigene Kennung `Glide-Markdown-Inventar`, Version 1) enthält die übergebenen Listen, Ordner, Labels, Papierkorb und Pinnwände samt Feldwerten, die Objekt-/Anhangszuordnung, Zählung und jeden festgestellten Erhalt-/Darstellungshinweis. `MANIFEST.json` hasht alle anderen ausgegebenen Dateien. Fehlende oder unsichere Anhänge verhindern nicht die lesbare Ausgabe, werden aber ausdrücklich je Objekt/Anhang gemeldet. Ein E/A-Fehler oder Abbruch verwirft den eigenen Zwischenordner. Markdown ist kein Sicherungsformat; ausführbare Serien-/Erinnerungs-/Animations-/Layoutsemantik wird nicht als wiederimportierbar zugesichert.

Einstellungsformat **2**; alle neuen Schlüssel sind additiv und werden beim Laden normalisiert, fehlende Werte ergeben das frühere Verhalten. Persönliche Einstellungen sind nicht Teil eines Aufgabenbackups.

**Fokus seit 3.33.14:** `time_tracking` erhält additiv `focus`, `elapsed_seconds` und `goal_seconds`; `started_at = null` bedeutet Pause. `time_booking` enthält die Aufgabenkennung und erfasste Minuten vor/nach einer vorbereiteten Buchung. Ablauf und Fehlerwiederholung stehen in [Architektur](02_ARCHITECTURE.md#2-nutzdaten-und-speicherweg). Aufgabenformat 20 und Einstellungsformat 2 bleiben erhalten. Die alte Normalisierung in 3.33.13 entfernt die Fokuszusatzfelder und verwirft pausierte Timer; solche Fassungen dürfen einen laufenden oder noch ungeklärten Fokusbestand daher nur in getrennter Testablage öffnen. Vor einem Versionsrückwechsel Fokus in 3.33.14 vollständig buchen und beenden; offene Buchungsnachweise zuerst klären.

| Bereich | Schlüssel (Auswahl) |
|---|---|
| Erscheinung | `design` (aus `theme`, `color_mode`, `glass_mode` abgeleitet und als Spiegelwerte zurückgeschrieben; Unbekanntes → `glass_dark`), `design_auto` (Designpaar `light`/`dark` für „Automatisch hell/dunkel“, 3.33.21; Unlesbares → aus), `backdrops` je Design, `animations_enabled` |
| Navigation | `sidebar_visible`, `sidebar_narrow` (schmale Seitenleiste, 3.33.21), `sidebar_sections_closed`, `label_sections_closed`, `sidebar_locations` (gerätespezifische Bereichszuordnung), `startup_view`, `startup_list_id` |
| Ansichten | `list_detail_mode`, `table_columns`, `table_column_widths`, `saved_filters`, `daily_capacity_minutes` (0–1.440, 0 = kein Vergleich), `today_routines` (≤ 20 Listenkennungen) und `routine_done_days` (Kennung → ISO-Tag) für Routinen in „Heute“ (3.33.20), `recent_labels`/`recent_move_targets` (je ≤ 5, 3.33.20) |
| Startseite | `home_tile_order`, `home_tiles_hidden` (seit B04 steht die neue Kachel `gallery` in einer gespeicherten eigenen Auswahl einmalig ausgeblendet; Marke `home_tiles_gallery` wie `home_tiles_330`), `home_tile_span`, `home_columns`, `home_density`, `home_calendar_mode`, `home_filter_tiles`, Gismo-Pflegewerte `mascot_care`. Seit B03 (15.10.2026) entfernt das Normalisieren `mascot_name` und `mascot_playful`; ältere Fassungen lesen dann ihre Vorgaben (Gismo, Spielereien an) |
| Pinnwände | `pinboards` je Pinnwand: Karten mit Positionen und Größe, Anordnung, Spaltenboard, Bereiche (≤ 50), Verbindungen (≤ `MAX_CONNECTIONS` = 200, mit Art, Beschriftung, Strichart, Farbe), Hintergrund, Vorschau, Auto-Anheften. Verweise auf entfernte Karten fallen beim Normalisieren weg; ältere Fassungen lesen die Pinnwand als freie Fläche |
| Sonstiges | `system_notifications` (Vorgabe aus), `data_format_written`, `today_plan_migrated`, `release_notes_seen` (zuletzt gelesene Karte „Neu in …“, 3.33.20; Unlesbares entfällt), `show_hints` (ergänzende Bedienhinweise, seit B06; Vorgabe aus; ersetzt `view_hints` je Ansicht, das beim Laden übernommen und entfernt wird – ältere Fassungen zeigen dann eingeklappte Hinweise) |

### Tagesplanung seit 3.39.0

Aufgabenformat 23 und Einstellungsformat 2 bleiben unverändert. `daily_hints` speichert aktiviert/Zeiten/Wochentage; `daily_hint_state` die normalisierten Zustellbelege, Aufschub in UTC und übersprungene Termine. Der vollständige nächste Zustellzustand wird vor der Anzeige atomar gespeichert. Fehler lässt den letzten Dateistand erhalten und erlaubt Wiederholung, Neustarts stellen nicht doppelt zu. Die echte 3.38-Normalisierung und deren atomarer Settings-Schreiber bewahren diese additiven Schlüssel einschließlich unbekannter Zusatzfelder; der Rundlauf wird gesondert geprüft.

`busy_calendar` speichert ausschließlich die ausdrücklich gewählte lokale Quelldatei, Importzeitzone und deren SHA-256-/Größen-/Ladebelege. Keine Termine im Aufgabenbestand, keine Änderung der ICS-Datei. Kalenderlesen geschieht außerhalb des UI-Threads; bis zum passenden Ergebnis bleibt die Belegung unbekannt. Unlesbare Konfiguration wird sichtbar beibehalten und nur ausdrücklich ersetzt/entfernt. Aufgabenbackups enthalten wie bisher keine persönlichen Einstellungen und somit keine Kalenderquelle oder Tageshinweise.

Die Belegdatei ist UTF-8, regulär und höchstens 12 MiB groß: 5.000 VEVENT, 128 VTIMEZONE, 200.000 Zeilen, 65.536 Byte je entfalteter Eigenschaft und 32 Verschachtelungsstufen. Ein Auswertungsfenster umfasst höchstens 370 Tage; pro Serie gelten endliche Schritt-/Vorkommensgrenzen. Überschreitungen brechen sichtbar ab und ergeben keine Teilbilanz. Die gebündelten IANA-2026e-/CLDR-48.2-Daten liegen samt Quellenhashes und Original-Lizenzbelegen unter `resources/timezones`; keine systemweite Änderung und keine zusätzliche Laufzeitabhängigkeit.

Entlasten schreibt über `item_change`: Zieltag oder Vorrat, Planungsuhrzeit nach dem Umplanungsvertrag, Fälligkeit bleibt erhalten. Vor Übernahme werden Aufgaben-/Kapazitäts-/Belegfingerprints erneut verglichen; veraltete Vorschau oder unbekannte Kalenderbelegung verhindert das Schreiben. Ein Undo umfasst die ganze Auswahl, Schreibfehler rollt alles zurück.

## Austauschformat (`.glideexchange`)

Transportformat für fremde Systeme und KI, **kein Speicherformat**. Zwei getrennte Zahlen: `DATA_SCHEMA_VERSION` (wie Glide speichert, 26) und `EXCHANGE_FORMAT_VERSION` (worauf sich ein fremdes System verlassen kann, 2; Erstellen 1 bleibt lesbar). Leitsatz: Die Quelle beschreibt, was entstehen soll; Glide entscheidet, wie es intern gespeichert wird.

```json
{
  "format": "glide.exchange",
  "format_version": 2,
  "mode": "create",
  "generator": { "type": "ai" },
  "created_for": { "application": "Glide", "application_version": "…", "data_schema": 20 },
  "capabilities": { "…": "was die erzeugende Fassung kann" },
  "labels":  [ { "key": "label-1", "name": "Release", "color": "accent" } ],
  "folders": [ { "key": "folder-1", "title": "Projekt", "parent": "folder-0" } ],
  "lists":   [ { "key": "list-1", "title": "Titel", "folder": "folder-1",
                 "description": "Wozu diese Liste da ist.", "items": [ … ] } ]
}
```

Ein Punkt: `type` (`task` ausführbare Handlung, `long` textorientierter Arbeitsgegenstand, `group` Behälter ohne Termin, `heading` reine Gliederung), `title`, `description`, `importance`, `due`/`due_time` (bis wann fertig), `planned_date` (wann daran arbeiten), `estimated_minutes`, `labels` (Schlüssel), `done`, `checklist` (Schritte ohne eigene Termine), `children` (eigenständig erledigbare Unterpunkte).

- **Keine internen Kennungen:** Die Datei arbeitet mit frei wählbaren Schlüsseln; echte IDs vergibt Glide beim Import. Eine exportierte Datei enthält keine Aufgaben- oder Listenkennungen; Bildkennungen innerhalb einer Bildfolge dienen nur deren Reihenfolge und Zeitachse.
- **Capabilities** nennen je Fähigkeit eine Stufe (0 = unbekannt). Seit 3.40.0 steht `animations` auf 1, `max_animation_frames` auf 120 und `animation_duration_ms` nennt 20–60.000 ms; Zeichnungslisten tragen ihre vollständige Folge. Anhänge, Wiederholungen und Erinnerungen stehen bewusst auf 0; `patch_mode` steht seit 3.35.0 auf 1 (Änderungsvorschläge, unten). Grenzen: `max_items` 5.000, `max_checklist_entries` 50, `max_depth` 12, 12 MB je Datei.
- **Import:** JSON, Formatname, Version und Modus prüfen → Felder, Werte, Verweise prüfen → Vorschau → Bestätigung → ein Rückgängig-Schritt. Unbekannte Felder nennt die Vorschau, der Fokus liegt dann auf „Abbrechen“. Der Import legt ausschließlich Neues an; scheitert das Speichern, gehen Listen, Ordner, Labels und Rückgängig-Stapel exakt zurück.
- **Markdown-Gliederung** als zweite, schwächere Ebene: `# Liste`, `## Abschnitt`, `- Aufgabe`, eingerückte Unterpunkte, `- [ ]` als Checklistenschritt, freier Text als Beschreibung. Ohne Schlüssel und Labels, daher nicht für den Rückweg.
- **Bedienung:** Datei › „Für KI bereitstellen …“ (Export), „KI-Ergebnis importieren …“ (`.glideexchange`, `.json`, `.md`), „Austauschformat anzeigen …“ (Anweisung für eine KI, aus den tatsächlichen Konstanten erzeugt).
- **Rundlauf erhält** Ordner, Listen mit Beschreibung, alle vier Punktarten, Unterpunkte bis Ebene 12, Beschreibungen, Labels, Fälligkeit mit Uhrzeit, Bearbeitungstag, Aufwand, Wichtigkeit, Erledigt und Checklisten; **nicht** Anhänge, Wiederholungen, Erinnerungen, Farben je Punkt, Verlauf, Papierkorb, Pinnwandpositionen.

### Stufe 2: Kontextpaket und Änderungsvorschlag (seit 3.35.0, G24)

Vorhandenes ändern, ohne interne Kennungen preiszugeben und ohne still zu überschreiben (Entscheidung Q3: Dokumente statt Schnittstelle). Version 1 bleibt unverändert lesbar; Änderungsvorschläge tragen `format_version` 2.

**Kontextpaket** (`.glidecontext`, „Für KI bereitstellen …“ mit Zweck „Vorhandene Aufgaben überarbeiten lassen“; Umfang aktuelle Liste, Ordner, alles oder die ausgewählten Punkte):

```json
{
  "format": "glide.context", "format_version": 2, "created_at": "…", "application_version": "3.35.0",
  "instructions": "Antworte mit … mode \"patch\" …",
  "fields": ["title", "description", "importance", "due", "due_time", "planned_date", "estimated_minutes", "done", "labels"],
  "lists": [ { "ref": "r-…", "kind": "list", "title": "…", "description": "…" } ],
  "items": [ { "ref": "r-…", "kind": "item", "list": "r-…", "parent": "r-…" | null,
               "base": "…", "fields": { "title": "…", "importance": 2, "due": "JJJJ-MM-TT" | null, "labels": ["Name"], … } } ]
}
```

- `ref` ist `r-` plus die ersten 16 Hexzeichen von SHA-256 über `glide-ref\0<Kennung>`: stabil, aber ohne Rückschluss auf die Kennung. Glide findet die Aufgabe über denselben Verweis wieder.
- `base` ist die Prüfsumme (SHA-256, 16 Zeichen) des kanonischen JSON der neun Austauschfelder – der Ausgangsstand.
- Nur Aufgaben und Langtexte (planbare Punkte); Labels erscheinen mit Namen.

**FP-06-Aufträge (3.44.0):** Das Format bleibt unverändert. Ein gewählter Patch-Auftrag ergänzt ausschließlich den vorhandenen Text `instructions`; `items`, `ref`, `base` und Ausgangsfelder bleiben erhalten. Ein Create-Auftrag nutzt das bereits erlaubte Wurzelfeld `notes` für Anweisung und Antwortschema; neue Aufgaben werden ausschließlich über `mode: "create"` importiert. Ohne Auftragswahl kommt kein Feld hinzu. Die je Auftrag genannten erlaubten Felder sind Anweisungen, keine zusätzliche Import-Zulassung: Die bestehende Prüfung der neun Felder bleibt maßgeblich.

Eigene Aufträge liegen additiv im Einstellungsschlüssel `exchange_recipes` (Einstellungen 2): Liste bis 50 Datensätze mit `id`, `title` (1–80 Zeichen), `mode` (`create`/`patch`), `instruction` (1–12.000 Zeichen) und `fields` (Teilmenge der neun Austauschfelder). Kennungen und Titel innerhalb eigener Vorlagen sind eindeutig; mitgelieferte Kennungen bleiben geschützt. Die Ressource `resources/exchange_recipes.json` trägt ihren eigenen `format_version: 1`. Eigene Vorlagen sind im Einstellungsteil der vollständigen `.glideapp`-Sicherung enthalten und werden auch ohne Aufgabenteil wiederhergestellt; sie enthalten keine Aufgabenverweise. FP-06 selbst änderte die Formate nicht; inzwischen gilt durch FP-02 Aufgabenformat 26, Austauschformat 2 und Vorlagenhülle 2 bleiben erhalten.

**Änderungsvorschlag** (Antwort, `.glideexchange` oder `.json`):

```json
{ "format": "glide.exchange", "format_version": 2, "mode": "patch",
  "changes": [ { "ref": "r-…", "base": "…", "set": { "due": "2026-10-20", "importance": 3 } } ] }
```

- **Prüfung** (`exchange_patch.py`, Tk-frei): Rahmen, höchstens 5.000 Änderungen, je Feld Typ und Grenzen (Titel 1–500 Zeichen, Beschreibung bis 20.000, Wichtigkeit 0–3, Datum `JJJJ-MM-TT` oder `null`, Uhrzeit `HH:MM` oder `null`, Aufwand 1–10.080 Minuten oder `null`, Erledigt `true`/`false`, Labels als Namen). Je Änderung ein Zustand: anwendbar, ohne Änderung, **Konflikt** (Prüfsumme passt nicht mehr – die Aufgabe wurde seit dem Paket geändert), nicht gefunden (gelöscht, archiviert oder nie im Paket), ungültig (Feld unbekannt, Wert falsch, dieselbe Aufgabe doppelt, Erledigt an einer Wiederholung).
- **Vorschau:** jede Änderung Feld für Feld (alt → neu) mit Zustand; übernommen wird nur Anwendbares. Konflikte werden nie überschrieben.
- **Übernahme:** erst eine Vorsicherung `backups/vor_vorschlag_<Zeitstempel>.glidebackup` (wie `vor_import_*`, nie rotiert), dann alle Änderungen als ein Rückgängig-Schritt über `item_change`. Unbekannte Labelnamen entstehen neu; ohne Fälligkeit bzw. Bearbeitungstag entfällt die zugehörige Uhrzeit. Kennungen, Anhänge, Wiederholungen und Erinnerungen bleiben unberührt.

**Einplanen 3.33.13 (KO01/AU02):** kein Formatwechsel und kein neues Feld. Die gemeinsame Aktion schreibt ausschließlich `planned_date`; „Ohne Tag“ erhält `planned_time`. Fälligkeit/Uhrzeit, Aufwand, Wiederholung, Anhänge und Kennungen bleiben erhalten. Mehrere Quelllisten werden über `item_change` atomar im bisherigen Speicherweg geschrieben, ein Undo nimmt die gesamte Auswahl zurück. Die Kapazitätsvorschau verändert keine Daten. Feldverträge und Bedienung stehen in [Funktionen](20_FUNKTIONEN.md).
