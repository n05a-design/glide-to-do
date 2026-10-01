# Glide – Feature-Gap-Analyse und Wettbewerbsbefund

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Punkt 1 des Master-Arbeitsauftrags. Diese Analyse erweitert die beiden
vorhandenen Betrachtungen – die
[Gesamtanalyse vom 16.09.2026](Glide_Gesamtanalyse_2026-09-16.md) (Todoist,
TickTick, Things, Notion, Obsidian, Anytype, Evernote) und die
[Konkurrenzanalyse vom 17.09.2026](Glide_Konkurrenzanalyse_2026-09-17.md)
(Notion, Planner, OneNote, Todoist, Google Keep) – um die im Auftrag genannten
Bereiche, die dort fehlten: **Whiteboards und Canvas**, **KI-gestützte
Produktivität**, **local-first Wissensmanagement** und **Tagesplaner**.

---

## 1. Die vier Betrachtungsfelder

### 1.1 Aufgabenmanagement

Der Vergleich der fünf meistgenutzten Apps ergibt drei Befunde, die für Glide
zählen:

| Befund | Beleg | Für Glide |
|---|---|---|
| **Verschachtelte Unteraufgaben sind selten.** Microsoft To Do erlaubt genau eine Ebene. | Vergleich 2026 | Glide hat beliebige Tiefe bis Ebene 100 – ein echter, benennbarer Vorsprung. |
| **Natürliche Spracheingabe ist Standard, aber oft kostenpflichtig.** Bei Todoist steckt sie hinter Pro. | Vergleich 2026 | Glide hat sie seit 3.11 in der Schnellerfassung, ohne Abonnement. |
| **Kalenderansicht und Pomodoro liegen hinter Premium.** TickTick verlangt 35,99 $/Jahr für die Kalenderansicht. | Vergleich 2026 | Glides Kalenderansicht ist Teil der Anwendung. |

Der Preisvergleich ist das stärkste Argument und zugleich das, das am
seltensten ausgesprochen wird: Things kostet einmalig 79,97 $ über drei Geräte,
Todoist 36 $/Jahr, TickTick 35,99 $/Jahr – dauerhaft.

### 1.2 Whiteboards und Canvas

Miro und FigJam waren bisher nicht betrachtet. Die übertragbaren Konzepte:

| Konzept | Bei Miro/FigJam | Für Glide |
|---|---|---|
| **Connectors** – Verbindungen zwischen Objekten | Kernfunktion beider | **In 3.23 umgesetzt** – als Beziehung zwischen Punktkennungen, nicht als gezeichnete Linie |
| **Sticky Notes** | Kernfunktion beider | **In 3.23 umgesetzt** – als echter Long-Task, damit ohne zweite Datenhaltung |
| **Frames** – benannte Bereiche auf der Fläche | Miro | **Sinnvoll, Stufe 2.** Eine Pinnwand mit 200 Karten braucht Gliederung. |
| **Minimap** | Miro | **Sinnvoll, Stufe 3.** Nützlicher als Zoom, weil Text beim Skalieren unlesbar wird. |
| **Präsentationsmodus** über Frames | Miro | **Sinnvoll, Stufe 3**, aber erst nach Frames. |
| **Freihandzeichnen** | beide | **Offen.** Ein Strich ist kein Punkt und bräuchte eine eigene Datenhaltung. |
| **Echtzeit-Mitarbeit, Cursor-Chat, Abstimmungen** | beide | **Nicht sinnvoll.** Setzt Server und Konten voraus. |
| 2.500 Vorlagen (Miro) | Miro | **Nicht sinnvoll.** Glide hat 16 gepflegte Praxisvorlagen; Menge ist hier kein Wert. |

### 1.3 Tagesplaner

Sunsama ist der direkteste Vergleich zu Glides Tagesmodell:

