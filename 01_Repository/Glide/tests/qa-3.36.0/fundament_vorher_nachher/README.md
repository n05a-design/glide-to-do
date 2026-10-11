# Fundament: Vorher-/Nachhermessung für 3.36.0

Stand 10.10.2026 · Glide 3.35.0 · Prüfkandidat für 3.36.0 vor Versionswechsel

Noch keine Produktionsabnahme. Referenz-Mac arm64, macOS 27.0.1, Python 3.14.5, Tk 9.0.3; ausschließlich künstliche Daten. Baseline ist die unveränderte App aus `62ad554` (Produktion 3.35.0). Quellhashes, Laufzeit, Rohwerte und Prüfdaten stehen in [zusammenfassung.json](zusammenfassung.json) und den einzelnen JSON-Dateien. Keine Profilerwerte in den Zeitreihen.

Je Verfahren fünf frische Prozesse und acht Folgerunden je Prozess: kalt n=5, warm n=40, p95 nach nächsthöherem Rang. „Kalt“ bezeichnet einen Aufbau ohne vorhandene Startseiten-Widgets bzw. ein noch nicht aufgebautes Einstellungsfenster; keinen Betriebssystem-Kaltstart. 1.000 Aufgaben, zwölf Aufgabenlisten, 1280 × 800. Jede Startseitenmessung macht die Signatur ungültig und führt den tatsächlichen Builder aus. Einstellungen einschließlich zentralem Modalweg, Mindestbreite, Mapping, Fokus und Griff; nur Benutzerwartezeit und Schließen sind ausgeschlossen. Drei Leerlaufrunden bis zur fertigen Darstellung.

## Direkter Start, abwechselnd Vorversion und Kandidat

| Messgröße | 3.35.0 Median / p95, ms | Kandidat Median / p95, ms | Ziel |
|---|---:|---:|---|
| Startseite kalt | 801,767 / 834,988 | 283,111 / 285,985 | ≤ 150 ms: **verfehlt** |
| Startseite warm, tatsächlicher Builder | 449,142 / 471,608 | 78,231 / 89,536 | ≤ 150 ms: erreicht |
| Einstellungen erste Anzeige | 598,900 / 637,944 | 177,668 / 180,033 | ≤ 250 ms: erreicht |
| Einstellungen erneut | 590,401 / 627,876 | 132,519 / 136,449 | ≤ 150 ms: erreicht |

Der Aufbau der Startseite verwendet natürliche Tk-Frame-Höhen statt einer Rückkopplung der Inhaltshöhe über eingebettete Canvas-Fenster. Geänderte Inhalte werden abgeglichen, unveränderte Widgets behalten ihre Lebensdauer. Diese Variante benötigt 119 statt 112 Widgets; Einstellungen weiterhin 137. Die Messung belegt keinen unveränderlichen Grenzwert von Tk.

## Start aus einem Python-Messreihenprozess

Zusätzliche getrennte Serie mit derselben App und demselben Werkzeug. Der Start über `subprocess.run` ergibt beim Kandidaten einen langsameren ersten Aufbau; die Ursache ist noch nicht abschließend belegt. Die Reihen werden nicht vermischt und die langsamere Serie wird nicht verworfen.

| Messgröße | 3.35.0 Median / p95, ms | Kandidat Median / p95, ms |
|---|---:|---:|
| Startseite kalt | 824,505 / 830,718 | 486,716 / 497,491 |
| Startseite warm | 456,760 / 480,861 | 79,945 / 90,240 |
| Einstellungen erste Anzeige | 604,840 / 617,291 | 185,603 / 199,586 |
| Einstellungen erneut | 599,178 / 638,576 | 136,399 / 144,001 |

## Viele Bibliothekskarten

10.000 Aufgaben in 200 Listen, zusätzlich Ordner, Notiz und Zeichnung, 1400 × 950, acht Messrunden nach Aufwärmen. [Vorversion](bibliothek-baseline-200.json), [Kandidat](bibliothek-kandidat-200.json).

- Geänderter Aufgabenstatus: Median 549,875 → 11,266 ms, p95 559,869 → 11,710 ms; neue Kartencontainer je Runde 2 → 0.
- Unveränderte Aktualisierung: Median 10,302 → 10,212 ms.
- Umordnen: Median 218,148 → 233,570 ms, p95 222,157 → 234,365 ms; etwa 7 % langsamer, in beiden Ständen keine neuen Kartencontainer. Kein allgemeiner Geschwindigkeitsgewinn für jede Bibliotheksaktion behauptet.

## Entscheidung D46 und weitere Prüfungen

Das vereinbarte Kaltziel von 150 ms ist nicht erreicht. Entwicklungsplan §15.7/§15.8 und D33 verlangen, messbare Zielabweichungen ausdrücklich vorzulegen. Vorgeschlagene Ausnahme: kalter Aufbau ≤ 300 ms im direkten Start und ≤ 500 ms im beobachteten Kindprozessverfahren; warmer tatsächlicher Builder bleibt ≤ 150 ms. **Am 10.10.2026 durch D46 ausdrücklich akzeptiert**, Wortlaut: „A – belegte Kalt-Ausnahme übernehmen (Empfehlung)“. Endgültigen Lieferstand nach verbleibenden Korrekturen erneut prüfen. Alle gewählten Funktionen bleiben im Paket.

