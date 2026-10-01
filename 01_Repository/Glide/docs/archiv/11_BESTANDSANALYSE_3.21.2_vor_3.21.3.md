# Bestandsanalyse – historischer 3.7-Befund

Aktueller Entwicklungsstand: **3.21.0 / Aufgabenformat 15** mit Kalenderimport aus ICS. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md), [QA](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.

Diese datierte Analyse bleibt als Nachweis erhalten. Der aktuelle Bestand ist
Glide 3.21.0; maßgeblich sind [Startkontext](03_STARTKONTEXT.md),
[Projektübergabe](09_PROJECT_HANDOFF.md) und [QA-Bericht](07_QA_BERICHT.md).

Stand: 12.09.2026 · App-Version 3.7.0 · Aufgabendatenformat 12

## Grundlage und Ergebnis

Kanonischer Quellstand, startbare Kopie und Ressourcen, Integrationssuiten und
aktuelle Dokumentation wurden abgeglichen. Das Verzeichnis ist kein Git-Checkout.
Die [Funktionsmatrix](25_FEATURE_ABGLEICH_3.7.0.md) führt die Anforderungen weiter.

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Der aktuelle kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

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
  `tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json`
- Hashnachweis: `tests/qa-3.7.0/dynamische-kacheln/gepruefter_quellstand_sha256.json`
- Historische Oberflächenbilder (kein Nachweis des jüngsten UI-Stands): `tests/qa-3.7.0/oberflaeche/`

Die vorherige Bestandsanalyse bleibt unverändert unter
`docs/archiv/11_BESTANDSANALYSE_3.6.0_vor_3.7.0.md`.
