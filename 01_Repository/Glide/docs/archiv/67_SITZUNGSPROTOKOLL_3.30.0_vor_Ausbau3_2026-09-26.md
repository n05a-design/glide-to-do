# Sitzungsprotokoll 24.–26.09.2026 – Zeichnungsseite, Modernisierung, Ausbau

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Dieses Protokoll hält eine zusammenhängende Arbeitssitzung zwischen Nutzer und
Agent fest: Aufträge, Rückfragen und Antworten, Entscheidungen samt Gründen,
das Getane, die Lehren und die offenen Punkte. Es ist ein festgeschriebener
Nachweis und ersetzt keine Verträge.

**Maßgeblich für den Stand sind:**

- [Projektübergabe](09_PROJECT_HANDOFF.md);
- [Vertrag 3.30](66_MODERNISIERUNG_3.30.0.md);
- [QA-Bericht](07_QA_BERICHT.md).

Die planungsseitige Auswertung mit Empfehlungen für die nächste
Arbeitsvorbereitung steht in
[`00_Arbeitsvorbereitung/Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md`](../../../00_Arbeitsvorbereitung/Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md).

## 1. Chronologie

| Zeit | Auftrag des Nutzers (sinngemäß) | Ergebnis |
|---|---|---|
| 24.09. | Die Arbeitsanleitung in den Dokumenten 61/62 umsetzen; die App liegt in `src/glide`, die startbare Kopie in `07_Python-Versionen`. Bei offenen Punkten fragen, sonst Aufgaben, Lehren und Probleme ablegen und die Doku aktuell halten, weil mehrere Agenten arbeiten. | Glide **3.29.0**: Zeichnungsseite als eigene Listenart, Aufgabenformat 19, eingebettete Fläche, Autosave, PNG-Referenz und Nachzeichnen ([Vertrag 3.29](65_ZEICHNUNGSSEITE_3.29.0.md)). |
| 24.09. | „Funktioniert wie ein Traum.“ Das Farbspektrum soll mit voller Helligkeit öffnen; Scrollleisten nur, wenn wirklich gescrollt werden kann; offene Punkte und Prüfergebnisse prüfen und dokumentieren. | Nachbesserung 3.29.0: Spektrum mit voller Helligkeit, Scrollbereich ohne Fokusrahmen-Überhang, Abnahmetests, QA-Bericht. |
| 25.09. | Online-Recherche gegen Notion, Trello, OneNote, Figma, Microsoft Planner und Affinity; die Pixel-Nische ist der USP. Daraus Recherche, Arbeitsvorbereitung und Aufgabenkatalog. | Drei Planungsdokumente in `00_Arbeitsvorbereitung`: 44 Pakete in fünf Etappen, 16 offene Entscheidungen E-01 bis E-16. Zusätzlich recherchiert: Aseprite, Pixelorama und Lospec für die Nische. |
| 25.09. | „Die Dokumentation durchsuchen, alle Aufgaben bündeln, prüfen, ob die älteren schon erledigt wurden, und dann komplett abarbeiten.“ | Rückfrage (Abschnitt 2), dann Glide **3.30.0** mit Aufgabenformat 20: alle Etappen und die „Später“-Pakete, erste Vollprüfung grün. |
| 25.09. | „Erneut versuchen“, ein abgebrochener Diagnoseaufruf, „weiter“ und ein zurückgesetztes Nutzungslimit | Unterbrechungen ohne inhaltliche Folgen; die Arbeit lief an der unterbrochenen Stelle weiter. |
| 25.09. | „weiter“ (nach dem Abschlussbericht 3.30) | Suche nach Offenem, zweite Rückfrage (Abschnitt 2), dann der Ausbau (Abschnitt 4) samt Echtdatenprobe. |
| 26.09. | „weiter“ (nach Unterbrechung) | Abschlusslauf ausgewertet, QA-Bericht, QA-Verlauf, Abgleich `07_Python-Versionen`, Endkontrolle. |
| 26.09. | Frage, ob die Doku vollständig abgelegt ist; den ganzen Chat mit Entscheidungen, Lehren und Tätigkeiten in Dokumentation und Arbeitsvorbereitung ablegen; Aktualität aller Dokumente prüfen, Überholtes archivieren, nicht mehr Zutreffendes entfernen. | Dieses Protokoll, das Gegenstück in der Arbeitsvorbereitung und der Dokumentabgleich (Abschnitt 6). |
| 26.09. | „Die nächsten Aufgaben“ – Rückfrage mit den verbleibenden Grenzen und Release-Vorbereitungen; alle sieben Punkte gewählt | Zweiter Ausbau (Abschnitt 6a): Anhänge im Detailbereich, Zeichnungen in Folien, Stundenraster, Gruppierung mit Überschriften, Lasttest, Windows-Prüfpaket, Produktdatenblatt-Entwurf. |

