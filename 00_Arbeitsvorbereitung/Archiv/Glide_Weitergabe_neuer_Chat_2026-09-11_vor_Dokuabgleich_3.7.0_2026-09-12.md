# Glide – kompakte Weitergabe an einen neuen Chat

Stand: 12.09.2026. Diesen Text als Kontext für die Fortsetzung verwenden.

## Auftrag und aktuelle Prioritäten

Glide ist eine lokale, deutschsprachige Aufgabenanwendung für macOS und Windows. Arbeite pragmatisch, datenschonend und mit möglichst wenigen Abhängigkeiten. Bestehende Funktionen und Nutzerdaten bewahren.

Der Nutzer möchte mögliche Erweiterungen gegenüber Todoist, Microsoft To Do, Planner und Google Keep beurteilen. Seine jüngste Korrektur ist maßgeblich:

1. **Erinnerungen haben Vorrang.** Datum/Uhrzeit und Wiederholungen existieren; eine verlässliche Erinnerungsfunktion fehlt.
2. **Pinnwand und Reiteransicht für Listenelemente sind ausdrücklich erwünscht.** Vorläufige Lesart der Reiter: Aufgaben oder Aufgabengruppen innerhalb einer bestehenden Liste. Die genaue Ebene ist noch offen.
3. **Keine zusätzlichen Ablagefächer oder parallele Statusverwaltung:** „In Bearbeitung“ und Labels erfüllen diesen Zweck bereits.
4. **Keine neue Projektmappe als Datenstruktur:** Ordner, Listen, Beschreibungen und Anhänge existieren. Ein möglicher Mehrwert wäre lediglich eine ergänzende Ansicht derselben Inhalte.

Die separate [Vorschlagsdatei](Glide_Funktionsvorschlaege_2026-09-11.md) enthält die Zukunftsideen. Diese Funktionen wurden noch nicht implementiert; die Ideensammlung ist keine pauschale Umsetzungsfreigabe. Der jüngste Umsetzungsauftrag betrifft den konsistenten Vorlageneditor, Mac-Dropdowns sowie dynamische Ordner-/Listenkacheln. Bei einer Fortsetzung den konkreten Auftrag des Nutzers und diese Prioritäten beachten.

## Arbeitsorte

Workspace: `~/Library/CloudStorage/OneDrive-Persönlich/Glide ToDo`

Relative Pfade ab Workspace:

