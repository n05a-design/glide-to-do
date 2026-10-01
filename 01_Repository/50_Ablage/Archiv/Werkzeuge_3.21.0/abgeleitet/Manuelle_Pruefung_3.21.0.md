# Verbleibende manuelle Prüfung – Glide 3.21.0

Stand: 14.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Kalenderimport 3.21

- [ ] Je eine echte Datei einlesen: Export aus **Apple Kalender**, aus **Outlook**, aus
      einem **Webkalender** (Feiertage, Schulferien) und eine **Einladung** (.ics aus einer
      Mail) – Teilnehmerangaben fehlen erwartungsgemäß.
- [ ] Rundlauf: eine Liste mit 3.20 als ICS schreiben, dieselbe Datei importieren – es darf
      **kein** Punkt entstehen (eigene UIDs). Danach die UIDs in der Datei von Hand ändern
      und erneut importieren: jetzt entstehen die Punkte.
- [ ] Serientermine gegenprüfen: Was übernommen wurde, und was im Bericht als nicht
      abbildbar gezählt wird (etwa „jede zweite Woche" oder „zehnmal").
- [ ] Termin mit Alarm, Termin mit Ort, Termin mit Kategorien, Termin mit Priorität – jede
      Angabe in der Punktmaske kontrollieren.
- [ ] Zeitzonen: ein Termin aus einem Kalender einer anderen Zeitzone; ein Termin in UTC.
      Stimmt die Uhrzeit in Glide mit der im Kalender angezeigten überein?
- [ ] Zeitraumfilter durchprobieren (alles, ab heute, letzte zwölf Monate) und den Bericht
      mit den Übersprungsgründen gegen die Datei halten.
- [ ] Beide Ziele ausprobieren, danach Rückgängig – auch neu angelegte Labels müssen
      verschwinden.
- [ ] Eine große Datei (mehrere Hundert Termine) einlesen: Dauer und Bedienbarkeit.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe, Tastaturbedienung; Escape
      und Abbrechen dürfen nichts verändern.

## Weiterhin offen aus 3.20 und früher

- [ ] Kalenderausgabe: Dateien in Apple Kalender, Outlook und Thunderbird einlesen,
      dieselbe Datei zweimal (Aktualisieren statt Verdoppeln).
- [ ] Änderungsverlauf: Vorgänge über einen Arbeitstag gegenprüfen, Sammeleinträge, Filter,
      Abschalten, Leeren, Format-15-Sicherung im Backup-Ordner.
- [ ] CSV-Import: Rundlauf, Dateien aus Excel und Numbers, Zuordnung von Hand, Rückgängig.
- [ ] Druckausgabe: alle vier Formate auf Papier und als PDF.
- [ ] App-Backup: Speichern, Wiederherstellen mit Vorschau – nur mit getrenntem Datenordner.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen; dort
      fehlt der Zeitzonendatenbank-Rückfall möglicherweise, der Hinweis muss erscheinen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und
      Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch
Beispielbackups ersetzen.
