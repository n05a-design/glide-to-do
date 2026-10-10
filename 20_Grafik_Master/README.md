# Grafik-Master

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2

Hier liegen die Quellen des Glide-Logos und alle freigegebenen Exporte. Glide
selbst und die Paketierung arbeiten mit **Kopien** daraus (siehe unten). Wer
einen Master ändert, erneuert danach die Kopien.

## Struktur

| Ordner | Inhalt | Verwendung |
|---|---|---|
| `01_Logo` | `Glide-Logo-01.svg` und `Glide-Logo.png`: das Zeichen allein, eine Fläche in Glide-Blau | Kopfzeile, „Über Glide“ und Startfenster, dort in der Akzentfarbe der Oberfläche |
| `03_Fav-Icon` | `App-Icon-transparent-02.svg` und `App-Icon-transparent.png`: blaue Fläche mit ausgespartem Zeichen | aktuelles Programmsymbol, Basis für Dock, Taskleiste, Installer und Website |
| `04_Affinity` | `Glide-Logo.af`: die Arbeitsdatei aller Exporte | Quelle |
| `05_Inspiration` | Stilvorlagen und Skizzen, darunter `Glide-Logo-Position.png` (Skizze der Logoposition vom 29.09.2026) und `Inspiration für Glide.png` | Belege, keine Programmdateien |
| `06_Beispielbilder` | Motive für Showcase und Arbeitsdokumente | siehe unten |

Glide-Blau ist `rgb(1,133,225)` = `#0185E1`. Ein Archivordner entfällt seit 03.10.2026: Vorfassungen trägt Git.

**Rechte (öffentliches Repository):** `05_Inspiration` und `06_Beispielbilder` enthalten auch Fremdbilder aus Bildagenturen und Webquellen. Vor einer Veröffentlichung klären, ob sie öffentlich liegen dürfen; sonst entfernen (offen beim Inhaber als I9, siehe [Entwicklungsplan](../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber)).

