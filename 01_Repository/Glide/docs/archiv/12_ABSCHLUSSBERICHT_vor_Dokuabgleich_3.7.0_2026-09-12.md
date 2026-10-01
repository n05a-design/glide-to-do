# Abschlussbericht Glide 3.7.0

Stand: 07.09.2026 · App-Version 3.7.0 · Aufgabendatenformat 12

## Freigabestand

Glide 3.7.0 ist als geprüfter lokaler Windows-Quellstand abgeschlossen. Der
vollständige Prüflauf vom 07.09.2026 meldete Exitcode 0 über alle zehn
Prüfsuiten und die zugehörigen Daten-, Fixture-, Release- und Screenshot-
Schritte. Die manuelle Plattformabnahme bleibt eine getrennte Freigabe.

## Inhalt des Releases

3.7.0 ergänzt den 3.6-Stand um die scroll- und breitenstabile
Listen-/Ordner-Kachelansicht, Bearbeiten aus Kacheln, zweispaltige Details für
Listen und Ordner, Containeranhänge, die Schema-12-Migration mit
Originalkopie, konsistente Aktionsleisten, die robuste Labelauswahl und den
Datum-/Zahl-Hover im Jahresraster. Die Startseite und Vorlagenansicht behalten
ihre bisherigen Funktionen und verhalten sich auch bei schmalen Fenstern
kontrolliert.

Der vollständige Einzelabgleich jeder Anforderung steht in
`docs/25_FEATURE_ABGLEICH_3.7.0.md`; die technische Versionsübersicht steht in
`docs/24_VERSION_3.7.0.md`.

## Nachweise

- Automatisierter QA-Lauf: `tests/qa-3.7.0/automatisch/ergebnis.json`
- Kontroll- und Hashnachweis: `tests/qa-3.7.0/abschluss-kontrolle.json`
- Windows-Bilder: `tests/qa-3.7.0/oberflaeche/`
- Startbare Kopie: `../../07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.7.0.pyw`
- Ausführlicher Word-Bericht: `../../10_Dokumentation/Glide_3.7.0_Auftragsabgleich_QA_Leistung.docx`

## Restliche Freigaben

Vor einer öffentlichen Auslieferung sind ein echter Start auf den vorgesehenen
Windows-Zielgeräten, Skalierungs-/Accessibility-Matrix, macOS-Abnahme,
Installer, Signierung, Storeidentität und Marken-/Lizenzfreigaben separat zu
entscheiden und zu prüfen. Diese Punkte ändern den abgeschlossenen lokalen
Funktionsstand nicht, sind aber Voraussetzungen einer Veröffentlichung.

Die früheren Abschlussberichte bleiben als historische Belege im Archiv.

## Dokumentationsnachtrag vom 08.09.2026

Die aktuellen Einstiege, Zusatzunterlagen und der vollständige Funktionsabgleich
sind auf 3.7.0 fortgeschrieben. Der Word-Bericht ist inhaltlich aktualisiert;
seine Layoutprüfung bleibt wegen des fehlenden LibreOffice-Renderers offen.
Historische 3.6-Leistungswerte bleiben ausdrücklich als solche gekennzeichnet.
