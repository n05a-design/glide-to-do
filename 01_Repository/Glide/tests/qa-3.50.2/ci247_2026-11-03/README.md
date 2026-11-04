# CI-Nachlauf #247/#248 – Glide 3.50.2

Datierter Prüf- und Reparaturnachweis: Beginn 03.11.2026, lokaler Abschluss 04.11.2026. Ausgang `3e09079c`; keine Umdeutung früherer grüner oder roter Ergebnisse. Neue Umsetzung und tatsächliche Tests in [ergebnis.json](ergebnis.json).

## Rote Eingänge

[Glide-Prüfung #247](https://github.com/n05a-design/glide-to-do/actions/runs/41713292315), [PR-Prüfung #248](https://github.com/n05a-design/glide-to-do/actions/runs/41713568046) und [Mac-Paket #29](https://github.com/n05a-design/glide-to-do/actions/runs/41713292267), gleicher Quellcommit. Linux: `test_festlayout330` meldet Kopfknöpfe y=12 → 13 bei „Mein Tag“, feste äußere Kopfhöhe. Windows: `test_arbeitsmodi/gestaltung`, acht Seitenknöpfe nur bis y=141 statt 170 sichtbar, 44 andere Arbeitsmodi-Fälle grün. Mac: Paket gebaut, isolierte Startprobe Exit 1, „Gebündelte Schrift fehlt: Playfair Display SemiBold“; Sandbox-Positivkontrolle grün, externes Python korrekt blockiert. Rohlogs und Artefakt lokal erhalten.

## Ursachen und Reparaturen

- Kopf: Natürliche Höhe des zentrierten Titelblocks wechselt von 55 auf 54 px; beide Packstellen oben verankert. Keine Größen-/Abstandsgrenze gelockert.
- Seite: Beim `flush()` synchron neu aufgebauten Editor erhalten. Der äußere Durchlauf zerstörte noch die alte Instanz, verwarf die neue Referenz und erstellte einen zweiten Editor. Vorher exakt rot, nachher 206 Knopfprüfungen in fünf Konfigurationen grün; Test verlangt außerdem genau eine aktive Editorinstanz.
- Schriften: Windows meldet separate SemiBold-Familien; AppKit und Fontconfig melden bei konkreten Schnitten bzw. Aliasen die Stammfamilie. Mac fordert die unveränderten Original-PostScript-Schnitte `PlayfairDisplay-SemiBold` bzw. `Fraunces72pt-SemiBold` und deren Italic-Schnitte an. Echte Bold-Stammfamilien bleiben erhalten. `tkinter.Font` normalisiert Tupel sonst auf die Stammfamilie; die gemeinsame Schriftkopie erhält konkrete Familie, Größe, Neigung und Auszeichnung. Metrik und Messcache folgen dem angeforderten Schnitt. Paketprobe prüft Familien, sämtliche Stil-/Schnittkombinationen und die erhaltene Schriftanforderung.

Originaldateien/Lizenzen, öffentliche Schriftklassen und gespeicherte Auswahl unverändert. Tk-freie Katalogtests prüfen Plattformzuordnung, originalen name-ID-6-Eintrag der vier TTFs und das Kopieren von Schriftangaben. [Tk/AppKit-Quelle](https://github.com/tcltk/tk/blob/core-9-1-0/macosx/tkMacOSXFont.c).

## Prüf- und Liefergrenzen

Gezielte Windows/Tk-9.1-Prüfungen, Linux-Skalierungsgegenprobe und strenge Grundstufe werden im Abschluss erfasst. Keine native Mac-/Linux-Abnahme aus Windows-Proben abgeleitet. Kalibrierung ohne positive Basissuite weiterhin rot. Alter globaler lokaler Codex-Git-Objektbefund unverändert und keine Ursache dieser CI-Fehler. Neu gebaute Pakete und Remote-Matrix nur anhand tatsächlicher Läufe bewerten.


## Lokaler Abschluss

Sieben Bereichsprüfungen in [regression.json](regression.json) grün: feste Kopfzeile, Logo, Seiten, gesamte Aufgaben3380-Suite, Gestaltung, Werkzeugzeile und Beta350. Zusätzliche Rot-/Grünprobe mit Linux-Skalierung und Stil-Auswahl/Neustart grün. [Strenge Grundstufe](grundstufe.json) 19/19 grün: 242 Werkzeugtests (ein Skip), zweimal 1.127 Fachtests, Syntax, Analysen, Appstart, Fremdcode-, Datenschutz-, Ablage- und strenger Liefervergleich. Quelle/Python: 92 Code-Dateien und 171 Ressourcen bytegleich.

PR #60 inzwischen nach `main` `05922df6` gemergt; dieser Mergebaum ist identisch mit `3e09079c`. Alter Zweig gelöscht. Korrekturen werden auf `codex/glide-3.50.2-ci-korrekturen` geliefert. Dieser lokale Abschluss ersetzt nicht die neue native Remote-Matrix. Er enthält keine neue Gesamtabnahme und ändert weder Original-Rotbelege noch native Lieferpakete.

## Folgelauf #250 und zweite Reparatur, 04.11.2026

[Vollmatrix #250](https://github.com/n05a-design/glide-to-do/actions/runs/41735745303) auf `5f99b8fa` bleibt rot: Linux 42/45 Arbeitsmodi grün, drei Befunde (`kartenflaechen`, `schriftstile`, `eckenlabels`); Windows 44/45, nur `gestaltung` rot. Kopfkorrektur und Kalibrierung unter Linux bestanden. Die zweite Werkzeugzeile ist jetzt im Modus „kompakt_hell Seite“ abgeschnitten; der Schutz gegen doppelte Editorinstanzen besteht.

[Mac-Paket #31](https://github.com/n05a-design/glide-to-do/actions/runs/41735745447) auf demselben Commit ist grün: eigenständiger Start mit Tk 9.1, Sandbox-Positivkontrolle Exit 0, externes Python blockiert (71), Paketprozess Exit 0. TAR-SHA-256 `e081d2224caff036f74bfd395f3e58d7de5604bff71f0c42e9f950a3ed9ac9c1`; 491 Dateien, 30 Symlinks, Quellen unverändert, Ad-hoc-Signatur geprüft. Developer-ID/Notarisierung und menschliche Abnahme bleiben offen. CI-Artefakt ersetzt keine lokale Lieferdatei.

Weitere Korrekturen: Symbolcanvas ausdrücklich auf Kartenrolle registriert und nach Designwechsel neu gezeichnet. Fontconfig-SemiBold-Alias getrennt von gemeldeter Stammfamilie behandelt und beim Kopieren bewahrt. Einzeiligen Text anhand Inhalt/Breite statt rasterabhängiger Zeilenhöhe erkannt; feste Unterzeile schützt Normal/Bold/Italic vor Ein-Pixel-Wechseln. Umbruch der Seiten-/Zeichenwerkzeuge meldet den Höhenbedarf auch dann, wenn das begrenzte äußere Fenster selbst kein Configure-Ereignis erhält.

Der erste lokale Nachlauf der zweiten Reparatur war 44/45 grün, mit weiter abgeschnittener zweiter Werkzeugreihe bei großer Schrift im Kompaktmodus. Geometriespur: Werkzeuginhalt verlangt 72 px, fester Elternrahmen bleibt 40 px; ein nachträglicher Abgleich beseitigt den Befund. Meldung nach `reflow` allein kommt vor Abschluss der Tk-Geometriepropagation. Zusätzliches Configure der fertig angeordneten Reihen liefert den korrekten Zeitpunkt. Derselbe unveränderte Fall danach 132 Knopfprüfungen grün. Der rote Vorlauf bleibt lokal erhalten.

Ein erster zusätzlicher lokaler 45er-Lauf war 44/45 grün: Beta350 hielt nach Fokuswechsel eine inzwischen ersetzte Editorinstanz. Diagnoselauf 45/45 grün; der Test holt nach der speichernden Fokusänderung nun die aktuelle Instanz. Dokument-, Datei-, Undo-, Esc- und Schreibschutzprüfungen bleiben erhalten. Der ursprüngliche rote lokale Befund wird dadurch nicht nachträglich grün.

Der neue manuelle Bereich `ui-nachlauf` prüft unverändert alle 45 Fälle unter Linux/Xvfb (gleiche 1400×1100-Referenzfläche) und Windows (1920×1080). Eigene Laufgruppe verhindert Abbruch der Push-Vollmatrix. Positive Kalibrierungsbasis und Paketfreigabe werden allein im normalen Volllauf bewertet; der UI-Nachlauf macht daraus keine grüne Teilfreigabe.

**Gezielter lokaler Abschluss der zweiten Reparatur:** [Folgelaufnachweis](folgelauf250.json), sechs Bereichsprüfungen und der reparierte Kompaktfall grün; acht Schriftkatalogtests grün. [Strenge Grundstufe](grundstufe250.json) 19/19 grün, 244 Werkzeugtests (ein Skip), zweimal 1.128 Fachtests. Quelle/Python 92 Code-Dateien und 171 Ressourcen bytegleich. Neue native Nachläufe werden auf dem gepushten Commit bewertet; diese Aussage dokumentiert den Stand vor dem Push.
