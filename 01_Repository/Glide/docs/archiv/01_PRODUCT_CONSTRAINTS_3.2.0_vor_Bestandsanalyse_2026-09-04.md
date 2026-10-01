# Produktgrenzen

## Verbindlich

- Local First: Aufgaben, Notizen, Einstellungen und Anhänge funktionieren offline.
- Kein Benutzerkonto und keine Anmeldung.
- Keine Cloudpflicht und keine stillen Netzwerkzugriffe für Kernfunktionen.
- Nutzerdaten liegen im plattformgerechten Benutzerordner, nie im Installationsverzeichnis.
- Windows und macOS bleiben gleichwertige Zielplattformen.
- Datenkompatibilität hat Vorrang vor interner Umstrukturierung.
- Nur Python-Standardbibliothek plus Tk; jede weitere Laufzeitabhängigkeit braucht eine dokumentierte Entscheidung.

## Bewusste Nicht-Ziele des aktuellen Stands

- Cloud-Synchronisation
- Mehrbenutzerbetrieb
- Telemetrie oder Analytics
- Lizenzserver oder Aboverwaltung
- Push-Infrastruktur
- vollwertiger Rich-Text-/Blockeditor wie Notion
- Anbindung an externe Kalender, Mail- oder Kontaktdienste
- wiederkehrende Aufgaben und Erinnerungen mit Benachrichtigung
- Mehrsprachigkeit der Oberfläche

Langtexte und Anhänge sind bewusst leichtgewichtig umgesetzt: als Beschreibungstext einer Liste oder eines Ordners, als Aufgabenbeschreibung und als verwaltete lokale Dateikopie innerhalb eines Punkts.

Die Kalenderansicht seit 2.7 ist ausdrücklich **kein** Widerspruch zum Nicht-Ziel oben: sie zeigt ausschließlich die eigenen Fälligkeiten als Wochen- oder Monatsraster, liest und schreibt keinen externen Kalender und braucht kein Netzwerk.

## Labels

Seit 2.7 lassen sich Punkte, Listen und Ordner mit **Labels** versehen. Ein
Label ist ein benannter Marker mit eigener Farbe; derselbe Datensatz kann
mehrere tragen. Die Labelfarbe nutzt dieselbe Palette wie Listen- und
Aufgabenfarben, bleibt aber eine eigene Eigenschaft: die Aufgabenfarbe hebt
einen einzelnen Punkt hervor, das Label ordnet ihn einer wiederkehrenden
Kategorie zu.

Labels von Listen und Ordnern erscheinen ausschließlich in der großen
Darstellung im Hauptbereich – als farbige Zeile unter dem Seitentitel und in der
Labelspalte der Ordnerübersicht. Die Seitenleiste bleibt bewusst frei davon,
damit sie eine reine Navigationsspalte bleibt.

Nicht vorgesehen sind: Labels als Filterkriterium mit eigener Ansicht,
hierarchische Labels und automatisch vergebene Labels.

## Papierkorb

Gelöschte Listen und Ordner landen seit 2.7 im Papierkorb statt sofort
verworfen zu werden. Ein Eintrag bleibt ein vollständiger Datensatz und wird in
jedem Komplettbackup mitgesichert – einschließlich seiner Anhänge. Der
Papierkorb ist keine Versionsgeschichte, aber er nimmt **seit 2.11.0 auch
einzelne Punkte** auf – samt Unterpunkten, Beschreibung, Anhängen und der
Stelle, an der sie standen. Das war die Antwort auf einen gemeldeten
Datenverlust: Vorher entfernte „Löschen“ einen Punkt sofort und endgültig.
Er fasst höchstens 200 Einträge.

## Symbole

