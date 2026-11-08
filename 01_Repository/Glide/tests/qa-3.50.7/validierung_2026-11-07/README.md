# Validierung und Fortschreibung auf Glide 3.50.7

Stand 07.11.2026 · Glide 3.50.7 · Datenformat 26

Datierter Rundennachweis zum Auftrag „Validierung 3.50.6“ und dem Inhabernachtrag 3.50.7. Aktuelle Aufgaben gehören ausschließlich in den Entwicklungsplan §21.77, Marktbefunde in Markt §15, technische Einordnung in Analyse §13.30. Dieser Nachweis sammelt Eingabehashes, wirkliche Prüfungen und Grenzen; kein Merge und keine Releasefreigabe.

## Basis und Umfang

PR #69 war beim Start offen, `main` `8e71ae5286f6cfcc7f738cb238c29c180c3f289c`, Head `be37940866cf262c496cac43c92c62fea8470fcf`. Während der Runde wurde der PR auf `13bcb66a7ba2007c3d8828ba1e0e082cb8918c91` ergänzt (Notion-Neuverankerung); dieser Nachtrag wurde übernommen. Eigener Branch `codex/glide-3.50.7-validierung`. Ursprüngliche OneDrive-Ablage auf `40c20fd6` mit 368 Statuszeilen und beschädigtem Git-Objekt unangetastet; frischer Clone als Arbeitsbasis.

Der Auftrag wurde vollständig gelesen und in den bestehenden Quellen fortgeschrieben. Der ursprüngliche Download war beim Abschluss nicht mehr zugänglich; deshalb wird kein ungesicherter Originaldatei-Hash behauptet. D72/D73 halten die umgesetzten Inhabervorgaben fest, ohne ein zweites dauerhaftes Auftragsdokument anzulegen. Historische QA-Dateien werden nicht umetikettiert. Der vorhandene Market-Trends-Template-Bezug bleibt unverändert; die Präsentation ist separater Anhang.

## Korrekturen und Beleggrenzen

- Produktkommunikation, README, Über-Glide-Text, Produktregister und Veröffentlichungsunterlagen auf Desktop-Planer mit vier Produktbereichen ausgerichtet. Beschreibung und 15 Topics nach konkreter Freigabe unmittelbar auf GitHub geändert und zurückgelesen.
- Root-LICENSE (MPL-2.0) bleibt unverändert. Aktive alte Lizenzangaben und Erzeuger korrigiert; Python-Lieferung führt Originaltext und Hinweise mit. Neue native Lizenzbestände führen zusätzlich einen festen Git-Quellbezug. Historische Mac-Lizenzbasis unverändert.
- 3.50.6-Änderungen, D64–D71, Seitenleisten-/Anhangsnachträge und Quell-/Python-/Showcase-Stände gegen Code und Nachweise abgeglichen. Versionswechsel auf 3.50.7 über vorhandenes Werkzeug, Datenformat bleibt 26.
- Neue Seitenleistenprüfung deckte zwei konkrete Fehler auf: Ein vorhandenes `tkfont.Font` wurde erneut als Schriftbeschreibung gemessen, der abgefangene Fehler führte zu Ersatzhöhe 20; bei Rubik/mittel entstand eine Systemzeile von 28 px für 23 px Schriftzeilenhöhe statt der vorgesehenen 8 px Reserve. Nach einem Neustart im selben Prozess war `ttk.Style()` außerdem an einen fremden Tk-Interpreter gebunden (Stilabfrage 28, tatsächliches Rechteck 17 px). Direkte Schriftmessung und `ttk.Style(self.root)` korrigieren beide Ursachen.
- Die Sichtprüfung fand zusätzlich angeheftete Texte mit alter Schrift-/Hoverfarbe nach dem Designwechsel. Der erweiterte Test war vor der Korrektur bei Rubik/klein/dunkel rot (`#15243C` statt `#F5F5F7`). Erneutes Rendern dieser eigenen Farbrollen beim Designwechsel korrigiert den Befund.
- Zwei Prüfaufbauten wurden an den bestehenden Vertrag angepasst: Die Unterzeile wird am sichtbaren Fenster und den sichtbaren Texten unter dem Titel statt an einem ausgeblendeten Metadatenrahmen gemessen (D66, unveränderter Arbeitsmodi-Vertrag). Der Anhangshinweis wird während der ganzen echten Startphase beobachtet; der bisherige Beobachter kam nach einem bereits abgearbeiteten Leerlauf zu spät. Das direkte Testende der Kernprüfung löst globale Layoutbeobachter vor der Interpreterzerstörung, damit daraus keine neuen Leerlaufjobs entstehen.

