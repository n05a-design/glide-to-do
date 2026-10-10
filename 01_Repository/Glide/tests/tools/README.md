# Prüfwerkzeuge für Glide

Stand 10.10.2026 · Glide 3.37.0 · Aufgabenformat 23 · Einstellungen 2 · Vorlagen 2

Alle Werkzeuge werden aus `01_Repository/Glide` gestartet. Werkzeuge, die echte Tk-Fenster prüfen, brauchen eine grafische Sitzung (unter Linux Xvfb; das ersetzt keine native Windows- oder macOS-Abnahme). Zahlen zu Suiten und Formaten stehen bewusst nicht hier, sondern im Quelltext (`SUITEN`, `ANALYSEN`, `APP_VERSION`, `DATA_SCHEMA_VERSION`) – bis 3.21.3 rotteten sie in dieser Datei. Was tatsächlich lief: [QA-Bericht](../../docs/07_QA_BERICHT.md).

**Hintergrund unter macOS:** `pruefen.py` startet die Suiten mit `hintergrund/sitecustomize.py`; die Prüffenster nehmen keine Maus an, die **Tastatur ist nicht abgeschirmt**. `--vordergrund` schaltet das ab. Verhalten während eines Laufs: [Prüfplan, Regeln](../../docs/05_QA_TESTPLAN.md#regeln).

| Werkzeug | Zweck |
|---|---|
| `pruefen.py [--modus voll] [--protokoll PFAD] [--timeout S]` | Prüflauf: Vorprüfungen (Syntax, Version, Dokumentation, Fixtures), Unit-Tests, Tk-Probe, gemessener Zeitzonenversatz, alle Suiten, Showcase, Analysen; im Vollmodus zusätzlich Reproduktion von Beispiel- und Releasedaten und Fensterfotos (macOS und Windows, lokal im jeweiligen Prüfprotokoll). Exitcode 1 bei einem Fehlschlag, 2 wenn Tk oder die Zeitzone den Lauf unvollständig lassen |
| `ci_grundstufe.py [--protokoll PFAD] [--lieferstand-streng]` | CI-Grundstufe (GitHub Actions und lokal): Vorprüfungen, Werkzeugtests, Unit-Tests, Analysen, Startprobe, Lieferstand `src/glide` ↔ `07_Python-Versionen`, Fremdcode gegen `vendor/provenance.json`, Datenschutz (keine Benutzerpfade), Ablagegröße, Synchronisation. Ohne Integrationssuiten |
| `linux_gegenproben.py --protokoll PFAD [--basis-ergebnis DATEI] [--fall NAME]` | Kalibrierte UI-Erwartungen an isolierten, absichtlich defekten App-Kopien prüfen: Überlauf, Knopfreihenfolge, SVG-Fähigkeit, tatsächlich wirkendes Scrollen und Datumsübernahme. Jede positive Suite muss zuerst grün sein; Importfehler und Zeitüberschreitungen gelten nicht als Gegenprobe. In CI nach der Linux-Vollprüfung, lokal ohne Basisdatei mit eigener positiver Vorprüfung. Rohprotokolle außerhalb von OneDrive halten |
| `synchronisationswaechter.py` | Konfliktkopien `<Name>-<Gerätename>` neben ihrem Original und Hauptdokumente, die gegenüber der Git-Vorfassung ohne Vermerk („gekürzt“/„zusammengeführt“ mit dem Datum der Standzeile) mehr als 40 % ihrer Zeilen verlieren (W04, seit 08.10.2026); Schritt „Synchronisation“ der CI-Grundstufe |
| `ablagegroesse.py` | Keine Archivkopien von Glide-Daten, keine `*.fetch`-Reste, Archive, Nachweise und Releaseplanungen nur der sieben neuesten Versionen (je Datenformat bleibt ein Beleg), Fensterbilder nur der drei neuesten, keine Datei über 50 MB. Kürzen: `scripts/pflege/ablage_kuerzen.py` |
| `standpruefung.py` | Standangaben, Formatstufen, überholte Aussagen, Modullisten, relative Links, Titel, erster Vollprüfungsaufruf und Suitezahl aller aktiven Dokumente (R1–R14); ohne Tk, Sekunden |
| `analyse_statisch.py`, `analyse_erreichbarkeit.py` | Quelltextbefunde und Referenzen, keine Laufzeitgarantie |
| `attributpruefung.py` | Aufrufe über `self` ohne Ziel in ihrer Klasse, auch über geerbte Tk-Basen |
| `dublettenpruefung.py [--laenge N]` | Wiederholte Codeblöcke; meldet, bewertet nicht |
| `pruefe_tk.py` | Tk-Voraussetzung und unter macOS die native Mausisolierung der Prüffenster |
| `pruefe_showcase.py` | Pflichtprüfung des gelieferten Showcase (Import, Remapping, Vorschauen, Undo, Vorlagen, Neustart) |
| `showcase.py [--tag JJJJ-MM-TT]` | Erzeugt den Showcase aus den Bildern in `tests/fixtures/showcase/bilder` |
| `beispieldaten.py --ziel DATEI` | Demonstrationsbestand im aktuellen Format |
| `releasedaten.py --ziel DATEI --stichtag JJJJ-MM-TT [--screenshot PFAD.png]` | Release-Arbeitslisten zum aktuellen Stand; Planungsfristen folgen dem Stichtag, Webquellen nicht. Unter Windows zusätzlich Aufnahmen im hellen Design und seinem dunklen Gegenstück; gleiche Bilder brechen ab |
| `rundgang.py` | Probedaten „Rundgang“ (Liste, Notiz, Seite mit Bildern, Zeichnung) |
| `vorlagendaten.py` | Vorlagenkatalog `resources/templates/glide_vorlagen.glidetemplates` |
| `screenshots.py` | Linux/X11-Aufnahmen eigener Testfenster |
| `windows_vollpruefung.cmd` / `.ps1` | Windows: verlangt Python ≥ 3.14/Tk ≥ 9, prüft OneDrive-Platzhalter, startet den Vollmodus in `tests/qa-<Version>/windows_<Zeitstempel>`; Anleitung in der [manuellen Prüfliste](../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) |
| `symbolpruefung.py` | Private App-Schrift registrieren und tatsächliche Glyphenfamilien messen |
| `leistungspruefung.py --ziel DATEI.json` | Lokale synthetische Neudarstellungs- und Speichermessung |
| `dauerlauf.py --minuten 10 --aufgaben 4000 --ziel DATEI.json` | Dauerlauf: wachsende Callbacks, Undo-Stände, Speicher, Unversehrtheit nach Neuladen. Nicht im Standardlauf; zehn Minuten sind das Minimum, damit der 15-Sekunden-Takt der Erinnerungen oft genug feuert |
| `test_standpruefung.py`, `test_ablagegroesse.py`, `test_datenschutz.py`, `test_synchronisationswaechter.py` | Werkzeugtests der Wächter (Stand, Ablage, Benutzerpfade auch JSON-maskiert, Synchronisationskopien); laufen in der CI |

Die Windows-Vollprüfung nimmt zuerst `-PythonExecutable <Pfad>`, danach die separate Prüflaufzeit unter `%USERPROFILE%/.cache/glide-qa/python-3.14.8/runtime/python.exe`, danach `py -3.14` oder `python`. Ein ungeeignetes Python/Tk beendet den Starter mit Exitcode 3 vor der Suite. Der Cache ändert weder PATH noch die Standardinstallation. Herkunft und Herstellerhash stehen im aktuellen [QA-Bericht](../../docs/07_QA_BERICHT.md).
