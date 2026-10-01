# Verbleibende manuelle Prüfung – Glide 3.16.0

Stand: 13.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Vollständiges App-Backup 3.16

- [ ] **Nur mit getrennter Testablage arbeiten** (Datenordner wechseln), bevor eine Wiederherstellung ausgeführt wird.
- [ ] „Vollständiges App-Backup speichern …“: Erfolgsmeldung, Dateiendung `.glideapp`, Zahl der Anhänge und Inhaltsüberblick prüfen.
- [ ] „App-Backup wiederherstellen …“: Vorschauwerte mit dem tatsächlichen Bestand vergleichen – Erzeugerversion, Datum, Aufgaben, Listen, Ordner, Labels, Papierkorb, Anhänge, Vorlagen, Aktivitätstage.
- [ ] Jeden der vier Bereiche einzeln übernehmen und die Wirkung prüfen; danach alle gemeinsam.
- [ ] Ohne Aufgabenbereich wiederherstellen: Reiter, Pinnwände, Tagesauswahl, gespeicherte Filter und Tabellenspalten müssen leer bleiben.
- [ ] Abbruch und Escape: Bestand, Einstellungen und Vorlagen bleiben unverändert.
- [ ] Ein gewöhnliches `.glidebackup` öffnen: die drei Extrabereiche sind gesperrt, der Hinweis „nicht enthalten“ erscheint.
- [ ] Nach der Wiederherstellung im Backup-Ordner prüfen: `vor_import_*.glidebackup`, `settings_vor_restore_*.json`, `vorlagen_vor_restore_*.json`.
- [ ] Ein `.glideapp` über „Komplettbackup laden …“ öffnen: die Aufgaben kommen an, die Extras werden ignoriert.
- [ ] Archiv mit echten Anhängen erzeugen und wiederherstellen; Dateien in den Punktdetails öffnen.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe, Tastaturbedienung des Vorschaudialogs.

## Weiterhin offen aus 3.15

- [ ] Tagesplanung: Tageswechsel, Zähler, Summen in „Mein Tag“, Tabelle und Startseite, Kapazität 0/1/1440 und ungültige Eingaben.
- [ ] Kontextmenü der Tagesplanung, Serienvorrücken, Filterverhalten, Sichtbarkeit der Tagesschalter.
- [ ] Mit physischem Mac-Trackpad auf Startseite, Tabelle, Tagesplanung, Diagrammen, Vorlagen und Listen scrollen.
- [ ] Light/Dark: Tabellenkopf, Vorlageneditor, Punktdetails, Label-Unterdialog und App-weite Auswahlfelder.
- [ ] Dynamische Kacheln, Vorlagenbaum, Vorlagenrundlauf mit Export und erneutem Import.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch Beispielbackups ersetzen.
