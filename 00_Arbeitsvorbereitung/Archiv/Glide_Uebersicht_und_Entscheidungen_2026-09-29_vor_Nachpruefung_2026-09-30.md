# Glide – Übersicht und Entscheidungsmöglichkeiten vom 29.09.2026

Stand 29.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Entscheidungsvorlage, Antworten offen

Auftrag vom 29.09.2026: offene Punkte, Entscheidungen, Aufgaben und neue
Funktionen erforschen – auch im Vergleich mit der
[Wettbewerbsrecherche](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
und den Notion-Bildschirmfotos des Inhabers – und daraus Möglichkeiten für
Entscheidungen in Behebung, Entwicklung und Forschung zusammenstellen.

**So antworten:** „Alle Empfehlungen“ reicht. Sonst je Kennung, etwa
„B1 ja, E2 später, F4 nein“. Die Antworten gehören in Abschnitt 8.

Aufwand: S bis ein halber Tag, M bis zwei Tage, L mehr. Jede Umsetzung
bekommt wie bisher Tests, Doku und einen Vollprüflauf.

## 1. Kurzantworten auf die Fragen vom 29.09.2026

- **Logo als SVG oder PNG?** SVG.
  - Tk 9 rechnet SVG in jeder Größe scharf.
  - Die Akzentfarbe ist zuverlässig und kein Risiko: Glide ersetzt vor dem
    Rechnen nur den einen Füllwert `rgb(1,133,225)` im SVG-Text. Das dauert
    unter einer Millisekunde; `test_logo330` prüft es in fünf Designs.
  - Voraussetzung ist, dass der Master einfarbig bleibt.
  - Unter Tk 8.6 zeichnet Glide das Zeichen als Fläche. Die PNGs dienen
    dort als Programmsymbol.
- **Wie kommt man zur globalen Suche?** Drei Wege öffnen dieselbe Suche über
  Seiten, Punkte und Aktionen:
  - die Lupe ⌕ in der Kopfzeile (neu, links neben ⌘);
  - Strg+O bzw. Cmd+O;
  - Ansicht › Ansichten › „Seite, Punkt oder Aktion suchen …“.
- **Ist die manuelle Prüfung noch aktuell?** Nur zum kleineren Teil. Von
  201 alten Punkten prüfen Suiten 119 automatisch, 34 davon mit offenem
  „Handgefühl“; 6 sind überholt. 40 bleiben von Hand, gebündelt in fünf
  Sitzungen der
  [verdichteten Prüfliste](Checklisten/Manuelle_Pruefung_3.30.0.md).
- **Sind die Copyright-Vorschläge fertig?** Ja: die
  [Inhaberangaben](../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md)
  (Copyright, Datenschutz-URL, Sicherheitskontakt, Inno-AppId). Es fehlt
  nur deine Bestätigung (I1).
- **Lassen sich in Seiten und Notizen Ordner anlegen wie in Listen?** Ja,
  schon vorher:
  - „Bibliothek“ im Seitenbereich, „Notizbuch“ im Notizbereich;
  - Unterordner über das Kontextmenü.

  Neu seit heute:
  - „+“ und „…“ beim Überfahren in allen drei Bereichen;
  - ein Unterordner erbt die Art (Bibliothek oder Notizbuch).
- **Listen ließen sich nicht zuklappen:** behoben. Der Neuaufbau der
  Seitenleiste klappte den Ordner der geöffneten Liste jedes Mal wieder auf.

## 2. Heute umgesetzt

Vertrag 66, [Abschnitte 2.15 und 2.16](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md);
die Antworten zur Prüfung vom 28.09.2026 stehen
[dort in Abschnitt 7](Glide_Pruefung_und_Entscheidungen_2026-09-28.md).

- Logo, Lupe, Startseite ohne Eingabeleiste, Inhaltskarten bis ganz unten;
- Sicherungen nur bei Änderung, Startprüfung, Belastungstest (fand und
  behob verwaiste Verweise);
- Seitenleiste: „Notizen +“, Einklappen, Ordner in allen Bereichen;
- nebenbei: Notiztext in kleinen Fenstern, Fokusrahmen, bündige
  Übersichten, Titel-Doppelklick in Übersichten, ein Tk-9-Effekt auf der
  Startseite, Vorlagen-Archiv abgeglichen.
- Die Prüflisten sind verdichtet, veraltete Doku ist berichtigt, und
  überflüssige Ordner sind mit `_Z` markiert (Abschnitt 7).

## 3. Behebung – bekannte Lücken

| Nr. | Befund | Möglichkeiten | Empfehlung | Aufwand |
|---|---|---|---|---|
| B1 | Die Seitenleiste hat drei Bäume, die jeder für sich scrollen. Bei Mindesthöhe bleibt Seiten und Notizen je eine Zeile. | a) so lassen; b) die ganze Leiste scrollt wie in Notion, jeder Baum zeigt alle Zeilen | a) jetzt, b) wenn die kleinen Bereiche im Alltag stören | b: M |
| B2 | Im Seiten- und Notizbaum gibt es kein Ziehen; Verschieben geht über das Kontextmenü. | a) so lassen; b) Ziehen wie im Listenbaum, auch zwischen den Bereichen | b | M |
| B3 | Eine leere Notiz zeigt über dem Text einen Punktbereich mit „Noch keine Punkte vorhanden“ und Knopf. Das ist Form ohne Inhalt. | a) so lassen; b) leer nur eine Zeile „+ Punkt“, der Bereich wächst mit dem ersten Punkt | b | S |
| B4 | Bilder in Seiten: zwei Bilder auf gleicher Höhe können sich überlappen; Druck und „Markdown kopieren“ zeigen nur Dateinamen (Vertrag 66 §11). | a) so lassen; b) Überlappung verhindern; c) Bilder auch in Druck und PDF | b und c | M |
| B5 | Unter Windows und Linux ungeprüft: Vorschauen (WIC), Ziehen aus dem Explorer, Systemmitteilung, Lupe ⌕. | nur mit der Windows-Vollprüfung und Sitzung B | Vollprüfung mit Python 3.14 (I6) | – |
| B6 | Echter Windows-Bestand noch in Format 17. | Seit heute stellt der Start ihn selbst um, mit Vorsicherung. | vorher eine Vollsicherung `.glidebackup` (B2 der Prüfliste) | – |
| B7 | Tk 9.0.3 blendet eingebettete Rahmen einer ausgeblendeten Leinwand wieder ein. Umgangen, aber ein Tk-Fehler. | a) nur umgehen; b) zusätzlich mit dem Nachstellbeispiel an Tcl/Tk melden | b (braucht ein Konto bei core.tcl-lang.org) | S |

