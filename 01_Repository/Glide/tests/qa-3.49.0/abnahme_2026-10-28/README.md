# Abnahmeprüfung bis Glide 3.49.0

Stand 28.10.2026 · datierter Prüfbeleg · Aufgabenformat 26 · Bericht und Dokumentverweise am 29.10.2026 abgeschlossen

## Ergebnis

Nicht alle begonnenen Arbeiten sind abgeschlossen. Die 52 Abnahmeeinheiten (fachlich überlappend) und B01–B22 werden in den beiden finalen Berichtsformaten bewertet. Empfohlen wird eine ausdrücklich begrenzte technische Teilabnahme; keine Gesamtabnahme oder Releasefreigabe.

- [Prüfbericht PDF](Glide_Abnahmebericht_3.49.0_2026-10-28.pdf)
- [Bearbeitbarer Prüfbericht DOCX](Glide_Abnahmebericht_3.49.0_2026-10-28.docx)
- [Paketmatrix](paketmatrix.json), [Planregister](planregister.json), [Codeinventar](codeinventar.json)
- [Neue Prüfbilanz](testergebnis.json), [Originaler FP-01-Befund](lauf_wiederholen.json), [begrenzte Ursachenprobe](diagnose_wiederholen.json)
- [Tatsächlicher Lieferstand](lieferstand.json), [Prüfkopie und Quellhashes](eingefroren.json)

## Tatsächlich neu geprüft

Eingefrorene lokale Kopie mit isolierten Prozessdaten. CI-Grundstufe bestanden: 220 Werkzeugtests (ein Skip), zweimal 1060 Fachtests, fünf Analysen, Startprobe sowie formale/Fremdcode-/Datenschutz-/Ablagekontrollen. FP-01-Suite 8/9, Gültigkeit rot; darauf Stop, zwölf nachfolgende Suiten nicht ausgeführt. Originalsuite und Assertions unverändert. Die begrenzte Diagnose reproduziert den Fehler und zeigt einen erfolgreichen Lauf mit sauberem Sitzungsabschluss ausschließlich im Prüfharness. Das ersetzt keine Reparatur oder grüne Originalsuite.

Beide nativen 3.45.0-Archive SHA-256-gleich zum historischen Lieferbeleg; eingebettete Versionen 3.45.0, Python-Lieferung 3.47.0/Format 26. Keine neue native Signatur-/Startprüfung. Gezielte Funktionsbelege des vorherigen Nachlaufs haben denselben Apphash wie die eingefrorene Quelle.

## Grenzen und Darstellung

P8/4.0, WA-09/32/36–42, WA-41-Ursachen, vollständige aktuelle Lieferung und native/Menschenabnahmen sind im Bericht mit ihrer jeweiligen Grenze benannt. Nicht gewählte Optionen werden nicht als unfertige Features gezählt. Vier alte Modulverweise und einzelne Versions-/Lieferangaben sind im Eingangsstand widersprüchlich.

Der standardmäßige DOCX-Renderer scheiterte am hier nicht vorhandenen LibreOffice. Export erfolgte stattdessen mit einer eigenen unsichtbaren Word-Instanz, Quelle schreibgeschützt; finale PDF mit der PDF/A-1-Exportoption. Alle dreizehn finalen Seiten sind mit PDFium gerendert und gesichtet. Wiederholte Tabellenköpfe wurden zusätzlich anhand von Text, Bildpixeln und vergrößerten Ausschnitten kontrolliert, nachdem die Bildvorschau wiederholte Bereiche teilweise nicht anzeigte. Keine fremden Word-Dokumente geöffnet oder verändert. Rohlogs/Prüfdaten bleiben lokal; JSON-Berichtskopien pseudonymisieren Benutzerpfade.

Anwendungscode, Nutzerdaten und Lieferartefakte wurden durch dieses Audit nicht verändert. Kurze Auditverweise sind in QA-Bericht, Übergabe, Arbeitsrichtung und Entwicklungsplan ergänzt; der eingefrorene Eingangsstand bleibt im Manifest erhalten. Kein Commit/Push oder neue Version. Die abschließenden Hash-, Link-, Stand- und Dokumentkontrollen stehen in `abschluss.json`.
