# Glide – Entscheidungsvorlage nach der Analyse vom 01.10.2026

Stand **01.10.2026** · Glide 3.32.3 · Begleitdokument zum [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md)

Diese Vorlage sammelt die Richtungsentscheidungen, die aus der Analyse folgen. Jede Frage hat Optionen mit Vor- und Nachteilen und **eine** Empfehlung. Die Empfehlung ist kein Beschluss.

- Die Nummerierung setzt die verbindlichen Entscheidungen D01–D08 fort; D07 (Animationsexport) bleibt wie bisher offen.
- Bis zur Antwort gelten D01–D08 unverändert.
- Bereits beantwortete Fragen werden nicht erneut gestellt:
  - Q3 „Dokumente statt Schnittstelle“,
  - G07 „kein systemweiter Hotkey“,
  - „kein Einstieg für neue Nutzer“,
  - Stufe C der Systembenachrichtigungen,
  - eigene Felder je Liste.

Kurzantwort genügt, z. B. „D09 B, D10 A, D11 B …“.

## Übersicht

| Nr. | Frage | Empfehlung | Blockiert |
|---|---|---|---|
| D09 | Rolle des GitHub-Repositorys, Git, Ablageregeln | **B** Repository wird Quelle der Wahrheit | CI, G27, Doku-Pflege |
| D10 | `/morgen` = Fälligkeit, „morgen“ = Bearbeitungstag? | **B** Einheitliche Semantik | G01 |
| D11 | Gilt D06 auch für die Hinweiszeilen der Ansichten? | **B** Hinweise bei Bedarf | U02 |
| D12 | Standard der Startseite | **B** „Ruhig“ mit 5 Kacheln inkl. Gismo | U05 |
| D13 | Form der Eisenhower-Matrix (G02) | **B** Board-Gruppierung | G02 |
| D14 | Ansichtenmodell Heute/Demnächst | **B** Zwei Hauptansichten | U06 |
| D15 | Verteilung und Plattformen (G26/H-03) | **B** Paket mit eingebettetem Python + Tk 9 | Linux/Windows, Tk 9.1 |
| D16 | Speicherarchitektur bei großen Beständen | **A** JSON-Pfad optimieren (P08) | P08 |
| D17 | Umgang mit dem Monolithen (G27) | **B** Tk-freie Module je Feature | T3 |

## D09 – Repository, Git und Ablageregeln

