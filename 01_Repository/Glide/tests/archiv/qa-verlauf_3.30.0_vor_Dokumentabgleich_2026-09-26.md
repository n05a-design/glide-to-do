# Langfristiger Prüfverlauf

Stand 26.09.2026 · Glide 3.30.0 · Datenformat 20


| Datum | Stand | Ergebnis | Nachweis |
|---|---|---|---|
| 19.09.2026 | 3.25.0 Abschluss, Windows/Python 3.13.15 | Exitcode 0 | [Protokoll](qa-3.25.0/abschluss/ergebnis.json) |
| 20.09.2026 | 3.26.0 vor Nachbesserung | Exitcode 1, einschließlich Timeout im Breitentest | [Protokoll](qa-3.26.0/vor_umsetzung_2026-09-20/ergebnis.json) |
| 20.09.2026 | 3.26.0 Nachbesserung, Schema 17 | In Arbeit; einzelne Regressionen bestanden, keine Gesamtfreigabe | [Suiten-Zwischenstand](qa-3.26.0/nachbesserung_2026-09-20/zwischenstand.json) |
| 21.09.2026 | 3.26.0 erster Abschlusslauf | Exitcode 1; zwei Testumgebungsfehler, anschließend gezielt korrigiert | [Original](qa-3.26.0/abschluss_2026-09-21/ergebnis.json) · [Nachprüfung](qa-3.26.0/abschluss_nachpruefung_2026-09-21/ergebnis.json) |
| 21.09.2026 | 3.26.0 abschließende Vollprüfung, Windows/Python 3.13.15 | **Exitcode 0**; 47 automatisierte Schritte erfolgreich, manuelle Sichtprüfung im Werkzeug übersprungen; gesonderte Windows-Bilder angesehen | [Protokoll](qa-3.26.0/abschluss_final_2026-09-21/ergebnis.json) · [QA-Bericht 3.26](../docs/archiv/07_QA_BERICHT_3.26.0_vor_3.28.0.md) |
| 23.09.2026 | 3.28.0 Schnellprüfung, Windows/Python 3.12.7 | Exitcode 1; neue Kern-, Tagebuch- und Vorlagentests gezielt bestanden, Gesamtlauf durch nicht lokal verfügbare OneDrive-Platzhalter und zwei Zeitüberschreitungen offen | [Protokoll](qa-3.28.0/abschluss_2026-09-23/ergebnis.json) · [QA-Bericht](../docs/07_QA_BERICHT.md) |
| 23.09.2026 | 3.28.0 Nachprüfung Gismo-Flackern und Ablage | Gezielte Regression bestanden; kein vollständiger Startseiten-Neuaufbau mehr, 40 Archivziele und 12 neue Ziele geprüft; Gesamtfreigabe weiterhin offen | [Nachprüfung](qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json) |
| 24.09.2026 | 3.29.0 Zeichnungsseite, Vollmodus, macOS/Python 3.14.5 | Exitcode 1; alle 35 Suiten und fünf Analysen bestanden, Altbefunde behoben; Reproduktionsabgleich an Listenzeitstempeln gescheitert, Normalisierung korrigiert | [Protokoll](qa-3.29.0/zeichnungsseite_2026-09-24/ergebnis.json) |
| 24.09.2026 | 3.29.0 Nachprüfung Vollmodus | **Exitcode 0**; 50 automatisierte Schritte bestanden, Bilder und Sichtprüfung plattformbedingt übersprungen | [Protokoll](qa-3.29.0/zeichnungsseite_nachpruefung_2026-09-24/ergebnis.json) |
| 24.09.2026 | 3.29.0 Abnahme nach Rückmeldung | Exitcode 1; 49 Schritte bestanden, zeitabhängige Layoutmessung in `test_ui_followup36` (3 Wiederholungen grün), Prüfung gehärtet | [Protokoll](qa-3.29.0/abnahme_2026-09-24/ergebnis.json) |
| 24.09.2026 | 3.29.0 Abnahme-Nachprüfung | **Exitcode 0**; 50 automatisierte Schritte bestanden, Bilder und Sichtprüfung plattformbedingt übersprungen | [Protokoll](qa-3.29.0/abnahme_nachpruefung_2026-09-24/ergebnis.json) |
| 25.09.2026 | 3.30.0 Modernisierung (Format 20), Vollmodus, macOS/Python 3.14.5 | **Exitcode 0**; 52 automatisierte Schritte bestanden (37 Suiten einschließlich `test_drawing330` und `test_features330`, fünf Analysen, Reproduktion von Beispiel- und Releasedaten), Bilder und Sichtprüfung plattformbedingt übersprungen | [Protokoll](qa-3.30.0/abschluss_2026-09-25/ergebnis.json) · [QA-Bericht](../docs/07_QA_BERICHT.md) |
| 25./26.09.2026 | 3.30.0 Ausbau, erster Vollmodus | Exitcode 1; 49 Schritte bestanden. `test_release37` und `test_reminders` lösten die neue Rückfallwarnung aus (Markierung jetzt erst mit echtem Inhalt); Release-Abgleich scheiterte am Tageswechsel (Momentdatum jetzt relativ verglichen) | [Protokoll](qa-3.30.0/ausbau_2026-09-25/ergebnis.json) |
| 26.09.2026 | 3.30.0 Ausbau, Nachprüfung | Exitcode 1; 51 Schritte bestanden, `test_ui_followup36` unter Last (Sichtbarkeit nach dem Scrollen; Prüfung auf den stabilen Endzustand gehärtet) | [Protokoll](qa-3.30.0/ausbau_nachpruefung_2026-09-26/ergebnis.json) |
| 26.09.2026 | 3.30.0 Ausbau, Abschlusslauf, macOS/Python 3.14.5 | **Exitcode 0**; alle 52 automatisierten Schritte bestanden, Bilder und Sichtprüfung plattformbedingt übersprungen | [Protokoll](qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json) · [QA-Bericht](../docs/07_QA_BERICHT.md) |
