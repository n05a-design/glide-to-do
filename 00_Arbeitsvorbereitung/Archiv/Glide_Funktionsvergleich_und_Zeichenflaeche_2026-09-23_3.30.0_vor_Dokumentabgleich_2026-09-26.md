# Glide – Funktionsvergleich und Konzept für eine Pixel-Zeichenfläche

Stand 23.09.2026 · ergänzt 24.09.2026 · Recherche- und Planungsstand · Glide 3.28.0 · Aufgabenformat 18

> **Status dieses Dokuments:** Recherche, fachliche Planung und begonnene
> isolierte Umsetzung. Zellmodell, Kernwerkzeuge, Zell-Undo, JSON-/SVG-Rundlauf
> und eine getrennte Tk-Bedienprobe sind seit 24.09.2026 implementiert. Die
> Zeichenfläche ist noch nicht in `ListApp`, Nutzdaten, Backup oder Migration
> integriert. App-Version und produktives Datenformat bleiben unverändert.

> **Präzisierung vom 23.–24.09.2026:** Die Zeichenfläche ist nun auf 128 × 128
> logische Zellen, eine editierbare Ebene, quadratische Pinsel mit 1 × 1,
> 2 × 2, 4 × 4 und 8 × 8 Zellen, 4er-Füllung, Pipette und einen lokalen
> Undo-Puffer für 20 Zelländerungen eingegrenzt. PNG-Ausgabe ist nachrangig;
> ein lokaler PNG-Referenzanhang ist eingeplant. Die vertiefte SVG- und
> Speicheruntersuchung steht in
> [Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md).

## 1. Auftrag, Quellen und Bewertungsregeln

Diese Untersuchung vergleicht den dokumentierten Funktionsumfang von Glide mit
Todoist, Notion, Microsoft Planner, Trello, OneNote, Figma Design, FigJam und
Microsoft Paint. Daraus wird ein belastbares Konzept für eine neue Seitenart
**Zeichenfläche** abgeleitet. Die sechs beigefügten Bilder dienen als visuelle
Inspiration für sichtbare Raster, klare Zellkanten, Pixelmotive, Farbflächen und
Muster. Sie enthalten keine auszuführenden Anweisungen und sind keine technische
Spezifikation.

Für Aussagen über Glide wurden ausschließlich die im Projekt abgelegten
Dokumente ausgewertet. Der Quellcode wurde für diese Untersuchung nicht als
Funktionsnachweis verwendet und die App wurde nicht erneut vollständig geprüft.
Für die nachträglich angeforderte **technische Machbarkeitsbewertung** wurden
gezielt die vorhandenen Listen-, Speicher-, Undo-, Backup- und SVG-Ausgabepfade
gelesen. Daraus wird keine zusätzliche vorhandene Endnutzerfunktion behauptet.
Für Wettbewerber wurden aktuelle Hersteller- und Standardquellen verwendet;
Abrufdatum der Webquellen ist der **23.–24.09.2026**. Preise werden nicht
verglichen. Tarif- oder Plattformgrenzen erscheinen nur, wenn sie die
Funktionsbewertung verändern.

Die folgenden Kennzeichnungen gelten im gesamten Dokument:

| Kennzeichnung | Bedeutung |
|---|---|
| **Dokumentiert vorhanden** | Ein aktueller Glide-Vertrag beschreibt die Funktion. |
| **Eingeschränkt vorhanden** | Die Grundfunktion existiert, aber mit dokumentierten Grenzen. |
| **Widersprüchlich dokumentiert** | Ein älteres Dokument widerspricht einem neueren, spezifischeren Vertrag. |
| **Geplant, nicht umgesetzt** | Fachliche Empfehlung oder künftige Schnittstelle dieses Dokuments. |
| **Nicht belegt** | Die ausgewerteten Quellen reichen für eine belastbare Aussage nicht aus. |

## 2. Dokumentierter Glide-Iststand

### 2.1 Aufgaben, Planung und Ansichten – dokumentiert vorhanden

Glide 3.28.0 ist als deutschsprachige lokale Desktop-Anwendung ohne
Benutzerkonto, eigenen Cloudservice oder notwendige Internetverbindung
dokumentiert. Der aktuelle Bestand umfasst:

- verschachtelte Ordner, Aufgaben, Unterpunkte, Gruppen, Long-Tasks und
  Überschriften;
- Fälligkeit mit Uhrzeit, Wiederholungen, lokale Benachrichtigungen bei
  laufender App, Wichtigkeit, Labels, Checklisten und lokale Anhänge;
- Schnellerfassung, gespeicherte Filter, „Mein Tag“, einen von der Fälligkeit
  getrennten Bearbeitungstag, Aufwandsschätzung und Tageskapazität;
- Listen-, Tabellen-, Reiter-, Kalender-, Label- und Pinnwandansichten auf
  demselben Aufgabenbestand;
- Suche, Papierkorb, Rückgängig, dauerhaften begrenzten Änderungsverlauf,
  Vorlagen und Druckausgabe über eigenständiges HTML.

Benachrichtigungen werden nur verarbeitet, solange die Anwendung läuft.
Glide synchronisiert einen extern gewählten Datenordner nicht selbst. Die
Belegungsdatei hilft gegen erkannte gleichzeitige Nutzung, löst aber keine
Konflikte zwischen noch nicht synchronisierten Kopien.

Lokale Belege: [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md),
[QA-Testplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md).

### 2.2 Notizen und Tagebuch – dokumentiert vorhanden, Vertrag widersprüchlich

Seit Aufgabenformat 17 gibt es eigene Notizlisten mit `list_kind: "note"` und
strukturiertem `rich_note`-Inhalt. Der dokumentierte Editor umfasst Rich-Text,
13 Formatierungen, Links, Datum und Zeit, lokale Tastenkürzel, Suche,
Undo/Redo und Autosave. Notizinhalt bleibt bei einem Wechsel des Listentyps
erhalten. Aufgabenbackups und das Glide-Austauschformat bewahren die
strukturierte Notiz; TXT und Markdown enthalten den Text, jedoch nicht alle
Formatierungen.

