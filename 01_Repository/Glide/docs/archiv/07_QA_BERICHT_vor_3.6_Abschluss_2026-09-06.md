# QA-Bericht 3.5.0

Stand: 05.09.2026 · App-Version 3.5.0 · Aufgabendatenformat 11 · Einstellungsformat 1

## Windows-Abschluss

**Der vollständige automatisierte Windows-Prüflauf besteht mit Exitcode 0.**
Python 3.12.7 (64 Bit), Tcl/Tk 8.6.13, Anzeige 2560 × 1440,
Tk-Skalierungsfaktor 1,3339898 (etwa 96 logische DPI). Geprüft wurde der
vorhandene Interpreter `C:/Python312/python.exe`.

Maßgeblicher Nachweis: [ergebnis.json](../tests/qa-3.5.0/abschluss/ergebnis.json).
Der [Ausgangslauf](../tests/qa-3.5.0/windows-ausgang/ergebnis.json) bestand bereits
alle fünf Suiten; sein Gesamtfehler kam von alten Format-10-Release-Fixtures.

Bestanden sind Syntax, Versionskonsistenz, Dokumentverweise, aktuelle und
historische Fixtures, `test_glide`, `test_datenintegritaet`, `audit_app`,
`test_dialog_theme`, `test_ui_updates`, beide Analysen sowie die Reproduktion
und der echte Import der Beispiel- und Releaseplanungssicherung.
Die Dokumentverweise werden nach der redaktionellen Fortschreibung zusätzlich
in `tests/qa-3.5.0/abschluss/dokumentation-nachtrag.json` geprüft.

Alle App-Imports nutzten vorher gesetztes, isoliertes `GLIDE_DATA_DIR` in
Testverzeichnissen. Echte Nutzerdaten wurden weder geladen noch verändert.
Der App-Quellcode blieb unverändert und ist mit der startbaren Einzeldatei
3.5.0 bytegleich. SHA-256:
`4D7DCA5F644672A2D37EB2D9A01A202025375DA61E5733A90A8C5A766002CF82`.

## Zusätzliche Windows-Oberflächenprüfung

`test_ui_updates.py --screenshots` bestand und erzeugte 16 Aufnahmen:
Listen bei 1280 und 860 Pixel Breite, Startseite, Eingabe, Einstellungen,
Tastenkürzel, Über Glide und Rückfrage – jeweils Hell/Dunkel.
Die Suite misst außerdem die Listenanordnung bei 980 Pixel Breite.
Alle 16 Aufnahmen wurden angesehen. Die Fälligkeit zeigt Datum und Uhrzeit
bei ausreichender Breite vollständig; bei 860 Pixeln weichen die Metadaten
wie vorgesehen. Inhalte langer Dialoge sind scrollbar, Aktionen bleiben unten.
Die analoge Uhr ist bei dieser Skalierung sichtbar und lesbar.

Zusätzlich wurden alle sieben Wiederholungsauswahlen in beiden Themes bei
760 × 700 Pixel Fenstergröße programmatisch durchgeschaltet: insgesamt
14 Zustände. Abstand erscheint nur bei „alle N Tage“, die Wochentage nur bei
der entsprechenden Auswahl und das Enddatum bei jeder aktiven Wiederholung.
Die Wiederholung steht unter der Fälligkeit; Speichern bleibt innerhalb des
Fensters. Kein Tk-Rückruffehler. Sechs Aufnahmen der erweiterten Zustände
wurden erzeugt und angesehen. Nachweis:
[wiederholungsmaske.json](../tests/qa-3.5.0/abschluss/wiederholungsmaske.json).

Die Bilder liegen unter
[50_Ablage/Screenshots/3.5.0/windows-abschluss](../../../50_Ablage/Screenshots/3.5.0/windows-abschluss/).
Sie stammen ausschließlich aus eigenen Testfenstern. Die zwei zusätzlichen
Releaseplanungsbilder gehören zum Vollmodus. Die Linux-Aufnahmen im übergeordneten
Versionsordner bleiben als historische Vorprüfung erhalten.

## Symbolbefund – keine Gestaltungsfreigabe

Originalausgabe: [symbolpruefung.log](../tests/qa-3.5.0/abschluss/symbolpruefung.log).
Umgebung und Vergleich der Schriftangaben:
[umgebung.json](../tests/qa-3.5.0/abschluss/umgebung.json).

- Die benannte Schrift `TkDefaultFont` ist hier **Segoe UI 9**.
- Die Tupelangaben `("TkDefaultFont", 12)` und `("TkDefaultFont", 11)`,
  die auch in der App verwendet werden, ergeben dagegen **Arial**.
