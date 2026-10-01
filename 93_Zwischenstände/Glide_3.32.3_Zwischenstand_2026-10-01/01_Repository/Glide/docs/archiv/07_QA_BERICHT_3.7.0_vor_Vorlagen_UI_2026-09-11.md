# QA-Bericht – Glide 3.7.0, Nachbesserung 11.09.2026

Prüfumgebung: macOS, Python 3.14.5, Tk 9.0. Alle App-Importe mit temporärem
`GLIDE_DATA_DIR`; keine echten Nutzerdaten als Testbestand verwendet.

## Ausgangsprüfung

Der unveränderte Ausgangsstand wurde mit allen bisherigen zehn Suiten geprüft.
Neun bestanden. `test_glide_36` scheiterte vor der Ausführung am plattformabhängigen
Laden der `.pyw`-Datei. Ein expliziter SourceFileLoader behebt diese Testinfrastruktur.
Syntax, Versionen, Dokumentlinks, Fixtures und beide Analysen waren bereits grün.
[Protokoll](../tests/qa-3.7.0/macos-nachbesserung/baseline/ergebnis.json).

## Nachbesserung

Die zusätzliche Suite `test_template_workflows` prüft die 16 vollständigen Vorlagen,
die reproduzierbare Erzeugung, Sicherung und Migration von Vorlagenformat 1,
Abbruch ohne Änderung von Aufgaben, Labels oder Anhangsordner, den echten Editor
mit Unterdialogen in Hell/Dunkel, Umsortieren mit erhaltenen Unterpunkten,
Anhangsrundlauf, relative/absolute Fristen sowie kleine und horizontale
Tk-9-Trackpad-Ereignisse. Der gezielte Lauf bestand.

Der vollständige Abschlusslauf **bestand mit Exitcode 0**:

- Alle elf Testsuiten erfolgreich, einschließlich der neuen Vorlagenprüfung.
- Syntax, Versionskonsistenz, Dokumentationsindex und 195 lokale Dokumentlinks geprüft.
- Beide statischen Analysen erfolgreich.
- Beispiel- und Releasebackups neu erzeugt und inhaltlich gegen die ausgelieferten Dateien abgeglichen.
- Der Vorlagenkatalog ist deterministisch reproduzierbar; seine 16 Einträge durchlaufen die App-Validierung.
- Die startbare Python-Arbeitskopie und der Vorlagenexport stimmen bytegleich mit den kanonischen Dateien überein.
- 77 Archivnachweise mit SHA-256 geprüft: 40 Verschiebungen und 37 Sicherungskopien.

[Abschlussprotokoll](../tests/qa-3.7.0/macos-nachbesserung/final/ergebnis.json) ·
[Dateiprüfsummen](../tests/qa-3.7.0/macos-nachbesserung/aktuelle_dateien_sha256.json) ·
[Quellcodeänderungen](../tests/qa-3.7.0/macos-nachbesserung/aenderungen_app.diff).

Der vorherige Abschlussversuch deckte einen alten Fehler im Testaufbau auf:
Die reine Normalisierung der Beispieldaten ließ deren Ordner im Testbestand
zurück, ohne die nun enthaltenen Anhangsdateien zu laden. Der Test stellt jetzt
sämtliche temporär geänderten Sammlungen wieder her und prüft die drei Anhänge
zusätzlich über einen echten Import mit anschließendem Undo. Der korrigierte
Kerntest und der folgende vollständige Lauf bestanden.

## Offene manuelle Abnahme

Eine Sichtprüfung über Computer Use kam nicht zustande: zunächst fehlende Freigaben bzw. ein gesperrter Mac, danach ein abgebrochener Zugriffsversuch.
Die Widget- und Ereignistests ersetzen keine Prüfung mit physischem Trackpad
und keine visuelle Bewertung von Abständen, Textschnitt und Fokusdarstellung.
Windows mit Tk 8.6, hohe Skalierung, mehrere Monitore, längere Nutzung sowie
signierte Pakete bleiben gesonderte Abnahmen. Es wurde kein Installer erzeugt,
signiert, veröffentlicht oder ein Store-Release freigegeben.

[Auftragsabgleich](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md) ·
[Manuelle Prüfliste](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.7.0.md)
