# CI-Grundstufe 3.33.1 – Nachweis

Datiert 01.10.2026 · App unverändert 3.33.1 · Werkzeug- und Konfigurationsnachlauf, keine Produktionsversion

## Anlass

Nach dem Push vom 01.10.2026 lief in GitHub Actions die Vorlage „Python application“ und endete mit Exitcode 2:
- Python 3.10, `pytest` über das ganze Repository: 33 Elemente, **99 Fehler beim Einsammeln**.
- Ursachen, alle aus dem Protokoll belegt:
  1. **Archivkopien** wie `test_glide_3.12.0_vor_3.13.0.py` sind wegen der Punkte im Namen keine importierbaren Module.
  2. **Integrationssuiten** sind ausführbare Skripte, die schon beim Import `tk.Tk()` öffnen. Ohne Bildschirm: `no display name and no $DISPLAY`.
  3. **Altstände in `50_Ablage`** verweisen auf nicht vorhandene Pfade und kollidieren in den Modulnamen mit den aktiven Suiten.
- Lokal nachgestellt (pytest 9 in einer Arbeitsumgebung, Python 3.12, ohne Bildschirm): ebenfalls Abbruch beim Einsammeln, 61 Fehler.

Glides Prüfungen laufen nicht über pytest, sondern über die eigenen Werkzeuge in `tests/tools` und benötigen nur die Standardbibliothek.

## Änderung

- **Workflow:** `.github/workflows/python-app.yml` heißt jetzt „Glide-Prüfung“ und führt bei jedem Push und Pull Request auf `main` die Grundstufe aus. Kein flake8 und kein pytest mehr, also keine zusätzlichen Abhängigkeiten.
- **Grundstufe:** [`tests/tools/ci_grundstufe.py`](../../tools/ci_grundstufe.py) nutzt die Prüfungen aus `pruefen.py`:
  - Syntax, Versionskonsistenz, Dokumentationsindex mit Links, Fixtures;
  - `test_standpruefung.py` und die Tk-freien Unit-Tests;
  - die fünf Analysen, darunter `standpruefung.py`;
  - Startprobe mit temporärem `GLIDE_DATA_DIR` unter Xvfb: Start und sechs Ansichten ohne Callbackfehler und ohne Fehlerprotokoll;
  - Lieferstand `src/glide` ↔ `07_Python-Versionen` per SHA-256 als Hinweis.
- **Integrationssuiten unter Linux:** zweiter Job, nur auf ausdrücklichen Start („Run workflow“, Option „integrationssuiten“), informativ (`continue-on-error`).
- **Unverändert:** Programmcode in `src/glide` und `pruefen.py`.

## Nachtrag: Lieferstand, Aufräumen, tote Links (auf Wunsch des Inhabers)

- **Lieferstand:** `scripts/pflege/abgleich_07.py` hat `07_Python-Versionen` auf den Prüfkandidaten 3.33.1 gebracht: 11 Code-Dateien und 131 Ressourcen, keine Abweichung. Die 3.33.0-Hauptdatei liegt als `Archiv/Glide-Aufgaben-und-Listen_v3.33.0_Z.pyw` im Archiv. [Ausgabe](lieferstand_abgleich.txt).
- **Probestart aus `07_Python-Versionen`:** `Schnellstart.pyw` wählt `Glide-Aufgaben-und-Listen_v3.33.1.pyw`. Sechs Ansichten liefen ohne Callbackfehler, das Fehlerprotokoll ist leer (Linux, Tk 8.6, temporärer Datenordner).
- **Entfernt:**
  - `src/glide/app.pyw.fetch` (SHA-256 `d47c4233…`): eine frühere Zwischenfassung von 3.33.1 ohne verzögertes Einblenden der Dialoge und ohne gemerkten Logo-Abstand; `app.pyw` enthält beides.
  - `.github/workflows/python-publish.yml`: GitHub-Vorlage für PyPI-Veröffentlichung, für Glide nicht anwendbar.
  - Beide bleiben in der Git-Historie.
