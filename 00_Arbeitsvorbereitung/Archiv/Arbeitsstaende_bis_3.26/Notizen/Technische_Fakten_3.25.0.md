# Technische Fakten – Glide 3.25.0

Stand: 19.09.2026 · Glide 3.25.0 · interner Entwicklungsstand · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

3.25.0 beantwortet vierundzwanzig benannte Punkte unter einem Leitsatz: „form
follows function“ – zurück zu den Kernfunktionen, mit einer minimalistischeren
Oberfläche.

**Kein Formatsprung.** Aufgabenformat bleibt 16, Einstellungsformat 2,
Vorlagenformat 2.

## Was sich am Datenmodell ändert

| Ort | Änderung |
| --- | --- |
| Einstellungen | `overview_sections_closed` – Liste der zugeklappten Abschnitte der Übersichten. Nur bekannte Kennungen überleben die Normalisierung. |
| Einstellungen | `action_feedback` – `auto` (Vorgabe), `milestones` oder `all`. |
| Einstellungen | `mascot_name` – Name des Begleiters, höchstens 24 Zeichen. |
| Einstellungen | `home_tile_order` / `home_tiles_hidden` nehmen zusätzlich `boardpreview` und `mascot` auf. |
| Einstellungen | `design` kennt zusätzlich `minimal_light` und `minimal_dark`. |
| Aufgaben | unverändert. |
| Backup | unverändert. |

Alle neuen Einstellungsfelder sind additiv; eine Datei aus 3.24 bleibt gültig.

## Der Stillstand mit weißer Kopfleiste – die Ursachenkette

Das ist der wichtigste technische Befund dieser Version.

1. Glide startet als `.pyw`, also unter `pythonw.exe`. Dort sind
   `sys.stdout` und `sys.stderr` **`None`**.
2. Tkinter meldet jeden Fehler aus einem Callback über
   `traceback.print_exception(..., file=sys.stderr)`.
3. Ist dieser Strom `None`, scheitert die Fehlermeldung selbst mit einem
   `AttributeError` – **innerhalb** des Tcl-Aufrufs.
4. Der Interpreter bekommt damit einen Fehler in der Fehlerbehandlung. Die
   Ereignisschleife verarbeitet nichts mehr.
5. Windows zeichnet die Fläche eines Fensters, das seine Nachrichten nicht
   mehr verarbeitet, **weiß**. Das ist die „weiße Kopfleiste“.

Der Punkt daran: Sichtbar ist die letzte Stufe, verursacht hat es die erste.
Jeder beliebige Fehler an jeder beliebigen Stelle konnte den Stillstand
auslösen – deshalb „manchmal“ und deshalb kein Muster.

Behoben in drei Schichten:

| Schicht | Was sie tut |
| --- | --- |
| `_ensure_streams()` | Setzt vor allem anderen `sys.stdout`/`sys.stderr` auf beschreibbare Ströme, wenn sie fehlen. Nimmt dem Fall die Wirkung. |
| `ListApp.report_callback_exception` | Schreibt jeden Fehler mit Zeitstempel, Version und vollem Traceback nach `fehlerprotokoll.txt` neben den Daten, meldet sich einmal je Sitzung und reicht an einen bereits vorhandenen Bericht weiter. Gibt dem Fall einen Ort. |
| `run_modal` | Fängt ein gescheitertes `grab_set` ab, statt den Aufrufer mitzureißen, und gibt den Griff im `finally` zurück. |

`ERROR_LOG_FILE` wandert mit der Datenablage mit und wird bei 200 KB auf die
Hälfte gekürzt. Erreichbar über Hilfe → Fehlerprotokoll öffnen.

## „Verspätet“ sprang zur Startseite

Zweiter Fehler mit derselben Signatur „es passiert etwas anderes als gedacht,
und niemand meldet es“. `set_overdue_view()` setzte `view_mode` korrekt; die
Seitenleiste fand danach keine Zeile für diese Ansicht – sie hat seit 3.24
keine mehr –, markierte ersatzweise die erste Zeile, und deren
Auswahlereignis warf die Ansicht im nächsten Leerlauf auf die Startseite.

Sichtbar war das nur **nach** einem `update()`. Die bestehende Zusicherung in
`test_glide.py` prüfte unmittelbar nach dem Aufruf und blieb deshalb grün.

Die vier `pass`-Sonderfälle für Ansichten ohne Seitenleistenzeile
(gespeicherte Filter, Listenübersicht, globale Pinnwand – und die für
„Verspätet“ fehlende) sind durch **eine** Regel ersetzt: Eine Ersatzmarkierung
gibt es nur, wenn `active_row is None`, also wenn wirklich nichts geöffnet ist.

## Neue Bausteine

