# QA-Testplan – Glide 3.7.0

Stand: 07.09.2026

## Ergänzung: 14 UI-Rückmeldungen

Die achte Suite `test_ui_polish36` ist in Schnell- und Vollmodus enthalten.
Sie prüft Hell/Dunkel, 860/1280 Pixel Fensterbreite, alle sieben Akzentfarben,
vollständige Buttontexte und erreichbare Vorlagenaktionen, linke Textspalten,
Labelhover/-Bestätigung, zweispaltige Einstellungen, Icon-Klickweiterleitung,
Jahresraster sowie 50 unabhängige USNO-Phasenereignisse aus 2026.
`--screenshots PFAD` erzeugt eigene Aufnahmen der betroffenen Ansichten.
Rohdaten und Grenzen: [Funktionsabgleich 3.7](25_FEATURE_ABGLEICH_3.7.0.md).


## Automatisierter Release-Lauf

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.7.0/automatisch`

1. Syntax, Versionen, Dokumentindex und lokale Links.
2. Aktuelle Backup-Fixtures und Referenzformate 4–12 sowie Legacy 2.
3. `test_glide`: Kernbedienung, Struktur, Undo, Backup, Migration, Labels,
   Wiederholungen und Navigation.
4. `test_datenintegritaet`: Bestandswächter, 130 Strukturkombinationen,
   Mehrfachauswahl, Drag-and-Drop, Dialoge und Uhrzeit.
5. `audit_app`: Funktions-/Integritätsaudit.
6. `test_dialog_theme`: Hell/Dunkel, Modalität, Grab-Rückgabe und Resize.
7. `test_ui_updates`: Eingabe, Arten, Fälligkeit, Startseite, Personalisierung
   und Neustart; optional Windows-Bilder.
8. `test_glide_36`: reine Bausteinprüfung von Mondphase, Statistik,
   Einstellungen und Vorlagen.
9. `test_release36`: echte Widgets, private Fonts, Teilbackup mit Anhängen,
   Labels und leeren Ordnern, Vorlagen speichern/bearbeiten, Anlage und Datenwechsel.
10. Statische und Erreichbarkeitsanalyse; keine automatische Codeentfernung.
11. Beispiel- und Release-Fixtures reproduzieren und inhaltlich vergleichen.

Jeder App-Import erhält vorher einen temporären `GLIDE_DATA_DIR`.
Der Vollmodus erzeugt zusätzliche Windows-Screenshots. Ein grüner Lauf
bestätigt keine manuelle Prüfung, Signatur oder Veröffentlichung.

## Zusätzliche Nachweise

`test_release36.py --screenshots <Ordner>` und
`test_ui_updates.py --screenshots <Ordner>` erfassen eigene Testfenster.
Bilder müssen visuell bewertet werden: Schrift, abgeschnittene Inhalte,
sichtbare Aktionsleiste, Symbolachse, heutiger Tag im Jahresraster, Mondform,
Kontrast und Material-/Solidmodus.

`leistungspruefung.py --ziel <Datei.json>` misst Start, Neuaufbau und Speichern
bei 100, 1.000 und 5.000 flachen Aufgaben mit und ohne Materialdarstellung.
Drei Durchläufe je Neuaufbau; Median und Rohwerte dokumentieren. Kein
allgemeines Hardwareversprechen aus einem lokalen Test ableiten.

## Manuelle Plattformmatrix

Windows 100/125/150 Prozent, zweiter Monitor, Hochkontrast, ausgeschaltete
Systemtransparenz, Remote Desktop, reale Tastatur/Maus und längere Nutzung.
macOS inklusive CoreText-Registrierung, Cmd-Kürzel, Menüs, modaler Unterdialoge,
Paketierung und Gatekeeper. Zwei reale synchronisierte Arbeitsplätze:
geordnetes Schließen, vollständiger Abgleich, zweiter Start, Offlinekonflikt.
Kopien realer Anhänge wiederherstellen, ohne Originalbestände zu verändern.

Aktuelle Ergebnisse und ausdrücklich offene Fälle stehen in
[Version 3.7.0](24_VERSION_3.7.0.md).

## Stand 3.7.0

Aktuelle Ergänzungen und Prüfnachweise: [Version 3.7.0](24_VERSION_3.7.0.md). Versionsgebundene 3.6-Berichte beschreiben den vorherigen Stand.

Zusätzlich enthalten: `test_ui_followup36` für Vorlagenbreite, Diagrammachsen, Jahreswerte, Kacheln und Neustart sowie `test_release37` für Formatmigration/Originalkopie, Containeranhänge, Seitendetails, Statistik nach Löschen, Mausrad auf Chips/Diagrammen und Tageshover. Zusammen zehn Suiten. `test_release37.py --screenshots tests/qa-3.7.0/oberflaeche` erfasst die betroffenen eigenen Windows-Testfenster.