## 4. Entwicklung – Technik für Produktion und spätere Apps

| Nr. | Thema | Möglichkeiten | Empfehlung | Aufwand |
|---|---|---|---|---|
| E1 | `app.pyw` hat rund 52.000 Zeilen. | a) Monolith lassen; b) schrittweise in Module teilen, je Schritt Vollprüfung | b, sobald eine Versionsverwaltung da ist (Antwort 6: vorerst nicht); bis dahin nur neue Teile als Modul, wie `logo.py` | L |
| E2 | Reihenfolge der Aufteilung | Vorschlag: 1. Speichern, Sicherung, Migration; 2. Seitenleiste; 3. Notiz- und Seiteneditor; 4. Pinnwand; 5. Startseite; 6. Dialoge | so | – |
| E3 | Paket für macOS und Windows | PyInstaller ab 6.22 (unterstützt Tk 9) mit fester Version und Spezifikationsdatei, eingebettetes Python 3.14; dazu `pyproject.toml` für Version und Abhängigkeiten | vorbereiten; Signatur und Notarisierung erst mit I3 | M |
| E4 | Linux-App | a) später; b) AppImage oder Flatpak untersuchen | a | – |
| E5 | Automatische Prüfung auf allen drei Systemen | GitHub Actions mit macOS, Windows und Linux (virtueller Bildschirm) | erst mit Versionsverwaltung | M |
| E6 | Tempo bei sehr langen Listen | Nur sichtbare Zeilen aufbauen. Der Belastungstest zeigt 26.420 Punkte in 0,6 s beim Speichern; das Zeichnen ist nicht gemessen. | erst messen, dann entscheiden | S (Messung) |

## 5. Forschung und neue Funktionen

Aus der Wettbewerbsrecherche und den Notion-Bildern; nichts davon ist
angefangen.

