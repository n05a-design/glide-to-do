# Produktgrenzen

Stand 05.10.2026 · Glide 3.33.8 laut VERSION · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Glide ist eine deutschsprachige lokale Desktop-Anwendung für Aufgaben, Listen,
Seiten, Notizen, Notizbücher, Pinnwände und Pixelzeichnungen. Kernfunktionen
brauchen weder Internet noch Konto oder Cloudservice. Nutzerdaten liegen
außerhalb des Programmordners. Version und Prüfgrenzen stehen im
[QA-Bericht](07_QA_BERICHT.md), Aufgaben im
[Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md).

## Verbindliche Produktprinzipien

1. Apple-like: Es funktioniert möglichst selbstverständlich.
2. Form follows function: Gestaltung unterstützt die Funktion.
3. Keine Funktion doppelt.
4. Kein Platz wird unnötig verschwendet.
5. Nur das Wesentliche anzeigen, dieses klar und wirkungsvoll.
6. Möglichst geringe Komplexität für den Nutzer trotz umfangreicher Funktionen.

Vor neuen Funktionen prüfen: Gibt es bereits einen Weg? Welche konkrete Arbeit
wird leichter? Welche Bedienung verschwindet dafür? Bleiben Daten, Undo,
Tastatur und kleine Fenster zuverlässig? Offene Gestaltungsvorschläge sind
im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) gesammelt.

## Laufzeit und Oberfläche

Python mit Tk und Standardbibliothek; Python 3.14/Tk 9 ist die vorgesehene
Grundlage. Tk 8.6 bleibt mit eingeschränkter Systemintegration lauffähig.
tkinterdnd2 ist mitgeliefert und wird optional geladen
([Abhängigkeitsentscheidung](decisions/ABHAENGIGKEIT_TKDND.md)).

Symbole stammen aus der Textzeichentabelle `ICONS`; das Logo verwendet
`logo.py` und `resources/logo`. Schriften und deren Lizenznachweise bleiben
unter `resources/fonts`. Die Materialoptik nutzt opake getönte Tk-Flächen,
keine Durchsicht pro Widget. Mindestgröße 860 × 700; Schriftkontrast 4,5:1,
bei großer Schrift 3:1. Farbe trägt Bedeutung: Grün bestätigt, Rot löscht,
Lila fügt hinzu. Unwirksame Bedienelemente werden ausgeblendet.

## Bewusste Grenzen

- Kein Mehrbenutzerbetrieb, eigener Synchronisationsdienst, Cloudkonto,
  Telemetrie, Konfliktzusammenführung oder mehrsprachige Oberfläche.
- Extern synchronisierte Datenordner nur nacheinander benutzen. Die lokale
  Belegungsdatei verriegelt keine noch unsynchronisierten Cloudkopien.
- Erinnerungen werden nur bei laufender App verarbeitet. Details und
  Plattformgrenzen stehen im [Zustellvertrag](decisions/SYSTEMBENACHRICHTIGUNGEN.md).
- Notizen und Seiten sind eigenständige Arten; kein allgemeines
  Textverarbeitungsprogramm, keine allgemeine Konvertierungspflicht.
- Zeichnungen bleiben eine Rasterebene ohne Transparenz, Stiftdruck oder
  freien Fremd-SVG-Import. Die [Funktionen](20_FUNKTIONEN.md#9-pixel-werkstatt) nennen Formate
  und Sicherheitsgrenzen.
- ICS und CSV sind Dateiaustausch, keine externe Kalender-/Mailanbindung.
  Begrenzungen stehen im [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Installer, Signatur, Markenprüfung, endgültige Lizenz und Veröffentlichung
sind offene Schritte der [Veröffentlichung](10_VEROEFFENTLICHUNG.md).
Der [QA-Bericht](07_QA_BERICHT.md) unterscheidet automatische Nachweise und
ausstehende menschliche Plattformabnahme.
