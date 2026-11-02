# Werkzeugzeile, Pinnwandgrund, Ansichtssymbole und Seitenfuß – Glide 3.50.0, 02.11.2026

Nutzeraufträge: Abstände appweit prüfen, weil die Zeile zum Eingeben und Suchen zu nah an der Hauptansicht steht (auch bei der Pinnwand); die Pinnwand wie Liste und Tabelle ohne Fensterhintergrund darstellen; die drei Ansichtssymbole rechts, neue Knöpfe links davon; „Erwähnt ohne Verweis“ und den Hinweis zum Speicherstand in eine Zeile. Aufgabe und Abgrenzung im [Plan §21.50](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2150-werkzeugzeile-pinnwandgrund-und-ansichtssymbole), Regel in den [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md).

## Umsetzung

- `CONTENT_TOOLBAR_GAP` = 10 px oberhalb der Inhaltskarte für alle Ansichten mit Karte (Liste, Ordner, Tabelle, Pinnwand, Heute, Seite, Notiz …). Gemessen: Suchfeld → Karte vorher 1 px, nachher 11 px; Seitenwerkzeuge → Karte vorher 0 px, nachher 10 px.
- Pinnwandfläche, Bereichsflächen und Punktraster auf der Kartenfarbe statt dem Fensterhintergrund; Rand nur mit Tastaturfokus. Karten heben sich weiterhin über ihre Kontur ab.
- `pin_view_switch_right`: Der Umschalter ☷/⊞/▨ steht an der ersten Packstelle der Suchzeile und damit rechts außen; „≡ Anzeige“, „Spalten“, Tagebuchfilter und künftige Knöpfe stehen links davon. Vorher lag in Liste und Tabelle ein Knopf rechts davon.
- Seitenfuß `_foot_row`: „Erwähnt ohne Verweis …“ links, Statusmeldung (Speicherstand, Schreibschutz, Fundstellen) in derselben Zeile rechts daneben; aufgeklappte Fundstellen öffnen sich über der Fußzeile.
- Die Inhaltskante liegt bei 1280 × 800 bei 128 px (16 %). Die 15-%-Prüfung aus 3.38.0 (`test_aufgaben3380`, Fall Fläche) gilt seitdem zuzüglich des ausdrücklich verlangten Abstands (120 + 10 px).

## Prüfbelege

macOS arm64, Python 3.14.5, eigene Tk 9.1, synthetische Daten mit temporärem `GLIDE_DATA_DIR` vor dem Import.

- Neuer Fall `test_arbeitsmodi --fall werkzeugzeile`: Hell/Dunkel × 1280/860 px über Liste, Tabelle und Pinnwand – Abstand ≥ 10 px, Umschalter bündig rechts außen, kein Knopf rechts davon, Pinnwand auf Kartenfarbe; Seite mit Abstand zur Werkzeugleiste; Spaltenknopf links vom Umschalter; Seitenfuß einzeilig, Fundstellen darüber.
- [Messung vorher](messung-vorher.json) / [nachher](messung-nachher.json) mit [Sichtprobe](sichtprobe.py) und [Seitenfußprobe](sichtprobe_seitenfuss.py); Fensterbilder unter `fensterbilder/` (dunkles Design mit eigener Hintergrundfarbe).
- Angepasste Erwartungen: `test_workspace310` (Pinnwand auf Kartenfarbe), `test_aufgaben3380` (15 % plus Abstand).
- `test_ui39` (Dropdown-Fokus) scheiterte lokal zeitweise, mit derselben Häufigkeit auch an der vorherigen Fassung (1 von 3); unabhängig von dieser Änderung.
- [Endstand und Suiten](ergebnis.json).

## Lieferung und Grenzen

Python-Fassung bytegleich abgeglichen. Eigenständige Mac-App mit eigener Tk 9.1 neu gebaut und installiert; Belege und Vorfassung im [Abschluss](ergebnis.json). Windows-EXE bleibt beim ursprünglichen 3.50-Stand; kein neuer öffentlicher Release, kein vollständiger Matrixlauf. Menschliche Sichtprüfung in der [manuellen Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) ergänzt.
