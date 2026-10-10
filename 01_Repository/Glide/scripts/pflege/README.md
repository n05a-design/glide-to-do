# Pflegewerkzeuge

Stand 10.10.2026 · Glide 3.37.0 · Aufgabenformat 23

Werkzeuge für jede Arbeitsrunde und für Messungen. Sie legen keine
Archivkopien an: Vorfassungen von Fixtures, Showcase, Vorlagen und Dokumenten
trägt Git. Einziges Archiv ist `07_Python-Versionen/Archiv` mit den
Hauptdateien der sieben neuesten Versionen; Nachweise unter `tests/qa-*` und
Releaseplanungen gelten ebenfalls für sieben Versionen, Fensterbilder für drei
(Entscheidung des Inhabers vom 03.10.2026). Die CI-Grundstufe prüft das
([`ablagegroesse.py`](../../tests/tools/ablagegroesse.py)).

| Werkzeug | Wozu | Aufruf |
|---|---|---|
| [versionswechsel.py](versionswechsel.py) | Hebt die Version: `VERSION`, `APP_VERSION`, Versionsprüfungen der Tests, Beispieldaten, Rundgang, Showcase, Vorlagenkatalog, neue Releaseplanung und die Standangaben aller fortgeschriebenen Dokumente; ohne Archivkopien; kürzt zum Schluss die Ablage | `python3 scripts/pflege/versionswechsel.py 3.33.0 01.10.2026` |
| [showcase_abgleich.py](showcase_abgleich.py) | Prüft den aktiven Showcase über tatsächlichen Import/Neustart und kopiert Basis, Vorlagen, Anleitung und Starter nach `05_Probelisten_Testdaten/Showcase`; ohne Archivkopien, SHA-256, kein Eingriff in den bearbeiteten Arbeitsstand | `python3 -B scripts/pflege/showcase_abgleich.py` |
| [abgleich_07.py](abgleich_07.py) | Spielt den Stand aus `src/glide` nach `07_Python-Versionen` und prüft SHA-256 | `python3 scripts/pflege/abgleich_07.py` |
| [ablage_kuerzen.py](ablage_kuerzen.py) | Entfernt Archive, Nachweise und Releaseplanungen außerhalb der sieben neuesten Versionen und Fensterbilder außerhalb der drei neuesten (`git rm`); läuft am Ende von `versionswechsel.py` | `python3 -B scripts/pflege/ablage_kuerzen.py`; `--anzeigen` listet nur |
| [messung_ansichtswechsel.py](messung_ansichtswechsel.py) | Misst jeden Ansichtswechsel (Median in ms) und zeigt die teuersten Funktionen (cProfile) | siehe Kopf der Datei |
| [messung_performance.py](messung_performance.py) | Unprofilierter Vorher-/Nachher-Vergleich mit festen Aufgaben-, Notiz- und Bildseiteninhalten; erste/warme Wechsel, Median/p95 und Rohwerte | `python3 -B scripts/pflege/messung_performance.py --items 1000 --json <Ausgabe>`; `--app` für gesicherten Vergleichsstand |
| [analyse_codebasis.py](analyse_codebasis.py) | Größte Klassen und Funktionen, wiederholte Texte, identische Funktionen, häufige Aufrufe | `python3 scripts/pflege/analyse_codebasis.py` |
| [pfade_bereinigen.py](pfade_bereinigen.py) | Ersetzt Benutzerpfade (`/Users/<Name>/` → `~/`, `C:\Users\<Name>` → `%USERPROFILE%`) in Textdateien vor dem Upload ins öffentliche Repository; bytegenau, JSON bleibt gültig; `--pruefen` meldet nur | `python3 -B scripts/pflege/pfade_bereinigen.py tests/qa-<Version>/<Lauf>` |
| [messung_startseite.py](messung_startseite.py) | Unprofilierte Messung der Startseite (P03): Wechsel, Aktualisierung an Ort und Stelle, Widgetzahl; `--kacheln alt` oder `d12`, `--profil` nur zur Ursachensuche | `python3 -B scripts/pflege/messung_startseite.py --kacheln d12`; `--app` für gesicherten Vergleichsstand |
| [messung_fundament3360.py](messung_fundament3360.py) | P03/E01: tatsächlichen Startseiten-Builder erzwingen, erste/warme Werte und Median/p95 getrennt; Einstellungen einschließlich echtem Modalaufbau, ohne Benutzerwartezeit/Schließen. `--lebensdauer` beobachtet zusätzlich fünf Serien je 20 UI-Abgleiche und Dialogöffnungen (Widgets, Tcl-Rückrufe, Python-Speicher, offene Timer); bewusst ohne wachsenden Undo-Verlauf | `python3 -B scripts/pflege/messung_fundament3360.py --app src/glide/app.pyw --json <Datei> --rounds 8`; Vergleichsstände seriell mit demselben Werkzeug, Ausgabe außerhalb von OneDrive |
| [messung_suche.py](messung_suche.py) | Unprofilierte Messung der Suche (P07): Eingabe in der eingebetteten Palette bis zur gezeichneten Trefferliste, 10.000 Punkte und 200 Seiten, Median/p95 je Begriff | `python3 -B scripts/pflege/messung_suche.py --json <Datei>`; `--app` für Vergleichsstand |
| [messung_speicherweg.py](messung_speicherweg.py) | Unprofilierter Vergleich des Speicherwegs bei wachsendem Bestand (P08, T2): erstes Speichern, Undo-Schnappschuss, `save_items`, Verlaufsvergleich, JSON, Abhaken über `item_change`; Aufwärmlauf, Median/p95, Rohwerte; `--profil` für cProfile; `--ohne-verlauf` und Speicherentwicklung über 50 Abhak-Vorgänge (P01r) | `python3 -B scripts/pflege/messung_speicherweg.py --items 10000 --json <Ausgabe>`; `--app` für gesicherten Vergleichsstand |
| [zaehlung_aktualisierungen.py](zaehlung_aktualisierungen.py) | P06r: zählt je Aktion (Anlegen, Abhaken, Wichtigkeit, Einplanen, Löschen, Rückgängig, Umbenennen, Archivieren, Kopieren, Ordner, Papierkorb) Aufrufe von `save_items`/`save_settings`, tatsächlich geschriebene Daten-, Einstellungs- und Sperrdateien sowie Neuaufbauten von Seitenleiste und Inhalt; belegt Doppelarbeit, keine Zeitanteile | `python3 -B scripts/pflege/zaehlung_aktualisierungen.py --json <Ausgabe>`; `--code` für gesicherten Vergleichsstand |
| [messung_bildseite.py](messung_bildseite.py) | P04: Seite mit Bildern; Tippen fern von Bildern, Tippen im Umfluss und Scrollen – Layoutläufe, Umflussberechnungen, tatsächliche Bildzeichnungen, Median/p95/Rohwerte von `layout_images` | `python3 -B scripts/pflege/messung_bildseite.py --bilder 30 --runden 21 --json <Ausgabe>`; `--code` für gesicherten Vergleichsstand |
| [pruefaufrufe_probe.py](pruefaufrufe_probe.py) | Wiederverwendbare P09b-Messprobe aus Git 7f30baf: erster/warmer Ansichtswechsel, Median/p95/Rohwerte; separater Profilaufruf erklärt Wiederholungen. `_glide_laden.py` isoliert den Datenordner und lädt mit `--code` einen Vergleichsstand. `einmal` ist nur eine historische Prozessprobe | `python3 -B scripts/pflege/pruefaufrufe_probe.py --punkte 10000 --runden 9 --json <Ausgabe>` |
| [messung_speichervergleich.py](messung_speichervergleich.py) | P08a: abwechselnde Vergleichsserien gegen einen unveränderten Git-Stand mit 100/1.000/10.000 Aufgaben, flach und verschachtelt; ohne Tk-Fenster/I/O, Median/p95/Rohwerte und identische Verlaufssnapshots | `python3 -B scripts/pflege/messung_speichervergleich.py --baseline-ref <Git-SHA> --json <Ausgabe>` |

