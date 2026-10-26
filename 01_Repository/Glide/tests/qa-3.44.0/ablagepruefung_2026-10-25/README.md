# Ablage- und Dokumentationsprüfung vor Push und Merge

Prüfdatum 25.10.2026 · lokaler Kandidat auf Glide 3.44.0 / Format 26 · App `2c274277…`.

## Umfang

Der Auftrag umfasst die gesamte Projektwurzel einschließlich ignorierter Dateien, Git-Verwaltung und fünf separater Arbeitskopien. Er umfasst keinen Commit, Push, Merge, Versionswechsel oder Lieferabgleich. Die Metadateninventur enthält 10.863 Dateien und 1.398 Ordner, keine Verknüpfungen und keine Inventurfehler. Für alle 3.314 Dateien des Hauptbestands außerhalb von Git und Worktrees wurden Inhalte mit SHA-256 aufgenommen; ein langer Windows-Dateipfad wurde mit dem erweiterten Pfadpräfix nachgeprüft. Keine Cloud-Platzhalter im Hauptbestand. Die Arbeitskopien sind nach Git-Status und Commitzugehörigkeit bewertet; zusätzlich sind alle 28 ignorierten lokalen Dateien gegen den Hauptbestand gehasht und gleich. Ihre gesamten versionierten Binärinhalte wurden nicht noch einmal gehasht.

Die Prüfung bewertet Zuständigkeit, Aktualität, Erreichbarkeit, Aufbewahrung, Integrität und Uploadhygiene. Sie behauptet keine manuelle Zeile-für-Zeile-Codeprüfung und keine erneute Funktionsabnahme jedes Bildes, Archivs oder Fremdprodukts. Neue Marktvergleiche und Produktentscheidungen entstehen daraus nicht.

## Korrekturen

- `storage_health.py` in Architektur, Modulübersicht und Paketierungsanleitung nachgetragen; außerdem in den expliziten Kopierlisten für 07 und das Mac-Bundle ergänzt. Ohne diese Ergänzung hätte ein späterer Abgleich das neu importierte Modul ausgelassen. Kein Paket oder Lieferstand wurde dafür neu erzeugt.
- Testübersicht auf 103 registrierte Suiten berichtigt. Quellenstruktur neu per AST gezählt: 83 Laufzeitdateien plus Prototyp, App 65.144 Zeilen, `ListApp` 49.697 Zeilen / 1.738 direkte Methoden.
- Falsche Aussage „eingefrorene Windows-Vollprüfung bestanden“ in den Funktionen korrigiert. Die damaligen roten WA-41/WA-42-Belege bleiben unverändert.
- Übergabe zusammengeführt und gekürzt; heutiger Quellkandidat, historische Lieferung und externe GitHub-Prüfungen stehen in einer aktuellen Matrix. Wurzel-/Quell-README und Claude-Einstieg auf denselben Stand gebracht.

## Quellen, Nachweise und Aufbewahrung

[Bestandsbilanz](bestandspruefung.json), [vollständige Inventur vor der Bearbeitung](inventar_vorher.json), [SHA-256 des Hauptbestands](dateihashes_vorher.json), [Inhaltsdubletten](inhaltsdubletten.json), [lokale Aufbewahrungsprüfung](aufbewahrung_lokal.json), [Verweise](verweise.json), [HTTP-Prüfung externer Verweise](externe_verweise.json), [Uploadhygiene](uploadhygiene.json), [Arbeitskopien](arbeitskopien.json), [ihre lokalen Belege](arbeitskopien_lokale_belege.json), [Dokumentregister](dokumentregister.json), [Liefer-/Referenzabgleich](lieferung_referenzen.json) und [Remote-Läufe](remote.json) bilden die prüfbaren Einzelnachweise.

