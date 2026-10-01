# Glide – Entscheidungsvorlage nach der Analyse vom 01.10.2026

Stand **01.10.2026** · Bezug Glide 3.32.3 · Begleitdokument zum [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md)

Diese Vorlage sammelt die Richtungsentscheidungen, die aus der Analyse folgen. Jede Frage hat Optionen mit Vor- und Nachteilen und **eine** Empfehlung. Die Empfehlung ist kein Beschluss. Bis zur Antwort gelten D01–D08 unverändert; D07 (Animationsexport) bleibt wie bisher offen.

Kurzantwort genügt, z. B. „E01 B, E02 A, E03 B …“.

## Übersicht

| Nr. | Frage | Empfehlung | Blockiert |
|---|---|---|---|
| E01 | Rolle des GitHub-Repositorys, Git | **B** Repository wird Quelle der Wahrheit, schrittweise | CI, Doku-Pflege |
| E02 | `/morgen` = Fälligkeit, „morgen“ = Bearbeitungstag? | **B** Einheitliche Semantik | G01 |
| E03 | Gilt D06 auch für die Hinweiszeilen der Ansichten? | **B** Hinweise bei Bedarf | U02 |
| E04 | Standard der Startseite | **B** „Ruhig“ mit 4 Kacheln | U05 |
| E05 | Form der Eisenhower-Matrix | **B** Board-Gruppierung | G02 |
| E06 | Ansichtenmodell Heute/Demnächst | **B** Zwei Hauptansichten | U06 |
| E07 | Verteilung und Plattformen | **B** Paket mit eingebettetem Python + Tk 9 | Linux/Windows, N11, Tk 9.1 |
| E08 | KI-Richtung | **A** jetzt, **B** als Zukunft | N10 |
| E09 | Speicherarchitektur bei großen Beständen | **A** JSON-Pfad optimieren | P08 |
| E10 | Umgang mit dem Monolithen | **B** Tk-freie Module je Feature | T3 |

## E01 – Repository und Git

**Ausgangslage:**
- Seit 30.09. gilt „Git bleibt vertagt“.
- Das GitHub-Repository `n05a-design/glide-to-do` existiert und enthält jetzt den Laufzeitstand 3.32.3 sowie die Arbeitsvorbereitung.
- Tests, Verträge (`docs/`), CHANGELOG und Pflegewerkzeuge liegen nur lokal.
- Viele Doku-Links zeigen auf `../01_Repository/Glide/…` und sind hier nicht auflösbar.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Repository bleibt Ablage für Analyse und Laufzeitstand; Arbeit weiter lokal | Kein Umstieg | Zwei Wahrheiten; Links und Prüfungen nicht nachvollziehbar; kein CI |
| **B** Repository wird schrittweise Quelle der Wahrheit: zuerst `01_Repository/Glide` (src, tests, docs, scripts), dann Lieferung nach 07/Bundle aus dem Repository | Versionierung, Diff, CI, Rückverfolgbarkeit; Claude-Code-Sitzungen arbeiten direkt am echten Stand | Einmaliger Aufwand (Struktur, `.gitignore`, große Testprotokolle ggf. auslagern); Regel „Archivkopie vor Änderung“ wird durch Git-Historie ersetzt |
| **C** Repository nur als Archiv der Übergaben | Minimal | Verschenkt den Nutzen eines Repositorys |

**Empfehlung B.** Begründung:
- Die Arbeitsregeln (Versionen, Verträge, Hashes) passen ideal zu Git.
- Die bisherige `_Z`-/Archivkopie-Mechanik kann für die Ablage beim Inhaber bestehen bleiben.

**Folge:** Struktur `src/`, `tests/`, `docs/`, `scripts/`, `07_Python-Versionen/` als Lieferordner. CI-Grundstufe (T4).

## E02 – Bedeutung von „morgen“ in Eingabe und `/`-Befehlen

**Ausgangslage:**
- D01: Allgemeines „morgen“ setzt den **Bearbeitungstag**, „fällig/bis morgen“ die **Fälligkeit**.
- Bestehende Slash-Semantik bleibt.
- Im Code setzt `/morgen` jedoch die **Fälligkeit** (`SLASH_COMMANDS`: „fällig morgen“).
- Nach G01 bedeuten „morgen“ und „/morgen“ damit Verschiedenes.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Beibehalten wie D01; Unterschied durch Feldchips sichtbar machen | Keine Gewohnheitsänderung | Zwei Bedeutungen desselben Worts; widerspricht P1/P3; schwer zu erklären |
| **B** Einheitlich: Datum ohne Zusatz = Bearbeitungstag (auch `/morgen`); Fälligkeit nur mit „fällig“/„bis“ (`/bis morgen`, „bis Freitag“) | Ein mentales Modell, passt zu D01 und zu Things (Wann vs. Deadline) | Bestehende Gewohnheit `/morgen` ändert sich; keine Datenänderung nötig, nur Eingabe |
| **C** Einheitlich andersherum: Datum = Fälligkeit (D01 ändern) | Entspricht `/morgen` heute und Todoist-Gewohnheit | Widerspricht D01 und Glides Stärke „Bearbeitungstag zuerst“ |

