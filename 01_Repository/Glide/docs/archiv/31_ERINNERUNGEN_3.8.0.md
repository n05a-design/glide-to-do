# Lokale Erinnerungen – Glide 3.8.0

Stand: 12.09.2026 · Entwicklungsstand · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

## Bedienung und Funktionsumfang

In den Punktdetails unter **Erinnerung** stehen „Zur Fälligkeit“, 10 Minuten,
eine Stunde, ein Tag vorher, ein eigener Minutenabstand und ein fester einmaliger
Zeitpunkt zur Verfügung. Aufgaben und Long-Tasks unterstützen Erinnerungen;
Gruppen und Überschriften bleiben reine Struktur.

Der Schalter **Erinnerungen …** oberhalb des Arbeitsbereichs sowie
**Ansicht → Erinnerungen …** öffnen die gemeinsame Übersicht. Sie enthält
geplante, verschobene, offene/verpasste und bestätigte Hinweise. Vollständiger
Aufgabentext und Quellliste erscheinen unter der Auswahl. Aufgabe öffnen,
Erinnerung verschieben, Aufgabe erledigen und Hinweis bestätigen sind getrennte
Aktionen. Bestätigen erledigt die Aufgabe nicht. Ein Aufschub ändert keine Frist.
**Aufgabe öffnen** schließt die Übersicht, hebt eine aktive Suche auf, wechselt in
die Quellliste und markiert die Aufgabe samt aufgeklappter Elternebenen.

Die App prüft alle 15 Sekunden; beim Start erstmals nach einer Sekunde.
Offene Bearbeitungsdialoge werden nicht unterbrochen; nach deren Schließen
folgt die Prüfung im nächsten Intervall. Die Erinnerungsübersicht selbst
aktualisiert sich alle 15 Sekunden. Mehrere verpasste Termine bleiben eine
gemeinsame Übersicht und führen nicht zu einer Kette modaler Meldungen.

Bei einer neu zugestellten Erinnerung hebt Glide seinen Eintrag in der
Taskleiste beziehungsweise im Dock hervor – einmal je Prüflauf, nicht je
Aufgabe, und erst nach gespeichertem Zustellbeleg. Das Fenster kommt dabei
nicht ungefragt nach vorn und nimmt keinen Fokus. Der Schalter **Bei fälliger
Erinnerung Taskleiste bzw. Dock hervorheben** in den persönlichen Einstellungen
schaltet das ab; er steht standardmäßig an. Trägt die Plattform den Aufruf
nicht, bleibt der Hinweis trotzdem in der Übersicht offen.

**Betriebsgrenze:** Hinweise sind Anzeigen innerhalb von Glide. Das Programm
muss laufen. Ein minimiertes oder verdecktes Fenster erzeugt weiterhin **keine
Systembenachrichtigung** – die setzt eine installierte, beim Betriebssystem
registrierte Anwendung voraus und gehört zur Paketierung
([Entscheidung](../decisions/SYSTEMBENACHRICHTIGUNGEN.md)). Bei beendetem Programm,
Abmeldung, Ruhezustand oder ausgeschaltetem Gerät erfolgt keine Zustellung;
nach Rückkehr zur laufenden App bzw. Neustart werden vergangene Zeitpunkte
gesammelt angezeigt. Es gibt keinen Hilfsprozess, Autostart, Internetzugriff
oder neue Laufzeitabhängigkeit.

## Zeit- und Wiederholungsvertrag

- Feste Eingaben werden aus der aktuellen lokalen Zeitzone nach UTC umgerechnet.
  Sie behalten bei Zeitzonen- und Fälligkeitsänderungen denselben Zeitpunkt.
- Relative Hinweise werden von der aktuellen Fälligkeit in der lokalen Zeitzone
  abgeleitet. Ohne Fälligkeitsuhrzeit gilt sichtbar 09:00 Uhr. Abstände sind
  verstrichene Minuten; ein Tag bedeutet 24 Stunden, auch über Zeitumstellungen.
- Eine doppelte Herbststunde verwendet den ersten Zeitpunkt. Eine nicht
  existierende feste Eingabe in der Frühlingslücke wird zurückgewiesen. Eine
  vorhandene relative Frist in dieser Lücke wird um die Lücke nach vorn gerechnet.
- Eine relative Erinnerung ohne Fälligkeit ist inaktiv. Bei neuer Fälligkeit
  berechnet sie sich neu. Ein Aufschub gehört zum bisherigen Vorkommen und
  verfällt bei dessen Terminänderung; feste Erinnerungen bleiben unabhängig.
- Relative Erinnerungen folgen der bestehenden Serienlogik. Nach Abschluss
  gehört der Hinweis zum nächsten Vorkommen, ohne alten Aufschub/Zustellstatus.
  Feste einmalige Erinnerungen werden beim Vorrücken der Serie entfernt.
