# Glide Produktdatenblatt 3.30.0 – Entwurf

Stand 29.09.2026 · Glide 3.30.0 · unveröffentlichter Entwicklungsstand · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

> **Entwurf, keine Freigabe.** Grundlage ist der automatisch geprüfte
> Funktionsstand 3.30.0 ([QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
> Abschlusslauf mit Exitcode 0). Vor einer Einreichung stehen noch aus:
> - die manuelle Prüfung;
> - Installer und Signatur;
> - die Markenprüfung;
> - die offenen Inhaberangaben aus
>   [PRODUCT_IDENTITY](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md):
>   Copyright, Datenschutz-URL, Sicherheitskontakt und Installer-Kennung
>   ([Vorschläge](Inhaberangaben_Vorschlaege_2026-09-27.md)). Kennungen
>   (`de.shaye.glide`, `Shaye.Glide`), Vertriebsweg und Architekturen (x64,
>   arm64) sind seit dem 26./27.09.2026 entschieden.
>
> Die Store-Grenzen unten stammen aus der Recherche vom 04.09.2026 und müssen
> im Einreichungsformular erneut geprüft werden.

## Kurzprofil

Glide ist eine deutschsprachige Desktop-App für Aufgaben, Listen, Notizen,
Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Alles liegt lokal – ohne Konto,
Server, Abo oder Telemetrie. Die Laufzeit ist Python 3.14 mit Tk 9 und der
Standardbibliothek; mitgeliefert wird nur tkinterdnd2 (MIT) für das Ziehen
aus Finder und Explorer. Logo und Programmsymbol liegen seit dem 29.09.2026
als Master vor.

**Alleinstellung:** Glide verbindet Aufgabenorganisation mit einer echten
Pixel-Werkstatt. Zeichnungen werden zu Symbolen, Pinnwandkarten und
Galeriebildern; das Design „Pixel“ gibt der ganzen App diese Handschrift.

## Funktionsumfang 3.30

| Bereich | Leistung |
|---|---|
| Struktur | Listen, Ordner, Notizbücher und Bibliotheken, Aufgaben, Long-Tasks, Gruppen, Überschriften, Unterpunkte, Archiv statt Löschen |
| Seiten und Galerie | Seiten für lange Texte und KI-Berichte (Markdown hinein und hinaus, Aufgaben als echte Punkte, Vorlagen, eigenes Austauschformat), Bibliothek als Tabelle, Galerie für Bildersammlungen |
| Planung | Fälligkeit mit Uhrzeit, Wiederholungen, Erinnerungen bei laufender App, Bearbeitungstag, Aufwand, Kapazität je Wochentag, „Mein Tag“ mit Zeitplan und Stundenraster, Tagesbeginn und Wochenrückblick |
| Beziehungen und Zeit | Verknüpfte Punkte mit Rückverweisen, „wartet auf“ mit Kreisprüfung, Zeiterfassung je Punkt |
| Ansichten | Liste mit Gruppierung, Tabelle mit verschachtelten Unterpunkten, Detailbereich mit allen Feldern, Kalender, Startseite zum Anpassen, Galerie „Listen und Ordner“ |
| Pinnwand | Freie Fläche, geordnete Karten und Spaltenboard nach Feldern, Bereiche, beschriftete Verbindungen, Hintergründe, Präsentation und Folien als PDF |
| Pixel-Werkstatt | Flächen mit 16 bis 128 Zellen, sieben Werkzeuge, Symmetrie, Muster, Auswahl, Paletten (.gpl/.hex), Rückgängig je Aktion, Zwischenstände, PNG-Export, Pixelsymbole |
| Inhalt | Rich-Text-Notizen, Beschreibungen, Checklisten, Labels, Farben, lokale Anhänge, Vorlagen mit Eingabefeldern |
| Austausch und Sicherung | Komplett-, Teil- und App-Backup, CSV/TXT, Kalender ICS in beide Richtungen, Druck und PDF, Änderungsverlauf, Austauschformat für KI-Werkzeuge |
| Darstellung | Zehn Designs einschließlich „Pixel“ mit der Schrift Pixelify Sans, Hell und Dunkel, Kontrastdesigns, drei Schriftgrößen |

## Store-Texte (Entwurf)

**Kurzbeschreibung** (Microsoft empfiehlt unter 270 Zeichen; dieser Entwurf
hat 214):

> Aufgaben, Notizen, Seiten, Notizbücher, Pinnwände und Pixelzeichnungen in einer
> deutschsprachigen App – vollständig lokal, ohne Konto und ohne Abo. Plane
> deinen Tag, ordne Projekte auf Boards und gestalte eigene Pixelsymbole.

**Beschreibung** (höchstens 10.000 Zeichen):

> Glide ordnet, was du dir vornimmst – und gibt ihm ein Gesicht.
>
> Listen, Ordner und Notizbücher halten Aufgaben, Notizen und Zeichnungen
> zusammen. „Mein Tag“ zeigt, was heute ansteht, mit Zeitplan und
> Stundenraster. Die Pinnwand wird zum Board: Karten nach Fälligkeit,
> Wichtigkeit oder Label in Spalten ziehen, Bereiche benennen, Verbindungen
> beschriften und alles als Folien präsentieren.
>
> Die Pixel-Werkstatt ist Glides Besonderheit. Zeichne auf 16 bis 128 Zellen
> mit Pinsel, Formen, Symmetrie und Mustern. Verwende eigene Paletten und
> exportiere als PNG. Mache deine Zeichnungen zu Symbolen für Listen und
> Ordner. Das Design „Pixel“ trägt diese Handschrift durch die ganze App.
>
> Alles bleibt auf deinem Rechner. Glide braucht weder Internet noch Konto,
> sendet keine Nutzungsdaten und sichert deinen Bestand mit vollständigen
> Backups und einer Sicherung vor jeder Formatumstellung.

**Features** (bis zu 20, je höchstens 200 Zeichen):

1. Aufgaben, Listen, Ordner und Notizbücher – verschachtelt, mit Gruppen, Überschriften und Archiv.
2. „Mein Tag“ mit Zeitplan, Stundenraster, Kapazität je Wochentag, Tagesbeginn und Wochenrückblick.
3. Pinnwand als Board: Spalten nach Feldern, Bereiche, beschriftete Verbindungen und Präsentation.
4. Pixel-Werkstatt mit 16 bis 128 Zellen, Formen, Symmetrie, Mustern, Paletten und PNG-Export.
5. Eigene Pixelsymbole für Listen und Ordner, sichtbar in Seitenleiste, Suche und Galerie.
6. Detailbereich neben der Liste: alle Felder bearbeiten, ohne ein Fenster zu öffnen.
7. Verknüpfte Punkte, „wartet auf“ mit Kreisprüfung und Zeiterfassung je Punkt.
8. Wiederholungen, Erinnerungen und Kalenderaustausch per ICS.
9. Vorlagen mit Eingabefeldern wie {{Projektname}} für wiederkehrende Abläufe.
10. Zehn Designs, darunter „Pixel“ mit eigener Pixelschrift, sowie Kontrastdesigns.
11. Vollständig lokal: kein Konto, kein Abo, keine Telemetrie.
12. Backups, Wiederherstellung mit Vorschau und Sicherung vor jeder Formatumstellung.

## Daten und Grenzen

- Der Datenordner ist frei wählbar, auch ein synchronisierter Ordner.
  Glide synchronisiert nicht selbst; Fremdbelegung führt zum
  Schreibschutz.
- Ein Bestand aus einer neueren Glide-Version öffnet schreibgeschützt.
  **Ältere Versionen (3.29 und früher) dürfen nach der Umstellung nicht
  mehr gestartet werden** – im Store-Text zu „Neuerungen“ und in der Hilfe
  nennen.
- Erinnerungen erscheinen nur bei laufender App; es gibt keine
  Systembenachrichtigung.
- Die mitgelieferten Schriften DejaVu Sans und Pixelify Sans (SIL OFL 1.1)
  liegen mit Lizenztexten bei.

## Offene Punkte vor einer Einreichung

| Punkt | Stand |
|---|---|
| Manuelle Prüfung | [Prüfliste 3.30](../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md), [Windows-Prüfung](../00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md) |
| Screenshots | vom realen Windows-/macOS-Build aufnehmen; Agentenbilder belegen keine Plattformdarstellung |
| Installer, Signatur, Notarisierung | offen |
| Copyright, Datenschutz-URL, Sicherheitskontakt, Installer-Kennung | Vorschläge liegen vor, Bestätigung durch den Inhaber offen |
| Kennungen, Vertriebsweg, Architekturen | entschieden 26./27.09.2026 (PRODUCT_IDENTITY) |
| Programmsymbol | aus dem Logo-Master, `assets/icons` (29.09.2026) |
| Markenprüfung „Glide“ | offen, Fachanwalt |
| Store-Vorgaben | seit 04.09.2026 nicht neu abgerufen |

[Vertrag 3.30](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) ·
[Projektübergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md) ·
[Historische Microsoft-Recherche](Archiv/Store_Angaben_Microsoft_historische_Recherche_2026-09-24.md) ·
[Historische Apple-Recherche](Archiv/Store_Angaben_Apple_historische_Recherche_2026-09-24.md)
