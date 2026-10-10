# Logo und Symbole – Liefernachweis 3.37.0

Stand 11.10.2026 · Glide 3.37.0 · Aufgabenformat 23 · Mac vollständig grün, native Matrix ausstehend

Paket 2 setzt D28/D29/D41/D45 vollständig um: Tk-freies geglättetes Raster,
exakte App-PNGs, freigegebene Normal-/Kleinmaster und alle 63 Oberflächenzeichen
aus der tatsächlich verwendeten UI-Schrift. Keine neue Laufzeitbibliothek.
Ausgangslieferung 3.36.0, Liefercommit `efad5df`.

| Tor | Ergebnis |
|---|---|
| Freigegebene Master | vier SVGs bytegleich zu D45 und regulären Laufzeitkopien; [Hashes](master-abgleich.json) |
| Gezielte Pflicht-/Bestandssuite | `test_logo3370` und `test_logo330` grün; [Ergebnis](gezielt.json) |
| Vorversion 3.36.0 | drei getrennte passende rote Gegenproben: fehlendes Rasterlogo, falsche Iconmaße, Ersatzschrift |
| Fachlogik | 276 Unit-Tests grün; zwölf neue Raster-/PNG-/Geometrie-/Symboltests |
| Rastervergleich | 16/32/54/108/256 px gegen natives SVG; Mittelwert Alpha ≤ 8/255, p95 ≤ 32/255; [Rohwerte](qualitaet.json) |
| Rastertempo | acht kalte/warme Wiederholungen, je Höhe; unveränderte Form aus begrenztem Cache, Farbe separat; [Rohwerte](qualitaet.json) |
| Schrift und Größe | normale/fette UI-Schrift, echte Suche, große Schrift, Pixel-Kachelköpfe; ganze Tabelle ohne Ersatzschrift |
| Eigene Fensterbilder | Hell/Dunkel/Pixel und zwei Vergleichstafeln lokal außerhalb OneDrive; vom Agenten betrachtet, keine menschliche Freigabe |
| Erster eingefrorener Mac-Volllauf | 99 Schritte grün, zwei alte fest codierte Symbolerwartungen rot, zwei Schritte übersprungen; 829 Dateien unverändert; [Ergebnis](mac-erster-volllauf.json) |
| Korrigierter eingefrorener Mac-Volllauf | Exit 0, 101 ausgeführt/zwei übersprungen, 84 Suiten/276 Unit-Tests; alle 831 Dateien nach Lauf unverändert; [Ergebnis](mac-voll.json) |
| Strenge lokale CI | bestanden: 17 ausgeführt, ein SSL-Hinweis beim Originalabruf; [Ergebnis](grundstufe-lokal.json) |
| Native Linux-/Windows-Vollprüfung | ausstehend |
| 07 und Showcase | 40 Code-/141 Ressourcen-/sechs Showcase-Dateien SHA-256-gleich; [Abgleich](lieferabgleich.json) |
| Mac-Entwicklungsbundle | 40 Code-/55 Plattformressourcen gleich Quelle; Ad-hoc-Signatur im Bauordner und auf Rückkopie grün; [Bundle](bundle.json) |
| Menschen-/DPI-Abnahme | getrennt offen |

Der zusätzliche Konturvergleich fand einen horizontal gestreckten Rundungsrest:
Der Rasterweg füllte die aufgerundete Pixelbreite statt den vertikalen Maßstab
beizubehalten. Korrigiert; eine 8,5 Pixel breite Fläche bleibt 8,5 Pixel breit.
Der Integrationstest prüft die geometrische Mitte des Innenraums, nicht eine
von der aufgerundeten Bildbreite verschobene Position. Sie ist auch bei 16 px
vollständig transparent. Alle gezielten Tests danach erneut grün.

Normalmaster gelten für alle übrigen Größen; Kleinmaster ausschließlich 16/32 px,
auch im ICO-/ICNS-Bauweg. Die alte Affinity-Datei ist ausdrücklich nicht nachgeführt.
Die übernommenen Entwurfs-SVGs und die überholte Diagnose entfallen; Vergleichstafeln
und Git tragen Freigabe und Vorfassung. Rohprotokolle/Fensterbilder bleiben lokal.

Der Erstlauf scheiterte ausschließlich an den alten Literalen „☷“ und „↯“.
D29 verlangt Zeichen aus der verwendeten UI-Schrift. Die Bestandssuiten prüfen
nun weiterhin exakt den richtigen Symbolschlüssel mit seinem Rückmeldungstext
bzw. Kopfknopf; Unterscheidbarkeit und Schriftabdeckung bleiben verbindlich.
Drei positive Bestandssuiten sind grün; zwei echte falsche Symbolzuordnungen
scheitern genau an der Rückmeldung bzw. am Aktionsknopf. [Kalibrierungsnachweis](testkalibrierung.json). Die vier übernommenen Master-SVGs behalten
bewusst auch die unbedeutende Leerzeile ihrer freigegebenen Bytefassung;
`git diff --check` meldet deshalb vier reine SVG-Leerzeichenhinweise.

Die Entwicklung und der Versionswechsel begannen am 10.10.2026; eingefrorene Mac-Abnahme und Lieferabgleich endeten am 11.10.2026. Native Prüfungen erfolgen anschließend am unveränderten Kandidatcommit. Menschen-/DPI-Prüfungen bleiben eigene Tore.
