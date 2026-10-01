# Langfristiger Prüfverlauf

Stand 23.09.2026 · Glide 3.28.0 · Datenformat 18


| Datum | Stand | Ergebnis | Nachweis |
|---|---|---|---|
| 19.09.2026 | 3.25.0 Abschluss, Windows/Python 3.13.15 | Exitcode 0 | [Protokoll](qa-3.25.0/abschluss/ergebnis.json) |
| 20.09.2026 | 3.26.0 vor Nachbesserung | Exitcode 1, einschließlich Timeout im Breitentest | [Protokoll](qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json) |
| 20.09.2026 | 3.26.0 Nachbesserung, Schema 17 | In Arbeit; einzelne Regressionen bestanden, keine Gesamtfreigabe | [Suiten-Zwischenstand](qa-3.26.0/nachbesserung_2026-09-20/zwischenstand.json) |
| 21.09.2026 | 3.26.0 erster Abschlusslauf | Exitcode 1; zwei Testumgebungsfehler, anschließend gezielt korrigiert | [Original](qa-3.26.0/abschluss_2026-09-21/ergebnis.json) · [Nachprüfung](qa-3.26.0/abschluss_nachpruefung_2026-09-21/ergebnis.json) |
| 21.09.2026 | 3.26.0 abschließende Vollprüfung, Windows/Python 3.13.15 | **Exitcode 0**; 47 automatisierte Schritte erfolgreich, manuelle Sichtprüfung im Werkzeug übersprungen; gesonderte Windows-Bilder angesehen | [Protokoll](qa-3.26.0/abschluss_final_2026-09-21/ergebnis.json) · [QA-Bericht 3.26](../docs/archiv/07_QA_BERICHT_3.26.0_vor_3.28.0.md) |
| 23.09.2026 | 3.28.0 Schnellprüfung, Windows/Python 3.12.7 | Exitcode 1; neue Kern-, Tagebuch- und Vorlagentests gezielt bestanden, Gesamtlauf durch nicht lokal verfügbare OneDrive-Platzhalter und zwei Zeitüberschreitungen offen | [Protokoll](qa-3.28.0/abschluss_2026-09-23/ergebnis.json) · [QA-Bericht](../docs/07_QA_BERICHT.md) |
| 23.09.2026 | 3.28.0 Nachprüfung Gismo-Flackern und Ablage | Gezielte Regression bestanden; kein vollständiger Startseiten-Neuaufbau mehr, 40 Archivziele und 12 neue Ziele geprüft; Gesamtfreigabe weiterhin offen | [Nachprüfung](qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json) |
