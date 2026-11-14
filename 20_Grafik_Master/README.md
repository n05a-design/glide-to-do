# Grafik-Master und zentrale Logo-Übersicht

Stand 14.11.2026 · Glide 3.61.0 · Aufgabenformat 26 · Einstellungen 2 · Vorlagen 2

Am 05.11.2026 zusammengeführt und gekürzt: alle aktiven Logo-Quellen, Verwendungen und künftigen Aktualisierungsschritte stehen hier. Frühere Logo-Dateien sind auf ausdrücklichen Benutzerauftrag im Grafikarchiv erhalten; diese Ausnahme betrifft Grafiken, keine zusätzlichen Dokumentarchive.

## Verbindliche Quellen (D80)

| Master unter `01_Logo/svg` | Verwendung |
|---|---|
| `Logo_Glide-01.svg` | Glide-Kopfzeile, Startanzeige und Produktinfo. Transparente Kontur mit eigenem Schattenpfad. |
| `Logo_Glide-03.svg` | Glide-App-Icon und Favicon. Auch für Paket und Repository-README. |
| `Logo_Steps-01.svg` | Steps-Master für die Verwendung innerhalb der künftigen Anwendung. |
| `Logo_Steps-03.svg` | Steps-Master für App-Icon und Favicon. |
| `Logo_Glide-02.svg`, `Logo_Steps-02.svg` | Weitere bereitgestellte Markenvarianten. |
| `01_Logo/Exporte/Logo_Glide-01.png`, `Logo_Glide-03.png` | Ableitungen für die Weitergabe als Rastergrafik. |

Die SVG-Kopien in den Laufzeitressourcen und das Favicon sind bytegleich zu den Mastern. Die App verwendet beim Einfärben den Akzent für die Fläche. Der separate Schatten erhält je nach Untergrund und Akzent eine dunkle, helle oder mittlere Blaustufe. Der statische Export mit Markenfarben erhält den Master-Schatten `#15243C`. Das App-Icon verwendet seine vollständige Zeichenfläche mit lila Außenrahmen und gelbem Innenfeld.

## Wo das Logo vorkommt und was bei Änderungen zu erneuern ist

App-Pfade ohne Projektpräfix beziehen sich auf `01_Repository/Glide`; die Grafik-/07-Pfade beziehen sich auf die Repository-Wurzel. **Dies ist die zentrale Änderungscheckliste für künftige Logo-Wechsel.**

