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
| Abschlusslauf | wird nach erneutem Einfrieren mit diesem README ergänzt | `quellstand_abschluss.json`, `vollpruefung_abschluss.json` |

Rohprotokolle (`*.log`) bleiben lokal. Die Prüfungen laufen auf einer Kopie außerhalb der synchronisierten Ablage; maßgeblich ist das jeweilige Quellmanifest mit SHA-256 aller eingefrorenen Dateien.

## Grenzen

Keine Mac-Vollprüfung, kein Bundle- oder Paketneubau, keine native Linux-/Mac-Matrix, keine Screenreader-, DPI- oder Menschenabnahme. Linux/Tk 8.6 nur über die CI-Grundstufe und den GitHub-Lauf nach dem Push.
