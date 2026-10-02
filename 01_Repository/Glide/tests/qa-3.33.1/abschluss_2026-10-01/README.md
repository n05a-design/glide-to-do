# Abschluss 3.33.1 – Nachweis

Begonnen 01.10.2026, fortgeführt 02.10.2026 · App 3.33.1 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten

## Ausgangslage

Die Vollprüfung vom 01.10.2026, 18:51 ([Ergebnis](../bereiche_fenster_2026-10-01/vollpruefung/ergebnis.json)) endete mit Exitcode 1: `audit_app`, `test_ui39`, `test_features329` und `test_aufraeumen330` rot. Ausgangsstand ist Git 5b2682c; 3.33.1 war damit nur Prüfkandidat.

## Befunde und Korrekturen

[Nachstellung, Ursachen und Gegenprobe](nachstellung.json). Rohprotokolle (`nachstellung/*.log`) bleiben lokal.

| Suite | Ursache | Art | Korrektur |
|---|---|---|---|
| `test_ui39` | Dialog „Neu anlegen“: macOS meldet beim Einblenden 1 × 1 Pixel. Seit dem verborgenen Vermessen folgt keine echte Breite mehr; die breite Maske blieb einspaltig, die Beschreibung lag unter dem sichtbaren Rand (Bildschirmhöhe 720) | Fehler der App | Platzhaltergröße im Spaltenumschalter übergehen |
| `test_features329` | Vertrag 74 ließ im Bereich Notizen keine Zeichnung zu, Vertrag 65 sieht datierte Zeichnungen im Notizbuch vor | Widerspruch der Verträge | Inhaber am 01.10.2026: Notizbuch nimmt datierte Zeichnungen auf; `sidebar_policy.CONTAINED`, Zielordner in allen Anlege-/Verschiebewegen |
| `audit_app` | Prüfung meldete den Zeiger über jedem Widget; seit 3.33.1 sind Bereichsüberschriften Ablageziele | veraltete Prüfung | Zeiger nur über dem Zielbaum |
| `test_aufraeumen330` | Menüfolge aus 3.33.1 war in `test_features330` nachgeführt, hier nicht | veraltete Prüfung | Erwartung angeglichen |

Neu: zwei Tk-freie Unit-Tests (26 insgesamt) und ein Block in `test_bereiche3331` – Notizbuch-Zeichnung anlegen, echtes Ziehen aus „Zeichnungen“ ins Notizbuch, Momentdatum, Rückgängig, Ablehnung für gewöhnlichen Ordner und Aufgabenliste. Gegenprobe: dieselbe Suite scheitert am Quellstand aus Git 5b2682c (Exitcode 1) und besteht am neuen (Exitcode 0).

## Vollprüfung

[Eingefrorener Quellstand](quellstand.json): 324 Dateien (Quellen, Prüfungen, Fixtures, Pflege- und Paketwerkzeuge, ohne Archive).

**Erster Lauf** ([Ergebnis](vollpruefung/ergebnis.json), 01.10.2026 23:58 bis 02.10.2026 00:23): Exitcode 1, 75 Schritte bestanden, alle vier früheren Befunde grün. Neu rot: `test_fenster330` („Esc schließt nicht“, keine Fensterfotos) und `test_bereiche3331` (Return auf dem Klapppfeil). Ursache ist die Umgebung, nicht der Code:

- Das Display schaltete um 00:16:44 ab, der Bildschirm war gesperrt (`CGSSessionScreenIsLocked=Yes`). `test_fenster330` lief von 00:15:37 bis 00:19:26, `test_bereiche3331` um 00:20:50.
- Ein gesperrter Mac stellt weder Tastaturfokus noch Fensterfotos zu.
- Gegenprobe: `test_bereiche3331` mit identischem Code vor der Sperre zweimal grün, bei gesperrtem Bildschirm erneut rot an derselben Stelle (`nachstellung/gesperrt_test_bereiche3331.log`).
- Der Quellstand war nach dem Lauf unverändert (324 Dateien).

Dieser Lauf gilt nicht als Abnahme.

**Zweiter Lauf** ([Ergebnis](vollpruefung_2/ergebnis.json), 02.10.2026 00:27 bis 00:52, entsperrt, `caffeinate -dims`): Exitcode 1, 76 Schritte bestanden. `test_fenster330` und `test_bereiche3331` sind bei entsperrtem Bildschirm grün; das bestätigt die Ursache des ersten Laufs. Neu und einmalig rot: `test_features330` – im Reisetagebuch existierte die Aufgabenliste, trug aber nicht den Titel „Packliste“ (`StopIteration`).

- Mit identischem Code ist die Suite einzeln grün, ebenso in drei instrumentierten Wiederholungen (Titel jeweils korrekt „Packliste“) und im ersten Lauf.
- Der Test fügt den Titel am Anfang des Eingabefelds ein. Ein abweichender Titel entsteht, wenn zusätzlich Text im Feld landet. Die Suite scheiterte um 00:37:00, als der Inhaber Chatnachrichten tippte.
- Probe (`NSApplication.isActive`): Trotz Hintergrundmodus wird jede Prüf-App beim Start aktiv – mit und ohne verborgenes Einblenden des Dialogs, also nicht erst seit 3.33.1. Abgeschirmt ist nur die Maus. Tastatureingaben während eines Laufs können daher in Prüfdialogen landen; die Suiten mit echten Tastenereignissen brauchen die aktive App (siehe erster Lauf).
- Wahrscheinliche Ursache ist deshalb eingefangene Tastatureingabe; nachweisen lässt sie sich nachträglich nicht, weil der temporäre Datenordner gelöscht ist. Quellstand nach dem Lauf unverändert.

Konsequenz: Testplan und Sitzungsübergabe nennen die Grenze jetzt ausdrücklich; während einer Vollprüfung nicht tippen und den Mac nicht sperren.

**Dritter Lauf – Abnahme** ([Ergebnis](vollpruefung_3/ergebnis.json), 02.10.2026 00:52 bis 01:17, entsperrt, ohne Eingaben, `caffeinate -dims`): **Exitcode 0.** 77 Schritte bestanden – Syntax (283 Dateien), Version, Dokumentation (788 Links), Fixtures, Unit-Tests, alle 60 Integrationssuiten, Showcase, fünf Analysen, Beispiel- und Releasedaten. Zwei Schritte plattformbedingt übersprungen (Screenshot-Erzeuger nur Linux/X11, Sichtprüfung durch eine Person). Quellstand vor und nach dem Lauf unverändert (324 Dateien).

## Auslieferung

[Lieferabgleich](auslieferung.json), 02.10.2026:

- `scripts/pflege/abgleich_07.py`: 11 Code-Dateien und 131 Ressourcen, keine Abweichung. Geändert gegenüber Git 5b2682c sind nur `Glide-Aufgaben-und-Listen_v3.33.1.pyw` und `sidebar_policy.py`; der vorherige Stand liegt in Git (keine zusätzliche Ordnerkopie, D09).
- `packaging/macos/baue_app.py --ziel build/macos`: Entwicklungsbundle neu gebaut (im Arbeitsordner gab es keines).
- SHA-256 gegen `src/glide`: 142 Dateien in `07_Python-Versionen`, 56 im Bundle, alle gleich. Bundle 3.33.1, Kennung `de.shaye.glide`, `codesign --verify --deep --strict` bestanden. App-Prüfsumme `0d432ea8…` wie im eingefrorenen Quellstand.

## Grenzen

Physische Maus-/Trackpad-/OS-Fokusbedienung, Windows/Linux, Mehrmonitor/DPI und Screenreader bleiben manuell offen. Keine Releasefreigabe.