## 2. Rückfragen und Antworten des Nutzers

**25.09., vor 3.30.0:**

- E-01 bis E-16: **alle Empfehlungen**. Das Archiv (E-06) gehörte dazu – die
  Alternative „Ohne neues Datenformat“ hätte ausdrücklich „kein Archiv“
  bedeutet.
- Aus dem älteren Ideenvorrat: verknüpfte Punkte, Vorlagen mit Eingabefeldern,
  echte Abhängigkeiten, Tagesbeginn und Wochenrückblick, Kapazität je
  Wochentag, Zeiterfassung je Punkt.
- Visuelle Richtung nach dem Inspirationsbild: ein eigenes Design **„Pixel“**.
- Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste.

**25.09., nach dem ersten Abschluss 3.30.0** (wieder jeweils die Empfehlung):

- Ausbaustufen: Zeitblöcke per Ziehen, Präsentation als PDF, Rückgängig beim
  Kartenziehen, Detailbereich vollständig.
- Pixelschrift **Pixelify Sans** – einschließlich der Erlaubnis, die drei
  genannten Dateien herunterzuladen.
- Gismo **klein und statisch** in Leerzuständen.
- Umstellungstest **mit einer Kopie** des echten Bestands.

## 3. Entscheidungen des Agenten (mit Grund)

Nicht jede Frage war eine Produktentscheidung. Wo es eine übliche Lösung gab,
hat der Agent entschieden, ohne nachzufragen, und die Entscheidung
dokumentiert:

| Entscheidung | Grund |
|---|---|
| Archiv als Teil des gebündelten Formats 20 | Folgt aus der Antwort auf E-02/E-06 |
| Anordnungen Geordnet · Spalten · Frei | „Frei“ bleibt der letzte Eintrag wie bis 3.29; ältere Tests und Gewohnheiten |
| In der Liste bleibt Enter „abhaken“, in der Tabelle öffnet Enter den Detailbereich | Keine bestehende Tastenbedeutung brechen |
| Folien als Druckseite statt eigener PDF-Datei | Keine neue Laufzeitabhängigkeit (AGENTS.md, Regel 4); dieselbe Ausgabe wie „Drucken und PDF“ |
| Statische TTF-Schnitte von Pixelify Sans statt der variablen Schrift von Google Fonts | Tk (unter Windows GDI) kann variable Schriften nicht zuverlässig in Schnitten ansprechen |
| Zeitblöcke in der Zeitplanliste ziehen statt eines Stundenrasters | Passt zum bestehenden Umordnen (Zeilenhälfte), kein neues Bedienmodell |
| Detailbereich: Wechsel zu Gruppe/Überschrift mit Rückfrage | In der Maske sieht man den Wegfall der Planungsfelder vorher, im Bereich wirkt die Wahl sofort |
| Wiederholung und Beziehungen teilen Maske und Bereich (`read_repeat_rule`, `add_relation_targets`), Maskenlayout unverändert | Keine doppelte Logik, aber kein Risiko für die Layouttests der Maske |
| Neueres Format schreibgeschützt öffnen, unlesbare Datei vorher sichern, Rückfallwarnung | Ergebnis der Echtdatenprobe (Abschnitt 4) |
| Rückfallmarkierung erst mit echtem Inhalt, neutraler Warntext | Ein frisch angelegter, leerer Bestand soll keinen Fehlalarm auslösen |
| Zwei Testsuiten nicht anpassen, sondern das App-Verhalten verfeinern | Die Tests bildeten einen echten Anwendungsfall ab |
| Abgelöste Berichte 62–64 archivieren (26.09.) | Ihr Lesebestand und ihre Übergabe beschreiben den Stand vor 3.29/3.30 |