Vor dem Nachlauf: 84 Markdown-Dateien und 1.293 relative Inline-Verweise einschließlich Überschriftenziele ohne Befund. 218 unterschiedliche externe Inline-URLs geprüft: 214 antworten auf HTTP HEAD mit 200. Nachprüfung: [Google Keep](https://support.google.com/keep/answer/6320648?hl=en) und [DPMA](https://www.dpma.de/marken/markenrecherche/index.html) sind über den Web-Abruf mit Inhalt erreichbar; [AppFlowy](https://appflowy.com/guide/appflowy-local-ai-ollama) ist erreichbar, sein Seiteninhalt aber nicht extrahierbar. [EUIPO](https://www.euipo.europa.eu/en/trade-marks/before-applying/availability) bleibt wegen HTTP 403 ungeklärt. Ein HEAD-Fehler beweist kein fehlendes Dokument. Erreichbarkeit ist keine Neuvalidierung aller Herstellerbehauptungen. Quellen behalten ihr eigenes Recherche-/Abrufdatum.

Aufbewahrung auch im ignorierten lokalen Bestand ohne Befund: sieben Versionsstände 3.39.1 bis 3.44.0; Bilder der drei neuesten 3.43.0, 3.43.1, 3.44.0. Die 28 originalen Eingangsreferenzen stimmen vollständig mit ihrem Manifest überein und bleiben wegen Kontoangaben vom Upload ausgeschlossen. Migrations-/Messfixtures, Grafikmaster, Lizenzkopien und Lieferartefakte bleiben erhalten. Die größten Dubletten sind benötigte Showcase-/Fixture-Spiegel und in Lieferungen benötigte Ressourcen, kein freigegebener Löschbestand.

## Speicher und Bereinigung

Ausgangsbestand: 2.760.145.353 Byte (2,57 GiB), davon 938.507.528 Byte Git-Verwaltung, 1.402.588.239 Byte fünf Arbeitskopien und 419.049.586 Byte Hauptbestand. Das sind Dateipfadgrößen ohne NTFS-Verwaltung; mögliche Hardlinks sind mangels Dateiidentität nicht herausgerechnet. Eine Freigabe von genau so viel physischem Speicher wird nicht behauptet.

Alle fünf Arbeitskopien haben einen sauberen Git-Status. `beautiful-babbage-196492` enthält zwei Commits, die nicht im lokalen HEAD liegen; die vier anderen haben keine solchen Commits. Die 28 ignorierten lokalen Dateien sind inhaltsgleich im Hauptbestand vorhanden ([Abgleich](arbeitskopien_lokale_belege.json)). Vier nicht mehr vorhandene Mac-Arbeitskopien sind in Git als bereinigbare Registrierungen verzeichnet. Arbeitskopien, Branches, Stashes und Registrierungen wurden nicht entfernt.

Sechs bereits bekannte Git-Temporärdateien belegen laut `git count-objects` rund 98,19 MiB. Git-Objekte und Historie wurden nicht gelöscht oder neu gepackt. `git fsck --full --no-reflogs` endet mit Exitcode 0; gemeldete unreferenzierte Objekte sind Wiederherstellungsbestand und kein Integritätsfehler.

117 regenerierbare `.pyc`-Dateien (6.568.287 Byte) wurden als begrenzter Cacheplan geprüft. Die automatische Freigabeprüfung lehnte das Entfernen vor Ausführung mit „blocked by policy“ ab. Es wurde kein Cache gelöscht und kein alternativer Löschweg versucht. [Geprüfter Cacheplan](cache_bereinigungsplan.json). Deshalb gibt es in dieser Runde keinen ausgewiesenen Speichergewinn; neue Prüfbelege vergrößern den Bestand etwas.

## Push-/Mergegrenzen

Quelle und Python-Lieferung tragen beide 3.44.0 / Format 26, unterscheiden sich aber in neun Laufzeitdateien. Windows-Paket 3.42.0: 102/102 Manifestdateien gleich. Mac-Paket 3.42.0: 327/330 gleich, drei bereits bekannte Framework-/Signaturdateien fehlen. Keine native Paketprüfung in dieser Runde.

Die folgenden Remote-Zahlen sind der erste Abruf; der spätere externe Merge ist im Absatz darunter ausgewiesen. Lokal bleibt HEAD `71854ec` auf `claude/phasenabschluss-3.44.0`; die jüngsten Änderungen sind uncommittet. `.git/index.lock` ist vorhanden, seit 23.10.2026 datiert und wurde nicht entfernt. Sie ließ sich in einer kurzen Momentaufnahme exklusiv lesend öffnen ([Sperrbefund](indexsperre.json)); das ist keine Garantie für spätere Schreibaktivität. Ihr Alter allein belegt keinen sicheren Löschzeitpunkt; vor einem späteren Schreibauftrag laufende Git-Aktivität und Eigentümer klären. Remote sind `main` `d60ef81` und D55 `facf61a` bestätigt, deren Läufe #153/#154 grün. Diese Ergebnisse decken die neuen lokalen Korrekturen nicht ab.

Der [Abgleich aller 1.631 Remote-Dateien](remote_abgleich.json) findet lokal kein fehlendes Ziel. 30 Dateien unterscheiden sich von `facf61a`; eine Grafikabweichung ist ausschließlich CRCRLF gegenüber CRLF, der SVG-Inhalt ist gleich. Dokument-/Quellunterschiede gehören zu den uncommitteten Nachläufen. Ein langer Windows-Pfad wurde gesondert bytegleich bestätigt. Dies ersetzt den späteren Git-Abgleich des tatsächlich zu veröffentlichenden Commits nicht.

D55-Punkte 1–4 sind menschlich abgenommen; Punkt 5 und die übrigen nativen Konfigurationen bleiben offen. Während der Prüfung wurde PR #40 extern gemergt: `main` ist jetzt `291c393`, der D55-Zweig nicht mehr aufgeführt. Alle 1.631 Dateiblobs des Merges sind gleich `facf61a`; der vorangehende Remote-Dateiabgleich gilt damit auch für diesen Merge. [Abschluss-Snapshot](remote_abschluss.json): Glide-Prüfung #156 läuft noch, CodeQL #55 ist grün. Die jüngsten lokalen Korrekturen sind im Merge nicht enthalten. Die dokumentierten Abnahme-/Versionsgrenzen gelten für den nächsten Produkt-/Lieferabschluss weiter. Der aktuelle Prüfauftrag ist keine Releasefreigabe.

## Abschluss

Die [CI-Grundstufe](ci_abschluss/ergebnis.json) endet mit Exitcode 0: 19 Schritte, davon 18 ausgeführt und bestanden sowie ein erwarteter Lieferhinweis (neun Unterschiede zur Quelle). 165 Werkzeugtests (einer übersprungen), jeweils 896 Fachtests mit/ohne Systemzeitzonen, alle fünf Analysen, Syntax-/Versions-/Fixtureprüfung, Tk-Startprobe, 116 unveränderte Vendor-Dateien, Datenschutz, Aufbewahrung und Synchronisation bestanden. Windows / Python 3.14.7 / Tk 9.0.4, temporäre künstliche Daten. Nicht im strengen Liefermodus gelaufen; der dokumentierte Kandidatenunterschied bleibt bestehen.

Der abschließende reine Dokument-/Hygienenachlauf und die [Bestandserhaltung](bestandsabgleich_abschluss.json) sind in der [Abschlussbilanz](ergebnis.json) zugeordnet. Beim Anker-Nachlauf wurde ein Link auf die frühere Übergabeüberschrift erkannt; die bestehende Überschrift ist wiederhergestellt. Dieser rote Zwischenbefund bleibt in `verweise_abschluss.json`, das endgültige Ergebnis steht separat in `nachlauf.json`. Alle 798 geschützten Dateien sind hashgleich. Keine neue eingefrorene 103-Suiten-Matrix oder native Menschenabnahme in dieser Ablagerunde. Ergebnis: Ablage-/Dokumentationsprüfung abgeschlossen mit dokumentierten Git-, Liefer-, nativen und Bereinigungsgrenzen; keine uneingeschränkte Merge-/Releasefreigabe.
