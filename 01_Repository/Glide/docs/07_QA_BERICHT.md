# QA-Bericht – Glide 3.33.6

Stand 03.10.2026 · App 3.33.6 · Datenformat 20 · macOS, Python 3.14.5, Tk 9.0.3

Einziger Prüfbericht. Am 03.10.2026 mit dem bisherigen Prüfverlauf (`tests/qa-verlauf.md`) zusammengeführt und auf die Nachweise der letzten sieben Versionen gekürzt; ältere Läufe stehen nur noch als Zeile in der Übersicht, ihre Protokolle trägt Git. Wie geprüft wird: [Prüfplan](05_QA_TESTPLAN.md).

## Aktueller Stand

**3.33.6 geprüft und lokal ausgeliefert (02.10.2026):** Vollprüfung Exitcode 0 im dritten Lauf – 81 Schritte, alle 64 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; Quellstand (342 Dateien) unverändert. 146 Python-/60 Bundle-Dateien per SHA-256 gleich `src/glide`, Bundle `de.shaye.glide`, `codesign --verify --deep --strict` bestanden. [Nachweis](../tests/qa-3.33.6/heute_2026-10-02/README.md).

**Grenzen jeder bisherigen Abnahme:** echte Tastatur-, Maus- und Trackpadbedienung, Windows und Linux, DPI und mehrere Monitore, Screenreader. Alle Läufe mit temporärem `GLIDE_DATA_DIR` und künstlichen Daten; keine echten Nutzerdaten gelesen. Entwicklungsbundle mit Ad-hoc-Signatur und installiertem Python; **keine Releasefreigabe**.

## Versionen 3.33.0–3.33.6

| Version | Datum | Inhalt | Vollprüfung | Lieferung | Nachweis |
|---|---|---|---|---|---|
| 3.33.6 | 02.10.2026 | Heute und Demnächst (D14) | Exit 0 im 3. Lauf, 81 Schritte, 64 Suiten | 146/60 bytegleich | [README](../tests/qa-3.33.6/heute_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.6/heute_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.6/heute_2026-10-02/auslieferung.json) |
| 3.33.5 | 02.10.2026 | Eisenhower als Gruppierung (D13) | Exit 0, 80 Schritte, 63 Suiten | 145/59 | [README](../tests/qa-3.33.5/eisenhower_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.5/eisenhower_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.5/eisenhower_2026-10-02/auslieferung.json) |
| 3.33.4 | 02.10.2026 | Wiederholungen in der Schnelleingabe | Exit 0, 79 Schritte, 62 Suiten | 144/58 | [README](../tests/qa-3.33.4/wiederholung_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.4/wiederholung_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.4/wiederholung_2026-10-02/auslieferung.json) |
| 3.33.3 | 02.10.2026 | Deutsche Schnelleingabe mit Feldchips (G01, D10) | Exit 0, 79 Schritte, 62 Suiten | 144/58 | [README](../tests/qa-3.33.3/eingabe_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.3/eingabe_2026-10-02/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.3/eingabe_2026-10-02/auslieferung.json) |
| 3.33.2 | 02.10.2026 | Startseite „Ruhig“ (D12), Aufbau 764 → 507 ms | Exit 0 im 2. Lauf, 78 Schritte, 61 Suiten | 143/57 | [README](../tests/qa-3.33.2/startseite_2026-10-02/README.md) · [Protokoll](../tests/qa-3.33.2/startseite_2026-10-02/vollpruefung/ergebnis.json) · [Messung](../tests/qa-3.33.2/startseite_2026-10-02/messung/zusammenfassung.json) |
| 3.33.1 | 01./02.10.2026 | Vier Bereiche, Fenster, Logo | Exit 0 im 3. Lauf, 77 Schritte, 60 Suiten | 142/56 | [README](../tests/qa-3.33.1/abschluss_2026-10-01/README.md) · [Protokoll](../tests/qa-3.33.1/abschluss_2026-10-01/vollpruefung_3/ergebnis.json) · [Lieferung](../tests/qa-3.33.1/abschluss_2026-10-01/auslieferung.json) |
| 3.33.0 | 01.10.2026 | Fundament T2, P09a | Exit 0, 76 Schritte, 59 Suiten | 140/54 | [README](../tests/qa-3.33.0/fundament_2026-10-01/README.md) · [Protokoll](../tests/qa-3.33.0/fundament_2026-10-01/vollpruefung/ergebnis.json) · [Lieferung](../tests/qa-3.33.0/fundament_2026-10-01/auslieferung.json) |

„Lieferung“ nennt die Python-/Bundle-Dateien, die per SHA-256 gleich `src/glide` sind; jede Version mit gültiger Signatur und ausgeliefertem Showcase. Jede Funktionsversion hat eine neue Pflichtsuite, deren Gegenprobe mit der Vorversion rot war.

### Befunde und ungültige Läufe