## 4. Ausbau und Befunde am 25./26.09.

- **Leere `window.conf` im echten Datenordner.** Ursache war ein zweites
  Beenden während der Speicherabfrage; es leerte die Datei. Fix:
  `on_close` läuft nur einmal, `save_window_geometry` schreibt atomar. Eine
  Testverletzung der Datenisolierung war es nicht (Sitzungsprotokoll
  geprüft).
- **Echtdatenprobe** – nur mit einer Kopie in einem temporären Ordner, nach
  Zustimmung:
  - 6 Seiten und 138 Punkte, nach der Umstellung auf Format 20 inhaltlich
    gleich;
  - Vorsicherung bytegleich;
  - Original vorher und nachher per SHA-256 gleich.
- **3.29 überschreibt Format 20.** Die Planung hatte angenommen, ältere
  Fassungen lehnten Format 20 sichtbar ab. Tatsächlich meldet 3.29 „beschädigt“,
  beginnt leer und überschreibt die Datei bei der ersten Eingabe. Daraus
  entstanden:
  - Schreibschutz für neuere Formate;
  - eine Kopie unlesbarer Dateien (`liste_unlesbar_*`);
  - `data_format_written` mit Warnung;
  - Warnungen in allen Übergabedokumenten.
- **Kaputtes JSON verhinderte jedes Speichern** – die Formatsicherungen lasen
  die Datei erneut. Nach der Kopie entfallen sie für die Sitzung.
- **Pixelschrift im Gesamttest nicht gefunden:** Die beim Aufbau gefüllte
  Familienliste kannte sie nicht. Jetzt fragt Glide Tk direkt und setzt die
  Überschriften 300 ms nach dem Start neu.
- **Umgesetzt** (siehe [Vertrag 3.30](66_MODERNISIERUNG_3.30.0.md), Abschnitte
  2 und 9):
  - Zeitblöcke ziehen und Alt+↑/↓;
  - Folien und Notizfolien als Druckseite;
  - Karten-Rückgängig;
  - Detailbereich mit allen Feldern außer Anhängen;
  - Gismo in Leerzuständen;
  - Pixelify Sans mit Herkunftsnachweis.

## 5. Prüfläufe

| Lauf | Ergebnis | Befund und Folge |
|---|---|---|
| [abschluss_2026-09-25](../tests/qa-3.30.0/abschluss_2026-09-25/ergebnis.json) | Exitcode 0, 52 Schritte | Erster Abschluss 3.30.0 |
| [ausbau_2026-09-25](../tests/qa-3.30.0/ausbau_2026-09-25/ergebnis.json) | Exitcode 1, 49 von 52 | Rückfallwarnung in zwei Altbestandstests → Markierung erst mit Inhalt. Release-Abgleich scheiterte über Mitternacht → `pruefen.py` vergleicht das Momentdatum relativ. |
| [ausbau_nachpruefung_2026-09-26](../tests/qa-3.30.0/ausbau_nachpruefung_2026-09-26/ergebnis.json) | Exitcode 1, 51 von 52 | `test_ui_followup36` unter Last → Sichtbarkeit im stabilen Endzustand messen |
| [ausbau_abschluss_2026-09-26](../tests/qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json) | **Exitcode 0, 52 Schritte** | Endstand des ersten Ausbaus |
| [ausbau2_2026-09-26](../tests/qa-3.30.0/ausbau2_2026-09-26/ergebnis.json) | **Exitcode 0, 52 Schritte** | Maßgeblicher Endstand nach dem zweiten Ausbau, ohne parallele Last |

