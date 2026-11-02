# Glide 3.50.0 – Erster öffentlicher Stand

Stand 02.11.2026 · öffentliche erste Beta · Aufgabenformat 26 · Einstellungen 2

Quellstand `fbd83e78d434e0c8fd03fc948ccf4f0e54971456`, App-SHA-256 `8b11c8cb70f83affefcb1f7819bbe02d552ba6c682360dccbcf01bead4eaa64f`. Dokumentations- und Nachweisnachlauf wird getrennt geführt; frühere grüne Läufe gelten ausschließlich ihren ursprünglichen Eingaben.

## Prüfstand

| Bereich | Tatsächlicher Stand |
|---|---|
| Grundstufe | [19 Schritte grün](grundstufe.json): 238 Werkzeugtests (drei Skips), zweimal 1.112 Fachtests (je ein Skip), fünf Analysen, Startprobe, Fremdcode-, Datenschutz-, Versions-/Link- und strenger Python-Lieferabgleich |
| Neue Oberfläche | [Beta350-Bedienung](beta350_bedienung.json): zehn Designs und zehn Hintergrundoptionen, Kontrast, Speichern/Neustart, drei Größen, volle Seitenleiste, echtes Blockziehen mit Undo/Redo/Escape und Schreibschutz |
| Frischer Appstart | [Gegenfall rot](startschrift_rot.json), [Korrektur grün](startschrift_gruen.json): echter `main()`-Start mit mitgelieferter DejaVu Sans, unveränderten Standardsymbolen und vollständig sichtbaren Systemzählern; gehört als eigener Frischprozess zur Logosuite |
| Mac-Vollmatrix | [125 Schritte grün](voll_macos.json), alle 108 Integrationssuiten; zwei ausdrücklich übersprungene Tore: Plattformaufnahmen und menschliche Sichtprüfung |
| Linux-/Windows-Vollmatrix | [Native GitHub-Matrix](https://github.com/n05a-design/glide-to-do/actions/runs/41408047495) läuft; Ergebnisse erst nach Abschluss eintragen |
| Native Mac-Kern-/Paketprobe | [Zehn native Kerngruppen](p8_macos.json), [zwölf Getter-/Aktionsproben](native_getter_macos.json) und [Start der gelieferten App](mac_start_lieferung.json) grün; externes Python und ungebündelte Quellen im Paketprozess gesperrt |

[974 unveränderte nicht-Markdown-Prüfeingaben](matrix_eingaben.json) sichern Programm, Tests, Fixtures, Ressourcen und Bauwerkzeuge gegen den eingefrorenen Mac-Lauf. Der anschließende Dokumentations-/Vorschaubildnachlauf wird separat geprüft. Alle 108 Integrationssuiten bleiben Teil der Vollprüfung. Die vorhandenen Funktionen bis 3.50 einschließlich Import/Export, Wiederholung, Fokus, Nebenansicht, Seiten-/Notizaufgaben, Pinnwänden, Bildern, Zeichnungen, Sicherungen, Schreibschutz, Mutationsfehlern und Wiederanlauf werden gemeinsam geprüft. Die menschliche Prüfung folgt anschließend; Screenreader ist bis Bedarf zurückgestellt.

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

**macOS arm64:** [nativer Bau und kompilierter Quell-/Lizenznachweis](mac_bau.json), [Archiv-/Quellabgleich](mac_archivabgleich.json), [isolierter Runnerstart](mac_start_runner.json), [Bauabschluss](mac_bauabschluss.json), [tatsächlicher Lieferabgleich](mac_lieferabgleich.json). Python 3.14.5, Tcl/Tk 9.1.0, 463 Dateien und 30 interne Symlinks. [Nativer Workflow](https://github.com/n05a-design/glide-to-do/actions/runs/41408038981).

- Aktive lokale App: `~/Applications/Glide.app`; `build/macos/Glide.app` verweist darauf. OneDrive ergänzt an Frameworkordnern wiederholt Finder-Metadaten, die eine strenge Signaturprüfung im Syncordner beanstanden kann. Deshalb liegt die native Installation außerhalb des Syncordners; die Signatur wird am aufgelösten Bundlepfad geprüft. Keine neue Signatur und keine veränderten Appbytes durch den Lieferweg.
- Weitergabe: `build/macos/Glide-3.50.0-macos-arm64.tar.gz`, SHA-256 `0dd5a39d1631d0fce610c8e6e6c01a3e5b9e12ea285ed85cc17fe1ecf992d0bb`. Das TAR unverändert weitergeben und nativ entpacken, damit Dateimodi und Verknüpfungen erhalten bleiben. Die lokale Verknüpfung ist kein plattformübergreifendes Paket.
- Vorherige 3.49-App und ihr TAR bleiben als Rückweg erhalten. Mac ist Ad-hoc-signiert; Developer ID und Notarisierung sind nicht vorhanden.

**Windows x64:** Endlauf und anschließender nativer Paketbau laufen. Alte 3.45-Lieferung nicht als aktualisierten Endstand ausgeben; tatsächlichen Austausch und SHA-256 erst nach Erfolg eintragen. Linux verwendet die Python-Fassung; ein eigenständiges Linux-Binärpaket ist nicht gewählt.

## Vorläufe und Prüfgrenzen

Die früheren roten Läufe bleiben lokal erhalten. Veraltete Layout-/Menüerwartungen wurden nach der ausdrücklich beauftragten UI-Änderung angepasst; die Aktionssuche erhielt die fehlende Farbgruppe. Fachliche Kriterien, Formatgrenzen und Schreibschutz wurden bewahrt.

Der [Fokus-Gegenfall](fokus_rot.json) reproduziert auf `557331e` den fehlenden Editorfokus beim Ziehen aus der Seitenleiste. Der Griff übernimmt seit `6e4cff5` den Textfokus; echte Escape-Ereignisse prüfen den Abbruch. Der vollständige Mac-Lauf auf `6e4cff5` war [125 Schritte grün](vorlauf6e/voll_macos.json), ebenso die [Linux-Matrix](vorlauf6e/voll_linux.json) und ihre [Defektgegenproben](vorlauf6e/linux_defektgegenproben.json). Die danach durch Sichtkontrolle gefundenen Schrift-/Zählerfehler sind im neuen Frischprozess vorher rot und nachher grün belegt. Diese alten Matrix-/Paketbelege unter `vorlauf6e` werden nicht als Endstand umetikettiert.

Menschliche Sicht-/Bedienprüfung, DPI und mehrere Monitore folgen mit den tatsächlich gelieferten Paketen anhand der [bestehenden Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md). Screenreader (VoiceOver/NVDA/Orca) gehört bis zu einem konkreten Bedarf nicht zur aktiven Restliste.

Historische WA-41A/B-Untersuchungen bleiben als Grenzen erhalten: systemweite Instabilität auf PC-02 und frühere Save/Reload-Differenz ohne gespeicherte Felddiagnose. Grüne Gegenläufe erklären ihre Ursache nicht; keine weitere Intel-Stressserie oder spekulative BIOS-/CPU-Änderung. Appweite WA-32/39/36-Vorhaben haben belegte Teilabschlüsse und werden durch diesen konkreten Stand nicht als vollständig umgebaut bezeichnet. Ungewählte Zukunftsfunktionen sind keine fehlenden 3.50-Implementierungen. Öffentliche Signatur/Notarisierung, Lizenz, Marke und weitere Vertriebskanäle bleiben gesonderte Entscheidungen.
