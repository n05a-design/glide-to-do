# Paketierung Glide

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

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
python3 packaging/macos/baue_app.py --ziel build/macos [--symbol logo_1024.png]
```

Baut `Glide.app` als Entwicklungsbundle:

- mit Quellen, Ressourcen und einer Kopie des Python-Starters aus dem
  installierten python.org-Framework;
- mit Ad-hoc-Signatur.

macOS führt den Prozess als „Glide“ mit der Kennung `de.shaye.glide`, geprüft
am 26.09.2026 mit getrenntem Datenordner. Das Bundle braucht das installierte
Python mit Tk und ist nicht zur Weitergabe gedacht. Ohne `--symbol` entsteht
ein Pixel-„G“ als Platzhalter; das echte Logo liegt nur als Affinity-Datei
vor.

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

