# Kalenderimport aus ICS – Glide 3.21.0

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

3.20 schreibt Kalenderdateien, 3.21 liest sie. Wer eine Einladung, einen Schulungsplan, den
Urlaubskalender der Firma oder seine eigene Glide-Ausgabe als `.ics` vorliegen hat, bekommt
daraus Aufgaben mit Fälligkeit – mit derselben Vorsicht wie beim CSV-Import: Vorschau
zuerst, ein Rückgängig-Schritt, und niemals über vorhandene Punkte schreiben.

## Bedienung

- **Datei → „Kalenderdatei (ICS) importieren …"**, über die durchsuchbaren App-Aktionen
  oder im Kontextmenü einer Liste unter „Exportieren"; zuerst die Dateiauswahl, dann der
  Vorschaudialog.
- Der Dialog nennt **Dateiname, Kalendername, Erzeuger und Zahl der gefundenen Termine**
  sowie, was davon übernommen, übersprungen oder nicht gelesen werden kann.
- Vier **Inhaltsoptionen**: Beschreibungen übernehmen, Orte an die Beschreibung anhängen,
  Kategorien als Labels, Erinnerungen übernehmen. Zwei **Umgangsregeln**: Dauer als
  geschätzten Aufwand übernehmen und abgesagte Termine (`STATUS:CANCELLED`)
  überspringen. Vorbelegt sind alle.
- **Zeitraum**: alles, ab heute oder ab einem gewählten Datum – ein Jahreskalender soll
  nicht ungefragt hunderte alte Termine anlegen.
- **Ziel**: „Als neue Liste" (vorbelegt, Titel aus dem Kalendernamen, sonst aus dem
  Dateinamen; in der Ordneransicht im geöffneten Ordner) oder das Häkchen „An die geöffnete
  Liste anhängen".
- Die **Vorschau** zeigt die ersten acht Termine so, wie Glide sie anlegen würde.
- **„Importieren"** übernimmt, **Abbrechen** und Escape lassen den Bestand unverändert. Der
  Abschluss meldet Zahl der angelegten Punkte, übersprungene Termine mit Grund und nicht
  lesbare Felder. Der Import ist **ein** Rückgängig-Schritt, einschließlich neu angelegter
  Labels.

## Was gelesen wird

| ICS | Glide |
| --- | --- |
| `SUMMARY` | Aufgabentext (Pflicht; ohne Text wird der Termin übersprungen) |
| `DTSTART` als Datum | Fälligkeit, ganztägig |
| `DTSTART` als Zeitpunkt | Fälligkeit mit Uhrzeit |
| `DTEND` oder `DURATION` | geschätzter Aufwand in Minuten, wenn die Option aktiv ist |
| `DESCRIPTION` | Beschreibung |
| `LOCATION` | als Zeile „Ort: …" an die Beschreibung angehängt |
| `CATEGORIES` | Labels (vorhandene nach Namen wiederverwendet, fehlende neu angelegt) |
| `PRIORITY` | 1–4 → hoch, 5 → mittel, 6–9 → niedrig, 0 oder fehlend → keine |
| `RRULE` | Wiederholungsregel, soweit Glide sie kennt |
| `VALARM` mit `TRIGGER` | Erinnerung |
| `STATUS:CANCELLED` | Termin wird übersprungen, wenn die Option aktiv ist |
| `UID` | Duplikaterkennung, siehe unten |

Ein wiederkehrender Termin wird **eine** Aufgabe mit Wiederholungsregel, nicht eine Aufgabe
je Vorkommen – so, wie man sie in Glide selbst anlegen würde. `FREQ=DAILY`, `WEEKLY`,
`MONTHLY` und `YEARLY` werden übernommen, `INTERVAL` bei täglichen Regeln, `BYDAY` bei
wöchentlichen; `UNTIL` wird zum Enddatum. Was Glide nicht kennt – `COUNT`, `BYMONTHDAY`,
`BYSETPOS`, Intervalle bei Wochen, Monaten und Jahren –, wird verworfen: Die Aufgabe
entsteht dann ohne Wiederholung, und der Bericht zählt es. Eine Regel, die Glide nicht
abbilden kann, still zu vereinfachen wäre schlimmer als sie weglassen.

`VALARM` wird zur relativen Erinnerung, wenn der Auslöser ein Abstand vor dem Beginn ist
(`TRIGGER:-PT30M`), und zur festen Erinnerung bei einem Zeitpunkt
(`TRIGGER;VALUE=DATE-TIME`). Auslöser nach dem Beginn oder bezogen auf das Ende werden
verworfen und gezählt.

## Zeitangaben

- **Ortszeit ohne Kennung** (`20261001T093000`) wird als Ortszeit gelesen – genau so, wie
  3.20 sie schreibt.
- **UTC** (`20261001T073000Z`) wird in die Zeitzone des Geräts umgerechnet.
- **`TZID`**: Glide versucht die Zone über die Zeitzonendatenbank des Systems
  (`zoneinfo` aus der Standardbibliothek). Fehlt sie – unter Windows ist sie nicht
  garantiert –, wird die Zeit als Ortszeit gelesen und der Bericht weist darauf hin. Eine
  eigene Zeitzonentabelle liefert Glide bewusst nicht mit.

## Duplikate

