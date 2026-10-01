# QA-Bericht – Glide 3.29.0

Stand 24.09.2026 · App 3.29.0 · Datenformat 19 · macOS, Python 3.14.5

## Ergebnis 3.29.0

3.29.0 integriert die Zeichnungsseite (Aufgabenformat 19). Geprüft wurde auf
dem Entwicklungs-Mac mit Python 3.14.5 und isoliertem `GLIDE_DATA_DIR`.

- **Ausgangslauf vor Beginn** (Schnellmodus,
  [Protokoll](../tests/qa-3.28.0/vor_zeichnungsintegration_2026-09-24/ergebnis.json)):
  dieselben fünf bekannten Altbefunde wie seit 3.28 (Fixture 3.26.0,
  Vorlagenreproduktion, `test_features313`, `test_features322`,
  `test_features328`).
- **Erster Vollmodus nach der Integration**
  ([Protokoll](../tests/qa-3.29.0/zeichnungsseite_2026-09-24/ergebnis.json)):
  Syntax, Versionskonsistenz, Dokumentationsindex (842 Links), Fixtures, Tk,
  Zeitzone, **alle 35 Suiten** einschließlich der neuen `test_features329.py`
  und **alle fünf Analysen** bestanden. Die fünf Altbefunde sind behoben. Rot
  blieben nur die erstmals seit 3.26 wieder ausgeführten Reproduktionsabgleiche
  von Beispiel- und Releasedaten: Der Vergleich behandelte die seit 3.26
  vorhandenen Listenzeitpunkte `created_at`/`updated_at` noch als Inhalt.
  Korrektur in `pruefen.py`: Diese Erzeugungszeitpunkte sind wie `exported_at`
  ausgenommen; das Tagebuch-Momentdatum wird relativ zum Exporttag verglichen.
- **Nachprüfung im Vollmodus**
  ([Protokoll](../tests/qa-3.29.0/zeichnungsseite_nachpruefung_2026-09-24/ergebnis.json)):
  **Exitcode 0** – alle 50 automatisierten Schritte bestanden: Vorprüfungen,
  35 Suiten, fünf Analysen sowie Erzeugung und Abgleich von Beispiel- und
  Releasedaten. Das ist der erste vollständig grüne Gesamtlauf seit 3.26.0;
  er ersetzt keine manuelle Plattformabnahme.
- **Abnahmelauf nach Rückmeldung** (Farbspektrum, Scrollbereich, zusätzliche
  Abnahmetests; [Protokoll](../tests/qa-3.29.0/abnahme_2026-09-24/ergebnis.json)):
  49 Schritte bestanden, **ein Befund** in `test_ui_followup36`: Innenabstand
  einer Bestandskarte nach Schriftwechsel und Resize (rechts 109 statt 16 px).
  Drei Einzelwiederholungen waren grün; der Bereich wurde in 3.29 nicht
  geändert. Ursache ist eine Layoutmessung vor dem letzten Tk-Durchlauf unter
  Last. Die Prüfung misst jetzt bis zu sechsmal den stabilen Endzustand; die
  Abstandsanforderung selbst ist unverändert.
- **Abnahme-Nachprüfung**
  ([Protokoll](../tests/qa-3.29.0/abnahme_nachpruefung_2026-09-24/ergebnis.json)):
  **Exitcode 0** – alle 50 automatisierten Schritte bestanden (Vorprüfungen,
  35 Suiten, fünf Analysen, Reproduktion von Beispiel- und Releasedaten).
  Maßgeblicher automatisierter Nachweis des Endstands 3.29.0.

Die einzelnen Abnahmekriterien der Etappe mit Nachweis stehen im
[Vertrag 3.29, Abschnitt 11](65_ZEICHNUNGSSEITE_3.29.0.md).

Übersprungen bleiben plattformgebunden die Bildaufnahmen (nur Linux/X11 bzw.
Windows) und die Sichtprüfung. Bildschirmaufnahmen waren in der
Agentenumgebung nicht erlaubt; die Einbettung der Zeichenfläche wurde über
Widgetgeometrie geprüft (1280 × 860: Fläche 922 × 616 Pixel; 860 × 700:
502 × 420 Pixel). Offen und manuell: [Prüfliste 3.29](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.29.0.md)
mit Maus/Trackpad, Tastatur und Screenreader, DPI, Mehrmonitor, Windows,
Designs und dem Illustrator-/Affinity-Rundlauf. Ein Windows-Gesamtlauf für
3.29.0 fehlt.

## Ergebnis 3.28.0 (historisch)

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