**Empfehlung B.** Sie ergänzt D01 („bestehende Slash-Semantik bewahren“) um eine Ausnahme und braucht deshalb eine ausdrückliche Bestätigung. Feldchips zeigen in allen Fällen vor dem Speichern, was gesetzt wird.

## E03 – Gilt D06 auch für die Hinweiszeilen?

**Ausgangslage:**
- D06: „Hinweisgestaltung unverändert lassen“ – im Kontext eingetragen als Hinweis**block** (Seiten).
- Unabhängig davon zeigen Liste, Mein Tag, Tabelle, Pinnwand und Seite dauerhaft 2–3 Zeilen Bedienhinweise (U02).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** D06 umfasst auch diese Zeilen; unverändert | Kein Risiko für Gewohnheiten | Dauerhafter Platzverbrauch, P4/P1 verletzt |
| **B** D06 gilt nur für den Hinweisblock; Hinweiszeilen per „?“ ein-/ausklappbar, Zustand gemerkt | Platz für Inhalt, Hilfe bleibt einen Klick entfernt | Neue Nutzer sehen Hinweise erst nach Klick (abgefedert durch N06 „Erste Schritte“) |
| **C** Hinweise automatisch nach fünf Nutzungen einklappen | Selbstregulierend | Unvorhersehbar („wo ist der Text hin?“) |

**Empfehlung B.**

## E04 – Standard der Startseite

**Ausgangslage:**
- 12 von 19 Kacheln sind standardmäßig sichtbar, darunter Mondphase, Gismo-Pflege und Vorlagenwerbung.
- „Heute“ erscheint viermal.
- Teuerste Ansicht (U05).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert | Bekannt | Nur das Wesentliche (P5) verfehlt; Ladezeit |
| **B** „Ruhig“: Heute (zusammengeführt), Woche, Zuletzt, Angeheftet; alle anderen Kacheln wählbar. Gismo bleibt in leeren Zuständen und als wählbare Kachel | Klarer Tagesüberblick, schneller | Bestehende Nutzer verlieren gewohnte Kacheln (nur für neue Einstellungen ändern; Bestand behält eigene Auswahl) |
| **C** Kacheln stark reduzieren (Mondphase, Gismo, Impuls entfernen) | Weniger Code | Persönliche Note geht verloren; widerspricht dem bewusst gebauten Charakter |

**Empfehlung B.** Bestehende Einstellungen bleiben; nur der Standard für neue oder zurückgesetzte Startseiten ändert sich.

## E05 – Form der Eisenhower-Matrix (G02)

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Eigene Ansicht mit vier Quadranten | Wie TickTick | Neue Ansicht/Begriff (P6), eigener Code, Doppelung mit Board |
| **B** Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board. „Wichtig“ = Wichtigkeit ≥ 2; „dringend“ = fällig oder Bearbeitungstag ≤ heute + N Tage (einstellbar, Standard 2). Ziehen ändert die Wichtigkeit bzw. setzt den Bearbeitungstag (D02). Fälligkeiten werden nie gelöscht; „nicht dringend“ verschiebt nur den Bearbeitungstag | Nutzt `group_columns`/`set_group_value`, kein neuer Ort, klare D02-Abbildung | Quadrantenregel muss gelernt werden (durch Spaltentitel erklärt) |
| **C** Nicht umsetzen | Kein Aufwand | Lücke zu TickTick/SP bleibt |

**Empfehlung B.**

## E06 – Ansichtenmodell

**Ausgangslage:** Mein Tag, In Bearbeitung („alle mit Fälligkeit“), Verspätet, Nächste Aufgabe, Tagesbeginn, Tagesabschluss, Startseite-Heute überlappen (U06).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert | Kein Umlernen | Begriff „In Bearbeitung“ irreführend; viele Wege |
| **B** Zwei Hauptansichten: **Heute** (Mein Tag + Verspätet + Heute fällig + Nächste Aufgabe oben) und **Demnächst** (bisher In Bearbeitung, chronologisch). Tagesbeginn/-abschluss als Modi von Heute | Klar wie Things; Seitenleiste kürzer | Umbenennung; interne Kennungen bleiben (keine Datenänderung) |
| **C** Things-Modell vollständig (Heute, Demnächst, Jederzeit, Irgendwann, Logbuch) | Bewährt | Neue Begriffe/Felder („Irgendwann“) – mehr Komplexität |

