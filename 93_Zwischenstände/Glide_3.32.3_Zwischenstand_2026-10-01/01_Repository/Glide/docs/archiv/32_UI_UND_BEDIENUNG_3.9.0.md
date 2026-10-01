# Oberfläche und Bedienung – Glide 3.9.0

Stand 12.09.2026 · interner Quellstand · Aufgabenformat 13 · Einstellungen 2 · Vorlagen 2

## Änderungen

- Das bisherige Thema „Erinnerungen“ heißt in der gesamten App „Benachrichtigungen“: Kopfzeile, Übersicht, Punktdetails, Aufschub, Einstellungen, Fehlermeldungen und Systemmenü. Interne Bezeichner wie `reminder` bleiben für Daten, Vorlagen und Backups kompatibel.
- Benachrichtigungen, Aktionen und das Einstellungszahnrad stehen in derselben Kopfzeile. Offene Hinweise werden am Button gezählt. Nur Speicher-/Ablagefehler erhalten eine zusätzliche Statuszeile.
- Das Zahnrad öffnet die Einstellungen. Light Mode und Dark Mode sind dort wählbar, werden erst mit „Speichern“ übernommen und bleiben über Neustarts erhalten. Abbrechen ändert das Design nicht. Das bestehende Tastenkürzel und der Systemmenübefehl bleiben erhalten.
- Der Seitenleistenschalter blendet Listen und Ordner ein oder aus. Der rechte Inhalt und seine unteren Aktionen beanspruchen bei ausgeblendeter Leiste die frei werdende Breite. `sidebar_visible` wird additiv in den Einstellungen gespeichert; bei fehlendem Wert ist die Leiste sichtbar.
- „Aktionen“ zeigt alle anwendungseigenen Befehle aus Datei, Bearbeiten, Ansicht und Hilfe mit Suche, Bereichsauswahl und Tastenkürzeln. Untermenüs wie Export und Sortieren sind vollständig enthalten. Dieselben Menübefehle werden aufgerufen. Kopieren, Einfügen, Alles auswählen und Rückgängig wirken bei geöffnetem Texteingabefeld auf dieses Feld. Von macOS bereitgestellte Schreibtools, Diktat und Emoji-Palette sind Betriebssystemfunktionen; sie werden nicht als plattformübergreifende Glide-Funktionen nachgebildet.
- Der Benachrichtigungsbaum und seine Auswahl benutzen die App-Farben. Die Übersicht unterstützt weiter Öffnen, Verschieben, Erledigen und Bestätigen.
- „Verwenden“ ist in Vorlagenzeilen vertikal zentriert und erhält oben und unten gleichmäßigen Abstand.
- „Neue Liste“ und „Neuer Ordner“ messen die tatsächliche Formularhöhe. Reicht die nutzbare Bildschirmhöhe nicht, wird bei verfügbarer Breite zweispaltig angeordnet. Bei manueller Verkleinerung bleiben Scrollbereich und Abschlussaktionen erreichbar. Titel und Beschreibung haben thematische Ein-Pixel-Rahmen und sichtbare Fokusfarben. Labels verwenden die gemeinsame grafische Mehrfachauswahl mit Neuanlage.

## Einheitliche Dropdowns

`AppOptionMenu` ersetzt den früheren plattformabhängigen Auswahlfeldtyp auf allen Systemen. `OptionRows` zeigt farbige Chips, Hover und einen separaten Auswahlhaken. `LabelDropdown` nutzt dieselbe Fläche und Bedienlogik für Mehrfachauswahl. Einfache Auswahl übernimmt einen Wert und schließt; Mehrfachauswahl bleibt bis „Fertig“ oder Schließen offen.

`DropdownPopup` liegt als Frame innerhalb des Elternfensters. Es erzeugt weder ein separates Betriebssystemfenster noch einen eigenen modalen Eingabegriff. Ein vorangestelltes temporäres Bindtag fängt Außenklicks vor Widgetbindungen ab; der erste Klick schließt die Auswahl. Escape, Tab, Wechsel der Anwendung, Resize, Verbergen und Zerstören des Feldes schließen ebenfalls. Temporäre Bindings werden abgebaut. Ein vorhandener modaler Griff verbleibt beim aufrufenden Dialog.

Tastatur: Tab erreicht das Feld; Leertaste, Enter oder Pfeiltasten öffnen es. Pfeile, Pos1 und Ende navigieren; Enter übernimmt, Escape verwirft die Navigation. Bei Labels schaltet Leertaste die fokussierte Zeile um, Enter beendet die Auswahl. Lange Auswahlen sind scrollbar, lange Namen werden im Feld gekürzt und im Tooltip vollständig angezeigt. Native Datei-/Ordnerdialoge und bestehende Kontextmenüs bleiben Betriebssystem- bzw. Befehlsmenüs.

## Daten und Zustellung

Kein neues Aufgabenformat und keine Änderung am Zustellverfahren. Benachrichtigungen erscheinen innerhalb der laufenden App; Dock-/Taskleistenaufmerksamkeit bleibt separat abschaltbar. Die neue Benennung bedeutet keine Systemzustellung bei beendetem Programm. Bestehende Zeitpunkte, Aufschübe, Zustellbelege, Wiederholungen und Backups bleiben gültig.

## Nachweise

Der unveränderte Ausgangslauf 3.8.0 war vollständig erfolgreich: [Protokoll](../../../../50_Ablage/QA/qa-3.9.0/oberflaeche/ausgang/ergebnis.json).
Die neue Suite `test_ui39.py` prüft beide Themes, Seitenleistenbreite und Speicherung, Kopfzeile, Vorlagenabstände, echte Dropdown-Ereignisse, Tastatur, fehlende Zusatzfenster, unveränderte Grabs, zerstörte Felder, kurze/hohe Bildschirme, Menüparität und Suche.
Maßgeblich für den Abschluss und verbleibende Plattformprüfungen ist der [QA-Bericht](../07_QA_BERICHT.md).
