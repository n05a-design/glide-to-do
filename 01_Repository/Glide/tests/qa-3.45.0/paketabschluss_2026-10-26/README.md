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

Prüfergebnisse, Bauhashes und verbleibende tatsächliche Plattformgrenzen werden hier nachgeführt.