| Nr. | Funktion | Nutzen | Einordnung | Empfehlung | Aufwand |
|---|---|---|---|---|---|
| F1 | Inhaltsverzeichnis in Seiten | Lange KI-Berichte schnell durchqueren; passt zu „eine Seite, unendlich scrollend“ | Notion-Block „Table of contents“ | ja | S |
| F2 | Aufklappblöcke und Hinweisblöcke in Seiten | Gliedern ohne Unterseiten; Hinweise hervorheben | Notion „Toggle“ und „Callout“ | ja | M |
| F3 | Spalten in Seiten | Text neben Text | Weg A (ein Textfeld) trägt das nur eingeschränkt | nein | L |
| F4 | Titelbild für Seiten, auch als Pixelzeichnung | Wiedererkennung, stärkt die Pixel-Nische | offen seit 26.09. | ja, mit Pixelzeichnung | M |
| F5 | Bibliothek zusätzlich als Galerie mit Titelbild | Bücher und Sammlungen als Kacheln | braucht F4 | nach F4 | M |
| F6 | Import aus Notion und Todoist; Listen als Markdown exportieren | Umzug ohne Abtippen | Seiten nehmen Markdown schon an | ja, zuerst Notion-Markdown | M |
| F7 | Natürliche Datumsangaben in der Eingabezeile („Freitag 14 Uhr“, „in 3 Tagen“) | schnelleres Erfassen | „/heute“, „/morgen“ und Wochentage gibt es schon | ja | S–M |
| F8 | Fokusansicht: eine Aufgabe groß, Zeiterfassung läuft | konzentriertes Arbeiten | Zeiterfassung ist vorhanden | ja | M |
| F9 | Gewohnheiten mit Serie, Pomodoro-Timer | tägliche Routinen | Wiederholungen und Timer gibt es teilweise | später | M |
| F10 | Zeichnung als Symbol exportieren (ICO und Favicon 16/32/48) | Pixel-Nische: eigene App- und Website-Symbole | PNG-Export gibt es | ja | S |
| F11 | Wechsel Aufgabenliste ↔ Notiz | Eine Liste wird zur Notiz und umgekehrt. | Die Art ist heute nach dem Anlegen fest. | Frage: Fehlt dir das im Alltag? | M |

**Bewusst nicht** (unverändert aus der Wettbewerbsrecherche):
Echtzeitmitarbeit, KI-Funktionen mit Netz, Bildarchive aus dem Netz,
Datenbank-Baukasten mit eigenen Feldtypen, Vektor- und Ebenenfunktionen.

## 6. Nur durch den Inhaber

| Nr. | Aufgabe | Stand |
|---|---|---|
| I1 | Inhaberangaben bestätigen | [Vorschläge](../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md) liegen vor |
| I2 | Lizenzbedingungen veröffentlichen | Entwurf: kostenlos für private, nicht kommerzielle Nutzung |
| I3 | Apple-Developer-Konto und Windows-Code-Signing-Zertifikat | nötig für Signatur und Store |
| I4 | Markenprüfung „Glide“ | Fachanwalt für Markenrecht |
| I5 | Python 3.14.7 auf dem Mac | braucht dein Passwort |
| I6 | Windows-Vollprüfung und die fünf Sitzungen der Prüfliste | [Anleitung](Checklisten/Windows_Pruefung_3.30.0.md), [Prüfliste](Checklisten/Manuelle_Pruefung_3.30.0.md) |
| I7 | Die `_Z`-Einträge löschen | Liste in Abschnitt 7 |

## 7. Zum Löschen markiert (`_Z`)

Der Agent darf nichts endgültig löschen, und das Verschieben in den
Papierkorb wurde ihm verwehrt. Deshalb tragen diese Einträge die Endung `_Z`. Keiner wird noch gebraucht. Wer
vorher etwas nachsehen will, findet es im jeweiligen `Archiv`.

| Eintrag | Inhalt |
|---|---|
| `10_Dokumentation_Z` | Archiv und README, 74 Dateien, 1,0 MB |
| `30_Release_Exports_Z` | Archiv und README, 19 Dateien, 76 KB |
| `00_Arbeitsvorbereitung/Entscheidungen_Z` | nur Archiv, 23 Dateien |
| `00_Arbeitsvorbereitung/Fehlerprotokolle_Z` | Archiv und README, 3 Dateien |
| `00_Arbeitsvorbereitung/Notizen_Z` | nur Archiv, 30 Dateien |
| `40_Store_Material/Apple_Z`, `40_Store_Material/Microsoft_Z` | nur Archiv, je 8 Dateien |
| `07_Python-Versionen/__pycache___Z` | übersetzter Bytecode vom 28.09. (10 Dateien); entsteht nicht mehr |
| `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.28.0_Z.md`, `…_3.29.0_Z.md` | abgelöst von der verdichteten Prüfliste 3.30; Originale im Archiv |
| `01_Repository/Glide/build/macos/Glide_Platzhaltersymbol_Z.png` | das alte „G“ des Entwicklungsbundles |

## 8. Antworten des Inhabers

Offen.

| Nr. | Antwort | Umsetzung |
|---|---|---|
| B1–B7 | | |
| E1–E6 | | |
| I7 | Die `_Z`-Ordner hat der Inhaber am 30.09.2026 gelöscht | erledigt |
| F1–F11 | | |
| I1–I7 | | |
