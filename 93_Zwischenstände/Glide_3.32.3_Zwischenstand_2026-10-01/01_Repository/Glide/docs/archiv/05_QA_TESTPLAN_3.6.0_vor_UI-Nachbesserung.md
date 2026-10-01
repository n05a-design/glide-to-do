# QA-Testplan – Glide 3.6.0

Stand: 06.09.2026

## Automatisierter Release-Lauf

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.6.0/abschluss`

1. Syntax, Versionen, Dokumentindex und lokale Links.
2. Aktuelle Backup-Fixtures und Referenzformate 4–11 sowie Legacy 2.
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
[18_QA_3.6.0.md](18_QA_3.6.0.md).
