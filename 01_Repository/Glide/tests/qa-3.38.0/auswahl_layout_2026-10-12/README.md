# Aufgabenoberfläche und Windows-Kopfzeile – Lieferung 3.38.0

Stand 12.10.2026 · Glide 3.38.0 · Aufgabenformat 23 · geliefert; Menschenabnahme getrennt offen

Aktueller App-SHA-256: `bcdbc4da2197aadaffbe65cd57054c68b93db4d1aedcb9cbeb16c2204bd8ef41`.
Root, 07 und Bundle tragen diesen Stand. Die vollständige native Matrix am Kandidat a0288b7 ist grün.
Die strenge lokale Liefer-CI ist grün; die Tempoabweichung wurde als D48 angenommen.

## Aktueller Prüfstand

- [Mac-Vollprüfung](mac_titelzeile.json) Exit 0: 102 ausgeführt/zwei übersprungen,
  85 Integrationssuiten/294 Unit-Tests, alle 899 eingefrorenen Dateien unverändert.
- [Bedienflächen](bedienflaechen_titelzeile.json): sechs Hauptansichten,
  Referenzgröße 1280 × 800, zusätzlich 1280 × 840, 860 × 700 und große Schrift.
  Die 15-Prozent-Grenze bei Referenzgröße bleibt unverändert.
- [Vier Vorversionsgegenproben](vorversionsgegenproben.json) gegen den gelieferten
  3.37.0-Commit passend rot; dieselbe aktuelle Pflichtsuite wie im positiven Volllauf.
- [Bewegung](bewegung_titelzeile.json): 215 tatsächliche Abschlüsse, höchstens
  106,20 ms bei Ziel ≤ 150 ms. Abschaltoption und Abbruch schneller Folgen geprüft.
- [Sechs eigene Fenster](fenster_titelzeile.json) in Hell/Dunkel, Referenz-/Mindestgröße
  und großer Schrift neu aufgenommen und tatsächlich betrachtet. Lange Titel
  bleiben in begrenzten Zeilenspalten angeschnitten; der Inhaltsinspektor zeigt
  den vollständigen Titel. Menschliche Bedienung und DPI-Abnahme bleiben getrennt.
