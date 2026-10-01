# Codebefund und bereinigte Grenzfälle – Glide 3.7.0

Stand: 07.09.2026 · App-Version 3.7.0 · Aufgabendatenformat 12

Dieses Dokument beschreibt den aktuellen, ausführbaren Windows-Stand. Die
vorherige Fassung 3.6.0 liegt unverändert unter
`docs/archiv/08_CODE_BEFUND_3.6.0_vor_3.7.0.md`.

## Aktueller Befund

Der Quellstand unter `src/glide/app.pyw` ist eine einzelne startbare Tk-Datei.
Der vollständige Windows-Prüflauf vom 07.09.2026 endete mit Exitcode 0; alle
zehn App-, Integritäts- und Audit-Suiten sowie Fixture-, Release- und
Screenshot-Schritte waren erfolgreich. Die aktuelle Oberfläche deckt die
Listen-/Ordner-Kachelansicht, Seitendetails, konsistente Aktionsleisten,
scrollbare Label- und Inhaltsbereiche, Jahresraster-Hover und die
personalisierte Akzentfarbe ab.

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

Das maschinenlesbare Ergebnis und die Hashnachweise liegen unter
`tests/qa-3.7.0/automatisch/` und `tests/qa-3.7.0/abschluss-kontrolle.json`.
