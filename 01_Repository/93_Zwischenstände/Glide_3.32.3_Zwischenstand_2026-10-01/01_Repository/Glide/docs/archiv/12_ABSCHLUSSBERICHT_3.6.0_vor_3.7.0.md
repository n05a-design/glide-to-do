# Abschlussbericht Glide 3.6.0

Stand: 06.09.2026 · App-Version 3.6.0 · Aufgabendatenformat 11

## Freigabestand

Glide 3.6.0 ist als geprüfter lokaler Windows-Quellstand abgeschlossen. Der
vollständige Prüflauf vom 06.09.2026 meldete Exitcode 0 über 20 Schritte, ohne
fehlgeschlagene Stufe. Ausgenommen bleibt die bewusst manuelle Sicht- und
Plattformabnahme; sie ist kein versteckter Fehlerstatus.

## Inhalt des Releases

Die 3.6-Funktionen umfassen die ausgerichtete zweispaltige Navigation,
optische Startseitenkorrekturen, farbige Arten-/Listen-Auswahl, vollständige
Listen- und Ordneranlage, private TTF-Schriften, frei wählbare Datenablage mit
Sperrwarnung, geschütztes Umbenennen, Vorlagenverwaltung und additive
Teilbackups. Ergänzt sind Mondphase, Aktivitäts-Jahresraster, weitere
Personalisierung und abschaltbare Materialoptik mit Glaskanten.

Der vollständige Einzelabgleich jeder ursprünglichen Anforderung steht in
`docs/20_FEATURE_ABGLEICH_3.6.0.md`. Die Materialentscheidung einschließlich
der Grenze zu echtem selektivem Desktop-Blur steht in
`docs/19_GLASS_SURFACE_3.6.0.md`.

## Nachweise

- Automatisierter QA-Lauf: `tests/qa-3.6.0/abschluss/ergebnis.json`
- Hashes der startbaren Kopien, Schriften und Fixtures:
  `tests/qa-3.6.0/abschluss/dateien.sha256.json`
- reproduzierbare Leistungsaufnahme:
  `tests/qa-3.6.0/abschluss/leistung.json`
- Windows-Bilder: `tests/qa-3.6.0/abschluss/screenshots/`
- aktueller Übergabestand: `docs/17_UEBERGABE_3.6.0.md`

## Restliche Freigaben

Vor einer öffentlichen Auslieferung sind ein echter Start auf den vorgesehenen
Windows-Zielgeräten, Skalierungs-/Accessibility-Matrix, macOS-Abnahme,
Installer, Signierung, Storeidentität und Marken-/Lizenzfreigaben separat zu
entscheiden und zu prüfen. Diese Punkte ändern den abgeschlossenen lokalen
Funktionsstand nicht, sind aber Voraussetzungen einer Veröffentlichung.

Die früheren Abschlussberichte der Versionen 3.2 bis 3.5 bleiben im Archiv
erhalten. Ihre damaligen Zahlen und offenen Befunde sind historische Belege.
