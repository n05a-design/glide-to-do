# Prüfungen für Glide 3.7.0

Stand: 08.09.2026. Tests setzen vor dem App-Import `GLIDE_DATA_DIR` auf ihre
eigene Ablage. Niemals mit echten Aufgaben experimentieren.

## Vollständiger Windows-Lauf

```powershell
C:\Python312\python.exe tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.7.0/automatisch
```

Zehn Suiten: `test_glide`, `test_datenintegritaet`, `audit_app`,
`test_dialog_theme`, `test_ui_updates`, `test_glide_36`,
`test_release36`, `test_ui_polish36`, `test_ui_followup36`, `test_release37`. Ergänzt werden Syntax, Version, Dokumentationsindex,
Fixtures, statische Analyse, Erreichbarkeitsanalyse und beide Daten-Erzeuger.

Der End-to-End-Test prüft echte Archiv-/Dateirundläufe, Vorlagen bearbeiten und
speichern, Anlegemaske, Schriften, Umbenennen, Label-/Tiefengrenzen, Kalenderbeginn
und Datenordner. `--screenshots PFAD` erzeugt zusätzliche Windows-Bilder.

Aktuelle Nachweise: [QA 3.7](../docs/07_QA_BERICHT.md).
Historische 3.5-Ausgangsprüfung bleibt in `qa-3.6.0/ausgang-3.5.0`.
Der Name dieses Ordners macht seinen Inhalt nicht zu einer 3.6-Prüfung.

UI-Nachbesserung gezielt prüfen und aufnehmen:

```powershell
C:\Python312\python.exe tests/integration/test_ui_polish36.py --screenshots tests/qa-3.6.0/ui-nachbesserung/screenshots
```

Weiterer UI-Nachtrag (Kachelübersicht, Vorlagenbreite und Tageshistorien):

```powershell
C:\Python312\python.exe tests/integration/test_ui_followup36.py --screenshots tests/qa-3.6.0/vorlagen-jahresanzeige/screenshots
```

## Ergänzungen 3.7

`test_release37.py` prüft Schema-12-Originalkopie, Containeranhänge in allen
Dateirundläufen, Statistik nach Löschen, zweispaltige Seitendetails, Label- und
Diagrammscrollen sowie Tageshover. Aktuelle Bilder liegen in
`tests/qa-3.7.0/oberflaeche/`. Die oben genannten 3.6-Bildpfade sind historische
Nachweise; die Tests selbst laufen weiterhin im aktuellen Prüflauf.
