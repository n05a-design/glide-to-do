# Flackern, Debugging und Ablageprüfung – Glide 3.28.0

Stand 23.09.2026 · Glide 3.28.0 · Aufgabenformat 18

## Anlass und Ergebnis

Auf der Startseite wurde nach `Füttern` von Gismo ein kurzes Weißwerden oder
scheinbares Neuladen beobachtet, besonders im Dopamin-Design. Der Fehler lag
nicht an den gespeicherten Gismo-Werten und nicht an einer besonderen
Startseitenposition. Der Pflegepfad plante nach jeder Aktion mit 900 ms Abstand
einen vollständigen Aufruf von `refresh_home()` ein. `_refresh_home()` zerstört
alle Kinder von `home_content` und erzeugt Uhr, Kalender, Pinnwandvorschau,
Gismo, Diagramme und sämtliche Karten erneut.

Im Dopamin-Design ist das auffälliger, weil gleichzeitig mehrere Canvas-
Animationen und zeitversetzte Rückmeldungen im Tk-Ereignisstrom liegen. Der
Auslöser war allgemein der vollständige Neuaufbau; das Dopamin-Design verstärkte
nur seine Sichtbarkeit.

## Recherche und technische Einordnung

Die Python-Dokumentation beschreibt Tkinter als ereignisgetriebene,
einthreadige Oberfläche: Widgets bilden eine Hierarchie, Darstellung und
Geometrie werden durch die Tk-Ereignisschleife aktualisiert und Callback-Code
soll kurz bleiben. Das stützt die Korrektur, nur die tatsächlich geänderten
Widgets anzufassen statt den gesamten Widgetbaum zu ersetzen:

- https://docs.python.org/3/library/tkinter.html
- https://docs.python.org/3/library/tkinter.html#threading-model

Die Tcl/Tk-Dokumentation erklärt, dass Darstellungs- und Geometrieänderungen
über ausstehende Ereignisse und Idle-Aufgaben verarbeitet werden. `update`
arbeitet alle Ereignisse ab, `update idletasks` nur die Idle-Aufgaben. Ein
unnötig großer Neuaufbau vergrößert folglich die zu verarbeitende Zeichen- und
Geometriearbeit:

- https://web.tcl.tk/man/tcl9.0/TclCmd/update.html
- https://web.tcl.tk/man/tcl8.6/TkCmd/bind.htm

Unter Windows wird eine ungültige Fensterregion vor dem Neuzeichnen abhängig
vom Fensterhintergrund gelöscht. Microsoft dokumentiert dafür
`WM_ERASEBKGND`, die Update-Region und `WM_PAINT`. Das erklärt, warum ein
kurzer Zwischenzustand bei großflächiger Invalidierung als helle oder weiße
Fläche sichtbar werden kann; Glide greift nicht direkt in diese Win32-
Nachrichten ein, sondern vermeidet die großflächige Invalidierung:

- https://learn.microsoft.com/windows/win32/winmsg/wm-erasebkgnd
- https://learn.microsoft.com/windows/win32/gdi/the-update-region
- https://learn.microsoft.com/windows/win32/gdi/wm-paint

Eine Win32-Sonderbehandlung oder pauschales Double-Buffering wurde bewusst
nicht ergänzt. Die Ursache lag eine Ebene höher im eigenen Widget-Lebenszyklus
und ließ sich dort plattformneutral entfernen.

## Korrektur

- `ProgressBar.set_value()` aktualisiert Wert und Zeichnung eines vorhandenen
  Balkens.
- Die Gismo-Kachel hält ihre drei Balken lokal fest.
- `Füttern`, `Spielen` und `Ruhen` speichern weiterhin denselben Zustand, ändern
  aber nur diese drei Balken.
- Nach 900 ms wird ausschließlich Gismos gezeichneter Zustand zurückgesetzt.
- Es wird kein `refresh_home()` mehr geplant. Scrollposition, übrige Karten,
  Canvas-Animationen und Widgetidentitäten bleiben erhalten.

## Regressionstest

`tests/integration/test_features328.py` schaltet ausdrücklich in das
Dopamin-Design, öffnet die Startseite, löst `Füttern` aus und prüft:

1. Der Sättigungsbalken steigt sofort.
2. Der vorhandene Balken bleibt nach der Reaktionszeit existent.
3. `refresh_home()` wurde nicht aufgerufen.
4. Es entstand kein Tk-Callback-Fehler.

Zusätzlich bestanden Syntaxprüfung, Hauptsuite, Vorlagenworkflow und
Tagesplanungstest. Eine menschliche Sichtprüfung mit echter Maus bleibt trotz
der strukturellen Regression offen und steht in der manuellen Checkliste.

## Ablageprüfung

Die aktuelle Ablage wurde über Repository, Arbeitsvorbereitung, Probedaten,
startbare Fassung, Dokumentation, Grafik, Release-Exports, Storematerial,
Ablage und externe Testdaten geprüft. Überholte aktuelle READMEs wurden vor der
Aktualisierung in ihrem jeweiligen Archiv gesichert. Frühere Chat-Weitergaben
vom 18. und 19.09.2026 wurden archiviert. Die nicht lokal verfügbare
Weitergabe vom 16.09.2026 und drei ebenfalls nicht lokal verfügbare
3.21.4-Probedateien konnten wegen OneDrive `Access denied` nicht verschoben
werden und bleiben als ausdrücklich benannte Restpunkte sichtbar.

Die aktiven Nutzerkopien der Vorlagen und Probedaten tragen nun 3.28.0 und sind
per SHA-256 bytegleich zu ihren kanonischen Quellen. Historische, bereits im
Namen versionierte Funktions-, Prüf- und Entscheidungsdokumente wurden nicht
umetikettiert: Ihr alter Versionsstand ist Inhalt, keine veraltete Aussage über
den aktuellen Stand.

## Grenzen

Die vollständige Standprüfung kann weiterhin nicht alle OneDrive-Platzhalter
lesen. Der ältere Breiten-/Ereignistest `test_ui_followup36.py` und der ältere
Sammeltest bleiben separat als Zeitüberschreitung offen. Deshalb ist 3.28.0 ein
geprüfter Entwicklungsstand, aber noch keine vollständige Releasefreigabe.
