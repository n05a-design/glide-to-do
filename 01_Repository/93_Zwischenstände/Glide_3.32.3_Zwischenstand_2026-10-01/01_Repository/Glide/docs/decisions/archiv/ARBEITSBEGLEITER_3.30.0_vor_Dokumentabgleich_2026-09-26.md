# Arbeitsbegleiter und Markenfigur – Konzept und Formatentscheidung

Stand 25.09.2026 · Glide 3.30.0 · pflegbarer Begleiter auf der Startseite, stiller Auftritt in Leerzuständen, Assets offen

Punkt 21 des Auftrags vom 18.09.2026, fortgeschrieben mit Punkt 2 des
Startseitenabschnitts vom 19.09.2026. Diese Entscheidung ist nach Regel 4 der
[Arbeitsregeln](../../AGENTS.md) nötig, bevor Assets entstehen oder eine neue
Abhängigkeit eingeführt wird.

## Ergänzung 3.30.0 (Ausbau vom 25.09.2026)

Gismo steht seit dem Ausbau still neben der Hauptaktion leerer Zustände:
leere Liste, leerer Ordner, leeres Tagebuch, leere Suche, leerer Papierkorb
und leere Pinnwand. Das ist ein statischer Auftritt nach Stufe 2 der
Reihenfolge unten:

- 56 px, Zustand `ruhig`;
- ohne Sprechblase, ohne Blinzeln, ohne Führung;
- abgeschaltet mit „Spielereien aus“ in seiner Kachel, dann vollständig weg.

Die Rolle „Leere Zustände erklären“ bleibt beim Satz und der Hauptaktion. Die
Figur macht sie freundlicher, verdeckt nichts und ist nie der einzige Weg zu
einer Information. Ein führender Begleiter mit Hinweisen bleibt an ein
Endnutzer-Onboarding gebunden, das am 25.09.2026 nicht gewählt wurde.
Umsetzung: `empty_state_mascot`,
[Vertrag 3.30](../66_MODERNISIERUNG_3.30.0.md).

## Ergänzung 3.26.0

Standardname ist Gismo; ein vorhandener persönlicher Name bleibt erhalten. Kontextbezogene Sprechblasen, Füttern, Hover-Reaktionen und ein separat gespeicherter Spielereien-Schalter sind umgesetzt. Die Standardreihenfolge zeigt Gismo höher, ohne individuelle Kachelreihenfolgen zu überschreiben. Neue Bildassets sind weiterhin offen und werden nicht durch die Referenzabbildung als geliefert betrachtet.

## Historischer Stand 3.25.0

Die Startseite trägt seit 3.25 eine Kachel `mascot` mit einer **gezeichneten**
Figur (`MascotCanvas`): fünf Zustände, Blinzeln, eine Regung auf Berührung und
ein vergebbarer Name. Sie kommt ohne Bilddatei aus und folgt jedem Design von
selbst, auch den beiden farblosen Minimaldesigns.

Das ändert an dieser Entscheidung nichts, sondern setzt Stufe 2 der Reihenfolge
unten um – statische Auftritte ohne Führungslogik. Die Figur erklärt keine
leeren Zustände, begleitet keinen ersten Start und weist auf nichts hin. Ihr
Zustand spiegelt den Bestand, nicht den Menschen.

**Die Lieferliste unten bleibt vollständig gültig.** Die gezeichnete Figur ist
die Zwischenlösung, bis es Assets gibt; wer sie liefert, tauscht die
Zeichenbefehle gegen `tk.PhotoImage` und lässt alles Übrige stehen.
Siehe [Startseite und Begleiter](../58_STARTSEITE_UND_BEGLEITER_3.25.0.md).

## Die kurze Antwort

**Zwei Dinge, die dieselbe Figur sein dürfen, aber technisch getrennt bleiben.**

| | Markenfigur | Arbeitsbegleiter |
|---|---|---|
| Zweck | Wiedererkennung | Hilfe im richtigen Moment |
| Orte | Startbild, Store, Über-Dialog, Symbol | Startseite, leere Zustände, Abschlüsse |
| Zustände | einer | mehrere |
| Bewegung | keine oder eine | wenige, kurze |
| Kann entfallen | nein | ja, abschaltbar |
| Wann sinnvoll | mit dem ersten Release | frühestens nach dem Endnutzer-Onboarding |