| Anzeige / Verwendung | Besitzende Quelle / Ziel | Nötiger Schritt |
|---|---|---|
| Kopfzeile aller App-Ansichten | `src/glide/app.pyw`: `header_logo_color`, `sync_header_logo`, `draw_logo`; zentral `logo.py` | In-App-SVG und Größen-/Kontrastprüfung erneuern |
| Startfenster / Ladeanzeige | `app.pyw`: `show_start_window` | Kaltstart mit neuem Logo prüfen |
| „Über Glide“, Menüaufruf zur Produktinfo | `app.pyw`: `show_about_dialog` / `draw_logo` | Dialog öffnen; Fläche, Schatten und Proportionen auf hellem und dunklem Design prüfen |
| Fenster-Titelleiste, Alt-Tab / Fenstervorschau und geerbte Dialogsymbole | `apply_window_icon`, `logo.icon_photos` | Native SVG-Symbole und vorberechnete Größen 16/32/64/256 erneuern |
| Taskleiste / Dock / Systemmenü-Anzeige | Windows: EXE-Ressource plus AppUserModelID/Verknüpfung; macOS: Bundle-Icon und Bundle-ID | Eigenständige Pakete neu bauen; vorhandene Identitäten erhalten; echte Anzeige nach Neustart prüfen |
| Tray / Menüleisten-Symbol und Systemmitteilungen | `app_icon_photo(16)`, `system_notification_backend`, Windows-AppUserModelID und vorhandene Verknüpfung | 16-px-Symbol sowie tatsächliche native Zustellung/Anzeige prüfen |
| Aktive Laufzeit-SVGs | `01_Repository/Glide/src/glide/resources/logo/glide-{logo,app-icon}{,-klein}.svg` | Vier Kopien aus den zwei freigegebenen Mastern, keine Handkorrekturen |
| PNG-Rückfall und allgemeine Bilddateien | derselbe Ressourcenordner: `glide-logo.png`, `glide-app-icon.png`, `glide-app-icon[-macos]-{16,32,64,256}.png` | Aus den SVGs neu rasterisieren; Transparenz, Schatten und Icon-Rahmen prüfen |
| Windows EXE, Datei-Explorer, Desktop-/Startmenü-Verknüpfung und deren Vorschauen | `01_Repository/Glide/assets/icons/glide.ico`; `packaging/windows/verknuepfung_anlegen.ps1`; Paketbau | ICO mit 16/24/32/48/64/128/256 px neu erzeugen, EXE neu bauen, bestehende Verknüpfung auf neues Icon prüfen |
| Dateitypsymbole für `.glideapp`, `.glidebackup` usw. im Explorer/Finder | Betriebssystem-Zuordnung beziehungsweise künftiger Installer/Bundle-Dateitypvertrag | Vorhandene Zuordnung gesondert prüfen. Ein SVG-/PNG-Tausch registriert keinen Dateityp. Aktuell kein fertiger Dateizuordnungs-/Installervertrag; nicht als umgesetzt ausgeben |
| Finder-Vorschau, Dock und macOS-App-Menü / „Informationen“ | `assets/icons/glide_macos_1024.png` → `Glide.app/Contents/Resources/Glide.icns` und `Info.plist` | PNG mit bestehendem Apple-Rand, natives ICNS/Bundle neu bauen und signieren; Finder/Dock nativ prüfen |
| Linux-Programmstarter / Paket | `assets/icons/glide_512.png`, `packaging/paket` | Symbol neu erzeugen; beim nächsten nativen Paketbau übernehmen |
| Website-/Browser-Favicon und SVG-/PNG-Vorschauen | `20_Grafik_Master/03_Fav-Icon/favicon.svg`, `.ico`, `favicon-{16,32,64,256,512}.png` | Generator ausführen; bei tatsächlicher Webnutzung Deployment und Browsercache gesondert aktualisieren |
| Startbare Python-Lieferfassung | `07_Python-Versionen/logo.py`, `brand.py`, `svg_geometry.py`, Appdatei und `resources/logo` | `scripts/pflege/abgleich_07.py` ausführen und Hashgleichheit prüfen |
| Dokumentation / GitHub-README / Produktidentität | Root-README, `01_Repository/Glide/README.md`, `assets/marketing`, `docs/decisions/PRODUCT_IDENTITY.md`, Assets-/Paket-README | README-Symbol und Bildlinks prüfen. Reale Aufnahmen mit isoliertem Showcase erneuern und jede Ansicht einmal zeigen. |
| GitHub-Kartenvorschau | `assets/marketing/github-social-preview.png` und Repository → Settings → General → Social preview | Vorschau mit aktuellem App-Icon und neuer Leitaufnahme aktualisieren. 1280 × 640 px, unter 1 MB. Die README-Galerie wird über den Repository-Branch aktualisiert. |
| Projektseite und Demo | `assets/marketing/`, `tests/tools/projektseite_aufnahmen.py`, `05_Probelisten_Testdaten/Showcase/` | Ansichten mit dem aktuellen Build aufnehmen. Je Bild ein eigener Arbeitskontext. Alte Marketing-Bilder aus dem aktiven Ordner entfernen. |
| Bestehende native Lieferpakete und installierte Kopien | `build/windows`, `build/macos`, Downloads/Installationsziele | Nur durch neuen geprüften nativen Bau und bewusste Lieferung ersetzen; Ressourcen nicht nachträglich in signierte Pakete kopieren |
| Historische QA-Bilder, Originalreferenzen und alte Pakete | datierte Nachweise / Grafikarchiv | Als historische Belege unverändert lassen; nicht als aktuellen Logo-Stand verwenden |

Ein neues Icon kann trotz korrekter Dateien zeitweise aus Windows-/Finder-/Browsercaches angezeigt werden. Zuerst neuen Paket-/Dateihash und tatsächlichen Verknüpfungspfad prüfen; anschließend neu öffnen beziehungsweise neu anheften. Keine pauschale Cache-Löschung oder Explorer-Neustarts im laufenden Arbeitsbetrieb.

