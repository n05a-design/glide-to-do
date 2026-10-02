# Glide 3.33.3 – Deutsche Schnelleingabe mit Feldchips (G01)

Stand 02.10.2026 · Glide 3.33.3 · Aufgabenformat 20

Auftrag vom 02.10.2026: Feature-Umsetzung G01 (Auswahl B-01). Grundlage sind D01 und D10 in der [Arbeitsrichtung](ARBEITSRICHTUNG.md), U04 in der [UX-Prüfung](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md) und G01 in der [Funktionsrecherche](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md). Keine Datenformatänderung, keine neue Abhängigkeit.

## Bedienvertrag

| Eingabe | Feld | Beispiel |
|---|---|---|
| Datum ohne Zusatz: „heute“, „morgen“, „übermorgen“, Wochentag, „nächsten Freitag“, „in 3 Tagen“, „in einer Woche“, „24.12.“, „24.12.2026“ | Bearbeitungstag | „Exposé morgen“ |
| „fällig“, „fällig am“, „bis“, „bis zum“ vor einem Datum | Fälligkeit | „Angebot bis Freitag“ |
| Uhrzeit „14:30“, „14 Uhr“, „um 9:00“ direkt nach dem Datum | Uhrzeit dieses Datums | „morgen 14:30“, „bis 24.12. um 10 Uhr“ |
| Uhrzeit allein | Bearbeitungstag heute mit Uhrzeit | „Anruf um 15 Uhr“ |
| „45 Minuten“, „45 min“, „2h“, „1,5 Stunden“, „1 Std. 30 Min.“ | Aufwand | |
| „!hoch“, „!wichtig“, „!mittel“, „!niedrig“ | Wichtigkeit | |
| „#Labelname“ eines vorhandenen Labels | Label | Unbekannte Namen bleiben Text |
| `/morgen`, `/Freitag`, `/24.12.2026`, `/meintag` | Bearbeitungstag (D10) | |
| `/bis …`, `/fällig …` | Fälligkeit | `/bis Freitag` |
| `/wichtig`, `/hoch`, `/mittel`, `/niedrig`, `/Labelname` | wie bisher | |

- Je Art zählt die erste Angabe; weitere bleiben Text. Ein Wochentag meint wie bisher den nächsten, heute eingeschlossen; „nächsten“ schließt heute aus.
- **Sichtbar und rücknehmbar:** Unter der Eingabezeile steht jede Erkennung als Chip mit „Bearbeitungstag Sa 03.10.2026“, „Fällig …“, „Aufwand 45 Min.“ usw. Ein Klick auf × nimmt sie zurück: Der Text bleibt im Titel und wird auch nicht teilweise neu gedeutet („bis Freitag“ wird nicht zu „Freitag“). Zurückgenommenes gilt bis zum Leeren der Zeile. Tab ergänzt weiter angefangene „/“-Wörter; Escape blendet die Leiste aus.
- **Wörtlich:** Text in Anführungszeichen ("…" oder „…“) wird nicht gedeutet und behält seine Zeichen. Ohne Erkennung bleibt der Text unverändert; Satzzeichen werden nur dort aufgeräumt, wo eine Angabe herausgenommen wurde.
- **Schnellerfassung:** Derselbe Parser liest den Titel; die Chips stehen darunter. Ein ausgefülltes Feld „Fällig“ hat Vorrang vor einer Fälligkeit im Titel; der Chip sagt das.
- Nach dem Anlegen bleibt die Rückmeldung „Angelegt · …“ mit Rückgängig.
- Gespeicherte Daten ändern sich nicht. Die volle Eingabemaske bleibt bei ihren eigenen Feldern; Parser und Chips gibt es dort bewusst nicht.

Die Fachlogik ist Tk-frei in `capture_parser.py` (D17): Wörter mit Textstelle, geschützte Bereiche, Datums-, Uhrzeit-, Aufwands-, Wichtigkeits- und Labelerkennung, Schlüssel zum Zurücknehmen, Titelbereinigung. Die bisherigen Parser `parse_capture_due`, „/“-Befehle und Vorschläge sind dorthin umgezogen; das Feld „Fällig“ der Schnellerfassung nutzt weiter `parse_capture_due` mit seiner festen Bedeutung. 14 Unit-Tests mit festem Stichtag.

## Nicht in diesem Schnitt

- **Wiederholungen** („jeden Montag“, „alle 2 Wochen“): in 3.33.3 offen, weil eine Wiederholung im Datenmodell an der Fälligkeit hängt; nach der Entscheidung des Inhabers mit 3.33.4 ergänzt (Abschnitt unten).
- **Rest von U04:** „Erweitert“ und „Hinzufügen“ als Textknöpfe durch „+“ und `Shift+Enter` ersetzen gehört zu UX1.
- Monatsnamen („24. Dezember“), „nächste Woche“, „Ende des Monats“ und Filter in Alltagssprache (G15).

## Prüfung

Neue Pflichtsuite `test_eingabe3333.py` über echte Wege: Tippen mit `<KeyRelease>` zeigt drei Chips für „Angebot schicken morgen bis Freitag /wichtig“; × auf „Fällig“ per Klick; Return legt an (Titel „Angebot schicken bis Freitag“, Bearbeitungstag morgen, Wichtigkeit hoch, keine Fälligkeit); Rückgängig; Uhrzeit, Aufwand, Label; Anführungszeichen; Escape; Schnellerfassung mit Klick auf × und Vorrang des Fälligkeitsfelds; Handbuchtext. Gegenprobe: Mit 3.33.2 scheitert die Suite. `test_bilder330` prüft jetzt `/morgen` als Bearbeitungstag (D10).

