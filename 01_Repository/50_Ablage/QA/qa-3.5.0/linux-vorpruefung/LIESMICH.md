# Protokoll der Vorprüfung 3.5.0 (Linux)

Erzeugt mit `tests/tools/pruefen.py --modus schnell` unter Linux,
Python 3.12.3, Tcl/Tk 8.6, isoliertes `GLIDE_DATA_DIR`.

**Das ist eine Vorprüfung, nicht die Abnahme.** `ergebnis.json` meldet
"FEHLGESCHLAGEN" – ausschließlich wegen zweier Dokumentverweise, deren Ziele in
der Arbeitskopie fehlten, nicht im Projekt selbst:

- `docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md`
- `tests/fixtures/archiv/glide_releaseplanung_3.2.0.glidebackup`

Beide liegen auf dem Windows-Rechner. Alles Übrige lief mit Exitcode 0: Syntax,
Versionskonsistenz, Fixtures, fünf Suiten, zwei Analysen.

Die maßgebliche Abnahme ist der Windows-Vollmodus:

    & 'C:\Python312\python.exe' tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.5.0/abschluss
