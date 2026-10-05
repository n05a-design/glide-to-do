# Windows-Vollprüfung mit Fensterfotos – Nachweis

05.10.2026, 18:29–18:45 · Glide 3.33.8 unverändert · Windows x64, Python 3.14.8, Tk 9.0.4 (separate Prüflaufzeit) · gestartet vom Inhaber über `windows_vollpruefung.cmd`

Erster Windows-Lauf mit den Prüfwerkzeugen vom 05.10.2026 ([Vorbereitung](../windows_vorbereitung_2026-10-05/README.md)): Fensterfotos unter Windows und eine echte Dunkelaufnahme. App-Code, Lieferstand und Datenformat sind gegenüber dem grünen Lauf von 15:02 ([Nachweis](../windows_2026-10-05/README.md)) unverändert.

## Ergebnis

**[Originalergebnis](ergebnis.json): Exitcode 1, 85 Schritte – 83 ausgeführt, 1 fehlgeschlagen, 1 übersprungen.**

- Grün sind alle 66 Integrationssuiten, die Fachlogik-Unit-Tests, Showcase, Beispiel- und Release-Abgleich und vier der fünf Analysen.
- Übersprungen ist wie vorgesehen die Sichtprüfung.
- **Fehlgeschlagen ist `attributpruefung`:** Der Python-Interpreter ist selbst abgestürzt („Fatal Python error: _PyEval_EvalFrameDefault: Executing a cache.“, Exitcode 3221226505 = 0xC0000409).
  - Das Werkzeug liest `app.pyw` nur als Syntaxbaum; Glide-Code lief dabei nicht.
  - Derselbe Schritt war am selben Tag mit identischem Code und identischer Laufzeit dreimal grün.
  - Der Inhaber hat ihn um 18:56 dreißigmal einzeln wiederholt: 0 Abstürze ([Nachstellung](nachstellung.json)).
  - Einordnung: ein einmaliger, nicht reproduzierbarer Absturz des Interpreters; die Ursache ist nicht belegt. Nach dem Prüfplan bleibt der Lauf rot. Maßgeblich für die Funktion bleibt der grüne Lauf von 15:02.
  - Ein ähnliches, noch offenes CPython-Problem beschreibt sporadische Fehler im Auswertungskern von 3.14.6 ([python/cpython#155145](https://github.com/python/cpython/issues/155145)). Ein Zusammenhang ist nicht belegt.

## Neue Prüfwerkzeuge unter Windows bestätigt

- `test_fenster330` hat 50 Fenster geöffnet, geprüft und jedes fotografiert (lokal unter `fenster/`, nicht versioniert).
- Die [helle](screenshots/release_hell.png) und die [dunkle](screenshots/release_hell_dunkel.png) Aufnahme unterscheiden sich (`glass_light` / `glass_dark`). Die helle ist bytegleich mit der von 15:02.

## Auffälligkeiten aus den Aufnahmen (Vorbefunde, am Gerät zu bestätigen)

| Nr. | Befund |
|---|---|
| W01 | Gekürzte Seitenleistentitel sind rechts angeschnitten und haben kein „…“, hell wie dunkel und wie um 15:02 („Unterlagen & Asset“, „Releaseplanung 3.3..“). |
| W05 | „Für KI bereitstellen“ ist 1705 px breit, „Tabellenspalten“ 1317 px; die Knopfreihe steht links, anders als in den meisten Dialogen. |
| W06 | In 13 von 22 Fotos der Dialoge „Neue Liste“ und „Neuer Ordner“ sind Überschrift und Feldbeschriftungen weiße Flächen ohne Text; Eingabefelder und Knöpfe sind gezeichnet. Offen ist, ob der Aufnahmezeitpunkt (verzögert zeichnende Leinwandbeschriftungen) oder eine echte Zeichenlücke die Ursache ist. |
| W07 | „PNG auf 128 × 128 einpassen“ nach „Ganzes Bild zeigen“: Der Hinweistext steht doppelt und überlagert. |
| W08 | „Pixelsymbol“: Das 16 × 16-Raster ist nur rund 60 px groß und steht mitten in einer großen leeren Fläche (Zoom 5×). |

Prüfschritte am Gerät: [Prüfliste, B1](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung). Aufgaben: Entwicklungsplan W01, W05–W09.

Rohprotokolle (`*.log`) und Fensterfotos bleiben lokal.
