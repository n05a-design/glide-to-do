# Standardschrift Roboto Mono und durchsichtiger Pixelgrund – Glide 3.50.0, 03.11.2026

Inhaberauftrag 03.11.2026 (D59): Roboto Mono aus `20_Grafik_Master/07_Fonts/01_Roboto_Mono` als mitgelieferte, sofort wirksame und weiterhin wechselbare Standardschrift; Lizenz vom Inhaber geprüft (SIL OFL 1.1 ohne reservierten Schriftnamen, kostenloser und kostenpflichtiger Vertrieb erlaubt). Zusätzlich: neue Pixelzeichnungen ohne weißen Kasten, wenn sie als Symbol in Seiten und Seitenleiste stehen. Danach Prüfung aller Fenster und Ansichten nach den [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md), Commit und Push. [Plan §21.52](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2152-standardschrift-roboto-mono-und-durchsichtiger-pixelgrund).

## Umsetzung

- **Schriftdateien:** `RobotoMono-Regular/Bold/Italic/BoldItalic.ttf` (statische Schnitte, Version 3.001) und `OFL-RobotoMono.txt` unter `src/glide/resources/fonts`, SHA-256 in `provenance.json`. Variable Schriften sind nicht mitgeliefert: Tk wählt Schnitte über Gewicht/Neigung, nicht über Achsen.
- **Registrierung und Vorgabe:** `register_private_fonts` registriert jede TTF des Ordners prozessweit (Windows `FR_PRIVATE`, macOS CoreText, Linux Fontconfig). `PREFERRED_UI_FONTS` beginnt mit „Roboto Mono“; ohne Eintrag in den Einstellungen ist sie ab dem ersten Start die Oberflächenschrift. Das Feld „Schriftfamilie (leer = Roboto Mono; mitgeliefert auch DejaVu Sans)“ wechselt wie bisher.
- **Symbole:** Roboto Mono enthält keine der geometrischen ICONS-Zeichen. `symbol_policy.BUNDLED_SYMBOL_FAMILY` („DejaVu Sans“) liefert sie, bevor Systemschriften (nur Lupe) oder Textrückfälle greifen. Symbolknöpfe (`symbol_font`) und reine Symbol-Labels (`icon_font`: Bereichspfeile, Auswahlpfeil, Haken, Blockgriff, Mondphase, Pixel-Kachelköpfe) setzen die Begleitschrift ausdrücklich. In Mischtext – Baumzeilen, Datums- und Labelspalten – ergänzt Tk das Zeichen aus einer registrierten Schrift; unter Linux ist das DejaVu Sans, unter Windows und macOS ist es sichtzuprüfen.
- **B09:** `bundled_glyph_metrics` misst auch Roboto Mono (Pfadtrenner „›“ und Symbolmitte), DejaVu Sans wie bisher.
- **Pakete:** Lizenztext als `RobotoMono-OFL.txt` in den Windows- und macOS-Lizenzbeständen (`lizenzen_vorbereiten_windows.py`, `lizenzen_vorbereiten_macos.py`, `lizenzen/macos/manifest.json`); die Paketstartprobe verlangt „Roboto Mono“ zusätzlich zu DejaVu Sans und Pixelify Sans.
- **Pixelgrund:** `drawing_image.model_to_photo(..., transparent=True)` setzt den unbemalten Grund (Farbindex 0) durchsichtig, mit derselben Rechnung wie der ICO-Export. `page_icon_image` nutzt das für Seitenleiste, Angeheftet und Seitenkopf. Im Farbdialog stehen der karierte Grund („im Symbol durchsichtig“) und „Weiß“ (`OPAQUE_WHITE` = `#FEFEFE`, deckend) vorn. Bestehende Zeichnungen, Palette und Datenformat bleiben unverändert.
- **Python-Lieferung:** `abgleich_07.py` – 91 Code-Dateien und 152 Ressourcen ohne Abweichung. Version bleibt 3.50.0 (noch kein veröffentlichter Release auf GitHub); Quellhash geändert, ältere Paketbelege gelten nicht für diesen Stand.

## Prüfung

Linux/Tk 8.6.14 mit Xft, Python 3.12, künstliche Daten. Baseline auf dem unveränderten Stand `d3fcb80`, derselbe Satz danach ([Ergebnis](ergebnis.json)):

| Prüfung | Baseline | Neu |
|---|---|---|
| Fachlogik (1.114 → 1.118 Tests) | grün | grün (neu: Begleiterregel, Roboto-Mono-Metriken, Titelvorrang Heute) |
| `test_logo3370` Symbole/Logo | grün | erst rot (Pixel-Kachelkopf in Roboto Mono ohne Zeichen), nach `icon_font` grün |
| `test_uiux_paket` | 15 grün, rot b12_b13/b16 | erst zusätzlich rot b09 (Seitenleistensymbole ohne Metrik) und b11 (Heute: Fälligkeit 343 px breiter als Titel 281 px), nach Begleiterschrift und Titelvorrang 15 grün, rot nur b12_b13/b16 |
| `test_mindestgroesse330` | grün | erst Zeitüberschreitung: endlose Layoutschleife im Einstellungsdialog; nach `width=1`-Umbruch grün (75 Ansichten, 56 Dialogaufrufe) |
| `test_release36`, `test_kennzahlen33310`, `test_oberflaeche33321`, `test_arbeitsmodi` (inkl. neuer Prüfung durchsichtiger Grund), `test_glide`, `test_drawing`, `test_drawing330`, `test_pixel3350`, `test_paket3420`, `test_paketierung330` | grün | grün |
| `test_logo330`, `test_features330` | rot (Tk 8.6: Zählerfläche, Zeitgrenze) | unverändert rot, gleiche Ursache |

Die verbliebenen Rotfälle sind Umgebungsgrenzen von Linux/Tk 8.6 und auf GitHub mit eigener Tk 9.1 grün; `test_seitenkarten` braucht die volle Git-Historie (flacher Klon). Aufnahmen aller Ansichten und Dialoge mit Roboto Mono: siehe [Designprüfung](../designpruefung_2026-11-03/README.md).

## Grenzen

- Native Sichtprüfung unter Windows (PC-01) und macOS: Ersatzschrift für Symbole in Mischtext, Schriftbild bei 100/150/200 % DPI.
- Roboto Mono ist rund 10–15 % breiter als DejaVu Sans. Layouts messen, Befund 1 der [Designprüfung](../designpruefung_2026-11-03/README.md) (Titel gegen Metadaten) wird dadurch deutlicher.
- Druck-/HTML-Ausgaben behalten ihre Schriftliste; Codeblöcke behalten die Plattform-Monospace.
- Neue Windows- und Mac-Pakete auf diesem Quellstand stehen aus (GitHub-Lauf nach dem Push, Mac nativ).
