# Glide Shell – bestehende Anwendung in die Shell überführen (Anleitung und Startprompt für KI-Agenten)

Stand 28.11.2026 · Glide 1.0.3 · Glide-System V1.95 · Glide Shell 0.9.1 · Glide Bento 0.3.0 · [English version](AI_MIGRATION_EXISTING_APPS.md)

Diese Datei gilt für Anwendungen, die **schon existieren** und eine eigene Oberfläche haben, etwa STEPS oder Chess & Chains. Für ein neues Projekt gilt [KI_ANLEITUNG_NEUE_PROJEKTE.md](KI_ANLEITUNG_NEUE_PROJEKTE.md). Beide Dateien liegen im Shell-Paket und kommen mit jeder Übernahme ins Projekt.

## 1. Worum es geht

Die Glide Shell ist das Fundament der Anwendung, keine Bibliothek, aus der man einzelne Teile holt. Falsch ist: Die Anwendung behält ihr eigenes Theme-System, ihre eigenen Knöpfe und ihre eigene Fensterverwaltung und importiert daneben ein paar Shell-Bausteine. Dann gibt es zwei Theme-Systeme, zwei Knopfarten und widersprüchliche Regeln. Richtig ist: Die vorhandene **Fachlogik** wandert kontrolliert in die Architektur der Shell, und die eigenen allgemeinen UI-Teile werden Schritt für Schritt abgelöst. Die Fachlogik wird dabei nicht neu geschrieben.

