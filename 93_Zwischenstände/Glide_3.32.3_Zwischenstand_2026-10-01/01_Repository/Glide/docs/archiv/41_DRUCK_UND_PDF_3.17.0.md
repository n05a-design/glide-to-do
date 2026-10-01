# Druck- und PDF-Ausgabe – Glide 3.17.0

Stand: 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Ein Tageszettel auf Papier, eine Besichtigungscheckliste zum Abhaken, eine Listenübersicht
für eine Besprechung: Dafür gab es bisher nur den TXT- oder Markdown-Export. 3.17 erzeugt
eine gestaltete Druckansicht und übergibt sie an den Druckdialog des Systems.

## Der Weg zur Ausgabe

Glide schreibt eine **eigenständige HTML-Datei** und öffnet sie im Standardprogramm des
Systems – auf beiden Plattformen üblicherweise der Browser. Dessen Druckdialog druckt auf
Papier oder speichert als PDF.

Diese Entscheidung ist bewusst: Ein eigener PDF-Schreiber müsste Schriftbettung,
Zeilenumbruch und Seitenaufbau selbst lösen, ein Druck über Systembefehle wäre auf jeder
Plattform anders. Der gewählte Weg braucht **keine neue Laufzeitabhängigkeit**, liefert auf
macOS und Windows dasselbe Ergebnis und lässt dem Nutzer alle Optionen des Systemdialogs –
Papierformat, Rand, Seitenauswahl, Skalierung, PDF.

Die erzeugte Datei enthält **keine externen Verweise**: kein Skript, kein Stylesheet, keine
Bilder, keine Web-Schrift. Sie lädt nichts nach und funktioniert offline und in zehn Jahren
noch.

## Bedienung

- **Datei → „Drucken und PDF …“**, Tastenkürzel **Strg/Cmd+P**, über die durchsuchbaren
  App-Aktionen oder im Kontextmenü einer Liste unter „Exportieren“.
- Im Dialog das **Format** wählen:
  - **Tageszettel für heute** – „Mein Tag“, Punkte mit heutigem Bearbeitungstag, heute
    Fällige und Überfällige, jeweils als eigener Abschnitt mit Quellliste.
  - **Aktuelle Liste oder Ordner** – die geöffnete Liste in Lesereihenfolge; in der
    Ordneransicht alle enthaltenen Listen, jede als eigener Abschnitt.
  - **Tagesplanung des gewählten Tages** – die Punkte mit Bearbeitungstag an dem Tag, der
    in der Tagesplanung gerade betrachtet wird.
  - **Checkliste zum Abhaken** – dieselbe Menge wie „Liste oder Ordner“, auf Abhaken
    ausgelegt.
  Vorbelegt ist das Format, das zur geöffneten Ansicht passt.
- Sieben **Inhaltsoptionen** einzeln zuschaltbar: erledigte Punkte, Beschreibungen, Labels,
  Fälligkeit und Wiederholung, Bearbeitungstag und Aufwand, Ankreuzkästchen vor jedem Punkt,
  freie Notizzeilen am Ende. Vorbelegt sind alle außer „erledigte Punkte“ und „Notizzeilen“.
- **„Öffnen und drucken“** legt die Datei im temporären Ordner ab und öffnet sie.
  **„Als HTML speichern“** fragt nach einem Zielpfad und behält die Datei. Abbrechen und
  Escape erzeugen nichts.

## Darstellung

A4 mit 18 mm oberem und 16 mm seitlichem Rand. Kopfzeile mit Titel und Untertitel,
Abschnittsüberschriften mit Trennlinie, ein Punkt je Zeile mit gepunkteter Trennung.
Erledigte Punkte sind durchgestrichen und als „erledigt“ gekennzeichnet; Gruppen und
Überschriften tragen ihre Art, ihre Unterpunkte werden je Ebene um 12 pt eingerückt.
Zusatzangaben stehen in fester Reihenfolge unter dem Punkt: Quellliste, Fälligkeit,
Wiederholung, Bearbeitungstag, Aufwand, Labels, Anzahl der Anhänge. Die Fußzeile nennt
Programm, Druckzeitpunkt, Anzahl der Punkte und – falls gesetzt – den Profilnamen.

Seitenumbrüche sind so geregelt, dass eine Überschrift nicht allein am Seitenende steht und
ein Punkt mit seinen Zusatzangaben zusammenbleibt. Die Schriftliste beginnt bei DejaVu Sans,
sofern sie im System installiert ist, und fällt auf Systemschriften zurück. Die
mitgelieferten Schnitte werden nur prozesslokal für Glides eigene Oberfläche
registriert; das Anzeigeprogramm der Druckdatei sieht sie nicht.

## Grenzen

Kein Seriendruck, keine Vorlagen für das Layout, keine Kopf- oder Fußzeile mit eigenem
Logo, keine Seitenzahlen in der Datei selbst – die setzt der Druckdialog. Kein direkter
Druck ohne Dialog, keine Druckerauswahl innerhalb von Glide, kein Export nach DOCX oder
XLSX. Ab **2000 Punkten** wird die Ausgabe mit Hinweis abgeschnitten, damit aus einem
Klick nicht unbemerkt hunderte Seiten werden. Nutzdatendateien sind als Druckziel
ausgeschlossen. Die Ausgabe liest nur vorhandene Objekte: Sie verändert weder Aufgaben noch
Einstellungen und legt keine eigene Datenhaltung an.

## Abnahmekriterien

1. Alle vier Formate erzeugen eine vollständige HTML-Seite mit Zeichensatzangabe und
   Druckregeln.
2. Die Datei enthält keine externen Verweise, kein Skript und lädt nichts nach.
3. Titel, Punkttexte und Beschreibungen sind markup-sicher ausgegeben.
4. Jede der sieben Optionen wirkt einzeln und nachvollziehbar.
5. Der Tageszettel nennt seine Abschnitte und die Quellliste jedes Punkts.
6. Die Ordneransicht druckt alle enthaltenen Listen als eigene Abschnitte.
7. Ab 2000 Punkten erscheint der Hinweis und die Ausgabe endet dort.
8. Das Schreiben ist atomar, hinterlässt keine Temporärdatei und trifft keine
   Nutzdatendatei.
9. Drucken verändert Bestand und Einstellungen nicht.
10. Der Dialog ist in Hell und Dunkel bei 780×640 vollständig erreichbar; Abbrechen
    erzeugt nichts.

## Prüfung

Die Suite `tests/integration/test_features317.py` prüft mit isoliertem `GLIDE_DATA_DIR`
das Grundgerüst aller vier Formate, die Abwesenheit externer Verweise, das Escaping von
Titel, Punkttext und Beschreibung, jede der sieben Optionen einzeln, die Mengen je Format
einschließlich leerer Auswahl, den Ordnerdruck über mehrere Listen, Art und Einrückung von
Gruppen, die Obergrenze von 2000 Punkten, atomares Schreiben samt abgewiesener
Nutzdatendatei, die Unveränderlichkeit der Daten und den Dialog in beiden Themes bei
780×640. Der Gesamtlauf umfasst damit 21 Suiten.
[QA-Bericht](../07_QA_BERICHT.md) · [Release-Checkliste](../10_RELEASE_CHECKLIST.md) ·
[App-Backup 3.16](40_APP_BACKUP_3.16.0.md)
