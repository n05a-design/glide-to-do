# Projektübergabe – Glide 3.30.0

Stand 25.09.2026 · App 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

## Code und startbare Kopie

- **Kanonisch:** `src/glide/app.pyw` mit den Modulen `drawing.py` und
  `drawing_image.py`.
- **Startbare Kopie:** `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.30.0.pyw`,
  samt beiden Modulen und `resources`. 3.29.0 liegt im Unterordner `Archiv`.
- Der äußere Projektordner ist kein Git-Checkout.

## 3.30.0 (25.09.2026)

Mit 3.30.0 ist der Modernisierungskatalog vom 25.09.2026 vollständig
umgesetzt.

**Grundlage:** Die Entscheidungen E-01 bis E-16 folgen alle der Empfehlung.
Zusätzlich wurden gewählt:

- verknüpfte Punkte;
- Vorlagen mit Eingabefeldern;
- echte Abhängigkeiten;
- Tagesbeginn und Wochenrückblick;
- Kapazität je Wochentag;
- Zeiterfassung;
- das Design „Pixel“.

**Maßgeblich** für alles Neue ist der
[Vertrag Modernisierung 3.30](66_MODERNISIERUNG_3.30.0.md). Er enthält Umfang,
Bedienung, Datenvertrag Format 20, Einstellungs- und Pinnwandschlüssel,
Architektur, Abweichungen vom Katalog und die mitbehobenen Fehler.

Die Planungsdokumente liegen außerhalb des Repositorys in
`00_Arbeitsvorbereitung/`:

- `Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md` – jetzt mit Status je
  Paket;
- `Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md` – Entscheidungen
  als „entschieden 25.09.2026“;
- `Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md`.

Die Aufgabensammlung Zeichenfläche führt ZF-100, ZF-120, ZF-210 und die
Anlageoption „Pinnwand“ als umgesetzt.

**Ausbau am selben Tag** (alle Empfehlungen der Rückfrage gewählt):

- Zeitblöcke per Ziehen und Alt+↑/↓;
- Präsentation und Notizfolien als Druckseite bzw. PDF;
- Rückgängig beim Kartenverschieben;
- Detailbereich mit allen Feldern außer Anhängen;
- Gismo still in Leerzuständen;
- Pixelschrift „Pixelify Sans“ (SIL OFL 1.1) für Überschriften im Design
  „Pixel“.

Die Echtdatenprobe mit einer Kopie des Bestands fand einen Datenverlustweg in
3.29 (siehe unten).

**Bewusst nicht umgesetzt:**

- Einstieg für neue Nutzer (nicht gewählt);
- eigene Felder je Liste (nicht gewählt, die Gesamtanalyse rät ab);
- ein führender Begleiter mit Hinweisen und Führung (setzt ein Onboarding voraus).

## Worauf man achten muss

- **Glide 3.29 nach der Umstellung nicht mehr starten.** 3.29 hält einen
  Format-20-Bestand für beschädigt, beginnt leer und überschreibt ihn bei der
  ersten Eingabe. Zurück geht es nur über `liste_vor_format20_*.json`.
  - 3.30 selbst öffnet neuere Formate schreibgeschützt
    (`_read_only_reason`).
  - Unlesbare Dateien sichert 3.30 als `liste_unlesbar_*` und warnt über
    `data_format_written`, wenn eine ältere Version zwischendurch
    geschrieben hat.
  - Beim nächsten Formatwechsel diesen Weg beibehalten.

- **Leistengrenzen:** Zeichnung, Startseite und Pinnwand blenden Leisten
  unabhängig voneinander aus.
  - `_refresh_tree` ruft zuerst `restore_note_chrome()` und
    `restore_drawing_chrome()`, erst danach ordnet die Pinnwand. Diese
    Reihenfolge nicht umdrehen.
  - Ist die Listenoberfläche ausgeblendet, legt `restore_drawing_chrome` die
    Leisten in die Merkliste der Startseite.
- **Gruppierung:** Gruppierung und Spaltenboard teilen `group_columns`,
  `item_group_keys` und `set_group_value`. Neue Felder dort ergänzen, nicht
  in einer Ansicht.
- **Pinnwand-Rückgängig:** Flächenänderungen, die mehrere Karten betreffen,
  laufen über `board_view_change` und sind so zurücknehmbar.
- **Zeichnungskarten:** Sie tragen `page:<Seitenkennung>`. `valid_cards`
  liefert Punkte und Seiten, `valid_items` nur Punkte.
- **Detailbereich:** Er übergibt `item_change` bewusst keine Kennungen. Sonst
  würde die Auswahl beim Übernehmen auf den alten Punkt zurückspringen.
  - Wiederholungsregel und Beziehungsaufnahme teilen Maske und Bereich
    (`read_repeat_rule`, `add_relation_targets`). Neue Regeln dort ergänzen.
- **Pixelschrift:** `pixel_heading_family` fragt Tk direkt, nicht die beim
  Aufbau gefüllte Familienliste – im Gesamttest fehlte die Schrift dort.
  `reapply_heading_fonts` setzt die Überschriften kurz nach dem Start neu.
- **Druckseiten:** Pinnwanddruck und Folien teilen `board_region_lines`;
  geöffnet wird über `open_print_html`.

## Früherer Stand

Die Vorgeschichte der Zeichenfläche steht in
[Zeichnungsseite 3.29](65_ZEICHNUNGSSEITE_3.29.0.md) und
[Zeichenflächen-Übergabe](62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md). Deren
Aussagen zu Zell-Undo (20), fester Größe 128 und fehlenden Formwerkzeugen
sind seit 3.30 überholt.

Weitere ältere Stände:

- Tagebuch, Gismo und responsive Oberfläche:
  [Tagebuch und UI 3.28](59_TAGEBUCH_UND_UI_3.28.0.md);
- Flackerkorrektur:
  [Flackern und Ablageprüfung 3.28](60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Der Übergabetext zu 3.29 liegt im Archiv:
[Projektübergabe vor 3.30.0](archiv/09_PROJECT_HANDOFF_3.29.0_vor_3.30.0.md).

## Weiterarbeit und Prüfung

**Zuerst lesen:**

- [QA-Bericht](07_QA_BERICHT.md);
- [Release-Checkliste](10_RELEASE_CHECKLIST.md);
- [Daten und Migration](06_DATA_BACKUP_MIGRATION.md);
- die manuelle Prüfliste
  `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md`.

Tests immer mit isoliertem `GLIDE_DATA_DIR`.

**Vollaufruf:**

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/<neuer-Ordner> --timeout 900`

**Einzelsuiten der Neuerungen:**

- `tests/integration/test_drawing330.py`;
- `tests/integration/test_features330.py`.

Seit 3.30 öffnet der Zeichnungsimport eine Vorschau. Tests, die den Import
aufrufen, müssen `run_modal` ersetzen und „Als neue Zeichnung“ bestätigen –
sonst warten sie auf eine Eingabe (so geschehen in `test_features329`,
inzwischen angepasst).

**Keine menschliche Freigabe ersetzen die automatischen Prüfungen für:**

- Installer, Signatur;
- macOS;
- DPI und mehrere Monitore;
- Bildschirmleser;
- reale Maus- und Trackpadbedienung.

Diese Grenzen stehen im QA-Bericht und dürfen nicht als abgeschlossen
ausgegeben werden.
