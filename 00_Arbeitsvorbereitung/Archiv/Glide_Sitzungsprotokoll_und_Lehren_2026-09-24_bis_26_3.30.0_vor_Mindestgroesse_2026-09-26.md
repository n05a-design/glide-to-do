# Sitzungsprotokoll und Lehren für die Arbeitsvorbereitung – 24.–26.09.2026

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Die Arbeitsvorbereitung wertet hier die Sitzung vom 24. bis 26.09.2026 aus.
Im Mittelpunkt steht, was die Planung richtig vorhergesehen hat, was nicht
und wie die nächste Arbeitsvorbereitung aussehen sollte.

Die vollständige Chronologie steht im
[Sitzungsprotokoll 67](../01_Repository/Glide/docs/67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md).
Dort finden sich auch alle Rückfragen mit Antworten, die Entscheidungen des
Agenten, die Prüfläufe und die technischen Lehren.

## 1. Ablauf in Kürze

1. **24.09.:** Die Arbeitsanleitung aus den Dokumenten 61/62 wurde zu Glide
   3.29.0 (Zeichnungsseite, Format 19). Danach eine Nachbesserung nach der
   Rückmeldung: Farbspektrum mit voller Helligkeit, Scrollleisten nur bei
   Bedarf.
2. **25.09., vormittags:** Aus der Online-Recherche entstanden
   [Wettbewerbsrecherche](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md),
   [Arbeitsvorbereitung](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md)
   und [Aufgabenkatalog](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md):
   44 Pakete und die Entscheidungen E-01 bis E-16.
3. **25.09.:** „Alle Aufgaben bündeln und abarbeiten“ führte zu einer
   Rückfrage (alle Empfehlungen und sechs Zusatzideen, Design „Pixel“) und
   dann zu Glide 3.30.0 mit Format 20.
4. **25./26.09.:** „Weiter“ führte zu einer zweiten Rückfrage (wieder alle
   Empfehlungen) und zum Ausbau.
   - Die Echtdatenprobe mit einer Kopie fand, dass 3.29 einen
     Format-20-Bestand überschreibt; daraus entstanden Schutzmaßnahmen.
   - Die abschließende Vollprüfung ist grün.
5. **26.09.:** Dieses Protokoll und der Dokumentabgleich. Überholte Berichte
   sind archiviert, widerlegte Aussagen berichtigt.
6. **26.09.:** „Die nächsten Aufgaben“: Nach einer Rückfrage mit den
   verbleibenden Grenzen und Release-Vorbereitungen – alle gewählt – folgte
   der zweite Ausbau. Er umfasst:
   - Anhänge im Detailbereich;
   - Zeichnungen in Folien;
   - Stundenraster;
   - Gruppierung mit Überschriften;
   - Lasttest;
   - [Windows-Prüfpaket](Checklisten/Windows_Pruefung_3.30.0.md);
   - [Produktdatenblatt-Entwurf](../40_Store_Material/Produktdatenblatt_3.30.0_Entwurf.md).
7. **26.09.:** „Weiter mit den nächsten Aufgaben“: Der dritte Ausbau kam ohne
   Rückfrage aus, weil Vertrag 66 §11 die nächsten Aufgaben eindeutig nannte.
   Er umfasst:
   - Ziehen aus der Liste ins Stundenraster;
   - Nummern und Überschriften in der gruppierten Tabelle;
   - die Pixelschrift unter Linux;
   - einen mitbehobenen Menüfehler.

## 2. Was die Planung richtig vorhergesehen hat

- **Entscheidungen mit Empfehlung:** Die Nummern E-01 bis E-16 samt Empfehlung
  machten die Rückfrage kurz. Beide Male wählte der Nutzer „alle
  Empfehlungen“.
- **Datenklassen D0–D3:** Sie zeigten früh, welche Pakete ein neues
  Aufgabenformat brauchen. Das gebündelte Format 20 kam mit genau einer
  Migration aus.
- **Etappen nach Abhängigkeiten:** A bis E ließen sich in dieser Reihenfolge
  umsetzen, ohne Rückbau.
- **Pixel-Nische als Leitplanke:** Wettbewerbsideen wurden angepasst statt
  kopiert. Die Zeichnung bleibt ein Zellraster, und neue Sichtbarkeit
  entstand über Symbole, Galerie, Karten und Schrift.

## 3. Was die Planung nicht vorhergesehen hat

