# Vorlagen und Probedaten – aktueller Stand

Stand 30.09.2026 · Glide 3.31.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

| Datei | Verwendung |
|---|---|
| [Praxisvorlagen](Glide-Praxisvorlagen_3.30.0.glidetemplates) | 16 vollständige Praxisvorlagen; Glide ergänzt vier Notizbuchvorlagen (bis 27.09.2026 „Tagebuch“) und drei Seitenvorlagen |
| [Funktionsvorschau](Glide-Funktionsvorschau_3.30.0.glidebackup) | Künstliche Arbeitslisten, eine Zeichnung und eine archivierte Liste im aktuellen Format 20 |
| [Releaseplanung](Glide-Releaseplanung_3.30.0.glidebackup) | Interner Veröffentlichungsplan für Glide, keine Freigabe |
| [Rundgang](Glide-Rundgang_3.30.0.glidebackup) | Seit 27.09.2026: je eine Liste, Notiz, Seite und Zeichnung; die Seite erklärt die Funktionen mit Bildern. Einlesen über Datei › Listen/Ordner hinzufügen … |

Diese vier Dateien sind die Nutzerkopien der Bestände aus
`01_Repository/Glide/tests/fixtures/beispiele` beziehungsweise
`01_Repository/Glide/src/glide/resources/templates`. Sie tragen denselben Inhalt
und denselben Prüfstand. [Vollständige
Vorlagenanleitung](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md).

## Rundgang

Der Ordner „Rundgang“ zeigt je Seitenart, was Glide kann:

- **Rundgang · Liste:** Überschriften, eine wichtige Aufgabe mit
  Checklistenschritten und Label, eine überfällige Aufgabe, eine Gruppe mit
  Unterpunkten, Erledigtes und zwei Long-Tasks zu „/“-Befehlen und
  wiederkehrenden Checklisten.
- **Rundgang · Notiz:** Aufgaben oben, darunter formatierter Text mit
  Überschriften, Listen, Zitat und Code.
- **Rundgang · Seite:** „Glide in Bildern“ – fünf Aufnahmen des
  Glide-Fensters (Liste mit Auswahlleiste, Pinnwand, Zeichnung, Mein Tag,
  Suche), links, rechts und mittig im Text, dazu Aufgaben zum Ausprobieren.
- **Rundgang · Zeichnung:** ein Haus mit Garten auf 32 × 32 Pixeln.

Die Datei ist ein Teilbackup: Sie ergänzt einen Bestand und bringt keinen
zweiten Eingang mit. Erzeugt mit `01_Repository/Glide/tests/tools/rundgang.py`.

## Umfang der Funktionsvorschau

15 Seiten einschließlich Eingang, der Zeichnung „Skizze Musterhaus“ und der
archivierten Liste „Umzug 2025 (abgeschlossen)“, 6 Ordner, **170 Punkte**,
9 Labels und 3 Papierkorbeinträge – eine gelöschte Liste, ein gelöschter Ordner
und ein einzelner Punkt. Alle vier Punktarten kommen vor: 115 Aufgaben,
11 Gruppen, 14 Long-Tasks, 30 Überschriften. Vier echte kleine Textanhänge
zeigen Anhänge an Ordner, Liste und Punkt.

Fälligkeiten liegen an 36 Punkten, davon 8 mit Uhrzeit; 9 Punkte tragen einen
Bearbeitungstag, 9 einen geschätzten Aufwand, 31 eine Wichtigkeit, 107 mindestens
ein Label. Alle sieben Palettenfarben sind vertreten.

Die kleine Liste **„Notartermin“** im Ordner „Website-Betrieb“ zeigt die
Neuerungen von Format 20 an einer Stelle:

- zwei gegenseitig verknüpfte Punkte;
- „Notartermin wahrnehmen“ wartet auf „Unterlagen … sammeln“;
- zwei Uhrzeiten für den Zeitplan in „Mein Tag“;
- ein erledigter Punkt mit 25 Minuten erfasster Zeit;
- ein gezeichnetes Pixelsymbol an der Liste.

