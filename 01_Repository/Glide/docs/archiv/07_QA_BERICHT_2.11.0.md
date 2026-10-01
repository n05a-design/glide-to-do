# QA-Bericht 2.11.0

Stand: 03.09.2026 · App-Version 2.11.0 · Datenformat 10
Laufzeit der Prüfung: Python 3.12 mit Tk 8.6 unter Linux (Xvfb), Fenstergröße
1400 × 1100.

Dieser Bericht hält fest, **was tatsächlich geprüft wurde, mit welchem Ergebnis
und was ungeprüft bleibt**. Er ersetzt keine manuelle Prüfung auf den
Zielplattformen; welche Punkte dort offen sind, steht am Ende.

Der Schwerpunkt dieser Runde lag auf einem gemeldeten Datenverlust: Beim
Auflösen einer Gruppe verschwand ein Punkt aus der Mitte – nicht im Papierkorb,
nicht archiviert. Abschnitt 3 hält fest, was die Untersuchung ergeben hat.

---

## 1 Zusammenfassung

| Prüfung | Umfang | Ergebnis |
|---|---|---|
| Syntaxprüfung | `ast.parse` über den gesamten Quellstand | bestanden |
| `pyflakes` | Quellstand und alle drei Testdateien | keine Meldung |
| Integrationstest | 2 723 Zeilen, Funktionen und Datenformate | bestanden |
| Datenintegritätstest | 601 Zeilen, Bestandswächter, Gruppen, Papierkorb, Maske | bestanden |
| App-weiter Durchlauf | 828 Zeilen, elf Phasen über alle Bedienwege | keine Befunde |
| Zufallsläufe | rund 7 600 simulierte Bedienschritte in drei Läufen | keine Abweichung |
| Persistenz-Stresslauf | Speichern, Backup, Import, Rotation, Exporte | bestanden |
| Tote-Code-Analyse | AST über alle Klassen | keine ungenutzten Methoden oder Konstanten |
| Sichtprüfung | Hell und Dunkel, je zehn Aufnahmen | bestanden |

Quellstand: 13 689 Zeilen, 484 Methoden, eine Klasse für die Anwendung plus
fünf Widget-Klassen und eine Ausnahmeklasse.

---

## 2 Automatisierte Prüfungen

### 2.1 Integrationstest – `tests/integration/test_glide.py`

Prüft Funktionen und Datenformate an echten Daten, nicht an Attrappen. Der Test
isoliert den Datenordner über `GLIDE_DATA_DIR` und fasst echte Nutzerdaten nie
an.

Abgedeckt:

- **Datenformate** – Referenzbestände der Formate 10, 9, 8, 7, 6, 5, 4 und 2
  laufen durch die aktuelle Normalisierung. Jede Migration ist additiv; kein
  Bestand verliert beim Laden Inhalt.
- **Verschachtelte Ordner** – Ebenen, Vorfahren, direkte und rekursive Zähler,
  Unterbaumhöhe, Ordner- und Listenpfad, Kreis- und Tiefenschutz, Ablegezonen,
  Tastaturwege, Auflösen mit Nachrücken, Papierkorb über ganze Zweige.
- **Aufgabenarten** – Aufgabe, Long-Task, Zwischenüberschrift, Gruppe: Anlegen,
  Umwandeln in beide Richtungen, Gleichlauf mit den festen Labels, Zählweise,
  Nummerierungsneustart, Abstandszeile, Umbruchlogik.
- **Label-Chips** – Maße, Farbmischung, Helligkeitssuche, Kontrast aller sieben
  Palettenfarben in beiden Themes, Umbruch bei schmaler Fläche, Kopfzeile.
- **Persistenz** – Speicher- und Ladeidempotenz, Backup-Rundlauf mit Anhängen
  aus aktiven und gelöschten Listen, abgebrochener Import ohne Nebenwirkung,
  Schreibfehler ohne Datenverlust, fünf Varianten beschädigter Speicherdateien,
  kollidierende IDs, vollständige Rotationslogik.