## Prüfungen

Die unveränderte Anfangsbasis `be379408` bestand unter Windows 11, AMD Ryzen 7 5800X3D, Python 3.14.7 / Tk 9.0.4 die strenge CI-Grundstufe. Die nachfolgenden Ergebnisse gelten jeweils für die in `ergebnis.json` bezeichneten Bytes. Ein früher neuer Testaufruf scheiterte zunächst am selben falschen Messaufruf im Test; dieser Vorlauf ist kein gültiger Produktgegenbeleg. Der danach korrigierte Test zeigte vor dem Produktfix die echte fehlende Höhenreserve. Der erste Nachlauf zeigte den getrennten Interpreterfehler. Ursprüngliche rote Nachweise bleiben erhalten.

### Tatsächlich ausgeführte lokale Prüfungen

Die aktuellen UI-Läufe verwenden Windows 11 / AMD Ryzen 7 5800X3D, Python 3.14.7 mit eigener Tcl/Tk 9.1.0 aus einem vorhandenen eingefrorenen Prüfpaket. Dessen Laufzeit wurde nur gelesen; kein altes Glide-Paket wird als 3.50.7 ausgegeben. Alle Testdaten sind synthetisch und über `GLIDE_DATA_DIR` isoliert. Rohlogs, Runtimepfade und Fensterbilder bleiben außerhalb des öffentlichen Repositorys; Hashes und Ergebnisgrenzen stehen in `ergebnis.json`.

| Prüfung | Ergebnis und Geltung |
|---|---|
| Unveränderte Startbasis `be379408`, strenge CI-Grundstufe | 19/19 erfolgreich, Windows / Python 3.14.7 / Tk 9.0.4; eigene Baseline vor Produktionsänderungen |
| Strenge Grundstufe vor dem letzten Farbfix | 19/19 erfolgreich; 259 Werkzeugtests (1 Skip), zweimal 1.155 Fachtests; gilt für die damaligen Bytes, nicht als spätere native Vollmatrix |
| Neue Seitenleistenmatrix `seitenleistenzeilen3507` | 48 Konfigurationen / 384 sichtbare Zeilen, vier echte Schriftwahlen, drei Größen, Hell/Dunkel, 860/1280 px, vier Neustarts; Mindesthöhen und Schriftreserve, Interpreterzuordnung und angeheftete Textfarben erfolgreich; acht Bilder erzeugt, Hell/Dunkel nach dem Farbfix angesehen |
| UI-/UX-Paket | 17/17 erfolgreich auf 3.50.7 mit Tk 9.1; unveränderte 3.50.6-Gegenprobe ebenfalls 17/17 |
| `seitenleistenabstand3504` | 16 Hover-Geometrieprüfungen erfolgreich, inklusive schmal/ausgeblendet und Rückwechsel |
| `unterzeile` | 136 Ansichtsprüfungen erfolgreich, vorhandener D66-Vertrag erhalten |
| `anhangsnamen` | Erfolgreich: erzwungene Umbenennung, Begrenzung, ZIP mit Originalbytes, Rücknahme bei Schreibschutz, Speicherversagen, alte Backup-Pfade, vollständiger Dublettenvergleich und saubere Notion-Neuverankerung |
| `test_glide` | Nach Korrektur des Prüfaufbaus erfolgreich; ursprüngliche rote Probe und erster grüner Lauf mit separater Testende-Meldung bleiben als Vorläufe erfasst |
| Früherer gezielter 3.50.7-Lauf mit Tk 9.0.4 | `test_logo330` (einschließlich MPL-/Beschreibungstext und stabiler Kennungen), `test_import3410`, `test_mindestgroesse330` (75 Ansichten / 56 Dialoge), `test_kompression330`, `test_festlayout330` erfolgreich auf dem dortigen Quellhash; Import-Testende meldete einen verwaisten Tk-Aufruf. Die UI-/UX-Suite war dort 9/17 grün, 8 rot; nicht mit Tk 9.1 vermischen |
| MPL-/Paketwerkzeuge | Zwei neue Fälle zu Originalbytes/Hash/festem Commit sowie Ablehnung veränderter/fremder Quellen erfolgreich; vorhandene Mac-/Windows-Lizenzwerkzeuge mitgeprüft. Vollständiger Root-Lizenztext stimmt nach Leerraumnormalisierung mit SPDX MPL-2.0 überein |
| Python-Lieferung | 93 Code-Dateien / 171 Ressourcen bytegleich; vollständige MPL und Lizenzhinweis zusätzlich bytegleich kopiert |
| Showcase | Echter Import, Verweise, fünf Dokumentarten, drei Ordnertypen, sechs Originalmotive, Seitenbilder, Pinnwände, Undo, Vorlagen, Export und Neustart erfolgreich; sechs Lieferdateien unter 05 bytegleich abgeglichen |
| Dokumente | Stand-, Index-, Dateilink- und Datenschutzprüfung in der Grundstufe; zusätzliche Prüfung von 322 lokalen Markdown-Ankern ohne offenen Befund nach Korrektur eines alten Logo-Verweises |

