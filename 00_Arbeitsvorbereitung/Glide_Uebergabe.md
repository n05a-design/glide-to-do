# Glide – Übergabe an eine neue Sitzung

## Lokaler Stand 3.60.0 (13.11.2026)

**Glide 3.60.0** (Aufgabenformat **26**, Einstellungen **2**, Vorlagen **2**, Glide-System **V1.23.1**) setzt auf `main` `45ab307e` auf. Enthalten sind die ersten Schnitte der Shell-Migration und eine Fehlerkorrektur:
1. **Normallage:** `compact_mode.keep_visible` rechnet die Fensterlage beim Start Tk-frei; `ListApp.clamp_geometry` bleibt Fassade.
2. **Start und Import (WA-49, weiter teilweise):** Der Import von `app.pyw` legt auch mit `GLIDE_DATA_DIR` keine Ordner an. `test_startwege.py` (Teil von `SUITEN`) und der Gleichheitstest der Bytecode-Pfade in `test_runtime_config.py` sind die Vergleichsgrundlage für weitere Startänderungen.
3. **Einstellungsdialog:** Die Umbruchschaukel mit „Kreativ: DM Serif Display“ in kleiner Schrift ist behoben (`ui_design.settled_wrap_width`).

Quelle und startbare Python-Lieferung (`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.60.0.pyw`) sind per `abgleich_07.py` SHA-256-identisch; der Showcase ist abgeglichen. Auftrag, Entscheidungen und Folgepakete stehen im [Plan §21.89](Glide_Entwicklungsplan.md#2189-glide-3600-erste-shell-schnitte-start-baseline-und-beruhigter-einstellungsdialog-13112026), Prüfergebnisse und Grenzen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#prüfstand-3600-13112026), validierte Architekturgrenzen im [Shell-Konzept](../01_Repository/Glide/docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md#6-validierte-grenzen-13112026).

Logo- und Showcase-Ergänzung [Plan §21.90](Glide_Entwicklungsplan.md#2190-logo-wechsel-und-werkhaus-showcase-für-3600-13112026) mit aktualisierten Master-, Paket- und README-Ressourcen.

**Nächste Schritte:** Plattformmatrix (Windows, Linux, macOS mit Tk 9.1), Paketbau und menschliche Abnahme für 3.60.0. In der Shell-Migration folgt der Modal-Vertragstest mit echtem Grab vor jeder Verlagerung von `run_modal`; jedes Folgepaket braucht eine eigene Freigabe.

## GitHub-Prüfstand 3.55.1 (13.11.2026)

`main` steht auf `45ab307` mit PR #80 und der Dokumentationspflege für Glide-System V1.17.3. Für diesen Commit sind Linux- und Windows-Vollprüfung, beide eigenständigen Entwicklungsbauten und deren isolierte Starts belegt. Die lokal gesicherten Windows- und Mac-Pakete sind hashgeprüft. Der [native macOS-Volllauf](https://github.com/n05a-design/glide-to-do/actions/runs/43405769310) ist nach 105 erfolgreichen Schritten im Zeitfall für Seitenkarten rot (1,1176 bei Grenze 1,10). Der gezielte Vorlauf bestand. Originalwerte und Laufzeitkontext stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md#macos-seitenkarten-im-vollmodus). Nächster Einstieg im [Plan §21.89](Glide_Entwicklungsplan.md#2188-prüfung-und-lieferabgleich-3551-13112026).

PC-02 Intel hat eine DLL-Suchpfadabhängigkeit im Windows-Paket reproduziert. Der lokale korrigierte Starter ist im nativen Windows-Regressionsfall und auf einer Paketkopie geprüft. Der reguläre Paketneubau bleibt offen. [A/B-Nachweis](../01_Repository/Glide/docs/07_QA_BERICHT.md#gezielte-windows-paketprobe-auf-pc-02-intel).

## Dokumentationsabgleich (13.11.2026)

Die [Pflegematrix](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) führt Zuständigkeiten und Änderungsfolgen zentral. Architektur, Glide-System und Shell-Konzept sind als Istvertrag, Bestand und Zielbild abgegrenzt; doppelte Modulaufzählungen im Shell-Konzept wurden durch Registerverweise ersetzt. Auftrag und Umfang stehen im [Plan §21.87](Glide_Entwicklungsplan.md#2187-dokumentationsbezüge-und-konsolidierung-13112026), die Prüfungen im [Dokumentationsnachweis](../01_Repository/Glide/tests/qa-3.55.1/dokumentation_2026-11-13/README.md). Die App-Freigabe bleibt beim folgenden QA-Stand; diese Pflege ist keine neue Plattform- oder Paketabnahme.

## Lokaler Prüfstand 3.55.1 (12.11.2026)

3.55.1 kennzeichnet den korrigierten Stand nach der macOS-Abnahme. Enthalten sind die vereinfachte Tagesentlastung, der reparierte JSON-Canvas-Export und korrigierte Dateinamenvorschläge. Aufgabenformat 26, Einstellungen 2 und Vorlagenformat 2 gelten weiter. Die [QA-Nachweise](../01_Repository/Glide/docs/07_QA_BERICHT.md#lokale-nachabnahme-und-prüfstand-3551-12112026) dokumentieren Abnahme und Freigabestatus.

## Vorangegangener GitHub-Stand 3.55.0 nach PR #78

**Glide 3.55.0** (Aufgabenformat **26**, Einstellungen **2**, Vorlagen **2**) lag nach PR #78 auf `main` bei `766978d`. PR #77 (`a72d5e9`) brachte die fachlichen Änderungen ein. PR #78 ergänzte die App-Neuerungskarte „Neu in 3.55.0“ und korrigierte die Dokumentation.
1. **Tagesplanung & Kapazität (`WA-12`):** `planning.py` berechnet geplanten Aufgabenaufwand, Kalenderbelegung und Netto-Kapazität. `day_relief.py` bereitet Tagesbilanz und Überlastungsgründe auf. `ListApp` in `app.pyw` bindet die Bilanz und den Entlastungsdialog ein. Ungeschätzte Aufgaben bleiben gesondert sichtbar und Fälligkeiten bleiben beim Umplanen erhalten.
2. **Laufzeitkonfiguration (`WA-49` / `M095`):** `runtime_config.py` bündelt die Tk-freie Auflösung der Datenpfade. Ein expliziter Pfad oder `GLIDE_DATA_DIR` hat Vorrang vor `datenordner.json` und dem Plattformstandard. Unter Windows liegen Daten standardmäßig in `%APPDATA%/Glide`, der Cache in `%LOCALAPPDATA%/Glide/Cache`. `app.pyw` nutzt die Pfadfunktionen und verwaltet weiterhin einzelne Laufzeitoptionen.
3. **Glide Shell Framework Architekturkonzept:** Der Entwurf beschreibt die schrittweise Entkopplung von Fensterverwaltung, Navigation und Fachlogik. Mit der Pfadauflösung liegt ein erster Baustein vor.

Die damalige Python-Lieferung 3.55.0 war per SHA-256 mit Quelle, Schnellstart, Laufzeitmodulen und mitgelieferten Ressourcen abgeglichen. Linux- und Windows-Vollprüfung sowie eigenständiger Windows-x64- und macOS-arm64-Paketbau mit isoliertem Start sind auf `766978d` belegt. Der separate native macOS-Vollmodus scheiterte am Zeitgrenzwert für Seitenkarten-Druck. Details stehen im [QA-Bericht für 3.55.0](../01_Repository/Glide/docs/07_QA_BERICHT.md#plattformprüfung-und-pakete-auf-main-12112026).

## Vorangegangener Stand 3.54.0 (`main` nach PR #76)

Auf Inhaberwahl (D78) bündelte **Glide 3.54.0** (Datenformat **26**, Glide-System **V1.16**) drei zusammenhängende Pakete auf Basis des gemergten `main`-Stands 3.53.0 (`9e767bea`):
1. **Vollständige Fundortübersicht („Fundorte anzeigen …“, `WA-21`):** `usage_locations(...)` und `UsageLocation` in `src/glide/object_references.py` sowie `show_usage_locations_dialog` und `open_usage_location` in `src/glide/app.pyw` zeigen alle Verwendungen einer Aufgabe, Seite, Notiz, Liste oder Zeichnung über acht Fundortarten (`home`, `reference`, `rich_link`, `task_line`, `live_list`, `relation`, `pinboard`, `mention`) samt Zielstatus (`active`, `archived`, `trash`, `missing`), direktem Öffnen in Haupt- oder Nebenansicht und Verknüpfen unverknüpfter Erwähnungen als ein Rückgängig-Schritt.
2. **Pinnwand-Export als JSON Canvas 1.0 (`.canvas`, `WA-07` / `FP-07` Stufe 2):** `export_json_canvas` und `CanvasExportReport` in `src/glide/pinboard_pages.py` sowie `ItemWorkspace.export_board_json_canvas` in `src/glide/app.pyw` exportieren jede Pinnwand (`global`, `list:<id>`, `folder:<id>`) in das offene Format JSON Canvas 1.0 (`group`-Bereiche, `text`-Karten für Aufgaben/Seiten/Notizen/Zeichnungen mit stabilen IDs, Maßen und Farben sowie `edges` mit Richtung und Beschriftung) einschließlich ausdrücklichem Verlustbericht.
3. **Vollständige Ablösung klassischer Tk-Steuerelemente (`Sperrklinke = 0/0`, UI-Feinschliff §21.76):** Alle verbliebenen 35 klassischen Tk-Instanzen (`28 × Checkbutton`, `2 × Radiobutton`, `4 × Listbox`, `1 × Scale`) sind durch themengerechte Eigenzeichnungen (`GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`) ersetzt; in `tests/tools/altbestandteile.py` steht `BESTAND` für alle vier Klassen auf `0/0` und die Klassen sind in `WIDGETKLASSEN_VERBOTEN` gesperrt.

Quelle (`01_Repository/Glide/src/glide`) und startbare Python-Lieferung (`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.54.0.pyw`) waren zum damaligen Lieferzeitpunkt per `abgleich_07.py` SHA-256-identisch. Die 3.54.0-Hauptdatei liegt heute im Archiv. 1.158 Unit-Tests, `altbestandteile.py`, `attributpruefung.py`, `test_glide_system.py`, `standpruefung.py`, `test_kontrast330.py`, `test_zugang400.py` und `test_animation3400.py --fall frames` sind grün. Vollständige plattformübergreifende Vollmatrix, eigenständige 3.54.0-Paketbauten und menschliche Sichtabnahme bleiben getrennte offene Tore (`release_ready=false`); Details in [Plan §21.85](Glide_Entwicklungsplan.md#2185-dreierpaket-3540-fundortübersicht-wa-21-json-canvas-10-wa-07-und-sperrklinke-00-d78-10112026) und im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Vorangegangener Stand 3.53.0 (`main` nach PR #75)

Auf Inhaberwahl (D77) ersetzt 3.53.0 die Familien Technisch: Roboto Mono, Kreativ: Playfair Display und Klassisch: Fraunces durch DM Mono, DM Serif Display und Charis SIL; Modern bleibt Rubik. Für alle vier Familien werden sämtliche UI-Symbole unter normalem und fettem Tk-Gewicht geprüft; die lokale Testzuordnung steht im [QA-Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md#schrift--und-symboländerungen--d77-10112026). Frühere gespeicherte Schriftzuordnungen bleiben erhalten. Die strenge Windows-CI-Grundstufe besteht mit 19/19; der gezielte D66-Nachlauf besteht mit 48 Konfigurationen. Der finale eingefrorene Windows-Volltest ist mit Exitcode 0 abgeschlossen: 130/131 Schritte ausgeführt, allein die gesonderte Sichtprüfung der Bilder übersprungen. `test_tempo330` und `test_seitenkarten/druck_tempo` bestanden; der Seitenkartenquotient lag bei 1,0107 gegenüber Grenze 1,10. Frühere Tempo-Rotläufe bleiben als historische Messbefunde erhalten, nicht als Rot des finalen Laufs. Linux-/macOS-Vollmatrix, native Paket-/Startabnahme und detaillierte Bedien-/DPI-Matrix sind offen; der Lauf weist `release_ready=false` aus. PR #75 (`codex/glide-3.53.0-release`) ist mit Merge-Commit `9e767bea` in `main` integriert; Tag und Veröffentlichung bleiben bis zum Abschluss der Gates offen. Prüfgrenzen und Laufdetails stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), die vollständige Projektbestandsaufnahme in [Glide_Projektbestandsaufnahme_2026-11-10.md](Glide_Projektbestandsaufnahme_2026-11-10.md) und [Analyse §13.32](Glide_Analyse.md#1332-pr-75-integration-d77-schriftwechsel-und-vollständige-projektbestandsaufnahme-10112026).

## Nachgewiesener Prüfstand 3.51.0 (historisch)

Der QA-Bericht dokumentiert für diesen Stand einen Windows-Volltest mit 131 automatisierten Schritten und eine strenge Grundstufe mit 19/19 Schritten. Ein zugehöriger 3.51.0-Merge-Commit oder Branch ist im aktuellen Clone nicht nachweisbar; „lokal gemergt“ bleibt daher eine gemeldete, hier nicht unabhängig belegte Historie. Prüfstand, Lieferabgleich und offene Sichtabnahme stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Abschlussprüfung und offene Nachweise (09.11.2026)

- **Öffentlicher Stand:** PR #71 ist gemergt. `main`/HEAD ist `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d` mit `VERSION=3.50.7`; der Merge-Tree ist byte-/treegleich zum PR-Head `2c3e543b47af6984556712525d122e48928dcb8c`. Die erfolgreichen PR-Checks belegen Windows- und Linux-Vollprüfungen sowie den Windows-Paketbau. Der native macOS-Paketbau und isolierte Start waren erfolgreich; der vollständige native macOS-Job wurde übersprungen. Eine vollständige macOS-Matrix ist deshalb nicht belegt.
- **Lokaler Kandidat am 09.11.:** `VERSION=3.52.0` war nur der veränderte Arbeitsbaum, nicht der Git-HEAD oder ein veröffentlichtes Release. Die Neuablagequittung bestätigt den anfänglich sauberen Checkout auf dem PR-71-Merge; die lokalen 3.51-/3.52-Änderungen kamen danach hinzu. Zum damaligen Auditzeitpunkt: 72 geänderte, 34 gelöschte und 5 ungetrackte Dateien. Der eingefrorene Windows-Volltest für genau diesen Stand endete mit Exitcode 0 (130/131 Schritte; „Sichtprüfung“ übersprungen). `app.pyw` und Python-Lieferdatei waren SHA-256-bytegleich; die Showcase-Hauptdateien stimmten mit dem Freeze überein. Zwei physische Showcase-Dateinamen sind klein geschrieben, Git führt sie groß geschrieben; Windows ist nicht case-sensitive. Linux-/macOS-Vollprüfungen, native Paketabnahme und menschliche Sichtprüfung blieben offen.
- **Glide-System / Steps:** Registerstand 1.14: 147 Featureeinträge einschließlich 20 technischer Systemfähigkeiten, 25 Wiederverwendungs-/Bausteinpakete und 311 Test-/Werkzeugdateien. Das ist kein unabhängig abgenommenes Framework; ein Steps-Projekt wurde nicht erzeugt.
- **Archiv:** Die Abnahme auf E: meldet `full_archive_accepted=true`; das Git-Bundle mit 131 Entwicklungsrefs besteht einen unabhängigen `fsck` (Exitcode 0). Das spätere Inventar weist 35.481 geprüfte Pfade aus, die Neuablagequittung 35.380; die Nettoabweichung aus 93 neuen Einträgen und 8 alternativen Zuordnungen sowie 68 bytegleich nachgewiesene Pfadverschiebungen ist dokumentiert, ohne Hashfehler. Alle 25 Dateien des SHA-256-Pflegepakets vom 09.11. sind verifiziert. Historisch beschädigte Codex-Checkpointobjekte im Roharchiv bleiben unverändert; der Bundle-`fsck` belegt ausschließlich das getrennte Git-Bundle.
- **Gelöschte Arbeitskopien-Dateien:** 33 der 34 Dateien wurden bytegleich im E:-Archiv gefunden. Die verbliebene 3.50.7-Pythonlieferung ist im lokalen Archivordner erhalten und bytegleich zur weiterhin in `main` versionierten Datei; eine separate E:-Kopie wurde nicht nachgewiesen. Es gibt damit keinen Hinweis auf einzigartige Quelldaten, die nur in dieser Arbeitskopie lagen. Die drei alten C:-Arbeitsverzeichnisse wurden nicht gelöscht; die dokumentierte Bereinigung bleibt ausstehend und ist nicht Teil dieses Audits.
- **Weitere offen am 09.11.:** Für 3.51.0 liegen dokumentierte lokale Windows-Nachweise, aber kein 3.51.0-Commit/-Branch im aktuellen Clone vor. Für 3.52.0 bleiben Linux-/macOS-Prüfungen, native Paketabnahme und menschliche Sichtprüfung offen. Paketierung, Signierung/Notarisierung, Release und menschliche Produktfreigabe sind nicht durch frühere Versionsstände ersetzt.

## Datierte Vorgeschichte: CI-Abschluss und Steps-Grundlage (08.11.2026)

Die folgenden Angaben sind Momentaufnahmen vor dem Merge von PR #71 und vor dem heutigen 3.52.0-Audit. Sie sind keine aktiven Status- oder Ausführungsanweisungen; für den aktuellen Stand gilt ausschließlich der Abschnitt oben.

**Fortsetzung 09.11.2026.** GitHub-Vollprüfungen und Paketbauten auf `5311699` grün. MacBook Air M2, Python 3.14.5/Tk 9.1.0 Aqua, derselbe Commit: vier von fünf gezielten Prüfungen grün, Seitenleistenmatrix beim Seiteneditoraufbau rot (`KeyError(✓)`). Der frühere lesende Trace belegt das gespeicherte Ersatzpaar `OK`/`[]` bei gleichen Schriftattributen und späterem Zugriff auf `✓`/`□`. Der neue Regressionsteil reproduziert genau diesen Fehler auch unter Windows. Der Cache-Schlüssel enthält jetzt beide tatsächlich aufgelösten Texte. Der gezielte Windows-Nachlauf besteht mit 48 Konfigurationen, 384 sichtbaren Zeilen und vier Neustarts. Die vier grünen MacBook-Fälle einschließlich Seitenkarten-Tempo 0,950464 bei Grenze 1,10 gelten für 5311699. Der native Seitenleistennachtest der Korrektur steht aus. Originalberichte und Altbelege bleiben erhalten. Nächster Schritt ist allein `seitenleistenzeilen3507` auf dem MacBook mit dem separat bereitgestellten Korrekturcommit.

Basis Main `d7e017f001e5c069eeb98a0f5302577966ac4098` nach #69/#70. PR #71 steht vor der Zusammenführung der Mac-Nachträge weiterhin auf dem **grünen** `f3408de`: vollständige Windows-/Linux-Matrix und Windows-Paketbau bestätigt. Diagnosezweig `diagnostic/glide-macos-workarea-20261108` trägt die gezielt geprüften Mac-/Kartenkorrekturen. Ziel 3.50.7, Datenformat 26, Systemkatalog 1.11.1. Kein eigener Merge, Tag, Release oder öffentlicher Download.

Auf `0e704f30751d1996d02e93f7f970043def9700cc` strenge lokale Grundstufe 19/19 grün (Python 3.14.7/Tk 9.1, 285 Werkzeugtests mit einem ausgewiesenen Plattform-Skip, zweimal 1.156 Fachtests, 343 Dokumentverweise, Quelle/Python bytegleich). Nativer Mac-Nachlauf 42527665270/Job 128874765645: Tempo, alle 63 Arbeitsmodifälle (17/13/14/9/10), Bedienung, Startseite und Altimport sowie Paketbau/isolierter Start erfolgreich. Dies ist eine gezielte Teilprüfung, kein vollständiger Mac-Vollmodus. Realer Paketnachweis: 37 Lizenzdateien, 24 BOM-Komponenten, null offizielle Schemafehler, MPL-Originalbytes und fester Quellbezug korrekt. Keine unprofilierte Geschwindigkeitssteigerung aus unterschiedlichen Rechnerzuständen abgeleitet. Die abschließende Änderung danach betrifft nur diese Dokument-/Prüfzuordnung und Systemversion 1.11.1; der Appcode bleibt bytegleich zu 0e704f3.

Nächster Schritt: den konsolidierten Schlusscommit einmal in PR #71 übernehmen und dessen gesamte Windows-/Linux-Matrix sowie den nativen Mac-Vollmodus auswerten. [Lebender CI-Stand und Commitzuordnung](https://github.com/n05a-design/glide-to-do/pull/71/checks). Bei Rot ausschließlich den ersten nachgewiesenen Blocker gezielt reproduzieren. Keine Fach-, Archiv- oder Optimierungsänderung zwischen Schlusscommit und Auswertung. MacBook-Nachtest zusätzlich vorbereitet; Python/Tk, verfügbare Fensterfläche und Quellcommit dort getrennt erfassen. Das Hosted-CI-Desktopwerkzeug darf persönliche Macs nicht verändern.

| Achse | Belegter Stand / Grenze |
|---|---|
| Quelle / Lieferung | App und startbare Python-Fassung bytegleich zu 0e704f3; 93 Code-/171 Ressourcendateien abgeglichen. Gemeinsame finale CI bleibt separat erforderlich. |
| System / Steps | 94 Quelldateien, 147 Featureeinträge inklusive 20 technischer Systemfähigkeiten, 25 Bestandspakete, 311 Test-/Werkzeugdateien. [Übernahmevertrag](../01_Repository/Glide/src/glide/README.md#9-grundlage-für-steps-und-weitere-projekte), eigene Identitäten/Pfade und echte Speicher-/Undo-/Restorewege erforderlich; noch kein Steps-Projekt und keine neutrale Framework-Abnahme. |
| Lizenz / Marketing | MPL-2.0, eigene SPDX-Hinweise, getrennte Fremdlizenzen, Quellbezug und Paket-BOM integriert. Positive Produktbeschreibung und freigegebene 15 Topics gesetzt; aktive Beta-/Erstversionswerbung und allgemeine Versionsbotschaften entfernt, technische/historische Herkunft erhalten. |
| Pakete | Windows-F340 und Mac-0e nativ gebaut/isoliert gestartet, Lizenz-/BOM-Prüfungen belegt. Alte Quellhashes nicht als neue Paketabnahme umdeuten. Keine öffentliche Signierung/Notarisierung oder Releasefreigabe. |
| Archiv / lokale Ablage | 35.380 Dateien/8.284.103.358 Bytes auf E gesichert; 286 Grafik-/Steps-/Vorbereitungsdateien gesondert. Vier Stashes exportiert; 131 Entwicklungsrefs unabhängig aus Bundle geklont und fsck=0. Roh-Git enthält schon vorher beschädigte Codex-Checkpointobjekte; unverändert erhalten, nicht als gesund bezeichnet. Weitere 68 vom Inhaber umgeordnete Inspirationspfade bytegleich vorhandenen Archivdateien zugeordnet. Nur früherer ausdrücklich temporärer Logo-Prüfrest (206.581.655 Bytes) gelöscht. |
| Neue C-Ablage | Noch nicht erzeugt. Erst nach grünem und ausdrücklich genehmigt gemergtem PR, verifiziertem neuen Main und letztem Lokaldelta-/Archivabgleich. Bisheriger Pfad bleibt bis dahin erhalten. |
| Offen | Linux-/macOS-Vollmatrix auf 3.53.0, native Paket-/Startabnahme, vollständige manuelle DPI/Mehrmonitor-/Bedienmatrix (die Sichtabnahme „passt alles“ ist dokumentiert), Signierung/Notarisierung/Release, Marken-/Beitragsrechte und die schon dokumentierten WA-32/36/39/41/46/49/50-Restumfänge. Windows-Volltest bestanden, aber `release_ready=false`; `main` steht nach PR #75 auf `9e767bea` (3.53.0), Tag und Veröffentlichung bleiben unverändert offen. Kein pauschaler Architektur-/Performanceabschluss. Aufgaben allein im Entwicklungsplan §21.83/§21.84. |

## Datierte Vorgeschichte des vorherigen Übergabeeinstiegs

Die nummerierten Abschnitte 1–3 sowie der WA-41-Sofortblock dokumentieren frühere Sitzungen. Für aktuelle Prioritäten gelten der Einstieg oben und der Entwicklungsplan.

Die folgenden Abschnitte dokumentieren die damalige Runde. Ihre alten PR-/Paket-/Metadatenzustände sind durch den aktuellen Einstieg oben fortgeschrieben und keine aktiven Ausführungsanweisungen.

**Fortsetzung am 08.11.2026 (historisch):** Main `d7e017f` enthält #69 und #70; neuer Branch `codex/glide-3.50.7-main-validierung` direkt davon. Gesicherte Übernahme `1b58d1e`, ursprünglicher Codex-Checkpoint `f0c4442`. Vorrang hat jetzt CI-Reparatur gemäß [Plan §21.78](Glide_Entwicklungsplan.md#2178-ci-abschlussauftrag-3507-auf-main-08112026). Die folgende Runde vom 07.11. bleibt datierte Vorgeschichte, keine aktuelle Aussage über einen offenen PR #69. Kein Gesamtabschluss; Main-Vollmatrix rot.

Stand 13.11.2026 · Glide 3.60.0 · Aufgabenformat 26

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
