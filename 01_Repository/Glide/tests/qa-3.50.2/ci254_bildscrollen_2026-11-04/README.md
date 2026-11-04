# CI #254: zuverlässiger Bildscrolltest B16

Stand 04.11.2026 · Glide 3.50.2 · Aufgabenformat 26

Nach Merge von PR #61 ist `main` `314b0a38`; sein Git-Baum ist exakt identisch mit dem zuvor grünen `40c20fd6` (`38ca8d18…`). [Merge-Lauf #254](https://github.com/n05a-design/glide-to-do/actions/runs/41900199421) scheitert unter Linux erstmals an B16, „kein Bild erreicht“. Windows-Vollprüfung und -Paket desselben Merge-Laufs sowie Mac-Paket #33 sind grün. Das ist ein anderer erster Blocker als die früheren Schrift-/Kopf-/Werkzeugfehler; spätere Linux-Suiten bleiben in diesem roten Versuch übersprungen.

## Befund und Änderung

Der alte Test wartete zehn `update()`-Runden, ermittelte sofort eine noch veränderliche Texthöhe und suchte ausschließlich in den ersten 900 Pixeln. Die Anwendung legt Bildflächen zeitversetzt an; schnelle Ereignisschleifen garantieren keine verstrichenen 120 ms. Eine kontrolliert verzögerte Bildanordnung reproduziert exakt „kein Bild erreicht“ bei unveränderter Anwendung. Das weist einen zeit- und ausschnittabhängigen Prüfaufbau nach; ein falscher Mausradschritt war in diesem CI-Bericht noch nicht erreicht.

Der Test wartet jetzt begrenzt auf fertige Bildflächen und ausstehende Konvertierungen, steuert alle echten Bildanker an und misst Radereignisse aus identischer Ausgangslage über Bild und nativer Tk-Textklasse. Der Referenzweg enthält keine App-Bindungen; ein gemeinsamer Fehler kann beide Wege daher nicht gleichzeitig falsch grün machen. Die 60-Pixel-Grenze bleibt, wirkungslose Bewegungen und mehr als ein Pixel Abweichung werden zusätzlich abgelehnt. Der Seiteninhalt muss unverändert bleiben.

Keine Produktionsdatei, Schrift, Ressource, Version, Datenformat oder Python-/Native-Lieferung geändert. Der manuelle `ui-nachlauf` enthält jetzt zuerst alle 17 UI-/UX-Verträge, danach die 45 Arbeitsmodi. Normale Vollmatrix und Pakettor bleiben bestehen. Zwei neue isolierte Defektgegenproben prüfen Einheitensprünge und wirkungsloses Bildrad; eine grüne positive UI-/UX-Basis bleibt Voraussetzung. Die Kalibrierung umfasst damit 20 Fälle.

## Nachweise und Grenzen

[Strukturierter Befund](ergebnis.json). Unveränderter alter Test mit 4.000 ms Layoutverzögerung rot; neuer Test unter derselben Verzögerung grün (drei Bilder, sechs Radproben). Eingeschalteter alter Einheitenschritt rot (58 statt 30 px); wirkungsloser Handler rot (0 statt 30 px). Beide in den regulären Gegenproben nur bei passender Assertion als erkannt gewertet. Rohprotokolle bleiben lokal. Bereichsabschluss und strenge Grundstufe werden nach tatsächlichem Ergebnis ergänzt; neuer nativer Fernlauf bleibt bis zum Push offen. Der rote Originalbericht wird nicht umetikettiert. Menschliche Sicht-/DPI- und native Paketlieferung sind eigene Nachweise.

**Lokaler Abschluss:** [UI-/UX](uiux-lokal.json) 17/17 grün; [strenge Grundstufe](grundstufe.json) 19/19, 245 Werkzeugtests (ein Skip), zweimal 1.128 Fachtests. [Beide Defektgegenproben](gegenproben.json) erreichen nach grüner positiver Einzelbasis genau die erwartete Assertion. 92 Code-Dateien und 171 Ressourcen der Python-Fassung bytegleich. Das erneuert keine unveränderten nativen Lieferdateien; neuer nativer CI-Nachlauf folgt auf dem gepushten Teststand.