Die abschließende strenge Grundstufe auf den letzten Bytes wird separat in `ergebnis.json` erfasst. Beispielbefehle vom Repository-Unterordner `01_Repository/Glide` aus (Protokollziele jeweils außerhalb der versionierten Ablage):

```text
python -B tests/tools/ci_grundstufe.py --lieferstand-streng --protokoll <Nachweis>
python -B tests/integration/test_arbeitsmodi.py --fall seitenleistenzeilen3507 --report <Ergebnis>
python -B tests/integration/test_arbeitsmodi.py --fall seitenleistenabstand3504 --report <Ergebnis>
python -B tests/integration/test_arbeitsmodi.py --fall anhangsnamen --report <Ergebnis>
python -B tests/integration/test_arbeitsmodi.py --fall unterzeile --report <Ergebnis>
python -B tests/integration/test_glide.py
python -B tests/integration/test_uiux_paket.py
python -B scripts/pflege/abgleich_07.py
python -B scripts/pflege/showcase_abgleich.py
```

### Rote Vorläufe, externe Matrix und Grenzen

Der erste neue Grundstufenlauf war wegen einer fehlenden Referenz auf `Glide-Lizenzstatus.md` im Release-Text rot; Referenz ergänzt, vorhandenen Vertrag nicht abgeschwächt. Die cp1252-Konsole brach danach an der Ausgabe eines Zeichens ab; weitere Läufe verwendeten UTF-8. Ein Abschlussvorlauf wurde vom Integritätswächter korrekt gestoppt, nachdem während der laufenden Unit-Tests noch README-Badge und portable Lizenzverweise korrigiert wurden (Unit-Exitcode 0, Gesamtlauf rot, Folgen übersprungen). Der vollständige Nachlauf startet erst nach diesem Dokumentabschluss. Ursprüngliche Höhen-/Interpreter-/Farbgegenproben und überholte Testannahmen werden nicht aus dem Ergebnis herausgerechnet. Ein erster neuer Höhen-Test hatte selbst den falschen Font-Messaufruf übernommen; das war kein gültiger Produktgegenbeleg.

Live geprüft auf PR #69 / `13bcb66a`: [Lauf 42409344418](https://github.com/n05a-design/glide-to-do/actions/runs/42409344418) und der parallele PR-Lauf haben grüne Grundstufen und rote native Vollprüfungen. Windows stoppt in `test_glide` am alten Unterzeilenrahmenvergleich; lokal reproduziert, oben begrenzt korrigiert. Linux meldet in `test_arbeitsmodi` 59/61 grün, rot `kompakt` (Kürzel bei Fokus `None`) und `pinnwandleiste` (Anordnung bei 1720 px/großer Schrift/Spalten ausgeblendet). Diese zwei Befunde sind auf Windows nicht als Linux-Korrektur erledigt. Linux-Defektgegenproben liefen danach durch; Folgeprüfungen nach dem Stopp blieben übersprungen. Paket-/Reader-/UI-Diagnosejobs waren übersprungen. Originalartefakte wurden anhand der von GitHub gemeldeten ZIP-Hashes verifiziert; sie enthalten keine neuen Auslieferungspakete.