| Funktion | Sunsama | Glide 3.23 |
|---|---|---|
| Tägliches Planungsritual | ja, verpflichtend | **teilweise** – „Mein Tag“ mit Eingangsblock, aber kein geführter Ablauf |
| Geplante Dauer je Aufgabe | ja | **ja** – `estimated_minutes` seit 3.14 |
| Tatsächlich benötigte Zeit | ja, mit Timer | **fehlt** |
| Warnung bei Überbuchung | ja | **ja** – Tageskapazität seit 3.15 |
| Wochenrückblick, Wochenziele | ja | **fehlt** |
| Fokusmodus / Tagesabschluss | ja | **teilweise** – Fokusmodus gibt es seit 3.23 für die Pinnwand, nicht für den Tag |
| Aufgabenimport aus Asana/Trello | ja | **nicht sinnvoll** – setzt Konten voraus |

Sunsama kostet 20 $/Monat. Die drei fehlenden Punkte sind nicht teuer
nachzubauen; sie sind unten aufgeführt.

### 1.4 Local-first Wissensmanagement

Sieben local-first Werkzeuge im Vergleich (Super Productivity, Obsidian Tasks,
Taskwarrior, Joplin, Logseq, todo.txt, Planify). Der Befund ist für Glides
Positionierung wichtiger als jede Einzelfunktion:

**Alle sieben bieten irgendeine Form von Synchronisation – über WebDAV,
Dropbox, Git, Nextcloud, Syncthing oder einen eigenen Dienst.** Glide bietet
als einziges Werkzeug ausdrücklich *keine* und verweist auf einen
synchronisierten Ordner mit der Regel „schließen, abwarten, öffnen“.

Zugleich zeigt der Vergleich: Wer diese Werkzeuge nutzt, zahlt mit
Einrichtungsaufwand („Reichhaltiges Feature-Set erfordert Setup“,
„CLI-Lernkurve“, „hängt von Community-Plugins ab“). Genau dort liegt Glides
Platz: **fertig statt konfigurierbar.**

---

## 2. Feature-Gap-Matrix

Bewertet wird nach dem Stand 3.23.0.

### 2.1 Vollständig vorhanden

Aufgaben mit Unterpunkten beliebiger Tiefe · Long-Tasks · Gruppen ·
Überschriften · Ordner bis fünf Ebenen · Fälligkeit mit Uhrzeit · sechs
Wiederholungsarten · lokale Erinnerungen · Wichtigkeit · Labels · Farben ·
Beschreibungen · lokale Anhänge an Punkt, Liste und Ordner · Checklisten je
Aufgabe · Papierkorb · Rückgängig · dauerhafter Änderungsverlauf ·
Volltextsuche · gespeicherte Filter · Listen-, Tabellen-, Reiter-, Pinnwand-,
Kalender- und Labelansicht · Mein Tag mit Tagesnavigation · Bearbeitungstag ·
geschätzter Aufwand · Tageskapazität · 16 Praxisvorlagen · Vorlagenkatalog ·
TXT-, CSV- und Markdown-Austausch · ICS-Im- und -Export · Druck und PDF ·
portable Aufgabenbackups · vollständiges App-Backup mit Inhaltsvorschau ·
sieben Designs · barrierearmer Kontrastmodus · Austauschformat für fremde
Systeme.

### 2.2 Teilweise vorhanden

| Funktion | Stand | Was fehlt |
|---|---|---|
| Whiteboard | Verbindungen, Notizen, Vollbild, Druck | Zeichnen, Zoom, Bereiche |
| Tagesplanung | Auswahl, Kapazität, Aufwand | geführtes Ritual, Wochenrückblick, tatsächliche Zeit |
| Notizfunktion | Beschreibung, Long-Task, Anhänge | formatierter Text, Verlinkung zwischen Punkten |
| KI-Anbindung | Austauschformat, Import mit Vorschau | Änderungsvorschläge (`patch`), Anbindung an einen Dienst |
| Barrierefreiheit | Kontrastdesigns, Tastaturbedienung, gemessene Kontraste | Screenreader-Abnahme, Hochkontrast-Abnahme |
| Endnutzer-Einstieg | Vorlagen, Beispieldaten | First-Run-Ablauf, Schnellstartanleitung |

### 2.3 Geplant