- Erledigte Aufgaben und Papierkorbinhalte lösen nichts aus. Wiederherstellung
  aktiviert offene Aufgaben mit ihrer Konfiguration und vorhandenen Zustellbelegen
  wieder. Alte unzugestellte Zeitpunkte erscheinen gesammelt als offen/verpasst.

## Daten, Migration und Fehler

Format 13 ergänzt pro Punkt `reminder: null` oder ein Objekt. Alte Formate
werden additiv normalisiert. Vor dem ersten Überschreiben einer älteren Datei
entsteht `backups/liste_vor_format13_<Zeitstempel>.json` mit ihren Originalbytes;
schlägt diese Sicherung fehl, wird nicht gespeichert. Die Kopie wird nicht rotiert.
Ältere App-Versionen können Format 13 nicht lesen; deshalb vor einem Rückwechsel
die gesicherte alte Datenablage in einem getrennten Ordner verwenden.

Die Konfiguration enthält `mode` und entweder `at` (UTC mit Offset) oder
`minutes`. `snoozed_until`/`snoozed_for`, `delivered_key`/`delivered_at` und
`acknowledged_key` ordnen Aufschub, Zustellung und Bestätigung einem konkreten
Vorkommen zu. Die stabile Identität vermeidet erneute Zustellung nach Neustart
oder Zeitzonenwechsel. Bestehende Undo-Stände erhalten denselben Zustellbeleg.
Die Anzeige offener Hinweise bleibt bis zur Bearbeitung/Bestätigung erreichbar.

Zustellmetadaten werden atomar gespeichert, bevor eine Zustellung als verarbeitet
gilt. Bei Speicherfehler wird der Beleg zurückgenommen und die Statuszeile meldet
das Problem; ein späterer Prüflauf versucht es erneut. Bei bekannter Fremdbelegung
pausiert die Verarbeitung. Hintergrundzustellung erzeugt weder Undo-Einträge
noch Bearbeitungs-/Erledigungsstatistiken. Benutzeraktionen nutzen `item_change`.

Voll-/Teilbackups erhalten Konfiguration, Aufschub und Zustellstatus; ein Restore
hat weiterhin eine vollständige Sicherung des vorherigen Bestands. Neue Kopien,
ergänzende Importe und verwendete Vorlagen bekommen neue Aufgabenidentitäten
und frische Zustellzustände. Feste Vorlagenzeitpunkte bleiben fest, relative
Erinnerungen folgen den verschobenen Vorlagenfristen. Die äußere Vorlagenversion
bleibt 2, ihre Teilpayloads tragen das Aufgabenformat. Persönliche Einstellungen
und der Vorlagenkatalog sind weiterhin nicht Teil eines Aufgabenbackups.

## Prüfung und verbleibende Arbeit

`tests/integration/test_reminders.py` prüft Migration mit verweigerter Sicherung,
einmalige Zustellung, Aufschub/Neustart, Fälligkeitsänderung, Serienabschluss aus
fremden Listen, Bestätigung, Papierkorb, 25 verpasste Hinweise, Backup-Rundlauf,
Speicherfehler, Schreibschutz, Uhrumstellung, Zeitzonenwechsel, das Aufheben einer
aktiven Suche beim Öffnen einer Aufgabe und echte Tk-Dialoge in Hell/Dunkel.
Für die Aufmerksamkeit wird geprüft: ein Anstoß bei zwei gleichzeitig fälligen
Hinweisen, keiner ohne neue Zustellung, keiner bei offenem modalem Dialog,
keiner nach Speicherfehler, Wirksamkeit des Schalters über das Speichern hinweg
und dass die Plattformermittlung auf der Prüfmaschine nicht wirft. Der vollständige Prüflauf umfasst zwölf Suiten und zwei Analysen.

Aktueller Prüfstatus und Rohprotokolle: [QA-Bericht](../07_QA_BERICHT.md).
Der vollständige unveränderte 3.7-Ausgangslauf liegt unter
`tests/qa-3.7.0/erinnerungen/ausgang/ergebnis.json`.

Offen bleiben native Sichtabnahme, physischer Ruhezustand/Trackpad, weitere DPI
und Monitore, Screenreader, Langzeitbetrieb sowie ein echter Windows-Systemlauf.
Automatisierte Zeit- und Widgettests ersetzen diese Abnahmen nicht.

Nächste Ausbauschritte: Plattformintegration für Systembenachrichtigungen mit
klar definierten Betriebszuständen, danach Reiteransicht und Pinnwand. Welche
Zustellung in welchem Betriebszustand überhaupt möglich ist und warum ein
Hilfsprozess ausscheidet, steht in der
[Entscheidung zu Systembenachrichtigungen](../decisions/SYSTEMBENACHRICHTIGUNGEN.md). Mehrere
Hinweise je Aufgabe, Ruhezeiten und persönliche Erinnerungsstandards sind noch
nicht umgesetzt. Es wurden keine echten Nutzdaten zu Testzwecken geöffnet.
