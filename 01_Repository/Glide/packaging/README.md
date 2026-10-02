# Paketierung Glide

Stand 02.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Der aktuelle Stand ist eine geprüfte Python-Anwendung mit Ressourcen.
Ein Installer, eine Signatur oder eine Store-Abnahme wird hier nicht behauptet.

Ein Paket muss `src/glide/app.pyw`, seit 3.29.0 die Module `src/glide/drawing.py` und
`src/glide/drawing_image.py` sowie den vollständigen Ordner `src/glide/resources` (Schriften und Vorlagen) einschließlich
Lizenz enthalten. Die Bedienprobe `drawing_prototype.pyw` gehört nicht ins Paket. Private Registrierung verlangt keine systemweite Installation
der Schrift. Daten dürfen nicht in den Installationsordner geschrieben werden.

Vor der ersten Veröffentlichung: Anbieteridentitäten, Zielarchitektur,
Betriebssystemminimum, Signierung und Upgrade-/Deinstallationsverhalten anhand
eines echten Pakets festlegen und prüfen. Verbindliche Statusliste:
[Releasecheckliste](../docs/10_RELEASE_CHECKLIST.md).

## Kennungen und Entwicklungsbundle (26.09.2026)

Die Kennungen sind festgelegt und ändern sich nie mehr:

- `de.shaye.glide` für macOS;
- `Shaye.Glide` für Windows.

Sie stehen einmal im Code (`APP_BUNDLE_ID`, `APP_USER_MODEL_ID`) und im
[Produktregister](../docs/decisions/PRODUCT_IDENTITY.md).

**macOS – [`macos/baue_app.py`](macos/baue_app.py):**

```
python3 packaging/baue_symbole.py
python3 packaging/macos/baue_app.py --ziel build/macos [--symbol anderes_1024.png]
```

Baut `Glide.app` als Entwicklungsbundle:

- mit Quellen (einschließlich `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py` und dem Schnellstart
  `glide_start.py`, über den das Bundle startet), Ressourcen, dem macOS-Teil von
  `vendor/tkinterdnd2` (Ziehen aus dem Finder, seit 27.09.2026) und einer Kopie des Python-Starters aus dem
  installierten python.org-Framework;
- mit Ad-hoc-Signatur.

macOS führt den Prozess als „Glide“ mit der Kennung `de.shaye.glide`, geprüft
am 26.09.2026 mit getrenntem Datenordner. Das Bundle braucht das installierte
Python mit Tk und ist nicht zur Weitergabe gedacht.

**Programmsymbole – [`baue_symbole.py`](baue_symbole.py)** (29.09.2026): Aus
dem App-Symbol (`src/glide/resources/logo/glide-app-icon.svg`, Kopie von
`20_Grafik_Master/03_Fav-Icon/App-Icon-transparent-02.svg`) entstehen mit Tk 9 unter
`assets/icons/`:

- `glide.ico` für Windows (16 bis 256 px);
- `glide_macos_1024.png` für macOS, mit Apples Rand;
- `glide_512.png` für Linux und Stores.

`baue_app.py` macht aus der macOS-Datei `Glide.icns`; die Windows-Verknüpfung
nimmt `glide.ico`. Der frühere Platzhalter „G“ entfällt.

**Windows – [`windows/verknuepfung_anlegen.ps1`](windows/verknuepfung_anlegen.ps1):**

- Legt eine Startmenü-Verknüpfung „Glide“ an: pythonw.exe mit `app.pyw`.
- Die Verknüpfung trägt die AppUserModelID aus `app.pyw`.
- Kein Adminrecht, keine Registry.
- Glide meldet sich beim Start mit derselben Kennung an
  (`set_windows_app_user_model_id`).
- Unter Windows noch nicht ausgeführt.

Beides ist die Vorstufe für eigene Systembenachrichtigungen (Stufe B in
[SYSTEMBENACHRICHTIGUNGEN](../docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md)).
Der Release-Build mit eingebettetem Python, Developer-ID-Signatur,
Notarisierung und Installer bleibt offen (PyInstaller laut `requirements/`).
Geprüft wird die Vorstufe von `tests/integration/test_paketierung330.py`.


`schema_backups.py` bündelt die Tk-freie Formatsicherung mit Dateistandprüfung; seit 3.33.0 in beiden Lieferwegen enthalten.

`sidebar_policy.py` führt Zuordnung, Inhaltsgrenzen, Vorlagenprüfung und Geschwisterreihenfolge der vier Bereiche ohne Tk (3.33.1).

`svg_geometry.py` führt SVG-Pfade einschließlich verkürzter kubischer Kurven, CSS-/Attributfarben und transparente Innenkonturen ohne Tk (3.33.1).

`home_tiles.py` führt Kachelbestand, Startseiten-Standard (D12), Normalisierung, eigene Auswahl und die zusammengeführte Kachel „Heute“ ohne Tk (3.33.2).

`capture_parser.py` führt die deutsche Schnelleingabe (G01) ohne Tk: Bearbeitungstag, Fälligkeit, Uhrzeit, Aufwand, Wichtigkeit, Labels und „/“-Befehle nach D01/D10, jede Erkennung mit Textstelle zum Zurücknehmen (3.33.3).

`eisenhower.py` ordnet Aufgaben ohne Tk in die vier Quadranten „Dringlichkeit × Wichtigkeit“ ein und bestimmt, was Ablegen ändert (G02, D13; 3.33.5).

`today_view.py` teilt die Ansicht „Heute“ ohne Tk in nächste Aufgabe, Verspätet, Liegen geblieben, Tagesplan, Heute fällig und Eingang auf – jede Aufgabe genau einmal (D14; 3.33.6).