- **Austauschformate** – TXT-, Markdown- und CSV-Export; TXT-Rundlauf für alle
  vier Arten einschließlich Wichtigkeit, Erledigt-Zustand und Uhrzeit.
- **Oberfläche** – Systemzeilen, responsive Spaltenbreiten, Hover-Tags,
  Bildlaufleisten in den Dialogen, Feldkanten, Kontextmenüs, Sicherheitsbereich
  des Seitenleistenzählers.

### 2.2 Datenintegritätstest – `tests/integration/test_datenintegritaet.py`

Neu in dieser Runde. Prüft die eine Zusage, an der die Runde hängt: **Eine
Umbauaktion darf keinen Punkt verlieren.**

| Abschnitt | Inhalt |
|---|---|
| 1 | Bestandswächter: rollt einen absichtlich herbeigeführten Verlust zurück, meldet ihn, lässt gültige Umsortierungen unangetastet, zählt den Papierkorb mit |
| 1b | Papierkorb für einzelne Punkte: Löschen, Titel, Unterpunkte, Wiederherstellen an dieselbe Stelle, Speicher-Rundlauf, Backup-Prüfung, verlorene Herkunft |
| 2 | **130 Kombinationen** aus Gruppieren und Auflösen: fünf Listenaufbauten über alle vier Arten mit Unterpunkten × jede Auswahl von zwei bis fünf Punkten, benachbart und verstreut. Nach jedem Schritt: Bestand vollständig, Baum vollständig, nichts nur hinter einem Klapppfeil sichtbar |
| 2b | Verschachtelte Gruppen, leere Gruppe |
| 3 | Ziehen mit Mehrfachauswahl: Reihenfolge nach und vor dem Ziel, Shift+Drag, Schutz vor dem eigenen Unterbereich |
| 4 | Drop auf die Seitenleiste: Rückfrage, Verschieben, Ablehnung ohne Wirkung |
| 5 | Strg+Klick ist Mehrfachauswahl und nicht das Kontextmenü – plattformgerecht geprüft |
| 6 | Gemeinsame Eingabemaske: identische Felder beim Anlegen und Bearbeiten, Uhrzeit über Formular, Übernahme, TXT- und Speicher-Rundlauf, erweiterte Eingabe |

### 2.3 App-weiter Durchlauf – `tests/integration/audit_app.py`

Prüft nicht einzelne Funktionen, sondern die **Wege durch die App**. Er hält
beim ersten Fehler nicht an, sondern meldet alle Abweichungen gesammelt – so
zeigt ein Lauf das ganze Bild statt des ersten Symptoms.

| Phase | Inhalt |
|---|---|
| 1 | Ordnerhierarchie, Kreis- und Tiefenschutz, Verschieben, Auflösen, Papierkorb |
| 2 | Speicher-Rundlauf, beschädigte Ordnerdaten, Schemaprüfung |
| 3 | Jede Ansicht mit Filter, Suche, Kopfzeile, Statistik, Eingabefeld |
| 4 | Jedes Kontextmenü für jede Zeilenart und jede Mehrfachauswahl |
| 5 | Jede erwartete Tastenbindung an Baum, Seitenleiste, Systembereich, Fenster |
| 6 | Ein- und Ausrücken per Tastatur, Sortieren, Ablegezonen |
| 7 | Long-Task-Text, Arten-Umwandlung, TXT-Rundlauf aller vier Arten |
| 8 | Aufbau jedes Dialogs samt Anzahl der Bildlaufleisten |
| 9 | Simuliertes Drag & Drop aller Quell-/Ziel-Kombinationen, Rückgängig, Punktverschiebung, Löschen eines Long-Tasks, Aktionen von einer Fortsetzungszeile aus, Suche, Backup-Rundlauf, Anlegen in Unterordnern |
| 10 | Label-Chips: Kontrast aller Farben in beiden Themes, Maße, Mischung, Umbruch, Kopfzeile |
| 11 | Abschlussprüfung: Endstand schemakonform, keine Fehlermeldung aufgetreten |

### 2.4 Zufallsläufe

