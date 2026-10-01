# Glasoberfläche und Materialgestaltung für Glide 3.6.0

Stand: 06.09.2026 · Technische Prüfung und umgesetzte Gestaltung für Python/Tk

## Ergebnis für Glide

Die gewünschte Richtung ist sinnvoll: Navigation mit räumlicher Tiefe, ein ruhiger
solider Arbeitsbereich, scharf lesbare Schrift und sparsame farbige Akzente.
Glide 3.6 setzt davon eine abschaltbare **Materialoptik aus Farben und Glaskanten**
um. Ein echter weichgezeichneter Desktop hinter der linken Tk-Seitenleiste ist
damit **nicht** umgesetzt oder nachgewiesen.

Der optionale Windows-DWM-Aufruf fordert ein Systemmaterial an. Selbst ein
erfolgreicher Aufruf macht die darüberliegenden, deckend zeichnenden Tk-Frames
und Treeviews nicht transparent. Diese Unterscheidung ist wesentlich: Die
Windows-Bilder belegen die aktuelle Gestaltung, keinen funktionierenden
Desktop-Blur.

## Bezug zum gezeigten ChatGPT-Fenster

Der Screenshot zeigt visuell eine dunklere Inhaltsebene und eine anders getönte
Navigationsfläche. Aus einem statischen Bild lässt sich nicht feststellen, ob
dahinter ein Live-Blur, ein getöntes Systemmaterial oder eine feste Farbe liegt.
Der interne Darstellungsweg dieser konkreten ChatGPT-Version wird daher nicht
behauptet. Übernommen wird die sichtbare Hierarchie.

Mit „Liquid OS“ ist hier als Arbeitsannahme Apples Liquid-Glass-Materialsprache
gemeint. Diese Bezeichnung ist keine Aussage über das Betriebssystem des
Screenshots.

## Materialien sauber unterscheiden

| Begriff | Eigenschaft | Konsequenz für Glide |
|---|---|---|
| Solide Fläche | Deckende Farbe, Hintergrund bleibt unsichtbar | Für lange Aufgabenlisten und Texte am verlässlichsten. |
| Alpha-Transparenz | Mischt Vorder- und Hintergrund, ohne zwingend zu verwischen | Ganze Fenster transparent zu schalten würde auch Schrift schwächen. |
| Frosted Glass / Blur | Hintergrund wird weichgezeichnet, mit Tönung überlagert | Benötigt eine passende Render- bzw. Kompositionsebene. |
| Mica | Von Thema und Hintergrundbild beeinflusstes, opakes Windows-Material | Kein Synonym für Live-Blur anderer geöffneter Fenster. |
| Desktop Acrylic | Halbtransparentes Windows-Material mit Milchglasanmutung | Besonders für vorübergehende Bedienflächen vorgesehen. |
| Liquid Glass | Apples native Materialsprache für eine hervorgehobene Bedienebene | Nicht als Tk-Farbwert oder einzelne CSS-Eigenschaft verfügbar. |

