# Dokumenten-Existenzprüfung

Stand 24.09.2026 · Glide 3.28.0 · Aufgabenformat 18

## Auftrag und Prüffrage

Geprüft wurde, ob jede nicht archivierte Dokumentdatei einen eigenständigen,
gegenwärtigen Zweck besitzt. Zusätzlich wurden die Archive als Bestandklasse
auf Erhaltungsgrund, Dubletten und Leseregel geprüft. „Existenzrecht“ bedeutet
hier: Die Datei ist für Navigation, Produktvertrag, Entscheidung, Ausführung,
Migration oder einen unveränderlichen Nachweis erforderlich. Ein bloßer alter
Dateiname oder ein Verweis auf einen anderen Verweis reicht dafür nicht.

## Ergebnis

- **110 aktive Dokumentdateien**: 76 .md, 15 .pdf, 19 .txt.
- **1311 archivierte Dokumentdateien**: 9 .docx, 1267 .md, 10 .pdf, 25 .txt.
- Die automatische Standprüfung bewertet davon die 76 aktiven
  Markdown-Dateien. PDF- und Textbelege werden über Zweck, Pfad und Hash
  bewertet, nicht über fortzuschreibende Standzeilen.
- **Sechs aktive Redundanzen archiviert**: vier historische Wegweiser, die
  doppelte Kurzfassung der Dokumentenpflege und der ausdrücklich abgelöste
  Reiterentwurf 3.10.0.
- **Keine aktive Dokumentdatei ohne begründeten Zweck verblieben.**
- Zwei sachlich überholte Hinweise wurden korrigiert: die Laufzeitangabe in
  requirements/runtime.txt und die plattformspezifische Behauptung in
  tests/tools/README.md.

## Archivierte Redundanzen dieser Prüfung

| Vorher aktiv | Neuer Ort | Grund |
|---|---|---|
| 00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-16.md | 00_Arbeitsvorbereitung/Archiv/Glide_Funktionsvorschlaege_Wegweiser_2026-09-24.md | Wegweiser auf bereits archivierte, abgeschlossene Vorschläge |
| 00_Arbeitsvorbereitung/Glide_KI_Austauschformat_und_Zukunftsarchitektur.md | 00_Arbeitsvorbereitung/Archiv/Glide_KI_Austauschformat_Wegweiser_2026-09-24.md | Wegweiser auf Archiv und aktuellen Austauschvertrag |
| 40_Store_Material/Apple/Store_Angaben_Apple.md | 40_Store_Material/Archiv/Store_Angaben_Apple_Wegweiser_2026-09-24.md | Wegweiser auf historische Store-Recherche |
| 40_Store_Material/Microsoft/Store_Angaben_Microsoft.md | 40_Store_Material/Archiv/Store_Angaben_Microsoft_Wegweiser_2026-09-24.md | Wegweiser auf historische Store-Recherche |
| 01_Repository/Glide/docs/decisions/DOKUMENTENPFLEGE.md | 01_Repository/Glide/docs/decisions/archiv/DOKUMENTENPFLEGE_Wegweiser_2026-09-24.md | verkürzte Doppelung des verbindlichen Pflegevertrags |
| 01_Repository/Glide/docs/32_REITERANSICHT.md | 01_Repository/Glide/docs/archiv/32_REITERANSICHT_3.10.0_aus_aktivem_Bestand_2026-09-24.md | abgeschlossener, durch Dokument 33 ersetzter Entwurf |

Alle aktiven Verweise wurden direkt auf das maßgebliche Dokument oder dessen
Archivziel umgestellt. Es wurde kein historischer Inhalt gelöscht.

## Entscheidung für jede aktive Dokumentdatei

Die Begründung einer Gruppe gilt für jede darunter vollständig aufgeführte
Datei. Dadurch bleibt die Prüfung vollständig, ohne denselben Satz über hundert
Mal zu wiederholen.

### Projektweiter Einstieg (1)

Behalten: führt durch die gesamte Arbeitsablage und verweist auf den kanonischen Repository-Einstieg.

- README.md

### Ablage- und Bereichseinstiege (10)

Behalten: erklärt den Zweck eines eigenständigen Projektbereichs; historische Detailinhalte werden nur verlinkt.

