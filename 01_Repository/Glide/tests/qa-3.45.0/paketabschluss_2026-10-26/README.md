# Aktualisierung aller Lieferungen und eigenständigen Pakete

Auftrag 26.10.2026: „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Der Auftrag erweitert die bisherige Featurephase um den tatsächlichen Liefer-/Paketabschluss.

## Bestand und Ziel

- Quelle: Glide 3.45.0 / Aufgabenformat 26, einschließlich WA-12, Verweisvorschau und Startseitenmodell. App `4244e610…`, Modell `ced120a5…`; 86 eigene Laufzeitdateien plus separater Prototyp. Gitbasis `4f101cd`, lokale Featureänderungen bleiben erhalten.
- Python-Lieferung vor Auftrag: 3.45.0, aber vier Laufzeitunterschiede zur Quelle; bisherige App `2e69d875…`.
- Windows-Paket vor Auftrag: `build/windows/Glide-3.42.0/Glide.exe`.
- Mac-Paket vor Auftrag: `build/macos/Glide.app`, Info.plist und Eingabemanifest 3.42.0; 327/330 historische Manifestdateien vorhanden, drei Python-Frameworkdateien fehlen in der Windows-Kopie.
- Werkzeuge gelesen: Arbeitsregeln, Übergabe/Plan, Paket-README, native Paketbauer, Lizenz-/Startverträge und Lieferabgleich. Keine Umbenennung alter Pakete als Ersatz für einen Neubau.
- Ziel: aktueller Quellstand bytegleich in Python-Lieferung und neu gebauten nativen Paketen; Code-, Versions-, Ressourcen-, Lizenz-, Start- und Hashprüfungen. Private Nutzerdaten bleiben außerhalb der Prüfungen; `GLIDE_DATA_DIR` zeigt vor jedem App-Import in einen temporären Ordner.

## Plattformen

Windows x64 mit Python 3.14.7 / Tcl-Tk 9.0.4 vorhanden. Neue isolierte Bauumgebung außerhalb OneDrive. Die strenge ACL-Sperrprobe bleibt auf vergängliche GitHub-Hosted-Runner beschränkt; lokal wird kein installiertes Python gesperrt.

Mac arm64 benötigt einen nativen Mac-Runner mit Framework-Python, `sips`, `iconutil` und `codesign`. Der Benutzer hat ausdrücklich „GitHub Actions mit macOS-Runner verwenden“ gewählt und „weiter“ beauftragt. Der neue native Workflow wird dafür auf `codex/glide-paketabschluss-3.45.0` übertragen; die Paketversion wird durch einen echten Neubau aktualisiert. Kein Merge oder öffentliche Veröffentlichung.

Die erste Windows-Vollprüfung lief vollständig und enthält sechs rote Befunde. Vier Altleser-/Abbauprüfungen verwendeten unpassende historische Begleitmodule bzw. erzeugten beim Abbau neue Ressourcen; die Altleser erhalten nun vollständige gepinnte Git-Lieferstände. Der echte Rückgängig-Animationsfehler ist mit roter Gegenprobe korrigiert; der B15-Prüfer unterscheidet native Stapelreihenfolge mit einer Vorder-/Hintergrundgegenprobe. Eine Standzeile ist berichtigt. Gezielte Nachläufe und erneute Vollprüfung folgen; der erste rote Lauf wird nicht umgedeutet.

## Belegter Zwischenstand