Die archivierte Liste steht nicht in der Seitenleiste. In „Listen und Ordner“
zeigt der Schalter „Archiv“ sie an; dort lässt sie sich zurückholen.

## Was sich womit ausprobieren lässt

Die Liste **„Kalender, Erinnerungen und Tagesplanung"** im Ordner
„Website-Betrieb" ist der Prüfbestand für alles seit 3.14. Sie ist absichtlich so
gebaut, dass jede Funktion eine sichtbare Wirkung hat.

| Funktion | Womit | Doku |
|---|---|---|
| Tagesplanung und Tageskapazität | Sechs Punkte auf dem heutigen Bearbeitungstag, Summe **270 Minuten** – einer ohne Schätzung, einer erledigt. Ein Punkt liegt auf morgen für den Tageswechsel. | [3.15](../01_Repository/Glide/docs/archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md) |
| Bearbeitungstag und Aufwand | „Grundrisse Parkquartier zeichnen": Bearbeitungstag heute, Aufwand 90 Minuten, Fälligkeit später – die drei Felder sind absichtlich verschieden. | [3.14](../01_Repository/Glide/docs/archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md) |
| Erinnerungen, beide Arten | „Rückruf Bauträger" relativ, 30 Minuten vor dem Termin. „Angebotsfrist Parkquartier" fest, am Vortag um 8 Uhr. | [3.8](../01_Repository/Glide/docs/archiv/31_ERINNERUNGEN_3.8.0.md) |
| Wiederholungen, alle sechs Arten | täglich, alle 14 Tage mit Ende, Wochentage Mo/Mi mit Ende, wöchentlich, monatlich, jährlich | [3.21](../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) |
| Kalenderausgabe als ICS | Liste öffnen, Datei → Kalenderausgabe, Umfang „Aktuelle Liste". Ganztags- und Zeittermine, eine RRULE je Art, VALARM für beide Erinnerungen. | [3.20](../01_Repository/Glide/docs/archiv/44_KALENDERAUSGABE_3.20.0.md) |
| Kalenderimport aus ICS | Dieselbe Datei wieder einlesen: Der Bericht muss alle Termine als Duplikate überspringen. Mit ersetzten UIDs entstehen Aufgaben, und das Serienende bleibt erhalten. | [3.21](../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) |
| Änderungsverlauf | Ansicht → „Änderungsverlauf …" oder Strg/Cmd+H. Nach dem Import stehen die angelegten Punkte als Sammeleintrag darin. | [3.19](../01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) |
| CSV-Import mit Spaltenzuordnung | Eine Probeliste als CSV ausgeben, in einem Tabellenprogramm ergänzen, über Datei → CSV importieren wieder einlesen. | [3.18](../01_Repository/Glide/docs/archiv/42_CSV_IMPORT_3.18.0.md) |
| Druck- und PDF-Ausgabe | „Drucken und PDF …", Checkliste wählen, im Druckdialog als PDF speichern. | [3.17](../01_Repository/Glide/docs/archiv/41_DRUCK_UND_PDF_3.17.0.md) |
| Vollständiges App-Backup | Erst „Vollständiges App-Backup speichern …", dann **in einer getrennten Ablage** wiederherstellen und die Inhaltsvorschau mit dem Bestand vergleichen. | [3.16](../01_Repository/Glide/docs/archiv/40_APP_BACKUP_3.16.0.md) |
| Tabellenansicht, „Mein Tag", Schnellerfassung, Filter, Reiter, Pinnwände | Mit allen Listen dieser Datei. Spaltenauswahl und Tagesauswahl sind persönliche Einstellungen und stehen **nicht** im Aufgabenbackup. | [3.13](../01_Repository/Glide/docs/archiv/36_TABELLENANSICHT_3.13.0.md) · [3.12](../01_Repository/Glide/docs/archiv/35_MEIN_TAG_3.12.0.md) · [3.11](../01_Repository/Glide/docs/archiv/34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md) · [3.10](../01_Repository/Glide/docs/archiv/33_REITER_UND_PINNWAND_3.10.0.md) |
| Papierkorb und Rückgängig | Die Datei bringt drei Papierkorbeinträge mit – eine gelöschte Liste, einen gelöschten Ordner und einen einzelnen Punkt. Wiederherstellen setzt sie an ihren Platz zurück; Rückgängig nimmt den Bestand zurück, **nicht** das Protokoll. | [3.19](../01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) |
| Hell- und Dunkelmodus, Akzentfarbe, Schriftgröße | Einstellungen → Darstellung. Alle sieben Palettenfarben kommen in dieser Datei vor, deshalb zeigt sie beide Themes mit echtem Inhalt. | [3.9](../01_Repository/Glide/docs/archiv/32_UI_UND_BEDIENUNG_3.9.0.md) |
| Beziehungen, Zeitplan, Zeiterfassung, Archiv, Design „Pixel“ | Liste „Notartermin“ und die archivierte Liste, siehe oben. Das Design „Pixel · Blockfarben“ unter Einstellungen → Darstellung; die Pinnwand-Neuerungen (Spaltenboard, Bereiche, Präsentation) mit einer beliebigen Liste. | [3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) |

