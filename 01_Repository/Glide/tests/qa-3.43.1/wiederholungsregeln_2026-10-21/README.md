# FP-02 – beide Ausbaustufen im lokalen Kandidaten

Stand 21.10.2026 · Glide 3.43.1 · Aufgabenformat 26 · Einstellungen 2

Das Paket umfasst jetzt zusammenhängend:

- Wochenintervalle mit mehreren Tagen, Monats-/Jahresintervalle, n-ten/letzten Wochentag, letzten Monatstag und letzten Werktag (Mo–Fr, ohne Feiertage).
- Bis zu fünf Folgetermine als Vorschau in Punktmaske und Inspektor.
- Folgetermine ab Fälligkeit oder tatsächlichem Erledigungstag.
- Pause/Wiederaufnahme sowie 1–10.000 verbleibende Vorkommen einschließlich des aktuellen; sichtbarer Rest und Ende nach dem letzten Abschluss.
- Deutsche Schnelleingabe mit erstem Termin und rücknehmbarem Chip, etwa „alle 3 Monate am 15.“, „jeden zweiten Dienstag im Monat“ und „drei Tage nach Erledigung insgesamt 3 Termine“.
- Statische Kalender-RRULEs mit Intervall, Monatsposition und wirksamer Anzahl/Ende, passender Import und vollständiger App-Sicherungsrundweg.

[Bedienung](../../../docs/20_FUNKTIONEN.md#erweiterte-wiederholungsrhythmen-fp-02-3440), [Datenvertrag](../../../docs/06_DATA_BACKUP_MIGRATION.md#format-26-fp-02-seit-3440).

## Gebündelte Prüfung

73 passende Fachtests und zwölf App-/UI-Fälle bestanden. Dazu der bisherige Wiederholungseinstieg und die zwei betroffenen Einstellungs-Altleserproben einschließlich 30 alter Filterkombinationen. Normale/große Schrift, echte Auswahl- und Knopfkommandos, Pausenwirkung, Restverbrauch, letztes Vorkommen, Undo/Redo, Neustart, Vorsicherung/Kopierfehler und tatsächlicher ausgelieferter Altleser sind einbezogen. 30 unabhängige Kalenderreferenzen umfassen 720 Folgetermine; der neue Kalender-Rundweg wird dagegen verglichen. [Paketbilanz](abschluss.json), [Appfälle](gezielt.json), [Aufrufbilanz](pruefaufrufe.json), [Kandidatenmanifest](quellstand.json), [hashgeprüfte Sicherung](kandidat_sicherung.json).

Auf die ausdrückliche Rückmeldung „Du prüfst und testest zu viel“ wurden beide Stufen gebündelt und weitere breite Zwischenläufe zurückgestellt. Es gibt für diesen Gesamtstand keine neue breite CI oder vollständige 101-Suiten-Matrix. Der frühere 99-Suiten-Lauf und die spätere FP-03-CI bleiben Nachweise ihrer jeweiligen Vorgängerstände. App-Version und Lieferung folgen D51 am Phasenende; das zwingende Format-26-Tor ist bereits aktiv.

Die älteren Zwischenproben bleiben getrennt erhalten. Ein früher Maskentest rief zunächst den regulären Inspektor statt des Maskendialogs auf. Eine Negativprobe schloss danach die fehlende Formatprüfung im direkten Ladeweg. Die Hauptsuite erwartete zunächst vom unveränderten Lieferfixture das neue Format; diese Erwartung trennt nun Lieferfixture 25 und aktuelle Schreibvorgänge 26. Die zwischenzeitlichen FP-03-Altleser-Zeitüberschreitungen stammten von der echten Rückstufungswarnung nach Zurücksetzen des künstlichen Datenfixtures: Die Probe setzt jetzt auch dessen Test-Marker zurück. Die Warnung im Produkt bleibt unverändert; beide betroffenen Proben sind grün. Historische rote Läufe werden nicht rückwirkend als grün bezeichnet.

## Grenzen und Schutz

Die sechs alten Regeln behalten ohne aktivierte Zusätze ihre bisherigen Felder und Rechenschritte. Neue Regeln und Steuerfelder sind durch Aufgabenformat 26, bytegleiche Vorsicherung und Altleser-Schreibschutz abgesichert. `rest` zählt einschließlich des aktuellen Termins; Überspringen verbraucht Vorkommen ohne Erledigungsbuchung. Bei Pause entstehen keine Folgetermine; die aktuelle Aufgabe und Erinnerung bleiben erhalten. Dynamische Erledigungsregeln und pausierte bzw. nicht zu DTSTART passende Regeln werden im Kalender nicht angenähert; der Exporttext benennt die Grenze. TXT und vollständige App-Sicherung erhalten die Zusatzwerte. CSV bleibt hinsichtlich vollständiger Serien begrenzt.

Keine neue Python-/Paketlieferung oder native Menschenabnahme. Die Prüfungen verwenden ausschließlich künstliche temporäre Daten. Rohlogs und lokale Orchestrierung bleiben ignoriert.