Regeln, die aus diesen Läufen folgen (nicht tippen, nicht sperren, Last vermeiden, „Flaky“ ist keine Ursache), stehen im [Prüfplan](05_QA_TESTPLAN.md#regeln).

- **3.33.6:** Zwei ungültige Vorläufe: gesperrter Bildschirm (`test_ui39`, `test_workspace310` rot, Stillstand) und ein Zeitrennen unter Last: `test_speicherlast330` prüfte den 700 ms später gezeigten Formathinweis erst nach seinem Leerlauf, während OneDrive über 200 % CPU belegte. Laden plus Leerlauf je rund 420–433 ms in 3.33.5 und 3.33.6, also keine Verlangsamung; die Suite akzeptiert jetzt „vorgemerkt oder gezeigt“. Sieben Altsuiten auf D14 gebracht.
- **3.33.5:** `test_features322`/`325` fanden einen nicht zugeordneten Palettenbefehl (Risiko R2, Gruppierung über Beschriftungen); behoben.
- **3.33.2:** Erster Lauf nur an der Attributprüfung gescheitert (Hilfsklasse ohne Canvas-Basis, heute `DeferredDrawCanvas`). Messung auf macOS mit 1.000 Punkten: Aktualisierung 764,2 → 506,7 ms, Wechsel 789,7 → 547,8 ms, Bibliothek 974 → 856 ms; Ziel 150 ms nicht erreicht, der Rest ist Tk-Layout je Widget.
- **3.33.1:** Erste Vollprüfung des Prüfkandidaten rot (`audit_app`, `test_ui39`, `test_features329`, `test_aufraeumen330`): Dialog „Neu anlegen“ blieb auf niedrigen Bildschirmen einspaltig (echter Fehler), Notizbücher nahmen keine datierten Zeichnungen auf (Klarstellung des Inhabers), zwei Prüfungen veraltet. Danach zwei ungültige Läufe: gesperrter Bildschirm ab 00:16 und vermutlich Tastatureingaben während des Laufs. Die Aktivierungsprobe zeigt: Der Hintergrundmodus schirmt die Maus ab, nicht die Tastatur. Einstellungsfenster bis zur Anzeige im Median rund 2,1 s.
- **3.33.0:** Formatsicherung 161,406 → 17,896 ms kalt und 0,064 ms nach dem Laden (5.000 Aufgaben, zwölf Runden), neun → eine JSON-Lesung; ungenutzte Tabellenmessung 77,117 → 0,001 ms. Der alte QA-Hintergrund scheitert absichtlich am nativen Mausisolierungstest, der neue besteht ([Nachweis](../tests/qa-3.33.0/fundament_2026-10-01/native_isolation.json)). Drei historische Recherchelogs fehlen seit dem GitHub-Upload.

### Nachläufe ohne neue App-Version

| Datum | Nachlauf | Nachweis |
|---|---|---|
| 03.10.2026 | Bereinigung der Ablage und Dokumentation: Archive auf 3.33.0–3.33.6, Fensterbilder nur 3.33.4–3.33.6, Dokumente zusammengeführt (Linux/Tk 8.6, künstliche Daten) | [README](../tests/qa-3.33.6/aufraeumen_2026-10-03/README.md) |
| 02.10.2026 | Schlanke Ablage: Archivkopien entfernt, CI-Schritt „Ablagegröße“ | [README](../tests/qa-3.33.6/ablage_2026-10-02/README.md) |
| 01.10.2026 | Analyse und Planung, Beschlüsse D09–D17, Showcase, Prüfaufruf- und Speicherwegmessung (Linux, Xvfb), Dokumentations- und Werkzeugabgleich zu 3.32.3 | Protokolle in Git (Ordner `tests/qa-3.32.3`, gelöscht am 03.10.2026) |

## Ältere Versionen

Nur das Ergebnis; Berichte und Protokolle stehen in der Git-Historie.

| Version | Datum | Ergebnis |
|---|---|---|
| 3.32.3 | 01.10.2026 | Exit 0, 73 Schritte, 58 Suiten; Bibliotheksrefresh bei 1.000 Aufgaben 776,2 → 4,9 ms; 139/53 bytegleich |
| 3.32.2 | 30.09.2026 | Exit 0, 72 Schritte, 57 Suiten; Ziehen in Seiten/Notizen (D04), Schriftcache, gebündelte Layouts |
| 3.32.1 | 30.09.2026 | Exit 0, 71 Schritte, 56 Suiten; Klappkontrolle (D08) |
| 3.32.0 | 30.09.2026 | Exit 0, 70 Schritte, 55 Suiten; Etappe 1, zwei Hänger behoben, Prüfungen erstmals im Hintergrund |
| 3.31.0 | 30.09.2026 | Exit 0, 69 Schritte, 54 Suiten; Rückmeldung R1–R11, 41 Fenster geprüft |
| 3.30.0 | 25.–29.09.2026 | Modernisierung, Format 20; zuletzt Exit 0 mit 66 Schritten, 51 Suiten |
| 3.29.0 | 24.09.2026 | Exit 0, 50 Schritte; Zeichnungsseite, Format 19 |
| 3.28.0 | 23.09.2026 | Gesamtlauf offen (OneDrive-Platzhalter, Zeitüberschreitungen); Tagebuch, Format 18 |
| 3.26.0 | 21.09.2026 | Exit 0, 47 Schritte (Windows, Python 3.13.15); Notizlisten, Format 17 |
| 3.25.0 | 19.09.2026 | Exit 0 (Windows, Python 3.13.15) |

## Offen und nur manuell prüfbar

Einzelpunkte: [Manuelle Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md).

- Bedienung mit echter Maus, Trackpad und Tastatur, vor allem Ziehen (Board, Seitenleiste, Stundenraster), Zeichnen, Chips der Schnelleingabe, „Heute“ und „Tag …“;
- Migration eines echten Bestands (mit Kopie automatisch geprüft; offen bleibt die Sichtkontrolle). **3.29 nach der Umstellung nicht mehr starten**;
- Windows-Gesamtlauf (fehlt seit 3.29), Linux-Desktop, Pixelschrift unter Windows und Linux;
- Bildschirmleser (NVDA, VoiceOver); DPI 100/150/200 % und zwei Monitore;
- Druck und PDF mit und ohne Pinnwandhintergrund; flüssige Bedienung mit 500 Karten.

**Nicht durch Agenten prüfbar:** Signatur, Notarisierung und Installer; Markenprüfung; Store-Freigabe.