Eine Wiederholung, die parallel zur Vollprüfung lief, scheiterte einmal am
Datenvergleich von `test_ui_followup36`. Drei Läufe ohne parallele Last
blieben grün und zeigten keinen Unterschied. Der Lasttest vom 26.09.
(Abschnitt 6a) konnte das auch unter vierfacher Last nicht wiederholen; die
Beobachtung gilt damit als Lastrauschen.

## 6. Dokumentabgleich am 26.09.

- **Archiviert** (verschoben nach `docs/archiv/`):
  - Zeichenflächen-Übergabe 62;
  - Archivprüfung 63;
  - Existenzprüfung 64.

  Die Verweise führen jetzt ins Archiv.
- **Korrigiert:**
  - Release-Checkliste (Quellstand und Migration standen auf 3.28/Format 18);
  - `src/glide/README.md` (Designs, Flächengrößen, Schriften);
  - Arbeitsbegleiter (zehn Designs);
  - die widerlegte Aussage „ältere Fassungen lehnen Format 20 sichtbar ab“ in
    Katalog und Arbeitsvorbereitung;
  - Überholt-Hinweise in den Planungs- und Recherchedokumenten vom 23. bis
    25.09.
- **Nach der Pflegeregel verschoben:** Die Prüfprotokolle `qa-3.25.0` bis
  `qa-3.27.0` (mindestens drei Versionen alt) liegen jetzt in
  `50_Ablage/QA/`; der Prüfverlauf verweist dorthin. Die Syntaxprüfung zählt
  deshalb 105 statt 107 Quelldateien – zwei Hilfsskripte lagen im Ordner
  `qa-3.26.0`.
- Die Verträge 45 bis 56 bleiben nach derselben Regel als fortgeltende
  Funktionsverträge aktiv.
- Jede geänderte Fassung liegt vorher unter
  `…_3.30.0_vor_Dokumentabgleich_2026-09-26` im jeweiligen Archiv.
- Geprüft wurden danach 75 aktive Dokumente ohne toten Link, der Index samt
  Archiv mit 924 Links und die Standprüfung.

## 6a. Zweiter Ausbau am 26.09.

**Entscheidungen des Agenten:**

- Die Version bleibt 3.30.0: derselbe unveröffentlichte Stand, kein neues
  Datenformat, nur ein zusätzlicher Einstellungsschlüssel `plan_day_grid`.
- Anhänge im Bereich nutzen die Ablage der Maske (`_store_pending_attachments`).
  Doppelte Dateien erkennt Glide an Name und Größe – der erste Entwurf verglich
  Pfade, die für abgelegte Kopien naturgemäß anders sind. Der Test fand das.
- Überschriften in gruppierten Listen sind synthetische Zeilen mit eigener
  Kennung je Abschnitt, weil dieselbe Überschrift in mehreren Abschnitten
  stehen kann.
- Das Stundenraster liegt rechts neben dem Zeitplan und nutzt
  `apply_time_plan`. Das Ziehen aus der Liste ins Raster bleibt als Grenze
  offen.
- Das Produktdatenblatt ist ein Entwurf. Store-Grenzen stammen aus der
  Recherche vom 04.09.2026; Inhaberangaben fehlen.
- Das Windows-Paket erzeugt genau eine Bildaufnahme (`release_hell.png`) –
  der erste Anleitungstext versprach mehr und wurde berichtigt.

**Lasttest:** Vier gleichzeitige Läufe von `test_ui_followup36`:

- Die Datenvergleiche blieben ohne Unterschied; die frühere Einzelbeobachtung
  ließ sich nicht wiederholen.
- Einmal scheiterte die Knopfsichtbarkeit, weil die Karte nach einmaligem
  Scrollen unter Last teils außerhalb des Sichtbereichs lag. Tk blendet
  eingebettete Widgets dort aus.
- Der Test scrollt deshalb vor jeder Messung neu. Die zweite Runde mit vier
  gleichzeitigen Läufen des korrigierten Tests war 4/4 grün.

