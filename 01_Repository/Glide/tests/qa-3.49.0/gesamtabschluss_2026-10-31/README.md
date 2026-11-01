# Abschlussfortsetzung am 31.10.2026

Glide 3.49.0 · Aufgabenformat 26 · eigene Tcl/Tk-9.1-Laufzeit / Python 3.14.5 / macOS arm64

Der Auftrag führt den vorherigen Dokumentationsaudit technisch fort. Der aktuelle Restumfang steht ausschließlich im [Entwicklungsplan §21.37](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2137-abschlussfortsetzung-mutationen-prüfablauf-tk-91-und-lieferung); datierte ältere Berichte bleiben erhalten. Quellkorrekturen sind integriert, die native Mac-Vollmatrix und lokale Python-/Showcase-/Mac-Lieferung sind abgeschlossen. Keine Gesamtabnahme oder 4.0-/öffentliche Freigabe.

## Technischer Schnitt

Anlegen, Kalender, Unter-/Geschwisterpunkte, Einfügen, direkte Übersichtsfelder/Labels und Sortierung prüfen den Schreibbesitz und frische Dialogziele. Gemeinsame Änderungsrahmen sichern Undo und Hauptspeicherung; nachgewiesene Savefehler erzeugen keine Erfolgsmeldung. Labelmanager ermittelt ersetzte Labelobjekte anhand stabiler ID. Tk-freie Ziel-/Feld-/Label-/Sortierregeln in `task_editing.py`.

Vier rote CSV-/ICS-Gegenproben zeigen den bisherigen Fehler: neue Listen/Punkte blieben nach fehlgeschlagener Hauptspeicherung im RAM. Korrigierte CSV-/ICS-/TXT-/Austauschwege setzen den ganzen Snapshot samt vollständigem Undo-Stapel und Dirty-Zustand zurück. CSV/ICS neu/anhängen danach viermal grün. Erfolgreich gespeicherte Importe schützen nachfolgende UI-Aufrufe.

[Bereichsproben](bereichsproben.json): ursprünglich 17 Mutationsfälle mit flüchtigem Fehlerinjektionsfehler; gezielte neue Rot-/Grünpaare 27/27 und 41/41, sieben Leerenfälle grün, vier Import- und zwei Labelmanagerfälle grün. [Alle 56 Mutationsfälle gemeinsam grün](mutationen.json), einschließlich der drei Gruppen-Dialoge mit frischen Objekten/Schreibschutz und des vollen Undo-Stapels beim mehrzeiligen Einfügen. [Rote Gruppenprobe](details_rot.json), [rote Undo-Probe](einfuegen_rot.json), [begrenztes Speicheraufrufinventar](speichereinstiege.json). [Quellhashes](quellhashes.json), [konfliktfreie Integration](integration.json).

Der frühere Leeren-/Entfernen-Fehler ist für den Prüfadapter deterministisch reproduziert: die pauschale Injektion traf manchmal die Sperrdateierneuerung, bevor eine Mutation begann. Neue Injektion erzwingt diese Erneuerung und weist danach den eigentlichen Hauptdateifehler nach. Keine Erklärung für WA-41A/B daraus ableiten.

## Neue Grundprüfung und Zugänglichkeit

[Grundstufe grün](ci.json): 235 Werkzeugtests (drei Skips), zweimal 1.082 Fachtests (je ein Skip), fünf Analysen, Tk-Startprobe und formale Kontrollen. Frischer tkinterdnd2-Abgleich: 116 Dateien bytegleich zum gepinnten Original. [Roter Vorlauf](ci_rot.json): neuer Folgestopp korrekt, ein alter unvollständiger Mock bekam jetzt den echten Reportvertrag und zwei zusätzliche Assertions; Produktionsvertrag unverändert. Rohlogs bleiben lokal.

