# Zusammenführung 3.63.0 mit main 3.62.0

Stand 15.11.2026 · Glide 3.63.0 · Aufgabenformat 26

Nachweis zur Zusammenführung des lokalen Kandidaten 3.63.0 mit `main` 3.62.0. Einordnung, Umfang und Grenzen stehen im [QA-Bericht](../../../docs/07_QA_BERICHT.md#zusammenführung-3630-mit-main-3620-15112026).

- `grundstufe/ergebnis.json` und `grundstufe/systemkontext.json`: abschließende CI-Grundstufe, 19 von 19 Schritten, Exitcode 0.
- Gezielte Läufe ohne eigene Ergebnisdatei: `test_uiux_paket.py` (`nachabnahme363`, `b09`, `b12_b13`), `test_reminders.py`, `test_modalvertrag.py`, `test_abbauvertrag.py`, `test_dialog_theme.py`, jeweils Exitcode 0.

Umgebung: Windows 11, Python 3.15.1 / Tk 9.0.4, künstliche Daten mit `GLIDE_DATA_DIR`. Keine Vollprüfung, keine nativen Pakete, keine menschliche Sichtabnahme.
