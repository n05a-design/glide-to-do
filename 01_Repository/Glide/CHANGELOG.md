# Änderungsverlauf

Stand 20.11.2026: Die Versionen 3.51.0 bis 3.33.18 sind am 14.11.2026 nach der Regel „sieben neueste ausführlich“ auf je eine Tabellenzeile gekürzt; ausführliche Einträge und die Nachträge vom 08./09.11.2026 trägt Git.


## 1.0.0 – 17.11.2026 (Quellstand, nicht veröffentlicht)

Der Meilenstein-Schnitt D93 ist in `main`; PR #153 wurde am 19.11.2026 auf Merge-Commit `a53e7790` integriert und hebt das Glide-System auf V1.54. Sein finaler PR-Head `db3bc6ca` bestand Grundstufe, CodeQL, Linux-/Windows-Vollprüfung und Windows-Paketbau in Workflow [#44585014542](https://github.com/n05a-design/glide-to-do/actions/runs/44585014542). Auf dem Merge-SHA `a53e7790` bestanden Main-Grundstufe/CodeQL und das macOS-arm64-Paket samt isoliertem Start; die native macOS-Vollsuite wurde übersprungen. Die Linux/Tk-9.1-Vollprüfung läuft noch; ihr Endstatus steht im [QA-Bericht](docs/07_QA_BERICHT.md). Kein Tag und kein GitHub Release sind veröffentlicht; Homebrew-/winget-Einreichung und menschliche Abnahme bleiben offen. Datenformat 26 und Austauschformat 2 unverändert. PR #148 ergänzt die DE/EN-Lokalisierung des Einstellungsdialogs; PR #150 integriert Seiteneditor, Aktionsfeedback, Shell-Modifier, Aufgabeninspektor, Kalenderfelder, Editorstatus und Mehr-Menü sowie den Dialogumbruchfix. Frühere rote Läufe und ihre damaligen Prüfkandidaten bleiben im QA-Bericht historisch dokumentiert und sind nicht der aktuelle Status.

