# Glide – Übergabe an eine neue Sitzung

**Aktuelle Fortsetzung 08.11.2026:** Main `d7e017f` enthält #69 und #70; neuer Branch `codex/glide-3.50.7-main-validierung` direkt davon. Gesicherte Übernahme `1b58d1e`, ursprünglicher Codex-Checkpoint `f0c4442`. Vorrang hat jetzt CI-Reparatur gemäß [Plan §21.78](Glide_Entwicklungsplan.md#2178-ci-abschlussauftrag-3507-auf-main-08112026). Die folgende Runde vom 07.11. bleibt datierte Vorgeschichte, keine aktuelle Aussage über einen offenen PR #69. Kein Gesamtabschluss; Main-Vollmatrix rot.

Stand 07.11.2026 · Glide 3.50.7 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

Am 07.11.2026 nach dem Validierungsauftrag zusammengeführt und gekürzt: überholte aktive Lauf-/Mergeanweisungen durch Quellenverweise ersetzt. Die datierten Originalnachweise bleiben in QA beziehungsweise nach der vorhandenen Aufbewahrungsregel über feste Git-Verweise erhalten. Keine weitere Roadmap und keine neue allgemeine Archivablage.

## 1. Tatsächlicher Stand

| Achse | Belegter Stand und Grenze |
|---|---|
| Ausgangspunkt | 3.50.6 / Format 26 in PR #69, anfangs `be379408`, ergänzt auf `13bcb66a`; PR beim Abgleich offen, `main` `8e71ae52` trägt noch 3.50.5 |
| Eigene Arbeit | `codex/glide-3.50.7-validierung`: Branding/MPL/Statusabgleich und gezielte Seitenleistenkorrektur; Zielversion 3.50.7 nach D73, kein neues Datenformat |
| Python und Showcase | Versionswechsel und separater Lieferabgleich; konkrete SHA-256 und Testergebnisse im [Rundennachweis](../01_Repository/Glide/tests/qa-3.50.7/validierung_2026-11-07/README.md) |
| Eigenständige Pakete | Windows 3.50.5 auf früherem Hash; Mac 3.50.6 lokal auf `f4339a5d…`, vor Seitenleisten-/Anhangsnachträgen. Kein Paketnachweis für 3.50.7. Diese Versionen bleiben getrennt. |
| Automatisierte QA | Strenge Windows-Grundstufe auf Startbasis grün; neue Prüfergebnisse auf aktuellen Bytes ausschließlich im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). PR-#69-Vollmatrix auf `13bcb66a` rot: Windows-Unterzeilentest, Linux kompakt/pinnwandleiste. Stopps und übersprungene Folgen sind kein Erfolg. |
| Native und menschliche QA | Mac-Befund `test_bedienung33316` offen, dortiger Vollmodus nach 80 Schritten gestoppt und 44 Folgeschritte nicht ausgeführt. Gemeldete und bestätigte Teilabnahmen vom 07.11. bleiben ihrem Vorzustand zugeordnet. Neue Gesamt-/DPI-/Mehrmonitorabnahme offen; Reader nach D58 zurückgestellt. |
| Veröffentlichung | Keine öffentlichen Releases beim Abgleich. Kein neuer Tag, Merge oder Release durch diesen Auftrag. MPL-2.0 ist beschlossen; Preis-/Serviceangebote, Marke und öffentliche Signierung separat. |
| GitHub-Auftritt | Neue Beschreibung und 15 Topics nach konkreter Freigabe aktualisiert und zurückgelesen. README-/Codeänderungen kommen über den eigenen PR. |

**Lokale Ausgangsablage:** Die gemeinsame OneDrive-Arbeitskopie steht auf `40c20fd6`, hat 368 offene Statuszeilen und ein nachgewiesen leeres Git-Objekt. Sie wurde nicht zurückgesetzt, umgeschaltet, bereinigt oder gestasht. Ein frischer Clone dient als Arbeitsbasis. Lokale Worktrees und vier ältere Stashes bleiben geschützt. Vor späterer Synchronisation vorhandene Änderungen und Git-Schaden gesondert sichern und prüfen; kein pauschales Ersetzen der Arbeitskopie.

## 2. Zuständige Dokumente

