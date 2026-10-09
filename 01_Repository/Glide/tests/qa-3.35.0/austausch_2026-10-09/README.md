# Pakete Pixel und Austausch 3.35.0 – Prüfung und Lieferung (09.10.2026)

Stand 09.10.2026 · Glide 3.35.0 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Pakete 5 und 6 des Sprints (Entwicklungsplan §15), gemeinsam in einem Volllauf: G19, G-03, G24, F-03.

**Gezielte Prüfung vor dem Volllauf (Hintergrundmodus, Netzbetrieb):** Pflichtsuiten `test_pixel3350` und `test_austausch3350` grün, Gegenprobe beider gegen die ausgelieferte 3.34.0 rot (keine Vorschau vor dem Umfärben; kein Kontextpaket). Grün außerdem `test_etappe1_332` (an die Symbolvorschau angepasst), `test_features330`, `test_drawing330`, `test_features323`, `test_features316`, `test_oberflaeche33321`, `test_wissen3340`, `test_glide`, `audit_app`, `test_kontrast330`, `test_fenster330`, `test_mindestgroesse330`; 257 Unit-Tests. Befund beim Prüfen: Ein dritter Klick auf die Farbleiste passte ebenfalls auf die Doppelklick-Bindung und öffnete den Dialog erneut; behoben (Dreifachklick abgefangen, in der Suite geprüft).

| Schritt | Ergebnis |
|---|---|
| [Vollprüfung](voll/ergebnis.json) | Exitcode 0: 99 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung); 82 Integrationssuiten |
| Python-Lieferung | `abgleich_07.py`: 37 Code-Dateien und 131 Ressourcen, keine Abweichung; Hauptdatei 3.34.0 ins Archiv (sieben Versionen) |
| Showcase | `showcase_abgleich.py` Exit 0 |
| [Bundle](bundle.json) | `build/macos/Glide.app` 3.35.0, Ad-hoc-Signatur im Bauordner und auf einer Rückkopie geprüft, 82 Code- und Ressourcendateien SHA-256-gleich zu 07 |

Windows-Vollprüfung und menschliche Abnahme (I6) offen; Rohprotokolle blieben lokal.