- **Shell-Handbuch für KI-Agenten (V1.69, 21.11.2026):** `docs/GLIDE_SHELL_KI_HANDBUCH.md` und der Projekt-Skill `glide-shell` bündeln Bausteine, Host-Verträge, erzwungene Regeln, Tests, Prüfwege, Versionierung, Übernahme und Git-Ablauf der Glide Shell.
- **Shell-Bausteine nach D98 (V1.69, 21.11.2026):** `text_fit` (Text auf Zeichen- oder Pixelbreite kürzen, Zeichen auf gleiche Breite bringen), `action_picker` (durchsuchbare Aktionsauswahl aus einem fertigen Menü) und `runtime_paths` (Daten- und Cacheordner nach Plattformkonvention, Umgebung und Zeiger) sind Teil von `glide_shell` 0.5.0. `ui_design`, `action_menu` und `runtime_config` reichen sie weiter und behalten Grenzen, Texte und Glide-Namen. Der Selbsttest prüft zehn Bereiche. Kein sichtbares Verhalten.
- **Glide Shell für Folgeprojekte (V1.68, D97, 21.11.2026):** `python -m glide_shell.selftest` prüft eine übernommene Shell mit echtem Tk auf dem Zielrechner, auch unter `python -O`. Der Demohost zeigt zusätzlich Fensterlage, Hell/Dunkel nach System und Rückgängig/Wiederholen. Neue Anleitung im Paket auf Deutsch und Englisch, die das Übernahmewerkzeug mitkopiert. `glide_shell` 0.4.0. Kein sichtbares Verhalten der App.
- **Shell-Bausteine nach D96 (V1.67, 21.11.2026):** `window_geometry` (Fenstergeometrie), `system_appearance` (Hell/Dunkel des Systems) und `redo_history` (Wiederholen-Stapel) sind Teil von `glide_shell` 0.3.0; `compact_mode`, `appearance` und `undo_history` reichen dieselben Objekte weiter. Laufzeittexte der Shell für Entwickler sind Englisch. Kein sichtbares Verhalten.
- **Shell-Paket 7: `motion` und Übernahmewerkzeug (V1.66, D95, 21.11.2026):** `motion` ist fünfter Baustein von `glide_shell` (`SHELL_VERSION` 0.2.0), der Demonstrationshost zeigt einen Übergang im eigenen `AfterScope`. `scripts/pflege/shell_uebernehmen.py` übernimmt das Paket mit Manifest in Folgeprojekte und prüft bestehende Kopien; lokale Änderungen bleiben ohne `--ersetzen` geschützt, seit V1.67 auch eigene Dateien, die eine neue Shell-Datei gleichen Namens überschreiben würde. Kein sichtbares Verhalten.
- **DE/EN-Zeichenimport, Symbolvorschau und Farbwahl (V1.65, 21.11.2026):** Symbolvorschau, Import- und Einfügevorschau, Ersetzen durch Import, Import als neue Zeichnung und Farbwahl folgen der aktiven Sprache; die Importzusammenfassung unterscheidet Einzahl und Mehrzahl. Standardtitel neuer Zeichnungen und Fehlertexte der Zeichenmodule bleiben unverändert. Offen im Zeicheneditor: Bildfolgen-Dialog und -Export, Journal-Untermenü, Modulfehlertexte.
- **Shell-Paket `glide_shell` und Demonstrationshost (V1.64, D95, 20.11.2026):** Die vier Shell-Bausteine liegen als Unterpaket `src/glide/glide_shell` mit eigener Paketversion 0.1.0; `python -m glide_shell.demo` startet einen Beispielhost nur aus Shell-Bausteinen. Folgeprojekte übernehmen den Ordner unverändert (Shell-Konzept §7). T330 belegt die Paketgrenze mit kopiertem Paket ohne Glide. Kein sichtbares Verhalten der App geändert.
- **DE/EN-Zeichendialoge (V1.63, 20.11.2026):** Farbe ersetzen, unbenutzte Farben, Zwischenstände, Zeichnung leeren, Referenzbild laden/neu rahmen/entfernen, Rahmen einpassen und Nachzeichnung prüfen folgen der aktiven Sprache, mit Einzahl/Mehrzahl statt „(n)“. Gespeicherte Zwischenstandsnamen und Aktionskennungen bleiben unverändert. Offen: Import-, Bildfolgen-, Symbolvorschau- und Farbwahldialoge sowie zwei „(n)“-Texte in Import und Austausch.
- **Shell-Restkopplung R3/R4 (V1.62, D94, 20.11.2026):** Alle 104 Zeitgeberaufrufe laufen über einen `AfterScope`, alle Dialoge über `modal_session.create_dialog`; direkt erzeugt wird nur noch der Tooltip. Die Sperrklinke steht auf 1 direktem Fenster und 0 Zeitgebern ohne Bereich. Kein sichtbares Verhalten geändert.
- **Shell-Restkopplung R2 (V1.61, D94, 20.11.2026):** 53 Zeitgeber der Wurzel, eigener Widgets und Dialoge laufen über einen `AfterScope` und enden mit ihrem Fenster; 11 bleiben ohne Bereich. `AfterScope` räumt am Widget abgebrochene Kennungen beim Planen auf. Die Sperrklinke zählt `_register_after`, `adopt` und `scope_for` jetzt korrekt als Bereich; die in V1.60 genannte Zahl 98 war zu hoch, richtig waren 64. Kein sichtbares Verhalten geändert.
- **Shell-Restkopplung R1 (V1.60, D94, 20.11.2026):** `modal_session.create_dialog` ist der gemeinsame Erzeugungsweg für Dialogfenster; 29 Dialoge nutzen ihn über die Fassade `ListApp._new_dialog`, direkte `tk.Toplevel` sinken von 46 auf 17. Eine Sperrklinke in `test_shell_importregel.py` verhindert neue direkte Fenster und neue Zeitgeber ohne `AfterScope`; der Modal-Vertrag hat 18 Fälle und zehn Gegenproben. Kein sichtbares Verhalten geändert.
- **Englische Benutzerdokumentation (20.11.2026):** `docs/user-guide/` enthält einen englischen Guide mit zwölf Themenseiten (Getting Started bis Troubleshooting) als kontrollierte Übersetzung von `docs/20_FUNKTIONEN.md`; die deutsche Quelle bleibt maßgeblich. Der Guide benennt den unvollständigen DE/EN-Oberflächenstand offen und führt noch deutsche Menü- und Dialogbeschriftungen kursiv mit englischer Erläuterung. Index, Pflegematrix, README, README.de und SUPPORT verweisen darauf; T299 `test_standpruefung.py` prüft Seitenliste, DE↔EN-Gegenverweise und Abschnittsanker in die deutsche Quelle; Glide-System V1.59 führt die erweiterte T299-Abdeckung. Keine App-, Datenformat-, Wiki- oder Releaseänderung.
- **PR-#156-Reparatur (20.11.2026):** Die gemeinsame `SavedFilters`-Enum-Normalisierung prüft gültige Speicherkennungen statt lokalisierter Anzeigenamen. Die Änderungen wurden in PR #156 am Merge-Commit `4b6bce08` nach `main` übernommen. Auf dem PR-Head bestanden Dokumentation/YAML/Stand, Linux-Grundstufe sowie Analyze Actions/Ruby; die Linux/Tk-9.1-Vollprüfung lief bei letzter Abfrage, mehrere native Accessibility-/UI-Jobs wurden übersprungen. `test_wissen33315.py`, alle 14 Ansichtenfälle einschließlich Persistenz und lokale CI-Grundstufe bestanden. Das ist kein Release oder Lieferwechsel.
- **DE/EN-Zeicheneditor-Status (V1.56-Teilstand, 20.11.2026):** Statuszeile, Werkzeug-/Muster-/Symmetrieangaben und Kernmeldungen für Auswahl, Kopieren, Undo und Redo folgen der aktiven Sprache; stabile Zeichen- und Aktionswerte bleiben unverändert. Dieser Teilstand ist mit der Fortsetzung in PR #157 enthalten. T118 prüft die Oberfläche, T329 die dynamischen Katalogschlüssel. App-Version 1.0.0 und Datenformat 26 unverändert; weitere Dialoge, externe Zeichenaktionen, dynamische Undo-Texte und menschliche Sichtprüfung bleiben offen.
- **DE/EN-Zeicheneditor-Steuerung (PR #157, gemergt 20.11.2026):** Werkzeugwahl, Anzeigeprofile, Referenz-/Vorschauknöpfe, Zoom- und Optionsmenüs sind in beiden Sprachen verfügbar; stabile Werkzeug-, Profil-, Muster- und Auswahlwerte bleiben unverändert. T118 prüft die Oberfläche und `test_i18n.py` die Katalogschlüssel. Animationsleiste, Mehr-Menü-Inhalte, weitere Zeichen-/Exportdialoge und menschliche Sichtprüfung bleiben offen; PR #157 ist als `55ad7e95` in `main`.
- **DE/EN-Zeicheneditor-Animation, Mehr-Menü, Paletten und Export (V1.58, 20.11.2026):** Animationsleiste, Bildauswahl, Abspieldialog, Pipettenhinweis der Kontextleiste, alle Einträge des Zeicheneditor-Mehr-Menüs, das Palettenmenü mit Speichern/Importieren/Exportieren/Löschen sowie Dateidialoge, Status- und Fehlertitel des PNG-, ICO-, SVG- und JSON-Exports folgen der aktiven Sprache. Palettenmeldungen unterscheiden Einzahl und Mehrzahl. Menübefehle, Paletten-IDs, Exportformate und Standard-Dateinamen bleiben unverändert. T118 ergänzt `drawing_more_locale` und `drawing_export_locale`. Offen bleiben das mit Seiten geteilte Journal-Untermenü, Import-, Referenz-, Nachzeichen-, Zwischenstands-, Bildfolgen- und Farbdialoge sowie Fehlertexte aus `glide_drawing`.

PR #154 bündelt Community- und Übergabeunterlagen sowie strukturelle Prüfungen. Die GitHub-Einstiege und Vorlagen werden nach dem Steps-Muster englisch zuerst angeboten; vollständige deutsche Gegenfassungen bleiben verlinkt. PR #154 ist offen und nicht gemergt; Remote-Prüfungen sind dem aktuellen Head zuzuordnen. Diese Änderungen aktivieren weder Wiki, Project, Funding, Tag/Release noch externe Kontofunktionen.

- Öffentliche GitHub-Projektseite: Die deutsche README wurde auf den Einstieg gekürzt; `README.en.md` ergänzt eine vollständige englische Fassung. Der Downloadstatus bleibt ausdrücklich unveröffentlicht.
- **English-first GitHub-Einstieg:** `README.md` ist nun die englische Primärseite, `README.de.md` die deutsche Fassung. Contributing- und Security-Einstiege haben ebenfalls englische Standarddateien und verlinkte deutsche Fassungen; Support, Verhaltensgrundsätze, PR-Vorlage und Issue-Formulare zeigen Englisch zuerst. Die GitHub-About-Beschreibung bleibt derzeit deutsch, weil GitHub die Änderungsanfrage mit HTTP 404 ablehnte.
- **Folgekorrektur Tooltip-Callback (Glide-System V1.54):** Der `<Motion>`-Callback der Tooltip-Bindung akzeptiert auch einen Aufruf ohne Eventobjekt. Die Linux-/Windows-Vollprüfung und der Windows-Paketbau bestanden auf dem finalen PR-#153-Head.
- **Folgekorrektur ButtonFlow (Glide-System V1.53):** Der ButtonFlow-Layoutdurchlauf beendet wiederkehrende, nicht aufeinanderfolgende Breiten mit der engsten beobachteten Breite und misst nach einer tatsächlichen Toplevel-Größenänderung neu. T312 prüft A-B-A-B-Zyklen. Der Fix ist Teil des final geprüften V1.54-Stands.
- **Folgekorrektur Dialogumbruch (Glide-System V1.48):** PR #152s Linux-Vollprüfung auf Head `f34fb73d` scheiterte erneut beim initialen Öffnen des Einstellungsdialogs (`schriftstile`). Der lokale Fix verschiebt die beiden Spaltenumbrüche hinter die anfängliche Fenstergeometrie; gezielter macOS-Test und 23 UI-Layout-Unit-Tests bestehen. Linux-Nachprüfung steht aus; keine App-Versions- oder Datenformatänderung.
- Werkzeugtest T299 prüft die Sprachumschaltung, Kernabschnitte, lokalen Datei-Links und englische Primärsprache der öffentlichen Einstiegspunkte.
- Mehrsprachigkeit (i18n DE/EN, Etappe 2): Zentrales i18n-Subsystem (`src/glide/i18n.py`, `de.json`, `en.json`) mit dynamischer Spracherkennung, Spracheinstellung, lokalisierten Menüs und ausgewählten Seitenleistenbeschriftungen. PR #148 ergänzt in `main` den Einstellungsdialog samt Auswahlwerten, Hilfen, Design-/Hintergrundnamen und Validierungsfehlern; PR #150 integriert weitere DE/EN-Flächen in Seiteneditor, Aktionsfeedback, Modifier-Beschriftungen, Aufgabeninspektor, Kalenderfelder, statische Editorstatusmeldungen und gemeinsames Editor-Mehr-Menü; gespeicherte Werte bleiben unverändert. Die vollständige Lokalisierung bleibt offen: weitere Dialoge, dynamische Undo-Toasts, Status-/Fehlertexte und Validierungsausnahmen sind teilweise deutsch. T329 prüft Katalogparität, Platzhalter, direkte App-Schlüssel und dynamische UI-Schlüssel.
- Installer & Paketierung (Etappe 3):
  - macOS: DMG-/TAR-Bauweg vorbereitet; die lokale Ad-hoc-Signatur ist keine Developer-ID-Signatur oder Notarisierung. Homebrew-Cask (`packaging/homebrew/Casks/glide.rb`) ist eine nicht eingereichte Vorlage.
  - Windows: Inno-Setup-Installer (`packaging/windows/glide_setup.iss`) mit stiller Installation (`/VERYSILENT`), Deinstallationsroutine und winget-Manifesten (`packaging/winget/manifests/s/Shaye/Glide/1.0.0/`) als technische Vorbereitung.
- KI-Agenten-Skill `glide-to-do` (Etappe 1): Exportierbarer und standardisierter KI-Skill für Claude Desktop, Cursor, Gemini CLI und Web-LLMs mit automatischer Prüfsummenvalidierung (`MANIFEST.json`).
- Veröffentlichung & CI/CD (Etappe 4): Automatisierte GitHub Actions Release-Pipeline (`.github/workflows/release.yml`) ist für Tags vorbereitet. Ein öffentliches Release und Release-Artefakte wurden nicht veröffentlicht.
- Qualitätssicherung & Systemregister: 100 Module (M001–M100), 329 Test-/Werkzeugdateien (T001–T329), Glide-System V1.54 auf `main` (PR #153). Der PR-#153-Head bestand die vollständige Linux-/Windows-Matrix und den Windows-Paketbau. Die nachgelagerten Main-/CodeQL-Prüfungen und der macOS-Paketbau auf Merge-SHA `a53e7790` sind davon getrennt und im QA-Bericht mit ihrem Live-Endstatus nachzuführen. Modulbudget WA-50 eingehalten. Main-, Liefer- und Freigabestand sind getrennt zu betrachten.
- **Gemini-Wissensbasis:** 20 thematische Module plus Index, Core Knowledge Pack, Source Manifest, Knowledge Gaps, Import Guide, Changelog und Audit-Summary unter `docs/ai/gemini/`. Englischsprachige, quellengebundene Ableitung des PR-#152-Snapshots `5631333a`; keine neue Produkt- oder Dokumentationsautorität. Zentrale Indexierung, relative Markdown-Links, Standregeln, Datenschutz und lokale CI-Grundstufe sind bestanden; der QA-Bericht dokumentiert die Grenzen einschließlich nicht abrufbarer Fremdpaket-Herkunft.
- **Glide-System V1.49 / T207 Diagnose:** `test_ui39.py` schreibt Fortschritts- und Stackdiagnosen, fängt einen blockierenden modalen Fehlerhinweis im Test ab, behält die Callback-Fehlerassertion und ergänzt einen isolierten `ui39`-Dispatch für Linux/Tk 9.1 und Windows/Tk 9.1. Der lokale macOS-Stack belegt den modalen Wartepfad, aber noch nicht die auslösende Callback-Ausnahme; beide GitHub-Vollprüfungen bleiben rot. Keine App-Version-, Datenformat- oder Paketfreigabeänderung.
- **Glide-System V1.50 / T207-Prüfnachtrag:** Der isolierte `test_ui39.py`-Dispatch besteht auf Linux/Tk 9.1 und Windows/Tk 9.1 bei aktiver Callback-Fehlerassertion. Die historischen Volltest-Timeouts und der lokale macOS-Callback-Auslöser bleiben ungeklärt; der aktuelle Linux-Volljob stoppte vor den Tests bei der Laufzeitinstallation. App-Version 1.0.0, Datenformat 26 und Paketfreigaben unverändert.
- **Glide-System V1.51 / T207-Diagnosekorrektur:** Der Tk-Callback-Collector wird nach der `ListApp`-Initialisierung erneut installiert, damit ein Fehlerhinweis des app-eigenen Handlers den Test nicht modal blockiert; Ausnahmen bleiben mit Traceback erfasst und per Assertion sichtbar. Fünf lokale Läufe bestanden danach auf macOS/Tk 9.0.3. Der vorherige `TypeError` wurde nicht reproduziert; seine Ursache und die remote Prüfung des korrigierten Testcodes bleiben offen. App-Version 1.0.0, Datenformat 26 und Paketfreigaben unverändert.
- **Glide-System V1.52 / Tk-Callback-Robustheit:** `bind_mousewheel` toleriert fehlende Eventobjekte und behandelt den ereignislosen Aufruf als folgenlos; `RoundedButton` toleriert sie bei Fokus-Neuzeichnung. Ein gezielter Tk-Callback wurde ohne Argumente für `<Button-4>`, `<Button-5>` und `<TouchpadScroll>` beobachtet; die Ursache der fehlenden Tcl-Substitution bleibt offen. `test_befunde330.py` prüft die ereignislosen Bindungsaufrufe, sechs lokale `test_ui39.py`-Läufe bestanden auf macOS/Tk 9.0.3, `test_linux_gegenproben.py` 4/4 und die CI-Grundstufe bestand nach Anpassung ihres Scroll-Mutationsankers. App-Version 1.0.0, Datenformat 26 und Paketfreigaben unverändert.


## 3.70.0 – 17.11.2026

Agenten-Skill `glide-to-do` komplettiert (WA-61 Pakete K3, K4, K5) und Meilensteinschnitt Release 1.0 (D93). Datenformat 26 und Austauschformat 2 unverändert.

- Skill-Paket K3 (Erweiterte Austauschfähigkeiten): Automatische Vorsicherung vor Create-Import (`vor_import_*.glidebackup`), Markdown-Seiten und -Notizen (`markdown` -> `rich_note` mit Aufgabenextraktion), Ordnerarten (`library`, `journal`, `standard`), Wiederholungsregeln (`repeat` tolerant EN/DE) und Erinnerungen (`reminder`). Neuer Integrationstest T327 (`test_austausch_k3.py`, 6/6 OK).
- Skill-Paket K4 (Bilder & Anhänge): ZIP-Container-Erkennung (`.glideexchange`, `.zip`) mit Zip-Slip-Schutz (`inspect_exchange_archive`), physischer Import von Anhängen für Ordner/Listen/Aufgaben in `ATTACHMENTS_DIR` mit automatischer Konfliktbereinigung (`store_attachment`), Galerielisten (`list_kind: "gallery"`), Seiten-Cover (`cover`), Markdown-Bildauflösung in Notizen, Paketausgabe (`write_exchange_package`) und atomare Rollback-Bereinigung. Neuer Integrationstest T328 (`test_austausch_k4.py`, 9/9 OK).
- Skill-Paket K5 (Verteilung & Ökosystem): Maschinenlesbares `MANIFEST.json` mit Hashes aller 18 Skill-Dateien, Verteilungsdokumentation `VERTEILUNG.md` für Claude Desktop, Cursor, Gemini CLI und Web-LLMs, Menüaktion Datei › Datenaustausch › KI-Skill exportieren … (`export_agent_skill`), GitHub Actions Release-Workflow packt `glide-to-do-skill-v$VERSION.zip` samt Prüfsummen.
- Meilenstein Release 1.0 (D93): Verbindlicher Meilenstein-Fahrplan `00_Arbeitsvorbereitung/Glide_Meilenstein_v1_Plan.md` und Tracking in GitHub Issue #129 verankert. Etappe 1 abgeschlossen, Vorbereitung für Etappe 2 (Mehrsprachigkeit i18n DE/EN).
- Prüfung & Systemregister: Glide-System auf V1.39 gehoben (328 Test-/Werkzeugdateien), Werkzeugtest T321 (18/18 OK), CI-Grundstufe 19/19 OK, Standprüfung 0 Befunde, 07-Lieferabgleich 0 Abweichungen.


## 3.69.0 – 16.11.2026

Ganzheitliche Dokumentations- und Übergabekonsolidierung, Audit-Bereinigung und Headless-CI-Absicherung. Datenformat 26 unverändert.

- Übergabe & Audit: `00_Arbeitsvorbereitung/Glide_Uebergabe.md` ganzheitlich und kontextbasiert für nachfolgende KI-Agenten ausgebaut (Status V1.36, D86–D90, 4 Shell-Bausteine, Skill WA-61/D92, Dokumentenautorität, priorisierte Handlungsfolge, Schutzregeln).
- Entwicklungsplan: `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md` auf aktuellen Stand synchronisiert, Arbeitsvorrat bereinigt, Anker korrigiert (§21.107).
- Sicherheitsrichtlinie: `SECURITY.md` und `01_Repository/Glide/SECURITY.md` auf Stand 16.11.2026 synchronisiert.
- CI-Absicherung: `tests/unit/test_desktop_adapter.py` mit Headless-SkipTest-Absicherung für Display-freie Umgebungen ergänzt; Linux-Grundstufe (Tk 8.6) grün.
- Prüfung: Standprüfung 0 Befunde, Testkatalog V1.36 5/5, Unit-Tests 1.230/1.230 grün, Vertragstests 100 % grün, CI-Grundstufe mit 19/19 Schritten bestanden (Exitcode 0).
- Nachtrag 16./17.11.2026 (ohne Versionswechsel, PR #119): `test_desktop_adapter.py` prüft die Zwischenablage über eine Attrappe, weil der Test unter Windows/Tk 9.1 mit `0xC0000005` abstürzte und die echte Zwischenablage überschrieb; `test_ki_ausgabe_darstellung.py` (T325) läuft in der Vollprüfung mit (114 Suiten); Shell-Konzept, Architektur, Prüfliste und Übergabe nachgezogen; `test_desktop_adapter.py` führt die Testkennung T326 statt der schon vergebenen T313 (Glide-System V1.37).


## 3.68.0 – 16.11.2026

Shell-Paket 5: Aktionen, Menüs und Desktop-Adapter (`desktop_adapter.py`, D86, D88). Datenformat 26 unverändert.

- Neues Shell-Modul `desktop_adapter.py` (nur Standardbibliothek und `tkinter`): Lagert anwendungsneutrale Menü-, Tastaturkürzel- und Plattformfunktionen aus `app.pyw` aus (`build_menu_tree`, `DesktopMenuBar`, `launch_path`, `copy_to_clipboard`, `read_from_clipboard`, `format_accelerator`, `format_redo_accelerator`, `primary_modifier`).
- Plattformgerechte Menüleiste: Kapselt Menüaufbau, Windows-Kopfleiste (`custom_menubar`) mit Mnemonics und Popup-Behandlung sowie macOS/Linux-Systemmenübindung (`root.config(menu=menubar)`).
- Einhaltung des Modulbudgets (WA-50): Alle Funktionen bleiben unter 50 Zeilen und Schachtelungstiefe 15.
- Prüfung: Neuer Unit-Test `test_desktop_adapter.py` (T313, 13 Fälle), `test_shell_importregel.py` (T319) um `desktop_adapter` erweitert (7/7 grün). Modalvertrag (17 Fälle), Abbauvertrag (5 Fälle) und Fensterlebensdauer (9 Fälle) grün. Ergebnisse im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3680--shell-paket-5-desktop_adapterpy-16112026).


## 3.67.0 – 16.11.2026

Shell-Paket 4: Erscheinungsbild und Bedienelemente ausgelagert (`custom_controls.py`, D88). Datenformat 26 unverändert.

- Neues Shell-Modul `custom_controls.py` (nur Standardbibliothek und `tkinter`): Lagert die anwendungsneutralen Canvas-Bedienelemente `CanvasLabel`, `GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`, `ThemedAutoScrollbar` sowie die Hilfsfunktionen `rounded_rect_points`, `bind_resize` und `paint_canvas_backdrop` aus `app.pyw` aus (~1.440 Zeilen).
- Saubere Entkopplung: Farb- und Schriftanpassungen an den Hostzustand erfolgen über entkoppelte Callback-Hooks (`set_font_provider`, `set_ink_provider`, `set_backdrop_painter`). `app.pyw` re-exportiert alle Steuerelemente drop-in-kompatibel.
- Einhaltung des Modulbudgets (WA-50): Alle Funktionen bleiben unter 50 Zeilen und Schachtelungstiefe 15.
- Prüfung: Neuer Integrationstest `test_custom_controls.py` (T312, 11 Fälle), `test_shell_importregel.py` (T319) um `custom_controls` erweitert. Alle 7 Shell-Importregeln und der Modalvertrag (17 Fälle) grün. Ergebnisse im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3670--shell-paket-4-custom_controlspy-16112026).

## 3.66.0 – 16.11.2026

Zentrierter Agenten-Skill `glide-to-do`, strenge Datenformatkopplung und Darstellungsprüfung (WA-61, D91/D92). Datenformat 26 unverändert.

- Neuer Agenten-Skill `glide-to-do` unter `skills/glide-to-do/` nach dem Agent-Skills-Standard (`SKILL.md`, Hilfsskript, Referenzen, Beispieldateien, Einrichtungsanleitungen für Claude, OpenAI und Google).
- Strenge Datenformatkopplung: `abdeckung.json` ordnet jedes Feld des Aufgabenformats 26 verbindlich ein. Werkzeugtest T321 `test_agenten_skill.py` gleicht Skill-Regeln, Konstanten und Datenmodell ab; Formatänderungen ohne Skillanpassung werden in der CI abgewiesen.
- Zentrales Prüfwerkzeug T323 `tests/tools/ki_ausgabe.py` und Werkzeugtest T324 `test_ki_ausgabe.py`: prüft KI-Ausgaben in vier Stufen auf Format, Glide-Regeln, Import und Anzeige.
- Vollprüfungs-Integrationssuite T325 `tests/integration/test_ki_ausgabe_darstellung.py`: prüft alle Skill-Beispiele, Formatgrenzen und fehlerhafte Ausgaben mit echter Tk-Oberfläche, Speichern, Prozessneustart und Anzeigeablesung.
- Entwicklungs-Skill `glide-aufbau` (`.claude/skills/glide-aufbau/`) und Referenz `glide-aufbau.md` als strukturierte Einstiegshilfe zum Verständnis von Glides Daten- und Objektmodell.
- Prüfung: Werkzeugtests 21/21, Skilltest 15/15, Ki-Ausgabeprüfung 6/6, Vollprüfungs-Integrationssuite grün. Ergebnisse im [QA-Bericht](docs/07_QA_BERICHT.md).

## 3.65.0 – 16.11.2026

Fokusrückgabe nach modalen Dialogen (D87). Datenformat 26 unverändert.

- Nach dem Schließen eines modalen Dialogs liegt der Tastaturfokus wieder auf dem Feld, das ihn vorher im aufrufenden Fenster hatte – auch bei Unterdialogen über einer Maske. Bisher hing das vom Fenstermanager oder vom einzelnen Aufrufer ab.
- Die Shell (`modal_session.py`) merkt sich den Fokus mit `remember_focus` und gibt ihn mit `return_focus` zurück. Ist das Feld inzwischen verschwunden, erhält das Fenster den Fokus; ein drittes Fenster, das der Dialog geöffnet hat, behält ihn. Aufrufer, die danach selbst einen Fokus setzen, behalten das letzte Wort.
- Prüfung: `test_modalvertrag.py` mit 17 statt 13 Fällen und neun statt sechs Gegenproben. Ergebnisse im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3650--fokusrückgabe-16112026).