## 7. Lehren

**Daten und Kompatibilität**

- Eine angenommene Eigenschaft älterer Versionen („lehnt sichtbar ab“) muss
  man prüfen, bevor sie in Übergaben steht. Eine Probe mit einer Kopie echter
  Daten fand in Minuten, was die Fixtures nicht zeigten.
- Jede Version braucht den Schutz vor unbekannten Formaten, *bevor* das
  nächste Format kommt – danach ist es für die alte Version zu spät.

**Tk und Oberfläche**

- `Canvas.lift` hebt Zeichenelemente, nicht das Widget; für Widgets
  `tk.call("raise", w._w)`.
- Was auf der Pinnwand bleiben soll, gehört in `draw_board`. Neuaufbauten nach
  Fokus- oder Größenwechsel löschen alles andere.
- Beim Schließen `winfo_exists()` prüfen und `after`-Aufträge bei `<Destroy>`
  abbrechen.
- Privat registrierte Schriften erscheinen unter macOS nicht verlässlich in einer
  früh gefüllten Familienliste. Deshalb direkt über `tkfont.Font(…).actual()`
  fragen.
- Die Reihenfolge in `_refresh_tree` (Notiz- und Zeichenleisten zuerst
  zurücksetzen) ist tragend.

**Tests**

- Neue modale Dialoge (etwa die Importvorschau) lassen ältere Tests warten,
  die `run_modal` nicht ersetzen.
- Tests, die Altbestände nachstellen, reagieren auf neue Schutzmechanismen.
  Zuerst fragen, ob der Test einen echten Anwendungsfall abbildet.
- Vergleiche mit Erzeugungsdaten brauchen relative Daten, sonst scheitern sie
  nach Mitternacht.
- UI-Messtests nie parallel zur Vollprüfung laufen lassen; unter doppelter
  Last werden sie unzuverlässig.
- Tastenereignisse in Tests erst nach `focus_force()` erzeugen.
- Ein Canvas blendet eingebettete Widgets außerhalb des Sichtbereichs aus.
  Wer Sichtbarkeit prüft, muss vor jeder Messung dorthin scrollen.
- Neue Menüaktionen brauchen einen Eintrag in der Gruppenzuordnung der
  App-Aktionen, sonst landen sie unter „Weitere Aktionen“ (Test prüft das).

**Arbeitsweise**

- Der Sitzungs-Arbeitsordner wird bei einem Neustart geleert. Fortschritt,
  Befunde und Zwischenstände gehören sofort in die Doku oder die
  Arbeitsvorbereitung.
- Vor jedem Überschreiben eines Dokuments die Archivkopie anlegen. Danach
  Index, Standprüfung und Linkprüfung laufen lassen.
- Rückfragen bündeln, jeweils mit Empfehlung. Nur echte Produktentscheidungen
  fragen, Download-Angaben (Datei, Quelle, Größe) gleich mitliefern.
- Planungsdokumente veralten mit der Umsetzung. Nach jeder Etappe ihren Status
  und ihre Aussagen abgleichen, nicht nur die Statusspalte.

## 8. Offene Punkte

- Manuelle Prüfung nach
  [Prüfliste 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md)
  (dazu 3.29 und 3.28). Sie umfasst:
  - echte Maus- und Trackpadbedienung;
  - PDF aus dem Browser;
  - die Pixelschrift unter macOS und Windows;
  - DPI-Skalierung und zwei Monitore;
  - Bildschirmleser;
  - einen Windows-Gesamtlauf.
- Nicht durch Agenten erledigbar: Signatur, Notarisierung, Installer,
  Markenprüfung, Store-Freigabe.
- Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste. Ein
  führender Begleiter setzt ein Onboarding voraus.
- Systembenachrichtigungen (ZF-200) und die nicht empfohlenen Punkte aus ZF-300
  bleiben im Vorrat.

**Wichtig für jeden Nutzer:** Nach dem ersten Start von 3.30 Glide 3.29 nicht
mehr starten.
