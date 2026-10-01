# Ansichten und Startseite – Glide 3.22.0

Stand 17.09.2026 · Glide 3.22.0 · Aufgabenformat 16 · Einstellungen 2

Dieses Dokument beschreibt vier Nachbesserungen an vorhandenen Ansichten:
Startseite, Aktionen, Tabelle und Filterzeile. Keine davon ändert das
Aufgabenformat.

## Startseite als Kachelraster

Die Startseite war eine Spalte in fester Reihenfolge. Auf einem breiten
Bildschirm blieb rechts die halbe Fläche leer, und abschalten ließ sich allein
die Bestandsstatistik.

Seit 3.22 stehen die Kacheln in einem Raster. Die Spaltenzahl folgt der
Fensterbreite – eine Spalte unter 980 Pixeln, zwei bis 1500, darüber drei –
und lässt sich auf einen festen Wert stellen. Uhr und Begrüßung bleiben als
breite Kopfkacheln darüber; die übrigen verteilt Glide auf die Spalten,
beginnend mit der jeweils kürzesten. Ohne diese Verteilung stünde die hohe
Bestandskachel allein und ließe neben sich eine leere Spalte.

„Startseite einrichten …“ – auf der Startseite selbst, im Einstellungsdialog
und im Ansichtsmenü – schaltet jede Kachel ein und aus und ordnet sie.

Neue Kacheln:

| Kachel | Inhalt |
|---|---|
| Mein Tag | Was für heute eingeplant ist, mit Aufwand und Hinweis auf den Eingang |
| Fokus | Ein konkreter nächster Schritt mit „Öffnen“ und „Erledigt“ |
| Die nächsten sieben Tage | Offene Fälligkeiten je Tag als Balken |
| Labels im Bestand | Die häufigsten Labels offener Punkte mit Anzahl |
| Impuls für den Tag | Ein wechselnder Satz zur Arbeitsweise |

Die Fokuskachel rät nicht, welche Aufgabe die wichtigste ist – das kann kein
Programm wissen. Sie nimmt die naheliegendste: offen, heute eingeplant oder
fällig, danach nach Wichtigkeit und Termin. Gibt es keine, bleibt die Kachel
leer, statt eine Aufgabe zu erfinden.

Bestehende Startseiten bleiben, wie sie waren: Die neuen Kacheln sind
ausgeschaltet, bis jemand sie einschaltet. Der alte Schalter
„Bestandsstatistiken anzeigen“ bleibt mit der Kachel „Dein aktueller Bestand“
gleichbedeutend.

## Aktionen nach Aufgabengruppen

Der Dialog „Alle App-Aktionen“ listete jeden Menübefehl in Menüreihenfolge.
Seit 3.22 stehen die Aktionen in Gruppen mit Zwischenüberschrift und
Zwischenraum – dieselbe Gliederung wie im Tastenkürzel-Fenster: Neu anlegen,
Import, Export, Bearbeiten, Struktur und Gliederung, Planen und einordnen,
Ansichten, Ansichtseinstellungen, Daten und Ablage, Programm und Hilfe. Die
Bereichsauswahl filtert nach diesen Gruppen statt nach Menütiteln. Auswahl,
Suche und Enter überspringen Überschriften. Eine Aktion, die in keine Gruppe
fällt, landet sichtbar unter „Weitere Aktionen“ statt stillschweigend zu
verschwinden; die Regression verlangt, dass diese Gruppe leer bleibt.

## Tabellenansicht

- **Überschriften linksbündig.** Tk zentrierte sie über linksbündigen Werten.
- **Spaltenbreiten selbst ziehen.** Die gezogene Breite wird je Liste
  gespeichert; die Titelspalte wächst nur so lange mit dem Fenster, wie
  niemand sie selbst eingestellt hat.
- **Sortieren durch Klick auf die Überschrift**, in drei Zuständen:
  aufsteigend, absteigend, Listenreihenfolge. Ohne den dritten Zustand gäbe es
  keinen Weg zurück zur tatsächlichen Reihenfolge. Die Richtung steht als ▲
  oder ▼ in der Überschrift. Leere Zellen bleiben in beiden Richtungen am
  Ende, statt beim Umschalten nach oben zu wandern.
- **Neue Spalte „Checkliste“** mit dem Stand `2/5`, sortierbar nach Anteil.
- „Breiten und Sortierung zurücksetzen“ steht im Spaltendialog.

Beides liegt additiv in `settings.json` (`table_column_widths`, `table_sort`)
und gilt je Liste.

## Filterzeile und Rückweg

Die Schaltflächen der Filterzeile trugen ihren Zwischenraum rechts. Dadurch
stand die äußerste acht Pixel vor der Flucht der Eingabezeile darüber,
während zwischen „Suche löschen“ und „Tabelle“ gar kein Abstand war. Seit
3.22 sitzt der Abstand links von jeder Schaltfläche; die Zeile endet bündig,
gleichgültig wie viele Schalter sichtbar sind.

Aus der Tabellenansicht führte bisher kein sichtbarer Weg zurück: Der Schalter
verschwand dort. Er ist jetzt ein Umschalter und heißt in der Tabelle
„Liste“. „Pinnwand“ bleibt ebenfalls erreichbar und führt zuerst in die Liste
zurück.

Die Schaltfläche „Gespeicherte Filter“ ist aus der Seitenleiste entfallen. Sie
stand an deren auffälligster Stelle, obwohl sie selten gebraucht wird, und
zeichnete ihre Ecken gegen den Fensterhintergrund statt gegen die
Kartenfläche – daher der dunkle Block darum. Der Manager bleibt über
„Ansicht › Gespeicherte Filter …“ und die App-Aktionen erreichbar; an den
gespeicherten Filtern selbst ändert sich nichts.

Die Regression steht in `tests/integration/test_features322.py`.

[Tabellenansicht 3.13.0](36_TABELLENANSICHT_3.13.0.md) ·
[Schnellerfassung und gespeicherte Filter](34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md) ·
[Oberfläche und Bedienung 3.9.0](32_UI_UND_BEDIENUNG_3.9.0.md)
