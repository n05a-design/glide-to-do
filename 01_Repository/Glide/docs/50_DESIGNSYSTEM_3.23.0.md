# Designsystem – Glide 3.23.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

## Was sich geändert hat

Bis 3.22 stand die Erscheinung von Glide an drei Stellen der Einstellungen:

| Feld | Werte |
|---|---|
| Design · Hell / Dunkel | Light Mode, Dark Mode |
| Farbmodus | Standard, Kontrast, Dopamin |
| Materialoptik mit Glaskanten verwenden | Häkchen |

Erst ihre Kombination ergab das Bild. Acht Kombinationen waren möglich, zwei
davon wirkungslos: Kontrast und Dopamin schalteten die Glasoptik ohnehin ab,
weil sie Kontrast kostet beziehungsweise gesättigte Töne verwäscht. Wer den
Dopamin-Modus wählte, sah trotzdem ein Häkchen, das nichts tat.

Seit 3.23 gibt es genau eine Auswahl: **Design**.

## Die sieben Designs

| Schlüssel | Name | Grundpalette | Farbschicht | Materialoptik | Gegenstück |
|---|---|---|---|---|---|
| `light` | Hell | hell | – | nein | `dark` |
| `dark` | Dunkel | dunkel | – | nein | `light` |
| `glass_light` | Liquid Glass · hell | hell | – | ja | `glass_dark` |
| `glass_dark` | Liquid Glass · dunkel | dunkel | – | ja | `glass_light` |
| `dopamine` | Dopamin · kräftige Farben | dunkel | Dopamin | nein | – |
| `contrast_light` | Kontrast hell · farbenblindenfreundlich | hell | Kontrast | nein | `contrast_dark` |
| `contrast_dark` | Kontrast dunkel · farbenblindenfreundlich | dunkel | Kontrast | nein | `contrast_light` |

## Aufbau

Ein Design ist eine Zeile in der Registry `DESIGNS` in `app.pyw` mit vier
Angaben:

- **`base`** – welche der beiden Grundpaletten (`THEMES`) gilt. Dieser Wert
  bleibt die Antwort auf die Frage „hell oder dunkel“, die an rund dreißig
  Stellen gestellt wird: von der Labelfarbe über die Kartenzeichnung bis zur
  Windows-Titelleiste. `theme_name` wird deshalb weiterhin geführt, aber
  abgeleitet statt gesetzt.
- **`layer`** – welche Farbschicht darüberliegt (`None`, `"contrast"`,
  `"dopamine"`). `color_mode()` liest sie und bleibt als Name erhalten.
- **`glass`** – ob die Materialoptik greift.
- **`partner`** – wohin der Hell-/Dunkel-Schalter der Kopfzeile führt.

**Ein weiteres Design braucht eine weitere Zeile, keinen zusätzlichen Code.**
Wer etwa ein gedämpftes Design für abends ergänzen will, trägt Grundpalette,
Farbschicht, Materialoptik und Gegenstück ein und nimmt den Schlüssel in
`DESIGN_ORDER` und `DESIGN_SWATCH` auf.

## Übernahme aus 3.22 und früher

Beim ersten Start von 3.23 entsteht aus den drei alten Werten einmalig ein
Design. Die Zuordnung ist vollständig und verliert nichts:

| Alter Zustand | Neues Design |
|---|---|
| `color_mode = dopamine` | Dopamin |
| `color_mode = contrast`, `theme = dark` | Kontrast dunkel |
| `color_mode = contrast`, `theme = light` | Kontrast hell |
| `glass_mode = true`, `theme = dark` | Liquid Glass · dunkel |
| `glass_mode = true`, `theme = light` | Liquid Glass · hell |
| `glass_mode = false`, `theme = dark` | Dunkel |
| `glass_mode = false`, `theme = light` | Hell |

Da die Materialoptik seit 3.7 standardmäßig an war, landet ein Bestand ohne
eigene Wahl bei einem der beiden Liquid-Glass-Designs – und sieht damit
unverändert aus.

**Die drei alten Werte bleiben geschrieben.** `settings.json` trägt weiterhin
`theme`, `color_mode` und `glass_mode`, abgeleitet aus dem Design. Eine ältere
Glide-Fassung, die dieselbe Datei öffnet – etwa aus einem synchronisierten
Datenordner –, findet dort, was sie erwartet, statt auf ihre Vorgaben
zurückzufallen. Geschrieben werden sie ausschließlich in `set_design`.

Das Einstellungsformat bleibt **2**: `design` ist additiv, wie
`sidebar_visible` seit 3.9.

## Der Hell-/Dunkel-Schalter

