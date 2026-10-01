# Glide 3.23.0 – Abschlussbericht zum Master-Arbeitsauftrag

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2 · Vorlagen 2

Rückführung auf die 46 nummerierten Punkte des Auftrags vom 18.09.2026.
Legende: **umgesetzt** · **Stufe 1** (weitere Stufen benannt) · **Konzept** ·
**offen**.

## Rückführung auf die Punkte

| Nr. | Thema | Stand | Nachweis |
|---:|---|---|---|
| 1 | Konkurrenzanalyse und neue Features | umgesetzt | [Feature-Gap-Analyse](Glide_Feature_Gap_Analyse_2026-09-18.md) |
| 2 | Glide als flüssige Anwendung | umgesetzt | Punkt 9; Grundsatz in [Leistung](../01_Repository/Glide/docs/51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md) |
| 3 | Design und Farbmodus zusammenführen | umgesetzt | [Designsystem](../01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md) |
| 4 | Liquid Glass als Designrichtung | umgesetzt | ebenda, Abschnitt „Liquid Glass“ |
| 5 | Form follows Function | umgesetzt | Gap-Analyse 2.6: fünf Redundanzen entfernt |
| 6 | Eingang und Mein Tag fusionieren | umgesetzt | Eingang eingerückt unter „Mein Tag“ |
| 7 | Navigation aufräumen | umgesetzt | neue Reihenfolge, „Verspätet“ erhalten |
| 8 | Tagespfeile korrigieren | umgesetzt | ◀ links, ▶ rechts |
| 9 | Performance untersuchen | umgesetzt | 336 → 129 ms, drei benannte Ursachen |
| 10 | Schnellerfassung überarbeiten | umgesetzt | Beschreibung, Kalender, Fensterleiste, Kästchen |
| 11 | Einheitliche Datumsauswahl | umgesetzt | `attach_calendar_picker`, letztes Feld ergänzt |
| 12 | Pinnwand als PDF und Druck | umgesetzt | belegte Fläche, nicht Bildschirmausschnitt |
| 13 | Pinnwand Richtung Whiteboard | Stufe 1 | Verbindungen, Notizen, Punkte anlegen |
| 14 | Pinnwand im Fokusmodus | umgesetzt | F11, Escape gestuft, Position erhalten |
| 15 | Tabellenspalten in der Breite | umgesetzt | Ursache: Prüfung beim Loslassen statt beim Drücken |
| 16 | Sortierung per Einzelklick | umgesetzt | dreistufig, war bereits Einzelklick |
| 17 | Jede Tabelle einzeln prüfen | umgesetzt | sieben geprüft, `prepare_table` zentralisiert |
| 18 | Tabellen linksbündig | umgesetzt | Stil und 17 Beschriftungen |
| 19 | Hover-Probleme | umgesetzt | Hover-Farben, Kontrast als Rechenregel |
| 20 | Punkteingabe mehrspaltig | umgesetzt | `ResponsiveColumns`, Umbruch unter 684 px |
| 21 | Maskottchen untersuchen | Konzept | [Arbeitsbegleiter](../01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md) |
| 22 | Globales Auf- und Zuklappen | umgesetzt | mit Schutz des aktiven Pfads |
| 23 | Redundanz auf der Startseite | umgesetzt | eine Kachel „Heute“ |
| 24 | Drucken sichtbar integrieren | umgesetzt | Kopfzeile plus Überlaufmenü |
| 25 | Fehler „Spalte“ | umgesetzt | AttributeError behoben, Regressionstest |
| 26 | Test-Suite erweitern | umgesetzt | neue Suite, neue Analyse |
| 27 | Benachrichtigungsansicht | umgesetzt | Flucht, Spaltenbreiten, Überschrift |
| 28 | Responsive Mindestbreite | umgesetzt | drei Dichtestufen |
| 29 | Sekundäre Buttons ausblenden | umgesetzt | vier Schaltflächen, Überlaufmenü |
| 30 | Weitere Informationen reduzieren | umgesetzt | Statuszeile, Suche löschen, Anzeige |
| 31 | Pinnwand bei geringer Breite | umgesetzt | Werkzeuge priorisiert |
| 32 | Zweispaltige Startseite länger | umgesetzt | 616 statt 980 Pixel, abgeleitet |
| 33 | Checklisten in der Listenansicht | umgesetzt | fünf Anzeigemodi, direkt abhakbar |
| 34 | Anhänge in der Listenansicht | umgesetzt | Name und Größe je Anhang |
| 35 | Umfangreiche KI-Antworten bearbeiten | umgesetzt | Import plus Anzeigemodus |
| 36 | KI-freundliches Austauschformat | umgesetzt | [Austauschformat](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md) |
| 37 | KI-Roundtrip | umgesetzt | verlustfrei für den abgebildeten Umfang |
| 38 | Beispiel und Prompt anpassen | umgesetzt | erzeugt aus den Konstanten |
| 39 | Menschen- und maschinenlesbar | umgesetzt | JSON verbindlich, Markdown als Zweitweg |
| 40 | KI grundsätzlich mitdenken | umgesetzt | Capability-Registry, Validierung, Vorschau |
| 41 | Bestehende Funktionen bewahren | umgesetzt | 27 Suiten, drei Anpassungen begründet |
| 42 | Datenverlust verhindern | umgesetzt | eigene Zusicherungen je Risikostelle |
| 43 | Komponenten zentralisieren | umgesetzt | vier gemeinsame Komponenten |
| 44 | Nicht oberflächlich umsetzen | umgesetzt | jeder Punkt mit Zusicherung |
| 45 | Große Features in Stufen | umgesetzt | Stufenplan für die Pinnwand |
| 46 | Abschlussprüfung und Doku | umgesetzt | dieses Dokument |

