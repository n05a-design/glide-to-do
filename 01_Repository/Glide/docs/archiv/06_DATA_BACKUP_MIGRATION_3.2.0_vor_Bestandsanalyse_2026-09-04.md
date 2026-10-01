# Daten, Backup und Migration

## Speicherorte

- Windows: `%APPDATA%\Glide\`
- macOS: `~/Library/Application Support/Glide/`
- Linux: `$XDG_DATA_HOME/Glide/` oder `~/.local/share/Glide/`

Die Umgebungsvariable `GLIDE_DATA_DIR` überschreibt den Ordner ab 2.5.5
vollständig. Sie ist der einzige plattformunabhängige Weg, einen Testlauf zu
isolieren: `APPDATA` wirkt nur unter Windows, sodass ein Test unter macOS oder
Linux sonst die echten Nutzerdaten verwenden und überschreiben würde. Sie muss
**vor** dem Import des Moduls gesetzt sein.

**Seit 3.2.0 gibt es keine Übernahme aus früheren App-Ordnern mehr.** Bis 3.1.0
sah Glide beim Start nach, ob unter einem früheren Programmnamen
(„Lokale Listen-App“) oder im Skriptordner Nutzerdaten liegen, und kopierte sie
in den aktuellen Datenordner. Diese rund 110 Zeilen sind auf ausdrücklichen
Wunsch entfernt. Wer einen solchen Altbestand hat, öffnet ihn über
„Datei → Komplettbackup laden …“ – die Formatprüfung und die
`normalize_*`-Funktionen sind unverändert und lesen weiterhin die Formate 4 bis 10.

Verwaltete Anhänge liegen flach unter `attachments/`. Im JSON werden ausschließlich relative Pfade der Form `attachments/<Dateiname>` gespeichert. Beim Hinzufügen wird die gewählte Datei mit dem Anhangs-ID-Präfix atomar dorthin kopiert; Glide speichert keinen Link zur Quelle. Dateien über 512 MB werden bereits vor dem Kopieren abgelehnt.

Speichername und Prüfregel stammen ab 2.5.5 aus einer gemeinsamen Funktion, und
der Zielpfad wird vor dem Kopieren validiert. Vorher konnten Dateinamen, die nach
der Bereinigung auf einen Punkt endeten oder deren Endung außerhalb von A–Z/0–9
lag, einen Pfad erzeugen, den die Prüfung anschließend ablehnte: Der Anhang galt
sofort als „nicht gefunden“, verschwand beim nächsten Start aus den Daten und
blockierte jedes Komplettbackup. Der vollständige Anzeigename bleibt im Datensatz
unverändert erhalten.

Das Entfernen eines Anhangs aus einer Aufgabe entfernt zunächst nur die Referenz. Die verwaltete Datei bleibt absichtlich erhalten, damit Rückgängig und automatische JSON-Sicherungen nicht sofort ins Leere zeigen. Dasselbe gilt für den Papierkorb: eine endgültig entfernte Liste gibt ihre Anhangsdateien nicht frei. Vollständige `.glidebackup`-Sicherungen enthalten die jeweils referenzierten Binärdateien; automatische JSON-Sicherungen enthalten nur Metadaten.

## Datenformat 10

Format 10 ergänzt zwei additive Dinge:

- `due_time` an einem Punkt: die freiwillige Uhrzeit einer Fälligkeit als
  `"HH:MM"`. Sie hängt am Datum – ohne `due` ist `due_time` immer `null`, weil
  eine Frist ohne Tag keine Frist ist. Ein fehlendes Feld heißt „ganztägig“;
  jeder Bestand bis Format 9 lädt damit unverändert.
- die Papierkorbart `item`. Ein Papierkorbeintrag kann jetzt nicht nur eine
  Liste (`list`) oder einen Ordner (`folder`) tragen, sondern auch einen
  einzelnen Punkt – im Feld `item`, samt Unterpunkten, Beschreibung und
  Anhängen. Dazu kommt `origin` mit `list_id`, `list_title`, `parent_item_id`
  und `index`: die Stelle, an der der Punkt stand.

**Warum die Zählung trotzdem steigt.** Beide Ergänzungen sind additiv, aber die
Richtung zurück ist es nicht: Eine ältere Glide-Version verwirft beim Laden
jeden Papierkorbeintrag mit unbekannter Art – stillschweigend. Ein gelöschter
Punkt wäre damit endgültig fort, sobald jemand die Datei einmal mit 2.10.0
öffnet. Mit der höheren Schemazahl weist die ältere Version die Datei
stattdessen sichtbar ab.

**Wiederherstellen eines Punkts.** `restore_item_from_trash` sucht das Ziel in
dieser Reihenfolge: die ursprüngliche Stelle unter demselben Elternpunkt, sonst
das Ende der Herkunftsliste, sonst das Ende der aktuellen Liste. Ist die
ursprüngliche ID inzwischen wieder vergeben, bekommt der Punkt frische IDs, statt
im Baum zu kollidieren. Ein Punkt darf nie deshalb verloren gehen, weil sein
alter Platz nicht mehr existiert.

## Bestandswächter

Umbauaktionen – Gruppieren, Auflösen, Ziehen, Ein- und Ausrücken, Verschieben in
eine andere Liste – ordnen Punkte um. Keine von ihnen darf einen entfernen.
`guarded_structural_change` zählt deshalb vor und nach jeder solchen Aktion alle
Punkt-IDs in allen Listen **und** im Papierkorb. Fehlt danach eine ID, wird der
Stand aus dem Rückgängig-Speicher wiederhergestellt und der Vorgang gemeldet.

Planmäßig entfallen darf allein, was der Aufrufer über `expected_removals`
ausdrücklich nennt – in der Praxis nur die leere Hülle einer aufgelösten Gruppe.
Absichtliches Löschen läuft nicht über diesen Weg, sondern über den Papierkorb,
und dessen Inhalt zählt in der Bilanz mit.

## Datenformat 9

Format 9 ergänzt ein einziges additives Feld: `parent_id` an einem Ordner. Es
nennt den Ordner, in dem dieser Ordner liegt. Fehlt das Feld oder ist es `null`,
steht der Ordner auf oberster Ebene – jeder Bestand bis Format 8 lädt damit
unverändert.

Beim Laden räumt `normalize_folder_parents` auf, in dieser Reihenfolge:

1. Ein Elternverweis auf einen nicht vorhandenen Ordner wird gelöscht.
2. Ein Ordner, der sich über die Elternkette selbst erreicht, wandert auf die
   oberste Ebene. Ohne diesen Schritt liefe jeder rekursive Durchlauf – Aufbau
   der Seitenleiste, Zähler, Papierkorb, Export – endlos.
3. Ein Zweig jenseits der zulässigen Tiefe rückt so weit heraus, bis die Grenze
   eingehalten ist.

Ein **portables Komplettbackup** wird strenger behandelt: ein unbekannter
Elternordner und ein Kreis in der Ordnerstruktur führen zur Abweisung. Eine
stille Korrektur wäre dort Datenverlust ohne Ansage.

Der Text eines Punkts ist einzeilig; nur ein Long-Task (`kind: "long"`) darf
eigene Zeilenumbrüche tragen. Beim Laden und bei jeder Umwandlung wird das
erzwungen. Im TXT-Export stehen die Folgezeilen als `Text:`-Fortsetzungen und
werden beim Import wieder zusammengesetzt.

Jede der vier Arten trägt im TXT-Format einen eigenen Marker an derselben
Stelle, an der sonst die Wichtigkeitsmarker stehen:

| Art | Marker |
|---|---|
| Aufgabe | keiner |
| Long-Task | `»` |
| Zwischenüberschrift | `§` |
| Gruppe | `📁` |

Bis 2.9.0 erkannte der Import einen Long-Task allein an seinen
`Text:`-Fortsetzungen. Das funktioniert nur bei mehrzeiligem Text – ein
einzeiliger Long-Task kam als gewöhnliche Aufgabe zurück. Seit 2.10.0 hängt die
Art nicht mehr an der Textlänge.

## Datenformat 8

Format 8 ergänzt ausschließlich additive Angaben:

- `kind` eines Punkts kennt zusätzlich `long` (mehrzeiliger Punkt) und
  `heading` (Zwischenüberschrift). Ein fehlendes **oder unbekanntes** `kind`
  bedeutet in der lokalen Speicherdatei weiterhin „gewöhnliche Aufgabe“ – ein
  Bestand aus einer neueren Version verliert dadurch Darstellung, aber keinen
  Punkt. Ein portables `.glidebackup` wird strenger geprüft und mit einer
  unbekannten Art abgewiesen, weil dort eine bewusste Migration nötig wäre.
- Ein Label kann das Feld `system` tragen (`long` oder `heading`). Es kennzeichnet
  die beiden festen Labels „Long-Task“ und „Überschrift“, die die Art eines
  Punkts tragen. Fehlen sie in der Datei, legt Glide sie beim Laden an und
  stellt sie an den Anfang der Labelliste. Tragen zwei Labels dieselbe Rolle,
  behält das erste sie; das zweite wird ein gewöhnliches Label.

Art und festes Label werden nach jedem Laden vollständig abgeglichen – auch über
die Kopien im Papierkorb. Ein Punkt kann deshalb nicht als Long-Task gespeichert
sein und das Label verlieren oder umgekehrt.

Ein Punkttext wird beim Laden auf eine Zeile normalisiert (Zeilenumbrüche und
Mehrfachleerzeichen werden zu einem Leerzeichen). Die Mehrzeiligkeit eines
Long-Tasks entsteht ausschließlich bei der Darstellung; dadurch bleiben TXT-,
CSV- und Markdown-Export zeilentreu und der TXT-Import eindeutig.

Eine Zwischenüberschrift trägt – wie eine Gruppe – nie `done`, `due` oder
`importance`; die Normalisierung erzwingt das.

## Datenformat 7

Format 7 ergänzt ausschließlich additive Felder: `labels` als eigene Sammlung
auf oberster Ebene, `trash` für gelöschte Listen und Ordner sowie `labels` als
Liste von Label-IDs innerhalb eines Punkts, einer Liste und eines Ordners.
Fehlen sie – also in jedem Bestand bis Format 6 –, gilt: keine Labels, leerer
Papierkorb. Ein destruktiver Migrationsschritt entfällt.

Der interne Teststand 2.7.0 schrieb bereits Format 7, kannte aber weder Labels
an Listen und Ordnern noch die endgültige Farbpalette. Beide Fälle sind
abgedeckt: fehlende Felder bedeuten „keine Labels“, und die damaligen
Farbschlüssel (`label_red`, `label_blue` …) werden beim Laden auf die
Listenfarbpalette abgebildet.

Ein Verweis auf ein nicht mehr vorhandenes Label wird beim Laden aus dem Punkt
entfernt; ein Papierkorbeintrag ohne gültige Nutzlast wird verworfen. Die
Aufgaben gelöschter Listen durchlaufen dieselbe Normalisierung wie aktive
Aufgaben, teilen sich mit ihnen die ID-Eindeutigkeit und zählen in dieselbe
Obergrenze. Der Papierkorb fasst höchstens 200 Einträge; der älteste fällt
heraus, wenn ein neuer hinzukommt.

## Automatische Sicherungen und Rotation

Automatische JSON-Sicherungen entstehen frühestens alle zwei Minuten, damit
nicht jede einzelne Änderung eine Datei erzeugt. Zusätzlich schreibt der
Fünf-Minuten-Zyklus einen garantierten Sicherungspunkt und speichert einen wegen
eines Fehlers offen gebliebenen Stand erneut.

Die Rotation greift in fester Reihenfolge:

1. Die neuesten **10** Sicherungen bleiben immer erhalten – auch wenn sie älter
   als das Höchstalter sind. Sonst stünde nach einer längeren Pause keine
   Rückfallebene mehr bereit.
2. Aus dem Rest verschwinden alle, die älter als **30 Minuten** sind.
3. Zuletzt begrenzt die Obergrenze von **40** die verbleibende Menge.

Portable `vor_import_*.glidebackup` unterliegen dieser Rotation nicht: sie sind
die Rückfallebene eines Imports und bleiben liegen, bis sie jemand von Hand
entfernt.

## Datenformat 6

Format 6 ergaenzt das optionale Feld `kind` eines Punkts mit den Werten `task`
und `group`. Eine Gruppe ist ein reiner Behaelter: `done` bleibt false, `due`
bleibt null und `importance` bleibt 0; Beschreibung, Anhaenge, Farbe und
Unterpunkte verhalten sich unveraendert. Fehlt das Feld – also in jedem Bestand
bis Format 5 –, gilt der Punkt als gewoehnliche Aufgabe. Damit entfaellt ein
destruktiver Migrationsschritt, und ein in 2.6.0 geschriebener Bestand bleibt
fuer aeltere Versionen lesbar, weil unbekannte Felder dort verworfen werden.
Komplettbackups mit unbekannter Punktart werden abgewiesen.

## Datenformat 5

Format 5 ergänzt die optionale Farbe eines Aufgabenpunkts. Die mit Format 4 eingeführten Ordner-/Listen-Beschreibungstexte (intern kompatibel als `note`), Aufgabenbeschreibungen, Anhangsmetadaten und der feste Eingang bleiben unverändert. Ältere direkte Aufgabenlisten sowie strukturierte Formate bis Version 4 werden beim Laden normalisiert; fehlende Aufgabenfarben werden als `null` ergänzt. Die Ansicht „In Bearbeitung“ ist reine Darstellung und erfordert kein neues Datenformat.

Die automatisierten Referenzen liegen unter `tests/fixtures/current_v7/`, `current_v6/`, `current_v5/`, `current_v4/` und `legacy_v2/`; der Integrationstest führt alle fünf Bestände durch die aktuelle Normalisierung.

## Austauschformat versus vollständige Sicherung

- TXT/Markdown/CSV: lesbarer Austausch; keine Binärdateien der Anhänge.
- `.glidebackup`: vollständiger, portabler Daten-Snapshot einschließlich aller referenzierten Anhänge.

## Sicherheits- und Konsistenzregeln ab 2.5.1

- Backup-Export wird zuerst vollständig in eine temporäre Datei geschrieben und erst danach atomar an das Ziel verschoben.
- Ein fehlender oder zu großer referenzierter Anhang bricht das Backup ab. Anhänge gelöschter, aber noch wiederherstellbarer Listen gelten als referenziert und liegen deshalb im Archiv.
- Label- und Papierkorbfelder, die keine Listen sind, werden abgewiesen – auch an einzelnen Listen und Ordnern.
- Restore prüft Schema, eindeutige IDs, Itemtiefe, Dateianzahl, Größen, Kompressionsrate, Pfade und exakte Referenzintegrität.
- Nicht referenzierte Dateien und fehlende referenzierte Dateien werden abgelehnt.
- Importierte Anhänge erhalten neue zufällige Speichernamen; vorhandene Bytes werden nie überschrieben. Die Suche nach einem freien Namen ist begrenzt und meldet einen Fehler, statt bei einem nicht normierbaren Anzeigenamen endlos zu laufen.
- Vor dem Ersetzen wird unter `backups/` ein vollständiges `vor_import_*.glidebackup` angelegt.
- Ein Commitfehler entfernt bereits neu angelegte Anhangsdateien und lässt den alten Datenstand aktiv.

## Backup-Kompatibilität

Vollständige `.glidebackup`-Archive der Datenformate 4 bis 9 werden akzeptiert. Schema, App-Kennung, IDs, Pfade, Größen, Punktart, Labels, Papierkorb und Referenzen bleiben strikt geprüft. Fehlende Felder älterer Formate werden additiv normalisiert: ohne `color` keine Aufgabenfarbe, ohne `kind` eine Aufgabe, ohne `labels`/`trash` keine Labels und ein leerer Papierkorb, ohne die festen Labels werden sie ergänzt. Abgewiesen werden eine unbekannte Punktart, eine unbekannte Papierkorbart, ein unbekannter Elternordner, ein Kreis in der Ordnerstruktur, doppelte Label-IDs, eine unbekannte Labelfarbe sowie Label- oder Papierkorbfelder, die keine Listen sind. Ältere oder zukünftige Komplettbackup-Formate werden weiterhin abgelehnt, bis eine explizite Migration vorhanden ist.

Die eingecheckten Referenzbestände liegen unter `tests/fixtures/current_v7/`, `current_v6/`, `current_v5/`, `current_v4/` und `legacy_v2/`; der Integrationstest führt alle fünf durch die aktuelle Normalisierung.
