# Technische Fakten Glide 3.20.0

Neu in 3.20: Kalenderausgabe als ICS. Fälligkeiten werden als Kalenderdatei geschrieben, die
Apple Kalender, Outlook, Thunderbird und Google Kalender einlesen – ohne Konto, ohne
Synchronisierung, ohne neue Laufzeitabhängigkeit.
[Bedienung und Datenregeln](../../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md).

Stand: 14.09.2026. Kanonisch: `01_Repository/Glide/src/glide/app.pyw`, `VERSION` und die
aktuellen QA-Rohlogs. Aufgabenformat 15 (seit 3.19), Einstellungen 2, Vorlagenformat 2 –
3.20 ändert kein Datenfeld. Python/Tk und Standardbibliothek; vier DejaVu-Sans-TTF-Schnitte
mit Lizenz.

Die Ausgabe ist reines Lesen: `ics_sources` holt die Mengen aus `print_document_sections` –
dieselbe Datengrundlage wie der Druck, damit Ausgabe und Ansicht nicht auseinanderlaufen –,
`ics_event_lines` baut je Punkt ein VEVENT, `ics_repeat_rule` bildet alle sechs
Wiederholungsarten samt `UNTIL` auf eine RRULE ab, `ics_alarm_lines` erzeugt VALARM aus
relativer oder fester Erinnerung, `escape_ics_text` und `fold_ics_line` stellen RFC 5545
her (Faltung nach Oktetten, nicht nach Zeichen), `write_ics_document` schreibt atomar über
`tempfile.mkstemp` und `os.replace` und weist Nutzdatendateien über
`validate_backup_target` ab. Kein neues Datenfeld, kein Verlaufseintrag, keine
Datenänderung.

Zwei Entscheidungen sind dokumentiert: Termine stehen in **schwebender Ortszeit**
(`DTSTART:20261001T093000`), damit keine Zeitzonentabelle mitgeliefert werden muss, die mit
jeder Sommerzeitreform veraltet; nur `DTSTAMP` und feste Alarme stehen in UTC, weil sie
schon im Bestand eindeutige Zeitpunkte sind. Und die **UID je Punkt ist stabil**
(`glide-<Punkt-ID>@glide.local`, Bearbeitungstage mit Suffix `-plan`), damit ein erneutes
Einlesen Termine aktualisiert statt verdoppelt. Dauer mit Uhrzeit: geschätzter Aufwand,
sonst 30 Minuten. Obergrenze 2000 Termine je Datei.

Alle vierundzwanzig Suiten, beide statischen Analysen sowie Vorlagen-, Beispiel- und
Releasedaten sind in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter Xvfb) mit
Exitcode 0 gelaufen. `test_features320.py` deckt Umfänge, Termintypen, Dauerregeln, alle
sechs Optionen, alle Wiederholungsarten, beide Erinnerungsarten, Escaping, Faltung samt
Rückfaltung, stabile UIDs, Obergrenze, Dateischreibung und Dialog ab. Bestandssuiten
mussten nicht angepasst werden, weil kein Datenfeld hinzukam. Der maßgebliche macOS-Lauf
mit Python 3.14.5 wird im
[QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) nachgewiesen.

Datenordner frei wählbar, Fremdsperre führt zum Schreibschutz. Installer, Signierung,
Storefreigabe, Screenreader, weitere DPI-/Monitorprofile und Langzeitbetrieb bleiben offen.
