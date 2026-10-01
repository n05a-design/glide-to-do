# Verbleibende manuelle Prüfung – Glide 3.20.0

Stand: 14.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Kalenderausgabe 3.20

- [ ] Je eine Datei in **Apple Kalender**, **Outlook** und **Thunderbird** einlesen und den
      Import bestätigen; danach Termine in Monats- und Wochenansicht ansehen.
- [ ] Ganztagstermine liegen auf dem richtigen Tag und belegen nicht zwei Tage.
- [ ] Termine mit Uhrzeit beginnen zur Frist und enden nach dem geschätzten Aufwand
      beziehungsweise nach einer halben Stunde.
- [ ] Wichtigkeit erscheint als Priorität, Labels als Kategorien, Beschreibung und
      Quellliste im Terminfenster; Umlaute, Semikola und Kommata korrekt.
- [ ] Eine Serie (täglich, alle N Tage, Wochentage, monatlich, jährlich) über mehrere
      Wochen kontrollieren, auch das Enddatum.
- [ ] Alarme: relative Erinnerung meldet sich vor der Frist, feste zum gesetzten Zeitpunkt.
- [ ] **Dieselbe Datei ein zweites Mal einlesen**: Termine werden aktualisiert, nicht
      verdoppelt.
- [ ] Option „Bearbeitungstage" zuschalten und prüfen, dass Planung und Fälligkeit als
      zwei getrennte Termine erscheinen.
- [ ] Datei in eine Cloud legen und als Kalenderabonnement einbinden; prüfen, wie die
      fremde Anwendung mit einer neu geschriebenen Fassung umgeht.
- [ ] Zeitzonenprobe: Datei auf einem Gerät in einer anderen Zeitzone öffnen – die Uhrzeit
      bleibt die eingetragene Ortszeit.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe und Tastaturbedienung des
      Ausgabedialogs.

## Weiterhin offen aus 3.19 und früher

- [ ] Änderungsverlauf: Vorgänge über einen Arbeitstag gegenprüfen, Sammeleinträge, Filter,
      TXT-Ausgabe, Abschalten, Leeren, Format-15-Sicherung im Backup-Ordner.
- [ ] CSV-Import: Rundlauf mit dem eigenen Export, Dateien aus Excel und Numbers,
      Zuordnung von Hand, beide Importziele, Rückgängig.
- [ ] Druckausgabe: alle vier Formate auf Papier und als PDF, Optionen, Seitenumbrüche.
- [ ] App-Backup: Speichern, Wiederherstellen mit Vorschau, Teilbereiche – nur mit
      getrenntem Datenordner.
- [ ] Mit physischem Mac-Trackpad auf Startseite, Tabelle, Tagesplanung, Diagrammen,
      Vorlagen und Listen scrollen.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und
      Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch
Beispielbackups ersetzen.
