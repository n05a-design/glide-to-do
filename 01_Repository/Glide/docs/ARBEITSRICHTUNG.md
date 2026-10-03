# Arbeitsrichtung, Entscheidungen und Abnahme

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20

Verbindliches Entscheidungsregister und Arbeitsablauf. Am 03.10.2026 mit der Entscheidungsvorlage vom 01.10.2026 und den Entscheidungslisten vom 25.–30.09.2026 zusammengeführt; deren Wortlaut trägt Git. Aufgabenstand und Reihenfolge: [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md). Technische Regeln: [Architektur](02_ARCHITECTURE.md).

**Grundsatz:** Entschiedenes wird nicht erneut vorgelegt. Offen sind nur D07, die Auswahl A–H mit ihrer Bearbeitungstiefe, die erste Importquelle (G21), das Bauwerkzeug (G26) und die Inhaberangaben I1–I6. Empfehlungen in Dokumenten ersetzen keine Entscheidung des Inhabers; jeder Umsetzungsschnitt außerhalb der beauftragten Performance-Arbeit braucht einen ausdrücklichen Auftrag.

## Verbindliche Entscheidungen

| Nr. | Entscheidung | Stand |
|---|---|---|
| D01 | Allgemeine Datumsangaben setzen den Bearbeitungstag; ausdrücklich „fällig/bis“ setzt die Fälligkeit. Erkannte Felder sind vor dem Speichern sichtbar und rücknehmbar. | umgesetzt 3.33.3 |
| D02 | Eine Aktion bewirkt die im sichtbaren Zielkontext erwartbare Änderung: Ziehen auf einen Bearbeitungstag setzt `planned_date`, auf einen Zeitblock zusätzlich `planned_time`, auf einen ausdrücklichen Fälligkeitstermin `due`/`due_time`; neutrales Umordnen erhält Termine. Ziel und Feld sind vor dem Loslassen erkennbar, ein Undo-Schritt. Keine pauschale Erlaubnis, Fälligkeiten zu löschen. | gilt für jeden UI-Vertrag |
| D03 | Desktop/Tk optimieren; Mobile und Toolkit-Probe zurückgestellt. | gilt |
| D04 | Drag-and-drop erweitert die bestehenden Bereiche. | umgesetzt 3.32.2 |
| D05 | Einzelne Aufgaben in Notizen und Seiten mit erhaltener ID; Liste, Notiz und Seite bleiben eigenständige Arten, keine allgemeine Umwandlung (beantwortet F11). | G29/G31 offen |
| D06 | Die Gestaltung der Hinweisblöcke in Seiten bleibt unverändert. | gilt |
| D07 | Exportumfang der Animation: abspielbares GIF oder zunächst Frames/Vorschau/PNG-Spritesheet (Empfehlung: Spritesheet zuerst). | **offen**, erst zur Pixel-Etappe |
| D08 | Alle Klappmechanismen über echte Bedienbindungen prüfen, einschließlich Zustandserhalt, Tastatur und Tk-Callbackfehler. | umgesetzt 3.32.1, Pflichtsuite |
| D09 | Das GitHub-Repository `glide-to-do` ist die maßgebliche Ablage (Wurzel = Projektordner, Quellbaum `01_Repository/Glide`); Uploads nur in diese Struktur. Öffentlich: Rohprotokolle (`*.log`) bleiben lokal, veröffentlichte Ergebnisse ohne Benutzerpfade (`pfade_bereinigen.py`, CI „Datenschutz“). Keine Archivkopien von Fixtures und Showcase, keine Fensterbilder neuer Vollprüfungen (02.10.2026); Archive und Nachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten, Dokumente werden zusammengeführt und gelöscht statt archiviert (03.10.2026); CI „Ablagegröße“ prüft das. Sicherheitsmeldungen über GitHub (`SECURITY.md`), Dependabot; CodeQL-Workflow vom Inhaber deaktiviert. Zwischenstände als Git-Tags. | gilt; CI-Grundstufe seit 01.10.2026 |
| D10 | Ein Datum ohne Zusatz setzt den Bearbeitungstag, auch `/morgen`; die Fälligkeit nur mit „fällig“/„bis“, `/bis`, `/fällig`. Eine Wiederholung in der Eingabe setzt die Fälligkeit auf ihren ersten Termin (Ergänzung 02.10.2026). | umgesetzt 3.33.3/3.33.4 |
| D11 | D06 gilt nur für Hinweisblöcke in Seiten; Hinweiszeilen der Ansichten werden über „?“ ein-/ausgeklappt, Zustand gespeichert (U02). | offen (UX1) |
| D12 | Startseite „Ruhig“ mit sieben Kacheln: Heute (zusammengeführt), Gismo, Woche, Zuletzt bearbeitet, Angeheftet, Zeichnungen, Pinnwand-Vorschau; eigene Auswahl bleibt. | umgesetzt 3.33.2 |
| D13 | Eisenhower als Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board; Ziehen ändert Wichtigkeit bzw. Bearbeitungstag, Fälligkeiten werden nie gelöscht. | umgesetzt 3.33.5 |
| D14 | Zwei Hauptansichten: Heute (Tag, Verspätet, Heute fällig, nächste Aufgabe) und Demnächst; Tagesbeginn/-abschluss sind Modi von Heute; interne Kennungen bleiben. | umgesetzt 3.33.6 |
| D15 | Verteilung als Paket mit eingebettetem Python und Tk 9 je Plattform (G26/H-03), nach Stufe 1; das Bauwerkzeug ist eine eigene Abhängigkeitsentscheidung. | offen (Stufe 4) |
| D16 | JSON bleibt Speicherformat; der Speicherweg wird beschleunigt (T2, P08, P09). SQLite nur als Suchindex-Cache (G14); Neubewertung erst über 20.000 Punkten. | gilt |
| D17 | Kein Großumbau: jede neue oder angefasste Fachlogik als Tk-freies Modul mit Unit-Tests; `ListApp` ruft sie auf (G27 schrittweise). | gilt, sieben Module seit 3.33.0 |