## Architekturänderungen

| Änderung | Wirkung |
|---|---|
| `DESIGNS`-Registry | Erscheinung an einer Stelle statt an dreien; neue Designs ohne Code |
| `render_pass` / `render_cached` | Kennzahlen einmal je Aufbau statt drei- bis fünfmal |
| `_parse_iso_date` mit `lru_cache` | Datumsprüfung ohne wiederholten `strptime` |
| `prepare_table` | eine Tabellenkomponente statt sieben Einrichtungen |
| `ResponsiveColumns` | mehrspaltige Masken, die bei wenig Platz umbrechen |
| `attach_calendar_picker` | Kalender an jedem Datumsfeld |
| `dialog_label` | linksbündige Dialogbeschriftung für `ListApp` |
| `contrast_ratio`, `readable_text_color`, `ensure_contrast` | Kontrast gerechnet statt geschätzt |
| Austauschschicht | eigene Formatversion neben dem Datenformat |
| `pack_relative` | Zeilenaufbau bricht nicht ab, wenn ein Bezug fehlt |

## Datenmodell

**Kein Formatsprung.** Aufgabenformat bleibt 16, Einstellungsformat bleibt 2.

Neue Einstellungswerte, alle additiv und mit Vorgabe:

| Wert | Bedeutung | Vorgabe |
|---|---|---|
| `design` | gewähltes Design | abgeleitet aus `theme`/`color_mode`/`glass_mode` |
| `list_detail_mode` | Informationsumfang der Listenansicht | `standard` |
| `pinboards[*].connections` | Verbindungen je Pinnwand | leer |

`theme`, `color_mode` und `glass_mode` bleiben als abgeleitete Werte
geschrieben, damit ältere Fassungen dieselbe Datei richtig lesen.

## Datenverlust – geprüfte Stellen

| Risiko | Zusicherung |
|---|---|
| Globales Zuklappen | Bestand unverändert, aktiver Pfad bleibt offen |
| Entfallene Startseitenkachel | `due` fällt aus der Auswahl, `today` bleibt sichtbar |
| Detailzeilen der Listenansicht | zählen nicht als Punkte, nicht in Export und Backup |
| Checklistenzeile abhaken | schreibt in die Checkliste, nicht in den Punkt |
| Austauschimport | legt nur an; bei Fehlschlag gehen Listen, Ordner, Labels und Rückgängig-Stapel zurück |
| Karte von der Pinnwand nehmen | nimmt ihre Verbindungen mit, lässt den Punkt unberührt |
| Punkt auf der Pinnwand anlegen | echter Punkt in der Quellliste, erscheint in allen Ansichten |
| Designübernahme | alle sieben Ausgangszustände geprüft |

## Prüfstand

- **27 Integrationssuiten**, darunter neu `test_features323.py`.
- **Vier Analysen**: statisch, Erreichbarkeit, Standprüfung und neu
  `attributpruefung.py`.
- Der Lauf unter Linux mit Python 3.12.3 und Xvfb ist grün bis auf zwei
  Schritte, die in dieser Umgebung nicht laufen können: die
  Dokumentationsprüfung (rund 400 historische Archivdateien liegen nicht in
  der Prüfumgebung) und die Screenshot-Erzeugung (braucht ImageMagick und eine
  Zielplattform).

## Offene Entscheidungen

| Frage | Wer entscheidet |
|---|---|
| Aussehen und Name der Markenfigur | Inhaber |
| Soll der Begleiter sprechen oder nur zeigen | Inhaber |
| Freies Zeichnen auf der Pinnwand – zweite Datenhaltung? | Inhaber |
| Gerichtete Abhängigkeiten statt ungerichteter Verbindungen | Inhaber |
| Anbindung an einen KI-Dienst statt Dateiaustausch | Inhaber, mit Datenschutzfolge |
| Publisher, Lizenz, Preis, Markenprüfung | unverändert offen |

## Nächste Phase

Unverändert gegenüber dem 16.09., und durch diese Fassung nicht kleiner
geworden:

1. Native Abnahme auf Windows und macOS.
2. Endnutzer-Einstieg beim ersten Start.
3. Paketierung mit Installer und Signierung.

Erst danach die vier Funktionen aus Abschnitt 2.4 der Gap-Analyse.
