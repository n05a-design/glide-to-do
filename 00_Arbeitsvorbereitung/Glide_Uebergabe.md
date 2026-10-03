# Glide – Übergabe an eine neue Sitzung

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · für den nächsten Chat oder Bearbeiter

Einstieg für jede Sitzung. Zusammengeführt am 03.10.2026 aus Sitzungsübergabe, Projektübergabe, Startkontext und dem Sitzungsprotokoll vom 24.–26.09.2026; die Vorfassungen trägt Git. Dieses Dokument sagt, wo was steht, was gilt und was als Nächstes ansteht – es ersetzt nicht die Fachdokumente.

## 1. In fünf Sätzen

- Glide ist eine lokale, deutschsprachige Aufgaben-, Notiz-, Seiten- und Pixel-App in Python 3.14 mit Tk 9: `src/glide/app.pyw` (rund 54.500 Zeilen, Klasse `ListApp`) und dreizehn Module, davon sieben Tk-freie Fachmodule nach D17.
- Aktueller Stand ist **3.33.6** (02.10.2026, Vollprüfung grün, ausgeliefert): Heute/Demnächst, Eisenhower, Schnelleingabe mit Feldchips und Wiederholungen, Startseite „Ruhig“, vier Seitenleistenbereiche, gemeinsame Formatsicherung. Verlauf: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
- Der Inhaber startet Glide **nur** aus `07_Python-Versionen` oder `01_Repository/Glide/build/macos/Glide.app`; eine Änderung ist erst bei ihm, wenn beide per SHA-256 abgeglichen sind.
- Beauftragt ist die Performance-Fortsetzung; neue Funktionen nur mit ausdrücklichem Auftrag. Entscheidungen trifft der Inhaber; Entschiedenes wird nicht erneut vorgelegt ([Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md)).
- Antworten, Dokumente und Oberfläche sind deutsch.

## 2. Wo was liegt

