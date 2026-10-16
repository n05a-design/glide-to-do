# UI-/UX-Paket 3.43.0 – Lieferung und Prüfung

Stand 16.10.2026 · Glide 3.43.0 · Datenformat 25 · Apphash `379e97e32e3cc5e52eeb104ec23937df28081b45bd0e63582d5065cd61a2b172`

Auftrag: [UI-/UX-Feature-Paket](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md) vom 15.10.2026, nach D50 vorrangig vor Paket 8. Status je Kennung im [Entwicklungsplan §17](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#17-ui-ux-feature-paket-aus-nutzerbeobachtungen-15102026), Regeln in [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md). Maschinenlesbar: [ergebnis.json](ergebnis.json). Alle Prüfungen mit künstlichen Daten und temporärem `GLIDE_DATA_DIR`; Rohprotokolle und Fensteraufnahmen bleiben lokal (die Showcase-Aufnahmen zeigen Fremdbilder, I9).

## Gezielte Prüfungen (Windows 11, Python 3.14.7, Tk 9.0.4)

| Prüfung | Ergebnis |
|---|---|
| Pflichtsuite `test_uiux_paket.py` (17 Fälle, B01–B19 einschließlich appweiter Knopfschutzprüfung, [Bericht](pflichtsuite_3.43.0.json)) | 17/17 grün |
| Rote Gegenprobe derselben Suite gegen den gelieferten 3.42.0-Quellbaum (`git archive 05483a8`, [Bericht](gegenprobe_3.42.0.json)) | 17/17 rot, jeweils mit dem Ursprungsfehler (siehe unten) |
| Fachlogik-Unit-Tests | 711 grün (neu: Glyphenmetrik, Hinweisschalter, Kacheln/Gismo, Neuerungsverlauf, Symbolregel) |
| Werkzeugtests einschließlich `test_design_richtlinien.py` | 150 grün |
| Stand-, Link- und Ablageprüfung (`standpruefung.py`, `ablagegroesse.py`) | grün; 64 aktive Dokumente, Archive und Nachweise nur der sieben neuesten Versionen |
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
| B09 | Pfadtrenner „›“ in der Startseitenkachel „Pinnwände“ zur Großbuchstabenmitte | +0,95 px | −0,05 px |
| B15 | Knöpfe mit Überlagerung oder Beschnitt (7 Ansichten, 5 Dialoge, 2 Größen, 2 Schriftgrößen, Hinweise an/aus) | 10 Befunde (u. a. „Zur Startseite“ vom Papierkorbtext überdeckt, „Nur offene“ abgeschnitten) | 0 |
| B11 | Datumsspalte in „Labels“ | 281 px | 177 px |
| B16 | größter Schritt eines Mausradrasters über einem Bild | 378–389 px | 30 px |

**Befund während der Prüfung behoben:** Mit 42 px hohen Kopfknöpfen in der Titelzeile (B07) wuchs der Kopf um 4 px; `test_aufgaben3380` meldete daraufhin die Bedienfläche in der Liste bei 1280 × 800 mit 121 statt höchstens 120 px (15 %). Kopfknöpfe und Windows-Menüs haben jetzt die Höhe der Titelzeile (38 px); die Bedienfläche hält die Grenze wieder ein, ohne das Kriterium zu ändern.

**A01-Probe:** ohne Seitenleiste bei 860 × 700 bis 420 × 520 keine überlappenden Knöpfe; unter 560 px Breite verschwinden Titel und zwei Windows-Menüs – Grundlage der Empfehlung „eigener Kompaktmodus“ im Entwicklungsplan §17.1.

## Eingefrorene Vollprüfung (Windows)

`pruefen.py --modus voll --timeout 600` auf einer Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `build`, `skills-main` und ohne die lokalen Nutzerbilder), Endstand mit Apphash `a7b1df81`: **110 Schritte ausgeführt, kein roter Schritt** – alle 92 Integrationssuiten (einschließlich `test_uiux_paket` und `test_ui_followup36`), 711 Unit-Tests, Showcase, Beispiel-/Releasedaten-Abgleich, Bildschirmaufnahmen und alle fünf Analysen einschließlich Standprüfung grün; übersprungen nur die Sichtprüfung, die wie immer einer Person vorbehalten ist.

Vorlauf am selben Tag (Apphash `2feea1ee`, vor der Punkt-für-Punkt-Prüfung unten): 109 Schritte, einziger roter Schritt die Standprüfung wegen Bildlinks in den nicht versionierten Ordner `bilder/`, eines Planlinks und einer Suitenzahl – als Dokumentkorrektur behoben. Danach wurden die Lücken aus der Punktprüfung geschlossen (Pfadtrenner, Knopfreihe des Spaltenboards, Bedienhinweis, Handbuch); deshalb der zweite, maßgebliche Volllauf oben.