## 3.64.0 – 15.11.2026

Shell-Paket 3c: Zeitgeber gehören einem Fenster oder einer Ansicht. Sichtbares Verhalten und Datenformat 26 unverändert.

- Neues Tk-Modul `window_lifetime.py` (nur Standardbibliothek und `tkinter`): Ein Zeitgeberbereich führt die Zeitgeber eines Widgets, bricht sie mit dem Widget ab und nimmt danach keine neuen an. `ListApp.after_scope` und `_register_after` sind Fassaden.
- Sieben Zeitgeber, die bisher an keiner Stelle geführt wurden, gehören jetzt einem Bereich: zuletzt geöffnete Seiten, Abholen und Abgleich des Hintergrundverlaufs, festes Layout, leere Rahmen, Symbole der Systemnavigation und die Dreieckmarker der Bäume.
- Prüfung: `test_fensterlebensdauer.py` (neun Fälle, sechs Gegenproben), `test_shell_importregel.py` mit der zentralen Liste der Shell-Module (D86); der Abbau-Vertragstest prüft zusätzlich das Schließen bei offener Rückfrage. Ergebnisse im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3640--shell-paket-3c-15112026).

## 3.63.2 – 15.11.2026

Zweite Korrekturversion nach dem CI-Volllauf: Befunde, die erst nach der Lieferung von 3.63.1 sichtbar wurden. Datenformat 26 unverändert.