Drei Läufe außerhalb der Testsuite, gezielt für die Fehlersuche geschrieben.
Sie feuern die Ereignisse, die auch die Oberfläche auslöst, statt Methoden
direkt aufzurufen, und prüfen nach **jedem** Schritt eine Bilanz.

| Lauf | Umfang | Prüfung nach jedem Schritt |
|---|---|---|
| Datenbilanz | 60 × 40 Schritte | Kein Punkt der Startliste fehlt, keine Kreise in den Daten |
| Listenübergreifend | 80 × 45 Schritte | Kein Punkt fehlt in **allen** Listen und im Papierkorb – einschließlich Löschen, Rückgängig, Listenwechsel, Filter, Drop auf die Seitenleiste |
| Anzeige gegen Daten | 100 × 40 Schritte | Alles aufgeklappt: Der Baum zeigt genau die Daten, keine Zeile zu viel, keine zu wenig |

Ergebnis: keine Abweichung. Die Läufe liegen als Werkzeug bei, nicht als Teil
der Testsuite – sie sind für die Fehlersuche gedacht, nicht für einen
reproduzierbaren Testlauf.

### 2.5 Tote-Code-Analyse

Ein AST-Durchlauf über alle Klassen sucht Methoden und Konstanten, die nirgends
im Quellstand vorkommen. Ergebnis: **keine**.

Entfernt wurde in dieser Runde `themed_date_picker`: Datum und Uhrzeit setzt
jetzt `DueField`, damit Anlegen, Bearbeiten und das Menü „Fälligkeit“ dieselbe
Auswahl zeigen.

---

## 3 Der gemeldete Datenverlust

**Befund: Die Gruppenfunktion war nicht die Ursache.**

`dissolve_selected_group`, `group_selected_items`, `remove_item_by_id`,
`filter_top_level_selection`, `move_item_relative_to_target`, `make_subitem`,
`toggle_indent_selected`, `indent_selected`, `outdent_selected` und
`move_selected_items` wurden gelesen und über rund 7 600 simulierte
Bedienschritte geprüft. Keine dieser Funktionen verliert einen Punkt.

Gefunden wurden stattdessen fünf Ursachen, die zusammen genau das gemeldete
Bild ergeben:

| # | Befund | Warum es wie ein Datenverlust aussieht |
|---|---|---|
| 1 | **`delete_item` ging am Papierkorb vorbei.** Ein Punkt wurde sofort und endgültig entfernt – ohne Rückfrage, ohne Papierkorbeintrag. | Genau die Beschreibung: nicht im Papierkorb, nicht archiviert, fort. Nur Rückgängig half, und das ist nach einem Neustart verbraucht. Besonders bei Mehrfachauswahl: Nach einer Shift-Bereichsauswahl zum Gruppieren löscht ein versehentliches Entf den ganzen Bereich. |
| 2 | **Strg+Klick öffnete das Kontextmenü statt mehrfach auszuwählen.** `<Control-Button-1>` war auf allen drei Bäumen gebunden; Tk bevorzugt die spezifischere Bindung, sodass `<Button-1>` unter Windows gar nicht mehr ankam. | Der eingebaute Strg-Zweig war toter Code. Der Nutzer musste auf Shift-Bereichsauswahl ausweichen – und die reicht über alle Ebenen hinweg, was größere Auswahlmengen erzeugt als beabsichtigt. |
| 3 | **Unterpunkte wurden beim Gruppieren unsichtbar.** Ein Punkt auf oberster Ebene wurde offen gezeichnet, derselbe Punkt eine Ebene tiefer zugeklappt. | Von außen nicht von einem Datenverlust zu unterscheiden: Der Punkt steht in den Daten, ist aber weder in der Liste noch im Papierkorb zu sehen. |
| 4 | **Ein Drop auf die Seitenleiste verschob kommentarlos** in eine andere Liste – ohne Rückfrage, ohne Meldung. | Beim Sortieren nach links abgerutscht, und die Auswahl liegt in einer anderen Liste. Wer dort nicht sucht, hält sie für verloren. |
| 5 | **Ziehen bewegte bei Mehrfachauswahl nur einen Punkt.** | Die übrigen bleiben unbemerkt an ihrem Platz; die Auswahl scheint sich aufzulösen. |

