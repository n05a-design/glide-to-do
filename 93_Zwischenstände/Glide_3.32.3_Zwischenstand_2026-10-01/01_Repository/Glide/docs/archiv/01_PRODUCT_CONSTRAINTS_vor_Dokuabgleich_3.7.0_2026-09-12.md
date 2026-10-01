# Produktgrenzen – Glide 3.7.0

Stand: 07.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

Glide ist eine deutschsprachige, lokale Aufgaben- und Listenanwendung für einen
Arbeitsplatz. Kernfunktionen benötigen weder Konto noch Internet oder Server.
Nutzerdaten liegen außerhalb des Programmordners. Die Laufzeit verwendet Python,
Tk und die Standardbibliothek. Mitgelieferte Schriften sind Ressourcen; sie
werden ohne dauerhafte Installation pro Prozess registriert.

## Funktionsumfang

Aufgaben, Gruppen, Long-Tasks und Überschriften, verschachtelte Ordner und Listen,
Labels, Wichtigkeit, Fälligkeit mit Uhrzeit, Wiederholungen, Papierkorb,
Rückgängig, Suche, Kalender, Startseite, Vorlagen und Backup/Import gehören zum
Produkt. Die Ansicht „Labels“ gruppiert den Bestand nach Labels. Freie Labels
werden manuell vergeben; Long-Task und Überschrift besitzen feste Artlabels.

Die Jahresanzeige zählt erfolgreich gespeicherte Aufgabenbearbeitungen. Erledigte
Aufgaben werden zusätzlich für das Tagesziel gezählt. Es gibt keine Überwachung
anderer Apps und keine Messung der Anwesenheitsdauer. Historische Erledigungsdaten
dienen als Ersatz, solange noch keine Bearbeitungshistorie vorliegt.

## Datenordner und externe Synchronisationsdienste

Der Datenordner ist seit 3.6 frei wählbar. Er darf in einem von OneDrive oder
einem anderen Dienst synchronisierten Verzeichnis liegen. Glide führt selbst
keinen Netzwerkabgleich durch. Der Zeiger liegt auf Windows unter
`%APPDATA%/Glide/datenordner.json`; `GLIDE_DATA_DIR` hat für einen Start Vorrang.

Ein leerer Zielordner kann eine Kopie des aktuellen Bestands erhalten. Bei einem
bestehenden Ziel öffnet Glide dessen Daten, statt sie zu überschreiben. Die
bisherige Ablage bleibt bestehen. Eine verschachtelte Kopie in den eigenen
Quellordner wird abgewiesen.

`glide.lock` enthält Rechnername, Prozess, Token und Aktivitätszeitpunkt. Eine
erkannte fremde Belegung unterbindet in diesem Start das Speichern und zeigt
einen Hinweis. Lokale Prozesse werden auf Windows ohne Signale geprüft; für
fremde Rechner gilt der Zeitstempel. Die Gültigkeit beträgt acht Stunden und
wird während der Nutzung aufgefrischt. Nur die eigene Sperre wird entfernt.
Diese Datei ist kein verteilter Transaktionsdienst: Zwei noch nicht abgeglichene
Cloudkopien können voneinander nichts wissen. Nacheinander arbeiten und den
Dienst vollständig synchronisieren lassen.

Einstellungen und Vorlagen liegen im gewählten Datenordner. Wird er extern
synchronisiert, können auch diese Dateien mitwandern. Nur die Zeigerdatei ist
garantiert gerätespezifisch. Aufgabenbackups enthalten die persönlichen
Einstellungen und den separaten Vorlagenkatalog nicht.

## Darstellung

Die Anwendung benutzt Textzeichen aus `ICONS`, keine Bildpakete für Symbole.
DejaVu Sans 2.37 wird in vier unveränderten TTF-Schnitten mit Lizenz ausgeliefert.
TTF/OTF können privat registriert werden; WOFF/WOFF2 werden nicht geladen.
Die Hauptansichten und anwendungseigenen Dialoge unterstützen Hell/Dunkel.

Der Schalter für Glasflächen aktiviert eine Materialanmutung mit Farben und
Kanten sowie einen optionalen Windows-DWM-Aufruf. Die Tk-Flächen bleiben opak:
echtes per Panel weichgezeichnetes Desktopglas ist nicht Bestandteil von 3.7.
Ausgewählte Labelmarkierungen und Kalendertage sind rund; native Treeview-Zeilen
und native Menüs bleiben rechteckig. Details: [Materialprüfung](<archiv/19_GLASS_SURFACE_3.6.0_vor_Nachbesserung_2026-09-11.md>).

## Weiterhin außerhalb des Produkts

Echter gleichzeitiger Mehrbenutzerbetrieb, Zusammenführung von Konflikten,
eigener Cloudservice, Telemetrie, Push, externe Kalender-/Mailintegration,
Mehrsprachigkeit und ein vollwertiger Rich-Text-Editor sind nicht umgesetzt.
Packaging, Signatur, Storeeinreichung, Preis, Publisher und Markenfreigabe
sind eigenständige Veröffentlichungsschritte und keine fertigen 3.7-Funktionen.

Die [Feature-Matrix](25_FEATURE_ABGLEICH_3.7.0.md) ordnet jeden Punkt des
beauftragten Ausbaus zu; der [QA-Bericht](07_QA_BERICHT.md) begrenzt die Freigabe.

## Stand 3.7.0

Aktuelle Ergänzungen und Prüfnachweise: [Version 3.7.0](24_VERSION_3.7.0.md). Versionsgebundene 3.6-Berichte beschreiben den vorherigen Stand.

## Nachbesserung vom 11.09.2026

Mac-Trackpad unter Tk 9, vollständige isolierte Vorlagenbearbeitung, 16 Praxisvorlagen,
relative Termine mit Vorlagenformat 2 und verbesserte Aufgaben-Vorschauen.
Der aktuelle [Nachtrag mit Migration, Bedienung und Prüfgrenzen](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
hat für diese Punkte Vorrang vor dem Prüfstand vom 07.09.2026.