Microsoft beschreibt Mica als Grundlage für App-Fenster und Acrylic für
vorübergehende Oberflächen. Die aktuelle WinUI-Dokumentation bietet außerdem
`SystemBackdropElement` für begrenzte Bereiche ab Windows App SDK 2.0.
Diese APIs gehören zu XAML/WinUI, nicht zu ttk.Treeview.
Quelle: [Microsoft System Backdrops](https://learn.microsoft.com/en-us/windows/apps/develop/ui/system-backdrops).

Apple beschreibt Material als Teil einer Hierarchie von Inhalt und Bedienung.
Für Glide folgt daraus die gestalterische Entscheidung, Effekte auf die
Orientierung zu konzentrieren und Arbeitsinhalte ruhig zu halten.
Quellen: [Apple Materials](https://developer.apple.com/design/human-interface-guidelines/materials),
[Apple Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass).
Das ist eine Übertragung auf Glide, keine native Apple-Implementierung.

## Warum der bisherige Tk-Aufbau eine Grenze setzt

Glide verwendet ein Tk-Hauptfenster, deckende Frames, selbst gezeichnete
Canvas-Elemente und native ttk.Treeviews. Ein Canvas kann Linien, Flächen,
Rundungen und Verläufe zeichnen. Ein solches Hintergrundbild wird jedoch durch
ein darüberliegendes deckendes Treeview übermalt. Ein Blur hinter dem Canvas
löst deshalb die eigentliche Kompositionsfrage nicht.

Tk bietet `wm attributes -alpha` für das Toplevel-Fenster. Es ist kein
regionenbezogener Hintergrundfilter für eine scharfe Seitenleiste.
Quelle: [Tk wm](https://web.tcl.tk/man/tcl9.1/TkCmd/wm.html).

Ein ausgeschnittener Screenshot des Desktops wäre nur eine Momentaufnahme. Er
müsste beim Verschieben, Skalieren, Scrollen und bei anderen Fenstern aktualisiert
werden. Neben Rechenlast entstehen Rückkopplungen, falsche Bildausschnitte und
eine zusätzliche Aufnahme anderer Fenster. Glide verwendet diesen Ansatz nicht.

## Tatsächlich umgesetzte Ebene

- `active_theme()` liefert getönte, weiterhin deckende Flächen.
- `RoundedContainer` zeichnet eine zurückhaltende Licht- und Schattenkante.
- Aufgabeninhalt, Eingaben, Menüs und Dialoge behalten eine lesbare Grundfläche.
- Die Startseitenaktionen besitzen sichtbare Konturen in ihrer Aktionsfarbe.
- **Einstellungen → Materialoptik mit Glaskanten verwenden** schaltet die
  Gestaltung aus oder an. Die Einstellung liegt in `settings.json` im
  ausgewählten Datenordner und kann daher durch dessen Synchronisierung
  mitwandern; sie ist nicht grundsätzlich gerätelokal.
- Die Windows-Chrome-Anpassung versucht das DWM-Systemmaterial optional.
  Fehler der Plattform führen zur normalen Tk-Darstellung.

Im Aufgabenformat wird nichts geändert. Der Schalter ist standardmäßig an.
Native Dateidialoge folgen weiterhin Windows bzw. dem jeweiligen Betriebssystem.

## Vergleich der möglichen technischen Wege

| Weg | Echte Unschärfe links | Aufwand und Pflege | Empfehlung |
|---|---|---|---|
| Bestehendes Tk mit Materialfarben/Kanten | Nein | Kleine lokale Änderung, keine neue Laufzeitbibliothek | In 3.6 umgesetzt und geprüft. |
| Tk plus globales Fenster-Alpha | Kein selektiver Blur | Einfacher Aufruf, aber auch Text durchsichtig | Für die geforderte Darstellung ungeeignet. |
| Tk plus DWM-Aufruf allein | Hinter deckenden Widgets nicht sichtbar | Plattformabhängig, nur Fensterhintergrund | Nur optionaler Zusatz, kein Leistungsversprechen. |
| Mehrere transparente native Hilfsfenster | Potenziell | Fokus, Z-Reihenfolge, DPI, Resize, Eingabe und Screenshots werden aufwendig | Kein verlässlicher kleiner Patch. |
| WinUI 3 mit eigenem Navigationsbereich | Ja, mit unterstützter Komposition | Neuer UI-Aufbau, Windows-Paketierung, Controls und Accessibility | Sauberer Kandidat für echten Windows-Blur. |
| AppKit/SwiftUI auf macOS | Native Materialien | Eigene macOS-Oberfläche und separate Geräteprüfung | Für einen nativen Mac-Zweig plausibel. |
| WebView mit HTML/CSS | Blur von Webinhalt innerhalb der WebView | UI-Neubau, Brücke zum Python-Datenmodell, Paketierung | Desktop-Blur zusätzlich vom Host abhängig. |
| Qt/QML mit eigener Komposition | Blur innerhalb der Szene möglich | Neue Abhängigkeit, Lizenz-/Buildentscheidung, neuer Baum und Drag & Drop | Plattformübergreifender Neubau, kein 3.6-Nachtrag. |

Die Einordnung von Aufwand ist eine Architekturbeurteilung des aktuellen
Glide-Codes. Es wurde kein Portierungsprototyp in allen genannten Frameworks
gebaut und kein Aufwand in Personentagen gemessen.

## Konkrete Gestaltung für eine spätere echte Glasebene

Die linke Navigation sollte ein zusammenhängendes Materialband erhalten.
Text, Icons und Zähler bleiben scharf darüber. Die Arbeitsfläche bleibt ein
solides Dunkelgrau, im Hellmodus eine ruhige helle Fläche. Zwischen beiden
Bereichen genügt eine feine Kontur. Glas auf jeder Aufgabenzeile würde den
Informationsvergleich erschweren und ist für diese Richtung nicht nötig.

Farben müssen Hierarchie und Zustand transportieren: eine klare Akzentfarbe
für Auswahl und Hauptaktion, bestehende Label-/Listenfarben für Zuordnung,
zurückhaltende neutrale Flächen für den Rest. Eine stärkere postmoderne Anmutung
kann durch asymmetrische Gewichtung, typografische Kontraste und sparsame
Materialwechsel entstehen. Das ist eine Designempfehlung; sie erfordert keine
ständig bewegten Lichter oder Verzerrung von Text.

## Zugänglichkeit und Bedienung

Material darf die Textlesbarkeit nicht vom zufälligen Hintergrund abhängig
machen. Vor einer nativen Freigabe sind hoher Kontrast, reduzierte Transparenz,
inaktives Fenster, Remote Desktop, hohe Skalierung und Tastaturfokus zu prüfen.
Die aktuelle Tk-Variante besitzt den manuellen Ausschalter. Ein vollständiges
automatisches Nachführen aller Windows-Accessibility-Einstellungen ist damit
nicht belegt.

Farbe bleibt durch Text, Symbole oder Zahlen ergänzt. Native Treeview-Auswahl
bleibt rechteckig, wie nach der ursprünglichen Rückfrage akzeptiert. Runde
Auswahl wurde an selbst gezeichneten Labels und Kalendertagen umgesetzt.

## Leistung und Verifikation

Die aktuelle Materialoptik benötigt keine dauernden Desktopaufnahmen und keinen
Blur pro Bild. Der [Leistungsbericht](21_LEISTUNGSBERICHT_3.6.0.md) vergleicht
denselben Tk-Listenaufbau mit ein- und ausgeschalteter Materialoptik. Der Versuch
ergab keinen erkennbaren zusätzlichen Engpass, erlaubt aber keinen Vergleich
mit echtem Acrylic oder Liquid Glass.

Zur Sichtprüfung gehören Startseite Hell/Dunkel, Scrollende mit Jahresraster,
Vorlagen, Einstellungen oben/unten und neue Liste. Für den Nachweis echten
Desktop-Blurs müsste zusätzlich ein bewegter Hintergrund sichtbar durch die
linke Navigation wirken, während Schrift und Arbeitsbereich unverändert bleiben.
Diesen Nachweis erbringt 3.6 nicht.

## Entscheidung

Glide 3.6 liefert die vorhandene lokale Tk-Anwendung mit vollständigen Funktionen,
mitgelieferten Schriften und optionaler Materialoptik aus. Echte selektive
Desktop-Unschärfe wäre eine eigene UI-Architekturarbeit. Sie ist hier umfassend
bewertet und klar abgegrenzt, nicht als erledigter Effekt etikettiert.