- Kompaktkopf: Suche, Erfassung, Menü und Normalansicht sind alle 28 px hoch wie der „…“-Knopf nach D85. Zuvor stand der Menüknopf mit 28 px zwischen 38 px hohen Nachbarn (`test_arbeitsmodi`, Fall `kompakt`).
- Bereichspfeile der Seitenleiste stehen auch unter Linux auf der Großbuchstabenmitte: Die Ausrichtung des gezeichneten Dreiecks brach ab, wenn die Symbolschrift ▾ nicht enthielt (Linux-CI `test_uiux_paket` b09, 1,17 px).
- Version und aktuelle Fixtures auf 3.63.2 angehoben. Prüfungen und Grenzen im QA-Bericht.

## 3.63.1 – 15.11.2026

Korrekturversion: Der CI-Volllauf 3.63.0 stoppte unter Linux bei `test_features323`; dahinter lagen weitere Befunde. Datenformat 26 unverändert.

- Der Anzeigeknopf der Zeichenleiste zeigt nur den Profilnamen mit Menümarker („Standard ▾“). Mit „Anzeige: …“ (180 px) passten die drei Pflichtknöpfe bei 860 × 700 nicht (`test_mindestgroesse330`). `test_features323` erwartet die Tagespfeile ◂/▸.
- Zeilenaktionen werden beim Scrollen nur umgesetzt statt alle Knöpfe und Bänder zu entfernen und neu zu setzen. Das Scrollen der Liste kostete seit den Zeilenbändern etwa 85 statt 50 ms je Bild (`test_tempo330`, Windows/Tk 9); jetzt wieder ~50 ms, die Tabelle ~18 statt 41 ms. `test_kompression330` und `test_notizbereich330` prüfen Klapppfeil und Spaltentitel gegen die aktuellen Konstanten.
- `test_bedienung33316` erlaubt die von D84 gewollten gemeinsamen Dreieckzeichen ausdrücklich, auch „Verspätet“ = „Nach oben“ (▴). Gleiche Nutzung soll nicht in unterschiedlichen Zeichen auseinanderlaufen (Inhaber 15.11.2026).
- Version und aktuelle Fixtures auf 3.63.1 angehoben. Prüfungen und Grenzen im QA-Bericht.

