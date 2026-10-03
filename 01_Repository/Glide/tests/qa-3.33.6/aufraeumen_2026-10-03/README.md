# Aufräumen der Ablage – Nachweis

03.10.2026 · App 3.33.6 unverändert, kein Versionswechsel · Linux/Tk 8.6, künstliche Daten · Ausgangsstand `7f30baf` (main nach PR #10)

Auftrag des Inhabers vom 03.10.2026: keine Dopplungen, nur aktuelle und für die Code-Basis relevante Dokumente; Archive auf die letzten sieben Versionen, Fensterbilder auf die letzten drei; leere Ordner und Archive entfernen; Erledigtes kennzeichnen; gleiche Inhalte zusammenführen und löschen statt archivieren; `.gitignore` für Archive, Protokolle und Sicherheit prüfen.

## Ergebnis (versionierter Stand, Git-Baum vorher/nachher)

| Bereich | Dateien vorher | MB vorher | Dateien nachher | MB nachher |
|---|---:|---:|---:|---:|
| gesamt | 4.985 | 1.158,0 | 843 | 406,3 |
| `00_Arbeitsvorbereitung` | 142 | 2,7 | 5 | 0,1 |
| `01_Repository/Glide/docs` | 177 | 7,1 | 16 | 0,2 |
| `tests/qa-*` | 1.922 | 422,9 | 284 | 79,2 |
| Releaseplanungen (`tests/fixtures/beispiele`) | 41 | 1,2 | 17 | 0,5 |
| `07_Python-Versionen/Archiv` | 582 | 155,0 | 7 | 16,5 |
| `05_Probelisten_Testdaten` | 86 | 85,8 | 7 | 76,6 |
| `20_Grafik_Master` | 50 | 133,2 | 34 | 111,5 |
| `40_Store_Material` | 29 | 0,1 | – | – |

Markdown-Dateien 659 → 56; Dokumentzeilen in `00_Arbeitsvorbereitung` und `docs/` 100.339 → rund 2.500; Änderungsverlauf 2.461 → 134 Zeilen; Fensterbilder 587 → 150 (3.33.4–3.33.6). Zahlen in [ergebnis.json](ergebnis.json); MB = 10⁶ Byte (die Ablageprüfung rechnet in MiB und meldet 387). Die Git-Historie behält alle früheren Stände; sie wurde nicht umgeschrieben.

## Regeln, die das dauerhaft halten

- **Sieben Versionen:** `tests/tools/ablagegroesse.py`, Regel „Archivalter“ – Hauptdateien in `07_Python-Versionen/Archiv`, Nachweise `tests/qa-<Version>` und Releaseplanungen nur der sieben neuesten Versionen. Ausnahmen (`DAUERHAFT`): je ältere Formatstufe ab 11 die letzte Releaseplanung als Lesbarkeitsbeleg und 3.30.0 für `test_tempo330`.
- **Drei Bildstände:** Regel „Fensterbilder“ – `fenster/` nur in den drei neuesten Versionen; neue Fensterbilder sind ohnehin nicht versioniert (`01_Repository/Glide/.gitignore`).
- **Kürzen:** `scripts/pflege/ablage_kuerzen.py` (mit `--anzeigen` als Probe) löscht, was die Regeln melden; `versionswechsel.py` ruft es am Ende auf. Die CI-Grundstufe (Schritt „Ablagegröße“) weist Abweichungen zurück.
- **`.gitignore`:** Abschnitte Sicherheit (Schlüssel, Zertifikate, Profile, `.env`, Zugangsdaten), Nutzerdaten (Bestände, Sicherungen, Showcase-`Arbeitsstand`), Protokolle (`*.log`), Archive (`**/[Aa]rchiv/` außer `07_Python-Versionen/Archiv`, `*_Z/`, `*.fetch`, `*.bak`), Werkzeuge. Grenze: Sie wirkt nur auf neue, nicht versionierte Dateien; `git add -f` und Web-Uploads umgeht sie. Deshalb prüfen zusätzlich CI (Datenschutz, Ablagegröße) und Secret Scanning.

## Zusammengeführt

| Neu | Ersetzt |
|---|---|
| `00_Arbeitsvorbereitung/Glide_Uebergabe.md` | Sitzungsübergabe 30.09., Projektübergabe (`docs/09`), Startkontext (`docs/03`), Sitzungsprotokoll 24.–26.09. (auch `docs/67`), Bestandsaufnahme Code und Dokumentation |
| `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md` (Statusmarken ✅ ◐ ▶ ○ ◇ ✕) | Entwicklungsplan 3.33ff, Entscheidungsvorlage D09–D17, Arbeits- und Featureplanung, Aufgabenauswahl, Funktionsrecherche Ausbau, Aufgabenkatalog und Arbeitsvorbereitung Modernisierung, Aufgabensammlung Zeichenfläche, Prüf-, Übersichts- und Rückmeldungsentscheidungen 27.–29.09. |
| `00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md` | Konkurrenz- und Featurematrix, Konkurrenzübersicht mit Vorlieben, Wettbewerbsrecherche, Funktionsvergleich, Produktprinzipien und UX-Prüfung |
| `00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md` | Checklisten Manuelle und Windows-Prüfung 3.30.0 |
| `docs/20_FUNKTIONEN.md` | Funktionsverträge `docs/45`–`docs/79` (32 Dateien) |
| `docs/10_VEROEFFENTLICHUNG.md` | `docs/10_RELEASE_CHECKLIST`, Entscheidungen Signierung, Vertrieb und Marke, Lizenzentwurf, `40_Store_Material` |
| `docs/02_ARCHITECTURE.md` | `DEV_NOTES`, Tk-Fallstricke und Performance-Regeln aus den Verträgen |

Ohne Nachfolger gelöscht, weil umgesetzt: Konzept „Seiten wie Notion“ (3.30) und die SVG-/Zeichnungsdaten-Untersuchung (3.29).

Auch korrigiert: Formatstufe 10 entstand mit 2.11.0, nicht 3.4.0 ([Daten und Migration](../../../docs/06_DATA_BACKUP_MIGRATION.md#formatstufen)); die Werkzeugübersicht behauptete, der Hintergrundmodus schirme die Tastatur ab.

## Bewusst behalten

- `07_Python-Versionen` ↔ `src/glide` und `05_Probelisten_Testdaten/Showcase` ↔ `tests/fixtures/showcase`: Lieferkopien, per SHA-256 abgeglichen; Git speichert gleiche Inhalte einmal.
- Grafikmaster in `20_Grafik_Master` (Inhaberdateien). Offen beim Inhaber: Rechte an Fremdbildern in `05_Inspiration` und `06_Beispielbilder` im öffentlichen Repository.
- Textangaben in `tests/tools/releasedaten.py`, die auf entfernte Dokumente verweisen: Sie sind Teil der reproduzierten Releaseplanung 3.33.6 und ändern sich erst mit der nächsten Produktionsrunde.

## Prüfung

Linux-Container, Python 3.14 mit Tk 8.6 unter Xvfb, künstliche Daten: CI-Grundstufe vollständig, Standprüfung ohne Befund, Werkzeugtests (`test_standpruefung`, `test_ablagegroesse`) grün, alle relativen Links aller Markdown-Dateien auflösbar. Keine macOS-/Tk-9-Abnahme nötig, da die App unverändert ist.