- 05_Probelisten_Testdaten/README.md
- 07_Python-Versionen/README.md
- 10_Dokumentation/README.md
- 20_Grafik_Master/README.md
- 30_Release_Exports/README.md
- 40_Store_Material/README.md
- 50_Ablage/README.md
- 50_Ablage/Screenshots/3.5.0/LIESMICH.md
- 50_Ablage/Screenshots/README.md
- 90_Testdaten_Extern/README.md

### Aktive Planung, Recherche und manuelle Abnahme (7)

Behalten: enthält aktuelle Produktentscheidungen, priorisierte Aufgaben oder noch auszuführende Abnahmen.

- 00_Arbeitsvorbereitung/Checklisten/Glide_Veroeffentlichung_Checkliste.txt
- 00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.28.0.md
- 00_Arbeitsvorbereitung/Fehlerprotokolle/README.md
- 00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md
- 00_Arbeitsvorbereitung/Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md
- 00_Arbeitsvorbereitung/Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md
- 00_Arbeitsvorbereitung/README.md

### Repository-Einstieg und Governance (8)

Behalten: öffentliches README, Arbeitsregeln, Änderungsverlauf, Lizenz- und Sicherheitsstatus haben getrennte verbindliche Rollen.

- 01_Repository/Glide/AGENTS.md
- 01_Repository/Glide/assets/README.md
- 01_Repository/Glide/CHANGELOG.md
- 01_Repository/Glide/LICENSE.md
- 01_Repository/Glide/packaging/README.md
- 01_Repository/Glide/README.md
- 01_Repository/Glide/SECURITY.md
- 01_Repository/Glide/src/glide/README.md

### Aktuelle Kern- und Releaseverträge (11)

Behalten: gegenwärtiger Architektur-, Daten-, QA-, Übergabe- oder Releasevertrag.

- 01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md
- 01_Repository/Glide/docs/02_ARCHITECTURE.md
- 01_Repository/Glide/docs/03_STARTKONTEXT.md
- 01_Repository/Glide/docs/05_QA_TESTPLAN.md
- 01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md
- 01_Repository/Glide/docs/07_QA_BERICHT.md
- 01_Repository/Glide/docs/09_PROJECT_HANDOFF.md
- 01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md
- 01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md
- 01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md
- 01_Repository/Glide/docs/DEV_NOTES.md

### Dokumentationssteuerung und Prüfung (4)

Behalten: Index, Pflegeregeln und Prüfberichte steuern den gültigen Lesebestand.

- 01_Repository/Glide/docs/00_INDEX.md
- 01_Repository/Glide/docs/63_ARCHIV_UND_DOKUMENTATIONSPRUEFUNG_2026-09-24.md
- 01_Repository/Glide/docs/64_DOKUMENTEN_EXISTENZPRUEFUNG_2026-09-24.md
- 01_Repository/Glide/docs/DOKUMENTENPFLEGE.md

### Fortgeltende Funktionsverträge (15)

Behalten: ältere Versionsnummer bezeichnet die Einführung einer weiterhin vorhandenen Funktion; der Vertrag bleibt bis zu einem kumulativen Ersatz aktiv.

- 01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md
- 01_Repository/Glide/docs/46_TAGESMODELL_3.22.0.md
- 01_Repository/Glide/docs/47_CHECKLISTE_3.22.0.md
- 01_Repository/Glide/docs/48_ANSICHTEN_UND_STARTSEITE_3.22.0.md
- 01_Repository/Glide/docs/49_PINNWAND_UND_DARSTELLUNG_3.22.0.md
- 01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md
- 01_Repository/Glide/docs/51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md
- 01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md
- 01_Repository/Glide/docs/53_PINNWAND_ARBEITSFLAECHE_3.23.0.md
- 01_Repository/Glide/docs/54_ANZEIGEMODI_3.23.0.md
- 01_Repository/Glide/docs/55_NAVIGATION_UND_PINNWAND_3.24.0.md
- 01_Repository/Glide/docs/56_STARTSEITE_UND_RUECKMELDUNG_3.24.0.md
- 01_Repository/Glide/docs/57_UEBERSICHT_UND_HIERARCHIE_3.25.0.md
- 01_Repository/Glide/docs/58_STARTSEITE_UND_BEGLEITER_3.25.0.md
- 01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md