**Ausgewählte Oberflächenreferenz (10.10.2026, D21):** [Glide-Oberflaeche-Referenz.png](05_Inspiration/Glide-Oberflaeche-Referenz.png), Bild 1 aus drei unabhängig erzeugten Entwürfen. Mit dem integrierten Image-Gen-Werkzeug aus vier eigenen Glide-Fensteraufnahmen mit künstlichen Daten erzeugt. Herkunft, Promptvorgaben, bekannte Abweichungen und Bindung an die native Tk-Oberfläche stehen im [Entwicklungsplan §15.4](../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#154-referenzentwürfe-und-zweite-auswahlrunde-10102026). Gestaltungsgrundlage für die ausgewählten Funktionen, keine Programmressource oder bereits abgenommene Oberfläche.

## Was die App daraus macht (seit 29.09.2026)

- **Laufzeit:** `01_Repository/Glide/src/glide/resources/logo/` enthält
  unveränderte Kopien:
  - `glide-logo.svg` aus `01_Logo/Glide-Logo-01.svg`, PNG aus `01_Logo/Glide-Logo.png`;
  - `glide-app-icon.svg` aus `03_Fav-Icon/App-Icon-transparent-02.svg`, PNG aus `03_Fav-Icon/App-Icon-transparent.png`.

  Das Modul `logo.py` liest sie ein.
- **Warum SVG:** Tk 9 rechnet SVG in jeder Größe scharf. Für die Akzentfarbe
  ersetzt Glide die Füllfarbe `#0185e1` (auch ältere RGB-Schreibweise möglich), bevor das Bild
  entsteht. Die gewählte Variante verwendet direkte Attribute; CSS-Exporte werden ebenfalls verarbeitet. Unter
  Tk 8.6 (ohne SVG) zeichnet Glide dasselbe Zeichen als Leinwandfläche;
  unter Windows und X11 bleibt sie ungeglättet. Als Programmsymbol lädt Glide
  dort nur das PNG des App-Icons und verkleinert es ohne Filterung.
  `glide-logo.png` verwendet die Laufzeit nicht. Ursache und Lösungswege:
  [Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md).
- **Paketierung:** `packaging/baue_symbole.py` erzeugt aus dem App-Icon unter
  `01_Repository/Glide/assets/icons/`:
  - `glide.ico` für Windows (16 bis 256 px);
  - `glide_macos_1024.png` für macOS, mit Apples Rand;
  - `glide_512.png` für Linux und Stores.

  Das macOS-Bundle und die Windows-Verknüpfung nehmen diese Dateien.

## Einen Master ändern

1. In `04_Affinity/Glide-Logo.af` ändern und wie bisher als SVG und PNG
   exportieren. Beim Logo muss es bei **einer** Füllfarbe `rgb(1,133,225)`
   bleiben. Sonst lässt sich die Akzentfarbe nicht mehr einsetzen, und
   `test_logo330` meldet es.
2. PNGs quadratisch exportieren. Die aktuellen PNG-Master vom 01.10.2026 haben 3509 × 3508 Pixel; die SVG-ViewBox ist quadratisch. Die Paketierung leitet ihre Zielgrößen aus SVG ab.
3. Die geänderte Datei nach `src/glide/resources/logo/` kopieren (Namen siehe
   oben) und `python3 packaging/baue_symbole.py` im Ordner
   `01_Repository/Glide` ausführen.
4. `python3 tests/integration/test_logo330.py` ausführen und danach den Stand
   nach `07_Python-Versionen` übernehmen.

## Befunde am Logo-Master (05.10.2026, Entscheidung beim Inhaber)

`01_Logo/Glide-Logo-01.svg` ist ein sauberer Einzelpfad mit gerade-ungerade-Füllregel und für die Darstellung unkritisch. Die folgenden Konstruktionsdetails werden erst in großen Größen (512/1024 px, Druck) sichtbar. Ob sie gewollt sind, entscheidet der Inhaber (Entwicklungsplan LG04).

**Nicht tangentiale Übergänge** (Master-Einheiten, viewBox 841,89):

| Punkt | Lage x / y | Übergang | Knick |
|---|---|---|---|
| 1 | 342,74 / 621,76 | um 4,3° geneigte Gerade → Rundung | 5,9° |
| 2 | 325,94 / 603,24 | Rundung → Gerade | 3,5° |
| 3 | 608,11 / 601,85 | Rundung → Gerade | 2,9° |
| 4 | 525,70 / 475,61 | um 2,6° geneigte Gerade → Rundung | 2,6° |
| 5 | 344,45 / 720,37 | Grundlinie: waagerechtes Stück → um 1,1° steigende Gerade | 1,1° |
| 6 | 561,92 / 124,93 | Rundung → Gerade (Ansatz oben rechts) | 7,3° |

- Weitere Knicke von 0,5–2,7° bei 516,11 / 484,28, 319,63 / 461,24, 326,30 / 562,37, 335,93 / 554,20, 529,95 / 576,66 und 621,39 / 195,69. Muster: Die Rundungen sind tangential zu achsparallelen Kanten angelegt; die anschließenden Geraden wurden geneigt, ohne die Rundungen nachzuführen.
- Fast achsparallele Geraden: 0,01° (Oberkante, 504,75 → 330,20), 0,22° (625,34 / 636,52 → 625,27 / 618,56), 0,50° (325,94 / 603,24 → 326,30 / 562,37), 1,05° (611,56 / 108,77 → 578,13 / 109,38), 1,09° (Grundlinie, Punkt 5). Das Paar mit 6,6° und 6,7° (Ober- und Unterkante des unteren Bogens) ist parallel und damit erkennbar gewollt.
- Kurzsegment: Der Außenumriss endet mit `h-.02`, einem 0,02 Einheiten langen Stück vor dem Schließen.
- Kleine Größen: Der Innenraum des „g“ ist im Logo bei 54 px 3,6 px breit, im App-Symbol bei 16 px 0,78 px, bei 32 px 1,56 px und bei 48 px 2,34 px. Bei 16 und 32 px läuft er auch geglättet zu; eine Kleingrößenfassung mit breiterem Innenraum wäre eine Option.

**Gestaltungsabnahme 10.10.2026 (D45):** Beide vorgelegten Entwürfe sind freigegeben: tangentiale Rundungsanschlüsse und entfernte Kurzsegmente für den Normalmaster, breiterer Innenraum ausschließlich bei 16/32 px. [Logo-Vergleich](05_Inspiration/Glide-Logo-Vergleich-2026-10-10.png) und [App-Symbol-Vergleich](05_Inspiration/Glide-App-Symbol-Vergleich-2026-10-10.png) zeigen alt/neu sowie 16/32/54/512 px. Die freigegebenen Vektorquellen liegen bis zur Übernahme ebenfalls unter `05_Inspiration`: `Glide-Logo-freigegeben.svg`, `Glide-App-Symbol-freigegeben.svg` sowie beide Fassungen `*-klein-freigegeben.svg`. Bei Lieferung 3.37.0 gehen sie in die regulären Master über; die Entwurfsdateien entfallen dann. Die Produktionsmaster und Ressourcen bleiben bis dahin unverändert. Die Affinity-Datei ist binär und wird nicht still als nachgeführt behauptet; maßgebliche neue SVG-/PNG-Exporte werden bei Übernahme ausgewiesen.

Eine Überarbeitung läuft über „Einen Master ändern“ oben.

## Hinweis zur Typografie

Glide bringt zwei privat registrierte Schriften mit, beide unter
`src/glide/resources/fonts/` samt Lizenztexten:

- DejaVu Sans in vier Schnitten;
- Pixelify Sans (SIL OFL 1.1) für die Überschriften im Design „Pixel“.

Eine systemweite Installation ist nicht nötig. Die Dateien müssen mit dem
Programm verteilt werden.

## Beispielbilder für Arbeitsdokumente

`06_Beispielbilder` enthält die vom Inhaber bereitgestellten Motive. Für den [aktiven Showcase](../05_Probelisten_Testdaten/Showcase/README.md) wurden sechs Originaldateien unverändert in die reproduzierbare Fixture-Ablage übernommen. Galerie, Seitenbilder und Aufgabenanhänge demonstrieren ihre Integration. Dateinamen, ursprüngliche Quelle und SHA-256 stehen im [Quellennachweis](../01_Repository/Glide/tests/fixtures/showcase/quellen.json). Die Grafikmaster werden durch Erzeugung und Prüfung nicht verändert.
