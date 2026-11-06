# Native Mac-Prüfung und Lieferung – Glide 3.50.5

Stand 06.11.2026 · Aufgabenformat 26 · Plan §21.70

Direkter Auftrag: alle am Mac notwendigen Arbeiten für Glide 3.50.5 erledigen. Ausgangs-App SHA-256 `a4bfe4ed9e90c0c10d8a1ee480d99bd46fd8dc50116f092ee52f8f3904ade2ee`; lokale Änderungen aus Windows bleiben erhalten. Keine neue Funktionsauswahl und kein Versionswechsel.

MacBook Air M2, macOS 27.2 arm64, Python 3.14.5 und eigene Tcl/Tk 9.1.0. Alle 1.749 Runtime-Dateien vorab bytegleich zum ursprünglichen Baumanifest. Apple-Bauwerkzeuge vorhanden; keine gültige Developer-ID-Signieridentität. Öffentliche Signierung und Notarisierung bleiben daher separat offen.

Vollmodus aus 1.767 unverändert und bytegleich eingefrorenen Dateien gestartet, `--timeout 900`, getrennte synthetische Daten/Temp je Prozess, unveränderte Abbruch- und Integritätsregeln. Lokale Rohablage: `~/gq/mac3505-20261106/`; Prüfkopie `voll/pruefkopie-y5tn7frn`. Gesamtergebnis noch ausstehend. Native Zusatzprüfungen, eigenständiger Paketbau und Lieferung folgen nacheinander.

Menschliche Gesamtabnahme, physische Trackpad-/Mehrmonitor-/DPI-Prüfung und zurückgestellte Screenreader-Abnahme werden durch automatische Prüfungen nicht bestätigt. Keine Git-/Releaseaktion.

## Erster Vollmodus und Kalender-Testvertrag

Der erste Vollmodus stoppte korrekt nach sieben grünen Vorstufen und 26 grünen Integrationssuiten in `test_features321` an der alten Erwartung eines 57-Zeichen-Titels. [Vollständiger ursprünglicher Bericht](voll_vorlauf.json); keine spätere Suite als ausgeführt gezählt. Gezielte Diagnose bestätigte: Parser faltet vollständig, neue Aufgabe hat 40 Zeichen einschließlich `...`, vollständiger Originaltitel bleibt genau einmal in der Beschreibung. Anwendung unverändert.

Nur diese Teststelle wurde angepasst: vollständiges Parsergebnis, exakter begrenzter Titel, maximale Länge sowie ursprüngliche Beschreibung/Ort und einmaliger vollständiger Originaltitel werden gemeinsam geprüft. Ganze Kalenderimport-Suite danach grün. Statischer Abgleich aller Integrationstests fand keine weitere direkte Textgleichheitsassertion mit einem festen Aufgabentitel über 40 Zeichen. Das ist keine Garantie gegen andere veraltete Erwartungen.

Zusätzlich reine Korrektur der Vorstufen-Bauanleitung auf `build/macos-vorstufe`; ausführbarer AST unverändert. Zwölf echte native NSAccessibility-Getter-/Aktionsfälle grün; [Bericht](native_getter.json). Keine VoiceOver-Abnahme daraus.

## Erweiterter Prüfauftrag und zweiter Vollmodus

Direkter Folgeauftrag: Voll-, Design- und allgemein alle Prüfungen starten. Zusätzlich zum vollständigen Standardlauf werden die unabhängige 17-Fälle-UI-/UX-Suite, alle 51 Arbeitsmodi einschließlich Design-/Schrift-/Flächenmatrizen, strenge CI-Grundstufe, Leistungsprobe und zehnminütiger Dauerlauf sowie native Paketprüfung vorgesehen. GUI-Läufe nacheinander; keine echten Nutzerdaten.