## Wiederverwendbarer Aktualisierungsablauf

Aus `01_Repository/Glide`, mit der geprüften Python-/Tk-9-Laufzeit:

```sh
python -B scripts/pflege/logo_abgleich.py
python -B scripts/pflege/logo_abgleich.py --pruefen
python -B scripts/pflege/abgleich_07.py
python -B tests/integration/test_logo330.py
python -B tests/integration/test_logo3370.py
```

`logo_abgleich.py` verteilt die Master unverändert, ruft `packaging/baue_symbole.py` auf und erneuert alle Laufzeit-PNGs, Paketsymbole, allgemeine PNG-Exporte und Favicons. `--pruefen` erzeugt Vergleichsdateien nur temporär und schlägt bei Abweichungen fehl. Zusätzliche PNGs müssen nicht manuell geliefert werden. Ändern sich die freigegebenen Farben, SVG-Stile oder Formen, auch `brand.py`, SVG-Leser und die echten Render-/Kontrasttests anpassen; keine Konturen aus Altdateien zurückholen.

Anschließend aktuelle Dokumentationsaufnahme/Verweise, Änderungsverlauf, Entwicklungsplan und QA-Nachweis fortschreiben. Windows und macOS mit `packaging/paket/baue_paket.py` beziehungsweise dem nativen Mac-Workflow neu bauen, Paketressourcen/PE beziehungsweise ICNS, Signatur und isolierten Start prüfen und erst danach die tatsächlichen Lieferziele ersetzen. Physische DPI-/Taskleisten-/Finderprüfung getrennt vom automatischen Rendernachweis bestätigen. Das Beispielarchiv bleibt erhalten; individuelle Nutzerbilder und Dokumentensymbole werden durch einen Markenwechsel nicht verändert.

**Übertragung nativer Pakete:** Einige Übertragungswerkzeuge ergänzen SVG-Metadaten (am 06.11. bei vier entpackten Paketdateien beobachtet). Deshalb native Pakete als vollständiges Originalarchiv übertragen und nach dem Entpacken gegen dessen Hashmanifest prüfen. Zusätzliche Metadaten dürfen nicht still in geprüfte Ressourcen gelangen; abweichende Dateien sichern und nur die nachweislich ursprünglichen Archivbytes wiederherstellen. Ein nachträglicher Ressourcentausch ist kein neuer Paketbau oder Signaturnachweis.

## Projektaufnahmen erneuern

In `01_Repository/Glide` unter Windows mit Python 3.14 und Tk 9:

```powershell
py -3.14 -B tests/tools/projektseite_aufnahmen.py --out assets/marketing
```

Das Werkzeug öffnet echte Ansichten und Dialoge aus einer separaten Kopie des Showcase. Das README verlinkt die aktuelle Galerie. Vor dem Ersetzen Motiv, Auflösung, Titelleiste, Schattenfarbe, Beschriftungen und Inhalt der jeweiligen Ansicht prüfen.

## Weitere Grafikquellen

`05_Inspiration` enthält historische Stilvorlagen und Entwurfsbelege. Sie sind keine aktuelle Logo-Quelle. Fremdbilder vor öffentlicher Veröffentlichung nach ihrer jeweiligen Lizenz prüfen.

`07_Fonts` enthält die unveränderten Originale und Lizenztexte für Rubik, Charis SIL, DM Serif Display und DM Mono. Die Runtime führt zusätzlich DejaVu Sans als internen Symbolbegleiter und Pixelify Sans für Pixel-Überschriften; Details im Schriftkatalog und Veröffentlichungsdokument.

Die vier Stock-Referenzen des [Showcase](../05_Probelisten_Testdaten/Showcase/README.md) stammen aus `06_Beispielbilder`. Die [Herkunftsdatei](../01_Repository/Glide/tests/fixtures/showcase/quellen.json) nennt die Originale und die Prüfsummen der für die Demo komprimierten Arbeitskopien. Frühere Logo- und Showcase-Stände sind in Git nachvollziehbar.
