# Arbeitsbegleiter und Markenfigur – Konzept und Formatentscheidung

Stand 16.10.2026 · Glide 3.43.1 · gezeichnete Figur vorhanden; B03 im Quellstand; neue Bildassets offen

Fortgeschriebene Gestaltungsidee aus den Aufträgen vom 18./19.09.2026. Am 15.10.2026 wurden die doppelten Asset-Lieferlisten und die überholten Tk-8.6-/Ein-Datei-Einbauprompts zusammengeführt. Vorfassungen trägt Git. Die Bereinigung ändert keine App-Funktion und beauftragt keine neuen Assets.

## Implementierter Stand und neuer Auftrag

Gismo ist eine gezeichnete Figur (`MascotCanvas`) in der Startseitenkachel. Seit 3.26.0 bestehen kontextbezogene Sprechblasen, Füttern und Hover-Reaktionen; persönlicher Name und separat gespeicherte Spielereien gab es bis 3.42.0 (seit B03 entfallen). Seit 3.30.0 erscheint Gismo außerdem still neben der Hauptaktion leerer Listen, Ordner, Notizbücher, Suchergebnisse, Papierkörbe und Pinnwände: 56 px, Zustand `ruhig`, ohne Sprechblase, Blinzeln oder Führung. In der aktuellen App blendet „Spielereien aus“ diese Auftritte aus. Verhalten und Einstiege stehen in [Funktionen, Startseite](../20_FUNKTIONEN.md#7-startseite).

**Vorgabe vom 15.10.2026 (B03), mit 3.43.0 geliefert:** Gismo heißt fest „Gismo“ und behält seine spielerischen Funktionen (Füttern, Spielen, Ruhen, Reaktionen), solange seine Startseitenkachel sichtbar ist. Umbenennung und separater Spielereien-Schalter entfallen; frühere Werte (`mascot_name`, `mascot_playful`) werden beim Laden entfernt (`home_tiles.retire_mascot_settings`). Wer ihn nicht möchte, blendet die Kachel aus – dann erscheint er auch nicht neben Leerzuständen. Die barrierefreie Bewegungsreduktion nimmt nur die Bewegung, nicht die Funktionen. Regeln und Belege: [Design Richtlinien](../DESIGN_RICHTLINIEN.md), Status im Entwicklungsplan §17.

## Rolle und Grenzen

Markenfigur und Arbeitsbegleiter können dieselbe Figur sein, bleiben aber unterschiedliche Aufgaben: Wiedererkennung im Projektauftritt gegenüber optionalen Reaktionen im Arbeitsablauf. Die Figur verdeckt keine Aktion und ist nie der einzige Informationsträger. Ihr Zustand spiegelt den Bestand, nicht die Bewertung eines Menschen.

- Keine ungefragte Unterbrechung beim Arbeiten, kein Fokusdiebstahl und keine Anzeige über offenen Dialogen.
- Informationen bleiben ohne Figur auffindbar; keine Produktivitätsbewertung aus Klicks oder Abschlüssen.
- Leerzustände werden durch Text und Hauptaktion erklärt; die Figur ergänzt sie.
- Führendes Endnutzer-Onboarding und Hinweise auf ungenutzte Funktionen sind nicht gewählt. Die alten Konzeptvorschläge dafür sind keine aktiven Aufträge.
- Eine eigene KI-Anbindung ist keine offene Gestaltungsoption dieses Dokuments; es gelten Q3 und die aktuellen [Produktgrenzen](../01_PRODUCT_CONSTRAINTS.md).

## Technische Grundlage

Glide verwendet Python 3.14/Tk 9 mit einem eingeschränkten Tk-8.6-Rückfall. Tk 9 kann SVG nativ anzeigen; die frühere pauschale Aussage, Tk könne keine SVG-Dateien darstellen, ist überholt. PNG bleibt für vorbereitete Bildfolgen und den Tk-8.6-Rückfall geeignet. Details zur Bildunterstützung und zum geglätteten Logo-Rückfall stehen in [Architektur](../02_ARCHITECTURE.md) und [Funktionen](../20_FUNKTIONEN.md).

Neue Bildassets dürfen keine zusätzliche Laufzeitbibliothek erfordern. Die vorhandene gezeichnete Figur bleibt der funktionsfähige Rückfall, solange kein ausgewählter und geprüfter Ersatz vorliegt. Die App ist kein einzelnes Skript mehr: `app.pyw` koordiniert Module; neue Fachlogik folgt D17.

## Zusammengeführte Assetoption für eine spätere Gestaltungsrunde

Diese Lieferoption beschreibt einen möglichen Ersatz der Zeichenbefehle, keine schon gelieferten oder zusätzlich beauftragten Dateien. Ein passender Vektor-/bearbeitbarer Master bleibt die Quelle. Transparente PNGs können feste Ausgabegrößen und Bewegungsbilder liefern; Tk-9-SVG-Nutzung und Rückfall werden bei tatsächlicher Umsetzung gemeinsam geprüft.

| Ausgabegröße | Möglicher Zweck |
|---|---|
| 64 × 64 | Zeile oder Kachelecke |
| 96 × 96 | Startseitenkachel |
| 128 × 128 | größerer Leerzustand |
| 192 × 192 | HiDPI der 96er-Ausgabe |
| 256 × 256 | HiDPI der 128er-Ausgabe |

Mögliche Zustandsfamilie: `ruhig`, `winkt`, `zeigt`, `freut`, `schlaeft`. Das ist eine Gestaltungsskizze und keine Aussage über exakt so benannte aktuelle App-Zustände. Eine ausgewählte Familie verwendet dieselbe Figur, Haltungssprache und Silhouette; Unterschiede bleiben auch klein erkennbar.

Technische Ausgabeoptionen:

- `begleiter_<zustand>_<groesse>.png`, transparent, mindestens zwei Pixel Luft an jeder Kante; keine unnötigen eingebetteten Profile. Auf allen Designs einschließlich farbloser Flächen lesbar.
- Bewegung bei Bedarf als vier bis sechs PNG-Einzelbilder, `begleiter_<zustand>_<groesse>_<n>.png`; Zeitsteuerung über abbrechbare `after`-Aufträge. Animiertes GIF ist dafür kein notwendiges Lieferformat.
- Keine 3D-/Video-/Schriftdatei als neue Laufzeitvoraussetzung; ein 3D-Programm darf eine Gestaltungsquelle sein.
- `PhotoImage`-Referenzen halten, fehlende Assets abfangen, keine hässliche ungefilterte Skalierung. Die bestehenden Schnittstellen und die globale Bewegungsreduktion bewahren, statt einen historischen Beispielprompt ungeprüft einzubauen.

## Was offen bleibt

Ein neuer bildbasierter Entwurf, seine endgültige Zustandsfamilie, konkrete Dateigrößen und Übernahme sind nicht ausgewählt. Der Name Gismo ist durch die neue B03-Vorgabe festgelegt; offene Marken-/Veröffentlichungsfragen bleiben im [Produktregister](PRODUCT_IDENTITY.md) und [Veröffentlichungsrahmen](../10_VEROEFFENTLICHUNG.md). Die neue UI-/UX-Ausführung soll keine zusätzliche Assetproduktion aus diesem Konzept ableiten.
