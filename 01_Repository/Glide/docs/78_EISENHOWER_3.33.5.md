# Glide 3.33.5 – Eisenhower als Gruppierung (G02)

Stand 02.10.2026 · Glide 3.33.5 · Aufgabenformat 20

Auftrag vom 02.10.2026 („einfach weiterarbeiten“ nach der Feature-Folge des Entwicklungsplans). Grundlage ist D13 in der [Arbeitsrichtung](ARBEITSRICHTUNG.md): keine eigene Ansicht, sondern eine Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board; Ziehen ändert Wichtigkeit bzw. Bearbeitungstag (D02); Fälligkeiten werden nie gelöscht. Keine Datenformatänderung, keine neue Abhängigkeit.

## Bedienvertrag

| Quadrant | Bedingung | Ablegen setzt |
|---|---|---|
| Sofort · wichtig und dringend | Wichtigkeit ≥ mittel und dringend | Wichtigkeit mittel (falls niedriger), Bearbeitungstag heute (falls nicht dringend) |
| Einplanen · wichtig, nicht dringend | Wichtigkeit ≥ mittel, nicht dringend | Wichtigkeit mittel (falls niedriger), Bearbeitungstag auf den Tag nach dem Fenster (falls nur der Bearbeitungstag dringend macht) |
| Kurz halten · dringend, nicht wichtig | Wichtigkeit < mittel und dringend | Wichtigkeit niedrig (falls höher), Bearbeitungstag heute (falls nicht dringend) |
| Später · weder wichtig noch dringend | sonst | Wichtigkeit niedrig (falls höher), Bearbeitungstag nach dem Fenster (falls nötig) |

- **Dringend** heißt: Fälligkeit oder Bearbeitungstag liegt höchstens zwei Tage nach heute oder ist vorbei. Fenster und Schwelle stehen als Konstanten in `eisenhower.py` (`DRINGEND_TAGE`, `WICHTIG_AB`); eine Einstellung dafür gibt es nicht.
- **Fälligkeit bleibt:** Liegt die Fälligkeit im Fenster, kann die Aufgabe nicht „nicht dringend“ werden; Glide lehnt das Ablegen ab und sagt warum. Eine Fälligkeit außerhalb des Fensters bleibt unverändert.
- Ändert sich nur, was der Zielquadrant verlangt; eine Uhrzeit am Bearbeitungstag bleibt. Die Rückmeldung nennt das geänderte Feld („Eingeordnet · Wichtigkeit mittel“) und bietet Rückgängig.
- Dieselbe Gruppierung gilt in Liste und Tabelle (gemeinsame Gruppenlogik); leere Abschnitte blendet die Liste wie bei jeder Gruppierung aus. Alt+←/→ und Doppelklick in eine Spalte wirken wie bei den übrigen Gruppierungen.
- Die Einordnung hängt vom Tag ab; der vorhandene Tageswechsel erneuert Board und Liste.

Die Fachlogik ist Tk-frei in `eisenhower.py` (D17): Quadrant je Aufgabe und Änderung beim Ablegen. Vier Unit-Tests mit festem Stichtag. In `app.pyw` nutzen `group_columns`, `item_group_keys` und `set_group_value` das Modul.

**Befund während der Umsetzung (Risiko R2):** Die Befehlspalette ordnet Menübefehle über ihre Beschriftung in Gruppen. Der neue Befehl „Gruppieren: Dringlichkeit × Wichtigkeit“ landete zunächst unter „Weitere Aktionen“; `test_features322`/`test_features325` haben das gefunden. Er steht jetzt unter „Ansichtseinstellungen“. Stabile Aktionskennungen vor UX1 bleiben empfohlen.

## Prüfung

Neue Pflichtsuite `test_eisenhower3335.py`: Gruppierung über das echte Auswahlmenü der Board-Optionen; vier Spalten in fester Reihenfolge; Zuordnung von fünf Aufgaben; Ablegen setzt Wichtigkeit bzw. Bearbeitungstag mit Rückmeldung; Ablehnung bei naher Fälligkeit ohne Änderung; Rückgängig; Alt+Rechts; Listengruppierung mit Abschnitten; Einstellung nach Neuladen. Gegenprobe: Mit 3.33.4 scheitert die Suite (kein solcher Menüeintrag).

## Abschluss 02.10.2026

[Nachweis](../tests/qa-3.33.5/eisenhower_2026-10-02/README.md), [Vollprotokoll](../tests/qa-3.33.5/eisenhower_2026-10-02/vollpruefung/ergebnis.json), [Quellstand](../tests/qa-3.33.5/eisenhower_2026-10-02/quellstand.json), [Lieferabgleich](../tests/qa-3.33.5/eisenhower_2026-10-02/auslieferung.json).

- **Vollprüfung Exitcode 0** (rund 14:01–14:27, ohne Eingaben): 80 Schritte, alle 63 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; Quellstand (338 Dateien) unverändert.
- **Auslieferung:** 145 Python-/59 Bundle-Dateien bytegleich, Bundle 3.33.5, Signatur gültig; Showcase ausgeliefert; 3.33.4-Hauptdatei als `_Z` archiviert.
- **Manuell offen:** Ziehen mit echter Maus im Board, Windows/Linux, DPI und Screenreader.
