# Grafik-Master

Stand 10.10.2026 · Glide 3.37.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2

Hier liegen die Quellen des Glide-Logos und alle freigegebenen Exporte. Glide
selbst und die Paketierung arbeiten mit **Kopien** daraus (siehe unten). Wer
einen Master ändert, erneuert danach die Kopien.

## Struktur

| Ordner | Inhalt | Verwendung |
|---|---|---|
| `01_Logo` | `Glide-Logo-01.svg` und `Glide-Logo.png`: das Zeichen allein, eine Fläche in Glide-Blau | Kopfzeile, „Über Glide“ und Startfenster, dort in der Akzentfarbe der Oberfläche |
| `03_Fav-Icon` | `App-Icon-transparent-02.svg` und `App-Icon-transparent.png`: blaue Fläche mit ausgespartem Zeichen | aktuelles Programmsymbol, Basis für Dock, Taskleiste, Installer und Website |
| `04_Affinity` | `Glide-Logo.af`: frühere binäre Arbeitsdatei, nicht auf D45 nachgeführt | reguläre SVGs sind seit 3.37.0 maßgeblich |
| `05_Inspiration` | Stilvorlagen und Skizzen, darunter `Glide-Logo-Position.png` (Skizze der Logoposition vom 29.09.2026) und `Inspiration für Glide.png` | Belege, keine Programmdateien |
| `06_Beispielbilder` | Motive für Showcase und Arbeitsdokumente | siehe unten |

Glide-Blau ist `rgb(1,133,225)` = `#0185E1`. Ein Archivordner entfällt seit 03.10.2026: Vorfassungen trägt Git.

**Rechte (öffentliches Repository):** `05_Inspiration` und `06_Beispielbilder` enthalten auch Fremdbilder aus Bildagenturen und Webquellen. Vor einer Veröffentlichung klären, ob sie öffentlich liegen dürfen; sonst entfernen (offen beim Inhaber als I9, siehe [Entwicklungsplan](../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber)).