**Frühere Antworten, die weiter gelten:**

| Herkunft | Inhalt |
|---|---|
| 25.09.2026 (E-01–E-16) | Format 20 als ein Paket; Suche `Strg/Cmd+O` (`Strg/Cmd+K` bleibt Kalender); Detailbereich zuschaltbar statt Maske ersetzen; eigenes Design „Pixel“; Rückgängig je Aktion; Zwischenstände als Anhänge; Größen 16/32/64/128; nur eigene Palette mitgeliefert; Pixelsymbol als eigene 16 × 16-Zeichnung; Spaltenboard zeigt alle Punkte; `Strg/Cmd+Enter` auf der Pinnwand legt eine Karte nur mit Titel an. Nicht gewählt: Einstieg für neue Nutzer, eigene Felder je Liste |
| 26.09.2026 | Seite und Notiz bleiben getrennt; Seiten vor allem für KI-Berichte; Ordnerarten Ordner, Buch, Notizbuch; Kennungen `de.shaye.glide`/`Shaye.Glide`; Milchglas als Tönung je Kachel |
| 27.09.2026 (E-01–E-13) | Python 3.14 mit Tk 9 als Grundlage; Systemmitteilungen als Option, Vorgabe aus; Vorschauen mit Tk-9-Mitteln ohne Bildbibliothek; Ziehen aus Finder/Explorer über tkinterdnd2; sofort speichern statt verzögert bündeln; keine Schnellerfassung für Seiten; Direktvertrieb zuerst (Windows x64, macOS arm64); kein Ordnerpfad über dem Titel; Titel höchstens 40 Zeichen |
| 28./29.09.2026 | Sicherungen nur bei Änderung plus Tagesstände; unbekannte Listenart öffnet schreibgeschützt, neue Arten nur mit neuer Formatnummer; Umstellung gleich beim Start; Bytecode im Systemcache; keine Unterseiten; Farben: festes Lila für Hinzufügen, Wiederherstellen grün, Importieren neutral, Nachzeichnen lila |
| 30.09.2026 (Q1–Q5) | Reihenfolge schnelle Gewinne → Planen → Wissen → Pixel → Austausch (Q1); keine plattformeigenen Abhängigkeiten, daher kein G07 (Q2); KI-Austausch über Dokumente statt Schnittstelle (Q3); Toolkit-Probe zurückgestellt (Q4, D03); Aufgabenzeilen im Notiztext, die Liste darüber zeigt genau diese Punkte (Q5); verschlüsselte Ablage keine Priorität |
| 01.10.2026 | Notizbücher nehmen im Bereich Notizen datierte Zeichnungen auf; Dokumentationskopien nach Wissensabgleich löschen statt archivieren |
| 03.10.2026 | Archive auf die sieben neuesten Versionen, Fensterbilder auf die drei neuesten; Dokumente gleichen Inhalts zusammenführen, ungenutzte Ordner auflösen |