Eigene Runtime aus den im Projekt gepinnten Originalquellen gebaut. [Zwölf native NSAccessibility-Getter-/Aktionsproben](native_macos91.json) grün. [P8-Vorlauf rot](p8_vorlauf_rot.json): Kästchenassertion bei konkurrierendem GUI-Test. [Isolierte Diagnose](p8_diagnose.json): gleiche fachliche Kriterien, nur ausführlichere Assertiondiagnose, zehn Gruppen grün. Fokuswartepunkt und tatsächlichen Fokusnachweis im Originaltest ergänzt; die [finale Originalsuite](p8_kern.json) besteht alle zehn Gruppen mit nativem Backend in der vollständigen Tk-9.1-Matrix. Echte VoiceOver-/NVDA-/Orca-Sprache und menschliche Bedienung sind dadurch nicht abgenommen.

Der frühere 21–31-Sekunden-Pinnwandbefund ließ sich im Einzelprozess nicht reproduzieren: 200 Karten mit unveränderter App und 800 Font-Anlagen [ca.59 ms mit Tk 9.1](pinnwand_tk91.json), [ca.89 ms mit Tk 9.0](pinnwand_tk90.json). Einzelmessungen mit Profiling, kein stabiler Benchmark und kein Beweis der historischen Ursache; kein spekulativer Fontcache eingebaut. Die originale Seitenkartensuite behält die relative +10-%-Grenze.

## Mutationskosten WA-36

[Identische Anfangsbestände, Vorher/Nachher](mutation_benchmarks.json), [Messskript](messung_mutationen.py): echter direkter Wichtigkeitswechsel über `update_in_progress_item`, zwei Warmläufe und neun Messungen; vollständiger Snapshot, Hauptspeicherung und Renderaufruf sowie anschließende Tk-Verarbeitung separat erfasst. Zwölf Aufgabenlisten plus leerer Eingang, keine Anhänge, natives Tk 9.1 am selben Mac. Gesamtkosten Median/p95 in ms:

| Aufgaben | Vorher | Nachher |
|---|---:|---:|
| 100 | 6,73 / 7,07 | 5,57 / 6,22 |
| 1.000 | 26,64 / 27,12 | 17,02 / 17,32 |
| 5.000 | 117,80 / 149,41 | 66,35 / 68,09 |
| 10.000 | 229,66 / 252,07 | 127,88 / 153,64 |

Anfangsfixture je Größenstufe SHA-256-identisch; pro Schritt RAM und gespeicherten Wert geprüft. p95 bei neun Proben entspricht dem Maximum; verschachtelte Teilzeiten nicht addieren. Diese Zahlen gelten nur für diesen Änderungsweg und lokalen Prüfplatz. Ein erster Fixture-Versuch enthielt einen unterschiedlichen Eingang-Zeitstempel und wurde verworfen; finale Messungen erst mit korrigiertem vollständigem Fixturehash und ohne parallelen Bau. Kein appweiter oder plattformübergreifender Performanceabschluss.

## Aufbewahrung

[Bereinigung](bereinigung.json): alle 751 vom Audit inventarisierten ignorierten QA-Dateien nach Pfad-/Symlink-/Größenprüfung und SHA-256 entfernt, 741 Bilder + zehn Logs = 13.907.192 Bytes. Die 28 Original-Nutzerbilder bleiben geschützt.

[Plattformmatrix mit allen aktuellen Nachweisen und offenen Zellen](plattformmatrix.json).

## Native Endmatrix und Lieferung

[Vollständige Mac-Matrix](voll_macos.json) `t1031-164116`: 126 ausgeführte Schritte grün, alle 108 Integrationssuiten, 1.082 Fachtests (ein Skip), native Tcl-Zugangsbindungen, P8-Kern, Showcase, fünf Analysen und Beispiel-/Releasedaten. Zwei ausdrücklich übersprungene Tore sind Windows-Aufnahmen und menschliche Sichtprüfung. Keine zufällige Wiederholung bis grün: der Tk-9.1-Rotlauf der anderen Sitzung wurde durch den belegten Aqua-Emacs-Fehler erklärt und nach Korrektur vollständig neu geprüft ([Originalbericht](../mac_gegenlauf_2026-10-31/README.md)).

