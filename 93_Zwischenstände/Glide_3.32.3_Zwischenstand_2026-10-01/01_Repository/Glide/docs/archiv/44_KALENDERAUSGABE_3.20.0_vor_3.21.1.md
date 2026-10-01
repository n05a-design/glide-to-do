# Kalenderausgabe als ICS – Glide 3.20.0

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Fristen stehen in Glide, Termine stehen im Kalender – und wer beides im Blick haben will,
tippt bisher ab. 3.20 schreibt die Fälligkeiten als **ICS-Datei**, die Apple Kalender,
Outlook, Thunderbird und Google Kalender einlesen. Keine Synchronisierung, kein Konto: eine
Datei, die man importiert oder abonniert, wenn man sie an einen bekannten Ort legt.

## Warum eine Datei und keine Anbindung

Eine echte Kalenderanbindung bräuchte ein Konto, OAuth, eine Netzwerkschicht und einen
Hintergrundprozess – alles vier Dinge, die Glide bewusst nicht hat. Die ICS-Datei ist das
Gegenstück zur Druckansicht aus 3.17: **reine Ausgabe** aus vorhandenen Objekten,
plattformgleich, ohne neue Laufzeitabhängigkeit, in einem Format, das in zehn Jahren noch
lesbar ist.

## Bedienung

- **Datei → „Kalenderdatei (ICS) …"**, über die durchsuchbaren App-Aktionen oder im
  Kontextmenü einer Liste unter „Exportieren".
- Im Dialog den **Umfang** wählen:
  - **Aktuelle Liste oder Ordner** – in der Ordneransicht alle enthaltenen Listen.
  - **Alle Listen** – der gesamte Bestand.
  - **Mein Tag und heute Fällige** – dieselbe Menge wie der Tageszettel.
  - **Tagesplanung des gewählten Tages** – die Punkte mit Bearbeitungstag an diesem Tag.
- Sechs **Inhaltsoptionen**: erledigte Punkte mitausgeben, Beschreibungen als
  Terminbeschreibung, Labels als Kategorien, Dauer aus dem geschätzten Aufwand,
  Bearbeitungstage als eigene Ganztagstermine, Erinnerungen als Kalenderalarm.
  Vorbelegt sind alle außer „erledigte Punkte" und „Bearbeitungstage".
- **„Speichern …"** fragt nach dem Zielpfad, **„Speichern und öffnen"** legt die Datei ab
  und übergibt sie an das Standardprogramm – dort landet sie im gewohnten Importdialog.
  Abbrechen und Escape erzeugen nichts.
- Die Kopfzeile des Dialogs nennt, wie viele Termine entstehen und wie viele Punkte ohne
  Fälligkeit übersprungen werden.

## Was ein Termin enthält

Grundlage ist die **Fälligkeit**: Ohne Fälligkeit gibt es keinen Termin – eine Aufgabe ohne
Datum hat im Kalender keinen Platz. Aus jedem fälligen Punkt entsteht ein `VEVENT`:

| Feld | Inhalt |
| --- | --- |
| `SUMMARY` | Punkttext, einzeilig; erledigte Punkte mit dem Präfix „Erledigt: " |
| `DTSTART` / `DTEND` | mit Uhrzeit: Beginn und Ende; ohne Uhrzeit: Ganztagstermin (`VALUE=DATE`, Ende am Folgetag) |
| `DESCRIPTION` | Beschreibung, Quellliste, Wichtigkeit, Aufwand und Labels – jede Angabe in eigener Zeile |
| `CATEGORIES` | die Labels des Punkts |
| `PRIORITY` | hoch → 1, mittel → 5, niedrig → 9, keine → ohne Angabe |
| `RRULE` | die Wiederholungsregel des Punkts |
| `VALARM` | die Erinnerung des Punkts |
| `UID` | `glide-<Punkt-ID>@glide.local` – bei erneuter Ausgabe dieselbe |

Die **Dauer** eines Termins mit Uhrzeit kommt aus dem geschätzten Aufwand, wenn er gesetzt
und die Option aktiv ist; sonst gilt eine halbe Stunde. Bearbeitungstage erscheinen – wenn
zugeschaltet – als eigene Ganztagstermine mit dem Präfix „Planung: " und einer eigenen UID,
damit sie den Fälligkeitstermin desselben Punkts nicht überschreiben.

Die stabile UID ist der praktische Kern: Wer die Datei ein zweites Mal einliest,
**aktualisiert** seine Termine statt sie zu verdoppeln, weil `UID` und `SEQUENCE` dem
Kalender sagen, dass es derselbe Termin in neuer Fassung ist.

## Zeitangaben ohne Zeitzonentabelle

Termine werden in **schwebender Ortszeit** geschrieben – `DTSTART:20261001T093000` ohne
Zeitzonenkennung. Ein Kalender liest sie als Zeit in der Zone des Geräts, und genau so ist
eine Frist in Glide gemeint: 9:30 bleibt 9:30, auch wenn man das Gerät mit auf eine Reise
nimmt. Der Weg über `VTIMEZONE` hätte eine mitgelieferte Zeitzonentabelle gebraucht, die
mit jeder Sommerzeitreform veraltet.

Ausnahme sind zwei Werte, die einen echten Zeitpunkt bezeichnen: der Zeitstempel der Datei
(`DTSTAMP`) und eine feste Erinnerung (`TRIGGER;VALUE=DATE-TIME`) stehen in UTC, weil sie
schon im Bestand als eindeutiger Zeitpunkt gespeichert sind.

