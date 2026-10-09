# Paket Komfort 3.33.20 – Prüfung und Lieferung (09.10.2026)

Stand 09.10.2026 · Glide 3.33.20 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Paket 2 des Sprints (Entwicklungsplan §15): KO02, KO03, KO05, KO06, U04, U20, N07, AB08, AU06 und die Befunde A16/A17 der Analyse.

**Gezielte Prüfung vor dem Volllauf (Hintergrundmodus, Akkubetrieb):** Pflichtsuite `test_komfort33320` grün, Gegenprobe gegen die ausgelieferte 3.33.19 rot (Menüeintrag „Diesen Termin überspringen“ fehlt). Grün außerdem `test_glide`, `test_features330`, `test_eingabe3333`, `test_heute3336`, `test_klappmechanismen3321`, `test_reminders`, `test_bedienung33316`, `test_planen33313`, `test_features311`, `test_features325`, `test_datenintegritaet`, `test_startseite3332`, `test_tempo33319`, `test_features321`, `test_mindestgroesse330`, `test_kontrast330`; 216 Unit-Tests. Zwei Testerwartungen in `test_features330` wurden auf U20 umgestellt (kein zweiter Anlegeknopf unter sichtbarer Eingabezeile, Notizbuch behält seinen Weg); dabei fiel auf, dass die Entscheidung am Zeichenstand hing – sie folgt jetzt der Ansicht.

**AB08 Startprobe:** `glide_start.py` mit dem System-Python 3.9.6 weist mit Exitcode 1 und Meldung ab, ohne den Datenordner anzulegen; der Bytecode-Cache wird vor der Prüfung umgelenkt, damit im signierten Bundle nichts entsteht.

| Schritt | Ergebnis |
|---|---|
| [Vollprüfung](voll/ergebnis.json) | eingefrorene Kopie außerhalb von OneDrive, Akkubetrieb: Exitcode 0, 95 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung); 78 Integrationssuiten |
| Python-Lieferung | `abgleich_07.py`: 32 Code-Dateien und 131 Ressourcen, keine Abweichung; Hauptdatei 3.33.19 ins Archiv (sieben Versionen) |
| Showcase | `showcase_abgleich.py` Exit 0, nach `05_Probelisten_Testdaten/Showcase` übernommen |
| [Bundle](bundle.json) | `build/macos/Glide.app` 3.33.20, Ad-hoc-Signatur geprüft, 78 Dateien, alle Code- und Ressourcendateien SHA-256-gleich zu 07 |

Windows-Vollprüfung und menschliche Abnahme (I6) offen; Rohprotokolle blieben lokal.
