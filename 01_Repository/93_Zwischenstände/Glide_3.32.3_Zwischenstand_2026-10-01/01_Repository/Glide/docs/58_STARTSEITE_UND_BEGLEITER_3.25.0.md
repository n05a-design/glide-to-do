# Startseite und Begleiter – Glide 3.25.0

Stand 19.09.2026 · Glide 3.25.0 · Aufgabenformat 16 · Einstellungen 2

Die Startseite bestand aus Überschriften, Zahlen und Aufzählungen – lauter
Text. Sie beantwortete viel, aber sie sah nach Arbeit aus. 3.25 bricht das an
drei Stellen auf: mit einem Bild statt einer Zeile, mit einer Figur statt einer
Kennzahl und mit vier Wegen statt zehn.

## Der Begrüßungsbereich

Zehn gleich aussehende Schaltflächen nebeneinander sind keine Auswahl, sondern
eine Wand. Vier davon führen dorthin, wo man täglich hinwill; die übrigen
stellt man einmal ein oder braucht sie selten.

| Bleibt als Fläche | Steht hinter „Weitere …“ |
|---|---|
| Mein Tag | Nächste Aufgabe · Verspätet · Kalender · Vorlagen |
| In Bearbeitung | Neue Liste · Neuer Ordner |
| Eingang | Startseite einrichten · Einstellungen |
| Pinnwand | |

Das ist dieselbe Auflösung, die die Pinnwand in 3.24 bekommen hat: wenige
sichtbare Flächen, alles Übrige in einem Menü, das nach Zweck gruppiert ist.
Bei schmalem Fenster bleiben „Mein Tag“ und „Weitere …“ stehen.

## Die Pinnwand als Bild

Eine Pinnwand ist eine Fläche, auf der Zusammenhänge räumlich stehen. Als Zeile
„Globale Pinnwand · 12 Karten“ geht genau das verloren.

Die neue Kachel `boardpreview` zeichnet stattdessen, was dort liegt:
maßstäblich verkleinert, mit den echten Positionen und den echten Verbindungen.
Ein Klick führt auf die globale Fläche.

`BoardPreview` bekommt die Geometrie über `global_board_preview()`: Karten als
`(x, y, Breite, Höhe)` in Flächenkoordinaten und Verbindungen als Indexpaare.
Die Kartenhöhe ist dabei eine Annahme – die wirkliche entsteht erst beim Aufbau
aus dem Text der Karte –, aber ihr Verhältnis zur Breite und ihre Position
stimmen, und darum geht es in einer Vorschau. Über vierzig Karten wird nicht
mehr gezeichnet; eine verkleinerte Fläche ist dann ohnehin nur noch ein Muster.

Ohne Karten zeigt die Vorschau eine Andeutung aus drei verbundenen Flächen.
Das ist keine erfundene Auskunft, sondern die Einladung, eine anzulegen – und
die Kachel bleibt auch leer ein Bild statt eines leeren Rahmens.

## Der Begleiter

`docs/decisions/ARBEITSBEGLEITER.md` hält seit 3.24 fest, wie die Figur später
geliefert wird: PNG in festen Größen, je Zustand ein Satz, Vektorquelle im
Grafikmaster. Diese Dateien gibt es noch nicht.

Bis sie da sind, zeichnet `MascotCanvas` die Figur mit Zeichenbefehlen. Das ist
kein Platzhalter aus Verlegenheit, sondern die bessere Zwischenlösung: keine
Datei, keine neue Abhängigkeit, kein Farbprofil; sie folgt jedem Design von
selbst – auch den beiden Minimaldesigns – und sie verschwindet rückstandslos,
sobald echte Bilder da sind. Wer die PNG nachliefert, tauscht die
Zeichenbefehle gegen `tk.PhotoImage` und lässt alles Übrige stehen.

Die Figur ist eine eigene Erfindung: ein rundes Wesen mit Antenne, ohne Vorbild
und ohne Namen. Den Namen vergibt, wer will, in der Kachel; er landet in
`settings["mascot_name"]`.

### Zustände

Es sind dieselben fünf wie im Entscheidungsdokument:

| Zustand | Wann | Woran man ihn erkennt |
|---|---|---|
| `sorgt` | Es ist etwas überfällig | Antenne nach hinten, Mund nach unten |
| `freut` | Das Tagesziel ist erreicht | Breiter Mund, Antennenspitze in `confirm` |
| `winkt` | Für heute ist etwas eingeplant | Hand, Blick zur Seite |
| `schlaeft` | Für heute steht nichts an | Augen als Striche, Antenne hängt |
| `ruhig` | Alles Übrige | Ohne Regung |

### Die Grenze, die bleibt

Der Zustand spiegelt den **Bestand**, nicht den Menschen. Das ist keine
Feinheit, sondern die Grenze, die das Entscheidungsdokument zieht: Glide leitet
aus Abschlüssen keine Bewertung ab. Eine Figur, die trauriger wird, weil jemand
wenig geschafft hat, täte genau das.

Sie reagiert deshalb auf das, was auf dem Tisch liegt – überfällige Fristen, ein
erreichtes Tagesziel, ein leerer Tag –, und ist ansonsten guter Dinge. Eine
Berührung ist die einzige Eingabe, die sie kennt: Sie antwortet mit einer Regung
und fällt danach in ihren Zustand zurück. Sie merkt sich nichts, rechnet nichts
mit und verlangt nichts.

### Was die Figur noch nicht ist

Sie ist eine Kachel, kein Begleiter im Sinne des Entscheidungsdokuments: Sie
erklärt keine leeren Zustände, begleitet keinen ersten Start und weist auf
nichts hin. Das bleibt Stufe 3 und setzt ein Endnutzer-Onboarding voraus, das
es noch nicht gibt. Die Reihenfolge aus dem Entscheidungsdokument bleibt damit
gewahrt: erst Markenfigur, dann statische Auftritte, dann Zustandslogik.

## Die Kachel „Nächste Aufgabe“

Die Kachel hieß bis 3.24 „Fokus“ – ein Zustand, kein Gegenstand. Sie zeigt
jetzt dieselbe Aufgabe, die „In Bearbeitung“ unter „Nächste Aufgabe“ zeigt,
und führt mit einer Schaltfläche genau dorthin. Beide Orte benutzen
`task_urgency_rank`; zwei Antworten auf dieselbe Frage wären eine zu viel.

## Kachelübersicht

| Schlüssel | Titel | Standard sichtbar |
|---|---|---|
| `clock` | Uhr, Datum und nächster Termin | ja |
| `welcome` | Begrüßung, Tagesziel und Schnellzugriff | ja |
| `today` | Heute – eingeplant und fällig | ja |
| `focus` | Nächste Aufgabe | ja |
| `week` | Die nächsten sieben Tage | ja |
| `labels` | Labels im Bestand | nein |
| `recent` | Zuletzt bearbeitet | ja |
| `templates` | Mit einer Vorlage starten | ja |
| `impulse` | Impuls für den Tag | nein |
| `calendar` | Kalendervorschau | nein |
| `overdue` | Verspätet | nein |
| `progress` | Fortschritt heute und diese Woche | nein |
| `boards` | Pinnwände | nein |
| `boardpreview` | Pinnwand-Vorschau | **ja (neu)** |
| `mascot` | Begleiter | **ja (neu)** |
| `stats` | Dein aktueller Bestand | ja |

[Übersichtlichkeit und Hierarchie](57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md) ·
[Arbeitsbegleiter](decisions/ARBEITSBEGLEITER.md) ·
[Startseite und Rückmeldung 3.24.0](56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md)
