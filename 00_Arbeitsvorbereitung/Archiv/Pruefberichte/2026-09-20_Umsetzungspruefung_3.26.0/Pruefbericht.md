# Umsetzungsprüfung des Entwicklungsauftrags für Glide 3.26.0

Stand: 20.09.2026 · geprüfter Quellstand Glide 3.26.0 · tatsächliches Datenformat 16

## Ergebnis

Der konsolidierte Entwicklungsauftrag ist im vorliegenden Quellstand **nur zu einem kleinen Teil umgesetzt**. Die Versionsnummer ist bereits 3.26.0, der Funktionsbestand entspricht weitgehend der archivierten 3.25.0-Fassung. Nachweisbar neu sind einige kürzere Pinnwand-Beschriftungen und die korrigierte Reiterauswahl. Die umfangreichen Anforderungen an Gismo, Rich-Text-Notizlisten, Schema 17, die neue Verlaufspolitik und die erweiterten Pinnwandwerkzeuge fehlen.

Das ist eine Prüfung des vorhandenen Ergebnisses. Ohne Bearbeitungshistorie lässt sich nicht zuverlässig zuordnen, welcher Agent welche Datei geändert hat. Angaben in Entwicklungsauftrag, Changelog und Übergabe gelten hier als Aussagen, die am Code zu überprüfen sind.

Die zwei zusätzlich gemeldeten Darstellungsprobleme sind im Quellcode nachvollziehbar. Die gespeicherte globale Pinnwand wurde ausschließlich lesend auf ihre Geometrie geprüft. Der Anwendungscode und die produktiven Aufgaben/Einstellungen wurden durch diese Prüfung nicht verändert.

## Grundlage und Nachweise

