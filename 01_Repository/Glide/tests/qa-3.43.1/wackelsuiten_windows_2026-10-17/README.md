# Nachlauf 17.10.2026 – wackelnde Windows-Suiten `test_tag3390` und `test_template_workflows`

Stand 17.10.2026 · Glide 3.43.1 unverändert (Apphash `ed2b7eb6`, Datenformat 25) · Prüfwerkzeugnachlauf ohne neue App-Version · Windows 11 Pro, Python 3.14.7, Tk 9.0.4, künstliche Daten

Alle Läufe mit `PYTHONUTF8=1` wie im Prüfstand und unter kurzem Pfad (`C:\gq\…`, Ausfuhr per `git archive`; lange Pfade sind auf diesem Rechner aus). Maschinenlesbar: [ergebnis.json](ergebnis.json). Rohprotokolle und Diagnosewerkzeuge bleiben lokal.

## Anlass

Im [3.43.1-Nachweis](../kuerzel_linux_tk91_2026-10-16/README.md) blieben zwei Suiten offen, die unter 3.43.1 und 3.43.0 gleich wackelten:

- `test_template_workflows`: Das Auswahl-Popup eines `AppOptionMenu` schloss sich von selbst – `invalid command name …dropdownpopup…` in `field._highlight(12)` (Zeile 150) oder `assert field._popup is not None` (Zeile 137). Abwechselnd gemessen: 3.43.1 4/7, 3.43.0 5/6 grün.
- `test_tag3390`: „Speichern nicht sichtbar“ im Dialog „Kalender als Belegzeiten“ (Zeile 325 über `click`, Zeile 142) oder Fokusprüfung `assert root.focus_get() is title` (Zeile 297); nach Mitternacht je zweimal gleich rot, in der eingefrorenen 3.43.0-Vollprüfung vom 16.10. grün.

## Ursachen

Zwei voneinander unabhängige Prüfwerkzeugfehler. Glide verhält sich in beiden Fällen richtig.

**1. Fester Dialogtakt vor Tks Layout (`test_tag3390`, „Speichern nicht sichtbar“).** `modal()` plant die Dialogaktion mit `root.after(80, perform)` *vor* dem Öffnen. Dauert der Aufbau bis `wait_window` länger als 80 ms, ist der Zeitgeber beim Eintritt in die Ereignisschleife schon abgelaufen; Tcl bearbeitet ihn vor dem Leerlauf, in dem Tk den frisch gezeigten Dialog erst anordnet und seine Kinder mappt. Im Fehlermoment gemessen: Dialog gemappt, 820 × 786, aber äußerer Rahmen, Fuß und `ButtonFlow` 1 × 1 und ungemappt, `body` angefordert 899 px – also nur noch nicht angeordnet. Aufbau bis `run_modal` 50–96 ms, davon `_center_dialog` (Anordnen des noch verborgenen Dialogs) 40–55 ms. Über 80 ms lief die Aktion nach 86–100 ms und scheiterte, darunter nach 146–296 ms auf dem fertigen Dialog. Betroffen ist jede Aktion, die den Dialog ohne vorheriges `pump()` anfasst: „Speichern“ in `calendar_save`, `invalid_preview` und den Hinweis-Einstellungen sowie die Geometriemessung im Fall `dialoge` (Zeile 532). „Vorschau/Abbrechen“ fiel nie auf, weil die Aktion dort zuerst eine Tabellenprüfung mit `pump()` ausführt. Ein Mensch kann den Dialog in diesem Zustand nicht bedienen: Er ist erst im nächsten Leerlauf sichtbar, und den erreicht Tk, sobald kein abgelaufener Zeitgeber mehr ansteht.

**2. Desktop-Vordergrund vorausgesetzt (Fokusprüfung in `test_tag3390`, Popup in `test_template_workflows`).** Unter Windows bekommen die Prüffenster den Vordergrund nur, solange niemand den Rechner bedient. Eine Eingabe in einem anderen Programm (hier der Claude-App) nimmt ihn ihnen; Tk meldet dann keinen Fokus mehr (`focus_get()` ist `None`), hält aber den Fokus je Fenster weiter (`focus_lastfor()`).