### Zeichenflächenvertrag und Übergabe (2)

Behalten: trennt den geprüften isolierten Prototyp von der noch nicht umgesetzten produktiven Integration.

- 01_Repository/Glide/docs/61_ZEICHENFLAECHE_ISOLIERTER_KERN_2026-09-24.md
- 01_Repository/Glide/docs/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md

### Geltende Produktentscheidungen (4)

Behalten: produktweite Entscheidung oder Invariante, auf die aktive Implementierung und Tests Bezug nehmen.

- 01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md
- 01_Repository/Glide/docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md
- 01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md
- 01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md

### Offene Releaseentscheidungen (3)

Behalten: Lizenz, Signierung, Marke oder Vertrieb sind vor einer Veröffentlichung noch verbindlich zu entscheiden.

- 01_Repository/Glide/docs/decisions/LIZENZENTWURF_3.26.0.md
- 01_Repository/Glide/docs/decisions/SIGNIERUNG_3.26.0.md
- 01_Repository/Glide/docs/decisions/VERTRIEB_UND_MARKE_3.26.0.md

### Aktive Testdokumentation (2)

Behalten: erläutert den tatsächlich ausführbaren Prüfrahmen und seine Grenzen.

- 01_Repository/Glide/tests/README.md
- 01_Repository/Glide/tests/tools/README.md

### Test-Fixtures und Testdokumentation (1)

Behalten: erklärt unveränderliche Testeingaben und deren Herkunft.

- 01_Repository/Glide/tests/fixtures/README.md

### Abhängigkeits- und Buildverträge (4)

Behalten: maschinennahe Manifestdatei; leere Listen sind eine bewusste Aussage über fehlende Zusatzabhängigkeiten.

- 01_Repository/Glide/requirements/build-macos.txt
- 01_Repository/Glide/requirements/build-windows.txt
- 01_Repository/Glide/requirements/dev.txt
- 01_Repository/Glide/requirements/runtime.txt

### Migrations- und Kompatibilitätseingaben (7)

Behalten: alte Textformate sind absichtliche Eingaben für Import- und Migrationsprüfungen.

- 90_Testdaten_Extern/Legacy_Probelisten/funktionstest_2026-05-28_10-38.txt
- 90_Testdaten_Extern/Legacy_Probelisten/probeliste_funktionstest___scrollen.txt
- 90_Testdaten_Extern/Legacy_Probelisten/probeliste_projektmarketing_neubau.txt
- 90_Testdaten_Extern/Legacy_Probelisten/probeliste_tagesgeschäft.txt
- 90_Testdaten_Extern/Legacy_Probelisten/probeliste_website___design.txt
- 90_Testdaten_Extern/Legacy_Probelisten/probeliste_weg_verwaltung.txt
- 90_Testdaten_Extern/Legacy_Probelisten/README_probelisten.txt

### Prüf- und Rendernachweise (31)

Behalten als kalter Nachweis: datierte Ergebnisse und Vorstände sind keine aktuelle Anleitung, sichern aber Reproduzierbarkeit und Provenienz.

- 01_Repository/Glide/tests/qa-verlauf.md
- 50_Ablage/QA/Bestandsanalyse_3.2.0/codeaudit.md
- 50_Ablage/QA/Dokumentation/README.md
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/artifact.md
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final1.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final2.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final2/3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final3.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final4.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final4/3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final5.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/final5/3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/QA_ABSCHLUSS.md
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/reference.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/3.2.0_2026-09-04/reference/2.6.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/_qa_docx_source/source.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/_qa_docx_v252_final3/2.5.2 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/_qa_docx_v252_final4/2.5.2 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/_qa_docx_v252_final5/2.5.2 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/_qa_docx_v252_intermediate/Glide_v2.5.2_intermediate.pdf
- 50_Ablage/QA/Dokumentation/Renderlaeufe/README.md
- 50_Ablage/QA/qa-3.5.0/linux-vorpruefung/LIESMICH.md
- 50_Ablage/QA/qa-3.6.0/ausgang-3.5.0/LIESMICH.md
- 50_Ablage/QA/qa-3.6.0/ui-nachbesserung/ausgang-app.txt
- 50_Ablage/QA/qa-3.6.0/vorlagen-jahresanzeige/ausgang-app.txt
- 50_Ablage/QA/qa-3.7.0/ausgang-3.6.0/app.pyw.txt
- 50_Ablage/QA/qa-3.7.0/dynamische-kacheln/app_vor_dynamischen_kacheln.pyw.txt
- 50_Ablage/QA/qa-3.7.0/dynamische-kacheln/refresh_library_page_vorher.py.txt
- 50_Ablage/QA/qa-3.7.0/dynamische-kacheln/vorher_test_release37.py.txt
- 50_Ablage/QA/qa-3.7.0/dynamische-kacheln/vorher_test_ui_followup36.py.txt
- 50_Ablage/QA/qa-3.9.0/oberflaeche/vor_tab_absicherung_abgebrochen/README.md