- Korrigierte App `d516ca67…`, Modell unverändert `ced120a5…`; der echte Animationsfehler ist mit einer roten Gegenprobe belegt. B15 prüft nun Tk-Stapelreihenfolge mit positiver Überlagerungsgegenprobe. 1.284 appweite Knopfprüfungen und 212 Verweisvorschau-Knopfprüfungen im gezielten Nachlauf grün.
- Altleser: Import, Ansichten und Wiederholungsregeln im vollständigen gezielten Nachlauf grün; Seitenkarten-Altleser ebenfalls grün. Ein streuender Seitenkarten-Tempolauf war rot; die unmittelbar danach allein ausgeführte Gegenprobe ist mit unveränderter Grenze grün (Verhältnis gemischt/Aufgaben 0,9065). Kein Grenzwert angehoben.
- Windows x64: echter Neubau 3.45.0, 87 kompilierte Modulnachweise, 103 Paketdateien, PE-Prüfung grün. Die lokale Startprobe ist grün (sechs Ansichten, Speichern/Dateilesen, Erledigen/Undo, App-Sicherung, Ressourcen/Lizenzen/Schriften/Logo/DND); kein externer Python-Suchpfad und kein Callbackfehler. Datei- und Produktversion 3.45.0. Ohne Inhaberzertifikat weiter unsigniertes Entwicklungsartefakt; keine lokale ACL-Sperrprobe.
- Mac arm64: [nativer Lauf 40328682255](https://github.com/n05a-design/glide-to-do/actions/runs/40328682255) vollständig grün an Commit `4e732200…`. Python 3.14.5 / Tcl-Tk 9.0.3, kompilierter Quellabgleich, Mach-O/Lizenzen/Ad-hoc-Signatur und isolierter Start grün; externe Python-Gegenprobe blockiert, Systeminstallationen unverändert. Portables TAR mit 333 Dateien und 29 Symlinks. TAR-SHA-256 `b6284197c62fddee1283207ead6680baed72bdf8826114e944316857284a7252`.
- Der erste Maclauf baute und startete korrekt, scheiterte aber am Archiv-Dateimengenvergleich. BSD-tar wird nun ohne zusätzliche Mac-Metadaten verwendet; die strikte Hash-/Dateimengen-/Modus-/Symlinkprüfung bleibt bestehen und schreibt ein vollständiges Inventar auch bei Fehlern. Der zweite Lauf ist grün; der rote erste Lauf bleibt erhalten.
- Die erneute lokale Windows-Vollprüfung ist am korrigierten Appstand unter `windows_voll_abschluss` grün: 123 Schritte, 122 ausgeführt/grün und eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Python- und Build-Zielordner sind nach diesem Abschluss und bestätigtem Hashabgleich übernommen.

## Tatsächliche Lieferung

[Liefermanifest](lieferung.json): Python-Fassung 86 Code-Dateien und 147 Ressourcen bytegleich; alle 103 Windows- und 333 Mac-Paketdateien nach der Kopie hashgleich. Aktive alte 3.42.0-Pakete liegen unter `build/windows/Archiv` beziehungsweise `build/macos/Archiv`. Die drei zuvor fehlenden Frameworkdateien sind vollständig vorhanden; [Mac-Abgleich](mac_entpackpruefung.json) trennt native TAR-/Signaturbelege und Windows-Linkdarstellung.

- Windows: `build/windows/Glide-3.45.0/Glide.exe`, ZIP `Glide-3.45.0-windows-x64.zip`, SHA-256 `47ff56183e48de0b196c7910b1393d4a1521f1d3afc9d7b7a483d436d7bdb7c9`.
- Mac: `build/macos/Glide-3.45.0-macos-arm64.tar.gz`, SHA-256 `b6284197c62fddee1283207ead6680baed72bdf8826114e944316857284a7252`. Nativ entpacken; die lokale .app ist eine vollständige Windows-Inspektionskopie mit NT-Linkzielen.
- [Python-Lieferprobe](python_lieferprobe.json): sechs Ansichten, neues Startseitenmodul tatsächlich aus 07, Speichern/Erledigen/Undo und Callbackfreiheit grün. Showcase-Import/Neustart und sechs Lieferdateien erneut geprüft.
- [Startprobe des kopierten Windows-Pakets](windows_liefer_start_nachlauf.json) und Gegenprobe des Bauoriginals grün. Ein erster Lieferstart meldete die fremde Host-Injektion `tv_x64.dll`; die beiden unmittelbaren Nachläufe bestanden denselben unveränderten strengen Bibliotheksvalidator. Keine Ausnahme ergänzt und kein fremder Prozess verändert. Der rote Beleg bleibt erhalten; ein allgemeiner Clean-Machine-Nachweis ist damit nicht ersetzt.

Native Mac-Signaturprüfung stammt vom Macrunner; Windows ersetzt sie nicht. Windows bleibt ein unsigniertes Entwicklungsartefakt. Menschliche Reader-/DPI-/Mehrmonitorabnahme, komplette Mac-/Linux-Matrix und öffentliche Veröffentlichungstore bleiben eigene Grenzen. Die strenge lokale CI-Abschlussprüfung nach Lieferung und Dokumentabgleich steht unter `ci_abschluss`.

**Strenger Abschluss grün:** 19/19 Schritte ausgeführt, 193 Werkzeugtests (einer übersprungen), zweimal 932 Fachtests, fünf Analysen, Startprobe, bytegleiche Python-Lieferung, 116 Vendor-Dateien sowie Datenschutz-/Ablage-/Synchronisationsprüfung grün. [Maschinenlesbarer Abschluss](ergebnis.json), [CI-Ergebnis](ci_abschluss/ergebnis.json), [Windows-Vollprüfung](windows_voll_abschluss/ergebnis.json). Öffentliche JSON-Nachweise haben bereinigte Benutzerpfade; unveränderte Originalbelege bleiben lokal im Bauordner erhalten.

## Zusätzliche GitHub-Matrix

Lauf [40329621330](https://github.com/n05a-design/glide-to-do/actions/runs/40329621330) auf `6c342f8`: Grundstufe grün; Windows-Vollmatrix mit eigener Tk-9.1-Laufzeit und nachgelagerter nativer Paketbau einschließlich echter ACL-Sperrgegenprobe grün. Das ist ein separater Runtime-/Paketnachweis; die lokal bereitgestellte Windows-Fassung verwendet weiterhin die oben nachgewiesene Python-3.14.7-/Tk-9.0.4-Laufzeit.

Die Linux-/Tk-9.1-Matrix bleibt wegen `test_arbeitsmodi`, Fall `kompakt`, rot: Nach dem synthetischen Kürzel ist der erwartete Modus/Mindestgrößenzustand nicht erreicht. Ursache nicht abschließend geklärt. Alle übrigen Suiten dieses Laufs und die kalibrierten Defektgegenproben sind grün. Keine pauschale grüne Remote-/Linux-Freigabe; Befund bleibt als konkrete WA-42-Restprüfung dokumentiert. Ein eigenständiges Linux-Paket ist nach Produktentscheidung nicht gewählt.
