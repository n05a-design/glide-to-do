# Technische Fakten Glide 3.19.0

Neu in 3.19: dauerhafter Änderungsverlauf. Anlegen, Ändern, Erledigen, Verschieben,
Umbenennen, Papierkorb, Wiederherstellen und endgültiges Entfernen bleiben mit Zeitpunkt,
Objekt, Liste und geänderten Feldern nachlesbar – über Programmstarts hinweg.
[Bedienung und Datenregeln](../../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md).

Stand: 13.09.2026. Kanonisch: `01_Repository/Glide/src/glide/app.pyw`, `VERSION` und die
aktuellen QA-Rohlogs. **Aufgabenformat 15** (vorher 14 seit 3.14), Einstellungen 2,
Vorlagenformat 2. Python/Tk und Standardbibliothek; vier DejaVu-Sans-TTF-Schnitte mit Lizenz.

Tragende Entscheidung: Der Verlauf entsteht nicht an den Bedienstellen, sondern in
`update_history` beim Speichern. `history_snapshot` baut einen kompakten Vergleichsstand
(Punkte mit Liste, Elternteil und vierzehn verglichenen Feldern; Listen, Ordner, Labels und
Papierkorb-Objekte), `history_events` bildet die Unterschiede auf Ereignisse ab,
`group_history_events` fasst ab 25 gleichartigen Ereignissen zusammen,
`record_history_events` hängt sie mit einem Zeitstempel an und hält die Obergrenze von 4000.
Dadurch ist jeder Weg durch die App erfasst – jede Änderung läuft über `save_items` –, und
der Verlauf benennt das Ergebnis, nicht die Absicht. Beschreibungen gehen nur als Hashwert
in den Vergleich ein, ihr Inhalt wird nie protokolliert; Anhänge nur als Anzahl.

Datenregeln: `history` liegt neben den Aufgabenfeldern in `glide_liste.json`.
`normalize_history_entries` prüft jeden Eintrag streng und verwirft Unlesbares, ohne die
Aufgaben zu berühren. `ensure_schema15_backup` sichert die Originaldatei als
`liste_vor_format15_*` vor dem ersten Speichern im neuen Format. `normalize_lists_data`
legt den gelesenen Verlauf in `_loaded_history` ab und nicht in `self.history`: Die Methode
läuft auch für fremde Archive, deren Protokoll den laufenden Bestand nicht überschreiben
darf. Ein vollständiger Import übernimmt den Archivverlauf und setzt einen Eintrag
„Bestand ersetzt"; ergänzendes Hinzufügen lässt den eigenen Verlauf stehen. Rückgängig
nimmt den Bestand zurück, nicht das Protokoll – die Rücknahme erscheint als weiteres
Ereignis. Die Protokollierung ist über `history_enabled` (Einstellung, additiv, Format 2
bleibt) abschaltbar.

Alle dreiundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, Beispiel- und
Releasedaten sind in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter Xvfb) mit
Exitcode 0 gelaufen. `test_features319.py` deckt Migration, alle Vorgänge, Feldlisten,
Sammeleinträge, Obergrenze, Backups, defekte Verlaufsfelder, Abschaltung, Leeren, Filter
und Dialog ab. Angepasst wurden die Formaterwartungen in sechs Bestandssuiten, die
Fixture-Schemastufe in `pruefen.py` (Formate 14 für 3.14.0 bis 3.18.0, darüber 15) und der
Bestandsvergleich in `test_features318.py`, der das Protokoll aus dem Vergleich nimmt. Neu
ist das Referenz-Fixture `tests/fixtures/current_v15/reference_v15.json`. Der maßgebliche
macOS-Lauf mit Python 3.14.5 wird im
[QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) nachgewiesen.

Datenordner frei wählbar, Fremdsperre führt zum Schreibschutz. Installer, Signierung,
Storefreigabe, Screenreader, weitere DPI-/Monitorprofile und Langzeitbetrieb bleiben offen.
