# Glide – Weitergabe an einen neuen Chat

Stand 23.09.2026 · Version 3.28.0 · Aufgabenformat 18 · Einstellungen 2 · Vorlagen 2

## Auftrag für den neuen Chat

Arbeite ab dem vorhandenen Stand weiter. Öffne zuerst `01_Repository/Glide/AGENTS.md`,
danach `01_Repository/Glide/docs/07_QA_BERICHT.md`,
`01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md` und
`01_Repository/Glide/docs/09_PROJECT_HANDOFF.md`. Bereits erledigte 3.28-
Funktionen nicht erneut als offen behandeln. Aussagen über Freigabe nur aus
aktuellen Prüfbelegen ableiten.

## Kanonische Pfade

| Zweck | Pfad |
|---|---|
| Kanonischer Quelltext | `01_Repository/Glide/src/glide/app.pyw` |
| Aktuelle Version | `01_Repository/Glide/VERSION` |
| Startbare Kopie | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.28.0.pyw` |
| Laufzeitressourcen | `01_Repository/Glide/src/glide/resources/` und `07_Python-Versionen/resources/` |
| Dokumentationsindex | `01_Repository/Glide/docs/00_INDEX.md` |
| QA-Bericht | `01_Repository/Glide/docs/07_QA_BERICHT.md` |
| Daten und Migration | `01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md` |
| Releasecheckliste | `01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md` |
| 3.28-Funktionstest | `01_Repository/Glide/tests/integration/test_features328.py` |
| Aktuelle Probedaten | `05_Probelisten_Testdaten/*_3.28.0.*` |
| Archivierungsmanifest | `00_Arbeitsvorbereitung/Umsetzung_3.28.0/archivierung_manifest.json` |

Der äußere Arbeitsordner ist kein Git-Checkout. Änderungen deshalb über
Dateien, Prüfsummen, Tests und Archivmanifest nachweisen.

## Umgesetzter Stand 3.28

- Der undokumentierte 3.27-UI-/UX-Stand wurde in den kanonischen Quelltext
  übernommen und als startbare 3.27-Fassung archiviert.
- Tagebuchordner, datierte Notizseiten, Favorit, Stimmung, Ort, Momentdatum,
  Schreibimpulse, Suche und Sortierung sind implementiert.
- Vier Tagebuchvorlagen ergänzen 16 vollständige Praxisvorlagen.
- Aufgabenformat 18 ergänzt `folder_kind` und `journal`; vor der ersten
  Migration entsteht eine bytegleiche `liste_vor_format18_*.json`.
- Gismo besitzt Sättigung, Energie und Vertrauen sowie Füttern, Spielen und
  Ruhen. Die Werte bleiben lokal und bewerten nicht die Arbeitsleistung.
- Pinnwandvorschau, schmale Fenster, Menüschaltflächen, Notizwerkzeuge,
  Punktmaske, neutrale Aktionsfarben und Mausrad-Autoscroll wurden überarbeitet.
- Der weiße Neuaufbau nach einer Gismo-Pflegeaktion ist behoben. Ursache war
  ein vollständiges `refresh_home()` nach 900 ms. Jetzt werden nur die drei
  Balken und Gismos Zeichenzustand aktualisiert. Das Dopamin-Design war nicht
  die alleinige Ursache, machte den Neuaufbau aber deutlicher sichtbar.

## Forschung und Begründung der Flackerkorrektur

Tkinter arbeitet ereignisgetrieben und einthreadig; Darstellung und Geometrie
werden über die Ereignisschleife abgearbeitet. Tcl/Tk beschreibt Display- und
Layoutänderungen als Idle-/Zeichenarbeit. Windows löscht und zeichnet
invalidierte Bereiche über `WM_ERASEBKGND` und `WM_PAINT`. Daher wurde keine
Win32-Sonderbehandlung eingebaut, sondern die unnötige großflächige
Widgetzerstörung beseitigt. Quellen und genaue Ableitung stehen in Dokument 60.

## Verifizierter Stand

- Quelle und startbare Kopie: SHA-256
  `32037B74820E07600368EBF74D4991A4491A02860EDACA2F83D4AE7F5BBAC403`.
- Vorlagenkataloge: SHA-256
  `62A9DCF8F04E57724FC1CA9B05B8EB9DD187E9F1E9738ACB542AB32E36B80455`.
- Bestanden: Syntax, `test_features328.py`, `test_glide.py`,
  `test_template_workflows.py`, `test_features315.py`, Erreichbarkeits- und
  Attributprüfung. Die statische Analyse und Dublettenprüfung melden
  Wartungshinweise, keine neue Funktionsregression.
- Der neue Gismo-Test erzwingt das Dopamin-Design und weist nach, dass Füttern
  keinen Startseiten-Neuaufbau mehr anstößt.

## Bewusst offene Punkte

1. Die komplette QA ist noch nicht freigegeben. `test_ui_followup36.py` und
   der ältere Sammeltest überschritten im kurzen Lauf die Zeitgrenze.
2. Mehrere OneDrive-Platzhalter sind lokal nicht lesbar. Dazu gehören die alte
   Chat-Weitergabe vom 16.09.2026, drei 3.21.4-Probedateien, ältere Tests,
   Fixtures und Dokumente. Sie wurden nicht gelöscht oder überschrieben.
3. Die manuelle Prüfung von Gismo/Flackern mit echter Maus ist offen.
4. macOS, DPI/Mehrmonitor, Screenreader, Installer, Signierung, Notarisierung
   und reale Verteilung sind offen.
5. Storetexte beruhen auf historischer Recherche vom 04.09.2026 und müssen vor
   jeder Einreichung neu recherchiert werden.

## Erster nächster Schritt

Die im QA-Bericht benannten OneDrive-Dateien über „Immer auf diesem Gerät
behalten“ lokal verfügbar machen. Danach im Repository ausführen:

`C:\Python312\python.exe tests\tools\pruefen.py --modus voll --protokoll tests\qa-3.28.0\abschluss_final --timeout 900`

Anschließend `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.28.0.md`
abarbeiten. Erst wenn beide Nachweise vollständig sind, 3.28 als freigegeben
bezeichnen.

## Datensicherheit

Tests immer mit isoliertem `GLIDE_DATA_DIR`. Echte Nutzerdaten nicht als
Fixture öffnen. Alte Dateien nur in `Archiv`/`archiv` verschieben, nie löschen.
Format 18 nicht mit einer älteren Glide-Version schreibend öffnen. Eine
startbare Python-Datei ist noch kein Installer oder signiertes Release.
