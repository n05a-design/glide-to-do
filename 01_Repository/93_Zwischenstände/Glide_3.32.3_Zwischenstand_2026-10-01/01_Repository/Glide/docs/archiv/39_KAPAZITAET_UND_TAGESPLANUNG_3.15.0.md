# Tagesplanung und Kapazität – Glide 3.15.0

Stand: 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Bearbeitungstag und geschätzter Aufwand liegen seit 3.14 an der Aufgabe. 3.15 führt sie
zu einer Planungsaussage zusammen: Wie viel Arbeit ist für einen Tag vorgesehen, und wie
verhält sich das zu einer selbst gesetzten Tageskapazität. Gerechnet wird ausschließlich
mit vorhandenen Feldern; es entsteht keine neue Aufgabeneigenschaft und kein neues
Datenformat.

## Bedienung

- **Ansicht „Tagesplanung"** in der Seitenleiste, auf der Startseite und im Menü
  **Ansicht**. Sie zeigt alle Aufgaben und Long-Tasks, deren Bearbeitungstag auf dem
  gewählten Tag liegt – vorbelegt mit heute. Sortiert wird nach Wichtigkeit, dann
  Fälligkeit, dann Titel.
- **Tageswechsel** über die Schaltflächen „◀" und „▶" in der Suchzeile sowie über
  **Ansicht → Tagesplanung: Tag zurück / Tag vor**; damit sind beide Richtungen auch
  über die durchsuchbaren App-Aktionen erreichbar. Der betrachtete Tag steht im
  Fenstertitel und in der Kopfzeile.
- **Kontextmenü einer Zeile** verschiebt den Bearbeitungstag um einen Tag vor oder
  zurück und entfernt ihn. Die Fälligkeit bleibt dabei unverändert. Öffnen in der
  Quellliste, Bearbeiten, Erledigen, Wichtigkeit und Reiter verhalten sich wie in
  „In Bearbeitung".
- **Einstellungen → Profil und Startseite → „Tageskapazität · Minuten (0 = aus)"**
  setzt den Vergleichswert. Zulässig sind ganze Minuten von 0 bis 1440.
- **Summen** stehen in der Kopfzeile der Tagesplanung, in „Mein Tag", in der
  Tabellenansicht und als Zeile „Heute geplant" in der Bestandskachel der Startseite.
  Die Startseitenzeile erscheint nur, wenn für heute tatsächlich ein Bearbeitungstag
  eingetragen ist, und verweist in die Tagesplanung.

Alle Anzeigen funktionieren in Hell und Dunkel, in allen drei Schriftgrößen, bei
kleiner Fensterhöhe und mit Tastatur.

## Rechenregeln

- Gezählt werden ausschließlich Punkte, für die `is_schedulable_item` zutrifft, also
  Aufgaben und Long-Tasks. Gruppen und Zwischenüberschriften tragen keine Planung und
  erscheinen in keiner Summe.
- Die **Tagesplanung** summiert `estimated_minutes` aller Punkte mit
  `planned_date == <Tag>`. Maßgeblich ist der Bearbeitungstag, nicht die Fälligkeit.
- **„Mein Tag"** summiert nur die eigene, bewusst zusammengestellte Auswahl –
  unabhängig davon, welchen Bearbeitungstag diese Punkte tragen. Beide Summen bleiben
  getrennt; die Auswahl wird nicht automatisch aus Bearbeitungstagen gefüllt.
- Die **Tabellenansicht** summiert die aktuell sichtbaren Zeilen und folgt damit Suche
  und Offenfilter. Die Tagessumme bleibt davon unberührt.
- Ein Punkt **ohne Aufwandsangabe** wird nicht geschätzt, sondern getrennt gezählt:
  „3 h 15 min geplant · 1 ohne Schätzung". Ein ungültiger Wert am Punkt zählt ebenso
  als „ohne Schätzung", statt die Summe zu verfälschen.
- **Erledigte** Punkte bleiben in der Summe und werden zusätzlich ausgewiesen:
  „… · davon 1 h erledigt". Eine Planung, die beim Abhaken schrumpft, ließe sich
  hinterher nicht mehr nachvollziehen.