Der zweite Einfrierversuch stoppte vor einer Suite, weil genau der parallel synchronisierte Windows-QA-Bericht ergänzt wurde. Originaler Fehlstartbeleg blieb unverändert. Ein neuer vollständiger Abgleich prüfte dieselbe unabhängige Kopie gegen zweimal stabilen aktuellen Quellbestand: 1.770 Dateien vollständig bytegleich. Separater lokaler Beleg `quellstand_stabilisiert.json`, kein Umschreiben des ursprünglichen Fehlstartmanifests. Danach direkter Vollmodus mit `--zugang-nativ` und unverändertem WA-42-Wächter gestartet.

Acht Vorstufen einschließlich nativer Tcl-Bindungen und 28 Integrationssuiten grün; anschließend `test_features323` an alter Anordnungserwartung zwischen Tagespfeilen und Suche-löschen gestoppt. [Ursprünglicher Bericht](voll_vorlauf_nativ.json). Die neue D63-Anordnung hängt Tagesknöpfe je nach Suchplatz links oder rechts ein; der Test prüft jetzt die Leserichtung passend zur tatsächlichen Packseite und den weiterhin vorhandenen rechten Löschknopf. Produktionscode unverändert. Gezielter Nachtest und neuer Gesamtlauf noch ausstehend. Separater Designlauf gestartet; Ergebnisse werden erst nach Abschluss ergänzt.

## Vollständiger separater Design-/Arbeitsmodilauf

Auf Anwendung `a4bfe4ed…` / Tcl/Tk 9.1.0 beide eigenständigen Läufe ohne Fehler und ohne Integritätsstopp beendet: [UI-/UX-Suite 17/17](uiux.json), [Arbeitsmodi 51/51](arbeitsmodi.json). Alle 51 Fälle in einem zusammenhängenden Prozess bestanden, keine kumulative Auswahl aus Einzelwiederholungen. Darunter neue Buch-/Suchbreite, Seitenleistenabstände, Titel-/Notizregeln, Heute-/Abschnittsgeometrie und getrennte Suchzustände; konkrete Messungen/Design-/Schriftkonfigurationen im Bericht. Dieser Mac-Erfolg erklärt die Windows-Interpreter-/Backendbefunde nicht.

[Zehn native Kerngruppen](native_kern.json) mit ausdrücklich aktivem nativen Backend ebenfalls grün, kein Rückruffehler. Logo-Abgleich im Prüfmodus grün; keine Ressourcen neu geschrieben. Menschliche Sicht-/Trackpad-/DPI-/Mehrmonitor- sowie zurückgestellte Reader-Abnahme bleiben getrennt.

## Dauerlaufbefund, Callback-Korrektur und Zusammenführung

Strenge Grundstufe (244 Werkzeugtests, zweimal 1.134 Fachtests), Fremdcode mit unveränderten macOS-Systemwurzeln (116 Dateien bytegleich, [Bericht](fremdcode.json)) und [Leistungsprobe](leistung.json) auf `a4bfe4ed…` grün. Der zehnminütige Dauerlauf hielt alle 4.015 Punkte nach Neuladen, meldete aber ein wachsendes verwaltetes Callback-Register (248→1.144); [ursprünglicher Bericht](dauerlauf_vorlauf.json). [Diagnose](callback_diagnose.json): nach 30 Erledigen-/Rückgängig-Zyklen 311 verwaltete gegenüber 17 echten Tk-Aufträgen, 295 davon bereits ausgeführt. `_register_after` behält jetzt nur Kennungen, die Tcl noch als lebend führt; aktive und fremde Aufträge werden nicht abgebrochen. Gegenprobe `test_aufraeumen330.py --callback-register` auf altem Stand rot, danach grün.

Vor dem Neustart traf über OneDrive der PC-01-Titelstand `246c6c3b…` ein; dabei entstanden Konfliktkopien (`…-MacBook Pro Max Ultra.*`, `app 2.pyw`). Nur `_register_after` übernommen, übrige Änderungen erhalten: App/Python **`f3afb8fe7b53e4fa8c2dacce7dda64ffabe3373cf5ff02124687c20b58731d1f`**, 93 Code-Dateien/171 Ressourcen bytegleich. Gegenprobe mit den neuen Galerietitelfällen im Aufräumtest zusammengeführt; Gegenprobe und vollständiger Aufräumlauf auf `f3afb8fe…` grün. Mac-Abschnitte der Dokumente übernommen, Konfliktkopien lokal außerhalb OneDrive gesichert und aus dem Quellbaum entfernt. Ein erster Einfrierversuch für den Abschluss brach mit dem Ende der vorherigen Sitzung ab, bevor eine Phase lief.