- Fokusprüfung: In acht instrumentierten Läufen um 15:23 (Inhaber am Rechner, Leerlauf 0–1,75 s) lag der Vordergrund am Prüfpunkt fünfmal bei einem anderen Prozess; dreimal meldete Tk dabei schon keinen Fokus mehr, und genau diese drei waren an Zeile 297 rot – `focus_get()` `None`, `focus_lastfor()` das Titelfeld, Inspektorfeld identisch, ungespeicherter Text unverändert. Die übrigen fünf scheiterten später am Dialogtakt oder waren grün. Glide hielt also Feld und Fokus; die Prüfung maß den Desktop.
- Popup: `DropdownPopup._check_focus` schließt die Auswahl, wenn die App den Fokus verliert, wie ein Systemmenü (`test_ui39` prüft das ausdrücklich). In 18 instrumentierten Läufen zeigte Lauf 12 den Ablauf vollständig: Vordergrund wechselt 125 ms nach einer Eingabe zu einem anderen Prozess, das Prüffenster erhält `<FocusOut>`, `focus_get()` ist `None`, `focus_lastfor()` das Optionsfeld im Prüffenster, `_check_focus` schließt. Es traf dort das letzte Öffnen vor dem Zerstören, deshalb blieb der Lauf grün; fällt der Wechsel zwischen ein `_open_popup` und den nächsten Zugriff, entstehen genau die beiden gemeldeten Fehlerbilder. `_owner_changed` (Lage-/Größenwechsel, Unmap) schloss in keinem Lauf.

**Ausgeschlossen:**

- **Datum und Uhrzeit:** Beide Mechanismen haben keine Datumsabhängigkeit, und der Dialog zeigt an beiden Tagen dieselben zwei Intervalle. Dieselben Fehler traten um 01:08 (sechs von sechs Läufen am Wettlauf rot) und um 15:23 auf. Ob ein Lauf rot wird, entscheidet die Aufbauzeit gegenüber 80 ms bzw. eine Eingabe des Inhabers während des Laufs. Die grüne Vollprüfung vom 16.10. belegt nur, dass beides dort nicht eintrat.
- **Fenstergröße:** Dialog 820 × 786 auf 2560 × 1440, vollständig im Bild; kein Größen- oder Lagewechsel des Prüffensters hat ein Popup geschlossen.
- **Vordergrundsperre als Ursache allein:** Ohne Bedienung hatte der Prüfprozess meist selbst den Vordergrund (`ForegroundLockTimeout` in der Registry 200 000 ms; `SPI_GETFOREGROUNDLOCKTIMEOUT` liest 2 147 483 647 – nur gelesen, nichts verstellt). Entscheidend ist der Wechsel während des Laufs, nicht die Sperre selbst.
- **Ursache in 3.43.1:** nein – dieselben Fehler mit der App aus 3.43.0 und dem Prüfstand aus 3.39.0, in dem `test_tag3390` mit Takt und Fokusprüfung eingeführt wurde (Gegenvergleich unten).

## Korrektur (nur Prüfwerkzeug)

- `tests/integration/test_tag3390.py`: `modal()` wartet nach dem Takt bedingungsbasiert, bis der Dialog gemappt und sein Fuß angeordnet ist (höchstens drei Sekunden, sonst eigener Fehler „Dialog … nicht angeordnet“), und bedient ihn erst dann. Die Fokusprüfungen im Kalender- und im Hinweisfall verlangen `focus_lastfor()` auf dem gehaltenen Feld und `focus_get()` als dieses Feld oder `None`; ein Wechsel in ein anderes Glide-Fenster bleibt über `focus_get()` sichtbar.
- `tests/integration/test_template_workflows.py`: Während der Popup-Prüfung zählt ohne App-Fokus der Fokus, den Tk für das Prüffenster hält (`current_focus_widget()` fällt nur bei `None` auf `owner.focus_lastfor()` zurück, danach wiederhergestellt). Das Schließen bei Fokusverlust bleibt in `test_ui39` geprüft.
- `docs/05_QA_TESTPLAN.md`: Windows-Regel berichtigt (Prüffenster verlieren bei Bedienung den Vordergrund) und Regel „Fokus und Sichtbarkeit in Suiten“ ergänzt.

