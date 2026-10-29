# Bildreferenzen zum UI-/UX-Feature-Paket

Stand 28.10.2026 · Glide 3.49.0 · 28 unveränderte, vom Benutzer bereitgestellte Originalbilder

Die IDs entsprechen exakt der Reihenfolge der 28 Bilder im Chat. Die Zuordnung ist redaktionell und benennt sichtbare Befunde oder Referenzen; nicht jedes Bild zeigt einen Fehler. [Auftrag](AUFTRAG.md), [Ausführungsprompt](PROMPT.md) und [Manifest](screenshots.json) bilden das zusammenhängende Paket.

Die Einzelbilder wurden nicht neu aufgenommen oder bearbeitet. Der im Auftrag genannte Zeitpunkt 15.10.2026, 13:42 Uhr ist keine verifizierte Aufnahmezeit jedes Bildes. Prüfsummen im Manifest wurden beim Kopieren gegen die temporären Originale verglichen.

**Lokale Originale (Pfade ohne Link, weil der Ordner nicht im Repository liegt):** Bilder enthalten teilweise Konto-, E-Mail- und andere personenbezogene Angaben, insbesondere S11 und einzelne Notion-Ansichten. Das Verzeichnis `bilder/` ist in der Wurzel-`.gitignore` ausgeschlossen. Bei Übergabe an einen anderen KI-Agenten ausdrücklich mitgeben; ein Git-Clone reicht dafür nicht. Für öffentliche Verwendung erst gesonderte datensparsame Fassungen vorbereiten, Originale unverändert erhalten.

**Beleggrenzen:** B01 benötigt einen nachgestellten Klick-/Scrollablauf. Für B04 liegt keine eigene Galerieaufnahme und für B18 keine geöffnete Neuerungs-/Über-Glide-Ansicht vor. S05/S06 zeigen die gemeldete Scrollfolge, beweisen aber nicht deren technische Ursache. Statische Notion-Screenshots belegen kein Laufzeitverhalten.

