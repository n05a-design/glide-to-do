# Phasenabschluss 3.44.0 – Versionswechsel, eingefrorene Vollprüfung und Lieferung

Stand 22.10.2026 · Glide 3.44.0 · Aufgabenformat 26 · Windows 11, Python 3.14.7 / Tk 9.0.4, künstliche Daten

Auftrag des Inhabers vom 22.10.2026 (Wortlaut in der [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md)): Stand prüfen, Dokumentation, Roadmap, Aufgaben und Version aufarbeiten, `07_Python-Versionen` aktualisieren und den finalen Stand auf GitHub pushen und zusammenführen. Ausgelegt als D51-Phasenende; Aufgabenstand und nächste Schritte im [Entwicklungsplan §21.10](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2110-phasenabschluss-3440).

## Ablauf

| Schritt | Ergebnis | Beleg |
|---|---|---|
| Ausgangsstand | Zweig `codex/bildvorschauen-wa26-2026-10-18`, HEAD `1042727` = GitHub-`main`; Featurearbeit seit PR #37 uncommittet (77 geänderte versionierte Dateien, 42 unversionierte Einträge mit 361 Dateien). 07 = 3.43.1 / Format 25 mit 23 Abweichungen zur Quelle ([Vorinventar](../../qa-3.43.1/dokumentationsaudit_2026-10-22/README.md)) | Commit `5e915a7` sichert den Kandidaten unverändert |
| Baseline | 856 Fachtests grün (App `604014f9…`) | lokale Konsole |
| Versionswechsel | `versionswechsel.py 3.44.0 22.10.2026`; Fixtures mit Format 26, Releaseplanung 3.44.0, 42 Standangaben, Aufbewahrung kürzt 3.39.0; CHANGELOG und Neuerungskatalog | Commit `d17675e` |
| Vorlauf 01 | eingefroren, App `d0bf4142…`, 2.514 Dateien: 120 Schritte, 109 grün, 10 rot, 1 Sichtprüfung übersprungen | [Ergebnis](vollpruefung_vorlauf01.json), [Quellmanifest](quellstand_vorlauf01.json) |
| Korrekturen | ein Produktfehler (Aktionskatalog), Prüferwartungen Format 26/FP-02-ICS, Sperrdatei im Markdown-Bytevergleich, Showcase-Serie; `test_ui39` nicht reproduzierbar (3/3 grün) | [Ursachen und Nachprüfung](gezielte_nachpruefung.json), Commit `3ca7f09` |
| Vorlauf 02 | nach wenigen Sekunden abgebrochen: Die Dokumentationsprüfung meldete Verweise des QA-Berichts auf dieses noch nicht angelegte README. Reine Reihenfolge der Dokumentarbeit, keine Code- oder Suiteänderung | – |
| Lauf 03 | eingefroren auf `3ca7f09` (App `d0bf4142…`, 2.519 Dateien): 120 Schritte, 117 grün, 2 rot, 1 Sichtprüfung übersprungen. Alle zehn Vorlaufbefunde behoben; rot nur `test_speicherlast330` (nativer Absturz 0xC0000005 ohne Log) und der Matrixfall „einplanen“ in `test_wiederholen`. Einzeln 2/2 bzw. 10/10 und 3/3 unter Fokusentzug grün, Ursache nicht belegt | [Ergebnis](vollpruefung_lauf03.json), [Quellmanifest](quellstand_lauf03.json), [Nachprüfung](nachpruefung_lauf03.json) |
| Lauf 04 | eingefroren auf `aa8313b` (Matrix-Assertion mit Diagnose, App unverändert `d0bf4142…`), `PYTHONFAULTHANDLER=1`: 120 Schritte, 117 grün, 2 rot, 1 übersprungen. `test_wiederholen` grün; rot `test_hintergrund330` (Hintergrundverlauf nach 60 s nicht fertig, `backdrop` seit `1042727` unverändert) und erneut `test_speicherlast330`: `save_items` scheitert in Runde 1 mit `name 'isinstance' is not defined`. Einzeln und dreifach parallel 3/3 grün; keine Restprozesse, kein Ereignisprotokolleintrag. Ursache nicht belegt, offener Befund WA-41 | [Ergebnis](vollpruefung_lauf04.json), [Quellmanifest](quellstand_lauf04.json) |
| Lauf 05 | unveränderte Bytes, erneut eingefroren; nach 16 von 120 Schritten abgebrochen. Der Inhaber arbeitete am Rechner; `test_release36` scheiterte, weil der Inline-Editor beim Verlust des Vordergrunds schloss (WA-42). Fokusabhängige Ergebnisse unter Desktopbedienung sind nicht aussagekräftig, und die Prüffenster störten die Arbeit | [Quellmanifest](quellstand_lauf05.json) |
| Lieferung | `abgleich_07.py` 79 Code-Dateien und 147 Ressourcen ohne Abweichung (App `d0bf4142…`), Showcase über Import/Neustart abgeglichen; 3.43.1 ins Archiv, 3.39.0 entfallen | [Lieferbeleg](lieferung.json), Commit `71854ec` (lokal) |
| CI-Grundstufe streng | 22.10.2026, 21:16 Uhr, Windows/Python 3.14.7: Exitcode 0, 19 Schritte ausgeführt, Lieferstand bytegleich | [Ergebnis](ci_grundstufe_streng.json) |
| Git/GitHub | PR #38 mit `5e915a7`, `d17675e`, `3ca7f09` als `2ac339e` in `main` zusammengeführt. GitHub-Prüfung #140 auf dem Merge rot im Job „Vollprüfung (Windows x64, eigene Tk 9.1)“, Grundstufe mit Hinweis auf 25 Lieferabweichungen, weil `aa8313b`/`71854ec` nicht gepusht sind. Nach Entscheidung des Inhabers vom 23.10.2026 kein weiterer Push | öffentliche Actions-Ansicht, 23.10.2026 |

Rohprotokolle (`*.log`) bleiben lokal. Die Prüfungen laufen auf einer Kopie außerhalb der synchronisierten Ablage; maßgeblich ist das jeweilige Quellmanifest mit SHA-256 aller eingefrorenen Dateien.

## Grenzen

Keine Mac-Vollprüfung, kein Bundle- oder Paketneubau, keine native Linux-/Mac-Matrix, keine Screenreader-, DPI- oder Menschenabnahme. Linux/Tk 8.6 nur über die CI-Grundstufe und den GitHub-Lauf nach dem Merge. **Ergebnis:** Die Phase ist versioniert und als Python-Fassung geliefert, ihre eingefrorene Windows-Vollprüfung aber nicht vollständig grün (WA-41/WA-42 offen).
