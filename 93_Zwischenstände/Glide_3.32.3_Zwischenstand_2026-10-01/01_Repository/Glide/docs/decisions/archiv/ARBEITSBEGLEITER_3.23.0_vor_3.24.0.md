# Arbeitsbegleiter und Markenfigur – Konzept und Formatentscheidung

Stand 18.09.2026 · Glide 3.23.0 · Konzept, noch nicht umgesetzt

Punkt 21 des Auftrags vom 18.09.2026. Diese Entscheidung ist nach Regel 4 der
[Arbeitsregeln](../../AGENTS.md) nötig, bevor Assets entstehen oder eine neue
Abhängigkeit eingeführt wird.

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