[707 relevante aktuelle Eingaben bytegleich](matrix_eingabeabgleich.json), [geprüfte Quell-/Test-/Fixture-/Ressourcenhashes](matrix_quellhashes.json). Eigener redundanter Teilversuch nach dieser Verifikation nach Ende seines Speicher-Kindprozesses beendet; keine GUI-Kindprozesse dafür signalisiert ([Stopnachweis](redundanz_stopp.json)). Er wird nicht als zusätzlicher vollständiger Erfolg gezählt. Die früher bewusst abgebrochenen eigenen Vorläufe bleiben [gesondert eingeordnet](vorlaeufe.json).

[56 Mutationsfälle der aktuellen Vollmatrix](mutationen_matrix.json). [Native Tcl-Bindungen](p8_tcl.json), [zehn P8-Kerngruppen](p8_kern.json) sowie [zwölf erneut ausgeführte echte NSAccessibility-Getter-/Aktionsproben](native_macos91_final.json) grün. Die weitere Aqua-Kürzelkorrektur aus der anderen Sitzung ist erhalten: reine Plattformregel in `interaction_policy.py`, Schutz der Strg-Buchstaben-Navigation auch auf macOS, keine Änderung an Befehlstasten oder Pfeiltasten. Der aktuelle Apphash ist `1fabf883d14ff7bb576803b90ac565fc18d5fcf32b79a53a9f8ce036de7bbbeb`.

[Lieferung](lieferung.json): Python-Fassung und Showcase 3.49.0, 91 Code-Dateien und 147 Ressourcen/Vendor-Dateien abgeglichen. [Echte Python-Lieferprobe](python_lieferprobe.json): sechs Ansichten, Speichern und Erledigen/Undo mit isolierten Daten, keine Callbackfehler, Module tatsächlich aus `07_Python-Versionen`. Eigenständiges macOS-arm64-Paket 3.49.0 mit eigener Tcl/Tk 9.1, 463 Dateien, Modul-/Quell-/Lizenzinventar und Ad-hoc-Signatur geprüft ([Bau](paketbau.json)). [Isolierter Start des Bauartefakts](paket_start_bau.json) und [direkt aus der gelieferten App](paket_start_lieferung.json) grün; externes Python, Bauumgebung, ungebündelte Runtime und Quellen im jeweiligen Kindprozess gesperrt. Installationen unverändert. Frühere Mac-App 3.45.0 als Rückweg erhalten.

Mac-Archiv `Glide-3.49.0-macos-arm64.tar.gz`, SHA-256 `74dda534ab2e7847ae1ed3d2ace8b2a66d580657bd22adc049f9a14e59fbb36d`. Lieferung unter `build/macos/Glide.app` und `build/macos/Glide-3.49.0-macos-arm64.tar.gz`; Code-/Ressourcen-SHA-256 stehen in den JSON-Belegen. Benutzerpfade der Berichtskopien pseudonymisiert, Rohlogs lokal.

Die frühere Seitenkarten-Verlangsamung ist von der anderen Sitzung auf mehrere aufeinanderfolgende Tk-Instanzen nach Startseitenaufbau im selben Prozess eingegrenzt; normales Glide verwendet eine Tk-Instanz pro Prozess. Der bestehende `druck_tempo`-Fall läuft nun mit unveränderter Messung und +10-%-Grenze in einem eigenen Kindprozess. Aktuelle Testhashes sind in der nativen Matrix enthalten. Kein spekulativer Fontcache; genauer CoreText-Auslöser bleibt ungeklärt ([Eingrenzung](../mac_gegenlauf_2026-10-31/README.md)).

[Reine Zeichenkodierungsreparatur](kodierung.json) der datierten Robustheits-README: 49 Zeichen rekonstruiert, Zahlen/Aussagen unverändert.

## Unabhängige Schlusskontrolle 31.10.2026 abends

