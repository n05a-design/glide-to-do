# Pixelanimation – Nachweisrahmen

Stand 13.10.2026 · Glide 3.40.0 · Aufgabenformat 24

Paket 5 setzt D18 im bestätigten Rahmen um: Bilder anlegen, duplizieren, löschen und umordnen; gemeinsame und eigene Dauer; unterbrechbare Vorschau; PNG-Spritesheet und PNG-Einzelbildfolge mit Zeitachse; Zwischenstände mit der ganzen Folge. Datenformat 24 mit Vorsicherung, Migration und schreibgeschütztem Altleser. Grundlage ist der private Codex-Entwurf; übernommen, an 3.39.1 angepasst und an den unten genannten Stellen korrigiert.

Gezielte Proben vor dem Einfrieren:

- [Pflichtsuite `test_animation3400`](gezielt.json): sieben Gruppen grün (Bilddialog, Speicherfehler, Vorschau, Export, Zwischenstand, 860 × 700 mit großer Schrift, Migration/Altleser), keine Callbackfehler.
- [Gegenprobe gegen 3.39.1](gegenprobe_3391.json) rot; die Vorversion kennt keine Bildfolgenaktionen.
- [Vier Defektgegenproben](defektgegenproben.json) an der neuen App, je passend rot: fehlendes Zurückrollen eines Strukturfehlers, Vorschau ohne Zeitgeberabbau, Ersetzen ohne Rückfrage, fehlende Format-24-Vorsicherung.
- 491 Unit-Tests grün, mit und ohne Systemzeitzonen; darunter 40 neue für `animation.py`, `animation_export.py`, Zwischenstände und die Formatbrücke.
- [Eigene Fenster in Hell und Dunkel tatsächlich betrachtet](fenster.json); PNGs nur lokal, künstliche Daten.
- [Auslaufende QA-Nachweise 3.34.0](aufbewahrung3340.json): fünf Dateien bytegleich zum Commit, auf den der QA-Bericht nun verweist.

Korrekturen gegenüber dem Entwurf:

- Der Test verglich die Dauern (Tupel) mit einer Liste und konnte so nie grün werden.
- Die Export-Probe exportierte zweimal dieselbe Folge; ein Ersetzen ohne Rückfrage blieb unerkannt. Sie ändert jetzt vorher die Dauer und verlangt die Rückfrage.
- Die Bildauswahl war eine native Combobox, die im dunklen Design hellgrau blieb; jetzt ein Glide-Knopf mit Menü.
- Die Bildfolgen-Tabelle folgt dem Muster der übrigen Dialogtabellen.
- Die Einzelbildfolge landet in einem lesbar benannten neuen Ordner statt in einem Zufallsnamen.
- Der Bildcache-Schlüssel validiert nicht bei jedem Aufruf die ganze Folge neu.

Der [erste eingefrorene Volllauf](mac_vorlauf.json) endete mit zwei Befunden: Der Pixelsymbol-Dialog nutzt den Zeichnungseditor und erhielt seit dem Entwurf die ganze Bildfolge statt eines Bildes, das Symbol ging verloren (`test_features330`); `test_seiten33318` änderte nur `drawing` am Bestand, das Backup war dadurch inkonsistent und der Import lehnte es zu Recht ab. Der Editor hat jetzt einen Einzelbildmodus ohne Bildfolgenknöpfe; der Test ändert beide Felder; der Format-20-Vergleich prüft die neue Bildfolge ausdrücklich. Die frische Vollprüfung ist unten belegt.

Mac-Abnahme und Lieferweg:

- [Frische eingefrorene Mac-Vollprüfung](mac_voll.json) am Kandidaten 2d002ad außerhalb OneDrive: Exit 0, 105 ausgeführt/zwei übersprungen; alle 1014 eingefrorenen Dateien danach unverändert. Der rebasierte Kandidat trägt denselben Code, dieselben Tests und Fixtures; hinzu kamen nur Dokumente und Belege des Lieferabschlusses 3.39.1.
- [Produktionsübernahme](produktionsuebernahme.json), [206 Lieferdateien](lieferung.json), [114 Bundle-Dateien und beide Signaturen](bundle.json). 3.39.1 liegt im Archiv.

Die erste native Matrix [38365723954](https://github.com/n05a-design/glide-to-do/actions/runs/38365723954) endete rot ([Auswertung](native_38365723954.json)), beide Befunde am Prüfstand: Unter Linux prüfte `test_animation3400` den Knopf „Duplizieren“, bevor die Knopfzeile unter Xvfb angeordnet war; unter Windows verglich `test_animation_export` den Sicherungspfad textlich, während Windows den Temp-Ordner einmal in Kurzform nennt. Die Suite wartet jetzt höchstens 3 s auf die Anordnung, der Unit-Test vergleicht aufgelöste Pfade; ein tatsächlich nie angeordneter Knopf macht die Suite weiterhin rot ([Prüfstandskorrektur](pruefstand_wartezeit.json)). App, Lieferdateien und Bundle unverändert.

**Lieferabschluss 13.10.2026:** Native Matrix [38380786813](https://github.com/n05a-design/glide-to-do/actions/runs/38380786813) am Kandidaten 3e50e6e grün – [Linux](linux_voll.json) 106 und [Windows](windows_voll.json) 106 ausgeführt, je eine menschliche Sichtprüfung übersprungen, [18 Defektgegenproben](linux_defektgegenproben.json) passend rot, [Windows-Desktop](windows_desktop.json). [Lieferabschluss](lieferabschluss.json): 206 Liefer- und 114 Bundle-Dateien unverändert, Signaturen erneut grün. [Strenge Kandidat-CI](grundstufe_kandidat.json) grün.
Tatsächliche menschliche Bedienung bleibt ein gesondertes Abnahmetor.
