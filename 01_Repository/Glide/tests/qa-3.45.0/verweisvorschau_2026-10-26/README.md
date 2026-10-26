# Lokale Verweise in der Nebenansicht nachschlagen

Fortsetzungsauftrag 26.10.2026 · D55 / WA-11 · Quellkandidat auf 3.45.0 · Aufgabenformat 26 unverändert.

Seiten-, Notiz-, Listen- und Aufgabenverweise lassen sich direkt neben der Hauptarbeit nachschlagen. Strg/Cmd+Umschalt+Klick auf einen lokalen Textverweis öffnet die Nebenansicht. Im Textkontext und im Mehr-Menü steht „Verweis in Nebenansicht öffnen“, wenn die aktuelle Stelle einen lokalen Verweis enthält. Das vorhandene Menü „Verweise und Rückverweise“ erhält „In Nebenansicht öffnen“ mit den verbundenen Zielen. Der bisherige normale Öffnungsweg und Strg/Cmd+Klick bleiben erhalten.

Das Ziel wird bei jeder Ausführung anhand typisierter IDs erneut aufgelöst. Aufgabenverweise zeigen ihre aktuelle Heimatliste/-seite und markieren die Aufgabe; Seitenaufgaben werden im lesenden Text hervorgehoben. Außerhalb einer gekürzten Vorschau liegende Ziele werden benannt. Archiv und schreibgeschützter Bestand bleiben lesbar. Fehlende/Papierkorbziele und nicht unterstützte Zeichnungen/Galerien werden nicht scheinbar angezeigt. Das Vorschaukürzel öffnet keine externen Adressen im Browser.

Der Haupteditor samt offenem Text bleibt bestehen. Die Vorschau erhält den Lesefokus; Esc/Schließen führt nach dem bestehenden D55-Weg zurück. Keine zweite schreibende Ansicht und keine neue gespeicherte Struktur. Zielauflösung Tk-frei in `side_view.reference_target`, UI-Adapter über `open_object_reference(..., side=True)` und den vorhandenen Nebenansichtshost. WA-21/Fundorte bleibt ein anderer, ungewählter Vorschlag.

## Nachweise und Grenzen

- Baseline: neun Nebenansicht- und drei Objektverweis-Fachfälle grün.
- [Rote Fachgegenprobe](fach_gegenprobe.json): drei neue Zielauflösungsfälle fehlen am vorherigen Stand erwartungsgemäß.
- [Fachabschluss](fach_abschluss.json): 29/29 passende Fälle grün – zwölf Nebenansicht-, drei Objektverweis- und 14 unveränderte Tagesvorschlagsfälle.
- [Neue Bedienfälle](ui_abschluss.json): 2/2 grün am endgültigen Produktionshash `b53e6822…`. Echter Strg+Umschalt-Klick, Textkontext unter einer Auswahl, Verweis-/Rückverweismenü, aktuelle IDs/Titel nach Objektaustausch, Taskmarkierung in Liste und Seite, Erhalt des Haupteditors, offener Text, alter Strg-Klick und Esc geprüft.
- Zweiter Bedienfall: Notizeditor, kein externer Browseraufruf, Archiv/Schreibschutz, vorhandenes Aufgaben-Undo mit neuen Objekten, veraltetes Menü nach Papierkorb/fehlendem Ziel, Zeichnung und Kompaktmodus. 204 Knopfprüfungen in acht Kombinationen aus 860 × 700/1280 × 800, mittlerer/großer Schrift und Hell/Dunkel.
- [Quellstand](quellstand.json): alle fünf Quell-/Prüfdateien sind bytegleich mit dem oben grün geprüften Stand. 85 Laufzeitdateien, 104 registrierte Suiten; die bestehende Arbeitsmodussuite enthält jetzt 15 statt 13 Fälle.

Die ersten roten UI-Vorläufe bleiben erhalten: fehlender Kontextmenüeintrag (zunächst nur im Mehr-Menü vorhanden), Fokusübergabe und ein nicht abgeschlossener Notiz-Fixtureschritt. Kontextbefehl und Fokus wurden ergänzt; der Fixture-Text wird vor dem Aufgaben-Undo übernommen. Der native Menücallback wird vor seiner Warnungsprüfung im Ereignislauf abgearbeitet. Details in `ui_einstiege_vorlauf*.json` und `ui_grenzen_vorlauf*.json`.

**Keine vollständige native D55-Freigabe:** Weitere Versuche mit drei alten Nebenansichtsfällen und einer zusätzlichen Tastatur-Undo-Probe waren rot ([Regressionsvorlauf](regression.json), [weiterer Nachlauf](regression_nachlauf.json)). Die Seitenkästchenprüfung scheitert identisch auch an der unveränderten Lieferung; die Inspektorsuite ist dort ebenfalls rot ([Liefergegenprobe](regression_liefergegenprobe.json)). Der Listenfall schwankt. Bei der zusätzlichen Tastenprobe fehlte der tatsächliche Tk-Fokus; damit ist sie kein grüner Tastenbeleg.

Eine pauschale Wartephase und ein geänderter Prüfstart haben diese Befunde nicht zuverlässig beseitigt. Beide Eingriffe und die zusätzliche Tastatur-Undo-Erweiterung wurden aus dem endgültigen Paket zurückgenommen. Die finale App und die finale Prüfdatei stimmen erneut exakt mit den beiden grünen Vorschaufällen überein. Diese Rücknahme erklärt die verschiedenen späteren Versuchshashes; rote Ergebnisse werden nicht nachträglich als grün ausgegeben. Die breite native Fokus-/Inspektorprüfung bleibt bei WA-42 und der menschlichen D55-Abnahme offen.

Die abweichende Startgröße 1280 × 860 ist im `ListApp`-Konstruktor belegt. Nachtrag 26.10.: Der Inhaber bestätigt „Automatische Fensterverwaltung ist aktiv“. Damit besteht zusätzlich ein möglicher Einfluss auf Geometrie/Fokus; die Ursache aller roten nativen Fälle ist nicht belegt. PowerToys-/Fenstereinstellungen und fremde Prozesse wurden nicht verändert.

## Liefergrenze

Quelle auf 3.45.0 / Format 26; keine neue Abhängigkeit, Laufzeitdatei oder Formatstufe. `07_Python-Versionen` bleibt beim vorherigen Abschluss `2e69d875…`; seit WA-12 und dieser Vorschau unterscheiden sich `app.pyw`, `day_proposal.py` und `side_view.py`. Gemeinsame Gesamtprüfung und Lieferung am nächsten Phasenende nach D51. Kein Commit/Push/Merge; alte Git-Indexsperre unangetastet. Native Mac-/Reader-/DPI-/Mehrmonitor- und menschliche Abnahmen bleiben offen.
