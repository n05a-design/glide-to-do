# Pinnwand und Darstellung – Glide 3.22.0

Stand 17.09.2026 · Glide 3.22.0 · Aufgabenformat 16 · Einstellungen 2

## Pinnwand

Die erste Pinnwandstufe aus 3.10 zeigte Karten fester Höhe in einem Raster mit
drei Schaltflächenreihen darüber. 3.22 macht daraus eine Arbeitsfläche.

**Mehr Fläche.** Raster, Vorschau, automatisches Anheften und „Finden“ stehen
jetzt oben in der Zeile „Liste · Pinnwand“. Die Statuszeile „1 von 1 Karten …“
ist entfallen; ihre Tastaturhinweise stehen in der Hinweiszeile der
Reiterleiste. Zusammen gibt das der Fläche rund achtzig Pixel Höhe zurück.

**Frei anordnen ist der Standard.** Wer ordnen will, stellt um; wer frei
arbeitet, muss nicht jedes Mal umstellen. Eine vorhandene Pinnwand behält ihre
gespeicherte Wahl.

**Kartenhöhe folgt dem Inhalt.** Titel, Status, Termin, Checklistenstand,
Beschreibungsauszug, Bildvorschau, Labels und Quellliste ergeben zusammen die
Höhe; eine Aufgabe ohne Zusatzangaben bekommt die Mindesthöhe statt derselben
hohen Fläche wie eine vollständig ausgefüllte. In der geordneten Ansicht füllt
jede Spalte ihre eigene Höhe, statt sich an der längsten Karte auszurichten.

**Bildvorschau.** Ist ein Bildanhang im Format PNG, GIF oder PPM vorhanden,
zeigt die Karte ihn verkleinert. Tk liest diese Formate von Haus aus; JPEG
bräuchte eine zusätzliche Bibliothek und bleibt deshalb außen vor – dort nennt
die Karte weiterhin nur die Anzahl der Anhänge. Der Schalter „Vorschau“
blendet Bilder je Pinnwand aus.

**Alles anheften.** „Alle Punkte anheften“ nimmt den ganzen Bereich auf. Der
Schalter „Auto“ heftet neue Punkte dieser Liste von selbst an – still, ohne
Meldung und ohne die Auswahl zu verändern. Ein Doppelklick auf die freie
Fläche öffnet die Auswahl vorhandener Punkte.

**„Alle Karten finden“ räumt auf, statt umzuschalten.** Bisher setzte es die
Pinnwand auf die geordnete Ansicht zurück – eine frei gebaute Anordnung war
danach weg. Jetzt bleibt die Betriebsart, und die Karten werden an
aufgeräumten Positionen abgelegt.

**Kein Flackern mehr beim Verschieben.** Über der Fläche lag ein gestricheltes
Rechteck, das bei jeder Mausbewegung neu gezeichnet wurde, und beim Ablegen
baute Glide die gesamte Oberfläche neu auf. Jetzt wandert die Karte selbst mit
dem Zeiger, und beim Ablegen wird nur die Pinnwand neu gezeichnet. Dasselbe
gilt für die Schalter: Eine Pinnwandeinstellung ist eine Sache der Pinnwand.

**Bildlaufleiste und Mausbedienung.** Die waagerechte Leiste war als einzige
Fläche der App eine native ttk-Leiste im Systemstil; sie ist jetzt dieselbe
gezeichnete Leiste wie überall sonst. Shift und Mausrad schieben quer, das
gedrückte Mausrad zieht die Fläche.

**Positionen** liegen wie bisher je Pinnwand in `settings.json` und bleiben
über Neustarts erhalten. `pinboards` erhält additiv `preview` und `auto`.

### Grenzen

Zoom, Verbindungslinien, frei skalierbare Einzelkarten, eigenständige
Notizzettel und Dateikarten ohne Aufgabe bleiben außen vor. Die Pinnwand
zeigt vorhandene Aufgabenobjekte; sie ist keine zweite Datenhaltung.

## Mausbedienung in der ganzen App

Knopf 2 war app-weit dem Kontextmenü zugeordnet. Unter macOS ist das richtig –
Tk meldet den Rechtsklick dort als Knopf 2. Unter Windows und Linux ist Knopf
2 das Mausrad; dort war das Schnellscrollen damit blockiert. Seit 3.22 gilt
die Zuordnung nur noch unter macOS. Auf den übrigen Systemen zieht das
gedrückte Mausrad Aufgabenbaum, Seitenleiste, Startseite und Pinnwand; der
Zeiger wechselt für die Dauer des Ziehens. Shift und Mausrad schieben quer.

## Farbmodi

Neben Hell und Dunkel gibt es einen **Farbmodus** in den Einstellungen.

**Kontrast · farbenblindenfreundlich.** Farbfehlsichtigkeit betrifft rund acht
Prozent der Männer und ist fast immer eine Rot-Grün-Schwäche. Die Palette
stammt deshalb aus der Reihe von Okabe und Ito: Ihre Töne – Orange, Himmelblau,
Blaugrün, Blau, Zinnoberrot – bleiben bei Deuteranopie, Protanopie und
Tritanopie unterscheidbar. Der zweite Hebel ist der Kontrast: Text, gedämpfter
Text und Linien werden deutlich stärker gesetzt, als es die normale Oberfläche
braucht. Farbe bleibt dabei nie die einzige Auskunft: Erledigt, Offen,
Wichtigkeit und Fälligkeit stehen weiterhin als Zeichen und Text in der Zeile.

**Dopamin · kräftige Farben.** Dunkle Flächen wie im Dunkelmodus, darauf
kräftigere Töne – dunkler Grund ist hier kein Schmuck, sondern die
Voraussetzung: Gesättigte Farben tragen erst auf einer ruhigen Fläche, auf
Weiß werden sie grell. Dazu kommt eine kurze Rückmeldung beim Abhaken und beim
Erreichen des Tagesziels: ein Wort, eine halbe Sekunde, keine Interaktion. Sie
läuft nur in diesem Modus und ist damit eine Wahl, keine Zumutung.

Beide Modi schalten die Materialoptik mit Glaskanten ab. Sie mischt Flächen
ineinander und nimmt damit genau den Kontrast weg, für den der Kontrastmodus
da ist; im Dopamin-Modus würde sie die kräftigen Töne verwaschen.

Der Modus liegt additiv als `color_mode` in `settings.json` und lässt sich mit
Hell und Dunkel frei kombinieren. Ein unbekannter Wert führt auf „Standard“
zurück. Aufgabenformat, Backup und Vorlagen bleiben unverändert.

### Grenzen

Eine Prüfung mit echten Hilfsmitteln – Bildschirmlupe, Vorlesefunktion,
Kontrastmessung am Gerät – steht aus und bleibt eine manuelle Aufgabe. Die
Rückmeldung im Dopamin-Modus ist eine eingeblendete Beschriftung; Tk kennt
keine echte Transparenz, das Ausblenden läuft über eine Farbmischung zur
Flächenfarbe.

Die Regression steht in `tests/integration/test_features322.py`.

[Reiter und Pinnwand 3.10.0](33_REITER_UND_PINNWAND_3.10.0.md) ·
[Ansichten und Startseite 3.22.0](48_ANSICHTEN_UND_STARTSEITE_3.22.0.md) ·
[Prüfstand](07_QA_BERICHT.md)
