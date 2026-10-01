# CSV-Import mit Spaltenzuordnung – Glide 3.18.0

Stand: 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Glide schreibt seit langem CSV-Dateien, lesen konnte es bisher nur eigene TXT-Exporte und
Backups. Wer eine Liste aus Excel, Numbers, einem Ticketsystem oder einer anderen
Aufgabenverwaltung mitbringt, musste sie abtippen. 3.18 liest CSV-Dateien beliebiger
Herkunft, zeigt vor der Übernahme, welche Spalte in welches Feld läuft, und übernimmt erst
danach.

## Bedienung

- **Datei → „CSV importieren …“** oder im Kontextmenü einer Liste unter „Exportieren“ der
  Eintrag „CSV importieren …“; beide öffnen zuerst die Dateiauswahl, dann den
  Zuordnungsdialog.
- Der Dialog nennt oben **Dateiname, erkannte Kodierung, erkanntes Trennzeichen sowie die
  Zahl der gelesenen Zeilen und Spalten**. Trennzeichen (automatisch, Semikolon, Komma,
  Tabulator, senkrechter Strich) und Kodierung (automatisch, UTF-8, Windows-1252, UTF-16)
  sind umstellbar; **„Erste Zeile enthält Spaltennamen“** ist vorbelegt, wenn die Datei
  einen Kopf erkennen lässt. Jede dieser drei Änderungen liest die Datei neu ein und
  aktualisiert Vorschau und Zuordnung.
- In der **Zuordnung** trägt jedes Glide-Feld ein Auswahlfeld mit allen Spalten der Datei
  und dem Eintrag „– nicht übernehmen –“. Zuordenbar sind: Aufgabe (Pflicht),
  Beschreibung, Erledigt, Wichtigkeit, Fällig, Uhrzeit, Art, Labels, Bearbeitungstag,
  Aufwand in Minuten sowie Ebene und Nummer für die Verschachtelung.
- Die **Vorschau** zeigt die ersten acht Datenzeilen in der Form, in der Glide sie anlegen
  würde: Einrückung, Art, Erledigt-Zustand und die übernommenen Zusatzangaben.
- **Ziel**: „Als neue Liste“ (vorbelegt, Titel aus dem Dateinamen, in der Ordneransicht im
  geöffneten Ordner) oder „An die geöffnete Liste anhängen“ – letzteres nur, wenn eine
  Liste geöffnet ist.
- **„Importieren“** übernimmt, **Abbrechen** und Escape lassen den Bestand unverändert. Der
  Abschluss meldet, wie viele Punkte entstanden sind, wie viele Zeilen übersprungen wurden
  und wie viele Zellen nicht gelesen werden konnten – mit den ersten drei Beispielen samt
  Zeilennummer. Ein Import ist ein einzelner Schritt und mit **Rückgängig** vollständig
  zurücknehmbar, einschließlich der dabei neu angelegten Labels.

## Spaltenerkennung

Die Zuordnung wird aus den Spaltennamen vorbelegt. Erkannt werden die eigenen
Exportbezeichnungen sowie gängige deutsche und englische Schreibweisen (etwa „Aufgabe“,
„Titel“, „Task“, „Subject“ für den Punkttext, „Fällig“, „Frist“, „Due Date“, „Deadline“
für die Fälligkeit, „Tags“, „Kategorie“ für Labels). Groß- und Kleinschreibung,
Leerzeichen, Unterstriche und Klammerzusätze spielen keine Rolle. Ohne Kopfzeile heißen
die Spalten „Spalte 1“, „Spalte 2“ … und werden nicht vorbelegt; die Zuordnung erfolgt
dann von Hand.

Eine von Glide geschriebene CSV-Datei wird vollständig erkannt: **Export und Import sind
zueinander umkehrbar**, einschließlich Verschachtelung, Art, Erledigt-Zustand,
Wichtigkeit, Fälligkeit mit Uhrzeit, Labels, Bearbeitungstag und Aufwand. Die Spalte
„Anhänge“ wird als solche erkannt, aber nicht übernommen: Ein Dateiname ohne Datei ist
kein Anhang.

## Werteregeln

| Feld | Gelesen wird |
| --- | --- |
| Aufgabe | Pflichtfeld. Leere Zelle überspringt die Zeile. Mehrzeilige Zellen ergeben einen Long-Task. |
| Beschreibung | Freier Text, Zeilenumbrüche bleiben erhalten. |
| Erledigt | `ja`, `x`, `1`, `wahr`, `true`, `erledigt`, `done`, `abgeschlossen` gelten als erledigt; `nein`, `0`, `falsch`, `false`, `offen`, `open`, `-` und leer als offen. |
| Wichtigkeit | `keine`/`niedrig`/`mittel`/`hoch`, `0`–`3`, `low`/`medium`/`high`. |
| Fällig, Bearbeitungstag | `TT.MM.JJJJ`, `TT.MM.JJ`, `JJJJ-MM-TT`, `TT-MM-JJJJ`, `TT/MM/JJJJ`. |
| Uhrzeit | `HH:MM`, `HH.MM`, `HHMM`, `HH`; ohne Fälligkeit wirkungslos. |
| Art | `Aufgabe`, `Gruppe`, `Long-Task`, `Überschrift`, `Zwischenüberschrift` und die englischen Schlüssel `task`, `group`, `long`, `heading`. |
| Labels | Mehrere Werte, getrennt durch `\|`, Komma oder Semikolon; höchstens zwanzig je Punkt. Fehlende Labels entstehen neu, vorhandene werden nach Namen wiederverwendet. |
| Aufwand | Ganze Minuten (`45`), Stunden-Minuten (`1:30`), mit Einheit (`45 min`, `1,5 h`). |
| Ebene, Nummer | Ebene: `1` ist die oberste. Nummer: `2.1.3` ergibt Ebene 3. Ist beides zugeordnet, entscheidet die Ebene. |

