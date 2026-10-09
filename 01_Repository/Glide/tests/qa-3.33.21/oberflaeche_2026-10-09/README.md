# Paket Ruhige Oberfläche 3.33.21 – Prüfung und Lieferung (09.10.2026)

Stand 09.10.2026 · Glide 3.33.21 · Referenz-Mac, Python 3.14.5 (python.org), Tk 9.0.3 · künstliche Daten, isolierter `GLIDE_DATA_DIR`

Paket 3 des Sprints (Entwicklungsplan §15): N01, U15, U05r, U09, U18, OB05, OB01r, W05; W07/W08 nachgestellt.

**Gezielte Prüfung vor dem Volllauf (Hintergrundmodus, Netzbetrieb):** Pflichtsuite `test_oberflaeche33321` grün, Gegenprobe gegen die ausgelieferte 3.33.20 rot (Designreihenfolge). Grün außerdem `test_kontrast330`, `test_mindestgroesse330`, `test_fenster330`, `test_festlayout330`, `test_aufraeumen330`, `test_features322`, `test_features324`, `test_features328`, `test_features329`, `test_features330`, `test_drawing330`, `test_bilder330`, `test_workspace310`, `test_startseite3332`, `test_seiten330`, `test_seiten33318`, `test_editor3338`, `test_notizbereich330`, `test_wissen33315`, `test_tempo33319`, `test_bereiche3331`, `test_klappmechanismen3321`, `test_heute3336`, `test_glide`, `test_bedienung33316`, `test_titel33312`, `test_features323`, `test_eingabe3333`, `test_features318`; 223 Unit-Tests. Angepasste Bestandserwartungen: offene Ansicht und Pinnwandschalter in der Rolle `active` (`test_aufraeumen330`, `test_features322`, `test_features324`), „Vorschau“/„Auto anheften“ im Menü „…“ (`test_features322`), Anordnung in der Schalterzeile (`test_workspace310`).

**Nachstellprobe W05/W07/W08** (eigener Prozess, Fensterfotos lokal):

| Befund | 3.33.20 | 3.33.21 |
|---|---|---|
| W05 „Tabellenspalten“ | 1251 px breit, Knöpfe links | 520 px, Knöpfe rechts |
| W05 „Für KI bereitstellen“ | 1504 px breit, Knöpfe links | 620 px, Knöpfe rechts |
| W07 „PNG auf 128 × 128 einpassen“ nach „Ganzes Bild zeigen“ | Hinweis einmal | unverändert – auf dem Mac nicht nachstellbar |
| W08 „Pixelsymbol“ | Raster füllt den Dialog (Zoom 32×) | unverändert – auf dem Mac nicht nachstellbar |

Ursache W05: Dialogtexte begannen ohne Umbruchbreite und forderten die volle Textlänge an. W07 und W08 bleiben für die Windows-Sichtprüfung B1a.

**OB01r** ([vorher](messungen/abstaende_vorher.json), [nachher](messungen/abstaende_nachher.json), `tests/tools/design_inventory.py`): direkte Abstandszahlen in Startseite, Bibliothek, Einstellungen und Schnellerfassung 134 → 3; die Menge der verwendeten Werte ist je Ansicht unverändert, sichtbar ändert sich nichts.

| Schritt | Ergebnis |
|---|---|
| [Vorlauf](voll_vorlauf/ergebnis.json) | Exitcode 1: 94 ausgeführt, 2 rot – beide Prüfwerkzeuge, App-Code unverändert: `test_wissen33315` startete die von der Aufbewahrung entfernte Vorversion 3.33.14 (A18), `test_tempo33319` zählte einen Sekundenwechsel als zweites Sperrschreiben (A19) |
| [Vollprüfung](voll/ergebnis.json) | nach W14/W15 auf neu eingefrorener Kopie (App-Quellen unverändert): Exitcode 0, 96 ausgeführt, 2 übersprungen (Linux-Aufnahmen, menschliche Sichtprüfung); 79 Integrationssuiten |
| Python-Lieferung | `abgleich_07.py`: 33 Code-Dateien und 131 Ressourcen, keine Abweichung; Hauptdatei 3.33.20 ins Archiv (sieben Versionen) |
| Showcase | `showcase_abgleich.py` Exit 0 |
| [Bundle](bundle.json) | `build/macos/Glide.app` 3.33.21, Ad-hoc-Signatur geprüft, 79 Dateien, alle Code- und Ressourcendateien SHA-256-gleich zu 07 |

Windows-Vollprüfung, Windows-Sichtprüfung zu W07/W08 und menschliche Abnahme (I6) offen; Rohprotokolle und Fensterfotos blieben lokal.