## Wiederholungen

| Glide-Regel | RRULE |
| --- | --- |
| täglich | `FREQ=DAILY` |
| alle N Tage | `FREQ=DAILY;INTERVAL=N` |
| an bestimmten Wochentagen | `FREQ=WEEKLY;BYDAY=MO,DI…` als `MO,TU,WE,TH,FR,SA,SU` |
| wöchentlich | `FREQ=WEEKLY` |
| monatlich | `FREQ=MONTHLY` |
| jährlich | `FREQ=YEARLY` |

Ein gesetztes Enddatum wird zu `UNTIL`. Glide rechnet Wiederholungen selbst nicht im
Voraus aus (eine Regel, kein Terminplaner) – im Kalender übernimmt das die Anwendung, die
die Datei liest. Beim monatlichen Vorrücken gilt dort die Regel des Kalenders und nicht
Glides Monatsletzter-Regel; das ist der eine Punkt, an dem Ausgabe und Bestand um einen Tag
auseinanderlaufen können.

## Dateiaufbau

Eine Datei, UTF-8, CRLF-Zeilenenden, `BEGIN:VCALENDAR` mit `VERSION:2.0` und
`PRODID:-//Glide//Aufgaben und Listen <Version>//DE`, `CALSCALE:GREGORIAN`,
`X-WR-CALNAME` mit dem Namen der Ausgabe. Zeilen werden nach RFC 5545 bei 75 Oktetten
**gefaltet** (Fortsetzung mit einem führenden Leerzeichen), Sonderzeichen escaped
(`\\`, `\;`, `\,`, `\n`). Geschrieben wird atomar über eine Temporärdatei; Nutzdatendateien
sind als Ziel ausgeschlossen. Ab **2000 Terminen** endet die Ausgabe mit einem Hinweis im
Kalendernamen und in der Abschlussmeldung.

Die Ausgabe liest nur vorhandene Objekte: Sie verändert weder Aufgaben noch Einstellungen
und legt keine eigene Datenhaltung an. Ein Verlaufseintrag entsteht dadurch nicht.

## Grenzen

Keine Synchronisierung und kein Abgleich zurück – was im Kalender geändert wird, kommt
nicht nach Glide. Kein Konto, kein Netzzugriff, kein Hintergrundprozess, keine
automatische Neuausgabe bei Änderungen. Keine `VTODO`-Ausgabe (Aufgabenlisten in Apple
Erinnerungen), keine Teilnehmer, keine Einladungen, keine Orte, keine Anhänge im Termin,
keine `VTIMEZONE`-Definitionen, keine Ausnahmetermine (`EXDATE`) und keine
Ausnahmeregeln. Punkte ohne Fälligkeit erscheinen nicht. Gruppen und Überschriften
erscheinen nicht – sie tragen keine Fälligkeit.

## Abnahmekriterien

1. Jeder Umfang erzeugt eine vollständige, RFC-konform aufgebaute Datei mit
   `BEGIN:VCALENDAR`, `VERSION`, `PRODID` und passender Zahl von `VEVENT`-Blöcken.
2. Punkte mit Uhrzeit erhalten Beginn und Ende, Punkte ohne Uhrzeit einen Ganztagstermin
   mit Ende am Folgetag.
3. Die Dauer folgt dem geschätzten Aufwand, wenn die Option aktiv ist, sonst der halben
   Stunde.
4. Jede der sechs Optionen wirkt einzeln und nachvollziehbar.
5. Alle sechs Wiederholungsarten und ein Enddatum erscheinen als korrekte `RRULE`.
6. Relative und feste Erinnerungen erscheinen als `VALARM` mit passendem `TRIGGER`.
7. Sonderzeichen, Semikola, Kommata und Zeilenumbrüche sind escaped; keine Ausgabezeile
   überschreitet 75 Oktette.
8. Die UID eines Punkts bleibt über mehrere Ausgaben gleich; Bearbeitungstag und
   Fälligkeit tragen verschiedene UIDs.
9. Punkte ohne Fälligkeit werden übersprungen und gezählt; Gruppen und Überschriften
   erscheinen nicht.
10. Ab 2000 Terminen endet die Ausgabe mit Hinweis.
11. Das Schreiben ist atomar, hinterlässt keine Temporärdatei und trifft keine
    Nutzdatendatei; Bestand, Einstellungen und Änderungsverlauf bleiben unberührt.
12. Der Dialog ist in Hell und Dunkel bei 780×640 vollständig erreichbar; Abbrechen
    erzeugt nichts.

## Prüfung

Die Suite `tests/integration/test_features320.py` prüft mit isoliertem `GLIDE_DATA_DIR`
den Aufbau aller vier Umfänge, Ganztags- und Uhrzeittermine, die Dauerregeln, jede der
sechs Optionen einzeln, alle Wiederholungsarten samt Enddatum, beide Erinnerungsarten,
Escaping und Zeilenfaltung, stabile UIDs über zwei Ausgaben, übersprungene Punkte ohne
Fälligkeit, die Obergrenze, atomares Schreiben samt abgewiesener Nutzdatendatei, die
Unveränderlichkeit von Bestand und Verlauf sowie den Dialog in beiden Themes bei 780×640.
Der Gesamtlauf umfasst damit 24 Suiten.
[QA-Bericht](07_QA_BERICHT.md) · [Änderungsverlauf 3.19](43_AENDERUNGSVERLAUF_3.19.0.md) ·
[Druck und PDF 3.17](41_DRUCK_UND_PDF_3.17.0.md)