- Kanonischer Code: `01_Repository/Glide/src/glide/app.pyw`
- Arbeitsregeln: `01_Repository/Glide/AGENTS.md`
- Startbare Arbeitskopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.7.0.pyw`, mit vollständigem Ressourcenordner.
- Aktuelle technische Übergabe: `01_Repository/Glide/docs/09_PROJECT_HANDOFF.md`
- Aktuelle UI-Nachträge: `01_Repository/Glide/docs/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md` und `01_Repository/Glide/docs/29_DYNAMISCHE_KACHELN_3.7.0.md`
- Produktgrenzen / Architektur: `docs/01_PRODUCT_CONSTRAINTS.md` und `docs/02_ARCHITECTURE.md` im kanonischen Projekt.

## Verifizierter Ausgangsstand

Unveröffentlichter Entwicklungsstand **3.7.0**; Aufgabenformat **12**, Einstellungen **2**, Vorlagenformat **2**. Python/Tk, lokale Ablage, ohne erforderliches Konto oder Internet.

Bereits vorhanden: verschachtelte Ordner/Listen, Aufgaben/Gruppen/Überschriften/Long-Tasks, Unterpunkte, Labels, Wichtigkeit, Fälligkeit mit Uhrzeit, Wiederholungen, Suche, Kalender, Anhänge, Papierkorb, Rückgängig, Vorlagen und Import/Export. Die Startseite enthält unter anderem analoge Uhr, Mondphase, Tagesziel und Aktivitätsanzeige.

Die vorherigen sechs Änderungswünsche wurden umgesetzt:

- Mac-Bildlauf: MouseWheel und Tk-9-TouchpadScroll; horizontale Gesten werden nicht zu vertikalem Scrollen.
- Vorlageneditor: vollständige Hell-/Dunkeldarstellung und Detailmasken wie bei normalen Aufgaben/Listen; isolierter Entwurf mit Abbruch ohne Übernahme.
- Vollständige Struktur- und Detailbearbeitung, Labels, Anhänge und relative Vorlagentermine.
- 16 Praxisvorlagen, darunter Immobilien, WordPress, WEG und Baukommunikation; reproduzierbar erzeugte Beispieldateien.
- Listenübersicht mit Pfad, Kennzahlen, Labels und getrennten Vorschauen der nächsten Aufgaben.
- Dokumentation, Ressourcen, Arbeitskopie und Beispiele abgeglichen; alte Dateien nachvollziehbar archiviert, keine endgültige Löschung und keine Änderung echter Nutzdaten.

Die jüngsten UI-Nachträge sind ebenfalls im kanonischen Code umgesetzt:

- Vorlagenbaum im App-Stil mit passenden Farben, gerundeter Fläche, App-Scrollleisten, dynamischen Metadaten und erhaltenen geöffneten/geschlossenen Zweigen.
- `MacOptionMenu` verwendet auf macOS App-Farben für Feld und Auswahlfenster; Tastatur, Abbruch und modale Dialogrückgabe sind berücksichtigt. Windows/Linux behalten `tk.OptionMenu`.
- Ordner-/Listenkacheln ohne redundante Typzeile, mit eigener Inhaltshöhe in 1–3 unabhängig gestapelten Spalten; 16 Pixel Innenabstand, 12 Pixel zwischen Kacheln. Die zyklische Eintragszuordnung bleibt stabil; Spaltenenden dürfen unterschiedlich hoch sein.
- Vollständige Öffnen-/Bearbeiten-Beschriftung, bei Bedarf zweizeilige Aktionen und automatisches Scrollen beim Tastaturfokus. Keine Änderung des Datenformats oder realer Nutzdaten.

## Prüfstand und Grenzen

Der jüngste vollständige Prüflauf ist erfolgreich: elf Testsuiten, Syntax, Versionskonsistenz, Dokumentation, zwei statische Analysen und Beispiel-/Releaseabgleiche. Nachweis: `01_Repository/Glide/tests/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json`, Exitcode 0, macOS/Python 3.14.5. Die gesonderten Geometriedaten liegen daneben in `geometrie.json` (18 Bestandsansichten, 194–436 Pixel Kachelhöhe). Startbare Arbeitskopie und alle sieben Ressourcen sind bytegleich mit dem Projekt. Der vollständige Vorlagen-/Mac-Nachtrag ist enthalten.

**Weiter offen:** physischer Trackpad-Test und vollständige native Sichtabnahme, weitere DPI-/Monitor-Konfigurationen, Screenreader, Langzeitbetrieb, Installer und Signierung. Automatisierte Widgettests belegen keine abgeschlossene manuelle Abnahme. Die letzten beiden Computer-Use-Versuche blieben bei ausstehenden Accessibility-/Screen-Recording-Freigaben stehen. Keine native Windows-Sichtprüfung erfolgt; der unveränderte Windows-Widgetpfad wurde auf dem Mac getestet.

## Regeln für weitere Implementierung

- Vor Codeänderungen `AGENTS.md` lesen, Ausgangstest und Nutzdatenpfade prüfen. Tests ausschließlich mit isoliertem `GLIDE_DATA_DIR`.
- Datenformatänderungen benötigen Migration, Originalsicherung und passende Tests.
- Bestehende Änderungswege `item_change`, `sidebar_change`, `guarded_structural_change` und `run_modal` verwenden; Symbole aus `ICONS`.
- Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung. Vor dem Überschreiben bestehender Dokumente den Originalstand im lokalen Archiv sichern.
- Kanonischen Code, startbare Arbeitskopie und Ressourcen konsistent halten. Prüfgrenzen offen nennen.
- OneDrive ist externe Dateisynchronisation, kein sicherer gleichzeitiger Mehrbenutzerbetrieb.
- Aufgabenbackups enthalten derzeit weder persönliche Einstellungen noch den separaten Vorlagenkatalog.

Nächster sinnvoller Einstieg: Erinnerungen anhand der separaten Vorschlagsdatei konkretisieren; Auslösung bei laufender/geschlossener App, nach Ruhezustand und Neustart getrennt prüfen. Vorhandene Fristen- und Wiederholungslogik wiederverwenden. Pinnwand und Reiter müssen bestehende Objekte referenzieren und dürfen keine parallelen Aufgabenkopien erzeugen.
