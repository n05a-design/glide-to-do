# QA-Bericht – Glide 3.28.0

Stand 23.09.2026 · App 3.28.0 · Datenformat 18 · Windows, Python 3.12.7

## Ergebnis

Der Funktionsstand 3.28 ist gezielt geprüft, aber **noch nicht als vollständiger
Release-Gesamtlauf freigegeben**. Der
[Schnelllauf](../tests/qa-3.28.0/abschluss_2026-09-23/ergebnis.json) bestätigt
Versionskonsistenz, Tk, Zeitzone, den Haupttest und den überwiegenden Teil der
Integrationssuiten. Sein Gesamtergebnis bleibt Exitcode 1, weil mehrere ältere
OneDrive-Platzhalter lokal nicht lesbar sind und zwei lang laufende UI-/
Gesamtprüfungen die bewusst gesetzte Grenze von 60 Sekunden überschritten.

Nach diesem Lauf wurden die veralteten Erwartungen der Vorlagenprüfung an die
vier neuen Tagebuchvorlagen angepasst. Die Vorlagenerzeugung verwendet nun
stabile Erstellungszeitpunkte. Anschließend bestanden einzeln:

- Syntaxprüfung des Quellstands und der startbaren 3.28-Kopie;
- `test_glide.py` einschließlich Kern-, Backup-, UI-, Ordner-, Papierkorb- und
  Migrationstests;
- `test_features328.py` für Format 18, Tagebuchdaten, Sicherung, Vorlagen,
  Menügestaltung, Aktionsfarben und verdichtete Notizwerkzeuge;
- `test_template_workflows.py` für 16 vollständige Projekt-/Listenvorlagen plus
  vier Tagebuchvorlagen, Reproduzierbarkeit, Migration und Dialoge;
- `test_features315.py` mit der seit 3.27 gültigen Tabellenfilter-Logik;
- im Schnelllauf unter anderem `test_datenintegritaet`, `audit_app`,
  `test_dialog_theme`, `test_ui_updates`, `test_glide_36`, `test_release36`,
  `test_ui_polish36`, `test_release37`, `test_reminders`, `test_ui39`,
  `test_workspace310` sowie die lesbaren Suiten 3.12 und 3.14 bis 3.26;
- Erreichbarkeits-, Attribut- und Dublettenprüfung. Die statische Analyse lief
  anschließend mit Exitcode 0 durch; ihre Größen- und Duplikathinweise sind
  Wartungshinweise, keine fehlgeschlagenen Funktionsprüfungen.

Nach der Meldung eines weißen Neuaufbaus beim Füttern von Gismo wurde der
Pflegepfad zusätzlich korrigiert und erneut geprüft. Der 3.28-Test läuft dafür
im Dopamin-Design, löst `Füttern` aus und weist nach, dass die vorhandenen
Pflegebalken aktualisiert werden, bestehen bleiben und kein `refresh_home()`
mehr aufgerufen wird. Syntax, Hauptsuite, Vorlagenworkflow und
Tagesplanungstest bestanden danach erneut. Die tatsächliche Sichtprüfung mit
echter Maus bleibt in `Manuelle_Pruefung_3.28.0.md` offen.
Der maschinenlesbare Nachweis liegt unter
[`tests/qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json`](../tests/qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json).

Quelle und startbare Version sowie deren jeweiliger Vorlagenkatalog wurden nach
der letzten Korrektur erneut kopiert und per SHA-256 auf Bytegleichheit geprüft.
Alle App- und Integrationstests arbeiten mit temporären `GLIDE_DATA_DIR`-
Verzeichnissen; die Nutzerdaten wurden nicht als Testbestand geöffnet.

## Offene technische Prüfblockaden

Folgende Dateien tragen auf diesem Rechner den OneDrive-Platzhalterstatus und
lieferten `PermissionError: [Errno 13] Permission denied`:

- `tests/integration/test_features311.py` und `test_features313.py`;
- `tests/fixtures/current_v15/reference_v15.json` innerhalb von
  `test_features322.py`;
- ältere Beispiel-Fixtures, zuerst
  `tests/fixtures/beispiele/glide_releaseplanung_3.10.0.glidebackup`;
- `docs/38_DOKUMENTATIONSABGLEICH_2026-09-13.md`;
- außerhalb des Repositorys
  `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.21.4.md`, wodurch die
  Standprüfung vor der inhaltlichen Auswertung abbricht.

Diese Dateien müssen in OneDrive zunächst lokal verfügbar gemacht werden;
danach ist der Schnell- oder Vollmodus erneut auszuführen. Das ist eine
Zugriffsblockade und kein bestandener Test.

`test_ui_followup36.py` überschritt wie bereits im 3.27-Ausgangsstand die
60-Sekunden-Grenze in der Fenstergrößen-/Ereignisverarbeitung. Der ältere
Sammeltest `test_vollpruefung325.py` überschritt dieselbe Grenze. Beide bleiben
offen und dürfen nicht als Erfolg gewertet werden.

## Manuelle Grenzen

Eine neue menschliche Sichtprüfung von 3.28 wurde nicht durchgeführt. Die vom
Nutzer gelieferten Bildschirmbilder dienten als Problembeleg, ersetzen aber
keinen abschließenden Bedienungstest. Ebenfalls offen bleiben macOS, native
Druckdialoge, DPI-/Mehrmonitor-Sonderfälle, Screenreader, Installer,
Signierung/Notarisierung und reale Verteilung. Erst nach lokalem Herunterladen
der Platzhalter, erneutem vollständigem Prüflauf und Sichtprüfung ist eine
Release-Freigabe belastbar.

Der letzte vollständig bestandene automatisierte Gesamtnachweis bleibt bis
dahin der archivierte Stand 3.26.0; er ist kein Freigabenachweis für 3.28.0.