**Reihenfolge einer Produktionsrunde** (Dokumentations-/Werkzeugnachlauf nach [Arbeitsrichtung](../../docs/ARBEITSRICHTUNG.md)):

1. Baseline mit passender bestehender Prüfung; der Ausgangsstand liegt in Git.
2. Umsetzen und Einzelsuiten ausführen.
3. `versionswechsel.py`, danach von Hand die CHANGELOG-Überschrift, den
   Abschnitt in [Funktionen](../../docs/20_FUNKTIONEN.md) und den Lieferabsatz
   in `07_Python-Versionen/README.md` (Hauptdatei, Inhalt, Nachweis; neue Module
   in der Modulliste). `abgleich_07.py` bricht mit Exitcode 1 ab, solange die
   README die neue Hauptdatei nicht nennt.
4. Vollprüfung: `python3 -B tests/tools/pruefen.py --modus voll --protokoll
   tests/qa-<Version>/<Name> --timeout 900` (unter macOS im Hintergrund).
5. `abgleich_07.py`, `python3 packaging/macos/baue_app.py --ziel build/macos`
   und `showcase_abgleich.py`.
6. QA-Bericht, Index, Entwicklungsplan und Übergabe nachführen.

Erst nach Schritt 5 trägt die Glide-Fassung des Inhabers den Stand.

`versionswechsel.py` pflegt Standzeilen und Fixtures, keine semantischen Aufgabenstatus. Titel, erste Prüfaufrufe, beantwortete Entscheidungen und nächste Schritte zusätzlich abgleichen. Für Werkzeugnachläufe `python3 -B tests/tools/test_standpruefung.py`, Syntax/Version/Stand/Index/Links und unveränderte App-/Paket-Hashes prüfen; den früheren Volllauf nicht überschreiben.

Messmodus der Pflichtsuite `tests/integration/test_library_performance3323.py --app <Quelle> --items 1000 --rounds 8 --measure <JSON>`: erneute Bibliotheksaktualisierungen innerhalb derselben Ansicht und neue Karten-/Aktionscontainer; Aufwärmdurchlauf und Rohwerte im JSON. Dateischreiben und Ansichtswechsel sind andere Messgrößen.

Für P08b misst `messung_speicherweg.py --lokale-punktmutation` den deklarierten lokalen `item_change`-Weg. Bei einer älteren App ohne dieses Argument verwendet die Probe den bisherigen Vollvergleich und kennzeichnet den tatsächlich gewählten Weg im JSON. `save_items` bleibt in dieser Probe als vollständiger Vergleich gemessen. Der Bestand verteilt 1.000/10.000 Aufgaben auf Listen mit je 200 Aufgaben; er ist nicht mit einer einzelnen Liste dieser Größe gleichzusetzen. Varianten seriell und in umgekehrter Reihenfolge messen, erste Speicherung und warme Werte getrennt auswerten.
