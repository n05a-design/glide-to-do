# Labels in der Kartenecke – Glide 3.50.0, 02.11.2026

Nutzerauftrag: Labels („Tags“) wie im Bildbeispiel des grünen „Text“-Chips bei Seite, Liste und Ordner oben rechts innerhalb des Fensters im Eck integrieren. [Plan §21.48](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2148-labels-in-der-kartenecke), Regel in den [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md).

## Umsetzung

- Chips stehen per `place` oben rechts in der Inhaltskarte, 12 px von der rechten und 8 px von der oberen Innenkante; eine Zeile bis 240 px, Rest als „+n“. Vorher standen sie in der Unterzeile des Kopfes unter den Kopfknöpfen.
- Liste, Ordner, Tabelle, Pinnwand und Notiz: oben ein Freiraum (8 px + Chiphöhe + 6 px), nur wenn Labels zugewiesen sind. Ohne Labels bleibt alles wie bisher.
- Seite: keine zusätzliche Zeile. Der Titel erhält rechts einen Einzug und endet 12 px vor den Chips; Kopfverweise am Titelende bleiben links davon. Ist der Titel in einem sehr niedrigen Fenster ausgeblendet, weichen auch die Chips.
- Nebenbefund: Der Titelumbruch wurde nur bei geändertem Rand neu gesetzt und folgte in voller Lesebreite und in schmalen Fenstern einer Größenänderung nicht. Jetzt wird er bei jeder Breite nachgeführt.
- Die feste Kopfhöhe reserviert nur noch eine Textzeile statt der früheren Chipreserve von 4 px. Dadurch endet das Logo wieder auf der Grundlinie der Unterzeile (B05), und die Inhaltskante liegt bei 1280 × 800 wieder bei höchstens 120 px (15-%-Regel), die nach dem Abstandsnachlauf §21.45 überschritten war (125 px in der Python-Fassung vor diesem Nachlauf).

Format 26, Einstellungen 2, Version und Abhängigkeiten unverändert.

## Prüfbelege

Alle Läufe macOS arm64, Python 3.14.5, eigene Tk 9.1, synthetische Daten mit temporärem `GLIDE_DATA_DIR` vor dem Import.

- Neuer Fall `test_arbeitsmodi --fall eckenlabels`: Liste, Tabelle, Pinnwand und Ordner bei 1280/860 px – Chips rechts oben mit festen Abständen, keine Überdeckung von erster Zeile oder Pinnwandleiste, Kopfhöhe unverändert; Seite in schmaler und voller Lesebreite – kein Freiraum, Titel 12 px vor den Chips, Umbruch folgt der Titelbreite; Kopfverweise ohne Überdeckung; Labels lösen entfernt Ecke und Reserve. Labels werden über den echten Zuweisungsweg `toggle_page_label` gesetzt.
- Kopfvertrag U10 in `test_glide` auf die Kartenecke umgestellt (Ort, Abstände, Freiraum an erster Packstelle, Kopfhöhe beim Labelwechsel gleich).
- [Geometrieprobe](geometrie.json) mit [Sichtprobe](sichtprobe.py): 32 Messungen in Hell/Dunkel × 1280/860 px über Liste, Tabelle, Pinnwand, Ordner, Liste ohne Labels und Seite (schmal/voll), 0 Überdeckungen, 0 Rückruffehler. Fensterbilder unter `fensterbilder/`.
- Endstand `app.pyw` `1e3f933b…`: 16 betroffene Integrationssuiten grün – `test_glide`, `test_titel33312`, `test_aufgaben3380` (einschließlich Fläche 15 %), `test_uiux_paket` (17 Fälle einschließlich B05 und 1.120 Knopfprüfungen B15), `test_arbeitsmodi` (alle Fälle), `test_features322`, `test_oberflaeche33321`, `test_seitenkarten`, `test_ansichten`, `test_seiten330`, `test_seiten33318`, `test_festlayout330`, `test_kartenfuss330`, `test_notizbereich330`, `test_pixel3350`, `test_wiederanlauf`. Ein erster Durchlauf während laufender Korrekturen zeigte B05 und Fläche rot; beide nach der Kopfhöhenkorrektur grün.
- [CI-Grundstufe](grundstufe.json).

## Lieferung und Grenzen

Python-Fassung bytegleich abgeglichen (91 Code-/147 Ressourcendateien). Eigenständige Mac-App mit eigener Tk 9.1 gebaut ([Bau](mac_bau.json), [Start des Baus](mac_start_bau.json)), installiert als `~/Applications/Glide.app`; Vorfassung unter `~/Applications/Glide-vor-Eckenlabels-20261102.app` erhalten. 463 installierte Paketdateien gegen das Bauinventar und Ad-hoc-Signatur geprüft ([Lieferabgleich](mac_lieferung.json)), isolierter Start der installierten App ohne externes Python grün ([Start](mac_start_lieferung.json)). Die Startprobe der installierten App war zuvor dreimal an ihrer Checkbox-Fokusprüfung rot (einmal parallel zu Tk-Suiten, zweimal einzeln direkt nach der Installation), danach fünfmal grün; Bauordner und Vorfassung durchgehend grün. Eine Ursache in dieser Änderung ist nicht belegt; die Prüfung hängt am Fensterfokus des Betriebssystems ([Abschluss](ergebnis.json)).

Windows-EXE bleibt beim ursprünglichen 3.50-Stand; kein neuer öffentlicher Release, kein vollständiger Matrixlauf. Menschliche Sichtprüfung in der [manuellen Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) ergänzt; Reader nach D58 zurückgestellt.
