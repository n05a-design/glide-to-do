# Codebefund und bereinigte Grenzfälle – historischer 3.7-Befund

Dieses Dokument ist ein abgeschlossener Nachweis und wird nicht nachgezogen. Der aktuelle Stand steht im [Dokumentationsindex](00_INDEX.md) und im [QA-Bericht](07_QA_BERICHT.md). Die folgenden Befunde gehören zum jeweils angegebenen älteren Stand.

Der dokumentierte Befund stammt aus dem 3.7-Abgleich. Für den heutigen Bestand
gelten [Architektur](02_ARCHITECTURE.md), [Startkontext](03_STARTKONTEXT.md) und
der [QA-Bericht](07_QA_BERICHT.md).

Stand: 12.09.2026 · App-Version 3.7.0 · Aufgabendatenformat 12

Dieses Dokument beschreibt den damaligen Quellstand von 3.7.0.

## Aktueller Befund

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Der damalige kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

## Bereinigte Grenzfälle

| Grenzfall | Aktueller Umgang | Nachweis |
|---|---|---|
| Schemawechsel von 11 auf 12 | Migration erzeugt vor dem ersten Schreiben eine Originalkopie, ergänzt `attachments` und meldet den neuen Stand. | `load_items`, `save_items`, `tests/integration/test_release37.py` |
| Anhänge an Listen und Ordnern | Containeranhänge werden validiert, in Teilbackup/Import/Vorlage/Kopie/Papierkorb/Restore übernommen und auf sichere Pfade begrenzt. | `attachment_owners`, Release-37-Suite |
| Zu tiefe Unterbäume und zu viele normale Labels | Tiefen- und Labelgrenzen werden vor der Mutation geprüft; bei Ablehnung bleibt der Bestand unverändert. | `MAX_ITEM_DEPTH`, `set_item_kind`, Integritätssuiten |
| Scrollen in Kacheln, Labels, Vorlagen und Startseite | Bildlauf wird an den tatsächlich scrollbaren Bereich weitergereicht; am oberen und unteren Rand entsteht kein Leerraumscrollen. | Gemeinsamer Canvasbereich, `YearHeatmap`, Label-Dialog, UI-Screenshots |
| Tagesraster ohne Datumsbezug | Hover zeigt deutschen Wochentag, Datum und Bearbeitungszahl des Quadrats. | `YearHeatmap`, `tageshinweis-dark.png` |
| Gelöschte erledigte Aufgaben in der Statistik | Tageswerte werden aus den vorhandenen Aktivitätsdaten gelesen; das Löschen des Punkts entfernt den historischen Tageszähler nicht. | `record_recent_list_edits`, `test_release37.py` |

## Bewusst getrennte Grenzen

Ein echter Synchronisationsdienst, Konfliktzusammenführung, native macOS-
Abnahme, Mehrmonitor-/DPI-Matrix, Screenreaderprüfung, Langzeitmessung,
Installer, Signierung und Storefreigabe sind weiterhin separate Freigaben. Sie
werden in `docs/10_RELEASE_CHECKLIST.md` geführt und sind nicht als erledigte
Codebefunde zu lesen.

## Prüfpfad

```text
tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.7.0/automatisch
```

Das aktuelle [Ergebnis](../../../50_Ablage/QA/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json) und der [QA-Bericht](07_QA_BERICHT.md)
grenzen den automatisierten Nachweis von der manuellen Plattformabnahme ab.