`src/glide`, `07_Python-Versionen` und `05_Probelisten_Testdaten` unverändert.

## Gegenproben mit Sonde

Eine lokale Sonde setzt jeden Zustand gezielt und unabhängig von der Bedienlage: `aufbau` verlängert jeden zentrierten Dialog um 120 ms, `desktop` lässt Tk dauerhaft keinen Fokus melden, `desktopwechsel` nimmt den Vordergrund mitten in der Hinweiszustellung weg. Drei Defektproben prüfen, dass die neuen Prüfungen echte Fehler weiter melden: `fokusdefekt` (Glide setzt nach dem Neuladen den Fokus auf die Eingabezeile), `hinweisdefekt` (die Zustellung setzt den Fokus in die Liste), `popupdefekt` (Tk meldet den Fokus bei offenem Popup im Hauptfenster). Alt = Prüfung aus `b2af7a7`, neu = korrigierte Prüfung; App jeweils 3.43.1, wo nicht anders genannt.

| Suite und Fall | Sonde | Alte Prüfung | Neue Prüfung |
|---|---|---|---|
| `test_tag3390 --fall kalender` | `aufbau` | rot, Zeile 325/142 „Speichern nicht sichtbar“ | grün |
| `test_tag3390 --fall kalender` | `desktop` | rot, Zeile 297 (Fokusprüfung) | grün |
| `test_tag3390 --fall dialoge` | `aufbau` | rot, Zeile 468/142 „Speichern nicht sichtbar“ (Dialog „Tageshinweise einstellen“) | grün |
| `test_tag3390 --fall hinweise` | `desktop` (dauerhaft) | grün – `None is None` | grün |
| `test_tag3390 --fall hinweise` | `desktopwechsel` | rot, Zeile 183 | grün |
| `test_tag3390 --fall hinweise` | `hinweisdefekt` | rot, Zeile 183 | rot, Zeile 205 (gehaltener Fokus: Liste statt Eingabezeile) |
| `test_tag3390 --fall kalender` | `fokusdefekt` | rot, Zeile 297 | rot, Zeile 326 (gehaltener Fokus: Eingabezeile statt Titel) |
| `test_template_workflows` | `desktop` | rot, Zeile 150 `invalid command name ….!dropdownpopup2…` | grün |
| `test_template_workflows` | `popupdefekt` | rot, Zeile 137 | rot, Zeile 147 (`_popup is not None`) |
| Gegenvergleich 3.43.0 (`5674936`): `test_template_workflows` | `desktop` | rot, Zeile 137 `assert field._popup is not None` | grün (neue Prüfung im 3.43.0-Baum) |
| Gegenvergleich 3.43.0: `test_tag3390 --fall kalender --app <3.43.0>` | `aufbau` | – | grün |
| Gegenvergleich 3.39.0 (`c38d960`, Einführung der Suite): eigene `test_tag3390 --fall kalender` | `aufbau` | rot: im Vorlauf Zeile 343/128 „Speichern nicht sichtbar“, im endgültigen Lauf schon an der Fokusprüfung Zeile 296 (Inhaber am Rechner) | – |

22 von 22 Fällen wie erwartet, Sonde in jedem Lauf nachweislich aktiv ([sonden.json](sonden.json)). Damit sind beide gemeldeten Fehlerbilder der Vorlagensuite (Zeile 150 und 137) und beide von `test_tag3390` (Zeile 325 und 297) gezielt erzeugt. Die Fehler bestehen seit Einführung der Suite in 3.39.0 bzw. mit der App aus 3.43.0 gleich. Ein erster Matrixlauf hatte zwei Fehlerwartungen: „dauerhaft kein Fokus“ im Hinweisfall (er ist mit der alten Prüfung grün, rot macht ihn erst der Wechsel – daraus entstand `desktopwechsel`) und eine Defektprobe mit echtem `focus_force` ins Hauptfenster. Die war untauglich, weil Windows-Tk unter dem Grab des Prüffensters die Aktivierung sofort zurückholt; sie meldet seitdem den Fremdfokus über Tk.

## Wiederholte Läufe unter Windows