Systembenachrichtigungen Stufe B (hängt an der Paketierung) · benutzerdefinierte
Felder je Liste · eigene Ansichten auf Basis dieser Felder · Windows-Installer
und macOS-Bundle mit Signierung.

### 2.4 Fehlt – und wäre sinnvoll

Nach Nutzen je Aufwand geordnet. Die ersten vier sind konkret genug, um sie zu
bauen.

1. **Verknüpfte Punkte.** Ein Punkt verweist auf einen anderen, und beide
   zeigen den Rückverweis. Die Datenstruktur dafür entstand in 3.23 bereits
   für Pinnwandverbindungen – dieselbe Beziehung, nur ohne Fläche darum. Das
   ist der günstigste offene Punkt mit dem größten Nutzen: Es löst
   „Besprechungsnotiz mit drei Aufgaben verbinden“ und ist die Vorstufe zu
   echten Abhängigkeiten.
2. **Bereiche auf der Pinnwand.** Ein benannter Rahmen, der Karten umschließt
   und mit ihnen wandert. Macht eine Fläche mit vielen Karten erst benutzbar
   und ist die Voraussetzung für einen Präsentationsmodus.
3. **Wochenrückblick.** Eine Ansicht über sieben Tage: was war geplant, was
   wurde fertig, was wanderte weiter. Die Daten liegen vollständig vor –
   `planned_date`, `done` und der Änderungsverlauf. Es fehlt nur die Ansicht.
4. **Geführter Tagesbeginn.** Ein Ablauf, der die Punkte des Eingangs und die
   heute fälligen nacheinander zeigt und fragt: heute, später oder gar nicht.
   Sunsamas stärkste Idee, und sie braucht keinen Server.
5. **Vorlagen mit Eingabefeldern.** Projektname, Objektadresse, Ansprechpartner
   einmal eingeben und in vorgesehene Felder übernehmen. Steht seit 3.10 im
   Vorrat und wäre für die Branchenvorlagen besonders wirksam.
6. **Zeiterfassung je Punkt.** Geplante gegen tatsächliche Dauer. Erst
   sinnvoll, wenn der Wochenrückblick existiert – sonst entstehen Zahlen ohne
   Ort, an dem man sie ansieht.
7. **Abhängigkeiten und Meilensteine.** „Veröffentlichung erst nach Freigabe“.
   Braucht gerichtete Beziehungen und eine Prüfung auf Kreise – eine eigene
   Funktion, nicht aus Pinnwandlinien abgeleitet.

### 2.5 Fehlt – und ist nicht sinnvoll

| Funktion | Warum nicht |
|---|---|
| Eigener Cloud-Sync | Verlangt Server, Konten, Konfliktauflösung und Betrieb. Widerspricht der Produktgrenze „ohne Konto, ohne Cloudzwang“. |
| Mobile App | Hieße Sync hieße Server hieße Konto. Eine Produktentscheidung, keine Lücke. |
| Team, Zuweisung, Kommentare | Glide ist ein persönliches Werkzeug. Planner und Todoist Business decken das. |
| Rich-Text-Editor mit Blöcken | Notion- und Obsidian-Gebiet. Beschreibung und Long-Task reichen für Aufgabenkontext. |
| Wissensgraph, Backlinks, Plugins | Obsidian gewinnt diesen Wettbewerb; er ist zehn Jahre alt. |
| Eingebettete Datenbanken | Verlangt ein allgemeines Feldsystem – aus einem Planer würde ein Baukasten. |
| Gantt-Diagramm | Setzt Abhängigkeiten und Ressourcen voraus. Für einen persönlichen Planer überdimensioniert. |
| Habit-Tracker, Pomodoro | TickTick-Gebiet. Ein Zähler ohne Bewertung wäre möglich, aber ohne erkennbaren Nutzen für die Planung. |
| Echtzeit-Mitarbeit auf der Pinnwand | Server und Konten. |
| 2.500 Vorlagen | Menge ist kein Wert; 16 gepflegte schlagen 2.500 ungepflegte. |
| Telemetrie, auch anonym | Ausdrückliche Produktgrenze. |

