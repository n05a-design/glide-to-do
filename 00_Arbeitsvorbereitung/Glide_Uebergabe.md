# Glide – Übergabe an eine neue Sitzung

Stand 14.11.2026 · Glide 3.61.0 · Aufgabenformat 26

Einstieg für die nächste Sitzung: tatsächlicher Stand, nächste Schritte, Regeln. Aufgaben und Rest führt der [Entwicklungsplan](Glide_Entwicklungsplan.md), Prüfergebnisse der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Entscheidungen die [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md). Am 14.11.2026 auf den aktuellen Stand gekürzt; frühere Übergabestände trägt Git.

## 1. Tatsächlicher Stand

| Achse | Stand |
|---|---|
| Version | **Glide 3.61.0** (Aufgabenformat **26**, Einstellungen **2**, Vorlagen **2**) setzt auf `main` `b362abca` (3.60.0 mit PR #82–#84) auf. Umfang im [Plan §21.92](Glide_Entwicklungsplan.md#2192-glide-3610-lücken-geschlossen-und-design-richtlinien-zusammengeführt-14112026) |
| Neu in 3.61.0 | Entlastungsdialog nennt Überlastungsgründe (D81); nicht erreichbarer Datenordner wird gemeldet, Zeiger mit BOM gilt wieder (D82); Suche findet zerlegte Umlaute; Design Richtlinien mit Gestaltungsregister und verbindlichen Marktlehren (D83) |
| Prüfung | Lokal unter macOS arm64 mit Python 3.14.5 und Tk 9.0; Ergebnisse und Grenzen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#prüfstand-3610-14112026). Linux- und Windows-Vollprüfung laufen auf GitHub zum PR |
| Vorstand 3.60.0 | Auf `b362abca` sind Grundstufe und Linux-Vollprüfung grün; Windows-Paket, macOS-Paket und Zugangsprüfung siehe [Technische Vollprüfung 3.60.0](../01_Repository/Glide/docs/07_QA_BERICHT.md#technische-vollprüfung-3600-auf-pc02-14112026) |
| Lieferung | `07_Python-Versionen` per `abgleich_07.py` SHA-256-gleich zur Quelle; eigenständige Pakete für 3.61.0 entstehen erst in den GitHub-Workflows |
| Lokale Ablage | Die OneDrive-Hauptablage wurde am 14.11.2026 auf GitHub-`main` `b362abca` gesetzt (GitHub hat Vorrang). Commits entstehen in frischen Klonen außerhalb von OneDrive |

## 2. Zuständige Dokumente

| Thema | Verbindliche Quelle |
|---|---|
| Aufgaben, Arbeitsvorrat, Rest | [Entwicklungsplan](Glide_Entwicklungsplan.md#aktueller-arbeitsvorrat), Runde [§21.92](Glide_Entwicklungsplan.md#2192-glide-3610-lücken-geschlossen-und-design-richtlinien-zusammengeführt-14112026) |
| Entscheidungen D01–D83 und Arbeitsablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Gestaltung | [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) mit [Gestaltungsregister](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md#gestaltungsregister) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Prüf- und Lieferstände | [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) |
| Technische Befunde | [Analyse §13.36](Glide_Analyse.md#1336-gesamtaudit-gegen-code-und-dokumentation-14112026) |
| Markt und Konkurrenz | [Markt §16](Glide_Markt_und_Vorbilder.md#16-nachrecherche-vom-12-und-14112026) |
| Regeln und Pflege | [AGENTS](../01_Repository/Glide/AGENTS.md), [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |

## 3. Nächste Arbeit und offene Entscheidungen

1. PR zu 3.61.0 prüfen und mergen (Inhaber). Linux- und Windows-Vollprüfung sowie das macOS-Paket dem Merge-Commit zuordnen.
2. Menschliche Abnahme am Mac: Entlastungsdialog mit Gründen, Meldung bei nicht eingebundenem Datenlaufwerk, Suche nach Text mit zerlegten Umlauten; offene Bedien-, Sicht- und DPI-Fälle stehen in der [Prüfliste](Glide_Manuelle_Pruefung.md).
3. Marktvorschläge neu reihen (WA-08, WA-20, WA-12-Rest, WA-53 bis WA-59): Inhaberentscheidung, Vorlage im [Arbeitsvorrat](Glide_Entwicklungsplan.md#aktueller-arbeitsvorrat).
4. Shell-Migration: zuerst der Modal-Vertragstest mit echtem Grab, dann jedes Folgepaket mit eigener Freigabe ([Plan §21.89](Glide_Entwicklungsplan.md#2189-glide-3600-erste-shell-schnitte-start-baseline-und-beruhigter-einstellungsdialog-13112026)).
5. Die sechs D83-Regeln bei jedem UI-Paket anwenden, das den Bereich anfasst; bestehende Oberflächen nicht ungefragt umbauen.
6. Inhaberangaben I1, Signierung I3, Markenprüfung I4 und Releasefreigabe I11 bleiben offen; Screenreader-Abnahme nach D58 zurückgestellt.

## 0. Sofortübergabe WA-41 – zuerst lesen

Diese Überschrift bleibt als bestehendes Linkziel erhalten. Sie betrifft die historische Fehleruntersuchung; aktuelle Entwicklungsprioritäten stehen in Abschnitt 3.

- **WA-41A:** sporadische Interpreter-/Prozessfehler auf PC-02 Intel, unter anderem `0xC0000005`, `0xC0000409`, „Executing a cache“. WHEA-/Systembefunde sind eine Spur, kein bewiesener CPU-Defekt. **WA-41B:** einmal abweichender gespeicherter/geladener künstlicher Bestand; konkrete Felder und Ursache ungeklärt, kein belegter Verlust echter Nutzerdaten. Beide Spuren getrennt erhalten.
- Zehn isolierte AMD-Prozesse waren grün; vollständige Suiten erzeugten UUIDs/Zeitstempel selbst. Kein byteidentischer Intel-Replay und kein Ursachenbeweis. [AMD-Nachweis](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/amd_vergleich_2026-10-27/README.md), [Gerätevergleich](https://github.com/n05a-design/glide-to-do/blob/f1a5b5b6e0f97f2b5eab1ac552999c33c6416e69/01_Repository/Glide/tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md).
- BIOS-/CPU-Einstellungen nicht ändern, keine unnötige neue Stressserie am instabilen PC-02. Keine spekulative Mengenschranke, kein Chunking oder `gc.collect()` als angeblicher Fix. Historischen Referenzstand und Originalkriterien bewahren.
- [Ursachenanalyse](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/wa41_2026-10-27/README.md), [Python-Vergleich](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/python315_vergleich_2026-10-27/README.md), [WHEA-/Lastbefunde und Dumpinventar](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json), [470-Dateien-Referenz](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Spätere Schutzfunktionen und Lieferung schließen diese Ursachenfragen nicht.
- Geschützte lokale Eingänge: `01_Repository/Glide/tests/qa-3.48.0/lokale_belege/eingang/initial.json` und `lokale_belege/minidumps/`; [Sicherungsmanifest](https://github.com/n05a-design/glide-to-do/blob/594f4c85eb60370a44282b06fcb8017df8181d70/01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Anfangsbestand 28.548.872 Bytes, SHA-256 `a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4`. Acht bekannte Minidumps sind keine FullMemory-Aufnahmen. Ein früher genannter externer Exportordner wurde nicht lokal bestätigt; keine Originale aufgrund dieser Angabe löschen.
- Dumps, Rohlogs und lokale Eingänge bleiben Git-ausgeschlossen und sind bei Rechnerwechsel ausdrücklich geschützt zu übertragen. Temporärpfade und Runtimeorte aus alten Berichten vor Wiederverwendung prüfen; Version, `sys.executable`, Tk und Binärhashes erfassen. Standardbefehl `python` ist kein Laufzeitnachweis.

## 5. Arbeits- und Prüfregeln

- Deutsch in Antworten und Dokumenten. Produktidentitäten und Datenpfade stabil halten; neue Fachlogik nach D17 Tk-frei.
- Vor Testimporten temporären `GLIDE_DATA_DIR` setzen. Kurze lokale Prüfpfade außerhalb OneDrive; keine echten Nutzerdaten oder ungesicherten Arbeitskopien verändern.
- Ergebnisse gelten für konkrete Quell-/Test-/Fixture-/Ressourcenbytes und Runtime. Originalrote, Skips, Stoppfolgen, Teilprüfungen, Lieferung und Menschenabnahme getrennt nennen.
- Vor dem Commit CI-Grundstufe, Stand-/Link-/Datenschutz-/Lieferprüfung. Rohlogs und persönliche Pfade nicht veröffentlichen.
- Ein Thema, ein Dokument. Historische Eingänge, Originalbilder, Lizenztexte, Migrationsfixtures und aktuelle QA-Nachweise nach ihrem Zweck erhalten. Ältere reproduzierbare QA-Ablage nur nach Manifest und fester Git-Zuordnung gemäß Pflegevertrag kürzen.
- [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) und [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) bleiben Eingangsreferenzen; teilweise personenbezogene Originalbilder bleiben lokal und müssen bei Übergaben ausdrücklich mitgegeben werden.
