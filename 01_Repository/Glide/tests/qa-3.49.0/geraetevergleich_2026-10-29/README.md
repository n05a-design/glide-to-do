# Gerätevergleich PC-01 / PC-02 / MacBook M2 und Korrekturen

Stand 29.10.2026 · Quelle 3.49.0 (Prüfkandidat) · Aufgabenformat 26 · App `39499ab3…` unverändert; geändert sind `glyph_metrics.py` und Prüfsuiten.

Auftrag 29.10.2026: Prüfläufe der drei Geräte vergleichen und einordnen; danach Prüfungsdokumente anpassen, die gefundenen Fehler beheben und die allgemeine Dokumentation prüfen. Arbeit im Hauptordner bei ruhender Codex-Fortsetzung. Kein Versionswechsel, keine Lieferung, kein Git.

## Einordnung

Rohbelege und Gerätebilanzen bleiben lokal in `13_TK-Test-Umgebung` (Git-ausgeschlossen); dort Befunde 1–14 im Vergleichsblatt.

| Fehlerbild | PC-02 Intel | PC-01 AMD | MacBook M2 | Ursache |
|---|---|---|---|---|
| Native Interpreterabbrüche und „unmögliche“ Python-Fehler (WA-41A) | wiederholt, 27.10. und 29.10. | nie (10/10 grün, gleiche Quelle und gleicher Python-Build) | nie | **Prüfplatz PC-02** |
| Testneustart ohne regulären Sitzungsabschluss | FP-01-Baseline | `test_ui_updates` (2×) | 14 Suiten | Prüfadapter |
| `⚑⚑` erreicht `ord()` in `glyph_metrics` | latent | nicht erreicht | 3 Suiten | Glide-Code |
| JPEG vor angeforderter Umwandlung abgefragt | – | – | 1 Suite | Testaufruf |
| Ablagepfad über 130 Zeichen | – | 14 Fachtests (09:09) | – | Prüfumgebung |

PC-02 ist systemweit instabil: laut Ereignisprotokoll seit Juli acht Bluescreens mit wechselnden Stoppcodes, 13 unerwartete Neustarts, seit 01.10. Abstürze auch unabhängiger Programme und 32 WHEA-19-Meldungen, 30 davon vom selben Kern (APIC 41). Ein CPU-, RAM- oder Firmwaredefekt ist ohne kontrollierte Gegenprobe nicht bewiesen; Glide-Code als Ursache von WA-41A ist durch den AMD-/Mac-Vergleich jedoch nicht gestützt. BIOS/CPU bleiben nach Nutzerentscheidung unverändert.

## Korrekturen

1. **`glyph_metrics.ink_center`** misst mehrzeichige Symbole über die gemeinsame Höhe aller Zeichen mit Umriss; Leerzeichen und leere Texte liefern weiterhin keine Verschiebung. `⚑⚑` steht damit wie `⚑`. Neuer Unit-Fall `test_multi_character_symbols_use_their_common_height`. Tk-frei (D17), kein Formatwechsel.
2. **Regulärer Sitzungsabschluss in Neustart-Suiten:** vor jeder regulären Sperrfreigabe `getattr(app, "finish_recovery_session", lambda: None)()`, auch in Kindprozess-Skripten; kompatibel zu Vergleichsquellen ohne Sitzungsschutz. 35 Stellen in 14 Suiten plus zwei in `test_oberflaeche33321`. `test_tagpaket33314` eröffnet nach dem Wiederbelegen der Sperre eine eigene neue Sitzung. Fachassertions und absichtlich unsaubere Abbruch-/Wiederanlauffälle unverändert. Regel im [Prüfplan](../../../docs/05_QA_TESTPLAN.md#regeln).
3. **`test_befunde330`** fordert wie `drawing_load_reference` zuerst `request_conversion` an und liest danach den fertigen Cache.

## Gezielte Prüfung auf PC-02

Python 3.14.7, Tk 9.0.4, je Suite eigener Prozess und eigenes temporäres `GLIDE_DATA_DIR`, Bytecode aus. Keine Speicherlastsuite, kein Volllauf. [Bilanz](ergebnis.json).

- 1.075 Fachtests grün (bisher 1.074 plus neuer Glyphenfall).
- Alle 18 betroffenen Suiten mit Korrekturen grün: drei Glyphensuiten, `test_befunde330` und die 14 Neustart-Suiten. Im ersten Lauf waren es 17; `test_oberflaeche33321` hatte einen eigenen Neustarthelfer ohne Abschluss, auf dem Mac vom Glyphenfehler verdeckt. Nach dieser Nachkorrektur einzeln grün.
- Rote Gegenproben der Vorfassungen: altes `glyph_metrics` scheitert mit `ord() expected a character, but string of length 2 found`; alte `test_workspace310` und `test_suche3337` scheitern unter Windows an denselben Stellen wie auf dem M2. Die Neustartlücke ist damit plattformunabhängig belegt.

## Speicherlast-Serie auf PC-02 (Nutzerauftrag)

Auf ausdrücklichen Wunsch „den Test, der am Intel-PC sonst immer rot läuft, mehrmals“: unveränderte `test_speicherlast330.py` fünfmal nacheinander über `gesichert_pruefen.py --art speicherlast`, je eigene eingefrorene Prüfkopie außerhalb OneDrive, Python 3.14.7, Zeitlimit 900 s, keine Wiederholung bis grün. 17:26–17:40 Uhr.

**Ergebnis: 5 von 5 grün** (157–169 s je Lauf einschließlich Einfrieren). Jeder Lauf: 26.420 Punkte/28,5 MB, 40 Änderungsrunden verlustfrei, sechs harte Schreiberabbrüche ohne halbe Datei, Sperre, Sicherungen, Startprüfung. Keine Absturz-, Assertion- oder Tracebackzeile, keine WHEA-Meldung und kein Anwendungsabsturz im Ereignisprotokoll während der Serie. App `39499ab3…`.

**Einordnung:** Das ist der bisher längste grüne Abschnitt dieser Suite auf PC-02, aber kein Nachweis einer Behebung. WA-41A trat dort immer sporadisch auf; mit Python 3.14.7 waren frühere Vollsuiten teils grün, und am selben Morgen brach der CI-Lauf unter 3.14.7 an anderer Stelle nativ ab. Keine Korrektur dieser Sitzung zielt auf WA-41A. Fünf Läufe sind zu wenige, um eine Ausfallrate oder ihre Änderung zu belegen. [Serie](ergebnis.json), Feld `speicherlast_serie`.

## Grenzen

- PC-02 ist der instabile Prüfplatz. Grüne Läufe hier sind kein Stabilitätsbeleg; Gegenlauf auf PC-01 und M2 bleibt offen.
- Der JPEG-Zweig ist nur unter macOS mit `sips` aktiv und lief hier nicht.
- Keine eingefrorene Prüfkopie, kein Volllauf, keine native/Menschenabnahme. `test_seitenkarten` auf dem M2 (minutenlanger Schriftaufbau) bleibt ungeklärt.
- Weitere Prüfhelfer mit direktem Abbau ohne Abschluss (`test_glide`, `test_tag3390`, `test_zugang400`) sind auf allen Geräten grün und blieben unverändert; nur bei tatsächlichem Fehlbild nachziehen.
- Rohlogs mit lokalen Pfaden bleiben lokal. Python-Lieferung 3.47.0, native Pakete 3.45.0.
