# Suchzeile bis zur rechten Inhaltskante – 3.50.4

Stand 05.11.2026 · Aufgabenformat 26

Erneuter menschlicher Befund: Die Suchzeile nutzt weiterhin nicht die ganze Breite. Das Benutzerbild zeigt im Buch rechts einen leeren Streifen. Die vorherigen Korrekturen betrafen den Buchbaum und den oberen Seitenleistenabstand; der eigene 10-px-Packabstand des Suchfeldrahmens blieb dabei bestehen.

`sync_search_row_spacing` hält die 10 px jetzt ausschließlich vor tatsächlich rechts gepackten Folgeknöpfen. Ohne solche Knöpfe reicht der Feldrahmen bis zur rechten Außenkante der Inhaltskarte. Der Abgleich erfolgt bei Suchanfrage/Löschen und beim Aufbau der Werkzeugzeile nach Ansichts-, Größen- oder Seitenleistenwechseln, einschließlich umgehängter globaler Kopfaktionen. Nur geänderte Packwerte werden gesetzt; keine rekursiven Update-Aufrufe, keine neue Abhängigkeit oder Datenänderung.

- Bestehende Werkzeugleisten-Baseline auf `a536c8d4…` vor Produktionsänderung grün.
- Neuer Pflichtfall `suchbreite3504` auf unveränderter Vorfassung gezielt rot: Suchfeld rechts 856, Inhaltskante 866, Lücke 10 px.
- App `1c48a095…`: 239 Prüfungen gegen die äußere Inhaltskarte grün. Buch/Labels/Liste; leere Suche, Suchanfrage und anschließendes Löschen; Hell/Dunkel/Glas, mittlere/große Schrift, 860/1280 px, volle/schmale/ausgeblendete Seitenleiste und Rückwechsel. Folgeknöpfe vollständig ohne Überdeckung; keine künstliche Test-Synchronisierung des neuen Abgleichs.
- Buchbreite 64/64, Seitenleistenabstand 16/16, `menschen3503`, `werkzeugzeile` und `ansichtssymbole` grün. Syntax und Python-Abgleich: 93 Code-Dateien/171 Ressourcen bytegleich. Neuer Fall gehört zu `--fall alle`, nun 49 Fälle.
- Echte Windows-Aufnahmen mit künstlichen Daten unter `%USERPROFILE%/gq/search4/bilder/`; Hellaufnahme des Buchs visuell kontrolliert. Rohberichte und Eingangsbildhash im [Ergebnis](ergebnis.json).

Menschliche Bestätigung der Suchzeile, des Buchs und des Seitenleistenabstands weiterhin offen. Keine neue strenge Grundstufe oder native Plattformmatrix auf diesem Hash; Windows-/Mac-Neubauten übernimmt der Benutzer heute Abend. Keine Git-/Releaseaktion. Neuer eingefrorener Starter: `%USERPROFILE%/gq/search4/Nachtest_starten.pyw`, eigene stabile Kopie synthetischer Daten; laufende ältere Prüffassungen unverändert.