Gezielte Pflichtsuite und drei passende rote Gegenproben gegen 3.35.0 liegen vor; fünf kalibrierte Erwartungen bestehen ihre positiven Mac-Läufe und scheitern an den jeweils absichtlich defekten Kopien. [UI-Lebensdauer](lebensdauer.json): nach fünf Aufwärmrunden jeweils 100 tatsächliche Startseiten-Builder, Bibliotheks-Titelabgleiche und erneute Modalöffnungen. Widget-/Tcl-Rückrufzahlen bleiben 119/945, 125/1198 und 137/204; offene Timer 5, 4 und 4. Nach GC steigen beobachtete Python-Allokationen um rund 45 KB, 3 KB und 2 KB; kein Nachweis für unbegrenzten Langzeitbetrieb und keine Aussage über den absichtlich ausgeschlossenen Undo-Verlauf. Eingefrorene Vollprüfung, native Linux-/Windows-Ergebnisse und vollständige Lieferung werden gesondert nachgeführt. Grüne Mac-Gegenproben sind kein Linux-Nachweis.


## Endgültiger Quellkandidat 3.36.0 nach Scrollleistenkorrektur

Erneut fünf frische Prozesse je Verfahren, warm je 40 Werte, unveränderte Prüfdaten/Modalvorbereitung. Alle zehn Rohdateien `lieferung-*.json` und [Zusammenfassung mit Quellhash](lieferung_zusammenfassung.json) bleiben erhalten; die vorangegangene Reihe wird als Entscheidungsbeleg D46 nicht überschrieben.

| Messgröße | Direkt Median / p95, ms | Kindprozess Median / p95, ms | Tor |
|---|---:|---:|---|
| Startseite kalt | 248,043 / 261,376 | 459,904 / 469,568 | D46 ≤ 300 / ≤ 500: erreicht |
| Startseite warm | 80,449 / 88,060 | 78,953 / 86,707 | ≤ 150: erreicht |
| Einstellungen erste Anzeige | 189,938 / 198,044 | 192,130 / 196,700 | ≤ 250: erreicht |
| Einstellungen erneut | 148,974 / 155,082 | 149,237 / 160,521 | D47: Median ≤ 150/p95 ≤ 170: erreicht |

Kein Messwert entfernt. Höchster warmer Einstellungswert direkt 160,461 ms, Kindprozess 163,995 ms. Ein getrenntes Profil lokalisiert etwa 133 ms innerhalb des nativen `wm deiconify`; es beweist keinen unveränderlichen Tk-Grenzwert. Ein isolierter Vergleich mit vorübergehendem Alpha-Wert brachte keinen verlässlichen Gewinn und wurde nicht in die App übernommen. Keine Funktions- oder Datenumfangsänderung. Die Einstellungs-Warmgrenze ist inzwischen durch D47 ausdrücklich angepasst; D46 betrifft ausschließlich die Startseite.

**E01-Entscheidung D47, 10.10.2026:** „A – 150 ms Median / 170 ms p95 akzeptieren (Empfehlung)“. Die Warmgrenze gilt für den Median ≤ 150 ms und p95 ≤ 170 ms; erste Anzeige weiterhin ≤ 250 ms. Höchster Einzelwert der vorgelegten Kandidatenserie: 164 ms. Funktionsumfang unverändert; nach Korrekturen aus der Vollprüfung den Lieferstand erneut messen.

## Reparaturen aus der Vollprüfung und abschließende Messreihe

Die erste eingefrorene Vollprüfung fand einen Monat→Woche-Konflikt, eine fehlende Updatekarte und eine veraltete Esc-Testannahme. Semantisch getrennte Kalenderrahmen, vollständige Updatekarten-Signatur und der Prüfvertrag für verborgene, modal beendete Dialoge sind korrigiert. Pflichtsuite und drei betroffene Suiten gezielt grün.

[Reparaturreihe 1](reparatur1_zusammenfassung.json): Startseite kalt im Kindprozess Median/p95 484/508 ms überschritt D46; Einstellungen erfüllten D47. Alle zehn Rohdateien bleiben erhalten. Daraufhin ausschließlich die wiederholte Heute-Zählung innerhalb eines einzigen UI-Aufbaus im vorhandenen Rendercache zusammengefasst; außerhalb des Aufbaus stets frisch, in der Pflichtsuite geprüft. Keine Ziellockerung und kein entfernter Messwert.

[Abschließende Reparaturreihe 2](reparatur2_zusammenfassung.json), wieder fünf frische Prozesse je Startverfahren, kalt n=5/warm n=40, einschließlich echtem Builder/Modalweg:

| Messgröße | Direkt Median / p95, ms | Kindprozess Median / p95, ms | Tor |
|---|---:|---:|---|
| Startseite kalt | 266,017 / 282,377 | 482,879 / 493,274 | D46: erreicht |
| Startseite warm | 74,673 / 88,421 | 75,062 / 89,598 | ≤ 150: erreicht |
| Einstellungen erste Anzeige | 174,565 / 178,148 | 178,655 / 197,131 | ≤ 250: erreicht |
| Einstellungen erneut | 133,671 / 140,399 | 132,825 / 137,384 | D47: erreicht |

Finaler App-SHA-256: `04a059704080685ee9a10957116508a3261a51316c6d27edc8249738259dbf01`. Höchster warmer Einstellungswert direkt 158,601 ms, Kindprozess 148,078 ms. Automatische native Plattformprüfungen und menschliche Sichtprüfung sind getrennte Tore.