**Ausgewählte Oberflächenreferenz (10.10.2026, D21):** [Glide-Oberflaeche-Referenz.png](05_Inspiration/Glide-Oberflaeche-Referenz.png), Bild 1 aus drei unabhängig erzeugten Entwürfen. Mit dem integrierten Image-Gen-Werkzeug aus vier eigenen Glide-Fensteraufnahmen mit künstlichen Daten erzeugt. Herkunft, Promptvorgaben, bekannte Abweichungen und Bindung an die native Tk-Oberfläche stehen im [Entwicklungsplan §15.4](../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#154-referenzentwürfe-und-zweite-auswahlrunde-10102026). Gestaltungsgrundlage für die ausgewählten Funktionen, keine Programmressource oder bereits abgenommene Oberfläche.

## Freigegebene Master und Laufzeit (3.37.0)

D45 vom 10.10.2026 gibt den geglätteten Normalmaster und eigene Kleinfassungen
frei: Rundungsanschlüsse sind tangential, das bedeutungslose Kurzsegment
entfällt. Ausschließlich 16/32 px verwenden den breiteren Innenraum.
Grundform und Glide-Blau bleiben erhalten. Die [Logo-Vergleichstafel](05_Inspiration/Glide-Logo-Vergleich-2026-10-10.png)
und die [App-Symbol-Vergleichstafel](05_Inspiration/Glide-App-Symbol-Vergleich-2026-10-10.png)
bleiben der Abnahmebeleg; die übernommenen Entwurfs-SVGs entfallen.

| Reguläre Quelle | Unveränderte Laufzeitkopie in `src/glide/resources/logo` |
|---|---|
| `01_Logo/Glide-Logo-01.svg` | `glide-logo.svg` |
| `01_Logo/Glide-Logo-klein.svg` | `glide-logo-klein.svg` |
| `03_Fav-Icon/App-Icon-transparent-02.svg` | `glide-app-icon.svg` |
| `03_Fav-Icon/App-Icon-klein.svg` | `glide-app-icon-klein.svg` |
| `01_Logo/Glide-Logo.png` | `glide-logo.png` |
| `03_Fav-Icon/App-Icon-transparent.png` | `glide-app-icon.png` |

Die binäre Arbeitsdatei `04_Affinity/Glide-Logo.af` ist **nicht nachgeführt**.
Für den freigegebenen Stand sind die vier regulären SVGs maßgeblich.
Andere vorhandene Varianten sind keine aktuelle Laufzeitquelle.

- **Tk 9:** natives SVG, im Logo mit der aktuellen Akzentfarbe. Die Farbe
  `#0185e1` wird vor dem Rendern ersetzt; keine zusätzliche Bildbibliothek.
- **Tk 8.6:** Logo als transparentes RGBA-PNG in genauer Höhe und Akzentfarbe,
  mit Flächenabdeckung und Gerade-Ungerade-Füllregel aus `logo_raster.py`.
  Der alte ungeglättete Canvas-Weg ist nicht mehr der Anzeige-Rückfall.
- **App-Symbole:** passende PNGs in exakt 16/32/64/256 px, jeweils randlos
  für Windows/Linux und mit macOS-Rand. Tk 8.6 lädt diese Dateien direkt;
  das große PNG und ungefiltertes `subsample` entfallen im Startweg.
- **Paketierung:** `packaging/baue_symbole.py` schreibt `assets/icons/glide.ico`
  (16/24/32/48/64/128/256), `glide_macos_1024.png` und `glide_512.png`.
  ICO und ICNS verwenden bei 16/32 px den freigegebenen Kleinmaster.
  Allgemeine PNG-Exporte bleiben für Dateiverwendung verfügbar; das Logo
  ist dabei auf seinen Zeichenrahmen zugeschnitten, das App-Symbol quadratisch.

## Master und Exporte nachführen

1. Den richtigen regulären SVG-Master bearbeiten. Das Logo bleibt eine
   einfarbige Fläche in `#0185E1`; Kleinmaster ausschließlich für 16/32 px.
2. SVGs unverändert in die oben genannten Laufzeitpfade kopieren.
3. Unter Python 3.14/Tk 9 im Ordner `01_Repository/Glide` erzeugen:

   ```sh
   python3 -B packaging/baue_symbole.py --ressourcen-ziel src/glide/resources/logo
   ```

4. Die allgemeinen Logo-/App-PNGs bytegleich in die regulären Masterpfade
   zurückkopieren. `baue_app.py` erzeugt daraus die ICNS-Fassungen; für den
   Kleinmaster benötigt es weiterhin Tk 9.
5. `test_logo330.py` und `test_logo3370.py` sowie Raster-/Symbol-Unit-Tests
   ausführen; 16/32/54/512 px, beide Akzente, Tk-8.6-Rückfall und Tk 9 prüfen.
   Native Menschen-/DPI-Sichtprüfung gesondert nachweisen.
6. Produktionsversion und eingefrorene Vollprüfung, 07-/Showcase-Abgleich,
   Bundle und Signatur nach dem verbindlichen Lieferweg durchführen.

## Hinweis zur Typografie

Glide bringt zwei privat registrierte Schriften mit, beide unter
`src/glide/resources/fonts/` samt Lizenztexten:

- DejaVu Sans in vier Schnitten;
- Pixelify Sans (SIL OFL 1.1) für die Überschriften im Design „Pixel“.

Eine systemweite Installation ist nicht nötig. Die Dateien müssen mit dem
Programm verteilt werden.

## Beispielbilder für Arbeitsdokumente

`06_Beispielbilder` enthält die vom Inhaber bereitgestellten Motive. Für den [aktiven Showcase](../05_Probelisten_Testdaten/Showcase/README.md) wurden sechs Originaldateien unverändert in die reproduzierbare Fixture-Ablage übernommen. Galerie, Seitenbilder und Aufgabenanhänge demonstrieren ihre Integration. Dateinamen, ursprüngliche Quelle und SHA-256 stehen im [Quellennachweis](../01_Repository/Glide/tests/fixtures/showcase/quellen.json). Die Grafikmaster werden durch Erzeugung und Prüfung nicht verändert.
