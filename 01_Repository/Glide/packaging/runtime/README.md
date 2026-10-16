# Eigene Tcl/Tk-9.1-Runtime

Stand 16.10.2026 · Glide 3.43.1 · Vorbereitung von Paket 8 / 4.0.0, keine Lieferung

`baue_runtime.py` exportiert saubere Git-Originale aus den Pins in `runtime_contract.py` und baut Tcl, Tk und die dazu passende CPython-3.14-Erweiterung `_tkinter` in einem neuen Ziel außerhalb von OneDrive. Installierte Python-Header und Quellheader müssen bytegleich sein. Native Ziele: macOS arm64, Windows x64 mit MSVC, Linux x64 mit verpflichtendem ATK/AT-SPI. Es gibt keine Systeminstallation.

`runtime_patches.py` wendet ausschließlich die in `patches.json` dokumentierten Korrekturen auf die exportierte Baukopie an. Quellpin, Originalbytes, Diffbytes und Ergebnisbytes müssen passen. Originalquellen bleiben unverändert. Die Mac-Korrektur betrifft bestätigte native Verträge bei Aktionswarteschlange, deaktivierten Inhalten, Fokus, Verfügbarkeit, Kennungen, Hilfe und Aufgabengruppen. Jede vorgemerkte Aktion besitzt Interpreter und Kommandodaten; entfernte, versteckte, deaktivierte oder ersetzte Ziele werden verworfen. Interpreterlöschung entfernt ausstehende Aktionen.

`hole_runtimequellen.py` lädt die offiziellen festen Git-Pins ausschließlich in ein neues Hosted-CI-Ziel unter `RUNNER_TEMP`. Der vorhandene Workflow `Glide-Prüfung` mit manuellem Bereich `zugang400` baut Linux und anschließend Windows; Linux prüft die reale externe AT-SPI-Textschnittstelle, Windows den Aufgaben-Kernablauf und danach tatsächliche NVDA-Sprache mit isoliertem Profil. Die nativen Vollprüfungen je Lieferung bleiben zusätzlich erforderlich.

Mac-Runtime4: zwölf native Anbieterfälle, vier installierte Tcl-Fälle, zehn GUI-Gruppen und isolierter privater Paket-Kernablauf grün. Neunter Linux-Lauf: Unicode/Caret, ACTIVE und deaktivierte Zustände sowie Tcl/GUI grün. Orca spricht Erfassung/Suche, meldet beim Wechsel jedoch fälschlich fokussierte Container; vollständiger Ablauf offen. Windows-Signaturgegenprobe und isolierter Paketprozess/Kernablauf im neunten Lauf grün; Gesamtnachweis wegen zweier abweichend restaurierter geschützter CI-Dateien rot. NVDA erreicht Heute, danach unknown; vollständiger Ablauf offen. [Nachweise und rote Vorläufe](../../tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md).

| Patch | Zweck |
|---|---|
| macos-accessibility-core | Native Aqua-Verträge für Namen/Werte, Kennungen, Hilfe, Fokus, Zustände und abgesicherte Aktionslebensdauer |
| common-accessibility-selection | Frühe Auswahl vor Map, entfernte Widgets und Bäume ohne Zusatzspalten ohne Tcl-Callbackfehler |
| linux-accessibility-text | Aktueller Text, Unicode-Zeichenoffsets, Zeichenzahl und Caret über AtkText |
| linux-accessibility-window | ACTIVE am gemappten Fenster mit tatsächlichem Tk-Eingabefokus |
| linux-accessibility-state | ENABLED/SENSITIVE/EDITABLE aus disabled/readonly; deaktivierter Text bleibt lesbar |
| linux-accessibility-focus | Virtuelle Vorfahrenereignisse sind kein Eingabefokus; Fokuswechsel sind keine neuen Kinder. Nach Orca-Befund vorbereitet, native Wiederholung offen |
| linux-accessibility-lifetime | Typgerechte native Callbackdaten, GObject-Referenzlebensdauer und DEFUNCT nach tatsächlichem SIG11; externer Lebensdauertest offen |
| windows-accessibility-name | get_accName liest den Namen; Beschreibung bleibt separat |
| windows-accessibility-identity | Stabile MSAA-Kindkennungen, Widget-/Root-Lebensdauer und gültige Fokus-Tabelle nach NVDA-unknown; COM-Gegenprobe offen |

Mac baut mit `--disable-framework --disable-zipfs --enable-aqua=yes`: getrennte Tcl-/Tk-Skriptdaten vermeiden den belegten PyInstaller-/Mach-O-Konflikt angehängter Archive. Windows erhält `manifest.uuid` aus Originalpräfix und verifiziertem Pin. `_tkinter` verwendet `TCL_WITH_EXTERNAL_TOMMATH` und `tommath.lib`; Tcl/Tk, zlib und TomMath liegen neben der eigenen pyd. Linux benötigt HarfBuzz sowie ATK/Bridge/X11.

Patchprozesse erzwingen LF lokal und verändern keine globale Git-Konfiguration. Elf Runtimeverträge samt tatsächlichem Git-Gegenfall sind grün. Plattformgemeinsame Patches gehören zur verpflichtenden Runtimeherkunft. `baue_paket.py --runtime-bau <runtime-bau.json>` verlangt Interpreter, Pins, Patchsatz und vollständige unveränderte Runtime-Dateihashes. Lizenzwerkzeuge verwenden Originalbelege einschließlich utf8proc; Reader-Testhelfer werden niemals mitpaketiert.

Standard-Vollmatrix und Windows-Paketjob sind auf eigene 9.1-Runtimes vorbereitet, Python-Pins Linux 3.14.8 / Windows 3.14.7. `pruefen.py` enthält 91 Integrationssuiten. `--zugang-nativ` erzwingt die native Kernprüfung in der Vorstufe; ab Version 4 ist sie ohne Option Pflicht. Native Tcl-Bindungen gehören dazu. Linux-Defektgegenproben bleiben erhalten. Gezielter Mac-Hintergrundpfad und drei Versionsvertragsfälle grün; finale eingefrorene Vollmatrix offen.

Vollständige tatsächliche VoiceOver-/NVDA-/Orca-Abläufe bleiben nach D36 Pflichtnachweise. Attribute, künstlich gesetzter Readerstatus im eigenen Tcl-Interpreter und direkte Tk-/spd-say-Ausgabe zählen dafür nicht. Menschen-/DPI-Abnahme nach D42 bleibt zusätzlich getrennt. Prototypen weiter Basisversion 3.42.0; Mac Ad-hoc-signiert, Windows unsigniert. Keine 4.0-Lieferung oder öffentliche Signaturfreigabe.

Aktuellster Nachlauf: [Native10](../../tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/native_vorlauf10.json), exklusiver Linux-Fokus grün, danach Orca-SIG11; Linux-Lebensdauer und native Probe vorbereitet. NVDA-Heute-Fokus repariert, weitere Readernavigation/MSAA-Prüfer und Reparse-ACL korrigiert; Native11 offen. Kein4.0-Liefernachweis.