- In der vom Werkzeug geprüften 12-Punkt-Schrift kommen `▣`, `◐`, `◈`, `▦`
  und `↻` aus **MS Gothic**, `▲` und `▼` aus **Arial**. Die zuerst genannten
  Zeichen werden mit 8 Pixeln, die Dreiecke mit 16 Pixeln Breite gemessen.
- Die Wichtigkeitsfähnchen stammen aus **Segoe UI Symbol**.

Die Bilder bestätigen den Größenunterschied. Der Befund widerlegt die
pauschale Annahme, alle diese Elemente würden als Segoe UI gezeichnet.
Das Werkzeug prüft zwei Schriftangaben; es inventarisiert nicht jede tatsächlich
verwendete Widgetschrift und deckt insbesondere nicht alle Fettschnitte ab.
Eine bewusste Vereinheitlichung der Schriftangaben oder der Symbolschrift bleibt
als eigene Oberflächenänderung offen. Es wurden keine Symbole ausgetauscht.

## Bereinigung und Releaseplanung

Die Release-Fixtures 3.2.0, 3.3.0 und 3.4.0 sind aus dem aktuellen Beispielordner
entfernt und im Fixture-Archiv erhalten. Die 3.3.0-Archivkopie wurde neu angelegt;
3.2.0 und 3.4.0 waren bereits bytegleich vorhanden. Im aktuellen Ordner bleiben
zwei Format-11-Backups. Der Beispielname lautet `Glide_Beispieldaten.glidebackup`;
unter Windows existierte nur eine Datei, deren Großschreibung angepasst wurde.

`Claude outputs/`, die verwaisten Linux-Screenshotkopien und der erledigte
Löschmerker sind entfernt. Acht Linux-Bilder und fünf Bilder aus `Claude outputs`
enthielten dieselben PNG-Bilddaten wie die regulären Aufnahmen; Unterschiede
betrafen die Verpackung/Metadaten. Eine zusätzliche Startseitenvorfassung war
keine Dublette und bleibt unter `50_Ablage/Screenshots/3.5.0/archiv/` erhalten.
Vor dem Löschen wurden sämtliche Kandidaten samt aktuellen Fixtures in einem
Archiv mit 22 einzeln per SHA-256 geprüften Dateien gesichert:
[Glide_3.5.0_vor_Bereinigung_2026-09-05.zip](../../../50_Ablage/Archiv/Glide_3.5.0_vor_Bereinigung_2026-09-05.zip).
Nachweise: `sicherung-vor-aufraeumen.json` und `aufraeumen.json` im Abschlussordner.

Die Releaseplanung wurde redaktionell auf Wiederholungen, Textsymbole,
Labelchips, Startseite, Spalten und fünf Testsuiten abgeglichen. Die neue
Sicherung enthält 119 Punkte in drei Arbeitslisten plus leerem Eingang.
Die Version des ersten eingereichten Store-Pakets bleibt eine Buildentscheidung;
3.5.0 bezeichnet hier den internen Planungsstand.
Microsofts Textvorgaben wurden am 05.09.2026 nachgelesen: Das Feld für Neuerungen
bleibt bei der ersten Einreichung leer. Diese Regel legt keine interne
App-Version fest. [Microsoft: Store listing info für MSI/EXE](https://learn.microsoft.com/en-us/windows/apps/publish/publish-your-app/msi/add-and-edit-store-listing-info).
Andere Webquellen behalten ihren historischen Recherchezeitpunkt 04.09.2026.

## Grenzen und offene Arbeiten

Die automatisierte Prüfung und die Sichtung statischer Bilder ersetzen keine
längere reale Mausbedienung. Offen bleiben der Startseiten-Hover mit echter Maus,
weitere DPI-Skalierungen/Monitore, macOS- und Linux-Zielplattformabnahme,
Systemuhr-/Zeitzonenwechsel bei Wiederholungen, Langzeitstabilität und das früher
gemeldete Einfrieren. Es wurde kein Installer gebaut oder signiert und kein
Store-Release freigegeben. Historische Randfälle an Label- und Punkttiefengrenzen
bleiben in der Releaseplanung offen; diese Sitzung war keine Behebung dieser Fälle.

Vorlagenverwaltung und frei wählbarer Datenordner wurden nicht implementiert.
Einstellungen und Tageszahlen bleiben gerätespezifisch und außerhalb des
Aufgabenbackups. Alte Word- und Store-Unterlagen bleiben gekennzeichnete
historische Arbeitsgrundlagen; die aktuellen Nachweise sind dieser Bericht,
die Übergabe und das neue Produktdatenblatt 3.5.0.

## Historische Nachweise

Die vollständige vorherige Berichtsfassung samt Linux-Vorprüfung und früheren
Windows-Prüfständen ist unverändert archiviert:
[QA-Bericht vor der Windows-Prüfung](archiv/07_QA_BERICHT_3.5.0_vor_windowspruefung.md).
