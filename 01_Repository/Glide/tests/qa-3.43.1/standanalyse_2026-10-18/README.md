# Standanalyse und Dokumentationsnachlauf vom 18.10.2026

Stand 18.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · keine Produktionsrunde

Dieser Ordner enthält ausschließlich die Prüfprovenienz zur fortgeschriebenen [Analyse](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md), [Marktrecherche](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md) und [Planung](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md). Die Ergebnisse und offenen Abnahmen stehen im einzigen [QA-Bericht](../../../docs/07_QA_BERICHT.md); hier entsteht kein zweiter Backlog. Die App-Version, Produktionslogik, Datenformate, Lieferpakete und echte Nutzerdaten bleiben unverändert.

## Untersuchungsgegenstand und Grenzen

Lokaler Zweig `claude/tag3390-sichtbarkeit`, HEAD `c0252bad69780c86b853f2653d5396e5256c0b32`; die Arbeitskopie war zu Beginn laut fest gesetztem Skriptwert sauber (nicht unabhängig gemessen; Einordnung in Analyse §12.2). Lokale Hauptdatei SHA-256 `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`. Windows 11, Python 3.14.7/Tcl-Tk 9.0.4. Upstream `9ec474b` und der getrennte Planungszweig `19c7df5` wurden gelesen, weder ausgecheckt noch gemergt. D51 und die dort bereits vergebenen Planungskennungen wurden dokumentarisch konsolidiert.

Alle 67 eigenen Produktionsmodule wurden strukturell erfasst; kritische Aufruf- und Datenflüsse wurden vertieft. Das ist keine vollständige Zweig- oder Plattformabdeckung. Wettbewerber wurden über Primärquellen untersucht, nicht installiert oder praktisch bedient. Nutzerreferenzbilder wurden nach Größe und Hash geprüft; kein neuer vollständiger visueller Produktaudit.

## Dateien und Belegfunktion

| Datei | Beleg |
|---|---|
| [ausgangsstand.json](ausgangsstand.json) | Git-Refs, vollständiger Apphash, einzelne Quell-/07-Hashes, Showcase, Paketmanifeste und Unverändertheitsbaseline |
| [dateiinventar.json](dateiinventar.json) | Metadaten einschließlich ignorierter Hauptcheckout-Dateien; private Arbeitsdaten/Logs und separate Worktrees abgegrenzt, Langpfade berücksichtigt |
| [dokumentinventar.json](dokumentinventar.json) | ursprüngliches Register der 48 aktiven Dokumente, Titel/Größe/Hashes, Konflikt- und Dublettenprüfung; aktuelle Behandlung im Analysedokument |
| [aufbewahrung.json](aufbewahrung.json) | sieben QA-Versionen, getrennte QA-Bildgrenze, Originalreferenzen geschützt, keine Löschung |
| [nutzerreferenzen.json](nutzerreferenzen.json) | alle 28 Originalbilder vorhanden und manifest-/hashgleich, nicht versioniert |
| [module-inventory.json](module-inventory.json) | Rollen, Größen, Struktur und bestehende Unit-Namensbezüge; kein eigener Testlaufbeleg |
| [probe_codegrenzen.py](probe_codegrenzen.py) | reproduzierbare isolierte Fehlerinjektionen, keine Produktionskorrektur |
| [ergebnis_codegrenzen.json](ergebnis_codegrenzen.json) | zwölf ausgeführte Proben mit Quellhash und ausdrücklich begrenzter Aussage |
| [remote.json](remote.json), [github_auftritt.json](github_auftritt.json) | datierter lesender API-/Git-Snapshot; keine fortlaufende Überwachung |
| [remote_abschluss.json](remote_abschluss.json) | erneuter Abschlussabruf: derselbe Commit, Gesamtworkflow erfolgreich; besondere Readerjobs ausgelassen |
| [Grüner CI-Abschluss](ci_abschluss/ergebnis.json) | 19/19 Schritte, Exitcode0; 152 Werkzeugtests, 714 Units mit und ohne Systemzeitzonen |
| [CI-Ausgangslauf](ci_ausgang/ergebnis.json) | 19 Schritte, 18 grün, Synchronisation während der laufenden Marktkonsolidierung rot; unverändert erhalten |
| [ergebnis.json](ergebnis.json) | bestandene abschließende Dokument-/Link-/Hash-/Standprüfung; unveränderte 213 Produktionsdateien sowie 07 und Showcase |
| [probe_codegrenzen_upstream.py](probe_codegrenzen_upstream.py), [ergebnis_codegrenzen_9ec474b.json](ergebnis_codegrenzen_9ec474b.json) | Gegenprüfung: dieselben zwölf Proben gegen `9ec474b`; A33 behoben, A32/A34/A35/A27 unverändert |
| [probe_datensperre.py](probe_datensperre.py), [ergebnis_datensperre.json](ergebnis_datensperre.json) | Gegenprüfung: 14 isolierte Fälle zur Datensperre `glide.lock` (A36/WA-30) |
| [sicherungsmanifest_gegenpruefung.json](sicherungsmanifest_gegenpruefung.json) | SHA-256 aller 56 vor der Gegenprüfung gesicherten Dateien und Wiederherstellungsweg; die Kopien liegen außerhalb des Repositorys |
| [gegenpruefung.json](gegenpruefung.json) | abschließende Prüfungen der Gegenprüfung |
| [abschluss_vorlauf.json](abschluss_vorlauf.json) | früherer Linkprüflauf mit zwei veralteten Marktankern; beide im aktuellen Plan korrigiert |

## Reproduktion der Schutzbefunde

Aus `01_Repository/Glide`:

```powershell
$env:PYTHONUTF8='1'
python -B tests/qa-3.43.1/standanalyse_2026-10-18/probe_codegrenzen.py --source src/glide/app.pyw --output <neues-Ergebnis.json>
```

