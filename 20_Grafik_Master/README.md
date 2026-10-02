# Grafik-Master

Stand 02.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Hier liegen die Quellen des Glide-Logos und alle freigegebenen Exporte. Glide
selbst und die Paketierung arbeiten mit **Kopien** daraus (siehe unten). Wer
einen Master ändert, erneuert danach die Kopien.

## Struktur

| Ordner | Inhalt | Verwendung |
|---|---|---|
| `01_Logo` | `Glide-Logo-01.svg` und `Glide-Logo.png`: das Zeichen allein, eine Fläche in Glide-Blau | Kopfzeile, „Über Glide“ und Startfenster, dort in der Akzentfarbe der Oberfläche |
| `02_App-Icon` | derzeit leer; aktuelle Exporte stehen in `03_Fav-Icon` | frühere weiße Variante wird nicht mehr verwendet |
| `03_Fav-Icon` | `App-Icon-transparent-02.svg` und `App-Icon-transparent.png`: blaue Fläche mit ausgespartem Zeichen | aktuelles Programmsymbol, Basis für Dock, Taskleiste, Installer und Website |
| `04_Affinity` | `Glide-Logo.af`: die Arbeitsdatei aller Exporte | Quelle |
| `05_Inspiration` | Stilvorlagen und Skizzen, darunter `Glide-Logo-Position.png` (Skizze der Logoposition vom 29.09.2026) und `Inspiration für Glide.png` | Belege, keine Programmdateien |
| `Archiv` | überholte Stände dieses Ordners | nur bei historischer Frage öffnen |

Glide-Blau ist `rgb(1,133,225)` = `#0185E1`.

## Was die App daraus macht (seit 29.09.2026)

- **Laufzeit:** `01_Repository/Glide/src/glide/resources/logo/` enthält
  unveränderte Kopien:
  - `glide-logo.svg` aus `01_Logo/Glide-Logo-01.svg`, PNG aus `01_Logo/Glide-Logo.png`;
  - `glide-app-icon.svg` aus `03_Fav-Icon/App-Icon-transparent-02.svg`, PNG aus `03_Fav-Icon/App-Icon-transparent.png`.

  Das Modul `logo.py` liest sie ein.
- **Warum SVG:** Tk 9 rechnet SVG in jeder Größe scharf. Für die Akzentfarbe
  ersetzt Glide die Füllfarbe `#0185e1` (auch ältere RGB-Schreibweise möglich), bevor das Bild
  entsteht. Die gewählte Variante verwendet direkte Attribute; CSS-Exporte werden ebenfalls verarbeitet. Unter
  Tk 8.6 (ohne SVG) zeichnet Glide dasselbe Zeichen als Fläche. Die PNGs
  dienen dort als Programmsymbol.
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

## Hinweis zur Typografie

Glide bringt zwei privat registrierte Schriften mit, beide unter
`src/glide/resources/fonts/` samt Lizenztexten:

- DejaVu Sans in vier Schnitten;
- Pixelify Sans (SIL OFL 1.1) für die Überschriften im Design „Pixel“.

Eine systemweite Installation ist nicht nötig. Die Dateien müssen mit dem
Programm verteilt werden.

## Beispielbilder für Arbeitsdokumente

`06_Beispielbilder` enthält die vom Inhaber bereitgestellten Motive. Für den [aktiven Showcase](../05_Probelisten_Testdaten/Showcase/README.md) wurden sechs Originaldateien unverändert in die reproduzierbare Fixture-Ablage übernommen. Galerie, Seitenbilder und Aufgabenanhänge demonstrieren ihre Integration. Dateinamen, ursprüngliche Quelle und SHA-256 stehen im [Quellennachweis](../01_Repository/Glide/tests/fixtures/showcase/quellen.json). Die Grafikmaster werden durch Erzeugung und Prüfung nicht verändert.
