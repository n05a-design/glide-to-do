# Mein Tag – bewusste Tagesauswahl in Glide 3.12.0

Stand 13.09.2026 · Aufgabenformat 13 · Einstellungsformat 2

„Mein Tag“ ist eine freiwillige Tagesauswahl über mehrere vorhandene Listen.
Eine Aufgabe wird dabei nur referenziert: Titel, Beschreibung, Labels,
Fälligkeit, Wiederholung und Anhänge bleiben am ursprünglichen Punkt. Die
Auswahl ersetzt weder die Fälligkeit noch das Tagesziel für erledigte Aufgaben.

## Bedienung

- Die Ansicht „Mein Tag“ steht in der Seitenleiste, auf der Startseite und im
  Menü „Ansicht“.
- In einer Liste markierte Aufgaben lassen sich über das Kontextmenü mit
  „Für Mein Tag einplanen“ aufnehmen. Bei einer Mehrfachauswahl werden alle
  geeigneten Aufgaben gemeinsam übernommen.
- In „Mein Tag“ öffnet ein Doppelklick die Quellliste. Das Kontextmenü entfernt
  den Punkt aus der Tagesauswahl, ohne die Aufgabe zu löschen.
- Die Seitenleistenaktion „Mein Tag leeren“ entfernt alle Zuordnungen für den
  aktuellen Tag. Erledigen und Bearbeiten wirken weiterhin auf dasselbe
  Aufgabenobjekt in der Quellliste.

## Tageswechsel und Daten

Die Auswahl wird mit dem lokalen Datum gespeichert. Beim nächsten Kalendertag
beginnt „Mein Tag“ leer; die Aufgaben selbst und ihre Fälligkeiten bleiben
unverändert. Nicht mehr vorhandene oder nicht geeignete IDs werden beim Laden
oder Anzeigen still aus der Auswahl entfernt. Es werden keine Aufgaben kopiert
und keine parallelen Statusfelder im Aufgabenbackup eingeführt.

Die Einstellung liegt additiv als `today_plan` in `settings.json` und ist kein
Bestandteil eines Aufgabenbackups. Ein beschädigter oder fremder Eintrag wird
auf eine leere Auswahl zurückgeführt. Die Oberfläche bleibt vollständig lokal
und benötigt weder Konto noch Internet.

## Grenzen und Abnahme

Die Ansicht zeigt bewusst ausgewählte Aufgaben, keine automatische Priorisierung
und keine Kapazitätsplanung. Mehrere Tageslisten, Arbeitsaufwand, Abhängigkeiten
und Systembenachrichtigungen bleiben eigenständige spätere Funktionen.

Die Regression in `tests/integration/test_features312.py` prüft Auswahlreihenfolge,
listenübergreifende Objektidentität, unabhängige Fälligkeit, Persistenz und den
Schutz gegen entfernte sowie strukturelle Punkte.