- Prüfgrundlage: `3.25 Änderungen-Prompt/Glide_3.26.0_Konsolidierter_Entwicklungsauftrag.md`, ursprüngliche Prompt-Formulierung und die mitgelieferten Screenshots.
- Aktueller Code: `01_Repository/Glide/src/glide/app.pyw`.
- Vergleichsbasis: `01_Repository/Glide/src/glide/archiv/app_3.25.0_vor_3.26.0.pyw`.
- SHA-256 des geprüften aktuellen Codes: `8a65dea23512809fc3b7b0f4b82debd8773246a633dfea356068b57537c6184d`.
- [Vollständiger Quellvergleich](quellvergleich.diff).
- [Reproduzierbare isolierte Prüfsonden](pruefsonden.py), [Ergebnisse](sonden-ergebnis.json), [Prüfstatus](pruefstatus.json).
- Alle nachfolgenden Codezeilen beziehen sich auf diese `app.pyw`. Die Prüfsonden setzen vor dem Import `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis. Sie starten die Anwendung nicht mit den echten Nutzerdaten.

## 1. Tatsächlich neue Codeänderungen

Der AST-Vergleich identifiziert genau fünf geänderte Klassenmethoden und keine neu hinzugefügten Klassenmethoden:

| Methode / Stelle | Tatsächliche Änderung | Bewertung |
|---|---|---|
| `board_action_groups`, Zeile 3897 | „Anheften“, „Verbinden“, „Kartengröße“ ohne Ellipsen | Umgesetzt für diese Beschriftungen |
| `show_card_context_menu`, Zeile 3933 | „Anheften“ und „Aktionen“ | Umgesetzt |
| `render_tabs`, Zeile 4239 | „Reiter“ ohne Ellipse | Umgesetzt |
| `tab_overview`, Zeile 4370 | Übergibt `(Wert, Beschriftung)` statt einzelner Zeichenketten an den Auswahldialog; öffnet zurückgegebene Punkt-ID | Tatsächlicher funktionaler Bugfix, isoliert bestätigt |
| `render_board`, Zeile 4523 | „Anheften“, „Verbinden“, „Aktionen“ | Umgesetzt |
| `APP_VERSION`, Zeile 62 | 3.25.0 → 3.26.0 | Versionswechsel |
| Handbuchdaten, Zeile 6272 | „Drucken und PDF …“ an Menübezeichnung angepasst | Korrektur eines Test-/Beschriftungsabgleichs |

Die restliche Anwendungslogik ist gegenüber der genannten archivierten Basis unverändert. Bereits in 3.25 vorhandene Funktionen dürfen deshalb nicht als neue Erfüllung dieses Auftrags gezählt werden.

## 2. Die zwei aktuellen Beobachtungen

### Doppelter Pfeil bei „Mein Tag“ / „Eingang“

**Befund bestätigt.** Links steht der native Aufklappindikator der Treeview. Daneben wird das feste Textsymbol `ICONS['inbox'] = '▼'` ausgegeben. Es sieht wie ein zweiter Aufklapppfeil aus, besitzt aber keine eigene Umschaltfunktion.

- Symboldefinition: Zeile 6853.
- Abschnitt wird als echter Elternknoten mit `open=...` erzeugt: Zeile 23998.
- Zusätzliches Symbol im Überschriftentext: Zeile 24052.
- Isolierte Probe: Der Text lautet `▼  Eingang · 1 ohne Bearbeitungstag` und bleibt auch nach dem Zuklappen unverändert.

Damit ist nicht die rechte Hälfte eines funktionierenden Doppelschalters kaputt. Ein Symbol und ein echtes Bedienelement sind optisch nicht unterscheidbar. Ein einzelner Klappindikator wäre eindeutig; alternativ könnte ein anders geformtes Eingangssymbol bleiben. Dieser Fehler wurde im geprüften Stand noch nicht korrigiert.

### Pinnwand-Vorschau als schmaler Streifen

**Befund bestätigt und mit der gespeicherten Geometrie erklärt.** Die produktive globale Pinnwand enthält zum Prüfzeitpunkt 205 Karten, 0 Verbindungen und die Anordnung „frei“. Die ersten 40 Karten liegen in drei Spalten; ihre Y-Positionen reichen von 16 bis 3396.

Die Vorschau verwendet nur diese ersten 40 Karten (`HOME_BOARD_PREVIEW_CARDS = 40`, Zeile 8842; Auswahl Zeile 9109), nimmt pauschale Kartenhöhen an und passt die gesamte Teilfläche proportional in eine kleine Kachel ein (`BoardPreview._fitted`, Zeile 1311). Daraus wird eine logische Fläche von ungefähr **932 × 3506**. Bei einer angenommenen Vorschau von 425 × 132 Pixeln bleiben dafür ungefähr **31 × 116 Pixel**; eine Karte ist nur noch ungefähr **10 × 4 Pixel** groß. Das erklärt die schmale dunkle Säule im Screenshot.

Weitere unabhängig nachweisbare Schwächen:

- Die Kachel nennt die Gesamtzahl von 205 Karten, zeigt aber höchstens 40.
- Die Zahl der Verbindungen stammt ebenfalls nur aus der Vorschau-Teilmenge. Eine Verbindung zwischen Karte 101 und 102 erscheint bei vorhandenem Gesamtbestand als **0 Verbindungen**. In den tatsächlichen Daten sind derzeit allerdings wirklich 0 Verbindungen gespeichert; die konkrete Zahl im Screenshot ist deshalb korrekt.
- Die Vorschau benutzt gespeicherte freie Koordinaten. Die reale geordnete Pinnwand berechnet ihre Positionen dagegen beim Zeichnen neu (`draw_board`, Zeile 5182). Bei „Geordnete Karten“ können Vorschau und Arbeitsfläche dadurch auseinanderfallen.
- Die ausdrücklich unerwünschten inneren Linien sind weiterhin vorhanden (`BoardPreview.redraw`, Zeile 1348).

Die Vorschaufunktion und diese Geometrie sind bereits in der archivierten 3.25.0-Fassung enthalten. Der Befund spricht für eine unzureichende Vorschau bei größeren Beständen, nicht für einen ausschließlich durch das Starten als `.pyw` ausgelösten Defekt. Es gibt hier keinen Hinweis auf verlorene Karten.

## 3. Anforderungsmatrix

„Vorhanden“ bedeutet nicht automatisch „neu umgesetzt“. „Offen“ bezeichnet eine nicht erfüllte Anforderung. „Prüfauftrag/Backlog“ wird nicht pauschal als fehlgeschlagene Pflichtimplementierung gewertet.

| Auftragspunkt | Stand | Nachweis / fehlender Teil |
|---|---|---|
| 1: Version 3.26.0 | Umgesetzt | `VERSION`, `APP_VERSION`, Hauptsuite und oberster Changelog-Eintrag stimmen überein |
| 1 / 9.6: Schema 17 | Offen | `DATA_SCHEMA_VERSION = 16`, Zeile 6460; keine neue Migration |
| 1: Dopamin-Modus / gleichwertige Rückmeldung | Bestehende Grundlage | Rückmeldungen und Kombo bereits in 3.25; keine neue app-weite Prüfung oder Erweiterung im Diff |
| 1: Minimaldesigns mit wählbarem Farb-Akzent und Kontrastgrau | Teilweise bestehend | Minimalpaletten und Akzentauswahl vorhanden; `active_theme` liest den Akzent aus der bereits in Grautöne umgewandelten Minimalpalette. Keine neue farbige Akzentlösung |
| 3: Fehlerprotokoll-Ordner | Angelegt | `00_Arbeitsvorbereitung/Fehlerprotokolle/` existiert und war leer |
| 3: Fehlerprotokoll praktisch dort ablegen | Nicht angebunden | Laufzeit schreibt weiterhin `fehlerprotokoll.txt` in den Nutzerdatenordner, Zeilen 213 und 7982. Der Auftrag verlangt ausdrücklich den Ordner; er definiert nicht eindeutig, ob Laufzeitprotokoll oder gesammelte Arbeitskopien dorthin gehören |
| 3: Abschlusslauf 3.25 in QA/Handoff | Teilweise dokumentiert | Erfolgreicher Windows-Lauf ist eingetragen; im QA-Bericht steht weiter unten gleichzeitig noch, Vollprüflauf/Screenshots seien offen |
| 3: `tests/qa-verlauf.md` | Angelegt | Zwei historische Einträge; fehlgeschlagener Lauf im Ordner 3.26 und aktueller Stand fehlen |
| 3: `Entscheidungen_3.26.0.md` | Angelegt | Entscheidungen zu Gismo, Herausgeber, Lizenz, Verlauf usw. festgehalten |
| 3 / 15: `PRODUCT_IDENTITY.md` aktualisieren | Offen | Steht auf 3.25; Herausgeber, Lizenzmodell und Preis weiterhin als offen geführt |
| 4.1: Gismo höher/prominenter | Offen | Startseitenaufbau gegenüber archivierter 3.25-Fassung unverändert |
| 4.1: Standardname Gismo | Offen | `mascot_name()` liefert ohne Nutzereingabe eine leere Zeichenkette; Probe bestätigt, Zeile 9027 |
| 4.1: Umbenennen | Bereits vorhanden | `rename_mascot`, Zeile 9032 |
| 4.1: Kontextabhängige zufällige Sprechblase | Offen | Klick zeigt weiterhin „Hallo!“ bzw. „Hallo, ich bin …“, Zeile 9809; vorhandene Statussätze sind kein zufälliger Sprechblasendialog |
| 4.1: Füttern / langsames Streicheln | Offen | Keine entsprechende Erweiterung; vorhandene kurze Berührungsreaktion aus 3.25 bleibt |
| 4.1: Abschaltbarkeit / keine Leistungsbewertung | Bestehende Grundlage | Optionale Kachel und bestehende Rückmeldung; neue Interaktionen fehlen |
| 4.2: Tatsächlicher Monatsname | Offen | Kacheltitel nimmt weiterhin „Monat als Raster“ aus den Darstellungsoptionen, Zeilen 9615–9617 |
| 4.3: Vorschau ohne Innenlinien, klare Outlines/Verbindungen | Offen | Unveränderter `BoardPreview`; Innenlinien und Platzhalter bleiben |
| 4.4: Verteilung Text/Grafik, optionale neue Kacheln prüfen | Keine neue Umsetzung nachgewiesen | Wochenübersicht, Labels, Statistik, Begleiter sind Altbestand; keine dokumentierte Neubewertung der optionalen Vorschläge gefunden |
| 5: Vier genannte Pinnwand-Buttons umbenennen | Umgesetzt | Reiter / Anheften / Verbinden / Aktionen |
| 5: Alle normalen Buttons ohne Ellipsen | Teilweise | Weiter vorhanden u.a. „Weitere …“, „Benennen …“, „Spalten …“, „Tastenkürzel …“; echte Kontextmenüeinträge separat beurteilen |
| 5.1: Schmale Fenster / Icon-Modus / Suchbreite | Offen als neue Nachbesserung | Bestehende Dichtelogik unverändert; `Anzeige` weiterhin textuell, „Nur offene Punkte“ fest gepackt; Titelbreite zieht Metadaten weiterhin ab. Keine vollständige aktuelle visuelle Abnahme |
| 2 / 5: Aktive Toggle-Outline und Füllung | Teilweise bestehend | `set_active` u.a. an Pinnwand-/Reiterschaltern vorhanden; keine neue app-weite Konsistenzkorrektur im Diff |
| 6: Bestehende Verbindung nach Änderung der Art aktualisieren | Offen / reproduziert | `configure_board` ändert nur `connection_style`; vorhandene Verbindung behält `style='line'`, obwohl die Vorgabe anschließend `forward` ist |
| 6: Auto verständlich erklären | Tooltip schon vorhanden, Auftrag sachlich widersprüchlich | „Auto“ heftet neue Punkte automatisch an, Zeilen 4814–4815 und 5441; es ist keine automatische Kartengröße |
| 6: Alle Punkte im Anheften-Dialog | Teilweise vorhandene Funktion | „Alle Punkte anheften“ ist im Aktionenmenü vorhanden; der Auswahldialog besitzt nur „Anheften“ und „Abbrechen“, Zeile 4082 |
| 6: Reiter-Menü reparieren | Umgesetzt und geprüft | Richtige Wertepaare; erwarteter Punktreiter wird geöffnet |
| 6: Ordner strikt begrenzen | Teilweise korrekt, zusätzliche Lücke gefunden | Anheften/Zeichnen begrenzt korrekt auf Ordner und Nachfahren. Neue Aufgabe kann aber über die unbeschränkte Zielliste außerhalb des Ordners angelegt werden; siehe Abschnitt 4 |
| 7.1: Logische Canvas-Ebenen | Teilweise Altbestand | Tags für Karten/Verbindungen/Interaktion vorhanden; kein erweitertes Ebenenmodell für Sektionen/Guides usw. |
| 7.2: Lasso | Offen | Freie Fläche hebt Auswahl auf; keine Rechteckauswahl in `card_press`, Zeile 5607 |
| 7.3: Guides / Abstände / Object-Snap | Offen; Grid-Snap bereits vorhanden | Raster verwendet Schrittweite 24, Zeile 5694; keine Alignment-Guides oder Object-Snap-Erweiterung |
| 7.4: Zoom 50–200 %, koordinatenneutral | Offen | Kartengrößen sind bereits vorhanden, aber kein gemeinsamer Canvas-Zoom |
| 7.5: Mini-Map | Bedingter Prüfauftrag, keine Umsetzung | Nicht als zwingend fehlendes Release-Feature zählen; Entscheidung/Prüfergebnis nicht gefunden |
| 7.6: Benannte Bereiche | Produktentscheidung offen | Abschnitt 1 des Auftrags lässt das Datenmodell ausdrücklich offen; keine Umsetzung vorhanden |
| 8: Punktmaske vollständig über FieldPairGrid | Teilweise Altbestand | Feldpaare Art/Wichtigkeit und Farbe/Zielliste sowie Planung vorhanden. Weitere Blöcke laufen separat über Frames/pack; kein Umbau gegenüber 3.25 |
| 9.1: Listenart Aufgabenliste/Notiz; Hybridlayout | Offen | Keine neue Listenart und kein oberer begrenzter Aufgabenbereich mit unterem Rich-Text-Editor |
| 9.2–9.5: Formatierung, Toolbar, Shortcuts, lokales Undo/Redo, Tagebuch | Offen | Bestehende Plaintext-Notizfelder und Long-Tasks erfüllen diese Anforderungen nicht |
| 9.6–9.7: Rich-Text-Persistenz, Migration, Suche | Offen | Keine strukturierte Speicherung von Rich-Text-Bereichen/Links, kein Schema 17, keine entsprechende Suche |
| 10: App-Verlauf | Teilweise Altbestand | Verlauf seit 3.19 in Aufgabendaten; filterbarer Dialog vorhanden, Zeile 32662 |
| 10: Seitenleistenansicht Verlauf | Offen | Bestehender Verlauf ist ein Dialog, keine neue Systemansicht |
| 10: Maximal 15 Aktionen oder 15 Tage | Offen / reproduziert | Grenze weiter 4000, Zeile 6472; 20 Einträge aus 2020 bleiben in Normalisierung erhalten |
| 10: Export/Backup als Aktionen | Nicht entsprechend erweitert | Keine neuen Ereignisse für diese Vorgänge; vorhandene Aktionsnamen behandeln Bestandsänderungen, Zeile 6483 |
| 11: Historische Kommentare auslagern | Offen | Umfangreiche Marker „Punkt … (3.22–3.25)“ weiterhin im Code; außerhalb der kleinen Differenz keine Bereinigung |
| 11: `DEV_NOTES.md` / `DOKUMENTENPFLEGE.md` | Nicht gefunden | Bestehende Architektur- und Archivdokumentation vorhanden, neues verlangtes Regelwerk nicht nachgewiesen |
| 11.5: Archivierung nach Versionsabstand / QA-Auslagerung | Nicht umgesetzt als neues Regelwerk | Alte Archivbestände sind vorhanden; keine neue regelbasierte Bereinigung belegt. Die Prüfung selbst hat nichts archiviert oder gelöscht |
| 12.1: PanedWindow | Bedingter Prüfauftrag, offen | Kein entsprechender neuer Einsatz; Notiz-Hybrid fehlt |
| 12.2: Debouncing / after | Altbestand vorhanden | Bestehende `after`-/`after_idle`-Nutzung; keine neue Bündelung aus diesem Auftrag nachgewiesen |
| 12.3: ttk-Widgets prüfen | Prüfauftrag | Vorhandene Komponenten sind keine neue dokumentierte Machbarkeitsprüfung |
| 13: Virtuelle Glide-Events | Prüfauftrag, offen | Keine `<<GlideTaskChanged>>` usw.; direkte Refresh-Ketten u.a. in `item_change` bestehen weiter |
| 14: Konkurrenz-Featureliste | Backlog, keine Pflichtabnahme | Nicht pauschal als unvollständig implementierte 3.26-Funktionen zählen |
| 15: Herausgeber, Lizenzentwurf, Marken-/Signing-Unterlagen | Entscheidungen teilweise erfasst, Ausarbeitung offen | Herausgeber und nicht-gewerbliche Nutzung stehen im Entscheidungsblatt; Register nicht fortgeschrieben, kein passender neuer Lizenztext/gesonderte Anleitung nachgewiesen |
| 16–18: Vollständige QA / Sichtprüfung / Abschluss | Offen | Gespeicherter Lauf fehlgeschlagen und älter als der aktuelle Code; kein vollständiger aktueller 3.26-Anforderungsnachweis |

## 4. Weitere konkrete Befunde

### Verbindungsart: Datenänderung fehlt, nicht das Neuzeichnen

`configure_board()` erzwingt bereits einen Neuaufbau. Dieser zeichnet jedoch dieselbe gespeicherte Verbindung erneut. Das Dropdown ist laut bestehendem Code die Vorgabe für die **nächste** Verbindung. Eine vorhandene Verbindung behält ihre eigene Art. Ein zusätzlicher Aufruf von `draw_board()` allein würde den gemeldeten Fehler daher nicht beheben. Es braucht eine klar definierte Bearbeitung der ausgewählten bestehenden Verbindung und deren gespeicherter `style`-Angabe.

### Ordner-Pinnwand: Auswahl begrenzt, Neuanlage nicht vollständig begrenzt

`eligible_lists()` (Zeile 3585) funktioniert in der isolierten Probe: enthalten sind die Liste direkt im Ordner und die Liste im Unterordner; die fremde Liste bleibt draußen. Die Behauptung, generell würden alle Listen angeheftet, ließ sich in diesem Pfad nicht bestätigen.

Ein anderer Pfad verletzt aber die verlangte strikte Grenze: `create_card_item()` erlaubt bei Ordnern die Ziellistenauswahl, übergibt der Punktmaske nur eine Vorauswahl und prüft das Ergebnis anschließend gegen **alle** Listen (Zeilen 5308–5347). Die Punktmaske baut ihre Auswahl ebenfalls aus allen Listen auf (Zeile 12838). Mit simuliertem Dialogergebnis wurde eine Aufgabe in der fremden Liste tatsächlich angelegt. Sie gehört anschließend nicht zur erlaubten Kartenmenge der Ordner-Pinnwand. Das kann wie eine verschwundene neue Karte wirken.

### Der Entwicklungsauftrag enthält selbst Unklarheiten

1. **Auto:** Der konsolidierte Auftrag bezeichnet Auto als automatische Kartengröße. Tatsächlich ist es automatisches Anheften. Der ursprüngliche Text fragte lediglich nach der Bedeutung. Für eine Weiterentwicklung sollte zuerst diese Beschreibung korrigiert werden, ohne den bestehenden Auto-Schalter umzudeuten.
2. **Verlauf:** Das System existiert bereits seit 3.19. Erforderlich ist seine Erweiterung/Anpassung an 15 Einträge bzw. 15 Tage und die gewünschte Navigation, kein zweiter Verlaufsspeicher.
3. **Benannte Bereiche:** Gleichzeitig als offene Produktentscheidung und als Ausbaupunkt aufgeführt. Entscheidung und Pflichtumfang müssen vor der Implementierung getrennt werden.
4. **Optionale Architektur:** Mini-Map, zusätzliche Widgets, PanedWindow und Events sind teilweise Prüfaufträge, keine bedingungslos zugesagten Funktionen.
5. **Git/Archivierung:** Der Auftrag nennt Git als historische Quelle. Die vorhandene Übergabe beschreibt ausdrücklich keinen Git-Checkout. Archivdateien dürfen daher nicht allein mit dem Argument entfernt werden, die Historie sei ohnehin in Git vorhanden.

## 5. QA-Bewertung

| Nachweis | Ergebnis | Aussagekraft |
|---|---|---|
| Gespeichert `tests/qa-3.25.0/abschluss/ergebnis.json`, 19.09.2026 20:05:57 | Exitcode 0, Windows/Python 3.13.15 | Erfolgreiche automatisierte Abnahme von 3.25; Sichtprüfung übersprungen |
| Gespeichert `tests/qa-3.26.0/abschluss/ergebnis.json`, 20.09.2026 01:44:21 | Exitcode 1 | 47 Schritte, zwei fehlgeschlagen; Versionsprüfung nennt intern 3.25.0/Schema 16 |
| Fehler dieses gespeicherten Laufs | `test_features325`, `standpruefung` | Fehlender Handbuch-/Menüabgleich „Drucken und PDF …“; fehlende Standzeile in `qa-verlauf.md` |
| Aktuelle Syntaxprüfung | Bestanden | Prüft Syntax, keine fachliche Erfüllung |
| Aktuelle Versionskonsistenz | Bestanden | Version 3.26.0 konsistent, tatsächliches Schema weiterhin 16 |
| Aktuell erneut ausgeführte `test_features325.py` | Exitcode 0 | Der damalige Beschriftungsfehler ist im jetzigen Code behoben; Suite prüft den 3.25-Umfang |
| Aktuelle `standpruefung.py` | Exitcode 1, 39 Meldungen | Zahlreiche Dokumentstände nicht fortgeschrieben; darunter auch Klassifikation des historischen Originalprompts, daher nicht 39 eigenständige Produktfehler |
| Neue isolierte Prüfsonden | Erfolgreich durchgelaufen, keine Tk-Callbackfehler | Reiterauswahl, Ordnerabgrenzung, Neuanlage außerhalb des Ordners, Verbindungseinstellung, Verlauf und Vorschaugeometrie gezielt geprüft |

Ein kompletter neuer Vollprüflauf wurde in dieser Bestandsprüfung nicht ausgeführt. Ein grüner Lauf der vorhandenen Suiten würde Rich-Text, Schema 17 oder Gismo ohnehin nicht belegen: Der Prüfstand enthält weiterhin die bisherigen 30 Suiten bis 3.25 und keine neue 3.26-Anforderungssuite. Eine vollständige aktuelle manuelle Sichtabnahme aller Fensterbreiten/Designs ist ebenfalls nicht Teil dieses Ergebnisses. Die historischen Screenshots wurden als Fehlerbelege ausgewertet, nicht als Nachweis der aktuellen Anwendung.

Die startbare Datei in `07_Python-Versionen` heißt weiterhin `Glide-Aufgaben-und-Listen_v3.25.0.pyw` und meldet intern 3.25.0. Sie ist nicht identisch mit `src/glide/app.pyw` (3.26.0). Bei Fehlervergleichen muss deshalb festgehalten werden, welche Datei gestartet wurde.

## 6. Empfohlene Reihenfolge für die weitere Entwicklung

1. Diesen Prüfstand als Ausgangspunkt festhalten; offenen Auftrag nicht als erledigte 3.26-Version behandeln.
2. Die bestätigten Bedienfehler gezielt beheben: doppelter Eingangspfeil, lesbare und konsistente Pinnwand-Vorschau, Bearbeitung vorhandener Verbindungsarten, Ziellistengrenze bei neuer Ordner-Pinnwand-Karte.
3. Noch offene einfache Änderungen abschließen: Kalender-Monatsname, Gismo-Standardname, restliche normale Buttontexte, „Alle“ im Auswahldialog, schmale Fenster und Punktmaske.
4. Rich-Text-Notizmodell, Persistenz und Schema-Migration zusammen planen und implementieren; bestehenden Verlauf entsprechend erweitern.
5. Bedingte Pinnwand-/Architekturvorschläge bewerten und festhalten, was in diese Version gehört.
6. Produktregister, QA-Bericht, Handoff, Prüfverlauf und tatsächlich geprüfte startbare Fassung abgleichen. Danach vollständiger Lauf in einem neuen Protokollordner und dokumentierte Sichtprüfung.

Diese Reihenfolge ist eine Empfehlung aus der Prüfung, kein bereits ausgeführter Änderungsauftrag. Es wurden nur die Prüfdateien in diesem Ordner neu angelegt; keine App-Funktion wurde repariert oder umgebaut.