## 3.63.0 – 15.11.2026

Mit `main` 3.62.0 zusammengeführt: 3.63.0 enthält die Änderungen aus 3.61.0 und 3.62.0. Entscheidungen des Kandidaten heißen D84/D85 (zuvor D81/D82), der Systemkatalog V1.28/V1.29. Veraltete Dokumentstellen zu Blätterzeichen, Zeilenaktionen und Zeicheneditor sind korrigiert; Nachweis im [QA-Bericht](docs/07_QA_BERICHT.md#zusammenführung-3630-mit-main-3620-15112026).

Nachabnahme desselben lokalen Versionskandidaten:
- Bereichsüberschriften und Angeheftet verwenden die Größe der Ordnerdreiecke. Vor-/Zurück-Knöpfe verwenden größere Glyphen aus dem Symbolbegleiter.
- „…“-Knöpfe ohne Outline und mit kompakter Grundhöhe; die Aktionsspalte setzt Zeilenhover und Auswahl nahtlos fort, ohne weißes Knopffeld. Knopfhover übernimmt den Hover für die ganze Zeile.
- Benachrichtigungen: „Alle bis morgen“ verschiebt aktuell offene Aufgaben- und Tageshinweise auf morgen 09:00 Uhr Ortszeit. Bereits geplante Zukunftstermine bleiben erhalten; zukünftig aufgeschobene Tageshinweise werden nicht mehr im offenen Badge gezählt.
- Zeicheneditor: persistierte Anzeigeprofile Standard, Erweitert, Animation und Bilder pixeln. Standard behält Grundwerkzeuge, Erweitert zeigt beide Zusatzleisten, Animation zeigt die Bildfolge, Bilder pixeln die Referenzaktionen. Mehr-Menüs erhalten die ausgeblendeten Funktionen.
- Tabellen: Baumspaltenüberschriften berücksichtigen den Indikatorplatz. Eigene Drag-Handler lassen native Kopf-/Trennlinienklicks wieder passieren; Sortierung wechselt tatsächlich auf-/absteigend.
- Gezielte Bedien-/Geometrie-/Fehlerprüfungen im QA-Nachweis; Systemkatalog V1.29. App- und Datenformatversion bleiben 3.63.0 / 26.

- Kleine, gefüllte Dreiecke (Inhaberwahl B) ersetzen die unterschiedlichen Outline-/Vollmarker. Bereichsüberschriften, Angeheftet und Auswahlfelder teilen die flache Rasterform mit allen ttk-Baumansichten; Größen folgen der Schrift.
- Appweite Dreieckzeichen für Navigation, Sortierung und weitere Beschriftungen auf die kompakte gefüllte Familie vereinheitlicht. Aufklapptext in gespeicherten Seiten bleibt unverändert.
- Version und aktuelle Fixtures auf 3.63.0 angehoben; Datenformat 26 unverändert. Prüfungen und Grenzen im QA-Bericht.

## Prüfwerkzeuge – 14.11.2026 (nach 3.62.0)

- **Abbauvertrag:** `test_abbauvertrag.py` schließt eine vollständige App über den normalen Weg und belegt: Hauptfenster abgebaut, Datensperre frei, kein Zeitgeber und kein später Rückruf danach; dazu drei Gegenproben. Teil von `SUITEN`. Vorstufe zur Fensterlebensdauer in der Shell. [QA-Bericht](docs/07_QA_BERICHT.md#abbau-vertragstest-auf-3620-14112026)
- App 3.62.0 und Datenformat 26 unverändert; Glide-System V1.27.

## 3.62.0 – 14.11.2026

- **Shell-Fundament, erster Baustein (Paket 3a):** Jeder modale Dialog wartet jetzt über das neue Modul `modal_session.py`. Es kennt nur Tk; Theme-Farbe, Bildschirmanteil und Fehlerprotokoll kommen von Glide. `run_modal`, `modal_over`, `ensure_dialog_min_width` und `bring_dialog_to_front` bleiben als Fassaden in `ListApp`, ihre 58 bzw. 6 Aufrufer sind unverändert. Verhalten unverändert.
- **Prüfungen:** `test_modal_session.py` prüft, dass das Modul nur Standardbibliothek und `tkinter` importiert. Die Gegenproben des Modalvertrags verändern jetzt das neue Modul.
- Glide-System V1.26; Datenformat 26 unverändert. Prüfumfang und Grenzen im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3620-14112026).

## Vertriebsentwürfe – 14.11.2026

- **Installation per Terminal (WA-60, Vorschlag):** Vorlagen für `winget install Shaye.Glide` und einen Homebrew-Cask aus den Release-Dateien unter `packaging/winget` und `packaging/homebrew`; nichts eingereicht, Prüfsummen bis zum veröffentlichten Release offen. Startmenüeintrag erst mit dem Inno-Setup-Installer. [Veröffentlichung](docs/10_VEROEFFENTLICHUNG.md#winget-und-homebrew-entwurf)
- App 3.62.0 und Datenformat 26 unverändert.

## Prüfwerkzeuge – 14.11.2026

- **Modalvertrag:** `test_modalvertrag.py` hält fest, was `run_modal` und `modal_over` heute garantieren: echter Grab in 13 Fällen, dazu sechs Gegenproben; Teil von `SUITEN`. Vorstufe zum Shell-Paket Fenster/Modal/Abbau. [QA-Bericht](docs/07_QA_BERICHT.md#modal-vertragstest-auf-3610-14112026)
- App 3.61.0 und Datenformat 26 unverändert; Glide-System V1.25.

## 3.61.0 – 14.11.2026

- **Überlastungsgründe sichtbar (D81):** „Tag entlasten“ nennt unter der Vorher/Nachher-Bilanz je überplantem Tag die Gründe; ein entlasteter Tag zeigt die Gründe davor und „nachher nicht mehr überplant“. Die Einzahl lautet jetzt „1 Aufgabe ohne Aufwandsschätzung kann …“. [Handbuch](docs/20_FUNKTIONEN.md#tageskapazität-und-entlastung-seit-3550).
- **Datenordner nicht erreichbar (D82):** Statt still abzubrechen nennt Glide Pfad und Quelle (`datenordner.json` oder `GLIDE_DATA_DIR`) in einem Systemdialog und beendet sich, ohne etwas anzulegen. Ein Zeiger mit Byte-Order-Mark ist wieder gültig. [Datenvertrag](docs/06_DATA_BACKUP_MIGRATION.md#ablage).
- **Suche:** Zerlegt gespeicherte Umlaute und Akzente (NFD, etwa aus macOS-Dateinamen) werden gefunden und an der richtigen Stelle markiert.
- **Neuerungskarte:** Einträge für 3.61.0 und die sichtbaren Änderungen von 3.60.0; der Eintrag zu 3.55.0 verspricht keine Überlastungsgründe mehr.
- **Design Richtlinien:** neu geordnet mit Grundsätzen P1–P6, den sechs verbindlichen Lehren aus der Marktanalyse (D83) und einem Gestaltungsregister aller gestaltungsrelevanten Entscheidungen, Fachentscheidungen und Inhaberzitate.
- **Dokumentation:** Übergabe auf den aktuellen Stand gekürzt, Arbeitsvorrat im Entwicklungsplan, Marktbericht §16 mit den Bewegungen bis 14.11.2026, Prüfplan und Faktenkorrekturen aus der Dokumentationsprüfung; dieses CHANGELOG auf sieben ausführliche Versionen gekürzt.
- Glide-System V1.24; Datenformat 26 unverändert. Prüfumfang und Grenzen im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3610-14112026).

## Dokumentationspflege – 14.11.2026

- **Tagesbilanz:** Das [Handbuch](docs/20_FUNKTIONEN.md#tageskapazität-und-entlastung-seit-3550) beschreibt die tatsächliche Anzeige. Die mit 3.55.0 angekündigten Überlastungsgründe werden berechnet, aber noch nicht angezeigt; der Eintrag zu 3.55.0 bleibt als Verlauf stehen.
- **WA-49:** 3.55.0 brachte den ersten Schnitt, die Tk-freie Pfadauflösung. Erst seit 3.60.0 legt der Import keine Ordner mehr an; Menüaufschub und Zeigerlesen beim Import bleiben offen.
- **Datenordnerzeiger:** Der [Datenvertrag](docs/06_DATA_BACKUP_MIGRATION.md#ablage) nennt das Verhalten bei unerreichbarem Ziel und bei BOM als offenen Befund.
- **Prüfstand 3.55.0:** Nachtrag zu Version, Laufzeit und Quellhash der Messdateien im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3550-11112026).
- **Markt, Plan, Übergabe, Index:** Featurematrix auf 3.60.0 ergänzt und eine verschobene Tabellenzeile repariert. Planeinstieg, Statusverweise, Register WA-12/WA-49 und Risiko R1 auf den Code ausgerichtet. Befunde in der [Analyse §13.36](../../00_Arbeitsvorbereitung/Glide_Analyse.md#1336-gesamtaudit-gegen-code-und-dokumentation-14112026), Rest im [Plan §21.91](../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2191-dokumentationskorrekturen-aus-dem-gesamtaudit-14112026).
- App 3.60.0, Datenformat 26 und Glide-System V1.23.1 unverändert.

## 3.60.0 – 13.11.2026

- **Marke und Projektseite:** Neues Glide-App-Symbol und zweifarbiges In-App-Logo. Die Fläche folgt der Themenfarbe, der Schatten bleibt eigenständig sichtbar. Der Showcase „Werkhaus West“ liefert einen bearbeitbaren Projektstand und 15 verschiedene Windows-Aufnahmen.
- **Showcase auf Linux:** Dieselben vier Studio-Motive liegen in den Demo-Sicherungen und Vorlagen als PNG vor. Galerie und Seitenbilder laden auch ohne externen JPEG-Decoder.
- **Seitenleiste:** Bei mehreren angehefteten Seiten passt Glide die Baumhöhen nach dem Layout an. Der Bereich „Zeichnungen“ bleibt dadurch auch bei eingeschränkter Fensterhöhe erreichbar.

- **Einstellungen mit „Kreativ“ in kleiner Schrift:** Der Einstellungsdialog öffnet auch mit DM Serif Display und der Schriftgröße „klein“ sofort. Vorher kreisten Umbruch und Spaltenbreite vor dem ersten Anzeigen endlos über drei Werte (gemessen unter macOS mit Tk 9.0.3). Die Tk-freie Regel `ui_design.settled_wrap_width` beendet die Runde bei einer wiederkehrenden Breite; das Ergebnis der übrigen Schriftkombinationen ist unverändert.
- **Fensterlage beim Start:** Die Lageregel der Normalansicht rechnet Tk-frei in `compact_mode.keep_visible`; `ListApp.clamp_geometry` bleibt die Fassade. Verhalten unverändert.
- **Import ohne Ordneranlage (WA-49):** Der Import von `app.pyw` legt auch mit `GLIDE_DATA_DIR` keine Ordner mehr an; das übernimmt der App-Start.
- **Prüfungen:** `test_startwege.py` hält als Teil von `SUITEN` Direktstart, Schnellstart und nachgestellten Paketstarter gegen vier künstliche Ablagen fest. `test_runtime_config.py` hält die drei Auflösungen des Bytecode-Ordners gleich. `test_arbeitsmodi.py` berücksichtigt zwei Eigenschaften von Tk 9.0 unter macOS.
- Glide-System V1.23.1; Datenformat 26 unverändert. Prüfumfang und Grenzen im [QA-Bericht](docs/07_QA_BERICHT.md#technische-vollprüfung-3600-auf-pc02-14112026).

## Dokumentationspflege – 13.11.2026

- Contributing-Einstieg und README-Navigation für Mitarbeit, Roadmap, Funktionen, Architektur, Entwicklungsablauf und Qualität ergänzt.
- Führende Dokumente und Änderungsfolgen in der [Pflegematrix](docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) zusammengeführt; Arbeitsregeln, Einstiege und Fachquellen darauf ausgerichtet.
- Shell-Konzept auf Zielarchitektur konzentriert, doppelte Modulaufzählungen ins bestehende Systemregister zurückgeführt und geplante Schnittstellen von vorhandenen Bausteinen abgegrenzt; Beschreibung von `RedoHistory` und den verbleibenden App-Kopplungen berichtigt.
- Glide-Systemkatalog als Dokumentationskorrektur auf V1.17.3 fortgeschrieben; App 3.55.1 und Datenformat 26 unverändert. Prüfumfang und Grenzen im [Nachweis](https://github.com/n05a-design/glide-to-do/blob/1fbf6a774fc75a7bc910926c76ef362c184d8d50/01_Repository/Glide/tests/qa-3.55.1/dokumentation_2026-11-13/README.md).

## 3.55.1 – 12.11.2026

- **Windows-Paketstart (lokaler Nachlauf, 13.11.2026):** Der Paketstart beschränkt den DLL-Suchpfad auf Anwendung, Paket und Windows-Systemverzeichnis. Die native Startprobe löst Pfadumleitungen vor dem Vergleich auf. Ein regulärer Paketneubau mit diesem Startskript steht aus.

- **Dateinamen unter macOS:** Die Speicherdialoge für JSON Canvas und App-Sicherung schlagen den Namen mit einfacher Dateiendung vor. Bestehende Sicherungen bleiben lesbar.

- **JSON-Canvas-Export:** Die aktive Pinnwand liefert ihre sichtbaren Karten, Positionen und Verbindungen. Der Export schreibt eine nutzbare Datei und zeigt die Formatgrenzen im Verlustbericht. Der Dateidialog und der Schutz der internen Daten sind über den App-Einstieg geprüft.

- **Tag entlasten:** Zielwahl und Rückmeldung stehen im festen Dialogfuß. Glide zeigt die Bilanz automatisch nach der Zielwahl. „Umplanen“ ist erst bei einer wirksamen Auswahl verfügbar. Fälligkeiten und gemeinsames Rückgängig bleiben erhalten.

## 3.55.0 – 11.11.2026

- **Neuerungskarte:** Die Startseite zeigt nach dem Update „Neu in Glide 3.55.0“ mit der Tagesbilanz und dem Fälligkeitserhalt. Nach „Gelesen“ bleibt der Eintrag unter Hilfe › Über Glide › Neuerungen verfügbar.

- **Tagesplanung & Kapazität (WA-12 / D57):** Transparente und handlungsorientierte Kapazitätsübersicht im Tagesentlastungs- und Planungsbereich (`planning.py`, `day_relief.py`, `app.pyw`). Exakte Berechnung von geplantem Aufgabenaufwand, belegter Kalenderzeit und verfügbarer Netto-Kapazität. Ungeschätzte Aufgaben werden transparent gesondert ausgewiesen und niemals heimlich als 0 Minuten gewertet. Konkrete Überlastungsgründe werden benannt. Im Entlastungsdialog wird die Fälligkeit von Aufgaben explizit als erhalten ausgewiesen (`Fälligkeit (bleibt)`), unterstützt von dynamischer Spaltenbreitenanpassung und atomarem Undo.
- **Architekturentkopplung & Initialisierung (WA-49):** Das Tk-freie Modul [`runtime_config.py`](src/glide/runtime_config.py) löst die Anwendungs-, Cache- und Logpfade auf. Die Pfadauflösung legt keine Verzeichnisse an. Windows verwendet für bestehende Daten weiterhin `%APPDATA%/Glide` und für den Cache standardmäßig `%LOCALAPPDATA%/Glide/Cache`.
- **Glide Shell Framework Vorbereitung:** Ausarbeitung des umfassenden Architektur- und Entkopplungskonzepts in [`docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) mit klarer Abgrenzung zwischen wiederverwendbarem Desktop-Fundament (Lifecycle, Window-Manager, Appearance, Widgets, Modal-Runner) und Glide-spezifischer Domäne sowie Entkopplung über Ports & Adapters.
- **System- und Testpflege:** Glide-Systemkatalog auf `V1.17` fortgeschrieben (`M095` `runtime_config.py`, `T313` `test_day_capacity.py`, `T314` `test_runtime_config.py`), 95 Quell- und 314 Testdateien, CI-Grundstufe 19/19 grün, Aufgabenformat 26 unverändert beibehalten.

## 3.54.0 – 10.11.2026

- Vollständige Fundortübersicht („Fundorte anzeigen …“, WA-21): listet für jede Aufgabe, Seite, Notiz, Liste und Zeichnung alle Verwendungen im Bestand auf (Heimatcontainer, Objektverweise, Textlinks, Aufgabenzeilen in Seiten/Notizen, Live-Listen, Aufgabenbeziehungen, Pinnwandkarten/-verbindungen und unverknüpfte Titelerwähnungen) samt Zielzustand, Öffnen im Haupt- oder Nebenbereich und direktem Verknüpfen unverknüpfter Erwähnungen.
- Pinnwand-Export als JSON Canvas 1.0 (`.canvas`, WA-07 / FP-07 Stufe 2): exportiert Bereiche als `group`-Knoten, Aufgaben-, Seiten-, Notiz- und Zeichnungskarten als `text`-Knoten mit stabilen Kennungen, Koordinaten, Maßen und Farben sowie Verbindungen als `edges`, begleitet von einem ausdrücklichen Verlustbericht über nicht abbildbare Glide-Metadaten.
- Klassischen Tk-Restbestand vollständig abgelöst (`Sperrklinke = 0`, UI-Feinschliff §21.76): alle 28 `Checkbutton`-, 2 `Radiobutton`-, 4 `Listbox`- und 1 `Scale`-Instanzen durch themengerechte Eigenzeichnungen (`GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`) ersetzt und in `altbestandteile.py` dauerhaft gesperrt.

## 3.53.0 – 10.11.2026

- Schrift- und Symbolprüfungen erweitert: alle vier auswählbaren Schriftfamilien werden mit sämtlichen UI-Symbolen in normalem und fettem Tk-Gewicht auf die tatsächlich verwendete Glyphenfamilie geprüft.
- `symbolpruefung.py` untersucht die vier Schriftstile statt nur der aktuell gewählten Familie; die lokale QA-Zuordnung benennt direkte Tests, indirekte Geometrieprüfungen sowie native und menschliche Abnahmegrenzen.
- Versionswechsel von 3.52.0 auf 3.53.0. Die plattformübergreifende Vollmatrix und menschliche Abnahme sind weiterhin Freigabetore.

## Frühere Versionen (verdichtet)

Vollständig beschrieben sind die sieben neuesten Versionen; ältere stehen verdichtet in der Tabelle darunter. Ihre ausführlichen Einträge, Verträge und Nachweise trägt Git (3.33.13–3.33.16 im Commit `6098877`, ältere im Stand vor dem 03.10.2026). Das aktuelle Verhalten beschreiben die [Funktionen](docs/20_FUNKTIONEN.md).

Datenformate und ihre Felder: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md#formatstufen).

| Version | Datum | Kern |
|---|---|---|
| 3.52.0 | 10.11.2026 | Vier Schriftstile (Rubik, DM Mono, DM Serif Display, Charis SIL), Schriftgewicht unabhängig von der Größe, Kopflogo und Akzente in der Themenfarbe. |
| 3.51.0 | 09.11.2026 | Die vier Plus-Knöpfe in der Seitenleiste erscheinen im Ruhezustand ohne Kontur. |
| 3.50.7 | 08.11.2026 | Produktkommunikation, MPL-2.0 und Validierung |
| 3.50.6 | 07.11.2026 | Menschliche Abnahme am Mac (D66–D71) |
| 3.50.5 | 05.11.2026 | Abnahmekorrekturen und Suchfelder |
| 3.50.4 | 05.11.2026 | Neuer Stand für die fortgesetzte menschliche Abnahme |
| 3.50.3 | 05.11.2026 | Korrekturen aus der menschlichen Abnahme |
| 3.50.2 | 03.11.2026 | Versions- und Ablageabgleich |
| 3.50.1 | 03.11.2026 | Themenflächen und lesbarere Schriftstile |
| 3.50.0 | 02.11.2026 | Erster öffentlicher Stand |
| 3.49.0 | 28.10.2026 | Tagesplanung, Verweise und geschützter Wiederanlauf |
| 3.48.0 | 27.10.2026 | Tagesnavigation, Mehrfachfelder und Verweise |
| 3.47.0 | 27.10.2026 | Mehrfachplanung und Nebenansichtsverlauf |
| 3.46.0 | 27.10.2026 | Tagessteuerung und Nachschlagen |
| 3.45.0 | 25.10.2026 | Sicherungsübersicht, Arbeitsmodi und Speicherstatus |
| 3.44.0 | 22.10.2026 | Wiederholen, eigene Rhythmen, Ansichten, Seitenkarten, Erwähnungen, KI-Aufträge und Markdown-Export |
| 3.43.1 | 16.10.2026 | Kürzel in Listen unter Linux/Tk 9.1 |
| 3.43.0 | 16.10.2026 | UI-/UX-Paket aus Nutzerbeobachtungen |
| 4.0.0 (Vorbereitung, keine Lieferung) | ab 15.10.2026 | Barrierefreiheit: eigene Tk-9.1-Laufzeit mit Patches, Reader- und Zustandsgegenproben; Stand im Entwicklungsplan (Paket 8) |
| 3.42.0 | 13.10.2026 | Eigenständige Entwicklungspakete |
| 3.41.0 | 13.10.2026 | Notion-Import und Seitenwiederherstellung |
| 3.40.0 | 13.10.2026 | Pixelanimation |
| 3.39.1 | 13.10.2026 | Wiederholungen richtig erfassen und austauschen |
| 3.39.0 | 12.10.2026 | Tagesplanung mit belegter Zeit |
| 3.38.0 | 11.10.2026 | Aufgaben unmittelbar bearbeiten |
| 3.37.0 | 10.10.2026 | Logo und Symbole |
| 3.36.0 | 10.10.2026 | Fundament und Tempo |
| 3.35.0 | 09.10.2026 | Pixel und Austausch |
| 3.34.0 | 09.10.2026 | Wissen und Seiten |
| 3.33.21 | 09.10.2026 | Ruhige Oberfläche |
| 3.33.20 | 09.10.2026 | Komfort im Alltag |
| 3.33.19 | 09.10.2026 | Tempo |
| 3.33.18 | 08.10.2026 | Seiten im Alltag (G28/G09/U08): Live-Listen zeigen Originalaufgaben samt Unteraufgaben direkt in Seiten. |
| 3.33.17 | 07.10.2026 | Wissen und Woche: eingebetteter Kalender, Kapazität/Zeitfenster, lokale Objektverweise und Rückverweise; Format 22 |
| 3.33.16 | 07.10.2026 | Bedienkomfort: eine Palette für Inhalte und Aktionen, höchstens vier Kopfknöpfe, einklappbare Hinweise, Bibliothekswege, Bearbeitungstag in der Datumsspalte, eindeutige Symbole (U01/U02/U13/U14/U16/U22/U24) |
| 3.33.15 | 07.10.2026 | Aufgaben im Wissen: echte Aufgaben im Notiztext, Übernahme in Listen mit erhaltenen IDs, „Aus Seiten“ (G29/G31/G32); Format 21 |
| 3.33.14 | 07.10.2026 | Tagesvorschlag „Was passt heute?“, geführter Tagesbeginn, Zeitblöcke per Tastatur, Fokus mit genau einmal gebuchter Zeit (AU01/AU03/H-02/G05) |
| 3.33.13 | 07.10.2026 | Gemeinsames Menü „Einplanen“ und verfügbare Zeit in allen Planungswegen (KO01/AU02, `planning.py`) |
| 3.33.12 | 06.10.2026 | Titel vor Kennzahlen, Herkunft rechts in Heute (U10/U19), erste Gestaltungsskala (OB01); ausführlicher Stand in Git |
| 3.33.11 | 06.10.2026 | Gezielter Speichervergleich (P08b), stabile Aktionskennungen, U03/U07; ausführlicher Stand in Git |
| 3.33.10 | 06.10.2026 | Kennzahlen und Messwerte je Aufbau wiederverwenden (P09b); ausführlicher Stand in Git |
| 3.33.9 | 05.10.2026 | Gemeinsamer Speichervergleich (P08a); ausführlicher Stand in Git |
| – | 05.10.2026 | Windows-Prüfung und Befunde festgehalten, App unverändert; ausführlicher Stand in Git |
| 3.33.8 | 05.10.2026 | Windows-Layout, Prüflaufzeit, Formatsicherung mit Inhaltsvergleich; ausführlicher Stand in Git |
| 3.33.7 | 05.10.2026 | Inhaltssuche in der Palette (G14 erste Stufe); ausführlicher Stand in Git |
| – | 03.10.2026 | Aufräumen der Ablage, App unverändert; ausführlicher Stand in Git |
| 3.33.6 | 02.10.2026 | Heute/Demnächst und Tagesmodi (D14); ursprüngliche Mac-Abnahme im festen Git-Stand |
| 3.33.5 | 02.10.2026 | Eisenhower-Gruppierung mit erhaltener Fälligkeit (D13); ausführlicher Stand in Git |
| 3.33.4 | 02.10.2026 | Wiederholungen in der Schnelleingabe mit erstem Termin und Feldchip; ausführlicher Stand in Git |
| 3.33.3 | 02.10.2026 | Deutsche Schnelleingabe mit Feldchips (G01, D10); ausführlicher Stand in Git |
| 3.33.2 | 02.10.2026 | Startseite Ruhig und beschleunigter Aufbau; ausführlicher Stand in Git |
| 3.33.1 | 01.10.2026 | Vier Seitenleistenbereiche, Fensterbedienung, Logo und Schaltflächen nachgezogen; ausführlicher Stand in Git |
| 3.33.0 | 01.10.2026 | Tk-freies Fundament: gemeinsame Formatsicherung, Bereichsregeln, SVG-Geometrie und Startseitenkacheln |
| 3.32.3 | 01.10.2026 | Bibliothek und Aktionsleiste behalten unveränderte Karten (Refresh bei 1.000 Aufgaben 776 → 5 ms); aktiver Showcase „Parkquartier“; Beschlüsse D09–D17 |
| 3.32.2 | 30.09.2026 | Drag-and-drop in allen Seitenleistenbereichen (D04); Schriftwerte je Tk-Interpreter zwischengespeichert |
| 3.32.1 | 30.09.2026 | Klappzustände von Labelgruppen, Fächern und Bereichen bleiben erhalten; Klapppfeile per Tastatur; D01–D06 übernommen |
| 3.32.0 | 30.09.2026 | ICO-Export, Aseprite-/ASE-Paletten, selbstfüllende Platzhalter, Tagesabschluss; Hänger bei Menübefehlen und Bildseiten behoben; Pflegewerkzeuge |
| 3.31.0 | 30.09.2026 | Rückmeldungen R1–R11: Menüdialoge öffnen wieder, Editor mit Blockaktionen, Farben nach Bedeutung, schnellere Übersicht |
| 3.30.0 | 25.–29.09.2026 | Modernisierung: Pixel-Werkstatt, Startseite zum Anpassen, Pinnwand als Board, Notizbuch, Seiten mit Bildern, Galerien, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen, zehn Designs, Logo; **Format 20** |
| 3.29.0 | 24.09.2026 | Zeichnung als eigene Listenart mit Referenzbild; **Format 19** |
| 3.28.0 | 23.09.2026 | Ordnertypen und Tagebuch (später Notizbuch); **Format 18** |
| 3.26.0 | 21.09.2026 | Notizen als Listenart, Begleiter Gismo, Lizenzentwurf; **Format 17** |
| 3.25.0 | 19.09.2026 | „Form follows function“: Übersicht und Hierarchie, Startseite mit Kacheln und gezeichneter Figur |
| 3.24.0 | 19.09.2026 | Kürzere Navigation; Pinnwand mit Mehrfachauswahl und gerichteten Verbindungen |
| 3.23.0 | 18.09.2026 | Zusammenhalt vorhandener Funktionen (46 Punkte) |
| 3.22.0 | 17.09.2026 | Checkliste je Aufgabe; **Format 16** |
| 3.21.0–3.21.4 | 14.09.2026 | Kalenderimport aus ICS, Serienende ohne UTC-Versatz, Beispielbestand testbar, Standprüfung |
| 3.20.0 | 14.09.2026 | Kalenderausgabe als ICS |
| 3.19.0 | 13.09.2026 | Dauerhafter Änderungsverlauf; **Format 15** |
| 3.18.0 | 13.09.2026 | CSV-Import mit Spaltenzuordnung |
| 3.17.0 | 13.09.2026 | Druck- und PDF-Ausgabe |
| 3.16.0 | 13.09.2026 | Vollständiges App-Backup (`.glideapp`) |
| 3.15.0 | 13.09.2026 | Tagesplanung und Tageskapazität |
| 3.14.0 | 13.09.2026 | Bearbeitungstag und geschätzter Aufwand; **Format 14** |
| 3.13.0 | 13.09.2026 | Tabellenansicht |
| 3.12.0 | 13.09.2026 | „Mein Tag“ (seit 3.33.6 „Heute“) |
| 3.11.0 | 13.09.2026 | Schnellerfassung und gespeicherte Filter |
| 3.10.0 | 13.09.2026 | Reiter und Pinnwand |
| 3.9.0 | 12.09.2026 | Einheitliche Oberfläche, Einstellungen, Hell/Dunkel |
| 3.8.0 | 12.09.2026 | Lokale Erinnerungen, Aufmerksamkeit in Taskleiste und Dock; **Format 13** |
| 3.7.0 | 07.–12.09.2026 | Kompakte Kacheln, Anhänge an Listen und Ordnern, dynamische Übersicht; **Format 12** |
| 3.6.0 | 06.09.2026 | Kachelübersicht der Listen, Jahresanzeige |
| 3.5.0 | 05.09.2026 | Wiederkehrende Aufgaben; **Format 11** |
| 3.4.0 | 05.09.2026 | Startseite neu: Uhr, Tagesziel, Schnellzugriffe, Bestand, Listenfarben |
| 3.3.0 | 04.09.2026 | Ansicht „Labels“ |
| 3.2.0 | 04.09.2026 | Keine Übernahme aus Altordnern; zentrale Textzeichen |
| 3.1.0 | 04.09.2026 | Aufräumversion ohne neue Funktion |
| 3.0.0–3.0.2 | 03.09.2026 | Neue Oberfläche (Inhalt nach oben, kein Schwarz im Hellmodus); Gruppen benutzbar, Mehrmonitor-Dialoge |
| 2.12.0 | 03.09.2026 | Ruhigere Eingabemaske |
| 2.11.0 | 03.09.2026 | Papierkorb auch für Punkte, Mehrfachauswahl, Uhrzeit; **Format 10** |
| 2.10.0 | 03.09.2026 | Label-Chips, verlustfreier TXT-Rundlauf |
| 2.9.0 | 03.09.2026 | Verschachtelte Ordner, Long-Task-Details |
| 2.8.0 | 02.09.2026 | Verspätet, Long-Task, Zwischenüberschrift, Anlage-Dialog |
| 2.7.0–2.7.2 | 02.09.2026 | Papierkorb für Listen und Ordner, Labels; **Format 7** |
| 2.6.0 | 01.09.2026 | Gruppen; **Format 6** |
| 2.5.1–2.5.5 | 31.08.–02.09.2026 | Ordneransicht, fester Eingang, Kontextmenü, „In Bearbeitung“, Anhangspfade; **Format 5** |
| 2.5.0, 2.4.1 | vor 31.08.2026 | Zwischenstand und Ausgangsstand |
