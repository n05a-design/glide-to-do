# Glide – Übergabe an eine neue Sitzung

Stand 05.11.2026 · Glide 3.50.5 · Erster öffentlicher Stand (intern: öffentliche erste Beta) · Aufgabenformat 26

Am 04.11.2026 zusammengeführt und gekürzt, zum Stand 05.11.2026 mit den Abnahmekorrekturen fortgeschrieben: wiederholte Sitzungsberichte und ersetzte Prioritäten entfernt. Datierte Ergebnisse bleiben im QA-Bericht, in der Analyse und im Entwicklungsplan; Originalbelege innerhalb der Aufbewahrung bleiben unverändert.

## 1. Tatsächlicher Stand

**Gittransport 05.11.2026, abends (Plan §21.69):** Auf Benutzerauftrag „alle Dokumente aktualisieren, Exe bauen, alles auf 3.50.5 bringen, anschließend pushen“ wurde der lokale 3.50.5-Arbeitsstand der OneDrive-Ablage (Basis `40c20fd6`, App `a4bfe4ed…`) als Zweig `claude/glide-3.50.5-abschluss` übernommen und mit `main` `759e4c9` (PR #61/#62: Bildscrolltest B16, UI-/UX-Schritt im `ui-nachlauf`, ci254-Nachweis) zusammengeführt. Anwendung und Lieferdateien bleiben dabei unverändert; Ablage nach `ablage_kuerzen.py` gekürzt. Windows-Paket 3.50.5 entsteht über GitHub Actions (Job „Windows-Paket“), Ergebnis im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Lokale OneDrive-Arbeitskopien nach dem Push über GitHub abgleichen, nicht per Dateikopie. Bisheriger Auftrag: alle Chatpunkte anhand Code/Dokumentation prüfen und eine echte Vollprüfung starten (3.50.5, Plan §21.68 / D63). Buchbreite D61 und neue Logos/Darkmode-Gelb D62 enthalten.

| Ebene | Belegter Stand und Grenze |
|---|---|
| Quelle, Python-Fassung, Showcase | 3.50.5 / Format 26, App `cb4a7aad…` (Nacharbeit 05./06.11.: Bildfolgenexport als Untermenü, Kopfknöpfe bei Enge an fester Stelle, Plan §21.69; vorher `a4bfe4ed…`). Einzelabgleich und Vollprüfungsnachlauf: Titelgrenze für TXT-Fortsetzungen und Vorlagenspeicherung nachgebessert; erweiterter Titelpflichtfall grün. Erster echter Vollmoduslauf auf altem Hash wegen veralteter Auslassungserwartung rot, neue eingefrorene Vollprüfung nach korrigierter Testfenstergeometrie gestartet. Folgende breite Ergebnisse gehören noch zum vorherigen Apphash `e984ba99…`: Strenge Grundstufe 19/19, UI-/UX 17/17, zweimal 1.134 Fachtests und 244 Werkzeugtests (ein Skip), realer Showcase-Abgleich und 93 Code-Dateien/171 Ressourcen bytegleich. 51 Arbeitsmodi-Fälle durch 50/51-Vollauf und grünen Kartenflächen-Nachtest abgedeckt; erneuter Gesamtlauf mit 0xC0000005 nach 21 Fällen abgebrochen. Kein stabiler monolithischer Abschluss. [Nachweis](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/README.md). |
| Remoteprüfungen | `main` `759e4c9` (PR #62, 05.11. 08:51): „Glide-Prüfung“ und CodeQL erfolgreich, Stand 3.50.2. Zusammengeführter 3.50.5-Zweig `claude/glide-3.50.5-abschluss` (PR #63): Windows-/Mac-Paket grün, Vollmatrix rot durch veraltete Testerwartungen nach 3.50.3/D63; vier Suiten angepasst, weitere offen (Liste im QA-Bericht). PR erst nach grüner Vollmatrix mergen. Frühere Momentaufnahmen (#251/#252 vom 04.11.) bleiben ihren Quellständen zugeordnet. |
| Vorhandene Lieferpakete | Python-Fassung und Showcase 3.50.5. Windows-Paket 3.50.5 aus GitHub Actions (Job „Eigenständiges Paket (Windows x64, PyInstaller 6.22.3)“: eigene Tk-9.1-Laufzeit aus Originalquellen mit den Bedienungshilfe-Patches, isolierte Startprobe; unsignierter Entwicklungsbau) unter `build/windows/Glide-3.50.5`, Hash im QA-Bericht. Bisheriger Windows-Abnahmekandidat `Glide-3.50.3-abnahme-20261105` (`ed3fd6dd…`) und reguläre 3.50.0-Pakete sind ältere Stände. `Glide.exe` SHA-256 `7b79b23d…`, Lauf 42107799561. Mac-Paket 3.50.5 in Lauf 42107804373 gebaut und isoliert gestartet, als GitHub-Artefakt verfügbar, noch nicht nach `build/macos` übernommen. |
| Menschliche Abnahme | Punkte 1–5 auf bisherigem nativen 3.50.3-Kandidaten bestanden. Punkt 6/Buchbreite nach Korrektur noch offen; als Nächstes auf Python-Prüffassung 3.50.5 mit eigener Kopie des synthetischen Nachtestbestands bestätigen, sowie Suchzeilenbreite und neuen Seitenleistenabstand bestätigen, dann Seiten-/Zeichenwerkzeuge und übrige Blöcke. Native Paketabnahme/DPI/Mehrmonitor separat offen, Screenreader zurückgestellt. |
| Planung | Einzige Roadmap im Entwicklungsplan. Die neuen Optionen Fundorte, Tages-/Wochenausbau und Portabilität sind Vorschläge; kein neues Featurepaket gewählt. D61 betrifft die Abnahmekorrekturen. |

Zeitpunkt und genaue Prüfgrenzen: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), [Standanalyse §13.27](Glide_Analyse.md#1327-stand--und-entwicklungschancenanalyse-vom-04112026), [CI-Nachweis](../01_Repository/Glide/tests/qa-3.50.2/ci247_2026-11-03/README.md). Frühere rote Läufe bleiben ihren Quellständen zugeordnet.

Fortsetzung auf Benutzerauftrag am 05.11.: Nativer 3.50.3-Windows-Kandidat geöffnet, EXE-Hash bestätigt. Die frühere lokale E-Prüfablage ist auf diesem Rechner nicht erreichbar; deshalb neue isolierte synthetische Showcase-Ablage mit zehn importierten Dokumenten, ohne frühere eigene Zeichnung. Lokaler Startkontext und Wiederanlauf unter `%USERPROFILE%/GlidePruefung/abnahme3503-20261105/`. „Vermarktung · Umsetzung“ für den ersten Nachtest geöffnet. Menschliche Rückmeldung weiterhin ausstehend; Details in Plan §21.65 und im aktuellen Nachweis.

## 2. Zuständige Dokumente

Aktualisierung 05.11., direkte menschliche Rückmeldung zum 3.50.3-Windows-Nachtest: Kopf/Symbolwechsel bei schmal/breit, Eingabe-/Suchabstand samt Plus-Erreichbarkeit und dauerhafte Aufgabenaktionen bei Scrollen/Unterpunkten jeweils bestanden. Nächster Schritt: Tabellen-/Label-/Buchbreiten; anschließend Seiten-/Zeichenwerkzeuge und übrige Abnahmeblöcke. Keine Gesamtabnahme, Details in Plan §21.65 und im aktuellen QA-Nachweis.

| Zweck | Verbindliche Quelle |
|---|---|
| Arbeitsregeln, Produktgrenzen | [AGENTS.md](../01_Repository/Glide/AGENTS.md), [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Aufträge, Entscheidungen D01–D63, Arbeitsablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); D49 mit Korrekturvorbehalt, neue Entscheidungen ab D64 |
| Aufgabenstatus, Reihenfolge und offene Auswahl | [Entwicklungsplan §21.62](Glide_Entwicklungsplan.md#2162-stand-roadmap-und-mehrwertanalyse-vom-04112026); Inventar §18, Paketgrenzen §19, Entscheidungsregister §20 |
| Technische Befunde und ihre Einordnung | [Analyse](Glide_Analyse.md) |
| Markt und Herstellerquellen | [Markt und Vorbilder §13](Glide_Markt_und_Vorbilder.md#13-neue-konkurrenzanalyse-vom-04112026) |
| Gestaltung aller angefassten Oberflächen | [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) |
| Verhalten, Architektur, Daten | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md), [Datenvertrag](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfungen und Lieferstände | [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), [manuelle Prüfung](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Lizenz, Signierung, Identität | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md), [Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md) |
| Dokumentregister und Aufbewahrung | [Index](../01_Repository/Glide/docs/00_INDEX.md), [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |

## 3. Nächste Arbeit und offene Entscheidungen

1. Menschliche Abnahme auf 3.50.5 fortsetzen (Plan §21.68): im Buch Mindestbreite/breites Fenster, volle/schmale/ausgeblendete Seitenleiste samt Rückwechsel nachtesten. Suchfeld im Buch ohne Suchanfrage bündig mit rechter Inhaltskartenkante und nach Suchanfrage/Löschen prüfen. Außerdem über Startseite hovern und gleichmäßigen Abstand oben/links/rechts bestätigen. Danach Seiten-/Zeichenwerkzeuge und übrige Blöcke. Lokaler aktueller Starter `%USERPROFILE%/gq/final5/Nachtest_starten.pyw`; synthetische Daten, keine echten Bestände.
2. Heute Abend native Windows-/Mac-Pakete am vorhandenen Bauplatz auf **3.50.5** bauen; neue Logos und Buchkorrektur enthalten. Quell-/Lizenz-/PE-/ICNS-/Signatur- und isolierte Startbelege sowie tatsächliche Lieferung erneuern, danach native menschliche Prüfung. Baugrenzen und vollständige Logo-/Shell-Checkliste in Plan §21.66/§21.67 und `20_Grafik_Master/README.md`.
3. Neue Featureauswahl nur nach konkretem Folgeauftrag. Empfehlung der Standanalyse ist WA-21/Fundorte; weitere Optionen und Technikreste WA-32/39/36 stehen allein im Plan. Bereits gelieferte Teilfunktionen nicht erneut als fehlend führen.
4. Öffentliche Signatur/Notarisierung, Lizenz, Marke und weitere Vertriebskanäle bleiben gesonderte Inhaberentscheidungen.

## 0. Sofortübergabe WA-41 – zuerst lesen

Diese Überschrift bleibt als bestehendes Linkziel erhalten. Sie betrifft die historische Fehleruntersuchung; aktuelle Entwicklungsprioritäten stehen in Abschnitt 3.

- **WA-41A:** sporadische Interpreter-/Prozessfehler auf PC-02 Intel, unter anderem `0xC0000005`, `0xC0000409`, „Executing a cache“. WHEA-/Systembefunde sind eine Spur, kein bewiesener CPU-Defekt. **WA-41B:** einmal abweichender gespeicherter/geladener künstlicher Bestand; konkrete Felder und Ursache ungeklärt, kein belegter Verlust echter Nutzerdaten. Beide Spuren getrennt erhalten.
- Zehn isolierte AMD-Prozesse waren grün; vollständige Suiten erzeugten UUIDs/Zeitstempel selbst. Kein byteidentischer Intel-Replay und kein Ursachenbeweis. [AMD-Nachweis](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/amd_vergleich_2026-10-27/README.md), [Gerätevergleich](../01_Repository/Glide/tests/qa-3.49.0/geraetevergleich_2026-10-29/README.md).
- BIOS-/CPU-Einstellungen nicht ändern, keine unnötige neue Stressserie am instabilen PC-02. Keine spekulative Mengenschranke, kein Chunking oder `gc.collect()` als angeblicher Fix. Historischen Referenzstand und Originalkriterien bewahren.
- [Ursachenanalyse](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/wa41_2026-10-27/README.md), [Python-Vergleich](https://github.com/n05a-design/glide-to-do/blob/40c20fd62db6ec31b4e3668dfc9e7f1550f67974/01_Repository/Glide/tests/qa-3.48.0/python315_vergleich_2026-10-27/README.md), [WHEA-/Lastbefunde und Dumpinventar](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json), [470-Dateien-Referenz](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Spätere Schutzfunktionen und Lieferung schließen diese Ursachenfragen nicht.
- Geschützte lokale Eingänge: `01_Repository/Glide/tests/qa-3.48.0/lokale_belege/eingang/initial.json` und `lokale_belege/minidumps/`; [Sicherungsmanifest](../01_Repository/Glide/tests/qa-3.50.5/abnahme_2026-11-05/aufbewahrung.json). Anfangsbestand 28.548.872 Bytes, SHA-256 `a3b8c0cac4c72e1820e71730ad78e312f2a30338678fbcfe2a2b6d91dae081f4`. Acht bekannte Minidumps sind keine FullMemory-Aufnahmen. Ein früher genannter externer Exportordner wurde nicht lokal bestätigt; keine Originale aufgrund dieser Angabe löschen.
- Dumps, Rohlogs und lokale Eingänge bleiben Git-ausgeschlossen und sind bei Rechnerwechsel ausdrücklich geschützt zu übertragen. Temporärpfade und Runtimeorte aus alten Berichten vor Wiederverwendung prüfen; Version, `sys.executable`, Tk und Binärhashes erfassen. Standardbefehl `python` ist kein Laufzeitnachweis.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei. Bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Vor jedem Testimport temporären `GLIDE_DATA_DIR` setzen; keine echten Nutzerdaten verwenden. Kurze Prüfpfade außerhalb OneDrive verwenden, Details in [CLAUDE.md](../CLAUDE.md).
- Jede Prüfung gilt für ihre konkreten Quell-/Test-/Ressourcenbytes. Vollmatrix, gezielte Tests, Lieferung und Menschenabnahme getrennt ausweisen. Vor einem beauftragten Commit CI-Grundstufe ausführen.
- Ein Thema, ein Dokument; überholte Erzählungen nach Zusammenführung löschen. QA-Nachweise sieben Versionen, QA-Bilder drei; Git trägt Vorfassungen. Originalreferenzen, Migrationsfixtures, Lizenztexte und Lieferressourcen nach ihrem eigenen Zweck erhalten.
- [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md), [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) und 28 lokale Originalbilder sind Eingangsreferenzen. Die teilweise personenbezogenen Bilder bleiben lokal und müssen bei Übergaben ausdrücklich mitgegeben werden.

**Vorherige Prüffassung (D62, 3.50.3):** `%USERPROFILE%/gq/logo1105/Nachtest_starten.pyw`, eingefrorene Quelle `ce60fd8c…` mit neuer G-Kontur und Buchbreite, bestehende eigene Tk 9.1, eigene Kopie des synthetischen Nachtestbestands. Startseite im breiten Fenster; neue Kopf-/Fenstersymbole selbst gesichtet, keine menschliche Abnahme daraus. Frühere lokale Starter sind historische Stände. Native Neubauten heute Abend durch den Benutzer vorgesehen.

**Vorherige gestartete Prüffassung 3.50.4 (vor Kartenbreitenkorrektur):** `%USERPROFILE%/gq/v3504/Nachtest_starten.pyw`, App `8b3076f9…`, eigene bestehende Tk 9.1, unabhängige synthetische Datenkopie mit stabil geprüften JSON-Bytes. Ältere 3.50.3-Prüffassung nach Benutzerbedienung geöffnet belassen. Als Nächstes menschlicher Punkt 6/Buchbreite, danach Seiten-/Zeichenwerkzeuge; keine neue menschliche Freigabe aus dem Start.

**Aktuell korrigierte Punkt-6-Prüffassung:** `%USERPROFILE%/gq/final5/Nachtest_starten.pyw`, App `85a61f0a…`, unabhängige stabile Kopie des synthetischen bisherigen Bestands; ältere Prüffenster unverändert. Buchbaum ohne zusätzliche 14-px-Abstände, 64 erweiterte Prüfungen bis zu beiden Karteninnenkanten grün; direkte menschliche Bestätigung weiterhin offen.