Aufgabenformat 18 ergänzt Tagebuchordner und datierte Notizseiten. Eintrag und
Ordner können Momentdatum, Favorit, Stimmung, Ortsnotiz und Schreibimpuls
tragen; Rich-Text, Labels und lokale Anhänge verwenden die bestehende
Notizinfrastruktur.

Lokale Belege: [Datenvertrag](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md),
[Tagebuchvertrag 3.28](../01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md),
[Entscheidungen 3.26](../01_Repository/Glide/docs/decisions/archiv/Entscheidungen_3.26.0.md).

### 2.3 Pinnwand – dokumentiert vorhanden, freie Zeichnung nicht belegt

Die Pinnwand ist eine zusätzliche Ansicht vorhandener Punkte und kein
eigenständiger Aufgabenspeicher. Eine Karte referenziert einen echten Punkt;
Bearbeitungen erscheinen deshalb auch in Liste, Tabelle, Suche und Backup.
Dokumentiert vorhanden sind:

- Listen-, Ordner- und globale Pinnwände;
- freie Kartenpositionen, geordnete Ansicht, drei Kartengrößen, Filter,
  Vollbild und Druck der belegten Fläche;
- Mehrfachauswahl, Lasso, optionale Ausrichtung, Abstands-Guides und
  vorübergehende Unterdrückung des Einrastens mit Alt;
- Zoom von 50 bis 200 Prozent in sechs Stufen und optionaler Navigator;
- Verbindungen als Linie oder mit einer beziehungsweise zwei Pfeilrichtungen;
- höchstens 500 Karten und 200 Verbindungen je Pinnwand;
- Transport zugehöriger Pinnwände in Komplettbackups sowie beim Hinzufügen
  exportierter Listen und Ordner, einschließlich Neuzuordnung der Kennungen.

Pfeile sind eine visuelle Beziehung und keine fachliche Aufgabenabhängigkeit.
Permanente benannte Bereiche, echte gerichtete Abhängigkeiten,
Pinnwand-Reisen und freie Zeichnungsdaten sind weiterhin offen.

Lokale Belege: [Pinnwand 3.23](../01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md),
[Navigation und Pinnwand 3.24](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md).

### 2.4 Import, Export und Wiederherstellung – dokumentiert vorhanden

Glide dokumentiert TXT-, CSV- und Markdown-Austausch, CSV-Import mit
Spaltenzuordnung, ICS-Import und -Export, ein versioniertes
`.glideexchange`-Format, portable Aufgabenbackups und vollständige
App-Backups. Wichtige Trennlinien:

- `.glideexchange` ist ein Transportformat und ersetzt kein Backup.
- ICS ist Dateiimport beziehungsweise Dateiausgabe, keine
  Kalendersynchronisierung.
- Ein `.glidebackup` ist ein geprüftes ZIP mit Daten und referenzierten
  Anhängen. Vollrestore ersetzt erst nach Validierung und Sicherung.
- Zoom, Werkzeugauswahl und andere reine Arbeitszustände gehören nicht in den
  fachlichen Inhalt einer künftigen Zeichnung.

Lokale Belege: [Daten-/Migrationsvertrag](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md),
[Glide-Austauschformat](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md).

## 3. Dokumentationskonflikte und verbindlicher Lesestand

Historische Analysen bleiben als Nachweise erhalten. Nicht jeder Konflikt ist
jedoch historisch: Der aktuelle allgemeine Produktgrenzen-Vertrag und die
aktuellen spezifischen Funktions- und Datenverträge widersprechen sich beim
Rich-Text weiterhin. Für diese Untersuchung gilt der spezifische Format-17/18-
Vertrag; der allgemeine Vertrag muss redaktionell korrigiert werden.

| Konflikt oder früherer Stand | Aktueller dokumentierter Stand | Konsequenz |
|---|---|---|
| Der aktuelle Produktgrenzen-Vertrag schließt einen Rich-Text-Editor aus. | Notizlisten mit Rich-Text sind seit Format 17 dokumentiert; Tagebuchseiten verwenden sie in Format 18. | Rich-Text ist ein zentraler Bestandteil längerer Notizen außerhalb von Long-Tasks und wird nicht erneut als Lücke geplant. Der allgemeine Vertrag ist zu korrigieren. |
| Bis 3.23 lagen Kartenpositionen und Verbindungen nur in Einstellungen beziehungsweise im App-Backup. | Seit 3.24 transportieren portable Backups einen getrennten `pinboards`-Abschnitt; Pinnwanddaten bleiben von Aufgabenobjekten getrennt. | Teilbackup, Startansicht und konkrete Kartenanordnung müssen bei einer als Pinnwand angelegten Aufgabenliste ausdrücklich gemeinsam geprüft werden. |
| Zoom und Navigator fehlten. | Der 3.26-Entscheidungsstand dokumentiert Zoom 50–200 Prozent und Navigator. | Vorhandene Bedienbausteine werden wiederverwendet statt neu ausgeschrieben. |
| Pinnwandverbindungen seien nur ungerichtet. | Seit 3.24 gibt es `line`, `forward`, `backward` und `both`. | Eine echte Abhängigkeitslogik bleibt trotzdem eine gesonderte Funktion. |
| Ordner- und globale Pinnwände könnten keine neuen Punkte anlegen. | Seit 3.24 wählt die vollständige Punktmaske dort eine Zielliste. | Kein neues Arbeitspaket erforderlich. |
| Freies Zeichnen müsse Teil der Pinnwanddaten werden. | Die geplante Zeichnung hat ein eigenes dauerhaftes Inhaltsmodell. | Sie wird als neue Seitenart geplant und kann später auf Pinnwänden referenziert werden. |
| Aufgaben- und Notizlisten können im aktuellen Dialog ineinander umgewandelt werden. | Die neue Produktentscheidung macht Inhaltsarten nach der Anlage unveränderlich. Nur Liste und Pinnwand wechseln die Ansicht desselben Aufgabenbestands. | Bedienvertrag, Hilfe und Datenvertrag müssen vor der Implementierung angepasst werden. |