| Baustein | Zweck |
| --- | --- |
| `FieldPairGrid` | Gleich breite Feldspalten, deren Eingabefelder auf einer Linie stehen – Beschriftung und Feld in getrennten Rasterzeilen. |
| `BoardPreview` | Verkleinerte Pinnwand als Bild; ohne Karten eine Andeutung. |
| `MascotCanvas` | Der Begleiter, gezeichnet statt geladen; fünf Zustände. |
| `rounded_rect_points()` | Die Stützpunkte eines abgerundeten Rechtecks – vorher dreimal ausgeschrieben. |
| `build_menu()` / `menubar_structure()` | Menüaufbau aus einer Beschreibung, samt Anmeldung beim Theme. |
| `finish_page_switch()` | Der gemeinsame Abschluss jedes Seitenwechsels – vorher viermal ausgeschrieben. |
| `reveal_tree_row()` | Pfad aufklappen, Zeile auswählen und ins Bild holen – vorher zweimal, einmal davon ohne Fehlerbehandlung. |
| `restore_focus()` | Fokusrückgabe nach einem Dialog. |
| `dialog_color()` | Farbe zu einem Themeschlüssel mit Rückfall statt `unknown color name`. |
| `task_urgency_rank()` | Eine Rangfolge für „als Nächstes dran“ – für Übersicht und Startseite. |
| `feedback()` + `ACTION_FEEDBACK_TEXTS` | Rückmeldung auf jede Aktion aus einer Tabelle. |
| `GLASS_LAYERS` | Die Glasschicht als Tabelle statt als zwei ausgeschriebene Zweige. |
| `MANUAL_SECTIONS` | Das Handbuch als Tabelle im Quelltext. |
| `MINIMAL_THEMES` | Zwei Farbtafeln aus echten Neutraltönen. |

## Geometrie der Pinnwandverbindungen

`border_point(box, ziel_x, ziel_y, abstand)` liefert den Schnittpunkt der
Sichtlinie mit dem Kartenrand, um `abstand` nach außen versetzt. Die Linie
läuft von Rand zu Rand statt von Mittelpunkt zu Mittelpunkt und liegt damit
nirgends unter einer Karte.

| Konstante | Wert | Bedeutung |
| --- | --- | --- |
| `CONNECTION_GAP` | 3 | Abstand zwischen Kartenkante und Linienende |
| `CONNECTION_MIN_LENGTH` | 5 | Darunter wird nicht gezeichnet (Karten überlappen) |
| Spitzenlänge | `max(6, min(12 + 2·Breite, Länge · 0,6))` | Die Spitze überragt die Linie nie |

`tag_raise("connection")` statt `tag_lower`: Die Linien liegen jetzt vor den
Karten. Da sie keine Karte mehr berühren, verdecken sie nichts – aber zwischen
überlappenden Karten bleiben sie sichtbar. Die Druckausgabe rechnet mit
denselben Werten.

## Schaltflächenbreite

`RoundedButton` misst seine Beschriftung mit `font measure` und hebt seine
Breite auf `Textbreite + 30` an (`+14` bei linksbündigem Text). Die
mitgegebene Breite ist damit eine Untergrenze. `fit_text=False` schaltet das
ab. Grenze nach oben gibt es keine – wer eine feste Breite braucht, setzt sie
nach dem Anlegen.

## Prüfstand

| Vorher | Jetzt |
| --- | --- |
| 28 Suiten | **30 Suiten** (`test_features325.py`, `test_vollpruefung325.py`) |
| 4 Analysen | **5 Analysen** (`dublettenpruefung.py`) |

`test_vollpruefung325.py` prüft in die Breite: 9 Designs × 3 Fensterbreiten ×
12 Ansichten, 5 Anzeigeumfänge, 16 Startseitenkacheln einzeln, 84 Menüaktionen
(Dialoge werden gebaut und sofort geschlossen), alle Pinnwandaktionen, alle
Rückmeldungsstufen, alle Zustände des Begleiters. Sie sammelt
`report_callback_exception` – dort landen genau die Fehler, die Tk verschluckt.

`dublettenpruefung.py` fand 14 Fundstellen mit 21 vermeidbaren Wiederholungen;
nach den vier Zusammenfassungen sind es 9 mit 13. Der Rest sind Farbtafeln und
Erstauf-Initialisierung – Daten und bewusst ausgeschriebene Parallelzweige.
Dass die Farbtafeln unverändert sind, ist belegt: alle neun Designs vor und
nach dem Umbau vollständig ausgegeben und verglichen.

Eine Portabilitätsgrenze ist mit 3.25 weg: `test_glide.py` erwartete die
Beispieldatei als `Glide_Beispieldaten.glidebackup`, im Repository liegt sie
klein geschrieben. Unter macOS und Windows dieselbe Datei, unter Linux nicht.
Suite, Erzeuger und Prüfstand benennen sie jetzt einheitlich klein.

## Was in der Vorabumgebung nicht prüfbar bleibt

Die Dokumentprüfung von `pruefen.py` verlangt jedes im Index verlinkte
Dokument. Der Index verweist auf rund 400 archivierte Dateien, die nur am
Arbeitsgerät vollständig vorliegen. Alle übrigen 40 Schritte laufen grün.