Die Markenfigur ist eine Gestaltungsaufgabe. Der Arbeitsbegleiter ist eine
Produktfunktion mit eigenen Regeln – und mit einem Risiko, das die Figur nicht
hat: Er kann nerven.

## Empfohlenes Ausgangsmaterial

**Vektorquelle als Master, ausgespielte PNG in festen Größen als Lieferung.**

Begründung aus dem tatsächlichen Stack:

- Glide läuft auf Python mit Tk/Tcl 8.6 und **ausschließlich der
  Standardbibliothek**. `tk.PhotoImage` liest GIF, PGM, PPM und – seit Tk 8.6 –
  PNG mit Alphakanal. Mehr nicht.
- **SVG kann Tk nicht darstellen.** Es gäbe die Erweiterung `tksvg`, aber das
  wäre eine neue Laufzeitabhängigkeit und damit ein Bruch mit der Produktregel,
  dass Glide ohne Zusatzinstallation läuft. Eine Vektordatei ist deshalb die
  **Quelle**, nicht das Lieferformat.
- **`PhotoImage` skaliert nur ganzzahlig** (`zoom`, `subsample`). Eine 128er
  Grafik auf 96 Pixel zu bringen, ergibt sichtbare Treppen. Deshalb braucht es
  **fertige Größen**, keine eine Datei zum Skalieren.

### Konkrete Lieferliste

| Datei | Größe | Zweck |
|---|---|---|
| `begleiter_64.png` | 64 × 64 | Zeile, Kachelecke |
| `begleiter_96.png` | 96 × 96 | Startseitenkachel |
| `begleiter_128.png` | 128 × 128 | leerer Zustand |
| `begleiter_192.png` | 192 × 192 | HiDPI der 96er, Über-Dialog |
| `begleiter_256.png` | 256 × 256 | HiDPI der 128er |

Dazu je Zustand ein eigener Satz (siehe unten) und die **Vektorquelle** unter
`20_Grafik_Master/`, damit spätere Größen ohne Nachzeichnen entstehen.

Technische Vorgaben: PNG-24 mit Alphakanal, transparenter Hintergrund, kein
eingebettetes Farbprofil (Tk ignoriert es, und es vergrößert die Datei),
Motiv mit mindestens zwei Pixeln Luft an jeder Kante, damit nichts anstößt.

### Bewegung: Einzelbilder, kein animiertes GIF

Tk kann ein animiertes GIF nur bildweise über `-format "gif -index N"` lesen;
die Zeitsteuerung muss ohnehin die Anwendung übernehmen. Ein GIF bringt also
keinen Vorteil, kostet aber Farbtiefe (256 Farben, harte Transparenzkante).

**Empfehlung: PNG-Einzelbilder je Bewegungsschritt**, benannt
`begleiter_<zustand>_<n>.png`, abgespielt mit `root.after`. Vier bis sechs
Bilder je Bewegung reichen; Glide steuert Dauer und Abbruch selbst, und die
Bewegung lässt sich zusammen mit den Animationen des Dopamin-Designs
abschalten.

**Keine 3D-Datei.** Es gibt nichts, was sie zur Laufzeit darstellen könnte. Ein
3D-Programm darf die Quelle sein, geliefert werden ausgespielte PNG.

## Zustände

Wenige, klar unterscheidbare – nicht eine Stimmung je Situation:

| Zustand | Wann | Bewegung |
|---|---|---|
| `ruhig` | Standard, Startseite | keine |
| `winkt` | erster Start, leerer Bestand | einmalig, kurz |
| `zeigt` | Hinweis auf eine Funktion | einmalig |
| `freut` | Tagesziel erreicht, lange Liste abgeschlossen | einmalig |
| `schlaeft` | nichts steht an, Feierabend | keine oder sehr langsam |

Fünf Zustände × fünf Größen ergeben 25 Dateien plus Bewegungsbilder. Das ist
überschaubar und deckt alles ab, was unten als Rolle beschrieben ist.

## Rollen – und ihre Grenzen

Was der Begleiter tun darf:

- **Leere Zustände erklären.** Eine leere Liste, eine leere Pinnwand, ein
  leerer Papierkorb – dort steht ohnehin Text, und ein Bild daneben macht ihn
  freundlicher, ohne etwas zu verdecken.