| Annahme in der Planung | Wirklichkeit | Folge |
|---|---|---|
| „Ältere Glide-Fassungen lehnen Format 20 sichtbar ab.“ | 3.29 meldet „beschädigt“, beginnt leer und **überschreibt** die Datei bei der ersten Eingabe | Schutz in 3.30, Warnung in allen Übergaben; die Annahme ist in Katalog und Arbeitsvorbereitung berichtigt |
| Erste Stufen reichen für AO-070 und MO-080 | Der Nutzer wollte gleich die zweite Stufe | Zweite Stufe am selben Tag umgesetzt |
| Pixelschrift nach offener Lizenzprüfung | Eine OFL-Schrift ließ sich sofort prüfen und bündeln | Pixelify Sans mit Herkunftsnachweis |
| Arbeitsbegleiter in Leerzuständen erst nach Stufe 3 | Ein stiller Auftritt (Stufe 2) genügt | Gismo statisch, abschaltbar |
| Prüfläufe sind tagesunabhängig | Ein Lauf über Mitternacht brach den Releaseabgleich | `pruefen.py` vergleicht das Momentdatum relativ |

## 4. Empfehlungen für die nächste Arbeitsvorbereitung

1. **Rückwärtsverhalten prüfen, nicht annehmen.** Vor jedem Formatwechsel mit
   der Vorgängerversion und einer Kopie echter Daten messen, was diese mit dem
   neuen Format macht.
2. **Schutz vor unbekannten Formaten eine Version vorher einbauen.** 3.30 hat
   ihn jetzt; ein Format 21 ist damit gegen einen Rückfall auf 3.30
   geschützt.
3. **Ausbaustufen gleich mitentscheiden lassen.** Die Rückfrage sollte „erste
   Stufe“ oder „vollständig“ als Option anbieten.
4. **Lizenzfragen sofort klären.** Offene Lizenzfragen bei Schriften, Bildern
   und Paletten gleich mit Quelle, Lizenz und Dateigröße vorlegen – das
   erlaubt eine Entscheidung in einer Rückfrage.
5. **Nach jeder Etappe Planungsdokumente inhaltlich abgleichen.** Nicht nur
   die Statusspalte, sondern auch Aussagen über den Ist-Zustand.
6. **Echte Daten nur als Kopie.** Vorher fragen, nur Zahlen berichten,
   Originale per Prüfsumme sichern.
7. **Vollprüfung ohne parallele Last** laufen lassen und über Mitternacht
   hinaus mit relativen Daten rechnen. Auch Archivkopien entstehen vor dem
   Lauf, nicht währenddessen.
8. **„Bekannte Grenzen“ als nächste Aufgabenliste pflegen.** Weil der Vertrag
   sie eindeutig führte, brauchte „weiter“ keine Rückfrage. Jede neue
   Grenze gehört sofort dorthin.

## 5. Stand der Planungsdokumente nach dem Abgleich

| Dokument | Stand |
|---|---|
| [Aufgabenkatalog](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md) | vollständig umgesetzt (3.30.0 mit Ausbau), Status je Paket |
| [Arbeitsvorbereitung](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md) | alle Entscheidungen „entschieden 25.09.2026“; Rückfall-Aussage berichtigt |
| [Wettbewerbsrecherche](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md) | Recherche vom 25.09.; ihre Ist-Spalten beschreiben 3.29 |
| [Aufgabensammlung Zeichenfläche](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md) | Status 3.30; offen nur ZF-200 (eigene Felder, Systembenachrichtigungen) und ZF-300 (nicht empfohlen) |
| [Funktionsvergleich](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md), [SVG-Untersuchung](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md) | Recherche vom 23.09.; Aussagen zu fester Größe 128 und 20er-Undo sind seit 3.30 überholt (Hinweis im Kopf) |
| [Prüfliste 3.30](Checklisten/Manuelle_Pruefung_3.30.0.md) | offen; Umstellung mit einer Kopie bereits automatisch geprüft |

## 6. Offene Punkte

- Manuelle Prüfungen nach den Prüflisten 3.30, 3.29 und 3.28 sowie die
  Windows-Vollprüfung mit dem neuen Paket.
- Freigabe des Produktdatenblatts nach der Abnahme; Inhaberangaben aus
  PRODUCT_IDENTITY.
- Signatur, Notarisierung, Installer, Markenprüfung, Store-Freigabe.
- Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste.
- Vorrat: Systembenachrichtigungen (ZF-200), führender Begleiter (braucht
  Onboarding), erweiterte Zeichenfunktionen aus ZF-300 (nicht empfohlen).