Alle fünf sind behoben. Zusätzlich wurde ein **Bestandswächter** eingeführt, der
die Zusage strukturell absichert statt sie an der Fehlerfreiheit einzelner
Methoden hängen zu lassen: Er zählt vor und nach jeder Umbauaktion alle
Punkt-IDs in allen Listen und im Papierkorb und stellt bei einer Lücke den
vorherigen Stand her. Siehe `docs/06_DATA_BACKUP_MIGRATION.md`.

---

## 4 Weitere Befunde und Behebungen dieser Runde

| # | Befund | Gefunden durch | Behebung |
|---|---|---|---|
| 1 | Ein Dialog konnte höher werden als der Bildschirm; die Schaltflächen standen dann unter dem sichtbaren Rand. | Sichtprüfung der neuen Eingabemaske | `_center_dialog` begrenzt Höhe und Breite auf `DIALOG_MAX_SCREEN_SHARE`; die Maske bringt eine eigene Bildlaufleiste mit. |
| 2 | Ein gelöschter Punkt hätte beim Backup seine Anhänge verloren, weil nur Listen als Anhangsquelle galten. | Erweiterung der Schemaprüfung | `validate_backup_schema` zählt auch den Punkt eines Papierkorbeintrags als Anhangsquelle. |
| 3 | Die Labelauswahl zeigte zwei Zeilen; ab einer Handvoll Labels war ständig zu scrollen. | Vorgabe aus dem Arbeitsauftrag | Zunächst eine Chipfläche über rund fünf Zeilen; seit 2.12.0 ein Aufklappfeld (`LabelDropdown`), das geschlossen eine Zeile belegt. |

---

## 5 Sichtprüfung

Je zehn Aufnahmen in Hell und Dunkel:

- Liste mit Aufgabe, Long-Task, Uhrzeit und Chips
- Neue Eingabemaske, leer und mit Zielliste
- Punktdetails mit Kalender, Uhrzeit, Labels, Beschreibung und Anhängen
- Punktdetails (Long-Task) mit mehrzeiligem Titelfeld
- Fälligkeitsfenster aus dem Kontextmenü
- Schmales Fenster: Label- und Fälligkeitsspalte weichen

---

## 6 Was ungeprüft bleibt

Diese Punkte kann kein Skript in dieser Umgebung beantworten. Sie stehen als
Aufgaben in der Veröffentlichungs-Checkliste.

| Bereich | Warum ungeprüft |
|---|---|
| Windows-Darstellung | Getestet wird unter Linux/Tk. Schriftmetrik, DPI-Skalierung, dunkle Titelleiste und native Dateidialoge verhalten sich dort anders. |
| macOS-Darstellung | Dasselbe, zusätzlich Cmd-Tastenkürzel, Cmd+Q über die Speicherabfrage und Gatekeeper. **Neu wichtig:** Unter macOS bleibt Strg+Klick das Kontextmenü und Cmd+Klick wird die Mehrfachauswahl – das ist auf einem echten Mac zu bestätigen. |
| Reale Nutzerdaten | Der Test arbeitet mit erzeugten Beständen. Eine Migration mit einer Kopie des echten Datenordners steht aus. |
| Echte Eingabegeräte | Drag & Drop wird simuliert, nicht mit Maus oder Trackpad ausgeführt. |
| Große Bestände | Geprüft wurden bis rund 200 Aufgaben. Verhalten bei mehreren Tausend ist nicht gemessen. |
| Installation und Signatur | Es gibt noch kein Build-Artefakt (siehe Checkliste). |

---

## 7 Prüfung wiederholen

```powershell
$env:GLIDE_DATA_DIR = "$env:TEMP\Glide-Test"
python tests/integration/test_glide.py
python tests/integration/test_datenintegritaet.py
python tests/integration/audit_app.py
python -m pyflakes src/glide/app.pyw tests/integration/*.py
```

Alle drei Testdateien isolieren den Datenordner selbst; die Variable oben ist
nur eine zusätzliche Sicherung. Ein Lauf dauert zusammen unter drei Minuten.
