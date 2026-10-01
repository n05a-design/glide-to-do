# Dokumentationsindex

Aktueller Einstieg: [Fundament 3.33](73_FUNDAMENT_3.33.0.md), [Arbeitsrichtung und Abnahme](ARBEITSRICHTUNG.md), [Projektübergabe](09_PROJECT_HANDOFF.md), [Ausbau ab 3.32](68_AUSBAU_3.32.0.md), [Modernisierung 3.30](66_MODERNISIERUNG_3.30.0.md), [Sitzungsprotokoll 24.–26.09.2026](67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md), [QA-Bericht](07_QA_BERICHT.md), [Zeichnungsseite 3.29](65_ZEICHNUNGSSEITE_3.29.0.md) und [isolierter Zeichenflächenkern](61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md). Die Detaildokumente der vorherigen Versionen bleiben fachliche Nachweise für fortbestehende Funktionen; die Übergabe 62 und die Prüfberichte 63/64 vom 24.09.2026 sind seit dem 26.09.2026 archiviert.

Stand 01.10.2026 · Glide 3.33.1 · Aufgabenformat 20 · Einstellungen 2 · Vorlagenformat 2

## Begriffe

- **Aufgabenliste:** Listenart `tasks`; zeigt ihre Punkte als Liste, Tabelle
  oder Pinnwand.
- **Pinnwand (Aufgabenboard):** eine Ansicht auf Aufgabenpunkte einer Liste,
  eines Ordners oder des ganzen Bestands; kein eigener Inhaltstyp. Seit 3.30
  auch als Spaltenboard nach einem Feld, mit Bereichen und Zeichnungskarten.
- **Notizseite:** Listenart `note`; Rich-Text-Notiz mit Aufgabenbereich darüber.
- **Zeichenfläche / Zeichnungsseite:** Listenart `drawing` seit 3.29.0; eine
  Zellzeichnung ohne Punkte, seit 3.30.0 in 16, 32, 64 oder 128 Zellen je
  Seite, [Vertrag 3.29](65_ZEICHNUNGSSEITE_3.29.0.md) und
  [Pixel-Werkstatt 3.30](66_MODERNISIERUNG_3.30.0.md).
- **Notizbuch** (bis 27.09.2026 „Tagebuch“): Ordnerart `journal`; ordnet seit
  3.30.0 jede Inhaltsart nach Momentdatum.
- **Archiv:** Status `archived` einer Liste oder eines Ordners (Format 20);
  archivierte Seiten fallen aus der Planung heraus und bleiben zurückholbar.

## Aktueller Einstieg

Die Funktionsverträge 45–58 bleiben ausdrücklich aktive Verträge fortbestehender Funktionen; ihr historischer Einführungsstand wird erhalten. Frühere Momentaufnahmen und Übergaben sind im Archiv.

- [Entwicklungsplan ab 3.33 (Analyse 01.10.2026): Backlog notwendig/sinnvoll/Zukunft, Stufen 0–5, Abhängigkeiten, Risiken, Zielwerte](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md)
- [Entscheidungen D09–D17 vom 01.10.2026: Optionen, Empfehlung und Beschlüsse (D12 mit sieben Kacheln)](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)
- [Weitere Aufgaben und Richtungsauswahl nach 3.32.2: 24 Aufgaben, acht Richtungen, Codebezüge und offene Priorisierung](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md)
- [Arbeits- und Featureplanung 30.09.2026: Quellen, Versionen, Codebefunde, Bildschirmfotos, Entscheidungen D01–D07 und Performance-Abschlussaufgabe](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)

Die Planung nach 3.29.0 (Wettbewerbsrecherche, Arbeitsvorbereitung und
Aufgabenkatalog vom 25.09.2026) liegt außerhalb des Repositorys in
`00_Arbeitsvorbereitung/`. Mit 3.30.0 ist sie umgesetzt; Umfang, Datenvertrag
und Abweichungen stehen im Vertrag 66.

- [Ausbau ab 3.32.0: Etappen der Funktionsrecherche vom 30.09.2026 (Symbol-Export, Paletten, Platzhalter, Tagesabschluss)](68_AUSBAU_3.32.0.md)
- [Modernisierung 3.30.0: Pixel-Werkstatt, Format 20, Startseite, Board, Notizbuch, Seiten, Galerie, Tk 9 und Bilder in Seiten](66_MODERNISIERUNG_3.30.0.md)
- [Sitzungsprotokoll 24.–26.09.2026: Aufträge, Entscheidungen, Lehren, Prüfläufe](67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md)
- [Zeichnungsseite 3.29.0: Listenart, Format 19, Autosave, Referenz und offene Punkte](65_ZEICHNUNGSSEITE_3.29.0.md)
- [Zeichenfläche: isolierter Datenkern und Bedienprobe](61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md)
- [Tagebuch, Gismo und responsive Oberfläche 3.28.0](59_TAGEBUCH_UND_UI_3.28.0.md)
- [Flackern, Debugging und Ablageprüfung 3.28.0](60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md)
- [Übersichtlichkeit und Hierarchie 3.25.0](57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md)
- [Startseite und Begleiter 3.25.0](58_STARTSEITE_UND_BEGLEITER_3.25.0.md)
- [Navigation und Pinnwand 3.24.0](55_NAVIGATION_UND_PINNWAND_3.24.0.md)
- [Startseite, Startansicht und Rückmeldung 3.24.0](56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md)
- [Designsystem 3.23.0](50_DESIGNSYSTEM_3.23.0.md)
- [Leistung, Navigation und schmale Fenster 3.23.0](51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md)
- [Glide-Austauschformat 3.23.0](52_AUSTAUSCHFORMAT_3.23.0.md)
- [Pinnwand als Arbeitsfläche 3.23.0](53_PINNWAND_ARBEITSFLAECHE_3.23.0.md)
- [Anzeigemodi der Listenansicht 3.23.0](54_ANZEIGEMODI_3.23.0.md)
- [Entscheidung: Arbeitsbegleiter und Markenfigur](decisions/ARBEITSBEGLEITER.md)
- [Mein Tag – ein Tagesmodell statt zweier 3.22.0](46_TAGESMODELL_3.22.0.md)
- [Checkliste je Aufgabe 3.22.0](47_CHECKLISTE_3.22.0.md)
- [Ansichten und Startseite 3.22.0](48_ANSICHTEN_UND_STARTSEITE_3.22.0.md)
- [Pinnwand und Darstellung 3.22.0](49_PINNWAND_UND_DARSTELLUNG_3.22.0.md)
- [Kalenderimport aus ICS 3.21.0](45_KALENDERIMPORT_3.21.0.md)
- [QA-Bericht](07_QA_BERICHT.md)
- [Daten, Backups und Migration](06_DATA_BACKUP_MIGRATION.md)
- [Projektübergabe](09_PROJECT_HANDOFF.md)
- [Release-Checkliste](10_RELEASE_CHECKLIST.md)
- [Kalenderausgabe als ICS 3.20.0](archiv/44_KALENDERAUSGABE_3.20.0.md)
- [Dauerhafter Änderungsverlauf 3.19.0](archiv/43_AENDERUNGSVERLAUF_3.19.0.md)
- [CSV-Import mit Spaltenzuordnung 3.18.0](archiv/42_CSV_IMPORT_3.18.0.md)
- [Druck- und PDF-Ausgabe 3.17.0](archiv/41_DRUCK_UND_PDF_3.17.0.md)
- [Vollständiges App-Backup 3.16.0](archiv/40_APP_BACKUP_3.16.0.md)
- [Tagesplanung und Kapazität 3.15.0](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md)
- [Bearbeitungstag und Aufwand 3.14.0](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md)
- [Dokumentationsabgleich 13.09.2026](archiv/38_DOKUMENTATIONSABGLEICH_2026-09-13.md)
- [Tabellenansicht 3.13.0](archiv/36_TABELLENANSICHT_3.13.0.md)
- [Mein Tag – bewusste Tagesauswahl 3.12.0](archiv/35_MEIN_TAG_3.12.0.md)

