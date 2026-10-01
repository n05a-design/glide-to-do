# Verbleibende manuelle Prüfung – Glide 3.15.0

Stand: 13.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## Tagesplanung und Kapazität 3.15

- [ ] Ansicht „Tagesplanung“ über Seitenleiste, Startseite und Ansichtsmenü öffnen; Zähler der Seitenleiste mit der Zeilenzahl vergleichen.
- [ ] Mit „◀“ und „▶“ mehrere Tage vor und zurück wechseln; Fenstertitel, Kopfzeile und Leertext prüfen.
- [ ] Tageskapazität in den Einstellungen auf 0, 1 und 1440 setzen sowie ungültige Eingaben testen; Rest- und Überschreitungsanzeige in Tagesplanung, „Mein Tag“, Tabelle und Startseite vergleichen.
- [ ] Aufgabe ohne Aufwand, erledigte Aufgabe und Gruppe im selben Tag: Summe, „ohne Schätzung“ und „davon erledigt“ prüfen.
- [ ] Kontextmenü: Bearbeitungstag einen Tag später, einen Tag früher, entfernen – jeweils mit Rückgängig; Fälligkeit muss unverändert bleiben.
- [ ] Serie mit Bearbeitungstag abhaken: Punkt verlässt den Tag, kein künftiger Tag erhält eine Summe.
- [ ] Suche und „Nur offene Punkte“ in der Tagesplanung und in der Tabelle; Tagessumme darf sich dabei nicht verändern.
- [ ] Tagesschalter erscheinen ausschließlich in der Tagesplanung, nicht in Liste, Tabelle oder Pinnwand.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe und Tastaturbedienung der neuen Zeilen und Schaltflächen.

## Weiterhin offen aus 3.14

- [ ] Mit physischem Mac-Trackpad auf Startseite, Tabellenansicht, Tagesplanung, Diagrammen, Vorlagen und Listen scrollen; kleine und horizontale Gesten prüfen.
- [ ] Tabellenansicht: Spaltenauswahl je Liste, Suche, „Nur offene Punkte“, Zeile doppelklicken und bearbeiten.
- [ ] Light/Dark: Tabellenkopf, Vorlageneditor, Vorlagendetails, Punktdetails und Label-Unterdialog visuell prüfen.
- [ ] App-weite Auswahlfelder: Feld/Popup, Kontrast, Pfeile, Enter, Escape, Außenklick und Rückkehr zum vorherigen Dialog.
- [ ] Dynamische Kacheln: 1–3 Spalten, lange Texte, alle Schriftgrößen, gleiche Abstände, vollständige Aktionen und Fokus-Scrollen.
- [ ] Vorlagenbaum: App-Farben, sichtbare Metadaten, erhaltene geschlossene Zweige und feste Abschlussaktionen.
- [ ] Eigene Kopie eines Projekts als Vorlage speichern, bearbeiten, verwenden, exportieren und nach Neustart wieder importieren.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch Beispielbackups ersetzen.
