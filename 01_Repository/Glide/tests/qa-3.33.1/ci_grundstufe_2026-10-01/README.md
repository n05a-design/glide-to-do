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
- **Unverändert:** `src/glide`, `07_Python-Versionen` und `pruefen.py`.

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
| Schriftmetrik, Layout oder Plattformverhalten unter Linux; einzeln nicht geklärt | `test_glide` (Kopfhöhe 44 statt 42 px), `test_mindestgroesse330` und `test_kompression330` (Text gekürzt), `test_rueckmeldung330` (Zeichenfläche springt), `test_features329` (Notizbuch-Zeichnung), `test_aufraeumen330` (zusätzlicher Menüeintrag „Neue Galerie“), `audit_app` (Ziehen in der Seitenleiste) |

Die Suiten sind auf den Referenz-Mac abgestimmt. Deshalb gehören sie vorerst nicht in die verpflichtende CI. Sie unter Linux zu kalibrieren, ist ein eigener Schritt (Entwicklungsplan, Zeile CI).

## Grenzen

- **Linux statt Referenz-Mac:** GitHub-Runner und dieser Container sind Linux mit Tk 8.6. Die Vollprüfung auf dem Mac bleibt maßgeblich.
- **Erster Lauf in GitHub Actions** erfolgt mit dem Pull Request; dessen Ergebnis steht im PR.