## Abschluss 02.10.2026

[Nachweis](../tests/qa-3.33.3/eingabe_2026-10-02/README.md), [Vollprotokoll](../tests/qa-3.33.3/eingabe_2026-10-02/vollpruefung/ergebnis.json), [Quellstand](../tests/qa-3.33.3/eingabe_2026-10-02/quellstand.json), [Lieferabgleich](../tests/qa-3.33.3/eingabe_2026-10-02/auslieferung.json).

- **Vollprüfung Exitcode 0** (02.10.2026, rund 11:58–12:22, ohne Eingaben, `caffeinate -dims`): 79 Schritte – Syntax, Version, Dokumentation, Fixtures, Unit-Tests, alle 62 Integrationssuiten, Showcase, fünf Analysen, Beispiel- und Releasedaten; Screenshot-Erzeuger und menschliche Sichtprüfung plattformbedingt übersprungen. Quellstand (333 Dateien) vor und nach dem Lauf unverändert.
- **Auslieferung:** `abgleich_07.py` ohne Abweichung (3.33.2-Hauptdatei als `_Z` archiviert), Bundle neu gebaut; 144 Dateien in `07_Python-Versionen` und 58 im Bundle per SHA-256 gleich `src/glide`; Bundle 3.33.3, `de.shaye.glide`, Signatur gültig. Showcase ausgeliefert.
- **Manuell offen:** Tippen und Zurücknehmen mit echter Tastatur und Maus, Schriftgrößen und schmale Fenster für die Chipleiste, Windows/Linux, DPI und Screenreader.

## Ergänzung 3.33.4: Wiederholungen

Entscheidung des Inhabers vom 02.10.2026: „Klar kann gerne eine Fälligkeit setzen, soll ja auch im Kalender auftauchen.“ Eine Wiederholung in der Eingabe setzt deshalb die Fälligkeit auf ihren ersten Termin; D01/D10 gelten für alle übrigen Datumsangaben unverändert.

| Eingabe | Regel (Datenmodell) | Erster Termin = Fälligkeit |
|---|---|---|
| „täglich“, „jeden Tag“, „alle 1 Tage“ | täglich | heute |
| „werktags“, „jeden Werktag“, „an Werktagen“ | bestimmte Wochentage Mo–Fr | nächster Werktag, heute eingeschlossen |
| „wöchentlich“, „jede Woche“ | wöchentlich | heute |
| „jeden Montag“, „montags“ | wöchentlich ab Montag | nächster Montag, heute eingeschlossen |
| „montags und donnerstags“, „montags, mittwochs und freitags“, „jeden Montag und Donnerstag“ | bestimmte Wochentage | nächster dieser Tage |
| „alle 3 Tage“, „alle 2 Wochen“, „alle zwei Wochen“ | alle N Tage (Wochen × 7, höchstens 365) | heute |
| „monatlich“, „jeden Monat“ | monatlich | heute |
| „jährlich“, „jedes Jahr“ | jährlich | heute |

- Eine Uhrzeit direkt dahinter wird die Uhrzeit der Fälligkeit („jeden Montag 18 Uhr“).
- Steht zusätzlich eine ausdrückliche Fälligkeit („jährlich bis 31.05.2027“), beginnt die Reihe dort; der Chip sagt „ab der Fälligkeit“.
- Der Chip nennt Regel und ersten Termin, etwa „Wiederholung jeden Montag · fällig ab Mo 05.10.2026“; × nimmt die ganze Angabe zurück, der Text bleibt im Titel.
- Regeln, die das Datenmodell nicht kennt („alle 3 Monate“, „jeden 15.“), bleiben Text. „alle Unterlagen“, „jeden Kunden“ oder „Montagsrunde“ sind keine Wiederholung.
- Abhaken erzeugt den Folgetermin über die vorhandene Wiederholungslogik; die Wiederholung lässt sich in der Eingabemaske wie jede andere bearbeiten.

Prüfung: drei weitere Unit-Tests (Fälligkeit, Vorrang einer ausdrücklichen Fälligkeit, kein Fehlalarm in normalem Text); `test_eingabe3333.py` tippt „Sport jeden Montag 18 Uhr“, legt mit Return an, prüft Regel, Fälligkeit, Kalender und den Folgetermin nach dem Abhaken sowie das Zurücknehmen per ×. Gegenprobe: 3.33.3 las dieselbe Eingabe als Bearbeitungstag. [Nachweis](../tests/qa-3.33.4/wiederholung_2026-10-02/README.md).

**Abschluss 3.33.4 (02.10.2026):** [Vollprotokoll](../tests/qa-3.33.4/wiederholung_2026-10-02/vollpruefung/ergebnis.json), [Quellstand](../tests/qa-3.33.4/wiederholung_2026-10-02/quellstand.json), [Lieferabgleich](../tests/qa-3.33.4/wiederholung_2026-10-02/auslieferung.json). Vollprüfung Exitcode 0 (rund 13:27–13:51, ohne Eingaben): 79 Schritte, alle 62 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; Quellstand (334 Dateien) unverändert. 144 Python-/58 Bundle-Dateien bytegleich, Bundle 3.33.4, Signatur gültig, Showcase ausgeliefert. Manuell offen: echte Tastatur- und Mausbedienung, Windows/Linux, DPI, Screenreader.
