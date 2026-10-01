# STARTKONTEXT FÜR NEUEN CLAUDE-CHAT

*(Diesen Text als erste Nachricht in den neuen Chat kopieren.)*

---

Behandle den folgenden Text als den **aktuellen, verbindlichen Projektstand**.
Stelle keine Fragen, die hier bereits beantwortet sind. Wenn eine Projektdatei
diesem Text widerspricht, gilt der tatsächliche Dateistand – prüfe ihn dann,
statt zu raten. Entferne oder ändere keine bestehende Funktion ohne
ausdrücklichen Grund. Antworte auf Deutsch.

## Projekt

**Glide** – lokale Desktop-App für Aufgaben und Listen, Python 3.12 + Tkinter,
Zielplattformen Windows und macOS. Kein Konto, keine Cloud, kein Netzwerk für
Kernfunktionen. Nur Python-Standardbibliothek plus Tk. Nutzdaten außerhalb des
Programmordners. Oberfläche und Dokumentation einsprachig Deutsch.

Repository: `/home/claude/work/Glide`
Gesamter Code: `src/glide/app.pyw` (Monolith, 14.590 Zeilen, Klasse `ListApp`).

**Stand: Version 3.2.0, Datenformat 10, alle drei Testsuiten grün.**

Ausführlicher Kontext: **`docs/09_PROJECT_HANDOFF.md`** – dort stehen
Dateiübersicht, alle Nutzeranforderungen, verworfene Ansätze und
Fehlerwissen. Bei Bedarf zuerst lesen.

## Pflichtlektüre vor der ersten Änderung

`AGENTS.md` (Arbeitsregeln) · `docs/01_PRODUCT_CONSTRAINTS.md` (Produktgrenzen) ·
`docs/02_ARCHITECTURE.md` (Aufbau, Stand 3.2.0) ·
`docs/09_PROJECT_HANDOFF.md` (vollständige Übergabe).

## Zentrale Architekturregeln (nicht umgehen)

- Jede Änderung an Punkten läuft durch `item_change`, jede an Listen/Ordnern
  durch `sidebar_change`. Die Änderung meldet ihre Wirkung mit
  `ChangeRecord.mark()`; ohne Meldung entfällt der Rückgängig-Punkt.
- Jede Umbauaktion läuft zusätzlich unter `guarded_structural_change`.
  `item_change` sitzt **innerhalb**, nie darum herum.
- Auswahlprüfung immer über `selected_items_for_change`.
- Jeder modale Dialog läuft über `run_modal`. Nie `grab_set` + `wait_window`
  von Hand.
- Alle Oberflächensymbole stehen in der Tabelle `ICONS` und sind
  **ausschließlich Textzeichen, niemals Emoji** (Test erzwingt < U+1F000).
  Anhang `⊕`, Kalender `▦`, Labels `◈`.
- Datenformat 10 bleibt. Testisolierung ausschließlich über `GLIDE_DATA_DIR`.
- `.pyw` nur mit `importlib.machinery.SourceFileLoader` laden.

## Tests (alle drei müssen grün sein)

```
xvfb-run -a python3.12 tests/integration/test_glide.py
xvfb-run -a python3.12 tests/integration/test_datenintegritaet.py
xvfb-run -a python3.12 tests/integration/audit_app.py
```

Nach Layoutänderungen zusätzlich `tests/tools/screenshots.py` – ein grüner Test
hat schon einmal eine kaputte Oberfläche verdeckt.

## Kürzlich abgeschlossen – nicht wiederholen

- **3.1.0:** gemeinsamer Änderungsrahmen eingeführt (31 von 39
  `undo_stack.pop()`-Stellen ersetzt), `run_modal`, drei strukturgleiche
  Methodenpaare zusammengeführt, Undo-Kürzungsfehler behoben.
- **3.2.0:** Verzeichnis-Migration und `LEGACY_LABEL_COLOR_MAP` entfernt
  (auf ausdrücklichen Nutzerwunsch), alle Emoji durch Textzeichen ersetzt,
  umfangreiche Beispieldaten erzeugt
  (`tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup`, erzeugt von
  `tests/tools/beispieldaten.py`).
- **Code-Überprüfung Etappen 1–4 abgeschlossen.** Insbesondere: Die 20 breiten
  `except Exception` wurden vollständig geprüft – 19 sind an ihrer Stelle
  richtig. Diese Analyse nicht wiederholen.

## Bekannte Fehler und Risiken

1. **App friert zeitweise ein** (gemeldet zu 3.0.1). Ursache gefunden und
   behoben: `grab_set`/`wait_window` gaben den Griff nicht zurück, wodurch eine
   Maske sichtbar blieb, aber keine Eingabe mehr annahm. **Nie reproduziert –
   Status: nicht verifiziert.** Bestätigung nur durch Benutzung auf Windows.
2. **Datenverlust beim Auflösen einer Gruppe** – früher aufgetreten, durch
   `guarded_structural_change` abgesichert. Diesen Bereich besonders vorsichtig
   behandeln.
3. **`insert_tree_items`** ist neun Ebenen tief verschachtelt – der
   wahrscheinlichste Ort für einen stillen Fehler.
4. **Nichts wurde je auf Windows oder macOS geprüft.** Alle Prüfläufe liefen
   unter Linux/Xvfb.
5. **Fallstrick:** `sync_current_list_reference()` schreibt `app_title` in den
   Titel der aktiven Liste zurück. Wer `active_list_id` von Hand umsetzt, ohne
   `app_title` mitzuziehen, benennt beim nächsten `save_items()` eine Liste um.
6. `docs/decisions/PRODUCT_IDENTITY.md` ist veraltet und nennt fälschlich
   Datenformat 9.

## Verworfen – nicht erneut vorschlagen

Dunkelblau im Dunkelmodus (bleibt grau) · selbstgezeichnete
Ordner-Klappdreiecke · Emoji als Symbole · Fixtures oder Formatprüfung
entfernen · Import-/Backup-Wege in den `item_change`-Rahmen zwingen ·
Umbenennen beim Klick aufs Klappdreieck.

## Nächste Aufgaben

- **P1 – empfohlen als Erstes:** Dokumentation auf 3.2.0 nachziehen
  (`docs/decisions/PRODUCT_IDENTITY.md`, `docs/07_QA_BERICHT.md`,
  `docs/10_RELEASE_CHECKLIST.md`). Risikolos, beseitigt eine echte Fehlerquelle.
- **P1:** manuelle Prüfmatrix Windows/macOS; Build-Kette (PyInstaller, Signing,
  Notarisierung); Produktidentität festlegen (Inhaberentscheidung).
- **P2, Entscheidung des Nutzers offen:** Drag & Drop für Anhänge – bräuchte
  eine externe Bibliothek (gegen Projektregel) oder einen Win32-Eingriff.
  Nicht ohne Freigabe bauen.
- **P3:** Etappe 5 der Code-Überprüfung, beginnend mit `insert_tree_items`.

## Arbeitsweise

Lösungsorientiert, präzise, direkt. Kleine, einzeln prüfbare Schritte. Kein
Datenverlust. Bestehendes Verhalten bei Refactorings exakt erhalten. Ehrlich
über den Status berichten – was nicht reproduziert wurde, gilt nicht als
behoben. Symbole, Farben und Layout sind Nutzerentscheidungen: Abweichungen
vorlegen statt umsetzen. `CHANGELOG.md` und betroffene Dokumentation immer
mitführen.