Der QA-Bericht zu 3.28 bezeichnet den Stand als gezielt geprüft, aber nicht
als vollständig releasefreigegeben. OneDrive-Platzhalter, zwei Zeitgrenzen und
offene manuelle Prüfungen verhindern eine weitergehende Aussage. In diesem
Dokument bedeutet „dokumentiert vorhanden“ deshalb nicht automatisch „auf
allen Zielplattformen abschließend abgenommen“.

## 4. Wettbewerbsvergleich

### 4.1 Welche Anwendung für welchen Glide-Bereich herangezogen wird

| Glide-Bereich | Primäre Referenzen | Übertragbarer Nutzen | Nicht ungeprüft übernehmen |
|---|---|---|---|
| Zeichnen | Microsoft Paint, Figma Design | leicht verständliche Werkzeugwahl, Farbe/Pipette, Zoom, logisches Pixelraster und skalierbare Ausgabe | komplexe Bildbearbeitung, KI-Werkzeuge, beliebige Vektorobjekte |
| Notizen und Ordnerstruktur | Notion | verschachtelte Seiten, klare Seitenhierarchie, mehrere Darstellungen desselben Bestands, Vorlagen und Papierkorb | Cloud-, Kollaborations- und Baukastenzwang |
| Aufgabenliste und Boardansicht | Todoist, Microsoft Planner, Trello | derselbe Aufgabenbestand als Liste beziehungsweise Karten in Spalten; Verschieben statt Kopieren | Board als zweiter unabhängiger Datenspeicher |
| Freie Pinnwand und visuelle Kacheln | OneNote, FigJam, Figma Design | freie Fläche, ein-/ausblendbare Navigation, Bereiche, Verbinder, Zoom und Auswahl | unendliche oder kollaborative Fläche als Pflicht für die Pixelzeichnung |

### 4.2 Aufgaben, Notizen und Seitenstruktur