- Bei **aktiver Kapazität** nennt die Anzeige die Restmenge mit Bezugsgröße:
  „… · 2 h 45 min frei von 5 h" beziehungsweise „… · 15 min über 2 h". Farbe allein
  trägt keine Aussage.
- **Wiederholungen** rechnen nur mit dem aktuellen Vorkommen. Beim Vorrücken einer
  erledigten Serie wird der Bearbeitungstag wie bisher geleert; es entsteht keine
  vorausberechnete Summe für einen künftigen Tag.

## Speicherung

Die Kapazität liegt additiv als `daily_capacity_minutes` in `settings.json` und wird wie
`daily_goal` normalisiert: ganze Minuten von 0 bis 1440, Vorgabe 0. Ein fehlender,
beschädigter oder fremder Wert führt auf 0 zurück, damit nie eine erfundene Kapazität in
der Anzeige steht. 0 schaltet den Vergleich ab; die Summen bleiben sichtbar.

Der betrachtete Planungstag ist eine Angabe der laufenden Sitzung und wird nicht
gespeichert – nach einem Neustart beginnt die Ansicht bei heute, statt einen vergangenen
Tag als Planung anzuzeigen. Es wird keine Tagesbilanz gespeichert: Jede Summe entsteht
bei der Anzeige aus dem aktuellen Bestand. Aufgabenformat 14, Einstellungsformat 2 und
Vorlagenformat 2 bleiben unverändert; Aufgabenbackups enthalten weder Kapazität noch
Ansichtszustand. [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md).

## Grenzen

Keine Zeiterfassung und keine gemessene Ist-Dauer. Keine automatische Verteilung von
Aufgaben auf Tage und keine Vorschläge, welche Aufgabe zu verschieben wäre. Keine
Auslastungsquote über mehrere Tage und keine Bewertung der arbeitenden Person: Die
Anzeige vergleicht geplante Minuten mit einem selbst gesetzten Wert und nichts sonst.
Kein Wochentagsprofil und keine Kapazität je Liste in dieser Stufe. Keine neue
Laufzeitabhängigkeit, kein Hintergrundprozess, kein Netzzugriff.

Eine Schätzung bleibt eine Schätzung. Aus der Summe folgt keine Zusage gegenüber
Dritten, und ein voller Tag ist kein technischer Fehlerzustand.

## Abnahmekriterien

1. Eine Aufgabe mit Bearbeitungstag und Aufwand erscheint in der Tagessumme genau
   einmal, auch wenn sie zusätzlich in „Mein Tag" liegt.
2. Aufgaben ohne Aufwand verändern die Summe nicht und werden als Anzahl genannt.
3. Gruppen und Zwischenüberschriften bleiben in jeder Summe unberücksichtigt.
4. Erledigen, Rückgängig, Verschieben, Kopieren und Löschen aktualisieren die Summen
   sofort und ohne Neustart.
5. Das Vorrücken einer Serie entfernt den Punkt aus dem alten Tag und erzeugt keine
   Summe für einen künftigen Tag.
6. Kapazität 0, 1 und 1440 sowie ungültige Eingaben verhalten sich wie festgelegt; ein
   beschädigter Einstellungswert führt auf 0 zurück.
7. Tabellenfilter und Suche verändern die Tabellensumme, nicht die Tagessumme.
8. Alle Dialoge und Zeilen sind in Hell und Dunkel bei 780×640 vollständig erreichbar.

## Prüfung

Die Suite `tests/integration/test_features315.py` prüft mit isoliertem `GLIDE_DATA_DIR`
Rechenregeln und Grenzwerte, Einstellungsmigration und Rückfall, Menge, Reihenfolge und
Leertext der Ansicht, Tageswechsel, Sidebar-Zähler, Such- und Offenfilter, Punktaktionen
mit Rückgängig, ungültige Tage, Serienvorrücken, Tabellensumme, Startseitenzeile sowie
den Einstellungsdialog in beiden Themes bei 780×640. Der Gesamtlauf umfasst damit
19 Suiten. [QA-Bericht](../07_QA_BERICHT.md) · [Release-Checkliste](../10_RELEASE_CHECKLIST.md).

[Bearbeitungstag und Aufwand 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md) ·
[Mein Tag 3.12](35_MEIN_TAG_3.12.0.md) ·
[Tabellenansicht 3.13](36_TABELLENANSICHT_3.13.0.md)