## Gesamtfolge auf `f3afb8fe…` und Abschlusskorrekturen

**Gesamtfolge 06.11., ab 10:09 MEZ** (1.787 Dateien bytegleich eingefroren, Python 3.14.5 / Tk 9.1.0, künstliche Daten): strenge Grundstufe (244 Werkzeug-, zweimal 1.135 Fachtests), UI/UX 17/17, Design-Inventar, Leistungsprobe (Start 1.240 ms), **zehnminütiger Dauerlauf grün** (Speicherzuwachs −8 %; Callback-Korrektur hält), native Getter, zehn native Kerngruppen, Logo-Abgleich, Symbolprüfung und **Mac-Paketbau grün**: `Glide-3.50.5-macos-arm64.tar.gz`, 17.388.371 Bytes, SHA-256 `f085b64dab52214b14cdba9504e83236a77634a2a0d82c4c4e615070a7893507`, 238 Quelldateien unverändert, isolierter Start bestätigt, nur Ad-hoc-Signatur (Developer-ID/Notarisierung offen). Paket lokal unter `~/gq/mac3505-20261106/final3/paket/`, nicht ausgeliefert.

Rot: Arbeitsmodi 48/51 – die drei Tastatur-/Fokusfälle liefen, während parallel ein eigener Oberflächentest Fokus nahm; Wiederholung allein auf derselben Kopie **51/51 grün**. Vollmodus stoppte an veralteten Testverträgen: `test_features330` (D63-Werkzeug-/Optionsmenü statt Einzelknöpfen, D62-Gelb `#FFDC0B`) und nach Korrektur (`final5`, Grundstufe erneut grün) an `test_logo330`.

**Produktkorrekturen danach (App `80abbabf…`):** (1) Kopflogo sprang zwischen Ansichten mit und ohne Kennzahlenchips um 1 px (39/40); `header_logo_height` bezieht sich jetzt immer auf die Textzeile der Unterzeile. (2) „Mehr › Bildfolge › Bildfolge exportieren …“ öffnete aus einem Menüeintrag ein zweites freies Menü; beide Exporte stehen jetzt direkt im Menü, ungenutzte `animation_export_menu` entfernt. Testverträge `test_features330`, `test_kartenfuss330` (D63-Startseitensuche als erlaubte Startseitenzeile) angepasst.

**Diagnoselauf** aller 65 übrigen Suiten/Analysen nacheinander auf der Arbeitskopie (kein Nachweis): 61 grün. Danach auf `80abbabf…` gezielt grün: Fenster, Kartenfuß, Logo, Animation, Zeichnung, `test_features330`, UI/UX 17/17, Arbeitsmodi 51/51; strenge Grundstufe grün bis auf die Synchronisationsprüfung (Kürzungsvermerk der Übergabe, behoben). 07 bytegleich.

**Offen:** `test_tempo330` – Liste 50,4–59,6 ms je Bild gegen Grenze 3×reines Tk+20 (≈50–53 ms), knapp und reproduzierbar über der Grenze; Grenze nicht gelockert. `test_bedienung33316` – auf macOS/Tk 9.1 unregelmäßig (9 von 10 Läufen rot) Text-Rückfall der Symbole (`v`/`^`/`>`), weil die Abdeckungsprüfung für DejaVu Sans zeitweise scheitert; unter 3.50.0 auf dem Mac grün, Ursache offen. Kein vollständig grüner Vollmodus und kein Paket auf `80abbabf…`; frühere Ergebnisse bleiben `a4bfe4ed…`/`f3afb8fe…` zugeordnet.
