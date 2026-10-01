# Glasoberfläche und moderne Materialanmutung in Glide 3.6.0

Stand: 06.09.2026 · Design- und Technikprüfung für Tkinter/Windows

## Was „Liquid Glass“ technisch bedeutet

Die aktuelle Materialsprache von Apple trennt eine funktionale Schicht für
Navigation und Bedienelemente von der Inhaltsschicht. Liquid Glass ist dort für
Sidebar, Tabbar, Popover und ähnliche Bedienelemente gedacht; die eigentliche
Inhaltsschicht bleibt ruhig und wird nicht flächendeckend mit Glas überzogen.
Die Variante „regular“ erhöht bei komplexen Hintergründen die Lesbarkeit durch
Unschärfe und angepasste Helligkeit, „clear“ lässt einen bildreichen Hintergrund
stärker durchscheinen. Farbe wird sparsam auf wichtige Aktionen gelegt.

Windows 11 bietet mit Mica ein gedämpftes, wallpaperbezogenes Material für die
Grundfläche und mit Desktop Acrylic ein tatsächlich weichgezeichnetes,
halbtransparentes Material für vorübergehende Flächen. Windows empfiehlt Mica
für die App-Grundfläche und Acrylic für Flyouts und Kontextmenüs. Beide
Materialien fallen bei deaktivierter Transparenz, hoher Kontrasteinstellung,
Remote Desktop oder nicht ausreichender Grafikleistung auf eine solide Farbe
zurück.

Quellen: [Apple Materials / Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials),
[Apple Adopting Liquid Glass](https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass),
[Windows System Backdrops](https://learn.microsoft.com/en-us/windows/apps/develop/ui/system-backdrops),
[Windows Materials overview](https://learn.microsoft.com/en-us/windows/apps/develop/ui/materials),
[DWM window attributes](https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmwindowattribute).

## Was in Tkinter möglich ist

Tkinter besitzt keine native, pro Frame weichgezeichnete Materialebene. Eine
Canvas kann Farben, Rundungen, Konturen und Schatten zeichnen, aber den bereits
gerenderten Desktop oder den Inhalt eines anderen Widgets nicht wie ein
Compositor verwischen. Eine globale `-alpha`-Einstellung würde das ganze
Fenster einschließlich Text und Eingabefeldern durchsichtig machen und wäre
deshalb keine belastbare Glasoberfläche.

Glide verwendet daher drei abgestufte Ebenen:

1. **Materialfarben:** `active_theme()` mischt ruhige Blau-/Grautöne für
   Grund-, Karten- und Eingabeflächen. Der Kontrast der Text-, Status- und
   Akzentfarben bleibt erhalten.
2. **Glaskanten:** `RoundedContainer` zeichnet bei aktivem Glasmodus eine
   zurückhaltende Schattenkante und eine helle Innenkante. Dadurch erscheinen
   Seitenleiste, Startseitenkacheln und Eingabeflächen als voneinander getrennte
   Schichten, ohne eine neue Laufzeitabhängigkeit einzuführen.
3. **Betriebssystemmaterial:** Unter Windows setzt Glide, wenn die DWM-API
   verfügbar ist, `DWMWA_SYSTEMBACKDROP_TYPE` auf das Mica-Material. Der Aufruf
   ist best effort; ältere Windows-Versionen und Systeme ohne Kompositor bleiben
   bei der lesbaren Tk-Farbvariante.

Die Inhaltsebene der Aufgabenliste bleibt dunkel beziehungsweise ruhig, während
die Navigation und die Karten Tiefe erhalten. Das entspricht der von Apple
beschriebenen Hierarchie: Material lenkt die Aufmerksamkeit auf Navigation und
Aktionen, es ersetzt nicht den Inhalt.

## Bedienung und Fallback

Der Schalter **Einstellungen → Glasflächen und weiche Hintergrundmaterialien**
steht standardmäßig auf „an“. Er kann für schwache Grafik, hohe Kontraste oder
eine vollständig flache Darstellung ausgeschaltet werden. Die Einstellung ist
gerätelokal und wird additiv in `settings.json` gespeichert; Datenformat 11 der
Aufgaben bleibt unverändert.

Wenn Windows den System-Backdrop nicht akzeptiert, wenn Transparenz in den
Systemeinstellungen ausgeschaltet ist oder wenn Glide unter macOS/Linux läuft,
bleibt die Materialanmutung aus Farben, Kanten und Rundungen bestehen. Es gibt
keinen leeren oder unlesbaren Zwischenzustand. Kontextmenüs und Dialoge werden
weiterhin als eigene thematisierte Flächen gezeichnet; ein echtes Desktop-
Acrylic-Flyout gehört zu einer späteren WinUI- oder WebView-Schicht.

## Leistungs- und Zugänglichkeitsentscheidung

Die Tk-Variante berechnet keine Screenshots, keine Vollfenster-Blur-Masken und
keine Animation pro Bild. Beim Themenwechsel werden nur Farben, Konturen und
bereits vorhandene Canvas-Flächen neu gezeichnet. Das hält Start, Scrollen und
den Datenpfad lokal und vorhersehbar. Große Bestände werden dadurch nicht mit
einem zusätzlichen Bildspeicher belastet.

Farbe bleibt ein Zusatzsignal: Aufgabenart, Labels, Fälligkeiten und Erledigt-
Status tragen weiterhin Text, Symbole oder Zahlen. Wer Transparenz abschaltet,
erhält dieselben Informationen in soliden Flächen. Die runden Auswahlbalken im
nativen `ttk.Treeview` bleiben eine bekannte Grenze; dafür wäre ein eigener
Canvas-Aufgabenbaum mit neuem Drag-and-Drop-, Tastatur- und Scrollverhalten
nötig.

## Ausbaustufe für einen echten System-Blur

Ein späterer Windows-only-Port könnte den Shell-Bereich in WinUI 3 hosten und
`MicaBackdrop` für die Grundfläche sowie `DesktopAcrylicBackdrop` für
transiente Oberflächen verwenden. Das wäre ein UI-Frameworkwechsel mit neuer
Paketierung, DPI-/Accessibility-Matrix und zusätzlicher Plattformpflege. Für
Glide 3.6 bleibt die portable Tkinter-Lösung deshalb die belastbare
Auslieferungsform; der native DWM-Aufruf ist eine optionale Verbesserung und
kein Laufzeitvoraussetzung.
