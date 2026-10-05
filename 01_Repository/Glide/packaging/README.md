# Paketierung Glide

Stand 05.10.2026 · Glide 3.33.8 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Der aktuelle Stand ist eine geprüfte Python-Anwendung mit Ressourcen. Ein Installer, eine Signatur oder eine Store-Abnahme wird hier nicht behauptet; offene Schritte stehen in der [Veröffentlichung](../docs/10_VEROEFFENTLICHUNG.md).

## Inhalt eines Pakets

`src/glide/app.pyw` mit allen Modulen daneben – `glide_start.py`, `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py`, `image_preview.py`, `logo.py`, `schema_backups.py`, `sidebar_policy.py`, `svg_geometry.py`, `home_tiles.py`, `capture_parser.py`, `eisenhower.py`, `today_view.py`, `content_search.py` (Aufgaben siehe [Modulübersicht](../src/glide/README.md)) –, der vollständige Ordner `resources` (Schriften mit Lizenztexten, Vorlagen, Logo) und `vendor/tkinterdnd2` nur mit den Bibliotheken der Zielplattform, samt Lizenzen. Die Bedienprobe `drawing_prototype.pyw` gehört nicht hinein. Daten werden nie in den Installationsordner geschrieben.

## Kennungen (26.09.2026, nie ändern)

- macOS: `de.shaye.glide` (`APP_BUNDLE_ID`)
- Windows: `Shaye.Glide` (`APP_USER_MODEL_ID`)

Eingetragen im [Produktregister](../docs/decisions/PRODUCT_IDENTITY.md).

## Werkzeuge

**Programmsymbole – [`baue_symbole.py`](baue_symbole.py):** erzeugt mit Tk 9 aus `src/glide/resources/logo/glide-app-icon.svg` (Kopie von `20_Grafik_Master/03_Fav-Icon/App-Icon-transparent-02.svg`) unter `assets/icons/` die Dateien `glide.ico` (Windows, 16–256 px), `glide_macos_1024.png` (macOS, mit Apples Rand) und `glide_512.png` (Linux, Stores).

**macOS-Entwicklungsbundle – [`macos/baue_app.py`](macos/baue_app.py):**

```
python3 -B packaging/baue_symbole.py
python3 -B packaging/macos/baue_app.py --ziel build/macos [--symbol anderes_1024.png]
```

Baut `Glide.app` mit Quellen und Modulen (Start über `glide_start.py`), Ressourcen, dem macOS-Teil von `vendor/tkinterdnd2`, einer Kopie des Python-Starters aus dem installierten python.org-Framework, `Glide.icns` und Ad-hoc-Signatur. macOS führt den Prozess als „Glide“ mit `de.shaye.glide`. Das Bundle braucht das installierte Python mit Tk und ist nicht zur Weitergabe gedacht.

**Windows-Verknüpfung – [`windows/verknuepfung_anlegen.ps1`](windows/verknuepfung_anlegen.ps1):** legt im Startmenü „Glide“ an (pythonw.exe mit `app.pyw`, Symbol `glide.ico`) mit der AppUserModelID; kein Adminrecht, keine Registry. Glide meldet sich beim Start mit derselben Kennung an (`set_windows_app_user_model_id`). Unter Windows noch nicht ausgeführt.

Geprüft wird die Vorstufe von `tests/integration/test_paketierung330.py`. Der Release-Build mit eingebettetem Python (D15), Developer-ID-Signatur, Notarisierung und Installer bleibt offen.