## Beauftragt

Fortlaufend (Wortlaut des Inhabers): „Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.“

Welche Pakete dazu offen sind, mit Status und Abnahme, steht nur im [Entwicklungsplan, Abschnitt 3](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#3-performance-stufe-0-beauftragt). Neue Funktionen erst nach Auftrag.

## Arbeitsablauf einer Implementierung

1. [Übergabe](../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md), Entwicklungsplan, die betroffenen Abschnitte in [Funktionen](20_FUNKTIONEN.md) und die Codestelle **samt Aufrufern** lesen (Funktionsnamen suchen, nicht Zeilennummern).
2. Baseline mit passender bestehender Prüfung und isoliertem `GLIDE_DATA_DIR`. Der Ausgangsstand liegt in Git; keine Ordner- oder Dokumentkopien.
3. Einen begrenzten Schnitt umsetzen; Fachlogik als Tk-freies Modul (D17). `item_change`, `sidebar_change`, `guarded_structural_change` und `run_modal` verwenden; atomare Speicherung, Sicherungen und Sperren bewahren.
4. Wirkung messen: gleiche Fixtures, Aufwärmlauf, kalte und warme Werte getrennt, Median und p95, Rohwerte. Profiling erklärt Ursachen, belegt aber keinen Gewinn.
5. Bedienweg und Invarianten über echte Bindungen prüfen: Callbackfehler, Undo, Auswahl/Fokus/Scrollen, Größen-, Design- und Schriftwechsel, Tageswechsel, Neustart. Neue Pflichtsuite mit Gegenprobe gegen die Vorversion.
6. `versionswechsel.py`, Quell- und Prüfstand einfrieren, Vollprüfung ([Prüfplan](05_QA_TESTPLAN.md)); ändert sich danach ein ausführbarer Pfad, betroffene Prüfungen und Volllauf wiederholen.
7. Nach grüner Vollprüfung `abgleich_07.py`, Bundle bauen, SHA-256 und Signatur prüfen, Showcase ausliefern. CHANGELOG, Funktionen, QA-Bericht, Entwicklungsplan und Übergabe nachführen. Manuelle Plattformabnahme bleibt ausdrücklich offen.

**Abschluss:** Erledigt ist eine Änderung erst, wenn `07_Python-Versionen` und das Bundle den geprüften Stand tragen.

## Nachläufe ohne neue App-Version

Reine Dokumentations-, Ablage- oder Werkzeugarbeit bekommt einen datierten Nachweis unter `tests/qa-<aktuelle Version>/<Thema>_<Datum>/` (README und `ergebnis.json`) und keine künstliche Produktionsversion. Geprüft werden CI-Grundstufe, Werkzeugtests und unveränderte App-/Lieferhashes; eine frühere Vollprüfung gilt für ihren eingefrorenen Stand und wird nicht als Lauf mit neuen Werkzeugen ausgegeben. Regeln für Dokumente: [Dokumentenpflege](DOKUMENTENPFLEGE.md).