Der Schalter in der Kopfzeile bleibt, was er war – ein Weg zwischen hell und
dunkel –, verlässt aber das gewählte Design nicht mehr. Wer im Kontrastdesign
arbeitet, landet im hellen Kontrastdesign und nicht im normalen Hellmodus.
Das Dopamin-Design hat kein helles Gegenstück und ist sein eigener Partner:
Der Schalter tut dort nichts und benennt das Design, statt einen Wechsel zu
versprechen, den es nicht gibt.

## Liquid Glass

Tk zeichnet keine weichgezeichneten Flächen; ein echter selektiver
Desktop-Blur bleibt außerhalb des lokalen Tk-Funktionsstands. Tiefe entsteht
deshalb aus dem, was Tk kann:

1. **Verlauf** über dem oberen Drittel jeder Karte, oben heller als unten, aus
   höchstens zwölf waagerechten Streifen. Das ist derselbe Reiz, den eine
   gewölbte Glasfläche im Licht erzeugt. Die Streifen werden nach oben hin
   schmaler, damit sie die gerundete Ecke nicht als Treppe überzeichnen.
   Darunter bleibt die volle Flächenfarbe stehen, sodass Text überall auf
   demselben Grund sitzt und der Kontrast nicht wandert.
2. **Helle Innenkante** und **dunkle Außenkante** – die Ebenenstaffelung.
3. **Gemischte Oberflächenfarben**: Fläche, Karte, Eingabefeld und Linie
   werden gegen einen kühlen Ton gemischt.
4. Unter Windows zusätzlich der **native DWM-SystemBackdrop**, wenn die
   Plattform ihn anbietet.

Fällt die Plattform zurück, bleibt die Oberfläche als lesbare Farbvariante
vollständig funktionsfähig. Der Verlauf kostet höchstens zwölf Rechtecke je
Karte, unabhängig von deren Höhe.

## Kontrast als Rechenregel

> **Fortgeschrieben am 26.09.2026:** Die Rechenregel gilt weiter. Seit 3.30
> tragen „Hell“ und „Dunkel“ kontrastfeste Schriftfarben in der Grundpalette;
> alle Designs sind zusätzlich über `legible_text_roles` und
> `RoundedButton.legible_text` abgesichert. Die Messung übernimmt
> `test_kontrast330.py`. Einzelheiten:
> [Vertrag 66, Abschnitt 2.6](66_MODERNISIERUNG_3.30.0.md).

Seit 3.23 wird Kontrast gemessen, nicht geschätzt.

- `contrast_ratio(a, b)` liefert das Verhältnis nach WCAG.
- `readable_text_color(fläche)` wählt zwischen heller und dunkler Schrift nach
  dem tatsächlich gemessenen Kontrast, nicht nach einer Helligkeitsschwelle.
  Eine Schwelle liegt bei gesättigten Tönen regelmäßig daneben.
- `ensure_contrast(fläche, schrift)` zieht eine Fläche so weit nach, bis die
  vorgegebene Schrift darauf 4,5:1 erreicht – gemischt gegen Schwarz oder
  Weiß, sodass der Farbton erhalten bleibt.

**Angewandt auf die Auswahl:** Sie trägt weiße Schrift, weil sie das in beiden
Betriebssystemen und in Glide immer getan hat. Gemessen erreichte Weiß auf dem
Lila der Standardpalette aber nur 3,5:1. Statt die Schrift zu wechseln und das
Bild umzuwerfen, wird die Fläche eine Spur tiefer gezogen. Nur wo Weiß von
vornherein aussichtslos ist – auf dem hellen Blau des Kontrastdesigns –,
entscheidet der Kontrast, und die Schrift wird dunkel.

Geprüft wird das über alle 49 Kombinationen aus sieben Designs und sieben
Akzentfarben.

## Hover

Ohne ausdrückliche Zuordnung nimmt Tk für den Zustand `active` – die
Tabellenüberschrift unter dem Mauszeiger – seine eigene helle Systemfarbe,
behält aber die Schriftfarbe des Themes. Im Dunkelmodus ergab das weiße Schrift
auf weißem Grund: Die Überschrift verschwand, sobald man sie anfasste. Beide
Tabellenstile tragen jetzt eine ausdrückliche Hover-Farbe, deren Schrift aus
`readable_text_color` folgt.

## Grenzen

- Kein Designwechsel je Liste oder je Ansicht. Das Design gilt für die
  Anwendung.
- Kein eigener Farbeditor. Die Akzentfarbe bleibt eine Auswahl aus der
  Palette; frei gewählte Farben müssten gegen jede Rolle auf Kontrast geprüft
  werden, und das wäre eine eigene Funktion.
- Die Designwahl steht in den persönlichen Einstellungen und damit **nicht** im
  Aufgabenbackup, sondern im vollständigen App-Backup.
