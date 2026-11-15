# Glide – Übergabe an eine neue Sitzung

Stand 15.11.2026 · Glide 3.63.2 · Aufgabenformat 26

Einstieg für die nächste Sitzung: tatsächlicher Stand, nächste Schritte, Regeln. Aufgaben und Rest führt der [Entwicklungsplan](Glide_Entwicklungsplan.md), Prüfergebnisse der [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Entscheidungen die [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md). Am 14.11.2026 auf den aktuellen Stand gekürzt; frühere Übergabestände trägt Git.

## Korrekturversionen 3.63.1 und 3.63.2 (15.11.2026)

Behebt die Befunde des CI-Volllaufs 3.63.0: veraltete Glyphenerwartungen in Tests, Anzeigeknopf im Zeicheneditor nur mit Profilnamen („Standard ▾“), flüssiges Scrollen trotz Zeilenbändern, gemeinsame D84-Dreieckzeichen ausdrücklich erlaubt, in 3.63.2 Kompaktkopf einheitlich 28 px und Bereichspfeile auch unter Linux auf der Kappenmitte. Lokaler Volllauf grün (Windows/Tk 9, künstliche Daten); Linux-CI, native Matrix, Pakete und Sichtabnahme offen. Auftrag im [Plan §21.99](Glide_Entwicklungsplan.md#2199-korrekturversionen-3631-und-3632-nach-dem-ci-volllauf-15112026), Befunde im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#korrekturversionen-3631-und-3632--ci-volllauf-15112026).

## Lokaler Kandidat 3.63.0 (15.11.2026)

Nachabnahme D85: größere Bereichs-/Navigationsmarker, randlose Zeilenaktionen mit durchgehenden Zuständen, Alle bis morgen 09:00 Uhr, vier Profile im Zeicheneditor und korrigierte Tabellenkopfbedienung. Auftrag und Abgrenzung im Plan §21.97; finale Laufbefunde im Nachabnahme-QA.

Inhaberwahl B / D84: kleine, gefüllte Dreiecke für Seitenleistenbereiche, Angeheftet, Ordner und Auswahlfelder, passende Größen je Schriftrolle. Quelle und Python-Lieferung tragen 3.63.0, Aufgabenformat 26; Systemkatalog V1.29. Auftrag und Rest im [Plan §21.96](Glide_Entwicklungsplan.md#2196-kleine-gefüllte-dreiecke-und-version-3630-15112026), Prüfbefunde und Grenzen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#prüfstand-3630--dreieckmarker-15112026). Native Pakete, Plattformmatrix und menschliche Sichtabnahme bleiben offen. Der Kandidat entstand auf 3.60.0 (`b362abca`) und ist am 15.11.2026 mit `main` 3.62.0 (`e29439db`) zusammengeführt; dabei wurden die Kennungen auf D84/D85, §21.96/§21.97 und V1.28/V1.29 gehoben. Die Tabelle in §1 beschreibt den Unterbau 3.62.0.

## 1. Tatsächlicher Stand

| Achse | Stand |
|---|---|
| Version | **Glide 3.63.2** (Aufgabenformat **26**, Einstellungen **2**, Vorlagen **2**) auf Branch `claude/glide-3-63-2` zum Merge vorgelegt; `main` trägt 3.63.1 (PR #96) und die Shell-Entscheidungen D86–D90 (PR #97). Umfang im [Plan §21.99](Glide_Entwicklungsplan.md#2199-korrekturversionen-3631-und-3632-nach-dem-ci-volllauf-15112026) |
| Neu in 3.63.x | Gefüllte Dreiecke (D84), randlose Zeilenaktionen, Alle bis morgen, Zeichen-Anzeigeprofile (D85); 3.63.1/3.63.2: Anzeigeknopf „Standard ▾“, flüssiges Scrollen mit Zeilenbändern, Kompaktkopf 28 px, Bereichspfeile unter Linux ausgerichtet |
| Neu in 3.62.0 | Erster Shell-Baustein: Jeder modale Dialog wartet über `modal_session.py`; `ListApp.run_modal` und Verwandte sind Fassaden. Sichtbares Verhalten unverändert |
| Prüfung | 3.63.2 lokal: Volllauf und CI-Grundstufe grün unter Windows 11, Python 3.15.1/Tk 9, künstliche Daten ([QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#korrekturversionen-3631-und-3632--ci-volllauf-15112026)). Linux-Vollprüfung auf GitHub für 3.63.2 steht aus; 3.63.1 stoppte dort nur noch an b09 |
| Lieferung | `07_Python-Versionen` per `abgleich_07.py` SHA-256-gleich zur Quelle 3.63.2; eigenständige Pakete entstehen erst in den GitHub-Workflows |
| Lokale Ablage | Die OneDrive-Hauptablage wurde am 14.11.2026 auf GitHub-`main` `b362abca` gesetzt (GitHub hat Vorrang). Commits entstehen in frischen Klonen außerhalb von OneDrive |

## 2. Zuständige Dokumente

| Thema | Verbindliche Quelle |
|---|---|
| Aufgaben, Arbeitsvorrat, Rest | [Entwicklungsplan](Glide_Entwicklungsplan.md#aktueller-arbeitsvorrat), Runde [§21.92](Glide_Entwicklungsplan.md#2192-glide-3610-lücken-geschlossen-und-design-richtlinien-zusammengeführt-14112026) |
| Entscheidungen D01–D90 und Arbeitsablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Gestaltung | [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) mit [Gestaltungsregister](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md#gestaltungsregister) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Prüf- und Lieferstände | [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) |
| Technische Befunde | [Analyse §13.36](Glide_Analyse.md#1336-gesamtaudit-gegen-code-und-dokumentation-14112026) |
| Markt und Konkurrenz | [Markt §16](Glide_Markt_und_Vorbilder.md#16-nachrecherche-vom-12-und-14112026) |
| Regeln und Pflege | [AGENTS](../01_Repository/Glide/AGENTS.md), [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |

## 3. Nächste Arbeit und offene Entscheidungen

1. 3.63.2 nach `main` bringen und der Linux-/Windows-Vollprüfung sowie den Paketen auf GitHub zuordnen (Inhaber). Die Repository-Regel „Changes must be made through a pull request“ sperrt derzeit Aktualisierungen bestehender Zweige; Beschränkung auf `main` empfohlen.
2. Menschliche Abnahme am Mac: Entlastungsdialog mit Gründen, Meldung bei nicht eingebundenem Datenlaufwerk, Suche nach Text mit zerlegten Umlauten; offene Bedien-, Sicht- und DPI-Fälle stehen in der [Prüfliste](Glide_Manuelle_Pruefung.md).
3. Marktvorschläge neu reihen (WA-08, WA-20, WA-12-Rest, WA-53 bis WA-59): Inhaberentscheidung, Vorlage im [Arbeitsvorrat](Glide_Entwicklungsplan.md#aktueller-arbeitsvorrat).
4. Shell-Migration: Seit 3.62.0 wartet jeder modale Dialog über `modal_session.py` (Paket 3a, [Plan §21.94](Glide_Entwicklungsplan.md#2194-glide-3620-shell-paket-3a-modal-weg-als-eigenes-modul-14112026)). Der Modal-Vertragstest liegt vor und ist unter Windows und nativ am Mac grün ([Plan §21.93](Glide_Entwicklungsplan.md#2193-shell-paket-3-vorstufe-modal-vertragstest-mit-echtem-grab-14112026)). Unter Linux/Xvfb mit Tk 9.1 ist er in der GitHub-Prüfung grün. Der Abbau-Vertragstest (Paket 3b, [Plan §21.95](Glide_Entwicklungsplan.md#2195-shell-paket-3b-abbau-vertragstest-14112026)) hält das Schließen fest. Die Richtung ist seit 15.11.2026 mit D86–D90 festgelegt ([Plan §21.98](Glide_Entwicklungsplan.md#2198-richtungsentscheidungen-zur-shell-trennung-d86d90-15112026)): flache Shell-Module mit Importregel, Paket `glide_shell` vor Paket 6, Reihenfolge 3c Fensterlebensdauer → Fokusrückgabe → Paket 4 → 5/6, Python-Prüfung am Anfang von `app.pyw`, Mac-Lauf der Vertragstests je Schnitt. Als Nächstes 3c; jedes Folgepaket mit eigener Freigabe ([Plan §21.89](Glide_Entwicklungsplan.md#2189-glide-3600-erste-shell-schnitte-start-baseline-und-beruhigter-einstellungsdialog-13112026)).
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
