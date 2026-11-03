# CI-Nachlauf #247/#248 – Glide 3.50.2

Datierter Prüf- und Reparaturnachweis: Beginn 03.11.2026, lokaler Abschluss 04.11.2026. Ausgang `3e09079c`; keine Umdeutung früherer grüner oder roter Ergebnisse. Neue Umsetzung und tatsächliche Tests in [ergebnis.json](ergebnis.json).

## Rote Eingänge

[Glide-Prüfung #247](https://github.com/n05a-design/glide-to-do/actions/runs/41713292315), [PR-Prüfung #248](https://github.com/n05a-design/glide-to-do/actions/runs/41713568046) und [Mac-Paket #29](https://github.com/n05a-design/glide-to-do/actions/runs/41713292267), gleicher Quellcommit. Linux: `test_festlayout330` meldet Kopfknöpfe y=12 → 13 bei „Mein Tag“, feste äußere Kopfhöhe. Windows: `test_arbeitsmodi/gestaltung`, acht Seitenknöpfe nur bis y=141 statt 170 sichtbar, 44 andere Arbeitsmodi-Fälle grün. Mac: Paket gebaut, isolierte Startprobe Exit 1, „Gebündelte Schrift fehlt: Playfair Display SemiBold“; Sandbox-Positivkontrolle grün, externes Python korrekt blockiert. Rohlogs und Artefakt lokal erhalten.

## Ursachen und Reparaturen

- Kopf: Natürliche Höhe des zentrierten Titelblocks wechselt von 55 auf 54 px; beide Packstellen oben verankert. Keine Größen-/Abstandsgrenze gelockert.
- Seite: Beim `flush()` synchron neu aufgebauten Editor erhalten. Der äußere Durchlauf zerstörte noch die alte Instanz, verwarf die neue Referenz und erstellte einen zweiten Editor. Vorher exakt rot, nachher 206 Knopfprüfungen in fünf Konfigurationen grün; Test verlangt außerdem genau eine aktive Editorinstanz.
- Schriften: Windows/Linux melden separate SemiBold-Familien, AppKit die Stammfamilie. Mac fordert die unveränderten Original-PostScript-Schnitte `PlayfairDisplay-SemiBold` bzw. `Fraunces72pt-SemiBold` und deren Italic-Schnitte an. Echte Bold-Stammfamilien bleiben erhalten. `tkinter.Font` normalisiert Tupel sonst auf die Stammfamilie; die gemeinsame Schriftkopie erhält konkrete Familie, Größe, Neigung und Auszeichnung. Metrik und Messcache folgen dem angeforderten Schnitt. Paketprobe prüft Familien, sämtliche Stil-/Schnittkombinationen und die erhaltene Schriftanforderung.

Originaldateien/Lizenzen, öffentliche Schriftklassen und gespeicherte Auswahl unverändert. Tk-freie Katalogtests prüfen Plattformzuordnung, originalen name-ID-6-Eintrag der vier TTFs und das Kopieren von Schriftangaben. [Tk/AppKit-Quelle](https://github.com/tcltk/tk/blob/core-9-1-0/macosx/tkMacOSXFont.c).

## Prüf- und Liefergrenzen

Gezielte Windows/Tk-9.1-Prüfungen, Linux-Skalierungsgegenprobe und strenge Grundstufe werden im Abschluss erfasst. Keine native Mac-/Linux-Abnahme aus Windows-Proben abgeleitet. Kalibrierung ohne positive Basissuite weiterhin rot. Alter globaler lokaler Codex-Git-Objektbefund unverändert und keine Ursache dieser CI-Fehler. Neu gebaute Pakete und Remote-Matrix nur anhand tatsächlicher Läufe bewerten.


## Lokaler Abschluss

Sieben Bereichsprüfungen in [regression.json](regression.json) grün: feste Kopfzeile, Logo, Seiten, gesamte Aufgaben3380-Suite, Gestaltung, Werkzeugzeile und Beta350. Zusätzliche Rot-/Grünprobe mit Linux-Skalierung und Stil-Auswahl/Neustart grün. [Strenge Grundstufe](grundstufe.json) 19/19 grün: 242 Werkzeugtests (ein Skip), zweimal 1.127 Fachtests, Syntax, Analysen, Appstart, Fremdcode-, Datenschutz-, Ablage- und strenger Liefervergleich. Quelle/Python: 92 Code-Dateien und 171 Ressourcen bytegleich.

PR #60 inzwischen nach `main` `05922df6` gemergt; dieser Mergebaum ist identisch mit `3e09079c`. Alter Zweig gelöscht. Korrekturen werden auf `codex/glide-3.50.2-ci-korrekturen` geliefert. Dieser lokale Abschluss ersetzt nicht die neue native Remote-Matrix. Er enthält keine neue Gesamtabnahme und ändert weder Original-Rotbelege noch native Lieferpakete.