## Der Kalenderrundlauf in vier Schritten

Die Liste enthält diese Anleitung auch als Long-Task, damit sie beim Ausprobieren
in der App steht:

1. Liste öffnen, Datei → Kalenderausgabe als ICS, Umfang „Aktuelle Liste".
2. Datei im Texteditor ansehen: Ganztags- und Zeittermine, eine `RRULE` je
   Wiederholungsart, `VALARM` für beide Erinnerungen. `UNTIL` steht **ohne „Z"** –
   bis 3.21.0 stand dort ein UTC-Zeitpunkt, wodurch sich das Serienende beim
   Wiedereinlesen um einen Tag verschob.
3. Datei → „Kalenderdatei (ICS) importieren …", dieselbe Datei wählen. Der
   Bericht muss **alle** Termine als Duplikate überspringen: Die eigenen UIDs
   werden erkannt, der Rundlauf legt keine Kopien an.
4. Gegentest: die `UID:`-Zeilen im Editor ersetzen und erneut importieren. Jetzt
   entstehen Aufgaben, und das Enddatum der Wochentagsserie muss unverändert
   bleiben – auch wenn die Systemzeitzone gewechselt wird.

## Releaseplanung

3 Arbeitslisten plus Eingang, 1 Ordner, 168 Punkte. Planungsstichtag 25.09.2026;
Recherche historisch 04.09.2026, Microsoft-Textvorgaben 05.09.2026. Die Fristen
sind unverbindliche Planungsvorschläge, keine Zusagen. Storevorgaben vor einer
Veröffentlichung erneut prüfen.

## Fristen, Formate, Archiv

Backupfristen beziehen sich auf den Erzeugungstag 25.09.2026. Anders als relative
Vorlagenfristen verschieben Backups sie beim Import **nicht** – ein am
Erzeugungstag fälliger Punkt ist später überfällig. Die aktuellen Dateien
verwenden Aufgabenformat 20 und benötigen Glide 3.30 oder neuer. Historische
Fassungen bleiben im Archiv für Migrationsprüfungen erhalten.

Alle überholten Fassungen liegen in [Archiv](Archiv/); gelöscht wurde nichts.
Technische Referenzformate für Migrationsprüfungen bleiben zusätzlich unter
`01_Repository/Glide/tests/fixtures` erhalten.

Die drei früher zusätzlich aktiven 3.21.4-Dateien liegen seit der
Archivprüfung vom 24.09.2026 ebenfalls unter `Archiv/`. Aktiv bleiben nur die
oben verlinkten 3.30.0-Nutzerkopien; die 3.29.0-Fassungen liegen seit dem
25.09.2026 im Archiv.

## Umgang mit echten Daten

Diese Dateien sind künstlich. Zum Ausprobieren einen getrennten Datenordner
verwenden (`GLIDE_DATA_DIR`) oder vorher ein eigenes Backup anlegen: Das
Wiederherstellen eines App-Backups **ersetzt** den vorhandenen Bestand. Keine
dieser Dateien enthält echte Personen-, Kunden- oder Objektdaten.