**Ausgangslage:**
- Seit 30.09. gilt „Git bleibt vertagt“ (ARBEITSRICHTUNG). G27 „Aufteilen von `app.pyw`“ wartet ausdrücklich auf eine Versionsverwaltung.
- Am 01.10.2026 wurde die komplette Projektablage nach GitHub (`n05a-design/glide-to-do`) hochgeladen.
- Im Zuge dieser Analyse auf die Projektstruktur ausgerichtet: Wurzel = Projektordner, Quellbaum in `01_Repository/Glide`. Siehe [Bestandsaufnahme §4](Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md#4-ablage-im-repository-upload-01102026).
- Offen sind drei Regeln:
  - Prüfprotokolle `*.log` schließt `Glide/.gitignore` aus.
  - Das 286 MB große Zwischenstandsabbild `93_Zwischenstände` verdoppelt den Bestand.
  - Künftige Uploads müssen dieselbe Struktur behalten.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Repository bleibt Ablagekopie; Arbeit weiter lokal, gelegentliche Uploads | Kein Umstieg | Zwei Wahrheiten; Uploads können wieder verrutschen; kein CI; G27 bleibt blockiert |
| **B** Repository wird Quelle der Wahrheit: lokaler Projektordner = Git-Arbeitskopie (Wurzel wie hier); Prüfprotokolle `tests/qa-*/**/*.log` freigeben; neue Zwischenstandsabbilder durch Git-Tags ersetzen, bestehende als Beleg behalten; `_Z`/Archivregeln bleiben für die Ablage | Versionierung, Diff, CI, Rückverfolgbarkeit; Claude-Code-Sitzungen arbeiten am echten Stand; G27 wird möglich | Einmalige Umstellung (Git-Client, Arbeitsweise); Repository wächst mit Belegen (Bilder, Sicherungen) |
| **C** Repository nur als Archiv der Übergaben | Minimal | Verschenkt den Nutzen |

**Empfehlung B.** Die Arbeitsregeln (Versionen, Verträge, SHA-256) passen ideal zu Git, und die Strukturkorrektur ist bereits erledigt.

**Folgen:**
- „Git vertagt“ in ARBEITSRICHTUNG/Übergabe ersetzen.
- Ausnahmen für Logs in `Glide/.gitignore`.
- CI-Grundstufe (T4).
- Upload-Regel: Projektordner in die Repository-Wurzel, nie in einen Unterordner.

## D10 – Bedeutung von „morgen“ in Eingabe und `/`-Befehlen

**Ausgangslage:**
- D01: Allgemeines „morgen“ setzt den **Bearbeitungstag**, „fällig/bis morgen“ die **Fälligkeit**.
- D01 bewahrt zugleich die bestehende Slash-Semantik.
- Im Code setzt `/morgen` jedoch die **Fälligkeit** (`SLASH_COMMANDS`: „fällig morgen“).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Beibehalten wie D01; Unterschied durch Feldchips sichtbar machen | Keine Gewohnheitsänderung | Zwei Bedeutungen desselben Worts; widerspricht P1/P3 |
| **B** Einheitlich: Datum ohne Zusatz = Bearbeitungstag (auch `/morgen`); Fälligkeit nur mit „fällig“/„bis“ (`/bis morgen`) | Ein mentales Modell, passt zu D01 und Things (Wann vs. Deadline) | Gewohnheit `/morgen` ändert sich; nur Eingabe, keine Datenänderung |
| **C** Einheitlich andersherum: Datum = Fälligkeit (D01 ändern) | Entspricht `/morgen` heute und Todoist | Widerspricht D01 und Glides Stärke „Bearbeitungstag zuerst“ |

**Empfehlung B.** Sie ergänzt D01 um eine Ausnahme und braucht deshalb eine ausdrückliche Bestätigung. Feldchips zeigen in allen Fällen vor dem Speichern, was gesetzt wird.

## D11 – Gilt D06 auch für die Hinweiszeilen?

**Ausgangslage:**
- D06 „Hinweisgestaltung unverändert lassen“ wurde im Kontext des Hinweis**blocks** in Seiten beantwortet.
- Unabhängig davon zeigen Liste, Mein Tag, Tabelle, Pinnwand und Seite dauerhaft 2–3 Zeilen Bedienhinweise (U02).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** D06 umfasst auch diese Zeilen; unverändert | Kein Risiko für Gewohnheiten | Dauerhafter Platzverbrauch (P4/P1) |
| **B** D06 gilt nur für den Hinweisblock; Hinweiszeilen per „?“ ein-/ausklappbar, Zustand gemerkt | Platz für Inhalt, Hilfe einen Klick entfernt | Hinweise erst nach Klick sichtbar |
| **C** Hinweise automatisch nach fünf Nutzungen einklappen | Selbstregulierend | Unvorhersehbar |

**Empfehlung B.**

## D12 – Standard der Startseite

**Ausgangslage:**
- 12 von 19 Kacheln sind standardmäßig sichtbar; „Heute“ erscheint viermal; die Startseite ist die teuerste Ansicht (U05).
- Gismo soll laut Entscheidung „Arbeitsbegleiter“ in der Standardreihenfolge hoch stehen.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert | Bekannt | P5 verfehlt; Ladezeit |
| **B** „Ruhig“: Heute (Tagesziel + eingeplant + nächste Aufgabe zusammengeführt), Gismo, Woche, Zuletzt, Angeheftet; alle anderen Kacheln wählbar | Klarer Überblick, schneller, Gismo bleibt | Nur für neue/zurückgesetzte Startseiten; Bestand behält eigene Auswahl |
| **C** Kacheln entfernen (Mondphase, Impuls …) | Weniger Code | Persönliche Note geht verloren |

**Empfehlung B.**

## D13 – Form der Eisenhower-Matrix (G02)

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Eigene Ansicht mit vier Quadranten (wie G02 ursprünglich beschrieben) | Wie TickTick | Neue Ansicht (P6), Doppelung mit Board |
| **B** Board-Gruppierung „Dringlichkeit × Wichtigkeit“ in der vorhandenen Pinnwand. Abbildung der Quadranten und Wirkung beim Ziehen siehe unten | Nutzt `group_columns`/`set_group_value`; kein neuer Ort; klare D02-Abbildung | Quadrantenregel muss gelernt werden (Spaltentitel erklären) |
| **C** Nicht umsetzen | Kein Aufwand | Lücke bleibt |

Abbildung bei Option B:
- „Wichtig“ = Wichtigkeit ≥ 2.
- „Dringend“ = fällig oder Bearbeitungstag ≤ heute + N Tage (Standard 2).
- Ziehen ändert die Wichtigkeit bzw. den Bearbeitungstag (D02).
- Fälligkeiten werden nie gelöscht.

**Empfehlung B.**

## D14 – Ansichtenmodell

**Ausgangslage:**
- Mein Tag, In Bearbeitung („alle mit Fälligkeit“), Verspätet, Nächste Aufgabe, Tagesbeginn/-abschluss und Startseite-Heute überlappen.
- Die Produktgrenzen verlangen bereits: keine Seitenleistenzeile als zweiter Weg (U06).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert | Kein Umlernen | „In Bearbeitung“ irreführend; viele Wege |
| **B** **Heute** (Mein Tag + Verspätet + Heute fällig + Nächste Aufgabe oben) und **Demnächst** (bisher In Bearbeitung, chronologisch); Tagesbeginn/-abschluss als Modi von Heute | Klar wie Things | Umbenennung; interne Kennungen bleiben |
| **C** Things-Modell vollständig (Heute, Demnächst, Jederzeit, Irgendwann, Logbuch) | Bewährt | Neue Begriffe/Felder |

**Empfehlung B.**

## D15 – Verteilung und Plattformen (G26/H-03)

**Ausgangslage:**
- G26 ist „ja, vorbereiten“.
- Glide braucht ein separat installiertes Python; volle Funktionen erst mit Tk 9 (macOS über python.org ab 3.14.5).
- Linux-Distributionen liefern meist Tk 8.6 (keine Mitteilungen, kein SVG, keine JPEG-Vorschau). Windows ist ungeprüft.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Status quo | Kein Aufwand | Eingeschränkt außerhalb macOS; Installationshürde |
| **B** Paket mit eingebettetem Python 3.14 + Tk 9 (Linux mit Xft) je Plattform; bestehendes macOS-Bundle als Vorlage | Gleiches Erlebnis überall; Voraussetzung für Tk-9.1-Barrierefreiheit und Signatur | Build-Pipeline je Plattform; Werkzeugwahl ist eigene Abhängigkeitsentscheidung |
| **C** Nur macOS offiziell | Fokus | Zielplattformen Windows/Linux faktisch aufgegeben |

**Empfehlung B** nach Stufe 1.

## D16 – Speicherarchitektur bei großen Beständen

**Ausgangslage:** Jede Aktion kostet linear mit dem Bestand: Abhaken 56 ms bei 1.000 und 446 ms bei 10.000 Punkten (T1).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** JSON-Pfad optimieren (T2, P08a, P08b) | Format, Sicherungen, Lesbarkeit bleiben; kleine messbare Schritte | Schreiben bleibt O(Bestand) (10.000 Punkte ≈ 30 ms JSON + `fsync`) |
| **B** SQLite als Hauptspeicher | Inkrementelles Schreiben | Neues Datenformat, Migration, Sicherungs-/Sync-Modell neu; Logseq zeigt die Dauer eines solchen Wechsels |
| **C** Eine Datei je Liste | Kleinere Schreibvorgänge | Atomarität, Sperren, Sicherungen komplexer |

**Empfehlung A.** B nur neu bewerten, wenn reale Bestände dauerhaft über 20.000 Punkte liegen. SQLite bleibt für den Suchindex (G14) als ersetzbarer Cache vorgesehen.

## D17 – Umgang mit dem Monolithen (G27)

**Ausgangslage:** G27 „Aufteilen von `app.pyw`“ (L) wartet auf die Versionsverwaltung (D09).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert weiterbauen | Kein Zusatzaufwand | Fachlogik nur mit Tk testbar; Suiten langsam |
| **B** Strangler: Jede neue oder angefasste Fachlogik (Parser, Wiederholung, Verlaufs-Diff, Suche, Referenzen) als Tk-freies Modul mit Unit-Tests; `ListApp` ruft auf. G27 wird so schrittweise erledigt | Kein Umbauprojekt, schnelle Tests, CI-fähig | ≈ 10–20 % Mehraufwand je Feature |
| **C** G27 als großer Umbau | Saubere Architektur | Hohes Regressionsrisiko ohne schnelle Tests |

**Empfehlung B.** Sie bestätigt die bestehende Linie („neue Parser-/Suchlogik möglichst als Modul ohne Tk-Abhängigkeit“) und macht sie verbindlich.

## Weiterhin offen ohne neue Empfehlung

- **D07** Animationsexport (GIF vs. Frames/Spritesheet) – erst zur Pixel-Etappe.
- Inhaberangaben, Signatur/Store, Markenprüfung (Namenskollision „Glide“ mit bekannten Produkten beachten), Plattformabnahme ([Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md)).
- Erste Importquelle für F-02/G21.