| ID / Bild | Anwendung | Abmessungen | Anforderungen | Sichtbarer Inhalt / Zweck |
|---|---|---|---|---|
| S01 · `bilder/01-glide-startseite-vorher.png` | Glide | 1888 × 940 | B01, B03, B04, B07, B09, B10 | Startseite mit tief beginnendem Kartenbereich; Gismo mit Spielereien- und Benennen-Buttons. Kein direkter Nachweis des Klickablaufs. |
| S02 · `bilder/02-glide-menue-datum-hinweise.png` | Glide | 330 × 71 | B06, B07 | Ausschnitt der Kopfmenüs mit Datum und Fragezeichen darunter. |
| S03 · `bilder/03-glide-kopfzeile-suche.png` | Glide | 578 × 78 | B06, B07, B10 | Kopfmenüs und Aktionsbuttons; Suchbeschriftung Su und abweichende optische Höhen. |
| S04 · `bilder/04-glide-seiten-blockleiste.png` | Glide | 729 × 45 | B14 | Blockleiste einer Seite; nur Aufgabe trägt eine Checkbox vor dem Text. |
| S05 · `bilder/05-glide-bildseite-vor-scrollen.png` | Glide | 810 × 828 | B16 | Bildseite vor dem kleinen Scrollschritt: großes Architekturbild und erster Folgeabsatz. |
| S06 · `bilder/06-glide-bildseite-nach-scrollen.png` | Glide | 815 × 820 | B16 | Bildseite nach dem Scrollschritt: Beginn des ersten Folgeabsatzes fehlt. Zusammen mit S05 betrachten. |
| S07 · `bilder/07-glide-notiz-aktionshintergruende.png` | Glide | 581 × 166 | B17, B19 | Notiz-/Notizbuchaktionen mit sichtbaren Hintergrundkästen; verwandte Referenz für Listenaktionen. |
| S08 · `bilder/08-glide-logo-hoehe.png` | Glide | 658 × 88 | B05 | Glide-Logo neben Titel und zweiter Statuszeile mit offenen/überfälligen Punkten. |
| S09 · `bilder/09-glide-punkteditor-geteilte-ansicht.png` | Glide | 1662 × 1607 | A02, B05, B17, B19 | Geteilte Punktbearbeitung mit verschiebbarem Trenner; Felder, Datumsbereiche und Aktionshintergründe. |
| S10 · `bilder/10-microsoft-to-do-kompakt.png` | Microsoft To Do | 507 × 515 | A01 | Microsoft To Do in kompakter Ansicht ohne Seitenleiste; Referenz für A01. |
| S11 · `bilder/11-microsoft-to-do-normal.png` | Microsoft To Do | 1206 × 941 | A01 | Microsoft To Do in normaler Ansicht mit Seitenleiste; enthält sichtbare Kontodaten. |
| S12 · `bilder/12-notion-fenster-tabs-leere-seite.png` | Notion | 1919 × 1030 | A02, A03 | Notion-Gesamtfenster mit Tabs, Seitenleiste und leerer Seite; statische Designreferenz. |
| S13 · `bilder/13-notion-ansichten-menue.png` | Notion | 860 × 289 | A03 | Notion-Auswahl Tabelle, Board, Liste, Timeline, Kalender, Galerie und Import; nicht alles ist beauftragt. |
| S14 · `bilder/14-notion-seitenaktionen.png` | Notion | 272 × 604 | A03 | Notion-Seitenaktionsmenü mit Aktionssuche, Duplizieren, Verschieben, Versionshistorie und weiteren Einträgen. |
| S15 · `bilder/15-notion-seitenkopf.png` | Notion | 380 × 115 | A03 | Notion-Seitenkopf mit Icon-, Cover- und Kommentarangebot; Hierarchiereferenz. |
| S16 · `bilder/16-notion-blockaktionen.png` | Notion | 1039 × 493 | A03 | Notion-Blockaktionsmenü, Suchfeld, Blockhandle und markierter Block. |
| S17 · `bilder/17-notion-blocktypen.png` | Notion | 492 × 724 | A03 | Notion-Menü für Blockumwandlung, darunter Überschriften, Listen, Zitat, Code und Spalten; Produktgrenzen beachten. |
| S18 · `bilder/18-glide-heute-pfeile.png` | Glide | 559 × 226 | B12, B13 | Heute-Ansicht: doppelte Pfeile und stark betonte nächste Aufgabe. |
| S19 · `bilder/19-glide-naechste-aufgabe-metadaten.png` | Glide | 1578 × 66 | B11, B12, B13 | Nächste Aufgabe mit stark hervorgehobenen Datums-/Labelmetadaten und verfügbarem Titelraum. |
| S20 · `bilder/20-glide-startseite-anpassen.png` | Glide | 1891 × 856 | B02, B03, B04 | Startseite mit Startseite anpassen isoliert rechts unten; Gismo ohne separate Buttons. |
| S21 · `bilder/21-glide-papierkorb-ueberdeckung.png` | Glide | 838 × 365 | B15 | Papierkorb-Leertext in kleinem Fenster; Text überdeckt den darunterliegenden Button. |
| S22 · `bilder/22-glide-labels-titel-abgeschnitten.png` | Glide | 858 × 992 | B11 | Labels-Ansicht: stark abgeschnittene Titel neben umfangreichen Datums-/Uhrzeitangaben. |
| S23 · `bilder/23-glide-fehlerprotokoll-flucht.png` | Glide | 606 × 256 | B08 | Leeres Fehlerprotokoll: Überschrift und Text beginnen an unterschiedlichen linken Kanten. |
| S24 · `bilder/24-glide-seitenleiste-symbolhoehen.png` | Glide | 236 × 505 | B09 | Seitenleiste mit Aufklapppfeilen und Papierkorbsymbol; optische Zentrierung prüfen. |
| S25 · `bilder/25-github-projektuebersicht.png` | GitHub | 3247 × 2031 | B20, B21, B22 | GitHub-Projektübersicht mit bestehendem Design-Skillnamen, Dateistruktur und README-Stand. |
| S26 · `bilder/26-github-readme-funktionen.png` | GitHub | 1128 × 2016 | B21, B22 | GitHub-README mit Schnellstart, Funktionen, Mindestgröße und Ablagetabelle. |
| S27 · `bilder/27-github-readme-ablage-regeln.png` | GitHub | 1129 × 1825 | B21, B22 | GitHub-README mit Ablage-, Dokumentations-, Qualitäts- und Veröffentlichungsregeln. |
| S28 · `bilder/28-glide-startseite-kartenlayout.png` | Glide | 1023 × 880 | B04, B09, B11 | Startseite bei schmalerem Inhaltsbereich: Pinnwände, Pinnwandvorschau, Zeichnungen und Kartenlayout. |

B20–B22 betreffen zusätzlich das vollständige Paket und seine Pflege. Fehlende Bildreferenz bedeutet nicht, dass eine ausdrückliche Textanforderung entfällt.
