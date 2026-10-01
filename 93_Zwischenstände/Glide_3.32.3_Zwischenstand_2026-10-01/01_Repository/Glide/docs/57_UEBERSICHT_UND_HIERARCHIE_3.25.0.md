# Übersichtlichkeit und Hierarchie – Glide 3.25.0

Stand 19.09.2026 · Glide 3.25.0 · Aufgabenformat 16 · Einstellungen 2

3.25 hat keine neue große Funktion. Der Auftrag war ein anderer: „form follows
function“ – eine Oberfläche, die auf die Kernfunktionen zurückkommt. Das
bedeutet an den meisten Stellen weniger, nicht mehr: weniger Text in einer
Auswahl, weniger Schaltflächen nebeneinander, weniger Einträge in einem Menü.
An einigen Stellen bedeutet es das Gegenteil – dort, wo bisher nichts stand,
wo aber eine Frage offen war.

## Was die Kopfleiste und die Masken betrifft

### Schaltflächen sind so breit wie ihre Beschriftung

Eine `RoundedButton` bekam ihre Breite bisher als Zahl mitgegeben. War die
Beschriftung länger, lief der Text über die Fläche hinaus und wurde an beiden
Enden abgeschnitten: „s HTML speicher“ statt „Als HTML speichern“. Sichtbar
wurde das im Druckdialog, betroffen war jede Fläche mit langer Beschriftung –
und jede Fläche, sobald jemand die Oberflächenschrift vergrößert.

Seit 3.25 misst eine Schaltfläche ihre Beschriftung selbst (`text_width`) und
wächst, wenn sie muss. Die mitgegebene Breite ist damit eine Untergrenze, keine
Festlegung. `fit_text=False` schaltet das für Flächen ab, deren Breite von
außen bestimmt wird.

### Feldpaare stehen auf einer Linie

Zwei Felder nebeneinander bekamen bisher je eine Zelle, in der Beschriftung und
Feld untereinander gepackt wurden. Bricht eine Beschriftung auf zwei Zeilen um –
„Tagesziel · erledigte Aufgaben (0 = aus)“ tut das in halber Spaltenbreite –,
rutscht das Feld darunter eine Zeilenhöhe tiefer als sein Nachbar.

`FieldPairGrid` trennt beides: Beschriftungen stehen in einer eigenen
Rasterzeile und werden an ihrer Unterkante ausgerichtet, die Felder in der
nächsten. Ein Umbruch verschiebt dann nur noch die Beschriftung. Nebenbei fällt
die zweite Fehlerquelle weg – beide Spalten tragen denselben halben
Zwischenraum, statt dass eine ihn allein trägt und dadurch schmaler ist.

Angewandt in den Einstellungen (Tagesziel und Tageskapazität), in der Punktmaske
(Art/Wichtigkeit, Farbe/Zielliste) und in der Planungseingabe (Bearbeitungstag
und Aufwand).

`ResponsiveColumns.MIN_COLUMN_WIDTH` steigt von 380 auf 440 Pixel. 380 reichte,
damit nichts abbricht – nicht, damit eine Spalte lesbar bleibt.

### Die Anzeigeauswahl ist kürzer und sitzt unter ihrem Auslöser

Die fünf Erklärungen waren ganze Sätze und dreimal so lang wie die Namen
daneben. Jetzt eine Zeile, gleicher Satzbau, kein Punkt am Ende:

| Umfang | Was zusätzlich erscheint |
|---|---|
| Kompakt | Nur Titel, Termin und Labels |
| Standard | Zusätzlich Symbole für Beschreibung, Checkliste und Anhänge |
| Checklisten | Zusätzlich jeden Schritt als abhakbare Zeile |
| Anhänge | Zusätzlich jeden Anhang mit Name und Größe |
| Erweitert | Zusätzlich Checkliste, Anhänge und Beschreibung |

`DropdownPopup.show` kennt zusätzlich `align`. Ein Schalter am rechten Rand der
Kopfleiste öffnete seine Auswahl bisher nach rechts und wurde dort an den
Fensterrand geschoben – sie stand dann neben ihrem Auslöser statt unter ihm.
`align="auto"` legt die rechte Kante der Fläche auf die rechte Kante des
Auslösers, sobald dieser in der rechten Fensterhälfte steht.

## Was die Übersichten betrifft

### „Erweitert“ arbeitet auch in abgeleiteten Ansichten

In „Mein Tag“, „In Bearbeitung“, „Verspätet“ und „Labels“ antwortete die
Schaltfläche „Erweitert“ mit dem Hinweis, man möge die Aufgabe in ihrer
Quellliste öffnen. Das war die Antwort auf eine andere Frage: Wer dort auf
„Erweitert“ drückt, will einen neuen Punkt anlegen, nicht einen bestehenden
bearbeiten.

Die Maske führt die Zielliste ohnehin als Feld. Gebraucht wird also keine
geöffnete Liste, sondern eine sinnvolle Vorbelegung – und die bringt die
Ansicht mit:

