# Nachabnahme 3.63.0 – 15.11.2026

Auftrag D85 / Plan §21.97 (bis zur Zusammenführung mit `main` 3.62.0 als D82 / §21.93 geführt): sechs Inhaberbefunde. Anzeigeprofile nach ausdrücklicher Klärung im Zeichen-/Pixel-Editor.

Gezielt geprüft:
- B09 und Erinnerungen vor Änderung als Baseline grün.
- `test_uiux_paket.py --fall nachabnahme363`: tatsächliche Spaltenkopfklicks auf-/absteigend, Hover-/Auswahlfarben bis zum Aktionsrand, größere Marker und vier Zeichenprofile ohne Dokumentänderung. `bedienpruefung.json`.
- B09 und B12-B13 grün; optische Bereichspfeilmitte -0,90 px innerhalb ±1 px.
- `test_reminders.py`: Sammelaufschub bis morgen 09:00 Uhr, Zukunftsterminerhalt, Aufgaben-/Tageshinweise gemeinsam, Badge 0, Speicherausfall/Rücksetzung, Schreibschutz und Neustart grün.
- `test_animation3400.py --fall frames` und `--fall geometrie` grün, jeweilige JSON-Berichte.
- 1.189 Unit-Tests grün.
- `grundstufe/ergebnis.json`: ursprünglicher Lauf mit Namensregel-Rot im letzten Schritt.
- `grundstufe-abschluss/ergebnis.json`: abschließende strenge Grundstufe grün, Exitcode 0, 19/19 Schritte ausgeführt; Quelle und Python-Lieferung bytegleich.

Sichtproben: Zeilenaktionen, Tabelle, Benachrichtigungen und Standard/Animation/Bilder pixeln/Erweitert. Windows / Python 3.15.1 / Tk 9.0.4, künstlicher Showcase, getrenntes `GLIDE_DATA_DIR`. Frühere rote Prüfversuche sind im zentralen QA-Bericht als Zwischenbefunde dokumentiert.

Keine vollständige native Plattform-/DPI-Matrix, Screenreader- oder Menschenabnahme; eigenständige Pakete und Git-Veröffentlichung offen. App bleibt 3.63.0, Aufgabenformat 26.


Abschlusslauf: `grundstufe/ergebnis.json` besteht die ersten 18 Schritte und scheitert ausschließlich an der Synchronisations-Namensregel für zwei reguläre Prüfberichte. Die eindeutig umbenannten Berichte bleiben erhalten. `grundstufe-abschluss/ergebnis.json` enthält den gesonderten finalen Nachlauf; die Profile normalisieren zusätzlich ungültige alte Einstellungswerte auf Standard.


Für die Git-Veröffentlichung wurden lokale Pfadpräfixe in den JSON-Nachweisen anonymisiert. Prüfstatus und Messwerte sind unverändert; die unveränderten Rohfassungen bleiben lokal außerhalb des versionierten Bestands erhalten.