Werte, die keiner Regel folgen, lassen ihr Feld leer und werden im Abschlussbericht
gezählt – die Zeile selbst geht dadurch nicht verloren. Ein führendes Apostroph, mit dem
der eigene Export Tabellenprogramme vom Rechnen abhält, wird beim Lesen wieder entfernt.
Gruppen und Überschriften tragen weiterhin keinen Erledigt-Zustand, keine Wichtigkeit und
keine Fälligkeit; entsprechende Zellen werden für diese Arten verworfen.

## Verschachtelung

Ist Ebene oder Nummer zugeordnet und **„Verschachtelung übernehmen“** angehakt, entsteht
ein Baum: Jede Zeile hängt unter der letzten Zeile geringerer Ebene. Ein Sprung um mehr
als eine Stufe wird auf eine Stufe begrenzt, eine Zeile mit Ebene über eins ohne
vorangehenden Elternpunkt landet auf der obersten Ebene. Ohne Zuordnung oder ohne Häkchen
wird flach importiert.

## Grenzen

Höchstens **5000 Zeilen** und **64 Spalten** je Datei, Dateigröße bis **12 MB**; darüber
bricht der Import mit Begründung ab, bevor etwas entsteht. Keine Anhänge, keine
Wiederholungsregeln, keine Erinnerungen, keine Farben, keine Ordnerstruktur aus einer
Spalte, kein Abgleich mit bestehenden Punkten – ein Import legt immer neue Punkte an und
überschreibt nie vorhandene. Kein XLSX (Tabellenprogramme speichern CSV), kein
gespeichertes Zuordnungsprofil, keine automatische Wiederholung eines Imports, kein
Zeitplan. Keine neue Laufzeitabhängigkeit: Kodierungs- und Trennzeichenerkennung, Lesen
und Zerlegen erledigt die Standardbibliothek. Das Aufgabenformat bleibt **14**; der Import
erzeugt ausschließlich Objekte, die Glide auch von Hand anlegen könnte.

## Abnahmekriterien

1. Eine mit „Als CSV“ geschriebene Liste lässt sich vollständig zurücklesen: Struktur,
   Art, Erledigt, Wichtigkeit, Fälligkeit samt Uhrzeit, Labels, Bearbeitungstag und
   Aufwand stimmen mit dem Ausgangsbestand überein.
2. Semikolon, Komma, Tabulator und senkrechter Strich werden automatisch erkannt; die
   manuelle Wahl überstimmt die Erkennung.
3. UTF-8 mit und ohne BOM, Windows-1252 und UTF-16 werden gelesen; Umlaute bleiben
   erhalten.
4. Ohne Kopfzeile heißen die Spalten „Spalte n“, die Zuordnung bleibt leer und der Import
   arbeitet mit der Hand-Zuordnung.
5. Jede Werteregel der Tabelle greift; unlesbare Zellen bleiben leer und werden gezählt,
   ohne die Zeile zu verwerfen.
6. Zeilen ohne Aufgabentext werden übersprungen und gezählt.
7. Verschachtelung entsteht aus Ebene und aus Nummer, Sprünge werden begrenzt, ohne
   Häkchen wird flach importiert.
8. Ziel „neue Liste“ und Ziel „geöffnete Liste“ landen am richtigen Ort; in der
   Ordneransicht liegt die neue Liste im geöffneten Ordner.
9. Zeilen-, Spalten- und Größengrenze brechen vor jeder Bestandsänderung ab.
10. Rückgängig nimmt einen Import vollständig zurück, einschließlich neu angelegter
    Labels; Abbrechen und Escape ändern nichts.
11. Der Dialog ist in Hell und Dunkel bei 780×640 vollständig erreichbar.

## Prüfung

Die Suite `tests/integration/test_features318.py` prüft mit isoliertem `GLIDE_DATA_DIR`
den Rundlauf über eine echte Exportdatei, alle vier Trennzeichen und vier Kodierungen,
Dateien mit und ohne Kopfzeile, die automatische Spaltenerkennung samt Synonymen, jede
Werteregel einschließlich Grenz- und Fehlwerten, Verschachtelung aus Ebene und Nummer,
beide Importziele, die drei Grenzen, den Bericht über übersprungene Zeilen und unlesbare
Zellen, Rückgängig mit Labelrücknahme sowie den Dialog in beiden Themes bei 780×640. Der
Gesamtlauf umfasst damit 22 Suiten.
[QA-Bericht](../07_QA_BERICHT.md) · [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md) ·
[Druck und PDF 3.17](41_DRUCK_UND_PDF_3.17.0.md)