| Ansicht | Was vorbelegt wird |
|---|---|
| Mein Tag | Bearbeitungstag = der betrachtete Tag |
| Labels | Das Label der Gruppe, in der die Auswahl steht |
| In Bearbeitung, Verspätet, Gespeicherte Filter | Nur die Zielliste |

Der Punkt geht dabei immer über seine Zielliste. In einer abgeleiteten Ansicht
zeigt `self.items` auf die zuletzt geöffnete Liste; dorthin anzuhängen wäre
nicht nachvollziehbar.

### Abschnitte sind aufklappbar

Die Abschnittsüberschriften der Übersichten waren flache Zeilen zwischen den
Punkten. Sie gliederten, ließen sich aber nicht schließen – und in „Mein Tag“
steht unter „Eingang“ alles, was noch keinen Tag trägt, was die eigentliche
Tagesplanung aus dem Bild schieben kann.

Ein Abschnitt ist jetzt eine Elternzeile mit Aufklapppfeil; seine Punkte hängen
als Kinder darunter. Der Zustand gehört zur Ansicht und nicht zu den Daten und
liegt deshalb in `settings["overview_sections_closed"]` – er übersteht den
Neustart. Unbekannte Kennungen entfernt die Normalisierung.

### „Nächste Aufgabe“ – ein Abschnitt und eine Rangfolge

Neu ist ein eigener Abschnitt am Kopf von „In Bearbeitung“, der genau eine
Aufgabe zeigt. Sie steht auch ohne ihn oben in der Liste – aber nur als erste
von vielen, und „als Nächstes“ ist etwas anderes als „zuerst sortiert“.

Welche Aufgabe das ist, entscheidet `task_urgency_rank` – eine Stelle für beide
Orte, an denen die Frage gestellt wird:

| Stufe | Bedingung |
|---|---|
| 0 | heute als Bearbeitungstag eingeplant |
| 1 | überfällig |
| 2 | für einen früheren Tag eingeplant |
| 3 | alles Weitere |

Innerhalb einer Stufe entscheidet die Wichtigkeit, dann der Termin. Bis 3.24
beantwortete die Übersicht die Frage nach Fälligkeit und die Startseitenkachel
nach einer eigenen Rangfolge – zwei Antworten auf dieselbe Frage. Die Kachel
heißt jetzt „Nächste Aufgabe“ statt „Fokus“ und führt mit einer Schaltfläche
genau in diesen Abschnitt.

Die nächste Aufgabe wird aus den übrigen Abschnitten herausgenommen: Zweimal
dieselbe Zeile wäre keine Hervorhebung, sondern eine Dublette.

## Was die Pinnwand betrifft

### Verbindungen liegen vor den Karten und enden an ihrem Rand

Die Linie lief bis 3.24 von Mittelpunkt zu Mittelpunkt und lag deshalb
zwangsläufig unter beiden Karten – samt ihrer Pfeilspitze, die genau dort
sitzt. Sichtbar war nur das Stück dazwischen, eine Richtung war nicht zu
erkennen.

`border_point` schneidet die Sichtlinie am Kartenrand; die Linie beginnt drei
Pixel davor und endet drei Pixel davor. Dort ist die Spitze frei, und die Frage,
ob sie vor oder hinter der Karte liegt, stellt sich nicht mehr. Zusätzlich
liegen die Linien jetzt vor den Karten (`tag_raise`), damit sie auch zwischen
überlappenden Karten sichtbar bleiben. Die Spitze schrumpft mit der Linie:
Zwischen zwei nebeneinanderliegenden Karten bleiben wenige Pixel, und eine
Spitze in voller Größe wäre größer als der Abstand, den sie überbrückt.

Die Druckausgabe benutzt dieselbe Geometrie – gedruckt sähe eine Linie von
Mittelpunkt zu Mittelpunkt anders aus als die auf dem Schirm.

### Rückweg, Reiterbeschriftung und Kontextmenü

* Die globale Pinnwand gehört zu keiner Liste und hatte deshalb keinen Reiter,
  der zurückführt. Escape brachte zwar in die Übersicht, aber nichts sagte das.
  Der Rückweg steht jetzt als erste Fläche der Reiterzeile: `◂ Übersicht`.
* Ein Reiter trug zwanzig Zeichen und dreizehn Pixel Innenabstand je Seite.
  Beides zusammen ergab breite Flächen, in denen der Text am Rand klebte.
  Jetzt vierzehn Zeichen, am Wortende geschnitten, und 22 Pixel je Seite. Den
  vollständigen Titel zeigt der Tooltip.
* Ein Rechtsklick auf eine Karte wählt sie aus und zeigt genau die Aktionen,
  die es für sie gibt; auf freier Fläche zeigt er, was man dort anlegen kann.

## Was das Programm als Ganzes betrifft

### Menüs nach Zweck gruppiert

„Ansicht“ trug fünfundzwanzig Einträge hintereinander: Reiter neben Papierkorb
neben Design neben Mein Tag. Ein Menü, in dem man jedes Mal sucht, ist kein
Menü, sondern eine Liste.

