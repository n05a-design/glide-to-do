# Bestandsanalyse Glide 3.6.0

Stand: 06.09.2026 · App-Version 3.6.0 · Aufgabendatenformat 11

## Grundlage

Geprüft wurden der lokale Quellstand, die startbare äußere Kopie, die
3.6-Integrationssuiten, Werkzeuge, Fixtures, Dokumentation und die erzeugten
Windows-Bilder. Die Übergabe aus dem vorherigen Bearbeitungsstand ist eine
Referenz; bei Widersprüchen gilt der aktuelle Code. Das Verzeichnis ist kein
Git-Checkout, daher werden keine nicht belegbaren Historienaussagen ergänzt.

## Ergebnis

Die ursprüngliche 3.6-Arbeitsliste ist vollständig in
`docs/20_FEATURE_ABGLEICH_3.6.0.md` abgebildet. Implementiert und geprüft sind
unter anderem die zweispaltige Seitenleiste, Startseiten-/Materialoptik,
farbige Auswahlfelder, vollständige Listen-/Ordneranlage, TTF-Registrierung,
Datenordner und Sperrdatei, verzögertes Umbenennen, Vorlagenkatalog,
verlustarme Teilbackups, Mondphase, Jahresraster und Personalisierung.

Der vollständige Prüflauf vom 06.09.2026 endete mit Exitcode 0: 20 Schritte,
keine fehlgeschlagene Stufe, eine bewusst separate Sichtprüfung. Die sieben
App-/Audit-Suiten, statische und Erreichbarkeitsanalyse, Fixture-/Release-
Abgleich, Dokumentationsindex und Screenshot-Erzeugung waren erfolgreich.

## Daten- und Codegrenzen

- Punktverschiebungen, Kind-Anlage und Import halten `MAX_ITEM_DEPTH = 100`
  ein; ein zu tiefer Unterbaum wird vor der Mutation abgewiesen.
- Artwechsel mit bereits 20 normalen Labels wird geschützt abgebrochen; kein
  Label wird still entfernt.
- Sichtbare Symbole kommen zentral aus `ICONS` und werden mit der privaten
  DejaVu-Sans-Familie gemessen. Legacy-Emoji werden höchstens beim Parsen alter
  Eingaben toleriert.
- Teilbackups validieren Archivpfade, Größen, Datenformat, Anhänge und IDs vor
  dem Import. Der Import ergänzt den Bestand und ersetzt ihn nicht.
- Die Sperrdatei warnt bei einem fremden aktiven Rechner und versetzt die App in
  Schreibschutz. Sie kann keine verteilte Zusammenführung leisten.

## Aktuelle Artefakte

- QA und maschinenlesbare Ergebnisse: `docs/18_QA_3.6.0.md` und
  `tests/qa-3.6.0/abschluss/ergebnis.json`
- vollständiger Funktionsabgleich: `docs/20_FEATURE_ABGLEICH_3.6.0.md`
- Glasoberfläche: `docs/19_GLASS_SURFACE_3.6.0.md`
- Messwerte: `docs/21_LEISTUNGSBERICHT_3.6.0.md`
- Hashnachweis: `tests/qa-3.6.0/abschluss/dateien.sha256.json`

Historische Bestandsanalysen und Vorprüfungen bleiben unter `docs/archiv/` als
unveränderte Nachweise erhalten. Sie sind nicht als aktueller Fehlerstatus zu
lesen.
