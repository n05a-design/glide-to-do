# Prüfwerkzeuge für Glide

Stand 01.10.2026 · Glide 3.33.1 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

**Hintergrund (macOS, seit 30.09.2026):** `pruefen.py` startet die Suiten mit
`hintergrund/sitecustomize.py`. Prüffenster nehmen dann weder Fokus noch
Tastatur; man kann während einer Vollprüfung weiterarbeiten.
`--vordergrund` schaltet das ab.

Prüfläufe verwenden `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt: In einer Zone ohne Versatz ist jeder Zeitzonenfehler unsichtbar. Seit 3.23 misst `pruefen.py` nach, welcher Versatz für die Suiten tatsächlich gilt. **Unter Windows wird `TZ` nicht gesetzt** – die Laufzeit baut daraus eine erfundene Zone ohne Sommerzeitregel; dort gilt die Systemzeitzone.

Alle Werkzeuge werden aus dem Repository gestartet. Werkzeuge benötigen eine
grafische Sitzung, soweit sie echte Tk-Fenster prüfen. Linux kann dafür Xvfb
verwenden; das ersetzt keine native Windows- oder macOS-Abnahme. Welche Läufe
tatsächlich ausgeführt wurden und welche Plattformprüfungen offen sind, steht
ausschließlich im [aktuellen QA-Bericht](../../docs/07_QA_BERICHT.md).

| Werkzeug | Zweck |
|---|---|
| `pruefen.py --modus voll --protokoll PFAD` | Vollprüflauf: alle Suiten aus `SUITEN`, alle Analysen aus `ANALYSEN`, Vorprüfungen einschließlich Tk-Voraussetzung und gemessenem Zeitzonenversatz, Daten-Reproduktion und Bilder. Die Zahlen stehen im Quelltext, nicht hier. Exitcode 1 bei einem Fehlschlag, 2 wenn Tk oder die Zeitzone den Lauf unvollständig lassen. |
| `ci_grundstufe.py [--protokoll PFAD] [--lieferstand-streng]` | CI-Grundstufe (D09), in GitHub Actions bei jedem Push/PR auf `main` und lokal gleich: Vorprüfungen aus `pruefen.py`, `test_standpruefung.py`, Tk-freie Unit-Tests, die fünf Analysen, Startprobe mit temporärem Datenordner (ohne Bildschirm über `xvfb-run`) und Lieferstand `src/glide` ↔ `07_Python-Versionen` (Hinweis, mit `--lieferstand-streng` Fehler). Ohne Integrationssuiten; ersetzt nicht die Vollprüfung. Exitcode 1 bei einem Fehlschlag |
| `standpruefung.py` | Standangaben und Formatstufen aller aktiven Dokumente gegen `VERSION` und `DATA_SCHEMA_VERSION`; seit 29.09.2026 außerdem bekannte überholte Aussagen (R9), vollständige Modullisten (R10) und alle relativen Links aktiver Dokumente (R11), aktuelle Titel (R12) und erster Vollprüfungsaufruf (R13), Suitezahl in laufenden Standzeilen gegen SUITEN (R14); gepflegte datierte Übergaben/Checklisten sind ausdrücklich registriert; ohne Tk, Laufzeit Sekunden |
| `analyse_statisch.py`, `analyse_erreichbarkeit.py` | Quelltextbefunde und Referenzen, keine Laufzeitgarantie |
| `beispieldaten.py --ziel DATEI` | Demonstrationsbestand im aktuellen Aufgabenformat erzeugen und importieren |
| `vorlagendaten.py` | Vorlagenkatalog `resources/templates/glide_vorlagen.glidetemplates` reproduzierbar erzeugen |
| `releasedaten.py --ziel DATEI --stichtag JJJJ-MM-TT` | Drei Release-Arbeitslisten plus Eingang zum aktuellen Stand, mit Quellen und Codebelegen |
| `screenshots.py` | Linux/X11-Aufnahmen eigener Testfenster; Windows nutzt `pruefen.py --screenshots` oder die `--screenshots`-Option der Integrationssuiten |
| `windows_vollpruefung.cmd` / `.ps1` | Windows: prüft Python/Tk und OneDrive-Platzhalter, startet dann den Vollmodus in `tests/qa-<Version>/windows_<Zeitstempel>`; Anleitung in `00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md` |
| `symbolpruefung.py` | Private App-Schrift registrieren und tatsächliche Glyphenfamilien messen |
| `leistungspruefung.py --ziel DATEI.json` | Lokale synthetische Neudarstellungs-/Speichermessung |
| `dauerlauf.py --minuten 10 --aufgaben 4000 --ziel DATEI.json` | Dauer- und Belastungslauf: wachsende Callbacks, Undo-Stände, Speicher und Unversehrtheit nach dem Neuladen |

Die Zwecke sind absichtlich ohne Versions- und Formatzahlen formuliert. Bis
3.21.3 stand hier „Achtzehn Suiten", „Format 14" und „für 3.14" – Angaben, die
bei jedem Stand hätten mitgehen müssen und es nicht taten. Was die Werkzeuge
tatsächlich erzeugen, bindet ihr Quelltext an `APP_VERSION` und
`DATA_SCHEMA_VERSION`.

`dauerlauf.py` gehört bewusst nicht in den Standardlauf: Er misst nichts, was
in Sekunden sichtbar wird, sondern ob über Stunden etwas wächst, das nicht
wachsen darf. Zehn Minuten sind das Minimum, damit der 15-Sekunden-Takt der
Benachrichtigungen oft genug feuert; `--minuten 1 --aufgaben 500` ist ein
Rauchtest des Werkzeugs, kein Nachweis. Exitcode 1 bei einem Befund.

Der Release-Erzeuger aktualisiert Planungsfristen anhand des Stichtags, nicht
automatisch die Webquellen. Ältere Quellenabrufe stehen in den Arbeitslisten.
[QA](../../docs/07_QA_BERICHT.md) · [Prüfungen und Umfang](../README.md) ·
[Historische Leistungsmessung 3.6](<../../docs/archiv/21_LEISTUNGSBERICHT_3.6.0_vor_Nachbesserung_2026-09-11.md>).

`python3 -B tests/tools/test_standpruefung.py` prüft veraltete gepflegte Einstiege samt Historienausnahmen. Inhaltlicher Abgleich von Aufgabenstatus/Entscheidungen bleibt zusätzlich erforderlich; [Arbeitsrichtung](../../docs/ARBEITSRICHTUNG.md).