Jedes Symbol der Oberfläche ist ein **Textzeichen** und steht in einer zentralen
Tabelle (`ICONS`). Farbige Emoji sind seit 3.2.0 ausgeschlossen: Sie kommen aus
einer Ersatzschrift des Systems, ignorieren die eingestellte Textfarbe, sind auf
Windows und macOS verschieden breit und passen nicht zuverlässig in die feste
Zeilenhöhe des Aufgabenbaums. Ein Textzeichen nimmt dagegen die Farbe seiner
Zeile an – deshalb steht das Fälligkeitssymbol bei einem überfälligen Punkt in
der Warnfarbe.

Nicht vorgesehen sind: Bilddateien als Symbole, ein Symbolsatz je Theme und vom
Nutzer wählbare Symbole.

**Ausnahme, Stand 3.2.0:** Zwei Marker außerhalb von `ICONS` sind weiterhin
farbige Emoji und wurden beim Umbau übersehen:

| Konstante | Zeichen | Wo sichtbar |
|---|---|---|
| `IMPORTANCE_MARKERS[3]` | 🚩 (U+1F6A9) | Aufgabenbaum, Kalender, Zwischenablage – Wichtigkeit „hoch“ |
| `GROUP_MARKER` | 📁 (U+1F4C1) | Aufgabenbaum vor Gruppentiteln **und** im TXT-Export |

Der Test prüft nur `ICONS` und hat sie deshalb nicht gemeldet. Die Umstellung
ist offen und keine reine Aufräumarbeit: Das Zeichen für „hoch“ ist eine
Gestaltungsentscheidung, und `GROUP_MARKER` wird beim TXT-**Import** wieder
gelesen – ein neues Zeichen macht ältere Exportdateien beim Reimport zu
gewöhnlichen Aufgaben.

## Struktur der Ablage

Seit 2.9.0 dürfen Ordner ineinander liegen – höchstens fünf Ebenen tief. Das ist
die Grenze, ab der eine Seitenleiste unlesbar wird und niemand mehr findet, was
er sucht. Ein Ordner kommt nie in sich selbst oder in einen eigenen Unterordner.

Nicht vorgesehen sind: Listen in Listen, Ordner über mehrere Speicherorte hinweg
und Verknüpfungen, die dieselbe Liste an zwei Stellen zeigen. Eine Liste liegt an
genau einer Stelle.

## Struktur innerhalb einer Liste

Seit 2.6.0 kann ein Punkt eine **Gruppe** sein. Das ist die bewusste, minimale Antwort auf den Wunsch nach Ordnern innerhalb einer Liste: eine Gruppe ist derselbe Datensatz wie eine Aufgabe, nur ohne Status, Fälligkeit und Wichtigkeit. Es entsteht kein zweites Objektmodell, keine zusätzliche Hierarchieebene und kein neuer Speicherort.

Seit 2.8.0 kommen zwei weitere Arten hinzu, nach demselben Grundsatz: derselbe Datensatz, nur anders dargestellt. Ein **Long-Task** ist eine gewöhnliche Aufgabe, deren vollständiger Text über bis zu fünf Zeilen sichtbar bleibt – gedacht für die eine Aufgabe, die einen ganzen Satz braucht, nicht als Ersatz für den Beschreibungstext. Eine **Zwischenüberschrift** gliedert eine Liste und lässt die Nummerierung darunter wieder bei 1 beginnen; sie trägt wie eine Gruppe keinen Status.

Beide sind zugleich über ein festes Label erreichbar. Das ist bewusst kein zweiter Mechanismus, sondern dieselbe Eigenschaft aus einer anderen Richtung: das Label ist die Art. Deshalb lassen sich „Long-Task“ und „Überschrift“ nicht löschen und nicht umbenennen – ein Label ohne zugehörige Art wäre eine Lüge über den Punkt.

Nicht vorgesehen sind: Gruppen über Listengrenzen hinweg, Gruppen als eigenständige Filterkriterien, automatische Gruppierung nach Datum oder Wichtigkeit, mehr als fünf angezeigte Zeilen je Long-Task und eigene Zeilenumbrüche in jeder anderen Punktart. Wer nach Fälligkeit gruppieren möchte, nutzt die abgeleiteten Ansichten „In Bearbeitung“ und „Verspätet“.
