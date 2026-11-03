# Korrigierte Schriftklassen und kräftigere Serifenschriften

Prüfdatum 03.11.2026 · Kandidat 3.50.1 · Basis `2f09acba` · Windows x64, Python 3.14.7, Tk 9.1.0.

## Auftrag und Umsetzung

Die korrigierte Reihenfolge entspricht den Originalordnern: Modern: Rubik, Technisch: Roboto Mono, Kreativ: Playfair Display, Klassisch: Fraunces. Beide Serifenschriften verwenden für Lesetext die unveränderten Original-SemiBold-Schnitte (600) statt Regular (400), für Hervorhebungen die bisherigen echten Bold-Schnitte (700). Beide mit passendem Original-Kursivschnitt. Keine Umbenennung oder Bearbeitung von Fontdateien, keine neue Laufzeitabhängigkeit. Rubik bleibt Vorgabe; gespeicherte Familien bleiben bestehen.

Tk kennt normal/bold; SemiBold wird deshalb als mitgelieferte eigene native Familie gewählt. Bold-Aufträge wechseln zur regulären Familie mit echtem 700er-Schnitt. Auf Windows kann Tk bereits SemiBold als `actual weight=bold` melden; Familienname, angeforderte Schrift und tatsächlicher OS/2-Gewichtswert der Originaldatei belegen die Unterscheidung. Glyphenmetriken berücksichtigen SemiBold und SemiBold Italic. Beim Größenwechsel eines Bereichstitels wird dessen Pfeilausrichtung erneut berechnet; vorher war im kleinen Serifentext ein Versatz von gut 2 px messbar.

## Prüfung

- Bestehender Schriftstile-Fall auf dem Basisstand grün.
- Erweiterter Fall `schriftstile`: echte Auswahl aller vier Klassen, Speichern, Anwendung auf Baum-/Hervorhebungsrollen, Neustart; beide Serifenschriften in „klein“ bei 860 × 700 sowie Proben von 8–11 pt, normale/fette/kursive Metriken und Symbole. Ergebnis in [ergebnis.json](ergebnis.json).
- B09/B11 je Playfair und Fraunces in kleiner Schrift grün: Symbolmitten und Spaltengeometrie. Die Datenprobe erhält die Schriftwahl ausdrücklich; ein vollständiger Showcase-Einstellungsimport würde sie überschreiben und wäre keine gültige Schriftgegenprobe.
- Tk-freie Katalogtests und Glyphentests auf tatsächliches Gewicht 600/700, Kursivschnitte und deutsche Zeichen grün. Bestehende Werkzeugzeilenprüfung grün.
- Strenge Grundstufe grün: 19/19 Schritte, 242 Werkzeugtests (ein Skip), zweimal 1.124 Fachtests, Appstart und strenger Liefervergleich. Python-Fassung: 92 Code-Dateien und 171 Ressourcen bytegleich.

Vier Windows-Fensterbilder mit synthetischen Daten für beide Serifenschriften, Hell/Dunkel und kleine Schrift lokal aufgenommen; Agentensichtprüfung erfolgt separat vom menschlichen DPI-/Mehrmonitorvergleich. Rohprotokolle und Bilder bleiben lokal. Native Windows-/Mac-Pakete und neue Remote-Vollmatrix nicht durch diesen Nachweis abgedeckt.
