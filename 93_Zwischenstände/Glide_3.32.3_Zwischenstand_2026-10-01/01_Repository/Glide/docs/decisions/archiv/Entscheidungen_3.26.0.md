# Entscheidungen und Umsetzungsstand 3.26.0

Stand 21.09.2026 · App-Version 3.26.0 · Datenformat 17

Der Entwicklungsauftrag ist fachliche Referenz. Maßgeblich ist der ausdrückliche Nutzerauftrag zur Umsetzung und Nachprüfung. Alte Screenshots und frühere Agentenaussagen sind keine Nachweise für den aktuellen Quellstand.

| Anforderung | Umsetzung und Abgrenzung |
| --- | --- |
| Mein Tag | Redundanten Textpfeil entfernt; native Baum-Aufklappfunktion erhalten. |
| Startseite | Tatsächlicher Monatsname, Gismo-Kontexte und Interaktionen, höhere Standardposition. Individuelle Kachelreihenfolgen bleiben erhalten. |
| Vorschau | Leere Pinnwand bleibt leer; keine Innenlinien. Große/extreme Bestände zeigen eine ausdrücklich verdichtete Übersicht mit höchstens 40 Karten, Gesamtzählung und unveränderten Modellkoordinaten. |
| Buttons und schmale Fenster | Dialogellipsen entfernt, Aktionsleisten pro Zeile unabhängig, kompakte Kopfzeilen und Anzeigen, Minimaldesign-Akzente einschließlich Kontrastgrau. |
| Pinnwand-Bugfixes | Ausgewählte Verbindungen ändern, Alle auswählen, Ordner-Ziellisten an Dialog und Mutation begrenzen. Auto anheften benennt die vorhandene Funktion; es bedeutet nicht automatische Kartengröße. |
| Canvas | Logische Tags, Lasso mit vollständiger Einschließung und Strg/Cmd-Ergänzung, optionale Ausrichtung mit sechs Bildschirmpixeln Toleranz, Alt-Unterdrückung, Abstands-Guides, Zoom 50–200 Prozent in sechs Stufen, optionaler Navigator. Druck nutzt logische Koordinaten. |
| Punkteingabe | FieldPairGrid für die gesamte Maske, schmal einspaltig, scrollbarer Inhalt, feste Abschlussaktionen und umbrechende Checklistenaktionen. |
| Notizlisten | Sechs Aufgabenzeilen plus Rich-Text-Editor, 13 Formate, Links, Datum/Zeit, lokale Tastenkürzel und Undo/Redo, Suchmarkierung, Autosave, Schema-17-Migration, Backups, Austausch, Duplikate und Vorlagen. TXT/Markdown enthalten den Notiztext; CSV bleibt auf Aufgaben ausgerichtet. |
| Verlauf | Seitenleistenansicht, Filter/Suche/Export, höchstens 15 Einträge und 15 Tage; Import/Export/Backup enthalten. |
| Rückmeldungen | Gemeinsame Mutationswege ergänzen Bearbeiten, Verschieben, Wiederherstellen, Labels, Fälligkeit und Planung. Notiz-Autosave löst keine Animationsflut aus. |
| Handbuch | HTML-Datei speichern oder im Standardprogramm zum Drucken öffnen. |
| Wartbarkeit | Historische Punktmarker entfernt, technische Gründe erhalten; Suchänderungen je Ereigniszyklus zusammengefasst. Architektur- und Widget-Bewertung dokumentiert. |
| Ablage | Historische Dokumente und alte QA-Verzeichnisse nach festgelegten Altersgrenzen archiviert; keine historischen Daten gelöscht. |
| Produktvorbereitung | Publisher festgehalten, persönlicher nichtkommerzieller Lizenzentwurf, Vertrieb/Markenrecherche-Vorbereitung und Signierungsanleitung vorhanden. |

## Bewusste offene Punkte

Permanente benannte Bereiche, echte gerichtete Aufgabenabhängigkeiten und Pinnwand-Reisen benötigen gemäß Abschnitt 1 des Auftrags eine fachliche Entscheidung. Der Abschnitt 14 bleibt Backlog. Neue Gismo-Bildassets sind vom Nutzer separat vorgesehen; die vorhandene Darstellung bleibt nutzbar. Es wurden keine Vertriebskonten angelegt, Markenrechte bestätigt oder signierte Installer veröffentlicht.

Kein vollständiger ttk- oder Virtual-Event-Umbau: Die Bewertung und bestehende Abhängigkeiten stehen in [Architektur](../02_ARCHITECTURE.md). Der tatsächliche Prüfnachweis und Plattformgrenzen stehen im [QA-Bericht](../07_QA_BERICHT.md).