Termine, deren `UID` schon als Glide-Punkt im Bestand steht – erkennbar an der eigenen
Form `glide-<Punkt-ID>@glide.local` –, werden **übersprungen** und gezählt. Der Rundlauf
„exportieren, importieren" legt dadurch keine Kopien an. Fremde UIDs werden nicht gemerkt:
Derselbe Fremdkalender zweimal importiert ergibt zweimal Aufgaben. Ein Abgleich, der
vorhandene Punkte aktualisiert, wäre eine Synchronisierung und bleibt eine eigene
Entscheidung.

## Zeitform des Wiederholungsendes

`UNTIL` trägt dieselbe Zeitform wie `DTSTART`: bei einem Uhrzeittermin schwebende
Ortszeit ohne „Z" (`UNTIL=20270131T235959`), bei einem Ganztagstermin ein reines Datum
(`UNTIL=20270131`). So verlangt es RFC 5545, und nur so überlebt das Enddatum den
Rundlauf in jeder Zeitzone. Bis 3.21.0 stand dort ein UTC-Zeitpunkt; beim Wiedereinlesen
verschob sich das Enddatum östlich von Greenwich um einen Tag.

Beim Lesen gilt die Umkehrung: `UNTIL` ist die Obergrenze einer Terminreihe, kein
Zeitpunkt, den jemand abliest. Glide nimmt deshalb den Kalendertag der Angabe, ohne
Zeitzonenumrechnung – auch bei einem fremden `…T235959Z`, das praktisch jedes
Kalenderprogramm so schreibt. `DTSTART` und Erinnerungen werden weiterhin umgerechnet;
dort ist der Zeitpunkt die Aussage.

## Grenzen

Höchstens **2000 Termine** und **12 MB** je Datei; darüber bricht der Import mit Begründung
ab, bevor etwas entsteht. Keine Synchronisierung, kein Abonnement, kein Netzzugriff: Glide
liest eine Datei, die man ihm gibt. Keine Teilnehmer, keine Einladungsantworten, keine
Anhänge, keine Ausnahmetermine (`EXDATE`), keine `VTODO`- oder `VJOURNAL`-Einträge, keine
Zeitzonendefinitionen aus `VTIMEZONE`, keine freien/gebuchten Zeiten. Ganztägige
Mehrtagestermine werden auf ihren ersten Tag gelegt – Glide kennt keine Zeitspanne über
mehrere Tage. Das Aufgabenformat bleibt **15**; der Import erzeugt ausschließlich Objekte,
die Glide auch von Hand anlegen könnte, und keine neue Laufzeitabhängigkeit.

## Abnahmekriterien

1. Eine mit 3.20 geschriebene Datei lässt sich lesen: Text, Fälligkeit mit und ohne
   Uhrzeit, Beschreibung, Labels, Wichtigkeit, Wiederholung und Erinnerung stimmen.
2. Derselbe Rundlauf ein zweites Mal legt keine Kopien an, weil die eigenen UIDs erkannt
   werden.
3. Gefaltete Zeilen, escapte Sonderzeichen, CRLF und LF, BOM und fehlende Leerzeilen
   werden gelesen.
4. UTC-Zeiten werden in Ortszeit umgerechnet; `TZID` nutzt die Systemdatenbank und fällt
   sonst auf Ortszeit zurück.
5. Ganztagstermine landen auf dem richtigen Tag; ein Mehrtagestermin auf seinem ersten.
6. Dauer wird zum Aufwand, wenn die Option aktiv ist; `DURATION` und `DTEND` führen zum
   gleichen Ergebnis.
7. Die vier übernehmbaren `FREQ`-Werte erscheinen – mit `INTERVAL` bei täglichen
   und `BYDAY` bei wöchentlichen Regeln – als Glide-Wiederholung; nicht
   abbildbare Regeln werden verworfen und gezählt.
8. Erinnerungen vor dem Beginn und feste Zeitpunkte werden übernommen, andere verworfen
   und gezählt.
9. Termine ohne `SUMMARY`, ohne `DTSTART`, mit `STATUS:CANCELLED` und außerhalb des
   gewählten Zeitraums werden übersprungen und mit Grund gezählt.
10. Termin- und Größenobergrenze brechen vor jeder Bestandsänderung ab; eine Zeilenobergrenze hat der ICS-Import nicht.
11. Beide Ziele landen am richtigen Ort; Rückgängig nimmt den Import samt neuer Labels
    vollständig zurück; Abbrechen ändert nichts.
12. Der Dialog ist in Hell und Dunkel bei 780×640 vollständig erreichbar.

## Prüfung

Die Suite `tests/integration/test_features321.py` prüft mit isoliertem `GLIDE_DATA_DIR`
den Rundlauf über die eigene Ausgabe aus 3.20 samt Duplikaterkennung, fremde Dateien mit
gefalteten Zeilen, Escaping, BOM und LF-Zeilenenden, UTC- und `TZID`-Zeiten, Ganztags- und
Mehrtagestermine, beide Dauerangaben, alle abbildbaren und drei nicht abbildbare
Wiederholungsregeln, beide Erinnerungsarten und zwei verworfene, alle Übersprungsgründe,
Zeitraumfilter, die Grenzen, beide Importziele, Rückgängig mit Labelrücknahme sowie den
Dialog in beiden Themes bei 780×640. Der Gesamtlauf umfasst damit 25 Suiten.
[QA-Bericht](07_QA_BERICHT.md) · [Kalenderausgabe 3.20](archiv/44_KALENDERAUSGABE_3.20.0.md) ·
[CSV-Import 3.18](archiv/42_CSV_IMPORT_3.18.0.md)