- [Gezielte native Windows-Prüfung](windows_titelzeile.json) am Commit 6992ce7,
  [Lauf 38220307993](https://github.com/n05a-design/glide-to-do/actions/runs/38220307993),
  grün: 36 Layoutkombinationen und alle drei zuvor roten Textsuiten. Diese gezielte
  Wiederholung ersetzt keine vollständige native Matrix.
- [Native Linux-Vollprüfung](linux_titelzeile.json) am Kandidat a0288b7 grün,
  103 ausgeführt/eine menschliche Sichtprüfung übersprungen. Alle
  [18 Defektgegenproben](linux_defektgegenproben_titelzeile.json) passend rot.
  [Windows-Vollprüfung](windows_voll_titelzeile.json) desselben [Laufs 38272561080](https://github.com/n05a-design/glide-to-do/actions/runs/38272561080)
  ebenfalls Exit 0, 103 ausgeführt/eine menschliche Sichtprüfung übersprungen,
  85 Integrationssuiten/294 Unit-Tests; [Referenzdesktop](windows_desktop_titelzeile.json)
  1920 × 1080, Python 3.14.7/Tk 9.0.4. [Native Quell-/Jobnachweise](native_titelzeile.json).
- [07/Showcase](lieferung_titelzeile.json): 42 Code-/141 Ressourcen-/sechs
  Showcase-Dateien bytegleich; [Bundle](bundle_titelzeile.json) mit 42 Code-/55
  Mac-Ressourcen gleich Quelle, Signatur im Bauordner und auf Rückkopie grün.
- [Serieller Tempoabschluss](tempo_abschluss.json): fünf direkte Prozesse × 40
  Wiederholungen nach Ende der vorigen Matrix. Einstellungen warm 146,85 ms
  Median/179,59 ms p95; erste Anzeige p95 203,90 ms. Startseite kalt p95 272,71 ms,
  warm 73,52/79,67 ms. Einstellungs-p95 verfehlte D47. Der Inhaber nahm am 12.10.2026 als D48
  ausdrücklich warm Median ≤ 150 ms/p95 ≤ 190 ms an; erste Anzeige ≤ 250 ms,
  Funktionsumfang unverändert. Wortlaut „A – Median 150 ms / p95 190 ms akzeptieren
  (Empfehlung)“. Damit erfüllt die Abschlussreihe D46/D48.

Die Windows-Menüs liegen innerhalb der Titelzeile; die Statuszeile darunter
behält ihre Breite. Die Titelmessung berücksichtigt die Menübreite. Vier
beschriftete Menüs und Alt-Kürzel bleiben erhalten. [Lokaler Menüpfad](menues_titelzeile_mac.json)
und [Textregressionen](titelzeilen_mac.json) sind zusätzlich auf dem Mac geprüft;
die unveränderte Titelprüfung ist am Vorgänger passend rot.

Die [strenge Liefer-Grundstufe](liefergrundstufe_titelzeile.json) ist grün: 17 Schritte
ausgeführt, 07 bytegleich; ein bekannter lokaler SSL-Zertifikathinweis beim
Abruf des Fremdcode-Originalpakets.

[Erneuter Lieferabschluss](lieferabschluss_titelzeile.json): 189 Liefer- und 97 Bundle-Dateien nach
der nativen Matrix unverändert. Gesamtes lokales Bundle erneut mit Bauordner
und frischer Rückkopie bytegleich, beide Signaturen grün. Die 899 Freeze-Dateien
waren nach der Mac-Vollprüfung unverändert; der anschließende vorgeschriebene
Lieferabgleich zog ausschließlich die 07-Hauptdatei auf die geprüfte Quelle nach.

## Frühere Kandidaten und Ursache

Der Langtextumbruch am Hash 49ca48aa verlor beim Größenwechsel eine Mehrfachauswahl.
Der korrigierte reine Layoutweg bewahrt Auswahl, Zeilenfokus und Bildlauf; ein
Bereichswechsel beendet den alten Auftrag. [Gezielte Proben](gezielte_proben.json)
und die entsprechende Defektkontrolle halten den Befund fest.

Am Vorgängerhash 8cda250c bestand die [Mac-Vollprüfung](mac-voll.json) mit 885 Dateien.
Die [native Matrix 38213392543](https://github.com/n05a-design/glide-to-do/actions/runs/38213392543)
am Main-Merge 029b821 bestätigte [Linux](linux-voll.json) und [18 Defekte](linux-defektgegenproben.json).
[Windows](windows-vollbefunde.json) endete mit drei echten Kopftextanschnitten:
Mindestgröße, langer Titel und Planungsrückmeldung. Übrige 82 Suiten grün.
Die zuvor grüne [Layoutdiagnose](windows_layout.json) deckte diese Textfälle
nicht ab; sie sind jetzt Bestandteil der gezielten Windows-Wiederholung.

[Windows-Ursache](windows_ursache.json), [früherer lokaler Menüpfad](menues_mac.json),
[frühere Kandidat-Grundstufe](kandidat_grundstufe.json), [Grundstufe nach Main](grundstufe_nach_main.json),
[frühere Bewegung](bewegung.json), [frühere Fenster](fensterbeurteilung.json) und
[Tempo-Diagnose](tempo.json) behalten ihre ursprünglichen Hashes und Ergebnisse.
[Kopfzeilen-Kandidat-Grundstufe](kopfzeilen_grundstufe.json) grün mit damals noch
abweichendem 07-Hauptstand; keine strenge Lieferabnahme daraus ableiten.
Ältere 49ca48aa-Lieferbelege stehen [getrennt](../aufgaben_2026-10-11/README.md).
Rohprotokolle und eigene Fensterbilder bleiben außerhalb OneDrive und Git.

[Strenge CI zum Lieferabschluss](ci_lieferabschluss_titelzeile.json): Exit 0, 17 Schritte ausgeführt, ein bekannter lokaler SSL-Hinweis beim Fremdcodeabruf. Abschließender inhaltlicher Statusabgleich und Standprüfung grün; App-/Lieferhashes unverändert.