In der obersten Ebene steht jetzt nur noch, worum es geht:

| Menü | Gruppen |
|---|---|
| Datei | Neu anlegen · Importieren · Exportieren · Datenaustausch · Sicherung · Vorlagen · Datenablage |
| Bearbeiten | Zwischenablage · Punkt ändern · Struktur |
| Ansicht | Ansichten · Mein Tag · Liste · Reiter · Pinnwand · Oberfläche |
| Hilfe | Handbuch · Tastenkürzel · Fehlerprotokoll · Über Glide |

Die Beschriftungen bleiben Wort für Wort dieselben: Sie sind die Schlüssel,
über die `ACTION_GROUPS` und die durchsuchbaren App-Aktionen jede Aktion ihrer
Aufgabengruppe zuordnen. `build_menu` baut jedes Menü aus einer Beschreibung
und meldet es dem Theme an – ein vergessenes `self.menus` kann es damit nicht
mehr geben.

### Handbuch

`Hilfe › Handbuch …` (F1) beantwortet die Frage, die weder die
Tastenkürzelübersicht noch die App-Aktionen beantworteten: *wo finde ich das?*
Neun Bereiche, je Baustein eine Zeile aus Name, Wirkung und Ort, mit Suchfeld
über alle drei Spalten. Die Tabelle steht als `MANUAL_SECTIONS` im Quelltext,
damit die Prüfwerkzeuge sie gegen die tatsächlichen Menüpunkte halten können.

### Über Glide führt zur Datenablage

Der Wechsel der Arbeitsdateien stand nur im Menü „Datei“. Gesucht wird er aber
dort, wo der Speicherort genannt wird. „Über Glide“ trägt jetzt drei
Folgeaktionen: Arbeitsdateien verschieben, Standardordner benutzen, Ordner
öffnen. Für den Cloudbetrieb – dieselbe Ablage auf mehreren Geräten – ist das
der Einstieg.

`themed_message_dialog` nimmt dafür `extra_buttons`; ein Hinweisfenster, das zu
etwas führen soll, braucht damit keinen eigenen Nachbau der ganzen Maske.

### Zwei Designs ohne Farbe

„Minimal hell“ und „Minimal dunkel“ sind kein abgeschwächter Kontrastmodus,
sondern die Gegenrichtung: Was sonst über Farbe unterschieden wird – überfällig,
heute fällig, erledigt, wichtig –, unterscheidet sich hier über Helligkeit. Je
dringender, desto größer der Abstand zur Fläche; im hellen Design heißt das
dunkler, im dunklen heller.

Jeder Wert ist ein echter Neutralton (R = G = B). Geprüft ist jede Schrift auf
jeder Fläche, auf der sie vorkommt: normaler Text über 4,5:1, Platzhalter über
3:1. Ein Design darf über `text_on_accent` bestimmen, welche dunkle Schrift auf
seiner Auswahlfläche steht – die gemessene Voreinstellung ist das blaugraue
`#15171C`, und das wäre in einem Design ohne Farbton der einzige farbige Ton im
ganzen Fenster.

### Rückmeldung auf jede Aktion

Eine Fahne beim Erledigen und Schweigen bei allem anderen sagt: Nur das eine
zählt. Gemeint war das Gegenteil. `feedback(schluessel, anzahl)` meldet jetzt
jeden abgeschlossenen Vorgang – Liste angelegt, Ordner angelegt, kopiert,
eingefügt, gruppiert, angeheftet, verbunden, rückgängig – aus einer Tabelle
`ACTION_FEEDBACK_TEXTS` mit Symbol, Einzahl und Mehrzahl.

Wie viel gemeldet wird, entscheidet `settings["action_feedback"]`:

| Wert | Wirkung |
|---|---|
| `auto` (Vorgabe) | Im Dopamin-Design jede Aktion, sonst nur Erledigtes und erreichte Ziele |
| `milestones` | Nur Erledigtes und erreichte Ziele |
| `all` | Jede Aktion |

Der Hauptschalter „Bewegte Rückmeldung“ bleibt darüber: Ist er aus, meldet sich
nichts.

## Neue Einstellungswerte

Alle additiv und mit Vorgabe; **kein Formatsprung**.

| Wert | Bedeutung | Vorgabe |
|---|---|---|
| `overview_sections_closed` | zugeklappte Abschnitte der Übersichten | leer |
| `action_feedback` | Umfang der Rückmeldung | `auto` |
| `mascot_name` | Name des Begleiters | leer |

`home_tile_order` und `home_tiles_hidden` nehmen zusätzlich `boardpreview` und
`mascot` auf.

[Startseite und Begleiter](58_STARTSEITE_UND_BEGLEITER_3.25.0.md) ·
[Navigation und Pinnwand 3.24.0](55_NAVIGATION_UND_PINNWAND_3.24.0.md) ·
[QA-Bericht](07_QA_BERICHT.md)
