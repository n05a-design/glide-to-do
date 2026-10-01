# Release-Checkliste – Glide 3.8.0

Stand 12.09.2026 · Aufgabenformat 13

Aktuelle Ergänzung: [Erinnerungen und Betriebsgrenzen](31_ERINNERUNGEN_3.8.0.md).
Vor Veröffentlichung: vollständigen 3.8-Prüflauf, native Sichtprüfung, tatsächlichen
Ruhezustand/Neustart und Migration auf Zielsystemen abnehmen. Keine Benachrichtigung
bei beendetem Programm bewerben. Das Hervorheben in Taskleiste bzw. Dock ist keine
Systembenachrichtigung und darf auch nicht als solche beschrieben werden; eine echte
setzt Startmenüverknüpfung mit AppUserModelID beziehungsweise ein `.app`-Bundle
voraus ([Entscheidung](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).

## Übernommene Checkliste des Vorgängers 3.7


## Quellstand und Unterlagen

- [x] Originalauftrag und Claude-Antworten gegen den Quellstand abgeglichen.
- [x] Neue Rundläufe für Vorlagen, Teilimporte, Datenordner, Schriften und Personalisierung angelegt.
- [x] DejaVu Sans in vier TTF-Schnitten einschließlich unveränderter Lizenz.
- [x] Materialdarstellung und Grenze zu echtem Blur dokumentiert.
- [x] Version, Fixtures, Featurebericht, Architektur, Datenvertrag und Startkontext fortgeschrieben.
- [x] Frühere Dokumente vor Ersetzung archiviert.
- [x] Historische synthetische Leistungswerte 3.6 mit Methode/Grenzen gekennzeichnet.
- [x] Aktueller vollständiger macOS-Quelltest: elf Suiten bestanden; [QA](07_QA_BERICHT.md).
- [x] Startbare 3.7-Kopie, Fonts und Hashmanifest gegen den kanonischen Quellstand prüfen.

## Manuelle Abnahme

- [ ] Jüngste Vorlagen-/Dropdown-/Kacheländerungen nativ unter Windows nachprüfen.
- [ ] Aktuellen Vorlagenbaum und Mac-Dropdowns in Hell/Dunkel visuell abnehmen.
- [ ] Kacheln bei Resize, großer Schrift und Tastaturfokus visuell abnehmen.

- [ ] Weitere DPI/Monitore, hohe Kontraste, Systemtransparenz/RDP.
- [ ] Lange reale Nutzung und bisher nicht reproduziertes Einfrieren.
- [ ] Reales sequenzielles Arbeiten mit zwei synchronisierten Datenablagen.
- [ ] macOS einschließlich privater Fontregistrierung und Cmd-/Dialogverhalten.
- [ ] Kopien realer Daten/Anhänge und Zielgeräte mit großen Beständen.

## Veröffentlichung

- [ ] Publisher, Support, URLs, Lizenzmodell, Preis und Markenprüfung.
- [ ] Reproduzierbare Installer/App-Pakete, stabile Plattformkennungen.
- [ ] Windows-Signatur; macOS Signatur, Notarisierung und Gatekeeper.
- [ ] Clean-Machine-Tests und finale Store-Screenshots.
- [ ] Storetexte und aktuell geltende Einreichungsanforderungen freigeben.

3.7.0 ist ein interner Quellstand. Es wird kein signiertes Binärpaket oder
öffentliches Stable-Release behauptet. Die offenen Punkte sind reale
Plattform-/Veröffentlichungsschritte; sie werden nicht durch grüne Quelltests erledigt.

## Stand 3.7.0

Aktuelle Ergänzungen und Prüfnachweise: [Version 3.7.0](24_VERSION_3.7.0.md). Versionsgebundene 3.6-Berichte beschreiben den vorherigen Stand.
