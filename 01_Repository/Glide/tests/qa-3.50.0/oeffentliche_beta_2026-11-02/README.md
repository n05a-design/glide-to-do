# Glide 3.50.0 – Erster öffentlicher Stand

Stand 02.11.2026 · Glide 3.50.0 · öffentliche erste Beta · Aufgabenformat 26

## Prüfungen und Lieferung

Arbeitsnachweis der laufenden Fertigstellung. Endmatrix und Artefakthashes werden erst nach tatsächlichem Abschluss eingetragen; diese Datei behauptet noch keine Gesamtfertigstellung.

- Ausgangsbaseline: 1.105 Fachtests, ein Skip, grün.
- Neue Fachlogik: Block-/Format-/Unicode-/Metadatenerhalt und Hintergrundauswahl grün.
- Native Mac-Bereichssuite: 39 Arbeitsmodi-/Nebenansichts-/Fokus-/Blockfälle grün (zunächst Tk 9.0.3).
- Native Mac-Geometrie mit Tk 9.1.0: 1.084 Knopfprüfungen über sieben Ansichten und fünf Dialoge, Mindestgröße/große Schrift/Hinweise an/aus grün.
- Werkzeugtests: 238, drei Skips, grün.
- Erster eingefrorener Mac-Volllauf stoppte korrekt an der überholten Erwartung `sidebar_shell.master is main_area`; Test auf neue volle Seitenleistenhöhe aktualisiert, Rotbeleg lokal erhalten.
- Eigenständiges Mac-arm64-Paket mit Python 3.14.5 / Tcl/Tk 9.1.0 gebaut; Quell-/Lizenzvergleich und isolierter Start mit gesperrtem externen Python grün. Tatsächliche Lieferung und abschließende Matrix folgen.

## Prüfgrenzen

Menschliche Prüfung durch den Inhaber folgt anschließend. Screenreader ist bis Bedarf zurückgestellt. Der datierte Windows-Nachweis nebenan gilt für den vorherigen Apphash; der neue Endstand wird separat geprüft. Historische WA-41A/B-Befunde bleiben erhalten und werden nicht durch grüne Gegenläufe als ursächlich behoben bezeichnet.