Verbindlich sind der [Shell-First-Vertrag](DESIGN_RICHTLINIEN.md#5-shell-first-vertrag-d105-d106) (Abhängigkeiten, Entscheidungsreihenfolge, Ausnahmen), die Gestaltungsregeln in [DESIGN_RICHTLINIEN.md](DESIGN_RICHTLINIEN.md) und die Bausteintabelle in [README.de.md](README.de.md).

## 2. Ablauf

| Schritt | Was | Ergebnis, das du festhältst |
|---|---|---|
| 1 | Fachfunktionen inventarisieren (jede Funktion, ihr Einstieg, ihre Daten) | Liste in `docs/` des Projekts |
| 2 | Datenmodelle und Speicherorte inventarisieren | Schema, Formatversion, Pfade, Sicherungen |
| 3 | Vorhandene Tests prüfen und laufen lassen | Ausgangsstand grün oder mit benannten Lücken |
| 4 | UI-Teile trennen: **allgemein** (Fenster, Dialog, Knopf, Feld, Menü, Kürzel, Farben, Scrollen) gegen **fachlich** (Brett, Notation, Akkordraster …) | Tabelle mit Zuordnung |
| 5 | Konkurrierende Framework-Funktionen benennen: eigene Theme-Tabelle, eigene Dialogfabrik, eigener Undo-Stapel, eigene Pfadlogik | Liste mit dem passenden Shell-Baustein je Eintrag |
| 6 | Shell (und bei Bedarf Bento) übernehmen: `python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --mit-bento <projekt>/src/<app>` | `SHELL_MANIFEST.json`, `BENTO_MANIFEST.json` |
| 7 | Host über `app_host` aufbauen (Hauptfenster, Startprüfung, Menü, Kürzel, Beenden) | Start über den App-Host |
| 8 | Fachlogik anbinden: bestehende Module bleiben, der Host ruft sie | keine Fachlogik in Shell oder Bento |
| 9 | Ansichten Stück für Stück auf Shell-Bausteine umstellen (`modal_session`, `custom_controls`, `desktop_adapter`, `window_geometry`, `command_history` …) | je Ansicht eine Vorher-/Nachher-Notiz |
| 10 | Farben als Rollenwörterbuch an Shell und Bento geben (`system_appearance.resolve`, `BentoContext.for_host`) | eine Farbquelle |
| 11 | Bento einsetzen, wo Karten oder Raster fachlich passen | – |
| 12 | Nutzerdaten erhalten: vor jeder Umstellung sichern, Format nur mit Migration und Rückweg ändern | Sicherung und Prüfprotokoll |
| 13 | Verhalten vorher und nachher vergleichen (gleiche künstliche Daten, gleiche Bedienwege) | Vergleichsprotokoll |
| 14 | Redundante allgemeine Komponenten erst nach grünem Vergleich entfernen | Löschliste mit Begründung |
| 15 | Regressionstests und `python -m glide_shell.conformance src/<app>` | „conform“ |
| 16 | Native Sicht- und Bedienprüfung auf den Zielplattformen | Befund je Plattform |

## 3. Nutzerdaten

- Nie mit echten Nutzerdaten testen; Datenordner der Tests über eine Umgebungsvariable isolieren, bevor das App-Modul importiert wird.
- Vor dem ersten Start der umgestellten Fassung eine bytegleiche Sicherung des alten Datenbestands anlegen.
- Eine ältere Fassung darf einen neueren Bestand nicht überschreiben (Formatversion prüfen, sonst nur lesen).
- Funktionen dürfen bei der Umstellung nicht verloren gehen. Fehlt in der Shell ein Baustein, bleibt die alte Lösung bis zur Framework-Erweiterung stehen. Das wird als Ausnahme nach Abschnitt 5.5 des Shell-First-Vertrags festgehalten.

## 4. Konkurrierende Komponenten erkennen

Hinweise auf ein zweites allgemeines UI-System: eigene Farbkonstanten in Ansichten, eigene `Toplevel`-Dialoge mit `grab_set`, eigene Scrollleisten, eigene Undo-Liste, eigene Plattformweichen für Kürzel, eigene Fenstergrößenlogik. Jeder Treffer bekommt den passenden Shell-Baustein oder einen Ausnahmeeintrag. Ein natives Tk-Widget allein ist kein Verstoß. Es zählt, ob es allgemeine Arbeit leistet.

## 5. Tests, die nötig sind

1. `python3 -m glide_shell.selftest` in `src/<app>` (Kopie, Manifest, Geometrie; auch mit `python3 -O`).
2. `python3 -m glide_bento.selftest`, wenn Bento übernommen ist.
3. `python3 -m glide_shell.conformance src/<app>`: Schichten, öffentliche Module, Zyklen, Versionen.
4. `python3 -B <glide>/01_Repository/Glide/scripts/pflege/shell_uebernehmen.py --pruefen --mit-bento src/<app>`: Kopien unverändert.
5. Die vorhandenen Fachtests des Projekts, unverändert grün.
6. Ein Integrationstest je umgestellter Ansicht über den echten Einstieg (Start, Bedienung, Schließen, Daten unverändert).

## 6. Wann die Migration abgeschlossen ist

- Die Anwendung startet über `app_host`, alle Dialoge laufen über `modal_session`.
- Es gibt genau eine Farbquelle; die Themenfarbe wirkt in allen Ansichten.
- Keine allgemeine Komponente ist doppelt vorhanden, jede Ausnahme ist begründet eingetragen.
- `conformance` meldet „conform“, Selbsttests und Fachtests sind grün.
- Jede frühere Funktion ist erreichbar; der Vorher-/Nachher-Vergleich ist dokumentiert.
- Die native Prüfung ist je Plattform festgehalten, offene Plattformen sind benannt.

## 7. Startprompt (in eine neue Sitzung kopieren)

```text
Du überführst die bestehende Tk-Anwendung „<Projektname>“ unter <Pfad> in die Glide Shell.
Quelle der Shell: <Pfad zu glide-to-do> (https://github.com/n05a-design/glide-to-do).

Lies zuerst vollständig:
1. 01_Repository/Glide/src/glide/glide_shell/KI_MIGRATION_BESTEHENDE_ANWENDUNG.md (dieser Ablauf),
2. …/glide_shell/DESIGN_RICHTLINIEN.md, Abschnitt 5 „Shell-First-Vertrag“,
3. …/glide_shell/README.de.md (Bausteine) und, falls Karten gebraucht werden, …/glide_bento/README.de.md.

Regeln:
- Die Shell ist das Fundament. Keine zweite allgemeine UI-Architektur, keine Kopie von Shell-Bausteinen.
- Fachlogik bleibt erhalten und wird angebunden, nicht neu geschrieben.
- Nutzerdaten nie anfassen; Tests nur mit künstlichen Daten in einem isolierten Datenordner.
- Fehlt ein Baustein: als Ausnahme eintragen und den Bedarf melden, nicht selbst ein allgemeines System bauen.
- Nach jedem Schritt: Selbsttests, `python -m glide_shell.conformance src/<app>` und die Fachtests.

Arbeite die 16 Schritte aus Abschnitt 2 der Reihe nach ab. Lege vor Schritt 6 die Inventare aus Schritt 1–5 im
Projekt ab und zeige sie mir, bevor du eine allgemeine Komponente entfernst.
Abgeschlossen ist die Migration erst, wenn alle Punkte aus Abschnitt 6 erfüllt und belegt sind.
```
