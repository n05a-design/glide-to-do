# Hinweise bei schmaler Breite und im Kompaktmodus – Glide 3.50.0, 02.11.2026

Nutzerauftrag: Bedienhinweise im Kompaktmodus und bei allen Breiten ab dem Umbruch, an dem das Glide-Logo verschwindet, ausblenden – auch bei Pinnwand, Seiten, Listen und Tabellen – und den Platz dem Inhalt geben. Aufgabe und Abgrenzung im [Plan §21.49](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2149-hinweise-bei-schmaler-breite-und-im-kompaktmodus), Regel in den [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md).

## Umsetzung

- Tk-freie Regel `interaction_policy.hints_visible(settings, narrow=…, compact=…)`: schmal oder kompakt → keine ergänzenden Hinweise, unabhängig vom gespeicherten Schalter. Die App fragt sie über `hints_shown()` ab. „Schmal“ ist dieselbe Kopfstufe „minimal“ (Kopf unter 900 px), bei der `sync_header_logo` das Logo ausblendet.
- Alle bisherigen Hinweisstellen hängen daran: Kartenfuß der Liste, Werkzeugleistenhinweis von Seite/Zeichnung/Galerie, erklärende Untertitel der Ansichten, Gruppierungshinweise von Tabelle und Pinnwand, Bedienwege in Nebenansicht, Heute („Doppelklick öffnet“) und Schnellsuche, Papierkorb-Zusatzsatz, Anpassungshinweis der Startseite.
- Die Tastenzeile von Pinnwand und Reitern erschien bisher unabhängig vom Schalter. Sie weicht jetzt bei schmaler Breite und im Kompaktmodus (`hints_room()`); ohne Text nimmt sie keine Zeile ein. Die Auswahlzahl („2 Karten ausgewählt“) bleibt als Zustand sichtbar.
- `sync_hint_space` gleicht die offene Ansicht beim Wechsel der Kopfstufe und beim Ein-/Ausschalten des Kompaktmodus neu ab. In der Tagesansicht wird nur der Text der Verweiszeile angepasst, kein Baumneuaufbau (ein erster Entwurf packte unter 900 px die Liste über das Tagesraster; `test_features330` fand das).
- Gespeicherter Schalter, Format 26 und Einstellungen 2 unverändert.

## Prüfbelege

macOS arm64, Python 3.14.5, eigene Tk 9.1, synthetische Daten mit temporärem `GLIDE_DATA_DIR` vor dem Import.

- Unit-Test `test_interaction_policy` (neuer Fall „schmal oder kompakt“, Schalter bleibt unverändert).
- Neuer Fall `test_arbeitsmodi --fall hinweisplatz`: Liste, Tabelle, Pinnwand und Seite mit eingeschalteten Hinweisen – bei 1280 px vorhanden, bei 860 px (Logo weg) in allen vier keine, Kartenfuß ausgepackt; Auswahlzahl der Pinnwand bleibt, ohne Auswahl keine leere Zeile; zurück bei 1280 px wieder vorhanden; im Kompaktmodus keine, danach wieder vorhanden. Gegen die vorherige Python-Fassung gezielt rot (Kartenfußhinweis bei 860 px).
- Angepasste Erwartungen: `test_uiux_paket` b06_b15 (Papierkorb-Zusatzsatz nur bei voller Breite), `test_kartenfuss330` (schmal kein Fuß ohne Auswahl, Leiste bei Auswahl), `test_bedienung33316` (Schalterprobe bei 1280 px).
- [Sichtprobe](sichtprobe.py) mit [Ergebnis](sichtprobe.json) und Fensterbildern unter `fensterbilder/`: Pinnwand bei 860 px vorher mit, nachher ohne Tastenzeile (Fläche entsprechend höher); Liste bei 860 px mit eingeschalteten Hinweisen vorher mit, nachher ohne Kartenfußhinweis. Bei 1280 px unverändert.
- [Endstand und Suiten](ergebnis.json).

## Lieferung und Grenzen

Python-Fassung bytegleich abgeglichen. Eigenständige Mac-App mit eigener Tk 9.1 neu gebaut und installiert; Belege und Vorfassung im [Abschluss](ergebnis.json). Windows-EXE bleibt beim ursprünglichen 3.50-Stand; kein neuer öffentlicher Release, kein vollständiger Matrixlauf. Menschliche Sichtprüfung in der [manuellen Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) ergänzt.