## Existenzrecht der Archive

Archivdateien werden nicht als aktuelle Anweisung gelesen. Ihr Zweck ist die
zeitliche Nachvollziehbarkeit von Entscheidungen, Migrationen, Änderungen und
QA-Läufen. Deshalb bleiben die 1311 archivierten Dokumentdateien erhalten.

Die Hashprüfung fand **61 Gruppen mit insgesamt 132 bytegleichen Archivdateien**.
Diese Gleichheit ist allein kein Löschgrund: Mehrere Dateien sind benannte
Vorstände unterschiedlicher Arbeitsschritte oder Bestandteile abgeschlossener
QA-Pakete. Ihre Pfade belegen, zu welchem Schritt sie gehörten. Sie bleiben
im kalten Archiv und werden von normalen Folgearbeiten nicht eingelesen.

Für künftige Bereinigungen gilt: Eine Archivdubletten-Gruppe darf nur reduziert
werden, wenn ein separates Manifest Quelle, Ziel, Hash und historischen
Kontext aller entfernten Pfade erhält. Eine solche Löschung war nicht Teil
dieser Prüfung.

## Bewusste Grenzfälle

- docs/45_... bis docs/59_... bleiben trotz älterer Versionsnummern aktiv,
  weil sie fortgeltende Funktionsverträge sind.
- Die Dateien LIZENZENTWURF_3.26.0.md, SIGNIERUNG_3.26.0.md und
  VERTRIEB_UND_MARKE_3.26.0.md bleiben aktiv, weil die betreffenden
  Veröffentlichungsentscheidungen weiterhin offen sind.
- Alte Probelisten unter 90_Testdaten_Extern sind Testeingaben, keine
  überholte Dokumentation.
- Datierte QA- und Renderdateien unter 50_Ablage/QA bleiben unveränderliche
  Nachweise; ihre Existenz behauptet keine aktuelle Releasefreigabe.
- CHANGELOG.md und docs/00_INDEX.md sind groß, besitzen aber jeweils eine
  nicht teilbare Verlaufs- beziehungsweise Navigationsfunktion. Neue Agenten
  sollen sie gezielt durchsuchen statt vollständig lesen.

## Nicht zur Dokumentenklasse gehörende Funde

fix_reiter_bug.py und replace_buttons.py im Repository-Stamm sind einmalige
Reparaturskripte. Sie wurden nicht als Dokumente bewertet und nicht verändert.
Vor einer öffentlichen Repository-Bereitstellung sollten sie separat als
Quellwerkzeug geprüft und gegebenenfalls nach tests/tools/archiv/ verschoben
werden.

## Prüfmethode und Abnahme

- vollständige Dateiinventur nach den Endungen Markdown, Text, PDF, DOCX, RTF
  und ODT; virtuelle Umgebungen wurden ausgeschlossen;
- Einzelzuordnung jeder aktiven Datei zu einer begründeten Bestandklasse;
- getrennte Hashprüfung der Archivdateien;
- direkte Verweise anstelle aktiver Wegweiser;
- Versions-, Stand- und Markdown-Linkprüfung nach der Bereinigung.

Ergebnis: Der aktive Dokumentbestand enthält nur Dateien mit einem aktuellen
operativen Zweck oder einem ausdrücklich als kalt gekennzeichneten Prüfzweck.
Historische Inhalte liegen in Archiven und müssen für normale Folgeaufgaben
nicht gelesen werden.