- **Den ersten Start begleiten.** Die fünf Dinge, die ein neuer Nutzer wissen
  muss, stehen im QA-Bericht als offener Punkt: Ordner → Listen → Gruppen →
  Aufgaben; Fälligkeit ≠ Bearbeitungstag ≠ Mein Tag; dieselbe Aufgabe in
  mehreren Ansichten; wo die Daten liegen; was Benachrichtigungen können.
- **Abschlüsse quittieren.** Das Tagesziel hat bereits einen Fortschrittsbalken
  und seit 3.22 eine kurze Rückmeldung im Dopamin-Design. Der Begleiter wäre
  deren Gesicht, nicht eine zweite Meldung.
- **Auf Ungenutztes hinweisen** – höchstens einmal je Funktion, abschaltbar,
  und nie während einer Eingabe.

Was er **nicht** tun darf:

- **Nicht ungefragt sprechen, während gearbeitet wird.** Der Maßstab ist die
  bestehende Regel für Erinnerungen: kein Fokusdiebstahl, keine Unterbrechung
  eines offenen Dialogs.
- **Nicht der einzige Weg zu einer Information sein.** Alles, was er sagt, muss
  auch ohne ihn auffindbar sein.
- **Nicht zählen, wie fleißig jemand ist.** Glide leitet aus Klicks oder
  Abschlüssen keine Produktivitätsbewertung ab – das steht seit 3.6 in den
  Gestaltungsregeln und gilt hier genauso.
- **Nicht zur Voraussetzung werden.** Abschaltbar in den Einstellungen, und
  abgeschaltet heißt vollständig weg, nicht kleiner.

## Reihenfolge

1. **Markenfigur zuerst.** Sie kostet nichts an Bedienlogik und wird für Store,
   Symbol und Über-Dialog ohnehin gebraucht.
2. **Statische Auftritte.** Leere Zustände und Startseitenkachel – rein
   dekorativ, ohne Zustandslogik.
3. **Erst danach der Begleiter mit Zuständen**, und erst nachdem es ein
   Endnutzer-Onboarding gibt. Ein Begleiter, der durch etwas führt, das es
   nicht gibt, hat nichts zu sagen.
4. **KI-Anbindung zuletzt**, wenn überhaupt. Sie hängt am Austauschformat aus
   3.23 und an einer Entscheidung über externe Datenübertragung, die noch
   aussteht.

## Was jetzt zu entscheiden ist

Bevor Assets entstehen:

- Wie sieht die Figur aus? (Gestaltungsaufgabe, nicht in diesem Dokument)
- Trägt sie einen Namen? Ein Name macht sie zur Marke und bindet sie an die
  offene Markenprüfung in [PRODUCT_IDENTITY](PRODUCT_IDENTITY.md).
- Soll sie überhaupt sprechen, oder nur zeigen? Eine Figur ohne Text braucht
  keine Tonalität und altert langsamer.

**Keine Arbeit an Assets, bevor diese drei Fragen beantwortet sind.** Fünf
Zustände in fünf Größen sind schnell gezeichnet und noch schneller überholt.

## Wie die Daten zu liefern sind – die kurze Fassung

Ergänzt 3.25.0, weil die Frage erneut gestellt wurde. Es ist dieselbe Antwort
wie oben, nur als Merkzettel:

1. **Vektorquelle als Master** (SVG oder das Projektformat eines
   Zeichenprogramms) unter `20_Grafik_Master/`. Sie wird nie ausgeliefert –
   Tk kann kein SVG darstellen, und `tksvg` wäre eine neue Laufzeitabhängigkeit
   und damit ein Bruch mit der Produktregel.
2. **PNG-24 mit Alphakanal** als Lieferformat, in **festen Größen**: 64, 96,
   128, 192, 256 Pixel im Quadrat. Nicht eine Datei zum Skalieren –
   `tk.PhotoImage` skaliert nur ganzzahlig, und 128 auf 96 ergibt sichtbare
   Treppen.
3. **Je Zustand ein vollständiger Satz**: `ruhig`, `winkt`, `zeigt`, `freut`,
   `schlaeft`. Benennung `begleiter_<zustand>_<groesse>.png`.
4. **Bewegung als PNG-Einzelbilder**, vier bis sechs je Bewegung, benannt
   `begleiter_<zustand>_<groesse>_<n>.png`. Kein animiertes GIF: Tk liest es
   ohnehin nur bildweise, die Zeitsteuerung macht die Anwendung selbst, und ein
   GIF kostet Farbtiefe und eine harte Transparenzkante.