Abwechselnd alte und neue Prüfung, 17.10.2026 15:47–16:02, Inhaber zeitweise am Rechner (Leerlauf seit der letzten Eingabe vor/nach den Läufen 0–45 s). App 3.43.1 außer in den letzten beiden Zeilen. Einzelwerte: [wiederholung.json](wiederholung.json).

| Lauf | Läufe | grün | rot und Stelle |
|---|---|---|---|
| `test_tag3390` (alle vier Fälle), neue Prüfung | 6 | 6 | – |
| `test_tag3390`, alte Prüfung | 6 | 0 | 2× Zeile 325/142 „Speichern nicht sichtbar“, 4× Zeile 532 in der Dialoggeometrie über `perform` (Zeile 111) |
| `test_template_workflows`, neue Prüfung | 6 | 6 | – |
| `test_template_workflows`, alte Prüfung | 6 | 5 | 1× Zeile 154 `invalid command name ….!dropdownpopup8…` |
| `test_tag3390`, neue Prüfung, App 3.43.0 (`--app`) | 4 | 4 | – |
| `test_template_workflows`, neue Prüfung im 3.43.0-Baum | 4 | 4 | – |

Zeile 532 ist eine dritte Erscheinungsform desselben Wettlaufs, zweimal einzeln nachgemessen: Dialog „Tag entlasten“ gemappt mit 820 × 702, Fuß `(0, 0, 1, 1)`, Inhalt 1 × 1 und nicht sichtbar. Die alte `test_tag3390` war damit in dieser Bedienlage nie grün; die neuen Prüfungen waren es in 20 von 20 Läufen.

## Weitere Prüfungen

| Prüfung | Ergebnis |
|---|---|
| CI-Grundstufe Windows mit `--lieferstand-streng` | bestanden, Exit 0, alle 19 Schritte: Syntax (307 Quelldateien), Versionen 3.43.1/Format 25, 191 Dokumentlinks, 152 Werkzeugtests, 714 Units auch ohne Systemzeitzonen, fünf Analysen, Startprobe, Lieferstand bytegleich, Fremdcode, Datenschutz, Ablagegröße, Synchronisation ([Protokoll](grundstufe.json)) |
| Erster Grundstufenlauf | ebenfalls Exit 0, aber Lieferstand nur als Hinweis „67 Abweichungen“: Ursache war diese Arbeitskopie, in der 75 Dateien von `07_Python-Versionen` mit CRLF statt LF ausgecheckt lagen (Git führt sie als LF). Im Repository sind alle 212 gemeinsamen Dateien von `src/glide` und `07_Python-Versionen` in `b2af7a7` blobgleich (nur die beiden eigenständigen `README.md` verschieden). Dateien neu aus Git angelegt, danach der strenge Lauf oben |
| App und Lieferstand | `src/glide`, `07_Python-Versionen` und `05_Probelisten_Testdaten` gegenüber `b2af7a7` unverändert; Apphash `ed2b7eb6` in `src/glide/app.pyw` und `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.43.1.pyw` |

## Grenzen

- Windows 11, Tk 9.0.4, künstliche Daten. Unter macOS (Hintergrundmodus, App bleibt aktiv) und Linux/Xvfb nicht ausgeführt; die GitHub-Vollprüfung bestätigt beide Suiten erst nach dem Push.
- Die eingefrorene Vollprüfung vom 16.10. gilt für ihren Stand; sie wird nicht als Lauf mit den neuen Prüfwerkzeugen ausgegeben.
- Dieselbe Abhängigkeit vom Desktop-Vordergrund ist an zwei weiteren Stellen möglich, aber nicht beobachtet und nicht geändert: `test_ui39` öffnet in seiner Dropdown-Grundprüfung 15-mal ein Popup und prüft es sofort, `test_planen33313` verlangt 30 ms nach dem Öffnen des Kalenders `focus_get()` im Dialog. Einen festen Takt vor dem Aufbau hat sonst keine Suite (`test_planen33313` plant ihn erst in `run_modal`, `test_aufgaben3380` prüft keine Sichtbarkeit).
- Unverändert offen: GitHub-Bestätigung des Windows-Paketlaufs und der Linux-Vollprüfung nach 3.43.1, Mac-Vollprüfung und Mac-Bundle, Menschenabnahme.