`test_ui_followup36` hing in der OneDrive-Arbeitskopie in `root.update()` – auch am unveränderten Stand `27bac83` –, läuft in der eingefrorenen Kopie aber grün: ein Umgebungseffekt des OneDrive-Pfads, kein Befund dieses Pakets.

## Prüfung aller Punkte des Originalauftrags

Am 16.10.2026 auf Wunsch des Inhabers jeden Punkt des [Originalauftrags](../../../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/AUFTRAG.md) gegen Code, Prüfungen und Dokumente abgeglichen. Dabei gefundene Lücken wurden vor der Lieferung geschlossen (letzte Spalte). „Automatisch“ heißt: echte Tk-Wege mit künstlichen Daten unter Windows 11/Tk 9.0.4; die menschliche Sicht-, DPI-, Mac- und Screenreaderabnahme bleibt für alle Punkte offen.

| Punkt | Auftrag (gekürzt) | Umgesetzt | Automatisch geprüft | Bei dieser Prüfung nachgezogen |
|---|---|---|---|---|
| A.1 | Kompaktmodus, kleinere Mindestgröße? | Untersucht mit Probe an echten Inhalten, Empfehlung „Kompaktmodus als Folgepaket“ ([Plan §17.1](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#171-a01--kompaktmodus-und-kleinere-mindestgröße)) | Messprobe 860 × 700 bis 420 × 520 | – ; Auswahl E-U1 beim Inhaber |
| A.2 | Zweites Fenster oder geteilte Ansicht? | Optionen A–D mit Aufwand, Risiko und Abnahmekriterien ([§17.2](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#172-a02--zwei-inhalte-gleichzeitig)) | – | – ; Auswahl E-U2 beim Inhaber |
| A.3 | Notion-Komponenten für Glide? | Priorisierte Tabelle in [Markt und Vorbilder §10](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md#10-notion-muster-für-glide-a03-15102026) | – | – ; Auswahl E-U3 beim Inhaber |
| B.1 | Nach „Gelesen“ an den Seitenanfang, in die Prüfung | ja | b01 (vorher 0,27) | – |
| B.2 | „Startseite anpassen“ links ausrichten | ja | b02 bei drei Breiten | – |
| B.3 | Gismo nicht umbenennen, Spielereien nicht abschaltbar; Ausblenden über die Startseiten-Einstellungen | ja; Kachel „Gismo – Begleiter“ unter „Startseite anpassen“ und „Weitere Einstellungen …“ | b03, Unit-Tests | – |
| B.4 | Galeriebilder als eigene Vorschau auf der Startseite | ja, Kachel „Galeriebilder“ | b04 | Handbucheintrag „Startseite“ ergänzt |
| B.5 | Logo niedriger | ja | b05 (vorher 6 px zu tief) | – |
| B.6 | Datum und „?“ entfernen, Hinweise in den Einstellungen schalten | ja | b06_b15, Unit-Tests | Bedienhinweis des Spaltenboards folgt jetzt ebenfalls dem Schalter; Handbucheintrag „Bedienhinweise“; toter Rest des „?“-Knopfs entfernt |
| B.7 | Menüs und Kopfsymbole auf gleicher Höhe? (prüfen) | geprüft: 10 px Versatz, behoben | b07 | – |
| B.8 | Fehlerprotokoll: gleiche linke Flucht, in die Prüfung | ja | b08 (vorher 3 px) | – |
| B.9 | Pfeile in Seitenleiste und **Pinnwände (Startseite)** zu tief, Papierkorbsymbol zu hoch; in die Prüfung | ja | b09 | **Pinnwände ergänzt:** Der Pfadtrenner „›“ in Startseitenknöpfen stand +0,95 px unter der Großbuchstabenmitte und war als Entscheidung E-U4 zurückgestellt. Jetzt einzeln optisch gesetzt (−0,05 px), Schreibweise unverändert; E-U4 entfällt |
| B.10 | Lupe statt „Su“ | ja (Segoe UI Symbol; Rückfallkette für macOS/Linux) | b10 | – |
| B.11 | Priorität je Ansicht festlegen und prüfen | Matrix in [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md); Metadaten auf Inhaltsbreite | b11 | Prüfung von „Labels“ auf Labels, Heute und Liste erweitert |
| B.12 | Keine doppelten Pfeile in Heute | ja | b12_b13 | – |
| B.13 | Nächste Aufgabe: nur Titel fett, keine Größenänderung | ja | b12_b13 | Prüfung sichert jetzt auch Datum, Label und Herkunft als normal |
| B.14 | Kein Kästchen vor „Aufgabe“ | ja | b14 | – |
| B.15 | Kurzer Papierkorbtext; Knopf nie überdeckt, appweit; Dokument mit allen UI-/UX-Anweisungen | ja; [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md) | b06_b15 | **appweite Prüfung neu (b15_appweit):** jeder sichtbare Knopf in sieben Ansichten und fünf Dialogen; fand „Nur offene“ im Spaltenboard bei 860 px abgeschnitten → Zeile bricht jetzt um. Gegen 3.42.0 findet sie das gemeldete Überdecken (S21) |
| B.16 | Kein Sprung beim Scrollen über Bilder | ja | b16 (vorher 389 px) | – |
| B.17 | Keine Hintergrundkästen hinter Listenaktionen | ja | b17_b19 | – |
| B.18 | Neuerungen unter „Über Glide“, Pflege dokumentiert | ja; Verfahren in [Veröffentlichung](../../../docs/10_VEROEFFENTLICHUNG.md) | b18 | Handbucheintrag „Über Glide“ ergänzt |
| B.19 | Keine Hintergrundkästen in der Punktbearbeitung | ja | b17_b19 | – |
| B.20 | Skills neutral als „Design Richtlinien“ integrieren, „und weitere“ | ja, Skill `design-richtlinien` | `test_design_richtlinien.py` | alle 15 Skills aus `skills-main/` begründet übernommen oder ausgeschlossen (Design Richtlinien) |
| B.21 | Verständlich für Dienste und Agenten ablegen | ja: Übergabe, Index, Plan, Prompt, Richtlinien verknüpft | Stand- und Linkprüfung | veraltete Angaben nachgezogen (D01–D50, Archiv- und Showcase-README, Arbeitsvorbereitungsindex, CLAUDE.md/AGENTS.md) |
| B.22 | Zuletzt: Dokumentation, Ablage, GitHub-Seite | Ablage gekürzt, README aktualisiert, Dokumente abgeglichen | Stand-, Link-, Ablageprüfung | Push und Merge erledigt (PR #27, `fe9366c`); **offen:** Auswertung der roten Tk-9.1-Vollmatrix (rot seit PR #26) |

## GitHub

Push am 16.10.2026 nach Anmeldung des Inhabers; [PR #27](https://github.com/n05a-design/glide-to-do/pull/27) vom Inhaber als Merge-Commit `fe9366c` in `main` zusammengeführt (Eltern `27bac83` und `23175b7`; Inhalt identisch mit `23175b7`). Ergebnis der GitHub-Prüfung unter „Offen“.

**Nach PR #29 (`8b59a8b`, Läufe 38927787712 und 38927780332 auf `b063518`):** Vollprüfung Windows mit eigener Tk 9.1 in beiden Läufen grün; Linux rot nur noch durch die drei Paket-8-Suiten `test_tempo330`, `test_planen33313`, `test_oberflaeche33321` und den Folgeschritt „Kalibrierte Erwartungen“ (`test_uiux_paket` und `test_klappmechanismen3321` dort grün). Der Windows-Paketlauf (PyInstaller, eigene Tk-9.1-Laufzeit) lief damit erstmals seit PR #26 wieder – zuletzt grün bei `a7f80b8` – und ist rot im Schritt „Isolierte Startprobe ohne externes Python“ (Paketbau und Quellvergleich grün). PR #26 hat diesen Weg umgebaut (eigene Laufzeit im Paket, zusätzliche Sperre der Paketlaufzeit, `windows_acl.py`); das UI-/UX-Paket änderte am Paketweg nichts. Ausgewertet über das Artefakt `paket-windows-belege` (`startprobe.json`, Lauf 38927787712): **Das Paket selbst ist grün** – `Glide.exe` 3.43.0 mit Tk 9.1.0 startet bei gesperrtem externem Python mit Exit 0, sechs Ansichten, Anlegen/Abhaken/Rückgängig, Dateilesen, Sicherungsrundlauf, Logo, gebündelte Schriften, Drag-and-drop und zugänglicher Kernablauf ohne Callbackfehler. Rot ist allein die Nachbereitung der Prüfung: Die native ACL-Restaurierung scheitert an Reparse-Punkten (WinError 5) – vier Symlinks im CPython-Quellbaum unter `paket-runtime/quellen/python/Misc/mypy` und `python3.exe` im Tool-Cache; beide Sperren kamen mit PR #26 hinzu. Prüfinfrastruktur aus der Vorbereitung von Paket 8 („Restaurierung originaler CI-Symlinks … native Wiederholung offen“), kein Befund dieses Pakets.

Auswertung der Protokolle beider Vollprüfungen und des Windows-Artefakts (16.10.2026, Inhalt `23175b7` = `fe9366c`, Vergleich mit `27bac83`; Seitensitzung „CI-Auswertung“): **Nativer Zugang ohne rote Stelle** (Native Tcl-Zugangsbindungen und `test_zugang400 --nativ` auf Linux und Windows grün). **Einziger Befund dieses Pakets:** `test_uiux_paket` Fall `b15_appweit` auf Linux und Windows – im leeren Papierkorb überdeckte der Leertext bei eingeschalteten Hinweisen „Zur Startseite“ (6–28 px). Ursache: `empty_state_top` zählte den Leertext nur, wenn er schon gemappt war; beim Ansichtswechsel ist er das unter Tk 9.1 noch nicht, und nichts rückte danach nach. Behoben: Gezählt wird der platzierte Leertext mit seiner tatsächlichen Höhe, `<Map>` und `<Configure>` ziehen Knopf und Gismo nach; b06_b15 prüft späten Map und nachträglich wachsenden Text (gegen `10b3aa3` rot). **Seit PR #26 rot, nicht aus diesem Paket** (Umstellung der ganzen Matrix auf eigene Tk 9.1): `test_klappmechanismen3321` (interne Prozedur `ttk::treeview::Keynav` in Tk 9.1 umbenannt – der Test führt jetzt die registrierte Klassenbindung aus), nur unter Linux `test_tempo330` (Radereignisse der Vergleichsansicht), `test_planen33313` (Strg+Umschalt+P unter X11/Tk 9.1) und `test_oberflaeche33321` (Systemdesign über `gsettings`, Prüfisolation) sowie daraus der Schritt „Kalibrierte Erwartungen“; diese drei Suiten gehören zu Paket 8. Die Korrektur ist ein Nachtrag zu 3.43.0 (Apphash `379e97e3`, 07 erneut bytegleich abgeglichen); der eingefrorene Volllauf oben bezieht sich auf `a7b1df81`, für den Nachtrag liefen die betroffenen Suiten gezielt.

## Lieferabgleich

- `versionswechsel.py 3.43.0 16.10.2026`: Fixtures, Showcase, Vorlagen, Releaseplanung und Standangaben neu; Ablage auf sieben Versionen gekürzt (3.37.0 entfällt, Verweise auf `0e7b358` festgesetzt).
- `abgleich_07.py`: 67 Code- und 146 Ressourcendateien in `07_Python-Versionen` bytegleich (nach den Nachbesserungen erneut abgeglichen, Apphash `a7b1df81`; nach dem Tk-9.1-Nachtrag nochmals, Apphash `379e97e3`), 3.42.0 ins Archiv.
- `showcase_abgleich.py`: Import, ID-Verweise, Dokumentarten, Bilder, Pinnwände, Undo, Vorlagen, Export und Neustart geprüft; sechs Dateien nach `05_Probelisten_Testdaten/Showcase`.
- Das Showcase-Werkzeug schreibt seine Vorlagendatei und das Manifest jetzt mit LF; unter Windows stimmten Prüfsumme und eingecheckte Bytes sonst nicht überein.

## Offen

- **GitHub:** Windows-Vollprüfung grün; Linux bis Paket 8 rot durch `test_tempo330`, `test_planen33313`, `test_oberflaeche33321` und „Kalibrierte Erwartungen“ (Tk-9.1-Umstellung durch PR #26). Windows-Paketlauf: Paket grün, rot nur die ACL-Restaurierung von Reparse-Punkten in der Prüfung (seit PR #26) – im [Nachlauf 16.10.2026](../acl_symlinks_2026-10-16/README.md) behoben, GitHub-Bestätigung offen.
- **macOS-Bundle und Mac-Vollprüfung:** auf Windows nicht baubar bzw. ausführbar; `packaging/macos/baue_app.py` und die eingefrorene Mac-Vollprüfung auf dem Referenz-Mac stehen aus. Bundle und eigenständige Pakete tragen bis dahin 3.42.0.
- **Menschenabnahme:** Sicht, DPI 100–200 %, Trackpad, große Schrift, alle Designs sowie Screenreader nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#ui-ux-paket-15102026-b01b19).
- **Produktentscheidungen** E-U1–E-U3 (A01–A03) beim Inhaber.