| Was | Wo |
|---|---|
| Arbeitsregeln und Abschlusskriterium | [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md), für Claude Code zusätzlich `CLAUDE.md` in der Wurzel |
| Aufgaben, Stufen, Ziele | [Entwicklungsplan](Glide_Entwicklungsplan.md) |
| Entscheidungen D01–D17 und frühere Antworten | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Code | `01_Repository/Glide/src/glide/` – Module siehe [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Datenformat, Backups, Austausch | [Daten und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfen | [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), Ergebnisse im QA-Bericht, Nachweise unter `tests/qa-<Version>/` |
| Startbare Fassung | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.33.6.pyw` plus Module, `resources`, `vendor`; Vorgänger 3.33.0–3.33.5 in `Archiv/` |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` (lokal, nicht versioniert), Kennung `de.shaye.glide` (Windows `Shaye.Glide`), nie ändern |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
| Fehlerprotokoll des Inhabers | `~/Library/Application Support/Glide/fehlerprotokoll.txt` – nur mit Erlaubnis lesen, nur Fehlereinträge |

## 3. Regeln, die immer gelten

- **Echte Daten nur als Kopie und nur mit Erlaubnis.** Tests und Messungen immer mit temporärem `GLIDE_DATA_DIR`, vor dem Import gesetzt. Originale nie verändern; nur Zahlen berichten.
- **Fotos nur vom eigenen Glide-Fenster** (`screencapture -l <Fensternummer>`), nie vom Bildschirm.
- **Plattformunabhängig:** keine Funktion nur für eine Plattform, keine neue Laufzeitabhängigkeit ohne Entscheidung.
- **Form folgt Funktion und die sechs Produktprinzipien** ([Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)); Farben nur über `BUTTON_ROLE_RULES`.
- **Jede Produktionsrunde bekommt eine Version** (`scripts/pflege/versionswechsel.py`). Reine Dokumentations-, Ablage- oder Werkzeugnachläufe bekommen einen datierten Nachweis zur unveränderten App-Version.
- **Ablage:** Das öffentliche Repository `n05a-design/glide-to-do` ist maßgeblich (D09). Uploads nur in die Projektstruktur, keine Benutzerpfade, keine Rohprotokolle, keine Archivkopien. Archive und Nachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten ([Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md)).
- **Dokumente:** ein Thema, ein Dokument; zusammenführen und löschen statt archivieren; Erledigtes im Entwicklungsplan markieren.

## 4. Lehren aus den bisherigen Runden

- **Rückwärtsverhalten messen, nicht annehmen:** 3.29 überschreibt einen Format-20-Bestand bei der ersten Eingabe. Vor jedem Formatwechsel die Vorgängerversion mit einer Kopie echter Daten prüfen; der Schutz vor unbekannten Formaten muss eine Version vorher im Code sein (seit 3.30 vorhanden).
- **Erst nach dem Abgleich erledigt:** Am 29.09.2026 prüfte der Inhaber einen alten Stand, weil 07 und Bundle nicht nachgezogen waren.
- **Vollprüfung ohne Last und ohne Eingaben** – Einzelheiten im [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md#regeln).
- **Optionen mit Empfehlung vorlegen:** nummerierte Fragen mit je einer Empfehlung und der Wahl „erste Stufe oder vollständig“ machen Rückfragen kurz; Lizenzfragen gleich mit Quelle und Lizenz vorlegen.
- **Inhaberentscheidungen früh abfragen:** Kennungen, Logo und Signatur blockieren Paketierung und Mitteilungen.
- **Planung nach jeder Etappe inhaltlich abgleichen**, nicht nur Statusspalten. Bekannte Grenzen sind die nächste Aufgabenliste.
- **Jede neue Oberfläche** bei 860 × 700 und großer Schrift prüfen; Farben als Rollen planen, damit die Kontrastprüfung greift.
- **Menübeschriftungen sind Schlüssel** der Befehlspalette (R2); vor Umbenennungen stabile Aktionskennungen einführen.
- Technische Fallstricke (Menübefehle unter macOS, `update()` in Rückrufen, Tk 9 und `place`, Bindtags): [Architektur, Abschnitt 5](../01_Repository/Glide/docs/02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt).

## 5. Prüfen

- **Vor jedem Commit:** `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` aus `01_Repository/Glide` (braucht Python mit tkinter, unter Linux Xvfb). Im Linux-Container möglich: CI-Grundstufe, Startprobe, `messung_speicherweg.py`; nicht möglich: macOS/Tk-9-Abnahme, Bundlebau, physische Bedienung. Ergebnisse als „Linux/Tk 8.6, künstliche Daten“ kennzeichnen.
- **Abnahme einer Version** auf dem Mac: `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.33.6/<Name> --timeout 900` – 81 Schritte, 64 Integrationssuiten, Unit-Tests, Showcase, fünf Analysen.
- **Letztes Ergebnis:** 3.33.6 am 02.10.2026, Exitcode 0; 146 Python-/60 Bundle-Dateien bytegleich.

## 6. Was als Nächstes ansteht

- **Beauftragt:** P04 Bildlayout, P06r doppelte Aktualisierungen, P08a/P08b Speicherweg, P09b Kennzahlen, Einstellungsfenster als Messpunkt, unveränderte Startseitenkacheln erhalten ([Entwicklungsplan, Abschnitt 3](Glide_Entwicklungsplan.md#3-performance-stufe-0-beauftragt)).
- **Braucht einen Auftrag:** UX1 „Weniger Oberfläche“ (vorher stabile Aktionskennungen), danach G05 Fokus und H-02, dann G29/G31/G32.
- **Kleine Reste für den nächsten Produktions- bzw. Werkzeugschnitt:** Code-Kommentar „Benachrichtigungen … Nicht-Ziel“ (AB06), Mindestversion Python/Tk prüfen (AB08), Kommentare zur Tastaturabschirmung in `pruefen.py` und `hintergrund/sitecustomize.py`, Verweise auf alte Dokumentnummern in den Textbausteinen von `tests/tools/releasedaten.py` (ändern nur zusammen mit neu erzeugter Release-Fixture).

## 7. Offen beim Inhaber

- Auswahl A–H (Richtung, Tiefe); D07 erst zur Pixel-Etappe; Importquelle und Bauwerkzeug erst in Stufe 4.
- I1 Inhaberangaben bestätigen, I2 Lizenz veröffentlichen, I3 Developer-ID und Code-Signing-Zertifikat, I4 Markenprüfung, I5 Python 3.14.7 installieren, I6 Windows-Vollprüfung und manuelle Prüfsitzungen ([Prüfliste](Glide_Manuelle_Pruefung.md)).
- Lizenzlage der Inspirations- und Beispielbilder in `20_Grafik_Master` (Stockfotos in einem öffentlichen Repository) prüfen.