### 2.6 Redundant – und deshalb in 3.23 entfallen

| War | Ist |
|---|---|
| Design + Farbmodus + Materialoptik | **eine** Designauswahl |
| Kachel „Mein Tag“ + Kachel „Heute fällig“ | **eine** Kachel „Heute“ mit zwei Abschnitten |
| Eingang als Hauptpunkt neben „Mein Tag“ | Eingang als Unterpunkt von „Mein Tag“ |
| Sieben Tabellen mit eigener Einrichtung | **eine** Komponente `prepare_table` |
| „Verspätet“ gleichrangig neben „In Bearbeitung“ | eingerückt als dessen Teilmenge |

Das ist die Anwendung von „Form follows Function“ auf den Bestand: Jedes
sichtbare Element muss eine eigene Funktion haben, die sich nicht mit einer
anderen überschneidet.

---

## 3. Was 3.23 im Wettbewerb verändert

| Merkmal | Glide 3.23 | Wer das sonst hat |
|---|---|---|
| Verbindungen zwischen Aufgaben auf einer Fläche | ja, strukturiert gespeichert | Miro (ohne Aufgabenmodell), Notion (nur in Datenbanken) |
| Austauschformat mit Capability-Angabe | ja | keines der verglichenen |
| Barrierearmer Kontrastmodus | ja | keines der verglichenen |
| Checkliste je Aufgabe | 50 Schritte | Planner 20, Todoist über Teilaufgaben |
| Fälligkeit und Bearbeitungstag getrennt | ja | Things („When“ vs. Deadline) |
| Vollständig offline, ohne Konto | ja | Taskwarrior, todo.txt – beide ohne Oberfläche dieser Art |
| Kosten | keine | Things 79,97 $ einmalig, Todoist 36 $/Jahr, TickTick 35,99 $/Jahr, Sunsama 240 $/Jahr |

---

## 4. Empfohlene Reihenfolge

Die Reihenfolge folgt nicht dem Nutzen einzelner Funktionen, sondern der
Frage, was Glide gerade am meisten fehlt.

**Zuerst, vor jeder weiteren Funktion:**

1. **Native Abnahme auf Windows und macOS.** Der Prüfstand läuft unter Linux
   mit Xvfb; die Sichtprüfung auf beiden Zielplattformen steht offen.
2. **Endnutzer-Einstieg.** Fünf Sätze beim ersten Start. Glide hat inzwischen
   mehr Konzepte, als jemand von selbst findet.
3. **Paketierung.** Ein grüner Quelltest ist kein installierbares Produkt –
   und Systembenachrichtigungen hängen daran.

**Danach, in dieser Reihenfolge:**

4. Verknüpfte Punkte (2.4 Nr. 1)
5. Wochenrückblick (Nr. 3)
6. Bereiche auf der Pinnwand (Nr. 2)
7. Geführter Tagesbeginn (Nr. 4)
8. Vorlagen mit Eingabefeldern (Nr. 5)

**Die strategische Frage bleibt dieselbe wie am 16.09.:** Soll Glide ein
fokussierter persönlicher Planer bleiben oder ein konfigurierbares
Arbeitsdaten-System werden? Diese Analyse ändert die Antwort nicht:
**task-first bleiben.** Jede Zeile in 2.5 ist ein Weg, der von dort wegführt.

---

## Quellen

- [Todoist vs TickTick vs Things 3: 5 To-Do Apps Ranked (2026)](https://unstar.app/blog/todoist-ticktick-things-3-microsoft-todo-apple-reminders-todo-apps-ranked-2026)
- [Best Local-First To-Do Apps in 2026](https://super-productivity.com/blog/best-local-first-todo-apps-2026/)
- [FigJam vs Miro (2026)](https://hedrick.io/post/figjam-vs-miro)
- [Sunsama Review 2026](https://efficient.app/apps/sunsama)
- Die beiden vorhandenen Analysen vom 16. und 17.09.2026 in diesem Ordner.

Preise und Funktionsumfänge sind Marktangaben zum Abrufzeitpunkt und vor einer
Veröffentlichung erneut zu prüfen.