- **Tote Links:** Der Push 2d09330 hat `90_Testdaten_Extern` entfernt. Die Grundstufe meldete zwei verbliebene Verweise (`docs/00_INDEX.md`, `README.md`); beide sind entfernt.
- **Grundstufe mit `--lieferstand-streng`:** alle Schritte bestanden ([Ergebnis](grundstufe_streng_py3.14rc2/ergebnis.json)).

## Ergebnisse (Linux-Container, Tk 8.6.14, künstliche Daten)

**Grundstufe** – [`grundstufe_py3.14rc2/ergebnis.json`](grundstufe_py3.14rc2/ergebnis.json):
- Alle Schritte bestanden, Exitcode 0, rund 2–3 Minuten.
- Vorab ebenso mit Python 3.12.3.
- **Hinweis Lieferstand:** 9 Abweichungen. `07_Python-Versionen` enthält im Repository noch `Glide-Aufgaben-und-Listen_v3.33.0.pyw`; es fehlen die 3.33.1-Hauptdatei, `sidebar_policy.py`, `svg_geometry.py`, das neue `logo.py` und vier Logo- bzw. Vorlagendateien. Die README dort nennt 3.33.1 als „Prüfkandidat; Auslieferung nach dem Volllauf“.

**Gegenprobe Integrationssuiten unter Linux** – `pruefen.py --modus schnell`, Python 3.12.3 mit Xvfb, [`integrationssuiten_linux_py3.12/`](integrationssuiten_linux_py3.12/):
- Vorprüfungen, Unit-Tests, Showcase und vier der fünf Analysen bestanden.
- `standpruefung` meldete einen Link im CHANGELOG auf diesen Nachweis, der während des Laufs noch nicht existierte. Das war ein Zwischenstand dieser Bearbeitung; im abschließenden Grundstufenlauf ist sie grün.
- 50 von 60 Suiten bestanden, 10 nicht:

| Ursache | Suiten |
|---|---|
| Braucht Tk 9 (SVG, `TouchpadScroll`) | `test_befunde330`, `test_tempo330` |
| Container läuft als root; `chmod 0o500` sperrt root nicht | `test_speicherlast330` (Schritt „Fehlendes Schreibrecht“) |
| **Auch auf dem Mac rot** (Vollprüfung 3.33.1 vom 01.10.2026, gleiche Meldung) – echte Befunde in 3.33.1 | `audit_app` (Ordner per Ziehen in Ordner: `Item folder:… not found`), `test_aufraeumen330` (zusätzlicher Menüeintrag „Neue Galerie“), `test_features329` (Titel der Notizbuch-Zeichnung) |
| Schriftmetrik, Layout oder Plattformverhalten unter Linux; einzeln nicht geklärt | `test_glide` (Kopfhöhe 44 statt 42 px), `test_mindestgroesse330` und `test_kompression330` (Text gekürzt), `test_rueckmeldung330` (Zeichenfläche springt) |

Die Suiten sind auf den Referenz-Mac abgestimmt. Deshalb gehören sie vorerst nicht in die verpflichtende CI. Die vier reinen Linux-Abweichungen zu kalibrieren, ist ein eigener Schritt (Entwicklungsplan, Zeile CI).

**Vollprüfung 3.33.1 auf dem Mac** ([Ergebnis](../bereiche_fenster_2026-10-01/vollpruefung/ergebnis.json), mit dem Push 2d09330 nachgeliefert):
- Exitcode 1: 73 Schritte bestanden, 4 fehlgeschlagen – `audit_app`, `test_ui39`, `test_features329`, `test_aufraeumen330`.
- `test_ui39` scheitert nur auf dem Mac (Auswahlfeld schließt nicht mit „Erste Option“); unter Linux bestanden.
- 3.33.1 bleibt damit Prüfkandidat.

## Grenzen

- **Linux statt Referenz-Mac:** GitHub-Runner und dieser Container sind Linux mit Tk 8.6. Die Vollprüfung auf dem Mac bleibt maßgeblich.
- **Erster Lauf in GitHub Actions** erfolgt mit dem Pull Request; dessen Ergebnis steht im PR.
