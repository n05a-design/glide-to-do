# Prüfung und manuelle Abnahme

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Aufgabenformat 20

Tests benutzen stets einen temporären `GLIDE_DATA_DIR` und `python -B`.
Kein Import und kein Test darf echte Nutzerdaten benutzen. Die dokumentierten
Versions-/Lieferkonflikte sind zunächst zu klären (Projektübergabe).

## Automatische Prüfungen

Aus `01_Repository/Glide`:

```bash
python -B tests/tools/standpruefung.py
python -B tests/tools/test_standpruefung.py
python -B -m unittest discover -s tests/unit
python -B tests/tools/ci_grundstufe.py --protokoll tests/qa-3.33.8/lokaler_lauf
python -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.33.8/vollpruefung --timeout 900
```

CI-Grundstufe: Syntax, Versionskonsistenz, Index/Links, Fixtures, Werkzeug-
und Unit-Tests, fünf Analysen, isolierte Start-/Ansichtsprobe, Lieferabgleich,
Fremdcodeherkunft und Datenschutz. Bestehende Integrationssuiten und
Referenz-Fixtures bleiben aktiv, auch für alte Datenformate. Die Vollprüfung
erzeugt/vergleicht zusätzlich Daten und Bilder. Ergebnisse und Rohprotokolle
werden lokal erzeugt; nur bereinigte Zusammenfassungen gehören in Git.

Die Integrationssuiten sind auf den Referenz-Mac abgestimmt. Linux-Grundstufe
und manuell startbare Linux-Suiten ersetzen keine Mac-Vollprüfung. Windows
verwendet `tests/tools/windows_vollpruefung.cmd`; Laufzeit, OS und tatsächlicher
Umfang stehen im Ergebnis. Ein roter Vorlauf bleibt ein roter Vorlauf.

## Nachweisregeln

Quell-/Prüfstand vor und nach dem finalen Lauf per SHA-256 erfassen.
Ausführbare Änderungen nach dem Einfrieren brauchen passende neue Prüfungen.
Vorhandene JSON-Ergebnisse niemals auf neue Versionen umetikettieren.
Formal grüne Stand-/Linkprüfung durch semantischen Abgleich ergänzen:
Funktionen, Datenformat, Aufgabenstatus, Entscheidungen und Grenzen gegen Code.
Für Dokumentpflege reichen Stand/Links, betroffene Werkzeugtests und Nachweis
unveränderter Laufzeit; keine künstliche App-Version.

Performance: gleiche Fixtures/Laufzeit/Methode, Aufwärmen, kalte und warme
Messungen trennen, Rohwerte, Median/p95. Profiling erklärt Ursachen;
unprofilierte Werte belegen den Gewinn. Viele Aufgaben bei gleicher Kartenzahl
belegen keine Skalierung auf viele Karten.

## Manuelle Kontrollmatrix

Alle Zeilen sind **offen**, bis ein tatsächlicher Geräteversuch dokumentiert ist.
Automatische Logikprüfungen ersetzen diese Abnahme nicht.

| Bereich | Zu prüfen |
|---|---|
| Vier Seitenleistenbereiche | Sichtbarkeit, Neu/Verschieben, gemischte Altordner, Notizbuchzeichnungen, Klappen, Zustand nach Neustart |
| Tastatur und Fokus | Tab-Reihenfolge, Kürzel, Esc/Return, OS-App-Wechsel, modale Dialoge und Rückkehr zum richtigen Feld |
| Ziehen | Maus/Trackpad, Bereichs-/Ordnerziele, Gruppenmitte/Rand, Termine/IDs/Undo |
| Aktualisierung | Auswahl, Fokus und Scrollposition; Tageswechsel, neue/gelöschte/archivierte Elemente |
| Zeichnung | Strich/Undo, Werkzeugwechsel, Zoom/Raster, Referenz/Nachzeichnung, Autosavefehler, Neustart, Export in externen Programmen |
| Seiten/Notizen/Bilder | Text, Formatspannen, Unicode, Umfluss, Größeziehen, Anhänge, Finder/Explorer, Galerie |
| Startseite | Eigene Kacheln, sieben Standards, Wiederherstellen, Neustart, Vorschauen, nächste Aufgabe |
| Planung und Ansichten | Tagesbeginn/-abschluss, Aufwand, Zeitblöcke, Kalender, Board-Spalten, abgeleitete Filter |
| Darstellung | Alle Fenster/Dialogs, zehn Designs, Kontrast, 860 × 700, Schriftgrößen, DPI/Mehrmonitor, Hochkontrast und RDP |
| Barrierefreiheit | Nur Tastatur, Screenreader, Canvas-Beschriftung und nachvollziehbare Statusmeldungen |
| Speichern/Backups | Unlesbar/neueres Format, Vorsicherungfehler, Schreibschutz, Fremdbelegung, Restore/Additivimport, Cloudordner nacheinander |
| Systemmitteilungen | Laufende App, verpasste Hinweise, Aufschub, Ruhezustand/Aufwachen, feste Plattformkennungen |
| Dauerbetrieb und Release | Dauerlauf, Clean Machine, Installer/Update/Deinstallation, Druck/PDF, Signatur/Notarisierung |

Während nativer Mac-Volltests Bildschirm entsperrt lassen und nicht tippen.
Der Hintergrundmodus schirmt die Maus ab, nicht die Tastatur. Hintergrund-Tk-
Fokus ist kein Nachweis physischer OS-Fokusbedienung. Menschliche Sichtprüfung
und Installer-/Storefreigabe bleiben gesondert offen.
