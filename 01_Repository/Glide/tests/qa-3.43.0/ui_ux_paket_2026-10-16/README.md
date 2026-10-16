# UI-/UX-Paket 3.43.0 – Lieferung und Prüfung

Stand 16.10.2026 · Glide 3.43.0 · Datenformat 25 · Apphash `2feea1eef7d55fc9b629757bbc4e8ed5ec41ce00da8840ed46bdd96d31eca936`

Auftrag: [UI-/UX-Feature-Paket](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md) vom 15.10.2026, nach D50 vorrangig vor Paket 8. Status je Kennung im [Entwicklungsplan §17](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#17-ui-ux-feature-paket-aus-nutzerbeobachtungen-15102026), Regeln in [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md). Maschinenlesbar: [ergebnis.json](ergebnis.json). Alle Prüfungen mit künstlichen Daten und temporärem `GLIDE_DATA_DIR`; Rohprotokolle und Fensteraufnahmen bleiben lokal (die Showcase-Aufnahmen zeigen Fremdbilder, I9).

## Gezielte Prüfungen (Windows 11, Python 3.14.7, Tk 9.0.4)

| Prüfung | Ergebnis |
|---|---|
| Pflichtsuite `test_uiux_paket.py` (16 Fälle, B01–B19, [Bericht](pflichtsuite_3.43.0.json)) | 16/16 grün |
| Rote Gegenprobe derselben Suite gegen den gelieferten 3.42.0-Quellbaum (`git archive 05483a8`, [Bericht](gegenprobe_3.42.0.json)) | 16/16 rot, jeweils mit dem Ursprungsfehler (siehe unten) |
| Fachlogik-Unit-Tests | 711 grün (neu: Glyphenmetrik, Hinweisschalter, Kacheln/Gismo, Neuerungsverlauf, Symbolregel) |
| Werkzeugtests einschließlich `test_design_richtlinien.py` | 150 grün |
| Regressionslauf aller Integrationssuiten der Arbeitskopie | nach Anpassung der Suiten, die das bewusst geänderte Verhalten festschrieben (Gismo-Knöpfe, „?“, Standardkacheln, Blockleiste, Lupe, Schrift der nächsten Aufgabe), alle grün; ein Befund im Code behoben (Kopfhöhe, siehe unten) |
| Linux-Defektmuster der CI (`linux_gegenproben.py`) | alle 18 Muster passen weiterhin auf den Quellstand |

**Vorher → nachher, gemessen im selben Kontext (Showcase-Daten, gleiche Fenstergröße):**

| Kennung | Messung | 3.42.0 | 3.43.0 |
|---|---|---|---|
| B01 | Scrolllage nach „Gelesen“ | 0,27 | 0,00 |
| B02 | Abstand „Startseite anpassen“ zur linken Rasterkante | 778 px | 0 px |
| B05 | Logo-Unterkante zur Grundlinie der Unterzeile | +6 px | −1 px |
| B07 | Mittellinie Windows-Menüs zu Kopfsymbolen | 10 px | 0 px |
| B08 | Überschrift zu Meldungstext (Fehlerprotokoll) | 3 px | 0 px |
| B09 | Bereichspfeil zur Großbuchstabenmitte | +1,5 px | −0,3 px |
| B11 | Datumsspalte in „Labels“ | 281 px | 177 px |
| B16 | größter Schritt eines Mausradrasters über einem Bild | 378–389 px | 30 px |

**Befund während der Prüfung behoben:** Mit 42 px hohen Kopfknöpfen in der Titelzeile (B07) wuchs der Kopf um 4 px; `test_aufgaben3380` meldete daraufhin die Bedienfläche in der Liste bei 1280 × 800 mit 121 statt höchstens 120 px (15 %). Kopfknöpfe und Windows-Menüs haben jetzt die Höhe der Titelzeile (38 px); die Bedienfläche hält die Grenze wieder ein, ohne das Kriterium zu ändern.

**A01-Probe:** ohne Seitenleiste bei 860 × 700 bis 420 × 520 keine überlappenden Knöpfe; unter 560 px Breite verschwinden Titel und zwei Windows-Menüs – Grundlage der Empfehlung „eigener Kompaktmodus“ im Entwicklungsplan §17.1.

## Eingefrorene Vollprüfung (Windows)

`pruefen.py --modus voll --timeout 600` auf einer Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `build`, `skills-main` und ohne die lokalen Nutzerbilder): **109 Schritte ausgeführt, alle 92 Integrationssuiten grün** (einschließlich `test_uiux_paket` und `test_ui_followup36`), Unit-Tests, Showcase, Beispiel-/Releasedaten-Abgleich, Bildschirmaufnahmen und vier von fünf Analysen grün; Sichtprüfung wie immer der Person vorbehalten. **Einziger roter Schritt:** die Standprüfung. Die Links der Bildreferenzen zeigten in den bewusst nicht versionierten Ordner `bilder/` (auf GitHub wären sie tot), dazu ein Planlink auf einen falschen Nachweisordner und die Suitenzahl in `tests/README.md`. Als reine Dokumentkorrektur behoben (Bildpfade als Text, Link und Zahl korrigiert); die Standprüfung ist danach grün. Ein ausführbarer Pfad hat sich nicht geändert; nur die Fehlermeldungen zweier Gegenprobenfälle der Pflichtsuite wurden danach präzisiert.

`test_ui_followup36` hing in der OneDrive-Arbeitskopie in `root.update()` – auch am unveränderten Stand `27bac83` –, lief in der eingefrorenen Kopie aber grün durch: ein Umgebungseffekt des OneDrive-Pfads, kein Befund dieses Pakets.

## Lieferabgleich

- `versionswechsel.py 3.43.0 16.10.2026`: Fixtures, Showcase, Vorlagen, Releaseplanung und Standangaben neu; Ablage auf sieben Versionen gekürzt (3.37.0 entfällt, Verweise auf `0e7b358` festgesetzt).
- `abgleich_07.py`: 67 Code- und 146 Ressourcendateien in `07_Python-Versionen` bytegleich, 3.42.0 ins Archiv.
- `showcase_abgleich.py`: Import, ID-Verweise, Dokumentarten, Bilder, Pinnwände, Undo, Vorlagen, Export und Neustart geprüft; sechs Dateien nach `05_Probelisten_Testdaten/Showcase`.
- Das Showcase-Werkzeug schreibt seine Vorlagendatei und das Manifest jetzt mit LF; unter Windows stimmten Prüfsumme und eingecheckte Bytes sonst nicht überein.

## Offen

- **Native Linux-/Windows-Vollmatrix** und **Windows-Paketlauf** der GitHub-Prüfung zum Pull Request: Ergebnis im [QA-Bericht](../../../docs/07_QA_BERICHT.md).
- **macOS-Bundle und Mac-Vollprüfung:** auf Windows nicht baubar bzw. ausführbar; `packaging/macos/baue_app.py` und die eingefrorene Mac-Vollprüfung auf dem Referenz-Mac stehen aus. Bundle und eigenständige Pakete tragen bis dahin 3.42.0.
- **Menschenabnahme:** Sicht, DPI 100–200 %, Trackpad, große Schrift, alle Designs sowie Screenreader nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#ui-ux-paket-15102026-b01b19).
- **Produktentscheidungen** E-U1–E-U4 (A01–A03, Pfadtrenner) beim Inhaber.
