# Verbleibende manuelle Prüfung – Glide 3.18.0

Stand: 13.09.2026 · Die automatische Abschlussprüfung liegt im [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md).

## CSV-Import 3.18

- [ ] Eine Liste mit „Als CSV“ exportieren, wieder importieren und mit dem Original
      vergleichen: Struktur, Art, Erledigt, Wichtigkeit, Fälligkeit mit Uhrzeit, Labels,
      Bearbeitungstag und Aufwand.
- [ ] Je eine Datei aus Excel und aus Numbers speichern und einlesen – Semikolon und
      Komma, mit und ohne BOM; Umlaute und scharfes S im Ergebnis prüfen.
- [ ] Trennzeichen und Kodierung im Dialog von Hand umstellen und die Wirkung in der
      Vorschau beobachten.
- [ ] Datei ohne Kopfzeile einlesen, Spalten von Hand zuordnen, Häkchen „Erste Zeile
      enthält Spaltennamen“ ein- und ausschalten.
- [ ] Verschachtelung: einmal über eine Ebenenspalte, einmal über eine Nummernspalte,
      einmal ohne Häkchen; Ergebnis im Baum und in der Tabellenansicht ansehen.
- [ ] Beide Ziele ausprobieren: neue Liste (auch in einem geöffneten Ordner) und Anhängen
      an die geöffnete Liste; danach Rückgängig und prüfen, dass auch neu angelegte Labels
      verschwinden.
- [ ] Datei mit Fehlwerten einlesen und den Abschlussbericht mit den Zeilennummern gegen
      die Datei halten.
- [ ] Große Datei (mehrere Tausend Zeilen) einlesen: Dauer, Bedienbarkeit des Dialogs und
      Reaktion an der Zeilengrenze.
- [ ] Hell/Dunkel, alle drei Schriftgrößen, kleine Fensterhöhe und Tastaturbedienung des
      Importdialogs; Escape und Abbrechen dürfen nichts verändern.

## Weiterhin offen aus 3.17 und früher

- [ ] Druckausgabe: alle vier Formate auf Papier und als PDF, Optionen, Seitenumbrüche,
      HTML-Datei in einem zweiten Browser.
- [ ] App-Backup: Speichern, Wiederherstellen mit Vorschau, Teilbereiche,
      Rückfallsicherungen – nur mit getrenntem Datenordner.
- [ ] Tagesplanung: Tageswechsel, Zähler, Summen, Kapazitätsgrenzen, Kontextmenü,
      Serienvorrücken.
- [ ] Mit physischem Mac-Trackpad auf Startseite, Tabelle, Tagesplanung, Diagrammen,
      Vorlagen und Listen scrollen.
- [ ] Light/Dark: Tabellenkopf, Vorlageneditor, Punktdetails, Label-Unterdialog und
      App-weite Auswahlfelder.
- [ ] Aktuelle Änderungen auf Windows mit Tk 8.6 und hoher Skalierung nachprüfen.
- [ ] Längere Nutzung, mehrere Monitore, synchronisierte Ablagen, Installer/Signatur und
      Upgrade separat abnehmen.

Nur getrennte Testdaten verwenden. Bereits bestehende Nutzerdaten nicht durch
Beispielbackups ersetzen.
