# Reiter und Pinnwand – Glide 3.10.0

Stand 13.09.2026 · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

Der Umsetzungsauftrag zu den nächsten Funktionen folgt der dokumentierten Reihenfolge: Reiteransicht, danach die erste Pinnwand für vorhandene Inhalte. Beide verwenden die bisherigen Aufgabenobjekte; es gibt keine neue Ablage oder Statusverwaltung.

## Reiter verwenden

Einen Punkt auswählen und im Kontextmenü oder unter Aktionen → Ansicht „Als Reiter öffnen“ wählen. Tastenkürzel: Cmd/Strg+Shift+O. Aufgaben, Long-Tasks und Gruppen sind möglich; Überschriften bleiben Gliederung.

Die Leiste sitzt über dem Arbeitsbereich. „Liste“ führt zur gewohnten Ansicht. Jeder Punktreiter zeigt den vollständigen Titel, Beschreibung, Art, Wichtigkeit, Termin mit Uhrzeit, Wiederholung, Benachrichtigung, Labels und Anhänge. Unterpunkte sind ebenfalls bearbeitbar und erledigbar. „Bearbeiten“ öffnet die vorhandene Maske.

„Reiter schließen“ oder Cmd/Strg+Shift+W schließt nur die Sicht. Strg+Bild↑/Bild↓ wechselt zwischen Liste und Punktreitern. „Reiter …“ zeigt alle offenen Reiter einschließlich anderer Listen. Lange Titel werden in der Leiste gekürzt, im Tooltip und Inhalt vollständig angezeigt. Die Leiste scrollt zum aktiven Reiter. Unter Aktionen → Ansicht lässt sich dessen Reihenfolge ändern.

Es gibt höchstens zwölf Punktreiter über alle Listen. Beim dreizehnten wird genau der am längsten nicht benutzte geschlossen und dies in der Hinweiszeile genannt. Bei Listenwechsel bleiben die zugehörigen Reiter erhalten. Eine Erledigung schließt keinen Reiter; Papierkorb, Überschriftenumwandlung oder weggefallene IDs entfernen ungültige Reiter. Undo/Wiederherstellen öffnet sie nicht erneut. Ein in eine andere Liste verschobener Punkt behält seinen Reiter unter der neuen Quelle.

## Pinnwand verwenden

In einer Liste oder einem Ordner „Pinnwand“ neben der Suche wählen. Alternativ Punkte in der Liste auswählen und über das Kontextmenü anheften. „Punkte anheften …“ bietet eine durchsuchbare Mehrfachauswahl vorhandener Punkte; bei Ordnern auch aus Unterordnern. Bis zu 500 Karten je Pinnwand.

Karten zeigen Titel, Erledigung, Termin, Beschreibungsauszug, Labels, Anhangzahl und Quellliste. Bearbeiten und Erledigen wirken auf denselben Punkt wie in Liste und Reiter. Anhänge lassen sich über den Reiter oder die vorhandene Detailmaske öffnen.

- **Geordnete Karten:** passende Spaltenzahl nach Fensterbreite, ohne manuelles Anordnen.
- **Frei anordnen:** Karten ziehen; optional an einem 24-Pixel-Raster ausrichten. Freie Positionen bleiben beim Wechsel zur geordneten Ansicht erhalten.
- **Kartenbreite:** kleine, mittlere oder große Karten für die aktuelle Pinnwand.
- **Filter:** vorhandene Labels sowie die normale Suche und „Nur offene Punkte“.
- **Alle Karten finden:** Filter aufheben, geordnet anzeigen und die Auswahl ins Sichtfeld holen.
- **Tastatur:** Pfeile, Pos1/Ende wählen Karten; Alt+Pfeile verschieben in freier Anordnung; Enter/F2 bearbeitet, Leertaste schaltet Erledigt um. Entf/Rückschritt nimmt ausschließlich die Karte von der Pinnwand. Escape führt zur Liste zurück.

„Von Pinnwand entfernen“ löscht keine Aufgabe. Löschen bleibt im bestehenden Aufgabenweg über Papierkorb. Bei gelöschten Punkten oder nicht mehr zum Board gehörenden Listen verschwinden die Karten; Wiederherstellen heftet sie nicht automatisch erneut an.

## Daten und Grenzen

`settings.json` enthält `open_tabs` (Quellliste, Punkt, Nutzungsreihenfolge), `active_tab` (Ansicht je Liste/Ordner) und `pinboards` (Punktreferenzen, Positionen, Raster, Anordnung und Breite). Kennungen werden beim Start und nach Änderungen gegen den Bestand geprüft. Ungültige Einstellungen fallen auf sichere Standardwerte zurück. Ansichtsänderungen werden atomar gespeichert; Schreibfehler setzen die Einstellung zurück.

Aufgabenbackups enthalten weiterhin Aufgaben und Anhänge, keine Einstellungen. Eine vollständige Datenordnerkopie bewahrt auch Reiter und Pinnwände. Keine Aufgabenmigration, keine neue Abhängigkeit, keine neue Hintergrundzustellung.

Bildvorschauen direkt auf Karten, Verbindungen, Zoom, neue Notizzettel und frei skalierbare Einzelkarten gehören nicht zu dieser ersten Stufe. Kartenhöhe folgt der Schriftgröße; die Breite wird je Pinnwand gewählt. Die Übersicht enthält Aufgabenobjekte und deren Anhänge, keine eigenständigen Dateikarten. Screenreader- und native Windows-Abnahme bleiben offen.

[Prüfstand](../07_QA_BERICHT.md) · [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md) · [Ursprünglicher Reitervertrag](../32_REITERANSICHT.md).
