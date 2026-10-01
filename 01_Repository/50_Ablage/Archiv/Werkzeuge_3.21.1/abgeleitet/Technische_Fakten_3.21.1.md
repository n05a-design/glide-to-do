# Technische Fakten – Glide 3.21.1

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

3.21.1 ist eine reine Fehlerbehebung. Kein neues Bedienelement, kein neues Feld, kein
Formatsprung. Behoben sind zwei Zeitzonenfehler im Kalenderrundlauf und ein Fehler im
Prüfstand, der einen Abgleichschritt seit 3.19 unmöglich grün werden ließ.

## Zeitform von `UNTIL`

`DTSTART` steht in Glide in **schwebender Ortszeit** oder als **reines Datum**. RFC 5545
verlangt, dass `UNTIL` dieselbe Zeitform trägt. 3.21.0 schrieb stattdessen einen
UTC-Zeitpunkt:

| | 3.21.0 | 3.21.1 |
| --- | --- | --- |
| Uhrzeittermin | `UNTIL=20270131T235959Z` | `UNTIL=20270131T235959` |
| Ganztagstermin | `UNTIL=20270131T235959Z` | `UNTIL=20270131` |

`ics_repeat_rule` nimmt dafür den neuen Parameter `ganztaegig`; `ics_event_lines` übergibt
ihn als `not zeit` – dieselbe Bedingung, die über den `DTSTART`-Werttyp entscheidet. Damit
können die beiden Angaben nicht auseinanderlaufen.

## Lesen von `UNTIL`

`ics_repeat_from_rule` nutzt nicht mehr `parse_ics_moment`, sondern die neue Methode
`parse_ics_until`. Sie nimmt den **Kalendertag der Angabe selbst**, ohne
Zeitzonenumrechnung, und lässt nur die Formen `JJJJMMTT`, `…THHMM[SS]` und `…THHMM[SS]Z`
zu. Alles andere ergibt `None`, die Regel entsteht dann ohne Enddatum und der Bericht
zählt es.

Die Abweichung von der sonstigen Regel „UTC in Ortszeit holen" ist beabsichtigt: `UNTIL`
ist die Obergrenze einer Terminreihe, kein Zeitpunkt, den jemand abliest, und Glide merkt
sich davon nur den Tag. Fremde Programme schreiben das Tagesende praktisch immer als
`…T235959Z`. Wer das als Zeitpunkt umrechnet, verlängert die Reihe östlich von Greenwich
um einen Tag und verkürzt sie westlich. `DTSTART` und `VALARM` rechnen weiterhin um –
dort ist der Zeitpunkt die Aussage.

## Verlaufszeiten im Fixture-Abgleich

`inhalt_normalisieren` in `tests/tools/pruefen.py` behandelt den Schlüssel `history`
gesondert und lässt in jedem Eintrag das Feld `at` weg. Begründung: Der Verlauf aus 3.19
entsteht in `update_history` beim Speichern und trägt den echten Zeitpunkt – genauso
unreproduzierbar wie `exported_at`. Zwei Erzeugungen im Abstand von Sekunden lieferten
unterschiedliche Werte, der Abgleich konnte damit **nie** gleich ausfallen. Verglichen
werden weiterhin `kind`, `action`, `target`, `list`, `count` und die über `identities`
normalisierte `id`.

Die Schritte „Beispieldaten-Abgleich" und „Release-Abgleich" liefen erst ab
`--modus voll`. Für 3.19.0 und 3.20.0 gab es keinen macOS-Lauf, deshalb blieb der Fehler
bis zum 3.21.0-Lauf unentdeckt.

## Zeitzone der Prüfläufe

`Prueflauf.__init__` setzt `TZ` auf `Europe/Berlin`, wenn die Umgebung keine Zone vorgibt
(`self.env.setdefault`). In UTC ist jeder Zeitzonenfehler unsichtbar, weil der Versatz
null ist – der `UNTIL`-Fehler war in der UTC-Vorabumgebung grün. Europe/Berlin hat
Sommer- und Winterzeit und deckt damit beide Versätze ab. Ein gesetztes `TZ` bleibt
unangetastet, damit sich jede Zone gezielt nachstellen lässt.

`test_features321.py` setzt die Zone zusätzlich selbst, vor dem Laden des Moduls – die
Suite muss auch beim direkten Aufruf in einer Zone mit Versatz laufen.

## Geänderte Dateien

| Datei | Änderung |
| --- | --- |
| `src/glide/app.pyw` | `ics_repeat_rule` mit `ganztaegig`, neue Methode `parse_ics_until`, `ics_repeat_from_rule` nutzt sie, `ics_event_lines` übergibt den Werttyp |
| `tests/tools/pruefen.py` | `verlauf_bereinigen` in `inhalt_normalisieren`, `TZ`-Vorgabe in `Prueflauf.__init__` |
| `tests/integration/test_features321.py` | Zonenvorgabe im Kopf, Abschnitt 1b mit vier Zonen und drei Schreibweisen |
| `tests/integration/test_features320.py` | Zeitform der Ausgabe für beide Werttypen |
| `tests/tools/releasedaten.py` | Versionsangaben und Verweis auf `tests/qa-3.21.1/abschluss` |

## Prüfstand

Alle **25 Suiten** und beide statischen Analysen sind in der Linux-Vorabumgebung mit
Exitcode 0 gelaufen (Python 3.12.3, Tk 8.6 unter Xvfb) – erstmals unter
`TZ=Europe/Berlin` statt UTC. Der Beispiel- und Releaseabgleich wurde gegen eine
unabhängige Zweiterzeugung nachgestellt und fällt gleich aus. Der maßgebliche macOS-Lauf
steht aus: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.1/abschluss`.

## Offen geblieben

`tests/tools/releasedaten.py` hängt an jeden Codebeleg den Zusatz
„Stand: 3.14.0 / Datenformat 13." (Zeile 70) und trägt im Kopf eine Memo-Zeile
„Releaseplanung für Glide 3.14.0 / Datenformat 13". Das ist seit 3.14 überholter
Inhalt im mitgelieferten Beispielbestand, aber unabhängig von dieser Fehlerbehebung –
siehe [Offene Entscheidungen](../Entscheidungen/Offene_Entscheidungen_3.21.1.md).
