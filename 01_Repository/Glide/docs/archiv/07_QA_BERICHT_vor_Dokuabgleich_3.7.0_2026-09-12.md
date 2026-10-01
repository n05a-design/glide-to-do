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

## Zweiter UI-Nachtrag: Vorlagenbaum und Mac-Dropdowns

Die vollständige Ausgangsprüfung bestand:
[Baseline](../tests/qa-3.7.0/vorlagen-ui-macos/baseline/ergebnis.json).
Nach der Änderung bestanden zehn Suiten sowie Syntax, Versionen,
Dokumentation und Beispieldatenabgleiche. Die elfte Suite suchte im Testcode
ausschließlich nach einem nativen Menubutton und fand das neue Mac-Feld nicht:
[erster Abschlusslauf](../tests/qa-3.7.0/vorlagen-ui-macos/abschluss/ergebnis.json).
Der Finder akzeptiert jetzt beide Plattformtypen bei unveränderten fachlichen
Assertions. Der [gezielte Wiederholungslauf](../tests/qa-3.7.0/vorlagen-ui-macos/test_release37_korrigiert.json)
bestand ebenfalls. Damit sind alle elf Suiten für diesen App-Quellstand erfolgreich;
der fehlgeschlagene erste Gesamtlauf bleibt als solcher dokumentiert.

Die erweiterte Vorlagensuite prüft beide Dropdownpfade, Farben, Auswahl,
Abbruch, lange Menüs und modale Grab-Rückgabe einschließlich Zerstörung
des Feldes. Hinzu kommen Vorlagenbaum-Stile, geschlossene Zweige sowie
Spalten und erreichbare Aktionen bei 800×640, 1050×780 und 1500×950.
Eine zusätzliche lesende Codeprüfung führte zur Absicherung von
Destroy/Grab und Popupkoordinaten außerhalb des Hauptbildschirms.
Der [geprüfte Quellstand](../tests/qa-3.7.0/vorlagen-ui-macos/gepruefter_quellstand_sha256.json)
wurde in die startbare Python-Arbeitskopie übernommen.

Zwei erneute Computer-Use-Versuche blieben bei ausstehenden Accessibility-
und Screen-Recording-Freigaben stehen. Es gibt deshalb weiterhin keine native
Sichtabnahme dieser Änderung. Windows wurde hier nur über den unveränderten
Widgetpfad geprüft, nicht auf einem Windows-System. Physische Mehrmonitor-,
Trackpad- und Screenreaderprüfungen bleiben offen. Die eigens gestartete
Vorschau wurde beendet; deren isolierte temporäre Beispieldaten wurden entfernt.


## Dritter UI-Nachtrag: dynamische Ordner-/Listenkacheln (12.09.2026)

Die gezielte Layoutsuite bestand. Ihre 18 Bestandsansichten kombinieren Hell/Dunkel,
ein bis drei Spalten und kleine/mittlere/große Schrift. Die tatsächlichen
Kachelhöhen lagen im Testbestand zwischen 194 und 436 Pixeln. Geprüft wurden
sichtbare Innenränder, vollständige CTA-Texte und -Flächen, gleiche Stapelabstände,
fehlende Überlappungen, Fokus-Scrollen und der Leerzustand. Öffnen, Rückkehr und
Neustart ließen den Bestand unverändert. Alle Daten lagen in einem temporären
`GLIDE_DATA_DIR`.

[Geometriedaten](../tests/qa-3.7.0/dynamische-kacheln/geometrie.json) ·
[Quellcodeänderungen](../tests/qa-3.7.0/dynamische-kacheln/aenderungen_app.diff) ·
[Prüfsummen von Code und Arbeitskopie](../tests/qa-3.7.0/dynamische-kacheln/gepruefter_quellstand_sha256.json).

Ein erster Geometrieversuch prüfte auch noch unsichtbare Canvas-Frames direkt.
Tk lieferte dort die alte tatsächliche Framebreite trotz bereits korrekt gesetzter
Canvas-Sollbreite. Eine isolierte Diagnose bestätigte die korrekte Aktualisierung
beim Sichtbarwerden. Die Prüfung scrollt nun jede Karte sichtbar und prüft danach
alle endgültigen Stapelpositionen zusammen; die Abstandsanforderungen wurden
nicht gelockert. Eine zusätzliche lesende Schlussprüfung fand keine weiteren
wesentlichen Fehler.

Der startbaren Python-Arbeitskopie wurde der gleiche Quellstand übergeben; ihr
Vorgänger liegt im dortigen Archiv. Der vollständige kombinierte Prüflauf **bestand mit Exitcode 0**:
alle elf Testsuiten, Syntax, Versionen, Dokumentverweise, beide statischen Analysen
sowie neu erzeugte Beispiel- und Releasedaten einschließlich ihres Inhaltsabgleichs.
[Abschlussprotokoll](../tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json).
Die sieben Ressourcen der Arbeitskopie stimmen bytegleich mit dem Projekt überein. Die oben genannten Grenzen der nativen Sichtabnahme und
der Windows-Ausführung bleiben bestehen.