| Thema | Verbindliche Quelle |
|---|---|
| Aufgaben, aktueller Abschlussrest | [Entwicklungsplan §21.77](Glide_Entwicklungsplan.md#2177-validierung-produktkommunikation-und-mpl-20-07112026-d72d73) |
| Entscheidungen D01–D73 und Arbeitsablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Prüf-/Lieferstände und Grenzen | [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), datierter Rundennachweis |
| Technischer Code-/Dokumentabgleich | [Analyse §13.30](Glide_Analyse.md#1330-validierung-von-pr-69-und-fortschreibung-auf-3507) |
| Markt, Quellen und Kommunikationsableitung | [Markt §15](Glide_Markt_und_Vorbilder.md#15-markt-und-produktkommunikation-am-07112026) |
| Produkttexte, MPL, Vertrieb und Marke | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md), [Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md) |
| Regeln und Design | [AGENTS](../01_Repository/Glide/AGENTS.md), [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md), [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |

## 3. Nächste Arbeit und offene Entscheidungen

1. Eigene PR-Änderungen auf der bezeichneten PR-#69-Basis prüfen. Merge durch den Inhaber; den 3.50.6-Stand nicht als bereits in Main integriert behandeln. Nach jeder tatsächlichen Integration neue Prüfungen dem konkreten Commit zuordnen.
2. Den aktuellen Stand als eigenständiges Windows- und Mac-Paket neu bauen, Quell-/Lizenz-/Binärabgleich und isolierte Startproben erneuern. Vor Weitergabe muss der in `Glide-Quellcode.txt` bezeichnete Commit erreichbar sein. Alte 3.50.5-/3.50.6-Pakete nicht umbenennen.
3. Bestehenden Mac-Befund klären und native Gesamtmatrix sowie menschliche Bedien-/DPI-/Mehrmonitorprüfung auf den neuen Bytes nachweisen. Die Windows-Seitenleistenprobe ersetzt weder native Mac-/Linux-Geometrie noch physische DPI-Abnahme.
4. Inhaberangaben I1, Signierung/Notarisierung I3, professionelle Namens-/Markenprüfung I4 und öffentliche Releasefreigabe I11 bleiben offen. I2 ist mit MPL-2.0 entschieden; nicht erneut als offene Lizenzwahl führen.
5. Weitere Produktideen bleiben ungewählt, sofern kein gesonderter Auftrag vorliegt. WA-21/Fundorte, WA-08/Zeitauswertung und andere Marktoptionen stehen allein im Plan. Technische Reste WA-32/39/36/37/38/40, WA-46 und WA-49/50 behalten ihren konkreten Teilstatus.
6. Frühere Zweigzusammenführung ist als Quellbündelung in PR #69 enthalten (Plan §21.72–§21.76); alte aktive Merge-Rezepte aus dieser Übergabe nicht wieder ausführen. Nichtintegrierte lokale Zweige/Stashes und Diagnosezweige erst nach eigener Zuordnungsprüfung behandeln.

## 0. Sofortübergabe WA-41 – zuerst lesen

Diese Überschrift bleibt als bestehendes Linkziel erhalten. Sie betrifft die historische Fehleruntersuchung; aktuelle Entwicklungsprioritäten stehen in Abschnitt 3.

- **WA-41A:** sporadische Interpreter-/Prozessfehler auf PC-02 Intel, unter anderem `0xC0000005`, `0xC0000409`, „Executing a cache“. WHEA-/Systembefunde sind eine Spur, kein bewiesener CPU-Defekt. **WA-41B:** einmal abweichender gespeicherter/geladener künstlicher Bestand; konkrete Felder und Ursache ungeklärt, kein belegter Verlust echter Nutzerdaten. Beide Spuren getrennt erhalten.
- Zehn isolierte AMD-Prozesse waren grün; vollständige Suiten erzeugten UUIDs/Zeitstempel selbst. Kein byteidentischer Intel-Replay und kein Ursachenbeweis. [AMD-Nachweis](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/amd_vergleich_2026-10-27/README.md), [Gerätevergleich](https://github.com/n05a-design/glide-to-do/blob/f1a5b5b6e0f97f2b5eab1ac552999c33c6416e69/01_Repository/Glide/tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md).
- BIOS-/CPU-Einstellungen nicht ändern, keine unnötige neue Stressserie am instabilen PC-02. Keine spekulative Mengenschranke, kein Chunking oder `gc.collect()` als angeblicher Fix. Historischen Referenzstand und Originalkriterien bewahren.
- [Ursachenanalyse](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/wa41_2026-10-27/README.md), [Python-Vergleich](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/python315_vergleich_2026-10-27/README.md), [WHEA-/Lastbefunde und Dumpinventar](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json), [470-Dateien-Referenz](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Spätere Schutzfunktionen und Lieferung schließen diese Ursachenfragen nicht.
- Geschützte lokale Eingänge: `01_Repository/Glide/tests/qa-3.48.0/lokale_belege/eingang/initial.json` und `lokale_belege/minidumps/`; [Sicherungsmanifest](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Anfangsbestand 28.548.872 Bytes, SHA-256 `a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4`. Acht bekannte Minidumps sind keine FullMemory-Aufnahmen. Ein früher genannter externer Exportordner wurde nicht lokal bestätigt; keine Originale aufgrund dieser Angabe löschen.
- Dumps, Rohlogs und lokale Eingänge bleiben Git-ausgeschlossen und sind bei Rechnerwechsel ausdrücklich geschützt zu übertragen. Temporärpfade und Runtimeorte aus alten Berichten vor Wiederverwendung prüfen; Version, `sys.executable`, Tk und Binärhashes erfassen. Standardbefehl `python` ist kein Laufzeitnachweis.

## 5. Arbeits- und Prüfregeln

- Deutsch in Antworten und Dokumenten. Produktidentitäten und Datenpfade stabil halten; neue Fachlogik nach D17 Tk-frei.
- Vor Testimporten temporären `GLIDE_DATA_DIR` setzen. Kurze lokale Prüfpfade außerhalb OneDrive; keine echten Nutzerdaten oder ungesicherten Arbeitskopien verändern.
- Ergebnisse gelten für konkrete Quell-/Test-/Fixture-/Ressourcenbytes und Runtime. Originalrote, Skips, Stoppfolgen, Teilprüfungen, Lieferung und Menschenabnahme getrennt nennen.
- Vor dem Commit CI-Grundstufe, Stand-/Link-/Datenschutz-/Lieferprüfung. Rohlogs und persönliche Pfade nicht veröffentlichen.
- Ein Thema, ein Dokument. Historische Eingänge, Originalbilder, Lizenztexte, Migrationsfixtures und aktuelle QA-Nachweise nach ihrem Zweck erhalten. Ältere reproduzierbare QA-Ablage nur nach Manifest und fester Git-Zuordnung gemäß Pflegevertrag kürzen.
- [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) und [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) bleiben Eingangsreferenzen; teilweise personenbezogene Originalbilder bleiben lokal und müssen bei Übergaben ausdrücklich mitgegeben werden.
