# Glide Produktdatenblatt 3.7.0

Stand: 12.09.2026 · lokaler Entwicklungsstand · Aufgabenformat 12

> **Hinweis:** Dieses Datenblatt beschreibt 3.7.0. Der Entwicklungsstand ist
> inzwischen 3.8.0 mit Aufgabenformat 13 und lokalen Erinnerungen. Vor einer
> Veröffentlichung ist es fortzuschreiben. Die Aussage, dass Glide keine
> Benachrichtigungen enthält, bleibt richtig: 3.8.0 zeigt Hinweise innerhalb der
> laufenden App und hebt Taskleiste bzw. Dock hervor, erzeugt aber keine
> Systembenachrichtigung.
> [Aktueller Stand](../01_Repository/Glide/docs/31_ERINNERUNGEN_3.8.0.md)

## Produkt

Glide ist eine deutschsprachige Desktop-App für Aufgaben, Listen, verschachtelte
Ordner und Notizen. Die Kernfunktionen laufen lokal ohne Konto, Server,
Cloudpflicht oder Internetzugriff. Python und Tk bilden die Laufzeitbasis.

## Funktionsumfang

| Bereich | Vorhandene Leistung |
|---|---|
| Struktur | Listen, Ordner bis fünf Ebenen, Aufgaben, Long-Tasks, Gruppen, Überschriften und Unterpunkte |
| Planung | Fälligkeit mit optionaler Uhrzeit, Wichtigkeit, lokale Kalenderansicht und Wiederholungsregeln |
| Inhalt | Beschreibung, lokale Anhangskopien, Farben und Labels an Punkten/Listen/Ordnern |
| Bedienung | Suche, Offen-Filter, Sortierung, Mehrfachauswahl, Ziehen, Rückgängig, Papierkorb, direkte Umbenennung |
| Startseite | Analoge Uhr, nächste eigene Fälligkeit, Tagesziel, letzte Listen, Bestand, Mondphase und Jahresaktivität |
| Vorlagen | Zehn Listen- und sechs Ordnervorlagen beim ersten Start; eigener Katalog, Bearbeiten/Speichern, Austausch und eigene Vorlagen samt Anhängen |
| Austausch | TXT-Import; TXT-/Markdown-/CSV-Export; portable Komplett- und Teilbackups mit Anhängen; ergänzender Listen-/Ordnerimport |
| Ablage | Datenordner frei wählen, vorhandene Daten öffnen oder in leeren Ordner kopieren, gerätespezifischer Zeiger, Fremdsperrwarnung und Schreibschutz |
| Darstellung | Hell/Dunkel, Akzentfarbe, drei Schriftgrößen, private mitgelieferte TTF-Schrift, farbige Auswahlen, optionale Materialoptik |
| Einstellungen | Name, Textlogo und Farbe, Startansicht, Wochenbeginn, Tagesziel, Bestand, Sekunden, Mondphase und Jahresanzeige |

Die Jahresanzeige zählt erfolgreiche Aufgabenänderungen, nicht die Dauer der
App-Nutzung. Alte Abschlusszahlen dienen als Rückfallwert; fehlende historische
Aktivität wird nicht erfunden. Wiederholungen rücken denselben Punkt beim
Abhaken vor, ohne Benachrichtigungsdienst.

## Daten und Portabilität

Standard unter Windows: `%APPDATA%\Glide`. Datei → Datenordner zeigt den
wirklich benutzten Pfad. Die Zeigerdatei ist gerätespezifisch; Einstellungen und
Vorlagen liegen dagegen in der gewählten Ablage und können mit ihr mitwandern.

Aufgabenformat 12, Einstellungen 2, Vorlagen 2. Ein Komplettimport ersetzt den
Bestand; der ergänzende Import behält ihn. Persönliche Einstellungen und
Vorlagenkatalog sind nicht Teil eines Aufgabenbackups. Teilbackups erhalten die
exportierte Struktur, Labels, Wiederholungen und verwaltete Anhangsdateien.

Vier DejaVu-Sans-TTF-Schnitte mit Lizenz sind enthalten. Windows registriert sie
nur für den Prozess. Eine systemweite Schriftinstallation ist nicht erforderlich.

## Nachweis und Grenzen

Der aktuelle kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

[QA 3.7](../01_Repository/Glide/docs/07_QA_BERICHT.md).

Die historische lokale Messung von 3.6.0 ergab bei 5.000 flachen Aufgaben eine mediane
Neudarstellung von 137,26 ms ohne Materialoptik und 144,73 ms mit aktivierten
Glaskanten. Das ist keine garantierte Antwortzeit und kein Vergleich mit einer
Vorgängerversion.
[Leistungsbericht](<../01_Repository/Glide/docs/archiv/21_LEISTUNGSBERICHT_3.6.0_vor_Nachbesserung_2026-09-11.md>).

Materialoptik bedeutet hier getönte deckende Flächen und Glaskanten. Ein echter
Desktop-Blur durch die Tk-Seitenleiste ist nicht nachgewiesen.
[Glasbericht](<../01_Repository/Glide/docs/archiv/19_GLASS_SURFACE_3.6.0_vor_Nachbesserung_2026-09-11.md>).

Nicht enthalten: Synchronisationsdienst, Mehrbenutzer-Konfliktauflösung,
externer Kalender, Benachrichtigungen oder Telemetrie. Eine Sperrdatei kann
Offline-Konflikte eines Cloudordners nicht ausschließen. Native Treeview-Auswahl
bleibt rechteckig. macOS, komplette DPI-/Mehrmonitor-/Accessibility-Matrix,
Langzeitbetrieb, Installer, Signierung und Storefreigabe bleiben gesondert zu
prüfen. Anbieter-/Lizenzmodell und Preis werden nicht aus dem Code abgeleitet.

Vollständiger Auftrag:
[Funktionsabgleich](../01_Repository/Glide/docs/25_FEATURE_ABGLEICH_3.7.0.md).




## Neu in 3.7

Dynamische Listen-/Ordnerkacheln mit eigener Höhe, 1–3 Spalten, 16 px Innenabstand, 12 px Zwischenraum, ohne Typzeile und mit umbrechenden Öffnen-/Bearbeiten-Aktionen, zweispaltige Seitendetails mit Farben, Labels und Anhängen. Jahresfelder zeigen Datum und Wochentag beim Darüberfahren. Tageswerte bleiben nach dem Löschen erhalten; der Bestand zählt vorhandene Aufgaben. Format 12 ergänzt Containeranhänge und erhält vor der ersten Migration eine unrotierte Originalkopie.

## Entwicklungsnachtrag 11.09.2026

16 ausführliche Vorlagen, vollständiger Vorlageneditor, relative Termine mit Vorlagenformat 2 und Mac-Trackpad-Unterstützung unter Tk 9. [Aktueller Funktions- und Prüfstand](../01_Repository/Glide/docs/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md). Storevorgaben und Freigaben wurden in diesem Nachtrag nicht neu recherchiert.

Vorlagenbaum und Mac-Auswahlfelder verwenden App-Farben. Der Windows-Auswahlfeldtyp bleibt erhalten.
