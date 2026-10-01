# Tagebuch, Gismo und responsive Oberfläche – Glide 3.28.0

Stand 23.09.2026 · Glide 3.28.0 · Aufgabenformat 18

## Ziel

3.28 führt den undokumentierten UI-/UX-Zwischenstand 3.27 in den kanonischen
Quellstand zurück und entwickelt ihn nach dem Grundsatz „Form follows
Function“ weiter. Dekoration ist nur dort hinzugekommen, wo sie Status,
Orientierung oder eine direkte Handlung vermittelt.

## Tagebuch

Ein Ordner kann jetzt die Art `Tagebuch` tragen. Neue Inhalte in einem solchen
Ordner entstehen als datierte Notizseiten und werden in der Ordneransicht nach
Momentdatum sortiert. Tagebucheinträge speichern zusätzlich:

- Favorit, Stimmung, Ortsnotiz und Momentdatum;
- den zuletzt verwendeten Schreibimpuls;
- Erstellungs- und Änderungszeitpunkt;
- Rich-Text-Inhalt, lokale Anhänge und vorhandene Labels.

Die Ordnersuche berücksichtigt Titel, Beschreibung, Notizinhalt und
Tagebuch-Metadaten. Im Notizkopf stehen die häufigen Tagebuchaktionen direkt;
seltene Formatierungen liegen im Menü `Mehr`. Mitgeliefert werden Tagesnotiz,
Dankbarkeit, Wochenrückblick und ein Jahresordner mit Quartalen.

### Recherchebezug Apple Journal

Die Recherche am 23.09.2026 stützt sich auf Apples Produkt- und Hilfeseiten:

- [Journal-Einführung](https://www.apple.com/newsroom/2023/12/apple-launches-journal-app-a-new-app-for-reflecting-on-everyday-moments/): Text, Medien, Orte, Favoriten/Filter, Vorschläge und Zeitpläne.
- [Einträge und mehrere Journale](https://support.apple.com/guide/iphone/write-in-your-journal-iph9824e83ce/27/ios/27): mehrere Journale, Farben/Symbole und Schreibimpulse.
- [Formatierung und Medien](https://support.apple.com/guide/iphone/add-formatting-photos-and-more-iph492ee70a8/27/ios/27): Formatierung, Fotos, Zeichnungen, Audio und Orte.
- [Such- und Kalenderfunktionen](https://support.apple.com/en-gb/guide/iphone/iph6257be047/ios): Suche, Filter, Sortierung und Kalendernavigation.
- [Gewohnheit und Zeitplan](https://support.apple.com/en-gb/guide/iphone/iph70107aec2/ios): Zeitpläne und Schreibserien.
- [Datenschutz der Vorschläge](https://www.apple.com/legal/privacy/data/en/journaling-suggestions/): lokale Vorschlagsverarbeitung und kontrollierte Freigabe.

Glide übernimmt bewusst nur Funktionen, die zum lokalen Offline-Modell passen.
Nicht behauptet oder simuliert werden Apples gerätebasierte Vorschlagslogik,
Face ID/Touch ID, Audioaufnahme mit Transkription, Health-/Fitness-Signale oder
Ende-zu-Ende-verschlüsselte iCloud-Synchronisierung. Anhänge bleiben lokale
Kopien in Glides Datenablage.

## Startseite und visuelle Bestandteile

- Gismo besitzt die drei verständlichen Zustände Sättigung, Energie und
  Vertrauen. `Füttern`, `Spielen` und `Ruhen` verändern sie; pro vergangenem Tag
  sinken Werte begrenzt. Der Zustand liegt ausschließlich in den Einstellungen.
- Die Pinnwandvorschau zeigt nun Rasterpunkte, Kartenschatten, Kopfzeilen,
  Textlinien und Verbindungen. Sie bleibt eine Vorschau und kein zweiter Editor.
- Fortschrittsbalken, Statuspunkte, Kartenhierarchie und Verbindungen sind die
  bevorzugten grafischen Mittel für weitere Texte. Rein dekorative Bilder oder
  neue Bildabhängigkeiten wurden nicht eingeführt.

## Hierarchie und schmale Fenster

- Die Menüschaltflächen `Datei`, `Bearbeiten`, `Ansicht` und `Hilfe` haben keine
  dekorative Kontur; Tastaturfokus bleibt sichtbar.
- Such- und Eingabefelder dürfen bis 180 Pixel schrumpfen. Fortschrittsstatistik
  und nachrangige Aktionsgruppen verschwinden bei knapper Breite.
- Pinnwandoptionen behalten `Anordnung` und `Zoom`; Label-, Kartenbreiten-,
  Verbindungs- und Navigatorsteuerung werden bei Minimalbreite ausgeblendet und
  bleiben über die breitere Ansicht erreichbar.
- Die Punktmaske gliedert sich sichtbar in `Einordnung` sowie `Planung und
  Inhalt`. Feldpaare stapeln sich unterhalb der Zweispaltenschwelle.
- Gedrücktes Mausrad plus Bewegung startet jetzt kontinuierliches automatisches
  Scrollen mit Totzone und richtungsabhängiger Geschwindigkeit. Loslassen stoppt
  unmittelbar.
- Neutrale Nebenaktionen verwenden im dunklen Design helles Grau und im hellen
  Design dunkles Grau. Bestätigen, Löschen, Fälligkeit und Wichtigkeit behalten
  ihre semantischen Farben.

## Datenformat und Migration

Aufgabenformat 18 ergänzt `folders[].folder_kind` sowie `lists[].journal`.
Fehlende Felder aus älteren Dateien werden additiv zu `standard` beziehungsweise
leeren Tagebuchwerten normalisiert. Vor dem ersten Überschreiben einer Datei
unter Format 18 erzeugt `ensure_schema18_backup` eine unrotierte Datei
`liste_vor_format18_<Zeitstempel>.json`. Ältere Glide-Versionen dürfen Format 18
nicht schreibend öffnen.

## Prüfung

`tests/integration/test_features328.py` prüft Format 18, Normalisierung,
Speichern/Laden, die vier Tagebuchvorlagen, konturlose Menüs, neutrale
Nebenaktionen und die verdichtete Notizwerkzeugleiste. Der vollständige
Prüfstand und verbleibende manuelle Grenzen stehen in
[07_QA_BERICHT.md](07_QA_BERICHT.md).
