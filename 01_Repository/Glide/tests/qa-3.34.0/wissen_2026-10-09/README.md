# Paket Wissen und Seiten 3.34.0 – Prüfung und Lieferung (09.10.2026)

Stand 09.10.2026 · Glide 3.34.0 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Paket 4 des Sprints (Entwicklungsplan §15): B4, G14h, P07, D-03, H-02r, N08.

**Gezielte Prüfung vor dem Volllauf (Hintergrundmodus, Netzbetrieb):** Pflichtsuite `test_wissen3340` grün, Gegenprobe gegen die ausgelieferte 3.33.21 rot (Bilder überlappen). Grün außerdem `test_bilder330`, `test_seiten330`, `test_seiten33318`, `test_suche3337`, `test_bereiche3331`, `test_klappmechanismen3321`, `test_workspace310`, `test_eisenhower3335`, `test_wissen33315`, `test_features311`, `test_tempo33319`, `test_kontrast330`, `test_mindestgroesse330`, `test_fenster330`; 243 Unit-Tests.

**P07 Suche** (`scripts/pflege/messung_suche.py`, 10.000 Punkte in 50 Listen, 200 Seiten mit je rund 2.000 Zeichen, sieben Begriffe, je neun warme Runden, Netzbetrieb; gemessen an den eingefrorenen Ständen):

| Stand | Median | p95 | Regel |
|---|---|---|---|
| [3.33.21](messungen/suche_3.33.21.json) | 100,8 ms | 131,7 ms | an der Grenze; nach Plan wäre FTS5 fällig |
| [3.34.0](messungen/suche_3.34.0.json) | 66,6 ms | 73,1 ms | unter 100 ms: kein FTS5-Index (P07 ✕) |

Ursache laut Profil: Der Textausschnitt jedes Inhaltstreffers normalisierte jedes Zeichen einzeln (rund 950.000 Aufrufe je fünf Eingaben). Seit 3.34.0 bildet eine Halbierungssuche die Trefferposition ab; ein Unit-Test vergleicht 400 Zufallstexte mit der früheren Fassung.

| Schritt | Ergebnis |
|---|---|
| [Vollprüfung](voll/ergebnis.json) | Exitcode 0: 97 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung); 80 Integrationssuiten |
| Python-Lieferung | `abgleich_07.py`: 35 Code-Dateien und 131 Ressourcen, keine Abweichung; Hauptdatei 3.33.21 ins Archiv (sieben Versionen) |
| Showcase | `showcase_abgleich.py` Exit 0 |
| [Bundle](bundle.json) | `build/macos/Glide.app` 3.34.0, Ad-hoc-Signatur im Bauordner und auf einer Rückkopie geprüft, 80 Code- und Ressourcendateien SHA-256-gleich zu 07 |

Windows-Vollprüfung, Linux-Sichtprüfung zu N08 und menschliche Abnahme (I6) offen; Rohprotokolle blieben lokal.