- [Schnellerfassung und gespeicherte Filter 3.11.0](archiv/34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md)

- [Reiter und Pinnwand 3.10.0](archiv/33_REITER_UND_PINNWAND_3.10.0.md)

- [Oberfläche und Bedienung 3.9.0](archiv/32_UI_UND_BEDIENUNG_3.9.0.md)

- [Lokale Erinnerungen 3.8.0](archiv/31_ERINNERUNGEN_3.8.0.md)

- [Dokumentationsabgleich und Archivnachweis](archiv/30_DOKUMENTATIONSABGLEICH_2026-09-12.md)

- [Dynamische Ordner-/Listenkacheln](archiv/29_DYNAMISCHE_KACHELN_3.7.0.md)
- [Mac, vollständiger Vorlageneditor und Auftragsabgleich](archiv/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
- [Praxisanleitung für Vorlagen](27_VORLAGEN_PRAXISANLEITUNG.md)
- [Aktueller QA-Bericht](07_QA_BERICHT.md)
- [Ablageprüfung und Archivierung](archiv/28_ABLAGEPRUEFUNG_2026-09-11.md)

Die versionierten Verträge 31 bis 41 und die Nachträge 24 bis 30 bleiben als
fachliche Detailnachweise erhalten. Ihr jeweiliger Versionsstand ist bewusst
im Dateinamen erkennbar; die kumulativ aktuelle Beschreibung steht in den
3.21-Dokumenten oben und in der Funktionsübersicht.

## Aktuelle Dokumente

- [01_PRODUCT_CONSTRAINTS.md](<01_PRODUCT_CONSTRAINTS.md>)
- [02_ARCHITECTURE.md](<02_ARCHITECTURE.md>)
- [03_STARTKONTEXT.md](<03_STARTKONTEXT.md>)
- [05_QA_TESTPLAN.md](<05_QA_TESTPLAN.md>)
- [06_DATA_BACKUP_MIGRATION.md](<06_DATA_BACKUP_MIGRATION.md>)
- [07_QA_BERICHT.md](<07_QA_BERICHT.md>)
- [08_CODE_BEFUND.md](archiv/08_CODE_BEFUND.md)
- [09_PROJECT_HANDOFF.md](<09_PROJECT_HANDOFF.md>)
- [10_RELEASE_CHECKLIST.md](<10_RELEASE_CHECKLIST.md>)
- [11_BESTANDSANALYSE.md](archiv/11_BESTANDSANALYSE.md)
- [12_ABSCHLUSSBERICHT.md](archiv/12_ABSCHLUSSBERICHT.md)
- [24_VERSION_3.7.0.md](archiv/24_VERSION_3.7.0.md)
- [25_FEATURE_ABGLEICH_3.7.0.md](archiv/25_FEATURE_ABGLEICH_3.7.0.md)
- [26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md](archiv/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
- [27_VORLAGEN_PRAXISANLEITUNG.md](<27_VORLAGEN_PRAXISANLEITUNG.md>)
- [28_ABLAGEPRUEFUNG_2026-09-11.md](archiv/28_ABLAGEPRUEFUNG_2026-09-11.md)
- [29_DYNAMISCHE_KACHELN_3.7.0.md](archiv/29_DYNAMISCHE_KACHELN_3.7.0.md)
- [decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md](<decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md>)
- [decisions/PRODUCT_IDENTITY.md](<decisions/PRODUCT_IDENTITY.md>)
- [decisions/SYSTEMBENACHRICHTIGUNGEN.md](<decisions/SYSTEMBENACHRICHTIGUNGEN.md>)
- [decisions/ABHAENGIGKEIT_TKDND.md](<decisions/ABHAENGIGKEIT_TKDND.md>) – tkinterdnd2 für das Ziehen aus Finder und Explorer (27.09.2026)
- [34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md](archiv/34_SCHNELLERFASSUNG_UND_FILTER_3.11.0.md)
- [35_MEIN_TAG_3.12.0.md](archiv/35_MEIN_TAG_3.12.0.md)
- [36_TABELLENANSICHT_3.13.0.md](archiv/36_TABELLENANSICHT_3.13.0.md)
- [37_PLANUNG_UND_AUFWAND_3.14.0.md](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md)
- [38_DOKUMENTATIONSABGLEICH_2026-09-13.md](archiv/38_DOKUMENTATIONSABGLEICH_2026-09-13.md)
- [39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md)
- [40_APP_BACKUP_3.16.0.md](archiv/40_APP_BACKUP_3.16.0.md)
- [41_DRUCK_UND_PDF_3.17.0.md](archiv/41_DRUCK_UND_PDF_3.17.0.md)
- [42_CSV_IMPORT_3.18.0.md](archiv/42_CSV_IMPORT_3.18.0.md)
- [43_AENDERUNGSVERLAUF_3.19.0.md](archiv/43_AENDERUNGSVERLAUF_3.19.0.md)
- [44_KALENDERAUSGABE_3.20.0.md](archiv/44_KALENDERAUSGABE_3.20.0.md)
- [45_KALENDERIMPORT_3.21.0.md](<45_KALENDERIMPORT_3.21.0.md>)
- [55_NAVIGATION_UND_PINNWAND_3.24.0.md](<55_NAVIGATION_UND_PINNWAND_3.24.0.md>)
- [56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md](<56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md>)
- [57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md](<57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md>)
- [58_STARTSEITE_UND_BEGLEITER_3.25.0.md](<58_STARTSEITE_UND_BEGLEITER_3.25.0.md>)
- [59_TAGEBUCH_UND_UI_3.28.0.md](<59_TAGEBUCH_UND_UI_3.28.0.md>)
- [60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md](<60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md>)
- [61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md](<61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md>)
- [65_ZEICHNUNGSSEITE_3.29.0.md](<65_ZEICHNUNGSSEITE_3.29.0.md>)
- [66_MODERNISIERUNG_3.30.0.md](<66_MODERNISIERUNG_3.30.0.md>)
- [67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md](<67_SITZUNGSPROTOKOLL_2026-09-24_BIS_2026-09-26.md>)

## Archivierung zum Übergang auf 3.28.0

- [Changelog 3.28.0 vor Flackerkorrektur](<archiv/CHANGELOG_3.28.0_vor_Flackerkorrektur_2026-09-23.md>)

## Archiv vor Tabellenansicht 3.13.0

- [archiv/CHANGELOG_3.12.0_vor_3.13.0.md](<archiv/CHANGELOG_3.12.0_vor_3.13.0.md>)

## Archiv vor Mein Tag 3.12.0

- [archiv/CHANGELOG_3.11.0_vor_3.12.0.md](<archiv/CHANGELOG_3.11.0_vor_3.12.0.md>)

## Historische Ausführungspläne

Die folgenden Dokumente beschreiben frühere Entscheidungen und Prüfstände.

- [exec-plans/2.10.0-label-chips-und-codepflege.md](<archiv/exec-plans/2.10.0-label-chips-und-codepflege.md>)
- [exec-plans/2.11.0-datenintegritaet-und-eingabemaske.md](<archiv/exec-plans/2.11.0-datenintegritaet-und-eingabemaske.md>)
- [exec-plans/2.12.0-oberflaeche-verdichten.md](<archiv/exec-plans/2.12.0-oberflaeche-verdichten.md>)
- [exec-plans/2.5.1-stabilisierung.md](<archiv/exec-plans/2.5.1-stabilisierung.md>)
- [exec-plans/2.5.2-qol-stabilisierung.md](<archiv/exec-plans/2.5.2-qol-stabilisierung.md>)
- [exec-plans/2.5.3-ui-und-struktur-stabilisierung.md](<archiv/exec-plans/2.5.3-ui-und-struktur-stabilisierung.md>)
- [exec-plans/2.5.4-uebersichten-und-ui-stabilisierung.md](<archiv/exec-plans/2.5.4-uebersichten-und-ui-stabilisierung.md>)
- [exec-plans/2.5.5-fehlerbehebung-und-macos.md](<archiv/exec-plans/2.5.5-fehlerbehebung-und-macos.md>)
- [exec-plans/2.6.0-gruppen-und-kontextmenues.md](<archiv/exec-plans/2.6.0-gruppen-und-kontextmenues.md>)
- [exec-plans/2.7.0-papierkorb-labels-kalender.md](<archiv/exec-plans/2.7.0-papierkorb-labels-kalender.md>)
- [exec-plans/2.7.1-ui-feinschliff.md](<archiv/exec-plans/2.7.1-ui-feinschliff.md>)
- [exec-plans/2.7.2-fokus-und-kalenderinteraktion.md](<archiv/exec-plans/2.7.2-fokus-und-kalenderinteraktion.md>)
- [exec-plans/2.8.0-arten-verspaetet-und-hover.md](<archiv/exec-plans/2.8.0-arten-verspaetet-und-hover.md>)
- [exec-plans/2.9.0-verschachtelte-ordner.md](<archiv/exec-plans/2.9.0-verschachtelte-ordner.md>)
- [exec-plans/3.0.0-oberflaeche-und-symbole.md](<archiv/exec-plans/3.0.0-oberflaeche-und-symbole.md>)

## Archiv – unveränderte Vorgänger


- [archiv/CHANGELOG_3.10.0_vor_3.11.0.md](<archiv/CHANGELOG_3.10.0_vor_3.11.0.md>)


- [archiv/02_ARCHITECTURE_3.2.0.md](<archiv/02_ARCHITECTURE_3.2.0.md>)
- [archiv/07_QA_BERICHT_2.11.0.md](<archiv/07_QA_BERICHT_2.11.0.md>)
- [archiv/07_QA_BERICHT_3.2.0.md](<archiv/07_QA_BERICHT_3.2.0.md>)
- [archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md](<archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md>)
- [archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE_3.2.0_abgeschlossen.md](<archiv/09_ARBEITSAUFTRAG_BESTANDSANALYSE_3.2.0_abgeschlossen.md>)
- [archiv/09_PROJECT_HANDOFF_3.2.0.md](<archiv/09_PROJECT_HANDOFF_3.2.0.md>)
- [archiv/09_STARTKONTEXT.md](<archiv/09_STARTKONTEXT.md>)
- [archiv/09_STARTKONTEXT_3.2.0.md](<archiv/09_STARTKONTEXT_3.2.0.md>)
- [archiv/10_RELEASE_CHECKLIST_2.11.0.md](<archiv/10_RELEASE_CHECKLIST_2.11.0.md>)
- [archiv/13_OBERFLAECHE_3.4.0_vor_Nachbesserung_2026-09-11.md](<archiv/13_OBERFLAECHE_3.4.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/14_OBERFLAECHE_NACHTRAG_3.4.0_vor_Nachbesserung_2026-09-11.md](<archiv/14_OBERFLAECHE_NACHTRAG_3.4.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/15_WIEDERHOLUNGEN_3.5.0_vor_Nachbesserung_2026-09-11.md](<archiv/15_WIEDERHOLUNGEN_3.5.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/16_UEBERGABE_3.5.0_3.5.0_vor_windowspruefung.md](<archiv/16_UEBERGABE_3.5.0_3.5.0_vor_windowspruefung.md>)
- [archiv/16_UEBERGABE_3.5.0_vor_Nachbesserung_2026-09-11.md](<archiv/16_UEBERGABE_3.5.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/17_UEBERGABE_3.6.0_3.6.0_vor_Kacheluebersicht.md](<archiv/17_UEBERGABE_3.6.0_3.6.0_vor_Kacheluebersicht.md>)
- [archiv/17_UEBERGABE_3.6.0_3.6.0_vor_UI-Nachbesserung.md](<archiv/17_UEBERGABE_3.6.0_3.6.0_vor_UI-Nachbesserung.md>)
- [archiv/17_UEBERGABE_3.6.0_vor_3.6_Abschluss_2026-09-06.md](<archiv/17_UEBERGABE_3.6.0_vor_3.6_Abschluss_2026-09-06.md>)
- [archiv/17_UEBERGABE_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/17_UEBERGABE_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/18_QA_3.6.0_3.6.0_vor_Kacheluebersicht.md](<archiv/18_QA_3.6.0_3.6.0_vor_Kacheluebersicht.md>)
- [archiv/18_QA_3.6.0_3.6.0_vor_UI-Nachbesserung.md](<archiv/18_QA_3.6.0_3.6.0_vor_UI-Nachbesserung.md>)
- [archiv/18_QA_3.6.0_vor_3.6_Abschluss_2026-09-06.md](<archiv/18_QA_3.6.0_vor_3.6_Abschluss_2026-09-06.md>)
- [archiv/18_QA_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/18_QA_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/19_GLASS_SURFACE_3.6.0_vor_3.6_Abschluss_2026-09-06.md](<archiv/19_GLASS_SURFACE_3.6.0_vor_3.6_Abschluss_2026-09-06.md>)
- [archiv/19_GLASS_SURFACE_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/19_GLASS_SURFACE_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/20_FEATURE_ABGLEICH_3.6.0_3.6.0_vor_UI-Nachbesserung.md](<archiv/20_FEATURE_ABGLEICH_3.6.0_3.6.0_vor_UI-Nachbesserung.md>)
- [archiv/20_FEATURE_ABGLEICH_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/20_FEATURE_ABGLEICH_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/21_LEISTUNGSBERICHT_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/21_LEISTUNGSBERICHT_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/22_UI_NACHBESSERUNG_3.6.0_3.6.0_vor_Kacheluebersicht.md](<archiv/22_UI_NACHBESSERUNG_3.6.0_3.6.0_vor_Kacheluebersicht.md>)
- [archiv/22_UI_NACHBESSERUNG_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/22_UI_NACHBESSERUNG_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0_vor_Nachbesserung_2026-09-11.md](<archiv/23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0_vor_Nachbesserung_2026-09-11.md>)
- [archiv/PRODUCT_IDENTITY_2.11.0.md](<archiv/PRODUCT_IDENTITY_2.11.0.md>)
- [archiv/README.md](<archiv/README.md>)
- [decisions/archiv/README.md](<decisions/archiv/README.md>)

## Archiv vor Erinnerungen 3.8.0


## Oberfläche 3.9.0 und gesicherte Vorgänger

- [32_UI_UND_BEDIENUNG_3.9.0](archiv/32_UI_UND_BEDIENUNG_3.9.0.md)


## Archiv vor 3.10.0

- [archiv/32_REITERANSICHT_Entwurf_3.9.0_vor_3.10.0.md](<archiv/32_REITERANSICHT_Entwurf_3.9.0_vor_3.10.0.md>)

## Ergänzte Archivnachweise 3.13 vor 3.14


## Ergänzte Archivnachweise Dokumentationsabgleich 2026-09-13


## Ergänzte Archivnachweise 3.14 vor 3.15


## Ergänzte Archivnachweise 3.15 vor 3.16


## Ergänzte Archivnachweise 3.16 vor 3.17


## Ergänzte Archivnachweise 3.17 vor 3.18

- [CHANGELOG_3.17.0_vor_3.18.0](archiv/CHANGELOG_3.17.0_vor_3.18.0.md)

## Ergänzte Archivnachweise 3.18 vor 3.19

- [CHANGELOG_3.18.0_vor_3.19.0](archiv/CHANGELOG_3.18.0_vor_3.19.0.md)

## Ergänzte Archivnachweise 3.19 vor 3.20

- [CHANGELOG_3.19.0_vor_3.20.0](archiv/CHANGELOG_3.19.0_vor_3.20.0.md)

## Ergänzte Archivnachweise 3.20 vor 3.21

- [CHANGELOG_3.20.0_vor_3.21.0](archiv/CHANGELOG_3.20.0_vor_3.21.0.md)

## Ergänzte Archivnachweise 3.21.2 vor 3.21.3

- [archiv/32_REITERANSICHT_3.21.2_vor_3.21.3.md](<archiv/32_REITERANSICHT_3.21.2_vor_3.21.3.md>)

## Ergänzte Archivnachweise 3.21.3 vor 3.21.4


## Archivnachweise der Abschlussprüfung am 15.09.2026


## Archivnachweise zu 3.25.0


## Archivnachweise zu 3.24.0


## Archivnachweise zu 3.23.0


## Archivnachweise zu 3.22.0


## Archivnachweis zur Zeitzonenprüfung am 18.09.2026


## Nachbesserung 3.26 und neue Archive

- [Verbindliche Dokumentenpflege](DOKUMENTENPFLEGE.md)
- [Entscheidungen_3.26.0](75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md)
- [DEV_NOTES](DEV_NOTES.md)
















- [32_REITERANSICHT_3.26.0_vor_Archivverweisen](archiv/32_REITERANSICHT_3.26.0_vor_Archivverweisen.md)








- [LIZENZENTWURF_3.26.0](decisions/LIZENZENTWURF_3.26.0.md)

- [SIGNIERUNG_3.26.0](decisions/SIGNIERUNG_3.26.0.md)

- [VERTRIEB_UND_MARKE_3.26.0](decisions/VERTRIEB_UND_MARKE_3.26.0.md)







## Archivnachweis zur Erweiterung der Zeichenflächenprobe am 24.09.2026


## Archivnachweis zum Nachzeichner am 24.09.2026


## Archivnachweis zur Zeichenflächen-Übergabe am 24.09.2026

## Archivnachweis zur Archiv- und Dokumentationsprüfung am 24.09.2026

- [Zeichenflächen-Übergabe vor Archivprüfung](archiv/62_ZEICHENFLAECHE_WEITERGABE_3.28.0_vor_Archivpruefung_2026-09-24.md)



## Archivnachweis zur GitHub-README- und Existenzprüfung am 24.09.2026

- [Changelog vor Existenzprüfung](archiv/CHANGELOG_3.28.0_vor_GitHub-README_und_Existenzpruefung_2026-09-24.md)
- [Zeichenflächen-Weitergabe vor Existenzprüfung](archiv/62_ZEICHENFLAECHE_WEITERGABE_3.28.0_vor_Existenzpruefung_2026-09-24.md)
- [Archivprüfung vor Existenzprüfung](archiv/63_ARCHIV_UND_DOKUMENTATIONSPRUEFUNG_3.28.0_vor_Existenzpruefung_2026-09-24.md)
- [Historischer Reiterentwurf aus aktivem Bestand](archiv/32_REITERANSICHT_3.10.0_aus_aktivem_Bestand_2026-09-24.md)
- [Dokumentenpflege-Wegweiser aus aktivem Bestand](decisions/archiv/DOKUMENTENPFLEGE_Wegweiser_2026-09-24.md)

## Archivnachweise zum Übergang auf 3.29.0 am 24.09.2026

Vor der Fortschreibung auf Glide 3.29.0 und Aufgabenformat 19 gesicherte
Fassungen:

- [Changelog vor 3.29.0](archiv/CHANGELOG_3.28.0_vor_3.29.0.md)

## Archivnachweise zur Abnahmeprüfung 3.29.0 am 24.09.2026

- [Changelog vor Abnahmeprüfung](archiv/CHANGELOG_3.29.0_vor_Abnahmepruefung_2026-09-24.md)

## Archivnachweise zum Modernisierungskatalog am 25.09.2026

- [Changelog vor Modernisierungskatalog](archiv/CHANGELOG_3.29.0_vor_Modernisierungskatalog_2026-09-25.md)

## Archivnachweise zum Übergang auf 3.30.0 am 25.09.2026

Vor der Fortschreibung auf Glide 3.30.0 und Aufgabenformat 20 gesicherte
Fassungen:

- [Changelog vor 3.30.0](archiv/CHANGELOG_3.29.0_vor_3.30.0.md)

## Archivnachweise zum Ausbau 3.30.0 am 25.09.2026

Vor dem Ausbau (Zeitblöcke ziehen, Folien als PDF, Karten-Rückgängig,
vollständiger Detailbereich, Gismo in Leerzuständen, Pixelschrift,
Schutz vor dem Überschreiben unlesbarer Bestände) gesicherte Fassungen:

- [Changelog vor dem Ausbau](archiv/CHANGELOG_3.30.0_vor_Ausbau_2026-09-25.md)

## Archivnachweise zum Dokumentabgleich am 26.09.2026

Abgelöste Berichte vom 24.09.2026, ins Archiv verschoben:

- [Zeichenflächen-Weitergabe 24.09.2026](archiv/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md) – ersetzt durch Projektübergabe, Vertrag 66 und Sitzungsprotokoll 67
- [Archiv- und Dokumentationsprüfung 24.09.2026](archiv/63_ARCHIV_UND_DOKUMENTATIONSPRUEFUNG_2026-09-24.md)
- [Dokumenten-Existenzprüfung 24.09.2026](archiv/64_DOKUMENTEN_EXISTENZPRUEFUNG_2026-09-24.md)

Vor dem Abgleich gesicherte Fassungen:

- [Zeichenflächenkern vor dem Dokumentabgleich](archiv/61_ZEICHENFLAECHE_ISOLIERTER_KERN_3.30.0_vor_Dokumentabgleich_2026-09-26.md)

## Archivnachweise zum zweiten Ausbau 3.30.0 am 26.09.2026

Vor dem zweiten Ausbau gesicherte Fassungen, darin Anhänge im Detailbereich,
Zeichnungen in Folien, Stundenraster, Gruppierung mit Überschriften,
Lasttest, Windows-Prüfpaket und Produktdatenblatt-Entwurf:

- [Sitzungsprotokoll vor dem zweiten Ausbau](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Ausbau2_2026-09-26.md)
- [Changelog vor dem zweiten Ausbau](archiv/CHANGELOG_3.30.0_vor_Ausbau2_2026-09-26.md)
- Außerhalb von `docs`, jeweils im `Archiv`-Unterordner des Ordners:
  - mit der Endung `_3.30.0_vor_Ausbau2_2026-09-26`: die READMEs der
    Arbeitsablage, der Arbeitsvorbereitung und der Python-Versionen, das
    AV-Sitzungsprotokoll und die Prüfliste 3.30;
  - das Store-README mit `_3.30.0_vor_Produktdatenblatt_2026-09-26`;
  - der Test `test_ui_followup36` vor der Lasttest-Korrektur unter
    `tests/integration/archiv`.

## Archivnachweise zum dritten Ausbau 3.30.0 am 26.09.2026

Vor dem dritten Ausbau gesicherte Fassungen. Der Ausbau umfasst:

- Ziehen aus der Liste ins Stundenraster;
- die gruppierte Tabelle mit Nummern und Überschriften;
- die Pixelschrift unter Linux.

Archivkopien in `docs`:

- [Sitzungsprotokoll vor dem dritten Ausbau](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Ausbau3_2026-09-26.md)
- [Changelog vor dem dritten Ausbau](archiv/CHANGELOG_3.30.0_vor_Ausbau3_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im `Archiv`-Unterordner, mit
der Endung `_3.30.0_vor_Ausbau3_2026-09-26`:

- die READMEs der Arbeitsablage, der Arbeitsvorbereitung und der
  Python-Versionen;
- das AV-Sitzungsprotokoll;
- die Prüfliste 3.30 (`_vor_Ausbau3_2026-09-26`).

Die startbare Fassung vor dem dritten Ausbau liegt unter
`07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau3_2026-09-26`.

## Archivnachweise zur Mindestgröße 3.30.0 am 26.09.2026

Vor der Überarbeitung für kleine Fenster gesicherte Fassungen. Die
Überarbeitung umfasst:

- Höhenstufen;
- ganze Chips und gekürzte Unterzeilen;
- Tabellenspalten nach Priorität;
- die sortierte gruppierte Tabelle mit Überschriften;
- die Suite `test_mindestgroesse330`.

Archivkopien in `docs`:

- [Sitzungsprotokoll vor der Mindestgröße](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Mindestgroesse_2026-09-26.md)
- [Changelog vor der Mindestgröße](archiv/CHANGELOG_3.30.0_vor_Mindestgroesse_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im `Archiv`-Unterordner, mit
der Endung `_3.30.0_vor_Mindestgroesse_2026-09-26`:

- die READMEs der Arbeitsablage, der Arbeitsvorbereitung und der
  Python-Versionen;
- das AV-Sitzungsprotokoll;
- die Prüfliste 3.30 (`_vor_Mindestgroesse_2026-09-26`).

Außerdem gesichert:

- `tests/tools/archiv/pruefen_3.30.0_vor_Mindestgroesse_2026-09-26.py`;
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Mindestgroesse_2026-09-26`.

## Archivnachweise zu Dialogen, Kontrast, Raster und Paketierung am 26.09.2026

Vor dieser Runde gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Kontrast_und_Paketierung_2026-09-26.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Kontrast_und_Paketierung_2026-09-26.md)

Außerhalb von `docs` mit derselben Endung:

- das Paketierungs-README (`packaging/archiv`);
- die READMEs der Arbeitsablage, der Arbeitsvorbereitung, der
  Python-Versionen und der Release-Exporte;
- das AV-Sitzungsprotokoll;
- die Prüflisten 3.30 und Windows;
- `tests/tools/archiv/pruefen_3.30.0_vor_Kontrast_und_Paketierung_2026-09-26.py`;
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Kontrast_und_Paketierung_2026-09-26`.

## Archivnachweise zur Dokumentprüfung am 26.09.2026

Prüfung aller aktuellen Dokumente der Ablage auf Vollständigkeit, Aktualität
und Referenzen.

- **Links und Stand:** 81 Markdown-Dateien ohne tote Links; alle
  Standangaben auf 3.30.0.
- **Inhaltlich fortgeschrieben** (vorher gesichert, Endung `_3.30.0_vor_Dokumentpruefung_2026-09-26`):
    „keine Zeiterfassung, kein Wochentagsprofil“ berichtigt
    die Kontrastfortschreibung
- **Außerhalb von `docs`, jeweils im benachbarten Archivordner:**
  - die READMEs von `tests`, `tests/tools`, `src/glide` und Repository;
  - die READMEs von Grafik-Master, Fehlerprotokollen,
    Arbeitsvorbereitung, Dokumentation und Ablage-Wurzel;
  - Aufgabenkatalog und AV-Sitzungsauswertung.
- **Archiviert, weil abgelöst:**
  - `00_Arbeitsvorbereitung/Checklisten/Glide_Veroeffentlichung_Checkliste.txt`
    (Stand 3.14.0) nach
    `Checklisten/Archiv/Glide_Veroeffentlichung_Checkliste_3.14.0_abgeloest_2026-09-26.txt`.
    Ersetzt durch die [Releasecheckliste](10_RELEASE_CHECKLIST.md) und die
    Releaseplanung in `05_Probelisten_Testdaten`.
  - `00_Arbeitsvorbereitung/Umsetzung_3.28.0/` (Archivierungsmanifeste
    von 3.28) nach `00_Arbeitsvorbereitung/Archiv/Umsetzung_3.28.0/`.
- **Entfernt:** verwaiste Bytecode-Dateien der Versionen 3.6, 3.7 und 3.29
  in `07_Python-Versionen/__pycache__`, reiner Zwischenspeicher ohne
  zugehörige Quelle.

## Archivnachweise zu den Hintergrundverläufen am 26.09.2026

Vor dem Einbau der Hintergrundverläufe (Vertrag 66, Abschnitt 2.8)
gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Hintergrund_2026-09-26.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Hintergrund_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `src/glide`, `packaging`, Repository,
  Ablage-Wurzel, Arbeitsvorbereitung und Python-Versionen;
- das AV-Sitzungsprotokoll und die Prüfliste 3.30;
- `pruefen.py`;
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Hintergrund_2026-09-26`.

## Archivnachweise zur Rückmeldung am 26.09.2026

Vor den Änderungen aus der Rückmeldung zu den Hintergrundverläufen (Vertrag
66, Abschnitte 2.8 und 2.9) gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Rueckmeldung_2026-09-26.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Rueckmeldung_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, Repository, Ablage-Wurzel und Python-Versionen;
- das AV-Sitzungsprotokoll und die Prüfliste 3.30;
- `pruefen.py`;
- die startbare Fassung (Hintergrundverläufe samt Absturzkorrektur) unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Rueckmeldung_2026-09-26`.

## Archivnachweise zur zweiten Rückmeldung am 26.09.2026

Vor den Änderungen aus der zweiten Rückmeldung (Vertrag 66, Abschnitt 2.10)
gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Rueckmeldung2_2026-09-26.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Rueckmeldung2_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `src/glide`, `packaging`, Repository,
  Ablage-Wurzel, Arbeitsvorbereitung und Python-Versionen;
- das AV-Sitzungsprotokoll und die Prüfliste 3.30;
- `pruefen.py` und `packaging/macos/baue_app.py` (dort mit Endung
  `_3.30.0_vor_Schnellstart_2026-09-26`);
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Rueckmeldung2_2026-09-26`.

## Archivnachweise zu Tk 9, Bildern in Seiten und festen Bestandteilen am 27.09.2026

Vor Abschnitt 2.14 des Vertrags 66 gesicherte Fassungen. Archivkopien in
`docs`:

- [Changelog](archiv/CHANGELOG_3.30.0_vor_Tk9_und_Bildern_2026-09-27.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von Repository, `src/glide`, `tests`, `packaging`,
  Ablage-Wurzel, Arbeitsvorbereitung, Fehlerprotokollen, Probelisten,
  Python-Versionen, Dokumentation, Grafik und Store-Material;
- `SECURITY.md`, `tests/qa-verlauf.md` und `pruefen.py`;
- die Prüfliste 3.30, das Seitenkonzept und die Entscheidungsvorlage vom
  27.09.2026;
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Tk9_und_Bildern_2026-09-27`.

## Archivnachweise zur Kompression am 27.09.2026

Vor der Kompression, der Bibliothekstabelle und dem Notizbuch (Vertrag 66,
Abschnitt 2.13) gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Kompression_2026-09-27.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Kompression_2026-09-27.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `src/glide`, Repository, Ablage-Wurzel,
  Arbeitsvorbereitung und Python-Versionen;
- das AV-Sitzungsprotokoll, die Prüfliste 3.30 und das Seitenkonzept;
- das Produktdatenblatt (`40_Store_Material/Archiv`) und das README der
  Probelisten (`05_Probelisten_Testdaten/Archiv`);
- `pruefen.py` (Stand ohne `test_kompression330`);
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Kompression_2026-09-27`.

## Archivnachweise zu Aufräumen, Seitenbereich und Galerie am 27.09.2026

Vor dem Aufräumen, dem Seitenbereich und der Galerie (Vertrag 66, Abschnitt
2.12) gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Aufraeumen_2026-09-27.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Aufraeumen_2026-09-27.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `src/glide`, `packaging`, Repository,
  Ablage-Wurzel, Arbeitsvorbereitung und Python-Versionen;
- das AV-Sitzungsprotokoll, die Prüfliste 3.30 und das Seitenkonzept;
- `pruefen.py` (Stand ohne `test_aufraeumen330`);
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Aufraeumen_2026-09-27`.

## Archivnachweise zu Seiten und Ordnertypen am 26.09.2026

Vor der Seitenart „Seite“ und den Ordnertypen (Vertrag 66, Abschnitt 2.11)
gesicherte Fassungen. Archivkopien in `docs`:

- [Sitzungsprotokoll](archiv/67_SITZUNGSPROTOKOLL_3.30.0_vor_Seiten_2026-09-26.md)
- [Changelog](archiv/CHANGELOG_3.30.0_vor_Seiten_2026-09-26.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `src/glide`, `packaging`, Repository,
  Ablage-Wurzel, Arbeitsvorbereitung und Python-Versionen;
- das AV-Sitzungsprotokoll und die Prüfliste 3.30;
- `pruefen.py` und `baue_app.py`;
- der Konzeptentwurf vor der Entscheidung;
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Seiten_2026-09-26`.

## Archivnachweise zu Logo, Sicherungen und Notizbereich am 29.09.2026

Vor Logo, Lupe, Kartenfuß, Sicherungen, Startprüfung und Notizbereich
(Vertrag 66, Abschnitte 2.15 und 2.16) gesicherte Fassungen. Archivkopien in
`docs`:

- [Changelog](archiv/CHANGELOG_3.30.0_vor_Logo_und_Sicherungen_2026-09-29.md)

Außerhalb von `docs` liegen die Kopien jeweils im benachbarten Archivordner,
mit derselben Endung:

- die READMEs von `tests`, `tests/tools`, `src/glide`, `packaging`,
  Repository, Ablage-Wurzel, Arbeitsvorbereitung, Probelisten,
  Store-Material und Python-Versionen; das README des Grafik-Masters endet
  auf `_vor_Logo_2026-09-29`;
- `AGENTS.md`, `qa-verlauf.md`, `pruefen.py` und `app.pyw`;
- Aufgabenkatalog, Aufgabensammlung, Seitenkonzept, Sitzungsprotokoll und
  Produktdatenblatt;
- die Prüfung vom 28.09.2026 vor den Antworten (`…_vor_Antworten.md`);
- die Prüflisten 3.28, 3.29 und 3.30 sowie die Windows-Prüfung vor der
  Verdichtung (`…_vor_Verdichtung_2026-09-29.md`);
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Logo_und_Sicherungen_2026-09-29`.

Zum Löschen durch den Inhaber markiert (Endung `_Z`, 29.09.2026): Ordner, die
nur noch ein Archiv und ein README enthielten, dazu `__pycache___Z` in
`07_Python-Versionen` und die abgelösten Prüflisten 3.28 und 3.29. Die Liste
steht in der
[Übersicht vom 29.09.2026](../../../00_Arbeitsvorbereitung/Glide_Uebersicht_und_Entscheidungen_2026-09-29.md).

## Archivnachweise zur Rückmeldung vom Abend am 29.09.2026

Vor den Änderungen R1–R11 (Vertrag 66, Abschnitt 2.17) gesicherte
Fassungen. Archivkopien in `docs`:

- [Changelog](archiv/CHANGELOG_3.30.0_vor_Rueckmeldung_Abend_2026-09-29.md)

Außerhalb von `docs`, mit derselben Endung:

- `tests/archiv/README_…` und `tests/archiv/qa-verlauf_…`;
- `tests/tools/archiv/pruefen_…`;
- `src/glide/archiv/app_3.30.0_vor_Rueckmeldung_Abend_2026-09-29.pyw`;
- in der Arbeitsvorbereitung das README und die Entscheidungsvorlage vor den
  Antworten (`Archiv/Glide_Rueckmeldung_und_Entscheidungen_2026-09-29_vor_Antworten.md`);
- die manuelle Prüfliste 3.30 (`Checklisten/Archiv/Manuelle_Pruefung_3.30.0_vor_Rueckmeldung_Abend_2026-09-29.md`);
- `src/glide/archiv/…`: Stand vor den Änderungen; die Architektur liegt als echte Kopie vor.
- die startbare Fassung unter
  `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Rueckmeldung_Abend_2026-09-29`.

Die Archivkopien von Changelog, Vertrag 66, Index, Testplan, Übergabe,
Entwicklungsnotizen, Test-README, README der Arbeitsvorbereitung und
`pruefen.py` sind aus dem heutigen Stand zurückgerechnet (die Ergänzungen vom Abend entfernt), weil sie erst
nach den Änderungen angelegt wurden.

## Archivnachweise zum Versionswechsel auf 3.31.0 am 30.09.2026

Vor dem Anheben auf 3.31.0 gesicherte Fassungen. Archivkopien in `docs`:

- [CHANGELOG](archiv/CHANGELOG_3.30.0_vor_3.31.0.md)

Außerhalb von `docs` liegen die Kopien mit derselben Endung im jeweils
benachbarten Archivordner: alle READMEs mit Standangabe, `qa-verlauf.md`,
die Beispieldaten und der Rundgang (`tests/fixtures/beispiele/archiv`) sowie
die startbare Fassung 3.30.0 in `07_Python-Versionen/Archiv`.

## Archivnachweise zum Versionswechsel auf 3.32.0 am 30.09.2026

Vor Etappe 1 der Funktionsrecherche gesicherte Fassungen. Archivkopien in `docs`:

- [CHANGELOG](archiv/CHANGELOG_3.31.0_vor_3.32.0.md)

Außerhalb von `docs` mit derselben Endung: READMEs mit Standangabe, `qa-verlauf.md`,
`pruefen.py`, Beispieldaten, Rundgang, Vorlagenkatalog und die startbare
Fassung 3.31.0 in `07_Python-Versionen/Archiv`.

## Archivnachweise zur Behebung des Hängers am 30.09.2026

- [Changelog vor der Bildseitenbehebung](archiv/CHANGELOG_3.32.0_vor_Bildseitenbehebung_2026-09-30.md)

## Archivnachweise zur Sitzungsübergabe am 30.09.2026


Außerhalb von `docs` mit derselben Endung: `AGENTS.md`, README der Arbeitsvorbereitung.
Der vollständige Stand 3.31.0 liegt seit 30.09.2026 unter
`07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.31.0_Endstand_2026-09-30`
und als `src/glide/archiv/app_3.31.0_vor_3.32.0.pyw` und `drawing_3.31.0_vor_3.32.0.py`.

## Archivnachweise zur Vollständigkeitsprüfung am 30.09.2026

- [Changelog vor der Nachprüfung der Weitergabe](archiv/CHANGELOG_3.32.0_vor_Nachpruefung_2026-09-30.md)

## Archivnachweise zur Arbeits- und Featureplanung vom 30.09.2026

- [Changelog vor dem Dokumentationsnachtrag](../archiv/CHANGELOG_3.32.0_vor_Arbeits_Featureplanung_2026-09-30.md)
- [Arbeitsvorbereitungs-README vorher](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [Sitzungsübergabe vorher](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [Funktionsrecherche vorher, Ausgangsstand 3.31](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md)

## Klappkontrolle und Inhaberantworten – 3.32.1

- [69 – Klappkontrolle, Änderungsvertrag und Kontrollmatrix](69_KLAPPKONTROLLE_3.32.1.md)
- [Pflichtsuite](../tests/integration/test_klappmechanismen3321.py)
- [Arbeitsplanung mit Antworten D01–D06, Erklärung D07 und Korrektur D08](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)

Archivkopien vor Versionswechsel und Entscheidungs-/Klappkontrolle:
- [CHANGELOG_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30](../archiv/CHANGELOG_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30.md)
- [README_3.32.0_vor_3.32.1](../archiv/README.md)
- [README_3.32.0_vor_3.32.1](../tests/README.md)
- [qa-verlauf_3.32.0_vor_3.32.1](../tests/archiv/qa-verlauf_3.32.0_vor_3.32.1.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Funktionsrecherche_Ausbau_2026-09-30_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.0_vor_3.32.1](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [README_3.32.0_vor_3.32.1](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Funktionsrecherche_Ausbau_2026-09-30_3.32.0_vor_Entscheidungen_Klappkontrolle_2026-09-30](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.0_vor_3.32.1](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [README_3.32.0_vor_3.32.1](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [Startanleitung vor Versions-/Linkkorrektur](../../../07_Python-Versionen/Archiv/README.md)

## Drag und Performance 3.32.2

- [Drag-and-drop und Performance 3.32.2](70_DRAG_UND_PERFORMANCE_3.32.2.md)
- [Neue Bedien-/Performance-Pflichtsuite](../tests/integration/test_drag_performance3322.py)
- [Unprofilierter Messvergleich](../scripts/pflege/messung_performance.py)

## Archiv vor 3.32.2

- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Funktionsrecherche_Ausbau_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [README_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Funktionsrecherche_Ausbau_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [README_3.32.1_vor_3.32.2.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [README_3.32.1_vor_3.32.2.md](../scripts/pflege/archiv/README_3.32.1_vor_3.32.2.md)
- [README_3.32.1_vor_3.32.2.md](../scripts/pflege/archiv/README_3.32.1_vor_3.32.2.md)
- [README_3.32.1_vor_3.32.2.md](../tests/README.md)
- [qa-verlauf_3.32.1_vor_3.32.2.md](../tests/archiv/qa-verlauf_3.32.1_vor_3.32.2.md)
- [README_3.32.1_vor_3.32.2.md](../tests/README.md)
- [qa-verlauf_3.32.1_vor_3.32.2.md](../tests/archiv/qa-verlauf_3.32.1_vor_3.32.2.md)
- [CHANGELOG_3.32.1_vor_3.32.2.md](../archiv/CHANGELOG_3.32.1_vor_3.32.2.md)
- [README_3.32.1_vor_3.32.2.md](../archiv/README.md)
- [CHANGELOG_3.32.1_vor_3.32.2.md](../archiv/CHANGELOG_3.32.1_vor_3.32.2.md)
- [README_3.32.1_vor_3.32.2.md](../archiv/README.md)
- [README_3.32.1_vor_3.32.2.md](../../../07_Python-Versionen/Archiv/README.md)
- [README_3.32.1_vor_3.32.2.md](../../../07_Python-Versionen/Archiv/README.md)


### Abschlussarchive 3.32.2 vom 30.09.2026

- [qa-verlauf_3.32.2_vor_Abschluss_2026-09-30.md](../tests/archiv/qa-verlauf_3.32.2_vor_Abschluss_2026-09-30.md)
- [README_3.32.2_vor_Abschluss_2026-09-30.md](../../../07_Python-Versionen/Archiv/README.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.2_vor_Abschluss_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.2_vor_Abschluss_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)

### Archive vor Richtungsauswahl 30.09.2026

- [README_3.32.2_vor_Aufgabenauswahl_2026-09-30.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.2_vor_Aufgabenauswahl_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.2_vor_Aufgabenauswahl_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)

## Bibliothekskarten 3.32.3

- [Bibliothekskarten, gemeinsame Aktionsleiste, Lebensdauer und Messung](71_KARTEN_PERFORMANCE_3.32.3.md)

## Vorfassungen vor Bibliotheks-Performance 3.32.3

- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.2_vor_Karten_Performance_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30_3.32.2_vor_Karten_Performance_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.2_vor_3.32.3.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.2_vor_Karten_Performance_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [README_3.32.2_vor_3.32.3.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [README_3.32.2_vor_Karten_Performance_2026-10-01.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [CHANGELOG_3.32.2_vor_Karten_Performance_2026-10-01.md](../archiv/CHANGELOG_3.32.2_vor_Karten_Performance_2026-10-01.md)
- [README_3.32.2_vor_3.32.3.md](../archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../assets/README.md)
- [README_3.32.2_vor_3.32.3.md](../packaging/README.md)
- [README_3.32.2_vor_3.32.3.md](../scripts/pflege/archiv/README_3.32.2_vor_3.32.3.md)
- [README_3.32.2_vor_Karten_Performance_2026-10-01.md](../scripts/pflege/archiv/README_3.32.2_vor_Karten_Performance_2026-10-01.md)
- [README_3.32.2_vor_3.32.3.md](../src/glide/archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../tests/README.md)
- [qa-verlauf_3.32.2_vor_3.32.3.md](../tests/archiv/qa-verlauf_3.32.2_vor_3.32.3.md)
- [qa-verlauf_3.32.2_vor_Karten_Performance_2026-10-01.md](../tests/archiv/qa-verlauf_3.32.2_vor_Karten_Performance_2026-10-01.md)
- [README_3.32.2_vor_3.32.3.md](../tests/fixtures/archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../tests/tools/archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../../../05_Probelisten_Testdaten/Archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../../../07_Python-Versionen/Archiv/README.md)
- [README_3.32.2_vor_Karten_Performance_2026-10-01.md](../../../07_Python-Versionen/Archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../../../20_Grafik_Master/Archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../../../40_Store_Material/Archiv/README.md)
- [README_3.32.2_vor_3.32.3.md](../../../50_Ablage/Archiv/README_3.32.2_vor_3.32.3.md)
- [README_3.32.2_vor_3.32.3.md](../../../50_Ablage/QA/Dokumentation/Archiv/README_3.32.2_vor_3.32.3.md)
- [README_3.32.2_vor_3.32.3.md](../../../50_Ablage/QA/Dokumentation/Renderlaeufe/Archiv/README_3.32.2_vor_3.32.3.md)
- [README_3.32.2_vor_3.32.3.md](../../../50_Ablage/Screenshots/archiv/README_3.32.2_vor_3.32.3.md)
- [README_3.32.2_vor_3.32.3.md](../../../Archiv/README_3.32.2_vor_3.32.3.md)

## Vorfassungen vor Abschluss 3.32.3

- [qa-verlauf_3.32.3_vor_Abschluss_2026-10-01.md](../tests/archiv/qa-verlauf_3.32.3_vor_Abschluss_2026-10-01.md)
- [Glide_Arbeits_und_Featureplanung_2026-09-30_3.32.3_vor_Abschluss_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [Glide_Sitzungsuebergabe_2026-09-30_3.32.3_vor_Abschluss_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30_3.32.3_vor_Abschluss_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md)
- [README_3.32.3_vor_Abschluss_2026-10-01.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [README_3.32.3_vor_Abschluss_2026-10-01.md](../../../07_Python-Versionen/Archiv/README.md)

## Fortlaufende Arbeitsrichtung und Richtungsabgleich 01.10.2026

- [Arbeitsrichtung, bestätigte Entscheidungen und Abnahme](ARBEITSRICHTUNG.md)
- [Dokumentations-/Prüfwerkzeugnachlauf](../tests/qa-3.32.3/dokumentationsabgleich_2026-10-01/ergebnis.json)
- [Bytegleiche Vorsicherungen](../tests/qa-3.32.3/dokumentationsabgleich_2026-10-01/vorsicherung.json)

Vorsicherungen vor dieser Fortschreibung (alte Inhalte bleiben als Belege erhalten):

- [01_Repository/Glide/AGENTS.md](<../archiv/AGENTS_3.32.3_vor_Richtungsabgleich_2026-10-01.md>)
- [01_Repository/Glide/README.md](../archiv/README.md)
- [01_Repository/Glide/CHANGELOG.md](<../archiv/CHANGELOG_3.32.3_vor_Richtungsabgleich_2026-10-01.md>)
- [01_Repository/Glide/scripts/pflege/README.md](<../scripts/pflege/archiv/README_3.32.3_vor_Richtungsabgleich_2026-10-01.md>)
- [01_Repository/Glide/tests/tools/README.md](../tests/tools/archiv/README.md)
- [01_Repository/Glide/tests/tools/standpruefung.py](<../tests/tools/archiv/standpruefung_3.32.3_vor_Richtungsabgleich_2026-10-01.py>)
- [01_Repository/Glide/tests/qa-verlauf.md](<../tests/archiv/qa-verlauf_3.32.3_vor_Richtungsabgleich_2026-10-01.md>)
- [00_Arbeitsvorbereitung/README.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md)
- [00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md](../../../00_Arbeitsvorbereitung/Checklisten/Archiv/Manuelle_Pruefung_3.14.0.md)
- [00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md](../../../00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md)
- [tests/README.md](../tests/README.md)

## Showcase-Nachlauf 01.10.2026

- [Aktiver Showcase: Datenumfang, Generator, Abgleich und Abnahme](72_SHOWCASE_3.32.3.md)
- [Anleitung der reproduzierbaren Fixture](../tests/fixtures/showcase/README.md)
- [Nutzeranleitung und getrennter Start](../../../05_Probelisten_Testdaten/Showcase/README.md)

Vorsicherungen vor diesem Daten-/Werkzeugnachlauf:

- [Originalarchiv der Beispieldaten vor dem Showcase](../tests/fixtures/beispiele/archiv/glide_beispieldaten_3.32.3_vor_Showcase_2026-10-01.glidebackup), bytegleich aus dem Zwischenstandsabbild wiederhergestellt.
- [05_Probelisten_Testdaten/Glide-Funktionsvorschau_3.30.0.glidebackup](<../../../05_Probelisten_Testdaten/Archiv/Glide-Funktionsvorschau_3.30.0_3.32.3_vor_Showcase_2026-10-01.glidebackup>)
- [01_Repository/Glide/CHANGELOG.md](<../archiv/CHANGELOG_3.32.3_vor_Showcase_2026-10-01.md>)
- [01_Repository/Glide/tests/qa-verlauf.md](<../tests/archiv/qa-verlauf_3.32.3_vor_Showcase_2026-10-01.md>)
- [01_Repository/Glide/scripts/pflege/versionswechsel.py](<../scripts/pflege/archiv/versionswechsel_3.32.3_vor_Showcase_2026-10-01.py>)
- [01_Repository/Glide/scripts/pflege/README.md](<../scripts/pflege/archiv/README_3.32.3_vor_Showcase_2026-10-01.md>)
- [01_Repository/Glide/tests/tools/pruefen.py](<../tests/tools/archiv/pruefen_3.32.3_vor_Showcase_2026-10-01.py>)
- [00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [05_Probelisten_Testdaten/README.md](../../../05_Probelisten_Testdaten/Archiv/README.md)
- [20_Grafik_Master/README.md](../../../20_Grafik_Master/Archiv/README.md)

## Analyse und Planung 01.10.2026

Dokumentations-, Analyse- und Werkzeugnachlauf zu 3.32.3; keine Produktionsversion, Anwendung unverändert.

- [Bestandsaufnahme Code und Dokumentation: Inventar, Ablage, Abweichungen AB01–AB17, Befunde T1–T8](../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md)
- [Konkurrenz- und Featurematrix: Stand 2026, zehn Produkte, Lücken N01–N20](../../../00_Arbeitsvorbereitung/Glide_Konkurrenz_und_Featurematrix_2026-10-01.md)
- [Produktprinzipien und UX-Prüfung: sechs Prinzipien, Befunde U01–U24, Prinzipien-Check](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)
- [Entwicklungsplan ab 3.33](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md)
- [Entscheidungsvorlage D09–D17](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)
- [Nachweise: Linux-Proben, Speicherweg-Messung, Bilder, Ablageabgleich](../tests/qa-3.32.3/analyse_planung_2026-10-01/README.md)
- [Messwerkzeug Speicherweg](../scripts/pflege/messung_speicherweg.py)

Vorsicherungen vor diesem Nachlauf:

- [01_Repository/Glide/CHANGELOG.md](<../archiv/CHANGELOG_3.32.3_vor_Analyse_2026-10-01.md>)
- [01_Repository/Glide/tests/qa-verlauf.md](<../tests/archiv/qa-verlauf_3.32.3_vor_Analyse_2026-10-01.md>)
- [01_Repository/Glide/scripts/pflege/README.md](<../scripts/pflege/archiv/README_3.32.3_vor_Analyse_2026-10-01.md>)
- [00_Arbeitsvorbereitung/README.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Konkurrenzuebersicht_und_persoenliche_Vorlieben_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Konkurrenzuebersicht_und_persoenliche_Vorlieben_2026-10-01.md)
- [README.md der Ablage](<../../../Archiv/README_3.32.3_vor_Analyse_2026-10-01.md>)

## Beschlüsse D09–D17 und Prüfaufrufe 01.10.2026

Dokumentations- und Messnachlauf zu 3.32.3; keine Produktionsversion, Anwendung unverändert.

- [Beschlüsse D09–D17 mit Begründung](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md#beschlüsse-vom-01102026); verbindlich in der [Arbeitsrichtung](ARBEITSRICHTUNG.md#verbindliche-entscheidungen)
- [Befund T8 und Vorschlag P09: wiederholte Prüfungen und Messungen je Bedienschritt](../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md#t8--wiederholte-prüfungen-und-messungen-je-bedienschritt-neu-gemessen)
- [Nachweise: Prüfaufruf- und Pixelschrift-Probe, Rohwerte](../tests/qa-3.32.3/pruefaufrufe_2026-10-01/README.md)

Vorsicherungen vor diesem Nachlauf:

- [01_Repository/Glide/CHANGELOG.md](<../archiv/CHANGELOG_3.32.3_vor_Entscheidungen_2026-10-01.md>)
- [01_Repository/Glide/tests/qa-verlauf.md](<../tests/archiv/qa-verlauf_3.32.3_vor_Entscheidungen_2026-10-01.md>)
- [00_Arbeitsvorbereitung/README.md](../../../00_Arbeitsvorbereitung/Archiv/README.md)
- [00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)
- [00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md)
- [00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md)
- [00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)
- [00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md)
- [00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
- [CLAUDE.md der Ablage](<../../../Archiv/CLAUDE_3.32.3_vor_Entscheidungen_2026-10-01.md>)

## Fundament 3.33.0 und zugehörige Vorsicherungen

- [Fundament-Vertrag](73_FUNDAMENT_3.33.0.md)

- [Vorheriger Regelsatz](../archiv/AGENTS_3.32.3_vor_3.33.0.md)

- [Abschlussnachweis Fundament 3.33.0](../tests/qa-3.33.0/fundament_2026-10-01/ergebnis.json)
- [Laufzeit-Vorsicherungen](../tests/qa-3.33.0/fundament_2026-10-01/vorsicherungen.json)
- [Dokument- und Werkzeugvorsicherungen](../tests/qa-3.33.0/fundament_2026-10-01/dokumentvorsicherungen.json)

## Ergänzungen 3.33.1

- [Bereiche und Fenster](74_BEREICHE_UND_FENSTER_3.33.1.md)

- [Recherche vor Roadmapabgleich 3.33.1](../../../00_Arbeitsvorbereitung/Glide_Funktionsrecherche_Ausbau_2026-09-30.md) – unveränderter vorheriger Planungsstand.

- [Dokumentationsreduktion, Wissenseinstieg und neue Logo-Varianten 3.33.1](75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md)