Das Skript setzt `GLIDE_DATA_DIR` vor dem App-Import auf ein temporäres Verzeichnis. Es erzeugt kein Tk-Fenster, verwendet künstliche Daten und unveränderte Produktionsmethoden; UI-/Dateiadapter werden an der untersuchten Fehlergrenze ersetzt. **Es soll bekannte Fehler zeigen und ist keine grüne Regressionssuite einer bereits behobenen App.**

- A32: Guard-Tiefen 0/19/20 jeweils mit direktem Schnappschuss und echtem `item_change`. Bei Tiefe 20 versagt die Wiederherstellung eines gezielt injizierten Punktverlusts; bei 0/19 funktioniert sie.
- A33: tatsächliches Undo/Apply-Snapshot bis `save_items=False`; Schritt verbraucht und Erfolg gemeldet. Der Upstream-FP-01-Kandidat enthält bereits eine separate Korrektur, die hier nicht angewendet wurde.
- A34: gültige Daten plus injiziertem `tk.TclError` beim UI-Aufbau. Fälschliche Schadensmeldung, Sicherung und leerer schreibfähiger RAM-Bestand; Originaldatei zunächst unverändert. Ein späteres Autosave wurde in dieser Probe nicht ausgeführt.
- A35: beide Editorfehler und der Erfolgsfall liefern aus `flush_rich_note` jeweils `None`; die vorhandenen `is False`-Barrieren greifen nicht.
- A27: unbekannte Einstellungsformatmarke 999 wird auf 2 normalisiert; unbekanntes oberstes Feld bleibt, verschachteltes Filterfeld verschwindet.

A31 ist ein statisch bestätigter synchroner Konversionsaufruf im UI-Thread, keine Messung einer typischen Wartezeit. Die Proben beweisen keine natürliche Verlusthäufigkeit oder Beschädigung echter Nutzerdaten. Korrekturaufgaben: WA-26–WA-29 und FP-01 im Entwicklungsplan.

## Aktuelle Ausführung und verbleibende Tore

Der ursprüngliche strenge CI-Lauf bestand 152 Werkzeugtests, 714 Fachlogiktests sowie nochmals 714 ohne Systemzeitzonen, alle fünf Analysen, Startprobe, Fremdcodeherkunft, Datenschutz, Retention und Lieferabgleich. Einziger roter Schritt war die zwischenzeitliche Kürzung des noch bearbeiteten Marktdokuments. Die abschließenden Prüfungen werden separat dokumentiert und überschreiben diesen Vorlauf nicht.

67 Code-/146 Ressourcen-/Vendordateien in 07 und sechs Showcase-Dateien stimmen zur lokalen Quelle. Das Windows-Paket 3.42.0 hat 102/102 korrekte Manifestdateien. Das lokale Mac-Bundle 3.42.0 hat 327/330; drei Python-Frameworkdateien fehlen. Keine aktuelle native Paketstart-/Signaturprüfung wurde daraus abgeleitet.

Keine neue vollständige lokale Integrationsmatrix, Mac-/Linux-/Tk-9.1-/Screenreaderbedienung oder Menschen-/DPI-/Mehrmonitorabnahme. Keine Commits, Pushes, Merges, Builds, Installationen oder Veröffentlichungen. Ein abgeschlossener Analyse-/Dokumentationsauftrag ist keine Releasefreigabe; praktische Tore und Produktentscheidungen bleiben offen.

**Abschluss:** Strenge CI erneut vollständig grün. Der rote Vorlauf bleibt erhalten; die abschließende Verweisprüfung und der unveränderte Produktions-/Lieferstand sind in `ergebnis.json` festgehalten.

## Gegenprüfung 18.10.2026

Nach dem Abschluss wurden die Abschlussaussagen gegen den erweiterten Claude-Auftrag gegengeprüft. Vor jeder Dokumentänderung wurde der uncommittete Stand gesichert ([Manifest](sicherungsmanifest_gegenpruefung.json)). Aus `01_Repository/Glide`:

```powershell
$env:PYTHONUTF8='1'
python -B tests/qa-3.43.1/standanalyse_2026-10-18/probe_codegrenzen_upstream.py --source <app.pyw aus 9ec474b> --label 9ec474b:01_Repository/Glide/src/glide/app.pyw --output <neues-Ergebnis.json>
python -B tests/qa-3.43.1/standanalyse_2026-10-18/probe_datensperre.py --source src/glide/app.pyw --output <neues-Ergebnis.json>
```

Beide Skripte setzen `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner und öffnen kein Tk-Fenster. Die Datensperrprobe startet zusätzlich einen kurzlebigen Python-Kindprozess als lebende Fremd-PID.

- Wiederholung der Originalprobe am lokalen Stand: Ergebnisdatei bytegleich zu `ergebnis_codegrenzen.json`.
- Upstream `9ec474b` (App-SHA-256 `61f7b96394f0ced5…`): A33 behoben, A32 (Tiefe 20, beide Varianten), A34, A35 und A27 unverändert.
- Datensperre (`c0252ba`): defektes JSON, JSON-Liste und unlesbarer Lockpfad gelten als frei; 8 Stunden ohne Schreiben gelten auch bei lebendem Prozess als verwaist; eine verschwundene Lockdatei wird beim Erneuern nicht neu angelegt; eine fremde Kennung führt korrekt zu Schreibschutz; die Freigabe lässt einen fremden Lock stehen. Rennen zweier Prozesse und Cloud-Abgleich sind nicht nachgestellt.

Weitere Ergebnisse und Grenzen: [gegenpruefung.json](gegenpruefung.json), Einordnung in Analyse §11.4 und §12.2.