Kein neuer vollständiger 107-Suiten-/nativer Mac-Vollmatrixbeleg für 3.50.7. Native Mac-/Linux-Geometrie, aktuelle eigenständige Pakete, physische DPI-/Mehrmonitorprüfung und menschliche Gesamtfreigabe bleiben getrennte Tore. PyInstaller ist im verfügbaren Standard-Python nicht installiert; es wurde kein Neubau behauptet. Reader ist nach D58 bewusst zurückgestellt.

## Bewahrung und Ablage

**Fortschreibung 08.11.2026:** Die unten beschriebene vorbereitete Alterskürzung ist im Endstand zurückgenommen, soweit sie 225 im aktuellen Main vorhandene historische Dateien betrifft. Originaldateien sind im Arbeitsbaum wieder vorhanden, alle Git-Blobs gegen `d7e017f` identisch geprüft. QA-Erststand und zugehörige Fixture sind ausdrücklich geschützt. [Bewahrungsnachtrag](bewahrung_nachtrag.json). Die folgende datierte Beschreibung sowie ZIP/Git-Nachweise dokumentieren den Zwischenstand und bleiben unverändert erhalten.

Die vorhandene Sieben-Versionen-/Drei-Bildversionen-Regel verschiebt mit 3.50.7 die Grenzen. 226 alte reproduzierbare Dateien wurden vor der Kürzung gegen Git geprüft und zusätzlich in einem lokal CRC-/SHA-verifizierten ZIP bewahrt. `aufbewahrung.json` nennt jeden Pfad, Dateihash, Git-Blob und festen Quellverweis auf `13bcb66a`. 81 aktive Verweise wurden auf diese unveränderlichen Git-Nachweise umgestellt. Datierte Originale innerhalb der verbleibenden Versionen, ursprüngliche Nutzerbilder, Lizenzbasen und lokale Diagnoseeingänge wurden nicht umgeschrieben. Die ursprüngliche OneDrive-Arbeitskopie und ihre vier Stashes blieben unberührt.

## Marktbericht als separater Anhang

Sechs editierbare Folien aus dem vorhandenen Market-Trends-Template, dessen Original unverändert blieb. Inhalte aus Markt §15 und aktuellen Primärquellen; tatsächliche ältere Produktaufnahme klar zugeordnet. Bilder/Quellen/Schriften und alle Folien gerendert kontrolliert, finale PPTX erneut importiert und auf Paket-/Layoutbefunde geprüft: null Befunde. SHA-256 `1e6646af5c466564bc24404cedbc2c6d81e4aee8ccec53e0df0450ef93b99218`. Keine native PowerPoint-Ausführung behauptet. Präsentation ist eine Zusammenfassung, keine zusätzliche Roadmap.

Offene Arbeit und Entscheidungen mit Priorität, nächstem Schritt und Fertigkriterium stehen ausschließlich im Entwicklungsplan §21.77.

## Fortsetzung 08.11.2026 auf aktuellem Main

Main `d7e017f001e5c069eeb98a0f5302577966ac4098` enthält den genannten Merge #69 `37750811` sowie #70 (Systemregister). Neuer Arbeitsbranch direkt von Main: `codex/glide-3.50.7-main-validierung`; vorherige Arbeit gesichert als `f0c4442`, übernommen als `1b58d1e`. Die frühere strenge Grundstufe auf der 13b-Basis ist inzwischen 19/19 erfolgreich; ihre Zahlen sind kein neuer Main-Volltest.

