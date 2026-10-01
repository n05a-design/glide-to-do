# Technische Fakten Glide 3.21.0

Neu in 3.21: Kalenderimport aus ICS. Termine einer Kalenderdatei werden Aufgaben mit
Fälligkeit – mit Dauer als Aufwand, Kategorien als Labels, abbildbaren Wiederholungen und
Erinnerungen, mit Vorschau vor der Übernahme und einem Rückgängig-Schritt.
[Bedienung und Datenregeln](../../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md).

Stand: 14.09.2026. Kanonisch: `01_Repository/Glide/src/glide/app.pyw`, `VERSION` und die
aktuellen QA-Rohlogs. Aufgabenformat 15 (seit 3.19), Einstellungen 2, Vorlagenformat 2 –
3.21 ändert kein Datenfeld. Python/Tk und Standardbibliothek; vier DejaVu-Sans-TTF-Schnitte
mit Lizenz.

Der Parser arbeitet ohne Fremdbibliothek: `unfold_ics_lines` fügt gefaltete Zeilen zusammen
und liest CRLF, LF und BOM, `parse_ics_property` zerlegt in Name, Parameter und Wert und
überliest Doppelpunkte innerhalb von Anführungszeichen, `parse_ics_events` sammelt VEVENT-
und eingebettete VALARM-Blöcke. `parse_ics_moment` liest Datum, Ortszeit, UTC und `TZID`
(über `zoneinfo` aus der Standardbibliothek, mit Rückfall auf Ortszeit samt Hinweis, wenn
das System die Zeitzonendatenbank nicht mitbringt), `parse_ics_duration` ISO-8601-Dauern,
`ics_repeat_from_rule` bildet RRULEs streng ab und verwirft alles, was Glide nicht genauso
wiederholen kann. `ics_events_to_items` erzeugt Punkte ausschließlich über `new_item`,
`import_ics_events` übernimmt sie als einen `snapshot_undo`-Schritt und setzt bei Fehlern
Labelbestand und Stapel exakt zurück.

Zwei Regeln sind wichtig: `known_glide_item_ids` erkennt eigene UIDs
(`glide-<Punkt-ID>@glide.local`) – der Rundlauf mit der Ausgabe aus 3.20 legt dadurch keine
Kopien an; und nicht abbildbare Angaben werden **gezählt statt vereinfacht**, damit im
Bericht steht, was fehlt (Wiederholungsregeln mit `COUNT`, `BYMONTHDAY`, `BYSETPOS` oder
Intervallen bei Wochen, Monaten und Jahren; Erinnerungen nach dem Beginn oder bezogen auf
das Ende; unbekannte Zeitzonen). Grenzen: 2000 Termine und 12 MB je Datei, geprüft vor jeder
Bestandsänderung.

Alle fünfundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, Beispiel- und
Releasedaten sind in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter Xvfb) mit
Exitcode 0 gelaufen. `test_features321.py` deckt Rundlauf samt Duplikaterkennung, Parser,
Zeitzonen, beide Dauerangaben, sechs abbildbare und sechs nicht abbildbare
Wiederholungsregeln, vier Erinnerungsfälle, alle Übersprungsgründe, Zeitraumfilter,
Grenzen, beide Importziele, Rückgängig und Dialog ab. Bestandssuiten mussten nicht
angepasst werden. Der maßgebliche macOS-Lauf mit Python 3.14.5 wird im
[QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) nachgewiesen.

Datenordner frei wählbar, Fremdsperre führt zum Schreibschutz. Installer, Signierung,
Storefreigabe, Screenreader, weitere DPI-/Monitorprofile und Langzeitbetrieb bleiben offen.
