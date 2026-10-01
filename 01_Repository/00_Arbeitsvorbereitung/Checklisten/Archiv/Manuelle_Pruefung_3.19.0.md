# Verbleibende manuelle Prüfung – Glide 3.19.0

Stand: 13.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Änderungsverlauf 3.19

- [ ] **Vor der ersten Nutzung eine Sicherung des echten Bestands anlegen** – 3.19 hebt das
      Aufgabenformat auf 15. Danach prüfen, dass `liste_vor_format15_*.json` im
      Backup-Ordner liegt und die alte Datei unverändert enthält.
- [ ] Einen Arbeitstag normal arbeiten und danach den Verlauf lesen: Stimmen Reihenfolge,
      Zeitpunkte, Objektnamen und Listen mit dem überein, was tatsächlich passiert ist?
- [ ] Jeden Vorgang einmal auslösen und im Verlauf wiederfinden: anlegen, umbenennen,
      Frist setzen, erledigen, wieder öffnen, ziehen, in eine andere Liste verschieben,
      in den Papierkorb, wiederherstellen, endgültig entfernen.
- [ ] Mehrfachbearbeitung über viele Punkte: Entsteht ein Sammeleintrag mit richtiger Zahl?
- [ ] Einen CSV-Import mit mehreren hundert Zeilen: Bleibt der Verlauf lesbar?
- [ ] Suche, Zeitraum- und Artfilter durchprobieren; Ausgabe als TXT öffnen und gegen die
      Ansicht halten.
- [ ] Protokollierung in den Einstellungen abschalten, arbeiten, wieder einschalten:
      Es entstehen keine Einträge in der Pause, alte bleiben erhalten.
- [ ] „Verlauf leeren" bestätigen und prüfen, dass Aufgaben, Listen, Ordner und Papierkorb
      unverändert sind.
- [ ] Komplettbackup schreiben, Bestand verändern, Backup wiederherstellen: Der Verlauf des
      Archivs erscheint samt Eintrag „Bestand ersetzt".
- [ ] Rückgängig nach mehreren Änderungen: Der Bestand kommt zurück, die Einträge bleiben
      stehen und die Rücknahme erscheint als weiteres Ereignis.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe und Tastaturbedienung des
      Verlaufsdialogs; Strg/Cmd+H prüfen.
- [ ] Größe der Speicherdatei nach längerer Nutzung ansehen (4000 Einträge als Obergrenze).

## Weiterhin offen aus 3.18 und früher

- [ ] CSV-Import: Rundlauf mit dem eigenen Export, Dateien aus Excel und Numbers,
      Zuordnung von Hand, beide Importziele, Rückgängig.
- [ ] Druckausgabe: alle vier Formate auf Papier und als PDF, Optionen, Seitenumbrüche.
- [ ] App-Backup: Speichern, Wiederherstellen mit Vorschau, Teilbereiche,
      Rückfallsicherungen – nur mit getrenntem Datenordner.
- [ ] Tagesplanung: Tageswechsel, Zähler, Summen, Kapazitätsgrenzen, Serienvorrücken.
- [ ] Mit physischem Mac-Trackpad auf Startseite, Tabelle, Tagesplanung, Diagrammen,
      Vorlagen und Listen scrollen.
- [ ] Light/Dark: Tabellenkopf, Vorlageneditor, Punktdetails, Label-Unterdialog und
      App-weite Auswahlfelder.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und
      Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch
Beispielbackups ersetzen.