| Dimension | Glide-Iststand | Vergleich und Grenze | Empfehlung für Glide | Quelle |
|---|---|---|---|---|
| Schnellerfassung | Eingang und deutsche Fristvorschau sind dokumentiert. | Todoist kombiniert Schnelleingabe, Datumssprache, Wiederholungen, Prioritäten und Labels. | Aufgaben-Schnellerfassung unverändert schnell halten; neue Seitentypen nur im vollständigen Anlagedialog anbieten. | [Todoist: Funktionen](https://www.todoist.com/de/features) |
| Verschachtelte Inhalte | Ordner können verschachtelt sein; Listen liegen darin. | Notion verwendet Seiten und Unterseiten ohne eigene Ordnerobjekte und zeigt sie in Seitenleiste und Brotkrumen. | Glides eigenständige Ordner beibehalten, aber Ein-/Ausklappen, Verschieben und Pfadanzeige an der klaren Notion-Navigation messen. | [Notion: Unterseiten](https://www.notion.com/en-gb/help/create-a-subpage), [Notion: Seitenleiste](https://www.notion.com/en-gb/help/navigate-with-the-sidebar) |
| Notizseiten | Strukturierter Rich-Text ist vorhanden. | Notion behandelt Seiten als frei strukturierbaren Inhalt; OneNote ordnet Notizbücher in Abschnitte, Seiten und Unterseiten. | Rich-Text als zentrale lange Darstellungsform außerhalb von Long-Tasks weiterführen; Zeichnungen werden ein eigener Inhaltstyp. | [Notion: Datenbankseiten](https://www.notion.com/en-gb/help/intro-to-databases), [OneNote: Notizen organisieren](https://support.microsoft.com/en-us/onenote/organize-your-notes) |
| Mehrere Ansichten | Liste, Tabelle, Kalender und Pinnwand zeigen Aufgaben. | Todoist kann denselben Bestand als Liste oder Board zeigen; Notion-Datenbanken besitzen mehrere Ansichten mit eigenen Filtern. | `Liste ↔ Pinnwand` als Ansichtswechsel modellieren, nicht als Typkonvertierung. | [Todoist: Boardansicht](https://www.todoist.com/help/articles/board-layout-in-todoist-nutzen-AiAVsyEI), [Notion: Ansichten](https://www.notion.com/help/views-filters-and-sorts) |
| Karten in Statusspalten | Glide besitzt eine frei positionierte Pinnwand, kein eigenes Kanban-Datenmodell. | Planner gruppiert denselben Aufgabenbestand in Boardspalten; Trello organisiert Boards in Listen und Karten. | Eine geordnete Boardansicht und die freie Pinnwand begrifflich trennen. Beide referenzieren Aufgaben statt Kopien anzulegen. | [Planner: Plan erstellen](https://support.microsoft.com/en-us/planner/create-a-plan-in-microsoft-planner), [Trello: Board erstellen](https://support.atlassian.com/trello/docs/creating-a-new-board/) |
| Kartendetails | Glide-Karten zeigen ausgewählte Aufgabendaten. | Trello-Karten können unter anderem Labels, Termine, Anhänge und Checklisten tragen; Todoist-Boardkarten bleiben dieselben Aufgaben mit ihren Parametern. | Kacheln kompakt halten und Detailbearbeitung im Originalobjekt öffnen. | [Trello: Karten und Listen](https://support.atlassian.com/trello/docs/add-and-customize-cards-and-lists/), [Todoist: Boardansicht](https://www.todoist.com/help/articles/board-layout-in-todoist-nutzen-AiAVsyEI) |
| Offline und Speichern | Glide arbeitet lokal ohne Konto. | Notion stellt ausgewählte Seiten offline bereit; Todoist synchronisiert später und warnt vor Verlust noch nicht synchronisierter Änderungen. | Automatisches lokales Speichern und sichtbare Fehler sind für Zeichnungen verpflichtend. | [Notion: Offline](https://www.notion.com/help/use-pages-offline), [Todoist: Offline](https://www.todoist.com/help/todoist/features/use-todoist-while-offline-4rbaZw) |
| Export und Wiederherstellung | Austauschformat, Teilbackup und App-Backup sind getrennt. | Notion weist darauf hin, dass ein Export nicht automatisch den gesamten Workspace wiederherstellt; Todoist-CSV ist ein Projektaustausch. | SVG-Austausch, Glide-Bestand und vollständiges Backup als drei verschiedene Zusagen dokumentieren. | [Notion: Datensicherung](https://www.notion.com/help/back-up-your-data), [Todoist: CSV](https://www.todoist.com/help/account-and-billing/security/import-or-export-a-project-as-a-csv-file-in-todoist-YC8YvN) |

### 4.3 Pinnwand, Zeichnen und skalierbares Raster

| Dimension | Glide-Iststand | Vergleich und Grenze | Empfehlung für Glide | Quelle |
|---|---|---|---|---|
| Freie Fläche | Pinnwand mit Karten, Verbindungen, Zoom, Navigator, Lasso und Ausrichtungshilfen. | FigJam kombiniert Seiten, Bereiche, Notizen, Formen und Verbinder. OneNote erlaubt Notizen an beliebigen Stellen einer Seite. | Pinnwand für Beziehungen und Kacheln behalten; die 128-×-128-Zeichnung als eigene Seite öffnen. | [FigJam-Leitfaden](https://help.figma.com/hc/en-us/articles/1500004362321-Guide-to-FigJam), [OneNote: Notizen organisieren](https://support.microsoft.com/en-us/onenote/organize-your-notes) |
| Raster und Zellfang | Pinnwand besitzt Ausrichtungshilfen, aber kein gespeichertes Pixelbild. | OneNote belegt sichtbare Rasterlinien, keinen Zellfang. Figma Design zeigt und verwendet ein Pixelraster bei starker Vergrößerung. | Rasteranzeige, Trefferregel und gespeicherte Zellen getrennt modellieren. | [Figma: Zoom und Pixelraster](https://help.figma.com/hc/en-us/articles/360041065034-Adjust-your-zoom-and-view-options), [OneNote: Zeichnen](https://support.microsoft.com/en-us/onenote/onenote-help-and-learning/draw-and-sketch-notes-in-onenote) |
| Pinsel und Farbe | Noch kein Zeicheneditor. | Die aktuelle Windows-11-Fassung von Paint dokumentiert Stift, Füllen, Pipette, Zoom und weitere Werkzeuge. | Vier Pinselgrößen, Farbe, Pipette und Füllung zuerst; kein Universal-Editor. | [Microsoft Paint](https://www.microsoft.com/en-US/windows/paint) |
| Ebenen | Nicht vorhanden. | Paint besitzt Ebenen und `.paint`-Projekte; Figma Design besitzt ein Objektmodell. | V1 verwendet genau eine editierbare Ebene. Eine optionale Referenzabbildung ist Editorhilfe und keine zweite Zeichenebene. | [Windows Experience Blog: Paint-Projekte](https://blogs.windows.com/windowsexperience/2025/10/16/new-experiences-currently-rolling-out-for-windows-11/) |
| Skalierung | Glide-Zoom verändert die Darstellung, nicht die Aufgaben. | SVG `viewBox` bildet einen logischen Koordinatenraum auf beliebige Ausgabeflächen ab. | Eine logische Zelle ist kein Displaypixel. `viewBox="0 0 128 128"` erhält das Raster beim Skalieren. | [W3C: viewBox](https://www.w3.org/TR/SVG2/coords.html#ViewBoxAttribute) |
| Bearbeitbarer Austausch | Noch keine Zeichnungsdatei. | Figma weist auf nicht übertragene SVG-Konstrukte und Umwandlungen von Text beziehungsweise Strichen hin. | Nur das enge eigene Glide-SVG als vollständig bearbeitbar zusagen; Fremd-SVG bleibt ein späterer Importtyp. | [Figma: SVG-Austausch](https://help.figma.com/hc/en-us/articles/360040030374-Copy-assets-between-design-tools), [Figma: Exportformate](https://help.figma.com/hc/en-us/articles/13402894554519-Export-formats-and-settings-for-static-designs) |

### 4.4 Ergebnis des Vergleichs

Glide übernimmt je Bereich ein passendes Bedienprinzip, statt eine der
Vergleichsanwendungen vollständig nachzubauen:

1. **Inhalt und Ansicht bleiben getrennt.** Eine Aufgabenliste kann als Liste
   oder Pinnwand angezeigt werden. Notiz und Zeichnung sind eigene, nach der
   Anlage unveränderliche Inhaltstypen.
2. **Gespeichert werden 16.384 logische Zellen.** Fenstergröße, Zoom und
   Display-Skalierung verändern den Inhalt nicht.
3. **Der erste Zeichenumfang bleibt klein.** Vier Pinsel, Pipette und
   4er-Füllung sind bestätigt. Weitere Werkzeuge werden erst nach einer direkten
   Produktentscheidung aufgenommen.
4. **Internes Modell und SVG haben verschiedene Aufgaben.** Das Zellmodell
   optimiert Bearbeitung und Autosave; das Glide-SVG liefert skalierbaren,
   textbasierten Austausch.

## 5. Festgelegtes Konzept der Zeichenfläche

### 5.1 Produktrolle

Die Zeichenfläche wird als eigener Inhaltstyp `drawing` neben `tasks` und
`note` geplant. Der Typ wird bei der Anlage festgelegt und anschließend nicht
in einen anderen Inhaltstyp konvertiert.

Die vier sichtbaren Anlageoptionen werden intern so abgebildet:

| Auswahl im Anlagedialog | `list_kind` | gespeicherte bevorzugte Ansicht |
|---|---|---|
| Notizen | `note` | Notizeditor |
| Liste | `tasks` | `list` |
| Zeichnung | `drawing` | Zeichenfläche |
| Pinnwand | `tasks` | `board` |

Liste und Pinnwand sind damit zwei Darstellungen desselben Aufgabenbestands.
Der Wechsel ist keine Konvertierung. Notizen und Zeichnungen besitzen dagegen
eigene Inhalte und keine Typwechsel-Aktion. Für künftige Arten wird eine
zentrale Fähigkeitstabelle geplant, die zulässige Ansichten und Aktionen
festlegt.

Ordner verwenden weiterhin `folder_kind: standard | journal` mit den sichtbaren
Bezeichnungen **Ordner** und **Tagebuch**. Auch diese Art wird bei der Anlage
festgelegt und anschließend nicht konvertiert. Ein Tagebuch darf Notizen,
Aufgabenlisten, Zeichnungen, als Pinnwand angelegte Aufgabenlisten und künftige
Inhaltsarten enthalten. Alle direkten Inhalte tragen ein `moment_date`, werden
standardmäßig absteigend nach diesem Datum sortiert und lassen sich nach einem
bestimmten Tag beziehungsweise Datumsbereich filtern.

### 5.2 Raster, Skalierung und Trefferregel

- Die Bildfläche besitzt fest **128 × 128 logische Zellen**. Andere Größen
  gehören nicht zur ersten Stufe.
- Eine logische Zelle ist kein physischer Bildschirmpixel. Die Darstellung darf
  beliebig vergrößert und verkleinert werden; gespeichert bleiben dieselben
  16.384 Zellen.
- Koordinaten beginnen oben links bei `(0, 0)` und sind ganzzahlig.
- Rasterlinien sind reine Darstellung. Das Ausschalten verändert weder
  Zellwerte noch Trefferberechnung.
- Die vier Pinsel sind quadratische, am Zeiger zentrierte Fußabdrücke mit
  **1 × 1, 2 × 2, 4 × 4 und 8 × 8 logischen Zellen** Kantenlänge.
- Für eine Pinselgröße `s` und die fortlaufende logische Zeigerposition
  `(u, v)` ist der Fußabdruck das achsenparallele Quadrat von
  `(u - s/2, v - s/2)` bis `(u + s/2, v + s/2)`, an den Bildgrenzen
  abgeschnitten. Damit sind auch die geraden Pinselgrößen eindeutig definiert.
- Eine Zelle wird vom Pinsel getroffen, wenn dessen geometrischer Fußabdruck
  mindestens ein Drittel ihrer Fläche überdeckt. Eine sichtbare Vorschau zeigt
  vor dem Auftragen, welche Zellen die Regel aktuell trifft.
- Die Größenangabe beschreibt die geometrische Kantenlänge. Durch die bewusst
  empfindliche Ein-Drittel-Regel kann die Vorschau an Zellgrenzen mehr als
  `s × s` Zellen markieren; dies ist sichtbares, getestetes Verhalten und kein
  Rundungsfehler.
- Zwischen aufeinanderfolgenden Mauspositionen wird der Pinselweg ausreichend
  fein interpoliert. Schnelle Bewegungen dürfen keine unbeabsichtigten Lücken
  hinterlassen.
- Zoom, Verschieben, sichtbare Rasterlinien, Werkzeug und aktuelle Farbe sind
  Ansichtszustände, keine Zeichnungsdaten.

### 5.3 Werkzeuge der ersten Stufe

| Werkzeug | Verbindliches Verhalten der ersten Stufe |
|---|---|
| Vier Pinsel | Quadratische Größen 1 × 1, 2 × 2, 4 × 4 und 8 × 8. Sie tragen die gewählte Farbe während Ziehen und Klicken auf alle nach der Ein-Drittel-Regel getroffenen Zellen auf. |
| Füllen | Verwendet ausschließlich 4er-Nachbarschaft: links, rechts, oben und unten. Diagonal berührende Bereiche bleiben getrennt. |
| Pipette | Liest die Farbe der getroffenen Zelle direkt in die Farbauswahl ein. Bei einer späteren Referenzanzeige muss klar zwischen Zeichnungs- und Referenzfarbe unterschieden werden. |

Ein eigener Radierer ist nach aktueller Produktentscheidung nicht vorgesehen.
Version 1 verwendet einen **deckend weißen Hintergrund**; Weiß setzt eine
Zelle daher sichtbar auf den Ausgangszustand zurück. Transparenz ist kein
Zellzustand der ersten Formatversion und benötigt später eine neue,
ausdrücklich versionierte Formatfunktion.

Version 1 enthält ausschließlich Pinsel, Füllung und Pipette. Gerade,
Rechteck, Auswahl und weitere Formwerkzeuge bleiben spätere, getrennt zu
bewertende Erweiterungen.

### 5.4 Eine Zeichenebene, Palette und optionale Referenz

Version 1 besitzt genau **eine editierbare Zeichenebene**. Ebenenreihenfolge,
Sperren, Mischmodi und Ebeneneffekte entfallen. Das verkleinert Datenmodell,
Undo und Bedienoberfläche erheblich.

Die Zeichnung verwendet eine lokale sRGB-Palette mit verbindlich höchstens
**256 Farben**. Dadurch bleibt jeder Zellwert ein zweistelliger Hex-Index. Die
erste Palette erhält eine stabile Kennung und Version; das Zeichenmodell führt
zusätzlich die tatsächlich verwendeten `#RRGGBB`-Werte mit, damit ein späterer
Palettenwechsel vorhandene Zeichnungen nicht ungewollt umfärbt.

Als späterer Ausbau wird eine einheitliche Glide-Inhaltspalette mit eventuell
nur 128 Farben untersucht. Semantische UI-Farben für Fokus, Fehler,
Bestätigung und Kontrast bleiben dabei eigene Design-Tokens. Eine neue Palette
gilt für neue Farbauswahl und Vorlagen; vorhandene Zeichnungen behalten ihre
eingebetteten Farben und kennzeichnen nicht mehr auswählbare Werte als
Legacy-Farbe.

Eine optionale Referenzabbildung ist keine zweite editierbare Ebene. Sie wird
als getrennte Editorhilfe ein-/ausgeblendet, nicht in die sichtbare
Zeichnungs-SVG exportiert und kann der Pipette Farben liefern. Ohne neue
Abhängigkeit ist dafür ein in Glides Anhangsordner kopiertes lokales PNG
vorgesehen. Der Anhang reist mit vollständigem und passendem Teilbackup;
beliebige SVG-Referenzen kann Tk 8.6 nicht direkt darstellen.

### 5.5 Undo, Autosave und Eingabesicherheit

- Eine tatsächliche Farbänderung genau einer logischen Zelle bildet eine
  Undo-Einheit. Der lokale Ringpuffer hält die letzten 20 Zelländerungen samt
  vorherigem und neuem Farbindex.
- Der Zeichen-Undo-Puffer ist vom heutigen globalen Glide-Snapshot getrennt.
  Er kopiert weder alle Listen noch die gesamte 128-×-128-Fläche.
- Wenn ein breiter Pinsel gleichzeitig mehrere Zellen verändert, werden die
  Zellen nach `y`, dann `x` einzeln in den Puffer geschrieben. Interpolierte
  Pinselpositionen werden in Bewegungsrichtung abgearbeitet; bereits auf die
  Zielfarbe gesetzte Zellen erzeugen keinen weiteren Eintrag.
- Auch eine Füllung schreibt jede tatsächlich umgefärbte Zelle als einzelne
  Änderung. Der Ring enthält anschließend nur ihre letzten 20 Zelländerungen;
  eine Vollfüllung ist bewusst **kein** zusammengefasster Undo-Schritt. Die
  iterative Breitensuche startet an der gewählten Zelle und reiht Nachbarn in
  der festen Reihenfolge links, rechts, oben, unten ein.
- `Escape` verwirft eine noch nicht abgeschlossene Vorschau. Fokusverlust und
  Loslassen außerhalb der Fläche schließen oder verwerfen die Aktion nach
  einer einheitlichen, getesteten Regel; sie dürfen keinen Dauer-Zeichenmodus
  hinterlassen.
- Autosave wird während eines Pinselzugs gebündelt. Es schreibt nicht nach
  jedem einzelnen Mausereignis, wird aber nach kurzer Ruhe sowie vor
  Seitenwechsel, Export, Backup und Programmende abgeschlossen.
- „Gespeichert“ darf erst erscheinen, wenn die lokale Datei erfolgreich
  ersetzt wurde. Fehler lassen den letzten gültigen Stand bestehen und bleiben
  sichtbar, bis Speicherung erneut gelingt oder bewusst verworfen wird.
- Der lokale Zeichen-Undo-Puffer endet beim Schließen der App. Die gespeicherte
  Zeichnung selbst bleibt durch Autosave und Backup dauerhaft.

## 6. Daten- und Austauschkonzept

### 6.1 Kanonisches JSON-Zeichenmodell

Das offene, versionierte JSON bleibt die empfohlene Darstellung innerhalb des
Glide-Bestands. Der folgende Entwurf ist ein **Planungsbeispiel, nicht das
aktuelle Glide-Schema**:

```json
{
  "format": "glide.drawing",
  "format_version": 1,
  "width": 128,
  "height": 128,
  "color_space": "srgb",
  "palette_id": "glide-drawing-default",
  "palette_version": 1,
  "palette": ["#FFFFFF", "#000000", "#2B7DE9"],
  "encoding": "hex8-row-v1",
  "rows": [
    "0000000000000000000000000000000000000000000000000000000000000000...",
    "0000000000000000000000000202020202000000000000000000000000000000..."
  ]
}
```

Jede der 128 Zeilen enthält genau 128 zweistellige Hex-Palettenindizes. Das
ergibt bei Glides aktueller eingerückter JSON-Ausgabe ungefähr 34 KB je
Zeichnung und eine feste Maximalgröße. Die wörtliche Alternative mit einem
XML-Element je Zelle benötigte ungefähr 325 KB. Nach Farben gruppierte
Koordinaten sind bei dichten Bildern größer und fehleranfälliger.

Vor jeder Übernahme werden Format, Version, exakt 128 Zeilen, Zeilenlänge,
Hexsyntax, Palettengröße und jeder Index geprüft. Der Editor dekodiert die
Zeilen in ein festes Array mit 16.384 Einträgen. Die vollständige Bewertung
steht in der [SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md).

### 6.2 Glide-SVG

SVG ist für Glide als skalierbares Text- und Austauschformat geeignet. Version
1 verwendet ein enges eigenes Profil:

- `viewBox="0 0 128 128"` für den logischen Zellraum;
- ein Hintergrundrechteck und horizontale `rect`-Läufe mit `height="1"`;
- `shape-rendering="crispEdges"` als Darstellungswunsch;
- das vollständige kanonische Zeilenmodell im Glide-Namensraum innerhalb von
  `metadata`;
- getrennte SHA-256-Werte für Modell und normalisierte sichtbare Rechteckläufe.

Tk 8.6 kann SVG nicht selbst darstellen. Glide liest deshalb das eigene Modell
und zeichnet es mit seinem Editor. Das ist ohne neue Abhängigkeit machbar; ein
allgemeiner Fremd-SVG-Renderer ist es nicht.

Der V1-Import akzeptiert keine Pfade, Transformationen, CSS, Skripte,
Ereignisattribute, Animationen, `foreignObject`, `image`, `use`, URL-Verweise,
Filter, Masken oder unbekannte Elemente. Dateiimport und Einfügen als Text
verwenden dieselbe Positivlistenprüfung. Ein verändertes oder unvollständiges
Fremd-SVG wird als Zeichnungsimport abgelehnt und verändert keinen Bestand.

Die sichtbare Ausgabe bleibt trotzdem ein reguläres Standard-SVG: `svg`,
`viewBox`, ein weißes `rect` und weitere farbige `rect`-Elemente lassen sich im
Browser anzeigen und in Illustrator oder Affinity Designer öffnen. Adobe führt
SVG als unterstütztes Illustrator-Format; Affinity dokumentiert SVG-Import und
-Export. Das Öffnen und externe Bearbeiten ist deshalb ein verbindlicher
Kompatibilitätstest. Ein externes erneutes Speichern kann jedoch Rechtecke
umformen oder Glides private `metadata` entfernen. Nur eine Datei, die danach
weiterhin das enge Glide-Profil erfüllt und deren sichtbare Grafik zum
eingebetteten Modell passt, darf wieder als vollständig bearbeitbare
Glide-Zeichnung importiert werden. Für einen sicheren Rückweg bleibt das
ursprüngliche Glide-SVG aufzubewahren.

Die vollständige Profildefinition, Konfliktmatrix und Sicherheitsprüfung steht
in der [SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md).

Quellen: [W3C: SVG-Metadaten](https://www.w3.org/TR/SVG/struct.html#MetadataElement),
[W3C: SVG-Erweiterbarkeit](https://www.w3.org/TR/SVG11/extend.html),
[W3C: Secure Static Mode](https://www.w3.org/TR/SVG/conform.html#processing-modes),
[Python 3.12: XML-Sicherheit](https://docs.python.org/3.12/library/xml.html),
[MDN: `viewBox`](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/viewBox),
[Adobe Illustrator: unterstützte Formate](https://helpx.adobe.com/in/illustrator/desktop/get-started/learn-the-basics/supported-file-formats.html),
[Affinity Designer 2: Import- und Exportformate](https://affinity.help/designer2/English.lproj/pages/Appendix/fileformat.html).

### 6.3 PNG

PNG ist nachrangig und gehört nicht zum ersten Austauschumfang. Ein späterer
PNG-Export kann die sichtbare 128-×-128-Komposition in ganzzahligen
Skalierungen ausgeben. Ein mögliches PNG-Referenzbild ist davon getrennt: Es
dient nur als Editorhilfe und wird nicht Teil der gezeichneten SVG-Grafik.

### 6.4 Speicherung, Backup und Migration

Das spätere Datenmodell erweitert `lists[].list_kind` auf
`tasks | note | drawing`. Aufgabenlisten erhalten zusätzlich eine portable
bevorzugte Ansicht `list | board`. Die konkrete zuletzt geöffnete Ansicht kann
weiter als Gerätezustand in den Einstellungen liegen.

Der empfohlene erste Speicherweg legt das ungefähr 34 KB große Zeilenmodell
als typbezogenes `drawing`-Feld in das Listenobjekt. Damit reist es automatisch
mit der gemeinsamen Glide-Datei. Duplizieren, Papierkorb, Vorlagen,
Teilbackup, Vollbackup, Wiederherstellung und Austausch müssen das Feld dennoch
jeweils explizit erhalten und validieren.

Ein PNG-Referenzbild liegt als normaler lokaler Glide-Anhang bei der
Zeichnung. Duplizieren, Papierkorb, vollständiges Backup und ein Teilbackup,
das diese Zeichnung enthält, müssen Datei und Verweis gemeinsam bewahren.

Tagebuchordner bleiben unveränderliche Containerart, dürfen jedoch jeden
unterstützten Inhaltstyp aufnehmen. `journal.moment_date` gilt deshalb nicht
mehr nur für Notizseiten. Die Ordneransicht sortiert alle direkten Inhalte
absteigend nach Momentdatum und bietet einen Tages- sowie Zeitraumfilter; bei
gleichem Datum sorgen Erstellungszeit und stabile ID für eine feste Reihenfolge.
Die bestehende Volltextsuche bleibt zusätzlich erhalten.

Die Entwicklung ist zukunftsorientiert: Das neue Format muss Zeichnungen nicht
auf alte Glide-Fassungen herunterkonvertieren. Beim einmaligen Übergang vom
aktuellen Format 18 werden bestehende Aufgaben und Notizen bewahrt, vor dem
ersten Schreiben eine unveränderte Sicherung erstellt und eine ältere Glide-
Fassung muss das neuere Format sichtbar ablehnen. Weitere historische
Sonderdarstellungen bestimmen nicht den neuen Zeichenvertrag.

SVG bleibt zunächst Austauschformat. Sollte es später die physische
Primärdatei werden, benötigt Glide zusätzlich einen Mehrdatei-
Transaktionsvertrag sowie neue Backup- und Papierkorbregeln.

## 7. Technische Machbarkeit in der bestehenden Architektur

Die dokumentierte Anwendung verwendet Python, Tk und die Standardbibliothek.
Die Umsetzung ist mit dem vorhandenen Stack grundsätzlich möglich. Vier
Schichten werden getrennt:

- **Listentyp:** `tasks`, `note` oder `drawing` sowie zulässige Ansichten;
- **Modell:** 16.384 Palettenindizes, Palette, Validierung und Zeilencodierung;
- **Editor:** vier Pinsel, 4er-Füllung, Pipette, lokales Zell-Undo und Autosave;
- **Darstellung/Austausch:** Tk-Zeichenfläche, Zoom, Raster und Glide-SVG.

Der aktuelle Konstruktor normalisiert jeden unbekannten `list_kind` still zu
`tasks`. Vor einer Schemaanhebung muss daraus eine explizite Typregistrierung
werden; ein unbekannter Typ in einem bekannten neuen Schema wird sichtbar
abgelehnt. Ansichten und Mutationen werden ebenfalls zentral nach Inhaltstyp
gesperrt, damit eine Zeichnung nicht versehentlich Aufgaben aufnehmen kann.

Das bestehende globale Undo kopiert den gesamten Glide-Bestand. Zeichnungen
verwenden deshalb einen eigenen Ringpuffer mit 20 kleinen Zelländerungen.
Autosave wird nach Eingabe gebündelt, da ein atomisches Neuschreiben der
gesamten Glide-Datei nach jedem Mausereignis unnötig wäre.

Der dauerhafte Glide-Änderungsverlauf bleibt davon getrennt. Sein
Vergleichsstand erhält für Zeichenlisten einen Hash des kanonischen
Zeichenmodells. Ändert sich dieser Hash, entsteht beim erfolgreichen,
gebündelten Speichern genau ein Listeneintrag **„Zeichnung geändert“**; einzelne
Zellen und frühere Bildstände werden nicht in den Verlauf kopiert. Der Verlauf
ist damit Nachweis einer Änderung, während Wiederherstellung über Backup oder
eine vor einem ersetzenden Import erzeugte Sicherung erfolgt.

Die geeignete Tk-Darstellung wird isoliert gemessen. Bei fest 128 × 128 und
einer Ebene sind Canvas-Zellen, zeilenweise Aktualisierung und ein Bildpuffer
realistische Kandidaten. SVG dient nicht als In-App-Renderer; Glide stellt das
validierte Modell selbst dar.

## 8. Risiken und bewusste Grenzen

| Risiko | Gegenmaßnahme |
|---|---|
| Fremdprogramm entfernt SVG-Metadaten oder wandelt Rechtecke in Pfade um. | Nur das enge Glide-Profil als verlustfrei importieren; Abweichung klar melden und Bestand unverändert lassen. |
| Vollständige Füllung blockiert die Oberfläche. | Iterative 4er-Füllung mit höchstens 16.384 Zellen; UI-Reaktionszeit im Prototyp messen. |
| Schnelle Eingabe lässt Zellen aus. | Pinselweg interpolieren und Ein-Drittel-Abdeckung für alle Kandidatenzellen berechnen. |
| Autosave meldet zu früh Erfolg. | Erst nach atomarem Ersetzen als gespeichert markieren; Fehlerzustand persistent anzeigen. |
| Zoom oder DPI verändert das Bild. | Speicherung ausschließlich in logischen Zellkoordinaten; Rundung an einer zentralen Stelle. |
| Unbekannte neue Listenart wird zu `tasks` normalisiert. | Zentrale Typregistrierung und sichtbarer Validierungsfehler statt stiller Rückstufung. |
| Aufgaben-, Notiz- und Zeichnungslogik wachsen auseinander. | Gemeinsamer Container-Lebenszyklus, aber typbezogene Inhalte und erlaubte Ansichten zentral definieren. |
| Unvertrauenswürdiges SVG greift auf externe Inhalte zu. | Strikte Teilmenge parsen; Skript, externe Referenzen und `foreignObject` ablehnen. |
| Weiß wird mit Transparenz verwechselt. | V1 verbindlich auf deckend weißen Hintergrund und `palette[0] = #FFFFFF` begrenzen; Transparenz erst in einer neuen Formatversion ergänzen. |
| Breiter Pinsel verbraucht alle 20 Undo-Plätze. | Zellweise Reihenfolge deterministisch halten und Wirkung in der Bedienoberfläche klar erklären. |
| Barrierefreiheit wird auf Mausbedienung reduziert. | Tastaturweg, sichtbaren Zellcursor, Fokus und textliche Statusmeldungen bereits im Prototyp prüfen. |
| Neue Zentralpalette färbt alte Bilder um. | Konkrete Farbwerte je Zeichnung bewahren; Palettenkennung versionieren und alte Werte als Legacy-Farben erhalten. |
| Gemischte Tagebuchinhalte erscheinen ohne nachvollziehbare Reihenfolge. | Einheitliches `moment_date`, feste Sortierschlüssel und kombinierbare Tages-/Zeitraumfilter für alle Inhaltsarten. |
| Referenz-PNG fehlt nach Teilbackup oder Wiederherstellung. | Datei wie einen lokalen Anhang transportieren, Verweis neu zuordnen und fehlende Datei sichtbar melden. |

## 9. Forschungsfazit

Eine textbasierte und erneut bearbeitbare Speicherung ist umsetzbar. Von den
beiden vorgeschlagenen Ideen ist die zeilenweise Speicherung die geeignete
Grundlage, wenn jede Zeile als kompakte Folge von Palettenindizes und nicht als
128 einzelne XML-Elemente gespeichert wird. Die farbweise Koordinatengruppe
eignet sich eher zur Erzeugung sichtbarer SVG-Geometrie.

Das enge Glide-SVG ist ohne neue Laufzeitabhängigkeit realisierbar. Glide
garantiert den Rundlauf nur für sein eigenes Profil; beliebiges Fremd-SVG bleibt
bewusst außerhalb der ersten Stufe. Eine logische Zelle bleibt durch `viewBox`
skalierbar und ist nicht mit einem physischen Displaypixel gleichzusetzen.

Die Listenarchitektur lässt sich zukunftsorientiert erweitern: `drawing` wird
ein eigener unveränderlicher Inhaltstyp, während Liste und Pinnwand zwei
Ansichten von `tasks` bleiben. Das neue Format muss nicht in alte Glide-
Fassungen zurückkonvertiert werden; der bestehende aktuelle Bestand wird beim
Formatsprung einmalig gesichert und bewahrt.

Die Produktentscheidungen vom 24.09.2026 stehen mit ihren technischen Folgen
in der
[SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md#8-bestätigte-produktentscheidungen-vom-24092026).
Die spätere Umsetzung ist in der
[Aufgabensammlung](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md)
geordnet. Der isolierte Kern ist begonnen; alle Integrations- und
Freigabepunkte bleiben **geplant, nicht umgesetzt**.

## 10. Lokale Quellen

- [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)
- [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md)
- [Daten, Backups und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md)
- [QA-Bericht 3.28.0](../01_Repository/Glide/docs/07_QA_BERICHT.md)
- [Glide-Austauschformat](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md)
- [Pinnwand als Arbeitsfläche 3.23](../01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md)
- [Navigation und Pinnwand 3.24](../01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md)
- [Tagebuch und UI 3.28](../01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md)
- [Entscheidungen und Umsetzungsstand 3.26](../01_Repository/Glide/docs/decisions/archiv/Entscheidungen_3.26.0.md)
- [SVG- und Zeichnungsdaten-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md)
- [Historische Konkurrenzanalyse 17.09.2026](Archiv/Glide_Konkurrenzanalyse_2026-09-17.md)
- [Historische Feature-Gap-Analyse 18.09.2026](Archiv/Glide_Feature_Gap_Analyse_2026-09-18.md)