Nach Codex' Abbruch durch das Nutzungslimit von einer Claude-Code-Sitzung am M2 nachgeprüft, ohne Änderung an Code, Tests oder Lieferung. [Zusammenfassung](schlusskontrolle_unabhaengig.json).

- Strenge CI-Grundstufe (`--lieferstand-streng`) 19 von 19 Schritten ohne Hinweis: `07_Python-Versionen` bytegleich zu `src/glide`, tkinterdnd2 116 Dateien bytegleich (mit System-Zertifikatsspeicher), Dokumente, Datenschutz und Ablage grün.
- Mac-Archiv `Glide-3.49.0-macos-arm64.tar.gz` passt zu seiner `.sha256` (`74dda534…`); das Bundle trägt App `1fabf883…` einschließlich `interaction_policy` und `pinboard_pages` des aktuellen Stands.
- Frisch entpackt: `codesign --verify --deep --strict` gültig; isolierte Paketprobe Exit 0, externes Python gesperrt (71). Das Paket bringt Python 3.14.5 und Tcl/Tk 9.1.0 mit, sechs Ansichten, Anlegen/Abhaken/Undo und Sicherung im Rundlauf grün. Der macOS-Emacs-Schutz aus §21.36 ist damit für Nutzer dieses Pakets wirksam.
- Geräteanleitung (`tests/README.md`, `packaging/runtime/README.md`, `docs/10_VEROEFFENTLICHUNG.md`): alle genannten Werkzeugoptionen und Dateien vorhanden, 93 Abschnittsanker der geänderten Dokumente lösen auf.
- `paketbau.json` meldet die Startprobe noch als „ausstehend“; das ist der Stand der Bauphase, überholt durch `paket_start_lieferung.json` und diese Probe.

## Freigabegrenzen

Windows-Paket weiterhin 3.45.0; aktuelle Windows-/Linux-Endmatrix und vollständige NVDA-/Orca-Kette fehlen. Echte VoiceOver-Ausgabe, DPI/Mehrmonitor/Clean-Machine und menschliche Bedienung sind durch native Getter nicht abgenommen. Inhaber übernimmt die Prüfung selbst (Antwort 31.10.2026), noch keine Ergebnisse oder Freigaben; die [bestehende Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) enthält konkrete Abschlussfälle und Rückmeldungsvorlage.

WA-41A/B bleiben ohne bewiesene Ursache; keine BIOS-/CPU-Änderung oder zusätzliche Intel-Stressserie. Der alte eigene Tk-9.1-Abbauabsturz nach bewusstem SIGTERM ist als solcher eingeordnet, kein spontaner WA-41A-Beleg. Appweite WA-32/39/P05/G27 und übriger WA-36-Umfang sind durch einen konkreten Mutationsschnitt nicht appweit geschlossen. Keine öffentliche Signatur/Notarisierung, kein Windows-Neubau, kein Git-Push, keine Gesamtabnahme und kein 4.0-Abschluss.

[Abschließende Syntax-/Versions-/Link-/Stand-/strenge Liefer-/Datenschutz-/Aufbewahrungskontrollen](schlusskontrollen.json).

**Eigengeräte-Entscheidung:** Inhaber übernimmt die verbleibenden Prüfungen selbst; kein Push/Workflowstart. [Startaufrufe](../../README.md#abschlussprüfung-auf-eigenen-geräten-entscheidung-31102026), [Runtimevoraussetzungen](../../../packaging/runtime/README.md#eigene-prüfgeräte--bau-und-auswahl-der-runtime), [Windows-Entwicklungsbau](../../../docs/10_VEROEFFENTLICHUNG.md#windows-entwicklungsbau-auf-eigenem-gerät-3490). Die nachträgliche Änderung der Runtime-README ist reine Anleitungspflege und im Eingabeabgleich erfasst. Programme, Fach-/Integrationstests, Fixtures und Ressourcen unverändert. Hosted-only ACL-Isolationsprobe bleibt offen; persönliche Installationen werden nicht gesperrt.
