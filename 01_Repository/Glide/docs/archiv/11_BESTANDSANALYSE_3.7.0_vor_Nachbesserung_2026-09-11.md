# Bestandsanalyse Glide 3.7.0

Stand: 07.09.2026 · App-Version 3.7.0 · Aufgabendatenformat 12

## Grundlage

Geprüft wurden der lokale Quellstand, die startbare äußere Kopie, die
3.7-Integrationssuiten, Werkzeuge, Fixtures, Dokumentation und die erzeugten
Windows-Bilder. Das Verzeichnis ist kein Git-Checkout; Aussagen über frühere
Historienstände werden deshalb nur aus vorhandenen Archiven übernommen.

## Ergebnis

Die ursprünglichen UI- und Funktionswünsche sowie die zusätzlichen
3.7-Anforderungen sind vollständig in
`docs/25_FEATURE_ABGLEICH_3.7.0.md` abgebildet. Umgesetzt und geprüft sind
unter anderem die volle Listen-/Ordner-Kachelansicht, Bearbeiten aus der
Kachel, zweispaltige Containerdetails mit Farbe/Labels/Anhängen, konsistente
Aktionsleisten, scrollbare Label- und Vorlagenbereiche, der Jahresraster-Hover
und die Schema-12-Migration mit Originalkopie.

Der vollständige Prüflauf vom 07.09.2026 endete mit Exitcode 0. Er umfasst zehn
Suiten, statische und Erreichbarkeitsanalyse, Fixture-/Release-Abgleich,
Dokumentationsindex und Screenshot-Erzeugung. Die Sichtprüfung der erzeugten
PNG-Bilder war erfolgreich.

## Daten- und Codegrenzen

- Containeranhänge werden bei Laden, Speichern, Backup, Import, Vorlage,
  Kopie, Papierkorb und Restore berücksichtigt; absolute oder unsichere Pfade
  werden abgewiesen.
- Punktverschiebungen, Kind-Anlage und Import halten
  `MAX_ITEM_DEPTH = 100` ein.
- Artwechsel mit bereits 20 normalen Labels wird geschützt abgebrochen; kein
  Label wird still entfernt.
- Sichtbare Symbole kommen zentral aus `ICONS` und werden mit der privaten
  DejaVu-Sans-Familie gemessen. Neue UI-Symbole bleiben textbasiert.
- Die Sperrdatei schützt vor parallelem Schreiben, ersetzt aber keine
  verteilte Synchronisation.

## Aktuelle Artefakte

- Feature- und Anforderungsabgleich: `docs/25_FEATURE_ABGLEICH_3.7.0.md`
- Versionsübersicht: `docs/24_VERSION_3.7.0.md`
- QA und maschinenlesbares Ergebnis: `docs/07_QA_BERICHT.md` und
  `tests/qa-3.7.0/automatisch/ergebnis.json`
- Hashnachweis: `tests/qa-3.7.0/abschluss-kontrolle.json`
- Oberflächenbilder: `tests/qa-3.7.0/oberflaeche/`

Die vorherige Bestandsanalyse bleibt unverändert unter
`docs/archiv/11_BESTANDSANALYSE_3.6.0_vor_3.7.0.md`.
