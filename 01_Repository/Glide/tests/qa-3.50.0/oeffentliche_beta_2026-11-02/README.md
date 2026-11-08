# Glide 3.50.0 – Erster öffentlicher Stand

Stand 02.11.2026 · öffentliche erste Beta · Aufgabenformat 26 · Einstellungen 2

Endstand Programm/Tests `b2b54e7`, App-SHA-256 `2fb07ca2f6d8d119639df56511e3313e0ac94564af66ad81a2c8284899a0403b` (App unverändert seit `b0fd56a`). Danach nur Dokumentations- und Nachweisnachlauf; frühere grüne Läufe gelten ausschließlich ihren ursprünglichen Eingaben.

## Prüfstand

| Bereich | Tatsächlicher Stand |
|---|---|
| Grundstufe | [19 Schritte grün](grundstufe.json): 238 Werkzeugtests (drei Skips), zweimal 1.112 Fachtests (je ein Skip), fünf Analysen, Startprobe, Fremdcode-, Datenschutz-, Versions-/Link- und strenger Python-Lieferabgleich |
| Neue Oberfläche | [Beta350-Bedienung](beta350_bedienung.json): zehn Designs und zehn Hintergrundoptionen, Kontrast, Speichern/Neustart, drei Größen, volle Seitenleiste, echtes Blockziehen mit Undo/Redo/Escape und Schreibschutz |
| Frischer Appstart | [Gegenfall rot](startschrift_rot.json), [Korrektur grün](startschrift_gruen.json): echter `main()`-Start mit mitgelieferter DejaVu Sans, unveränderten Standardsymbolen und vollständig sichtbaren Systemzählern; gehört als eigener Frischprozess zur Logosuite |
| Mac-Vollmatrix | MacBook M2, eigene Tcl/Tk 9.1.0: [125 von 127 Schritten grün](voll_macos.json) auf dem Endstand, alle 108 Integrationssuiten; zwei ausdrücklich übersprungene Tore: Plattformaufnahmen (nur Linux/X11) und menschliche Sichtprüfung |
| Linux-Vollmatrix | [GitHub-Lauf 41438822957](https://github.com/n05a-design/glide-to-do/actions/runs/41438822957) auf `b2b54e7`: Grundstufe und Vollprüfung Linux/Xvfb mit eigener Tk 9.1 grün |
| Windows-Vollmatrix | Derselbe Lauf: Vollprüfung Windows x64 mit eigener Tk 9.1 und nativer Zugangsprüfung grün, anschließend eigenständiges Paket gebaut und isoliert gestartet |
| Native Mac-Kern-/Paketprobe | [Zehn native Kerngruppen](p8_macos.json), [zwölf Getter-/Aktionsproben](native_getter_macos.json) und [Start der gelieferten App](mac_start_lieferung.json) grün; externes Python und ungebündelte Quellen im Paketprozess gesperrt |

[941 versionierte nicht-Markdown-Prüfeingaben des Mac-Laufs](matrix_eingaben.json) stimmen mit dem ausgecheckten Commit `b2b54e7` überein (Programm, Tests, Fixtures, Ressourcen, Bauwerkzeuge). Der anschließende Dokumentations-/Vorschaubildnachlauf wird separat geprüft. Alle 108 Integrationssuiten bleiben Teil der Vollprüfung. Die vorhandenen Funktionen bis 3.50 einschließlich Import/Export, Wiederholung, Fokus, Nebenansicht, Seiten-/Notizaufgaben, Pinnwänden, Bildern, Zeichnungen, Sicherungen, Schreibschutz, Mutationsfehlern und Wiederanlauf werden gemeinsam geprüft. Die menschliche Prüfung folgt anschließend; Screenreader ist bis Bedarf zurückgestellt.

## Umsetzung

- Hintergrundfarbe unabhängig vom Design: bestehende feste Palette, Designvorgabe und „Wie die Fensterfläche“. Letzteres verbindet helle bzw. dunkle Kartenfläche und Hintergrund ohne Materialschatten; Verläufe bleiben gespeichert. Eine neue Verlaufswahl schaltet die Flächenfarbe wieder auf Designvorgabe.
- Logo, Titel und Untertitel fluchten mit dem großen Inhaltsbereich. Breite und schmale Seitenleiste nutzen die volle Höhe; Ausblenden, Kompaktmodus und bestehende Abstände bleiben erhalten.
- Seitenblöcke am Sechspunktgriff ziehen: Zielmarke, Randscrollen, Escape-/Außerhalb-Abbruch, ein Undo/Redo; Formatierungen, Unicode, Links, Bilder und Aufgabenkennungen bleiben erhalten. Tabellen, Code und eingerückte Kindzeilen bleiben zusammen. Rechtsklick und Tastatur öffnen weiter die Formataktionen. Unzulässige Formatgrenzen verändern weder Dokument noch Undo oder gespeicherte Bytes.
- README und GitHub-Kurzbeschreibung als Einstieg für Interessenten, echte Paketvorschau mit künstlichen Daten, vollständige Featureübersicht bis 3.50, Pflegepflicht in der Dokumentenpflege. Kein Altbestandswarntext im Einstieg und kein wertender CodeQL-Absatz.
- Sicherheitsrichtlinien und Git-Regeln aktualisiert; Actions auf vollständige Commit-SHA, Bauabhängigkeiten auf Originalversionen und erzwungene PyPI-Hashes festgelegt. Die aktive serverseitige Analysekonfiguration bleibt separat; aus einer Workflowdatei allein wird keine Analyseabdeckung behauptet.
- Kein Formatwechsel für diese drei Funktionen: `background_color` ist eine Einstellung, Blockreihenfolge bleibt die bestehende Text-/Spanstruktur. Anforderungen an die nächste Formatstufe stehen im [Datenvertrag](../../../docs/06_DATA_BACKUP_MIGRATION.md#vorbereitung-der-nächsten-aufgabenformatstufe).

[Blockmessung](blockmessung.json), [ausführbares Messskript](blockmessung.py): 100 bis 10.000 Zeilen bzw. Spans, Format-/Linkerhalt; bei 10.000 Zeilen Median etwa 23 ms. Gemessen wird ausschließlich die unveränderte Tk-freie Blockfunktion auf diesem Mac, kein appweiter Performanceabschluss.

## Pakete und Lieferung

Python-Fassung und Showcase tragen 3.50.0. `07_Python-Versionen` enthält 91 Code-Dateien und 147 Ressourcen/Vendor-Dateien; strenger Hashabgleich grün. Der Showcase wurde mit künstlichen Daten neu erzeugt, importiert, exportiert und nach Neustart geprüft; seine sechs gelieferten Dateien stimmen mit den Fixtures überein.

**macOS arm64:** [nativer Bau und kompilierter Quell-/Lizenznachweis](mac_bau.json), [isolierter Runnerstart](mac_start_runner.json), [Bauabschluss](mac_bauabschluss.json), [Liefer- und Quellabgleich](mac_lieferabgleich.json) (208 Quelldateien gegen den ausgecheckten Commit `b0fd56a`, App `2fb07ca2…`) und [isolierter Start der gelieferten App](mac_start_lieferung.json). Python 3.14.5, Tcl/Tk 9.1.0, 463 Dateien und 30 interne Symlinks. [Nativer Workflow](https://github.com/n05a-design/glide-to-do/actions/runs/41426907797).

- Aktive lokale App: `~/Applications/Glide.app`; `build/macos/Glide.app` verweist darauf. OneDrive ergänzt an Frameworkordnern wiederholt Finder-Metadaten, die eine strenge Signaturprüfung im Syncordner beanstanden kann. Deshalb liegt die native Installation außerhalb des Syncordners; die Signatur wird am aufgelösten Bundlepfad geprüft. Keine neue Signatur und keine veränderten Appbytes durch den Lieferweg.
- Weitergabe: `build/macos/Glide-3.50.0-macos-arm64.tar.gz`, SHA-256 `eca6548e82e0a47578df58892948d6439af35ef12a3f863b4bd62dda5262e200`. Das TAR unverändert weitergeben und nativ entpacken, damit Dateimodi und Verknüpfungen erhalten bleiben. Die lokale Verknüpfung ist kein plattformübergreifendes Paket.
- Vorherige 3.49-App und ihr TAR bleiben als Rückweg erhalten. Mac ist Ad-hoc-signiert; Developer ID und Notarisierung sind nicht vorhanden.

**Windows x64:** [nativer Bau mit Quell-/Lizenz-/Modulnachweis](win_bau.json), [PE-Nachprüfung](win_pe.json), [isolierter Start auf dem Runner](win_start_runner.json) ohne externes Python und [Lieferabgleich](win_lieferabgleich.json): 104 Paketdateien gleich dem Bauinventar, alle 92 kompilierten Module gleich `b2b54e7`. Python 3.14.7, Tcl/Tk 9.1.0, PyInstaller 6.22.3. [Workflow-Lauf](https://github.com/n05a-design/glide-to-do/actions/runs/41438822957).

- Geliefert: `build/windows/Glide-3.50.0/Glide.exe` (SHA-256 `c0716a54…`) und `build/windows/Glide-3.50.0-windows-x64.zip`, SHA-256 `48828f13b81059a273353aabc75095f31d49833c88a0b004427ece86eb5a306f`. Das ZIP enthält den Ordner `Glide-3.50.0`; vollständig entpacken und `Glide.exe` starten.
- Die 3.45-Fassung liegt als Rückweg unter `build/windows/Archiv/Glide-3.45.0`, ihr ZIP bleibt daneben. Windows-Pakete sind unsignierte Entwicklungsartefakte; SmartScreen kann beim ersten Start warnen.

Linux verwendet die Python-Fassung; ein eigenständiges Linux-Binärpaket ist nicht gewählt.

## Vorläufe und Prüfgrenzen

Die früheren roten Läufe bleiben lokal erhalten. Veraltete Layout-/Menüerwartungen wurden nach der ausdrücklich beauftragten UI-Änderung angepasst; die Aktionssuche erhielt die fehlende Farbgruppe. Fachliche Kriterien, Formatgrenzen und Schreibschutz wurden bewahrt.

Der [Fokus-Gegenfall](fokus_rot.json) reproduziert auf `557331e` den fehlenden Editorfokus beim Ziehen aus der Seitenleiste. Der Griff übernimmt seit `6e4cff5` den Textfokus; echte Escape-Ereignisse prüfen den Abbruch. Der vollständige Mac-Lauf auf `6e4cff5` war [125 Schritte grün](vorlauf6e/voll_macos.json), ebenso die [Linux-Matrix](vorlauf6e/voll_linux.json) und ihre [Defektgegenproben](vorlauf6e/linux_defektgegenproben.json). Die danach durch Sichtkontrolle gefundenen Schrift-/Zählerfehler sind im neuen Frischprozess vorher rot und nachher grün belegt. Diese alten Matrix-/Paketbelege unter `vorlauf6e` werden nicht als Endstand umetikettiert.

Die Windows-Vollprüfung fand nach den Mac-/Linux-Läufen drei weitere Stellen: „Hilfe“ in der eigenen Windows-Menüzeile bei Mindestgröße gestaucht (`fbd83e7`), der Seitentitel neben der durchgehenden Seitenleiste abgeschnitten (`5ffc732`) und in `test_arbeitsmodi` ein fehlender Fensterfokus, nachdem der neue Fall `beta350` mit Neustart vor `seitenaktionen` eingereiht war (`b0fd56a`). Korrigiert in `5ffc732` (schmalere Menüknöpfe), `b0fd56a` (Titel kürzt auf den freien Platz, Schnellerfassung weicht unter 640 px Kopfbreite ins Überlaufmenü) und `b2b54e7` (`beta350` zuletzt, synthetischer Klick aktiviert vorher das Fenster wie ein echter). Die beiden ersten Korrekturen ändern die App und sind im Mac-/Linux-Endlauf enthalten; die dritte betrifft nur die Prüfreihenfolge.

Nach dem Merge war der erste `main`-Lauf ([41454826947](https://github.com/n05a-design/glide-to-do/actions/runs/41454826947)) unter Windows in `test_fortsetzung33311` rot, auf identischem Baum wie der grüne Lauf zuvor. Ursache war der Test: Er ließ `write_json_atomic` pauschal scheitern. Fiel der Speicheraufruf auf einen Sekundenwechsel, erneuerte `refresh_data_lock` vorher `glide.lock` über dieselbe Funktion, sodass der Sperrausstieg statt des geprüften Schreibwegs griff. Mit fälliger Sperrerneuerung ist der Fehler gezielt rot reproduzierbar. Jetzt scheitert nur das Schreiben von `data.json`; das ist auch im erzwungenen Fall grün. Die App ist unverändert.

Menschliche Sicht-/Bedienprüfung, DPI und mehrere Monitore folgen mit den tatsächlich gelieferten Paketen anhand der [bestehenden Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md). Screenreader (VoiceOver/NVDA/Orca) gehört bis zu einem konkreten Bedarf nicht zur aktiven Restliste.

Historische WA-41A/B-Untersuchungen bleiben als Grenzen erhalten: systemweite Instabilität auf PC-02 und frühere Save/Reload-Differenz ohne gespeicherte Felddiagnose. Grüne Gegenläufe erklären ihre Ursache nicht; keine weitere Intel-Stressserie oder spekulative BIOS-/CPU-Änderung. Appweite WA-32/39/36-Vorhaben haben belegte Teilabschlüsse und werden durch diesen konkreten Stand nicht als vollständig umgebaut bezeichnet. Ungewählte Zukunftsfunktionen sind keine fehlenden 3.50-Implementierungen. Öffentliche Signatur/Notarisierung, Lizenz, Marke und weitere Vertriebskanäle bleiben gesonderte Entscheidungen.