Aktuelle Originalbasis: Actions 42427354033, Linux-Artifact 13597026351 (ZIP SHA-256 `46cd8557080e2f0fc40ee8e82dd4b37e49d8c8125ea0c7f37a37cbd6194100a3`), Windows 13597052182 (`fc78d0235ee52b8886523bf12bb4052e794d778d53b39afb8987f27ee44ceb99`), beide heruntergeladen und gegen die GitHub-Hashes geprüft. Windows scheitert weiter am ursprünglichen Rahmenvergleich und danach an der offenen Erwerbssperre. Linux: 59/61 Arbeitsmodi, Kompakt und Pinnwandleiste rot; kein grüner Gesamtabschluss.

Die Kompakt-Ereignisspur belegt beim Rückwechsel: Press schaltet aus, der kurzfristige Fokusverlust setzt `down=False`, Release schaltet erneut ein. Der Reparaturkandidat prüft externen Fokusverlust erst im nächsten Leerlauf. Gezielter Windows-Kompaktfall und echte externe Fokusverlustprobe sind grün; native Linux-Bestätigung offen. Die externe Fokusprobe erzeugt den FocusOut-Hinweis erst bei tatsächlich an einen unabhängigen Interpreter abgegebenem Fokus, statt eine Nachricht bei weiterhin fokussierter App als äußeren Fokusverlust zu deuten.

Die Kernprüfung registriert ihre isolierten App-Instanzen in einem ExitStack innerhalb des Temp-Verzeichnisses: Auch bei Assertion-Abbruch werden Timer und Datensperre vor dem Verzeichnisabbau freigegeben. Regulärer Kernlauf grün; gezielte erzwungene Abbruchprobe grün: Assertion unmittelbar nach App-Konstruktion, Datensperre gelöst und alle erfassten isolierten Testverzeichnisse vollständig entfernt, kein WinError 32. Der D66-Vertrag bleibt über sichtbare Texte und die vorhandene 136-Fälle-Prüfung erhalten.

Pinnwand-Kandidat: Textbreite plus beidseitig 8 px statt zusätzlicher 26/30 px Breitenreserve für die Aktions-/Auswahlknöpfe. Keine Beschriftung oder Aktion entfernt; unveränderte Prüfung kontrolliert vollständige Textdarstellung, Erreichbarkeit und eine Leistenzeile. Native Linux-Validierung bleibt bis zum tatsächlichen Nachlauf offen.

Das neue Glide-Systemregister bleibt erhalten; eigenständige Systemversion 1.1 mit Änderungsverlauf und zusätzlichem MPL-Werkzeugtest, vier Registerprüfungen grün. Appversion 3.50.7 und Datenformat 26 sind davon unabhängig.

Gezielter Windows-Pinnwandnachlauf: 1.248 Knopfprüfungen erfolgreich; Kompakt und externer Fokusverlust ebenfalls erfolgreich. Native Linux-Bestätigung und finale Gesamtmatrix weiterhin offen.

Weiterer Grundstufenvorlauf auf Main-Kandidat rot: Timeout-Werkzeuggegenprobe erreichte unter gemessener CPU-Auslastung 100 % innerhalb 1 s nicht ihren eigentlichen Blockierfall. Der Prüfaufbau wartet jetzt auf ein vom Kind geschriebenes Bereitschaftsmerkmal (Startlimit 30 s); die eigentliche Timeout-Grenze bleibt 1 s, der absichtlich blockierte Fall 30 s, Stack-/Teiloutput-/Fortschritts-/Folgestopp-Assertions bleiben vollständig erhalten. Eigenständiges Merkmal statt parallelem Lesen der atomar ersetzten JSON-Datei vermeidet eine Windows-Dateisperre im Prüfaufbau. Alle 18 Prüfablauffälle danach grün. Produkt- und Vollprüfungszeitlimits unverändert.

Main-Reparaturkandidat: strenge Grundstufe im zweiten Nachlauf vollständig 19/19 erfolgreich (263 Werkzeugtests, 1 Skip; zweimal 1.155 Fachtests), Python 3.14.7 / Tcl-Tk 9.1.0. Quelle/Python bytegleich, 335 Dokumentlinks, Original-Fremdcodevergleich und Datenschutz erfolgreich. Details/Quellhashes in `main_fortsetzung.json`. Die erste rote Timeout-Probe bleibt separat erhalten. Native Gesamtmatrix weiterhin ausstehend.