**Empfehlung B.**

## E07 – Verteilung und Plattformen

**Ausgangslage:**
- Glide braucht ein separat installiertes Python.
- Volle Funktionen erst mit Tk 9 (macOS über python.org 3.14.5 gegeben).
- Linux-Distributionen liefern meist Tk 8.6; dort fehlen JPEG-Vorschau und Systemmitteilungen.
- Windows ist ungetestet.

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Status quo | Kein Aufwand | Eingeschränktes Erlebnis außerhalb macOS; Installationshürde |
| **B** Paket mit eingebettetem Python 3.14 + Tk 9 (mit Xft unter Linux) je Plattform, z. B. PyInstaller oder Briefcase; bestehendes macOS-Bundle als Vorlage | Gleiches Erlebnis überall; Voraussetzung für Tk-9.1-Barrierefreiheit und Signatur | Build-Pipeline je Plattform; Größe ≈ 30–60 MB [Einschätzung]; neue Werkzeugabhängigkeit nur beim Bauen |
| **C** Nur macOS-Bundle offiziell, Windows/Linux „wie besehen“ | Fokus | Zielplattformen Windows/Linux faktisch aufgegeben |

**Empfehlung B** nach Stufe 1. Die Werkzeugwahl (PyInstaller/Briefcase/Nuitka) ist eine eigene Abhängigkeitsentscheidung.

## E08 – KI-Richtung

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Austauschdateien (`.glideexchange`, G24 Kontextpaket, Änderungsdiff) | Vollständig lokal; Nutzer behält Kontrolle; vorhanden | Umständlich (Datei hin und her) |
| **B** Zusätzlich lokaler MCP-Server (stdio, nur bei laufender App oder als Kommando): zuerst lesend, später Änderungsvorschläge, die Glide als Diff zur Bestätigung zeigt | Moderne Assistenten (Claude, andere) arbeiten direkt mit Glide; keine Cloud in Glide | Neue Schnittstelle, Sicherheits- und Konsistenzfragen; Abhängigkeit von MCP-Spezifikation |
| **C** Eingebaute Cloud-KI | Komfort | Widerspricht Produktgrenzen (kein Cloudservice) |

**Empfehlung A jetzt (G24 in Stufe 4), B als Zukunftsoption nach G24.**

## E09 – Speicherarchitektur bei großen Beständen

**Ausgangslage:** Jede Aktion kostet linear mit dem Bestand – 56 ms bei 1.000, 458 ms bei 10.000 Punkten (T1).

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** JSON-Pfad optimieren (P08a: ein Vergleichsdurchlauf; P08b: nur geänderte Listen; T2) | Format, Backups, Lesbarkeit bleiben; kleine, messbare Schritte | Speichern bleibt O(Bestand) für das Schreiben selbst (bei 10.000 Punkten ≈ 30 ms JSON + `fsync`) |
| **B** SQLite als Hauptspeicher | Inkrementelle Schreibvorgänge | Migration, neues Datenformat, Backup-/Sync-Modell neu; Logseq zeigt, wie lang so ein Wechsel dauert |
| **C** Eine Datei je Liste | Kleinere Schreibvorgänge | Atomarität über Dateien, Sperren, Sicherungen komplexer |

**Empfehlung A.** B nur neu bewerten, wenn reale Bestände dauerhaft über 20.000 Punkte liegen. SQLite bleibt für den **Suchindex** (G14) als ersetzbarer Cache vorgesehen.

## E10 – Umgang mit dem Monolithen

| Option | Vorteile | Nachteile |
|---|---|---|
| **A** Unverändert weiterbauen | Kein Zusatzaufwand | Fachlogik nur mit Tk testbar; Suiten langsam |
| **B** Strangler: Jede neue oder angefasste Fachlogik (Parser, Wiederholung, Verlaufs-Diff, Suche, Referenzen) als Tk-freies Modul mit Unit-Tests; `ListApp` ruft auf | Kein Umbauprojekt, schnelle Tests, CI-fähig | Etwas Mehraufwand je Feature (≈ 10–20 %) |
| **C** Großer Umbau in Pakete | Saubere Architektur | Hohes Regressionsrisiko ohne umfassende schnelle Tests |

**Empfehlung B.** Bestätigt die bestehende Linie („neue Parser-/Suchlogik möglichst als Modul ohne Tk-Abhängigkeit“) und macht sie verbindlich.

## Weiterhin offen ohne neue Empfehlung

- **D07** Animationsexport (GIF vs. Frames/Spritesheet) – erst zur Pixel-Etappe.
- Inhaberangaben, Signatur/Store, Markenprüfung (Namenskollision „Glide“ mit bekannten Produkten beachten), Plattformabnahme.