5. **Transparenter Hintergrund, kein eingebettetes Farbprofil**, mindestens
   zwei Pixel Luft an jeder Kante. Tk ignoriert das Profil, und es vergrößert
   nur die Datei.
6. **Keine 3D-Datei, kein Video, keine Schriftdatei.** Es gibt nichts, was sie
   zur Laufzeit darstellen könnte. Ein 3D-Programm darf die Quelle sein.

Ergibt 5 Zustände × 5 Größen = 25 Standbilder plus die Bewegungsbilder.

### Zwei Dinge, die die Figur können muss

* **Auf jedem Untergrund tragen.** Glide hat neun Designs, darunter zwei
  farblose. Eine Figur, die nur auf Weiß funktioniert, funktioniert in einem
  Drittel der Fälle nicht. Am einfachsten: kräftige Silhouette, wenige Flächen,
  keine feinen hellen Linien.
* **Bei 64 Pixeln lesbar bleiben.** Das ist die kleinste Größe. Was dort
  verschwindet, gehört nicht in die Figur.

## Beispiel für einen Auftrag an ChatGPT oder Codex

Ergänzt 3.25.0. Zwei verschiedene Aufträge – ein Bildmodell zeichnet, ein
Codemodell baut ein. Sie gehören nicht in dieselbe Anfrage.

### a) An ein Bildmodell – die Figur entwerfen

```text
Entwirf ein Maskottchen für eine ruhige, lokale Aufgaben-App.

Stil: flache Vektorillustration, kräftige Silhouette, wenige Flächen,
keine feinen hellen Linien, keine Verläufe, keine Schatten, keine Textur.
Kein Text, keine Buchstaben, kein Logo im Bild.

Motiv: eine eigene, freundliche Figur – kein vorhandener Charakter,
keine Marke, kein Tier mit Wiedererkennungswert aus bestehenden Medien.
Sie soll bei 64 Pixeln Kantenlänge noch erkennbar sein.

Format: quadratisch, transparenter Hintergrund, Motiv mit Luft am Rand,
zentriert.

Liefere fünf Varianten derselben Figur in derselben Haltung und Größe:
1 ruhig, 2 winkend, 3 auf etwas zeigend, 4 freuend, 5 schlafend.
Zwischen den Varianten ändert sich nur der Ausdruck, nicht die Figur.
```

Danach von Hand: in ein Vektorprogramm übernehmen, als Master ablegen und in
den fünf Größen als PNG-24 ausspielen. Ein Bildmodell liefert keine
Vektorquelle und keine exakten Pixelgrößen – beides entsteht in diesem Schritt.

### b) An ein Codemodell – die Bilder einbauen

```text
Kontext: Python 3, Tkinter/Tk 8.6, ausschließlich Standardbibliothek,
einzelne Datei app.pyw. Keine neue Abhängigkeit, kein Pillow.

Aufgabe: Ersetze in der Klasse MascotCanvas die Zeichenbefehle durch
geladene PNG-Bilder.

Vorgaben:
- Die Bilder liegen unter src/glide/resources/mascot/ und heißen
  begleiter_<zustand>_<groesse>.png mit zustand aus
  (ruhig, winkt, zeigt, freut, schlaeft) und groesse aus (64, 96, 128, 192, 256).
- Gewaehlt wird die Groesse, die der angeforderten am naechsten liegt und
  nicht groesser ist; niemals hochskalieren.
- tk.PhotoImage-Objekte muessen als Attribut referenziert bleiben, sonst
  sammelt der Garbage Collector sie ein und das Bild bleibt leer.
- Fehlt eine Datei, faellt die Klasse auf die bisherigen Zeichenbefehle
  zurueck. Die App startet in jedem Fall.
- Die oeffentliche Schnittstelle bleibt: set_state(name), start(), react(name).
- Keine Bewegung, wenn app.animations_enabled() False liefert.
- Kommentiere nur, was nicht im Code steht: warum, nicht was.
```

Dieser zweite Auftrag ist bewusst eng: Er nennt die Randbedingungen, die ein
Modell sonst verletzt – Pillow statt Standardbibliothek, hochskalierte Bilder,
verlorene `PhotoImage`-Referenzen, ein Start, der ohne Assets scheitert.
