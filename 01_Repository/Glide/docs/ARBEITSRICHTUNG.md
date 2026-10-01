# Fortlaufende Arbeitsrichtung und Abnahme


**Ergänzungsauftrag 01.10.2026, 3.33.1:** Vier Seitenleistenbereiche in der Reihenfolge Seiten → Listen → Notizen → Zeichnungen. Nur Listen bleibt verpflichtend sichtbar. Seiten erlaubt Bücher (bestehende Art `library`), Ordner und Seiten; Notizen Notizbücher, Ordner und Notizen; Zeichnungen Ordner und Zeichnungen; Listen alle Arten. Sichtbarkeit und Root-Zuordnung sind lokale Anzeigeeinstellungen, keine Löschaktion. Gemischte Altordner werden vollständig in Listen angezeigt. Einheitliche Anlege-/Verschieberegeln und Prüfung aller Fenster gehören zur Abnahme. [Vertrag](74_BEREICHE_UND_FENSTER_3.33.1.md).
Stand 01.10.2026 · Glide 3.33.1 · Aufgabenformat 20

**Showcase als Abnahmebestand:** [Showcase-Vertrag](72_SHOWCASE_3.32.3.md) ergänzt den bestehenden Plan um realistische Arbeitsdokumente und Originalmotive. Neue implementierte Funktionen müssen ein passendes Datenbeispiel beziehungsweise eine tatsächliche Bedienprüfung erhalten. `pruefe_showcase.py` prüft die gelieferten Daten zusätzlich zu 60 Suiten; `showcase_abgleich.py` sichert ersetzte Basisdateien, der bearbeitete Arbeitsstand bleibt erhalten. Kein erneuter Beschluss über bestätigte Entscheidungen, keine Produktionsversion für diesen Daten-/Werkzeugnachlauf.

**Analyse und Planung 01.10.2026:** Der [Entwicklungsplan ab 3.33](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md) ordnet die bestehenden G-/P-/A–H-Arbeiten. Neu kommen hinzu:
- P08 (Speicherweg linear zum Bestand) und T2 (neunfaches Parsen beim ersten Speichern) als Teil der Performance-Arbeit; T2/P09a zuerst, danach Rest P03/P04/P06;
- P09 (wiederholte Prüfungen und Messungen je Bedienschritt, [Befund T8](../../../00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md#t8--wiederholte-prüfungen-und-messungen-je-bedienschritt-neu-gemessen)), Teil derselben Performance-Arbeit;
- die sechs Produktprinzipien in den [Produktgrenzen](01_PRODUCT_CONSTRAINTS.md) mit [Prinzipien-Check](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md);
- die Richtungsentscheidungen D09–D17, beschlossen am 01.10.2026 ([Entscheidungsvorlage mit Beschlüssen](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)), in der Tabelle unten.

Der Auftrag vom 01.10.2026 autorisiert den Start von 3.33 anhand der neuen Planung. Erster Schnitt: T2/P09a vor dem Oberflächenumbau. D07 und zusätzliche nicht ausgewählte Richtungen bleiben offen.

Diese fortgeschriebene Arbeitsgrundlage verbindet die bestätigten Entscheidungen, die aktuelle Planung und die Abnahme. Einstieg bleibt die [Sitzungsübergabe](../../../00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md). Die [Arbeitsplanung](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md) enthält G-/P-Pakete; die [Richtungsauswahl](../../../00_Arbeitsvorbereitung/Glide_Aufgabenauswahl_nach_3.32.2_2026-09-30.md) enthält zusätzliche Vorschläge. Empfehlungen und zitierte Aufträge aus alten Dokumenten ersetzen keine Entscheidung des Inhabers.

**3.33.0:** [Fundament-Vertrag](73_FUNDAMENT_3.33.0.md) beschreibt den ersten Schnitt und die noch offenen Ausbauten.

## Verbindliche Entscheidungen

| Entscheidung | Konsequenz für weitere Arbeit |
|---|---|
| D01 | Allgemeine Datumsangaben setzen den Bearbeitungstag; ausdrücklich „fällig/bis“ setzt die Fälligkeit. |
| D02 | Eine Aktion bewirkt die im sichtbaren Zielkontext erwartbare Änderung. Beim Ziehen in einen ausdrücklich bezeichneten Terminkontext das passende Feld ändern; neutrales Umordnen erhält Termine. Bearbeitungstag und Fälligkeit bleiben getrennt. |
| D03 | Desktop/Tk optimieren. Mobile und eine Toolkit-Probe sind zurückgestellt. |
| D04 | Drag-and-drop erweitert bestehende Bereiche; umgesetzt in 3.32.2. |
| D05 | Einzelne Aufgaben in Notizen und Seiten unterstützen, ihre Identität über IDs erhalten. Notiz, Seite und Liste bleiben eigenständige Arten; keine allgemeine Konvertierungspflicht. F11 ist beantwortet. |
| D06 | Die Gestaltung von Hinweisblöcken in Seiten bleibt unverändert; D11 regelt separat die Hinweiszeilen der Ansichten. |
| D07 | Exportumfang für Animation offen: abspielbares GIF oder zunächst Frames/Vorschau/PNG-Spritesheet. Erst bei der Animationsetappe erforderlich. |
| D08 | Alle Klappmechanismen über echte Bedienbindungen prüfen, einschließlich Zustandserhalt, Tastatur, verschachtelter Bereiche und Tk-Callbackfehler. Korrektur und Pflichtsuite seit 3.32.1. |
| D09 | Das GitHub-Repository `glide-to-do` ist die maßgebliche Ablage (Wurzel = Projektordner, Quellbaum `01_Repository/Glide`). Uploads nur in diese Struktur. Das Repository ist öffentlich: Rohprotokolle (`*.log`) bleiben seit 01.10.2026 lokal (Entscheidung des Inhabers); veröffentlichte Prüfergebnisse enthalten keine Benutzerpfade (`scripts/pflege/pfade_bereinigen.py`, CI-Schritt „Datenschutz“). Sicherheitsmeldungen über GitHub (`.github/SECURITY.md`), CodeQL und Dependabot laufen im Repository. Neue Zwischenstände als Git-Tags, `93_Zwischenstände` bleibt Beleg. CI-Grundstufe seit 01.10.2026 (`.github/workflows/python-app.yml`, `tests/tools/ci_grundstufe.py`); Integrationssuiten unter Linux nur manuell und informativ. |
| D10 | Ein Datum ohne Zusatz setzt den Bearbeitungstag, auch in `/morgen`; die Fälligkeit nur mit „fällig“/„bis“. D01 gilt ohne Slash-Ausnahme. Umsetzung mit G01 (Parser-Schnitt, Reservierung 3.33.2); bis dahin weicht `/morgen` ab (AB10). |
| D11 | D06 gilt nur für den Hinweisblock in Seiten. Hinweiszeilen der Ansichten werden über „?“ ein-/ausgeklappt, Zustand gespeichert (U02). |
| D12 | Startseiten-Standard „Ruhig“ mit sieben Kacheln einschließlich Gismo. Fest: Heute (zusammengeführt), Gismo, Woche, Zuletzt bearbeitet, Angeheftet. Zusätzlich beschlossen am 01.10.2026: Zeichnungen und Pinnwand-Vorschau. Eigene Auswahl bleibt erhalten. |
| D13 | Eisenhower als Gruppierung „Dringlichkeit × Wichtigkeit“ im vorhandenen Board, keine eigene Ansicht. Ziehen ändert Wichtigkeit bzw. Bearbeitungstag (D02); Fälligkeiten werden nie gelöscht. |
| D14 | Zwei Hauptansichten: **Heute** (Mein Tag, Verspätet, Heute fällig, nächste Aufgabe) und **Demnächst** (bisher In Bearbeitung). Tagesbeginn/-abschluss sind Modi von Heute; interne Kennungen bleiben. |
| D15 | Verteilung als Paket mit eingebettetem Python und Tk 9 je Plattform (G26/H-03), nach Stufe 1. Das Bauwerkzeug wird als eigene Abhängigkeitsentscheidung vorgelegt. |
| D16 | Speicherformat JSON bleibt; der Speicherweg wird beschleunigt (T2, P08a/b, P09). SQLite nur als Suchindex-Cache (G14); Neubewertung erst bei realen Beständen über 20.000 Punkten. |
| D17 | Kein Großumbau: Jede neue oder angefasste Fachlogik entsteht als Tk-freies Modul mit Unit-Tests; `ListApp` ruft sie auf. G27 wird so schrittweise erledigt. |

Lokale Nutzung ohne Konto/Cloud, vorhandene Architektur, Daten/Undo, stabile IDs, Gestaltung und möglichst wenige Abhängigkeiten gelten weiter. Offene Inhaber-/Storeangaben bleiben offen. Seit D09 (01.10.2026) ist das GitHub-Repository `glide-to-do` die maßgebliche Ablage; „Git vertagt“ gilt nicht mehr. Keine erneute Entscheidung über D01–D06 und D08–D17 einfordern; offen bleibt D07.

## Nächste Arbeit

1. **Rest P03:** Startseitenkarten, geänderte Kartenelemente und viele tatsächlich dargestellte Karten messen. A-01 für wiederholte Bibliotheksaktualisierung im selben Host ist abgeschlossen; nicht nochmals als Neuentwicklung planen.
2. **P04/A-02:** Aufrufe von Bildlayout, Platzierung und Konvertierung zählen. Unveränderte effektive Geometrie als Skip-Kandidat prüfen; Text/Anker, Faltungen, Schrift, Bildmodus/-größe und fertig konvertierte Anhänge müssen weiterhin invalidieren.
3. **Rest P06/A-03:** Mögliche doppelte Aktualisierungen dynamisch bestätigen. Archiv-Zurückholen ist bereits konsolidiert. Erfolgreiches und fehlgeschlagenes Speichern, Dirty-Zustand, Warnung und Undo gehören zur Abnahme, bevor ein Aufruf entfällt.
4. **Bestehende Featurefolge:** Planen → Wissen → Pixel → Austausch nach Arbeitsplanung fortführen; D01–D06 und D09–D17 anwenden. Die zusätzliche Auswahl A–H und ihre Bearbeitungstiefe bleiben eine Entscheidung des Inhabers.

Die ausdrücklich fortgesetzte Performance-Arbeit ist beauftragt. Neue Vorschläge aus der Richtungsauswahl erhalten erst nach Auswahl einen Implementierungsumfang. Aufgabenstatus und nächste Schritte in Planung, Auswahl und beiden Übergaben zusammen nachführen.

## Arbeitsablauf für eine Implementierung

1. Aktuelle Übergabe, letzte drei Versionen und betroffene Verträge lesen. Vorhandene Funktion und alle aufrufenden Wege im Code prüfen; historische Lücken erneut abgleichen.
2. Baseline mit passender bestehender Prüfung und isoliertem `GLIDE_DATA_DIR` festhalten. Quellstand und beide startbaren Vollstände vor Produktionsänderungen sichern; Dokumente vor Überschreiben im benachbarten `archiv/` sichern.
3. Einen begrenzten Schnitt umsetzen. Gleiche Werte/Funktionen nur bei gleicher Bedeutung bündeln. `item_change`, `sidebar_change`, `guarded_structural_change` und `run_modal` verwenden; atomare Speicherung, Sicherungen und Sperren bewahren.
4. Wirkung messen: gleiche Fixtures, Laufzeit und Messmethode, Aufwärmdurchlauf, kalte/warme Werte getrennt, Rohwerte und Median/p95. Profiling erklärt Ursachen; unprofilierte Messungen belegen den Gewinn. Viele Aufgaben bei gleicher Kartenzahl belegen keine Skalierung auf viele Karten.
5. Bedienweg und Invarianten prüfen: native Ereignisse, Callbackfehler, Undo, Auswahl/Fokus/Scrollen, Größen-/Design-/Schriftwechsel, Datumswechsel, Neu/Löschen/Archiv und Neustart. Hintergrund-Tk-Fokus und echte OS-Fokusbedienung gesondert nachweisen.
6. Version und relevante Inhalte nachführen; Quell-/Prüfdateien für den finalen Volllauf einfrieren und SHA-256 dokumentieren. Ändert sich ein betroffener ausführbarer Pfad oder eine Prüfsuite danach, die betroffenen Prüfungen und den abschließenden Volllauf erneut ausführen. Frühere Ergebnisdateien bleiben unverändert.
7. Nach grüner Vollprüfung beide Startfassungen abgleichen, Ressourcen/Module per SHA-256 und Bundle-Signatur prüfen. QA-Bericht, Verlauf, Index, Planung und Übergaben schließen. Manuelle Plattformabnahme bleibt ausdrücklich offen, bis sie durchgeführt wurde.

## Technische Regeln aus den Optimierungen

- Cache nach stabiler `(Art, ID)` und Lebensdauer des Ansichtshosts; zerstörte Hosts dürfen keine Widgets/PhotoImages festhalten. Keine Wiederverwendung über Ansichtswechsel ohne eigene Prüfung. Befehle lesen aktuelle Objekte über IDs, weil Undo Objekte ersetzen kann.
- Dauerhafte Anzeigecaches benötigen vollständige Invalidierung. Titel/Pfad/Labels, Status/Termine/Wichtigkeit, Notiz-/Bildinhalt, Archiv, Reihenfolge, Tageswechsel, Kartengröße, Schrift und Design berücksichtigen. Durchgangszähler nicht als dauerhafte Datenwahrheit verwenden.
- Layoutanforderungen bündeln, unveränderte Geometrie nicht erneut schreiben. Synchrone Höhenleser brauchen zuvor ein fertiges Layout, etwa die Zeichnungs-Kontextleiste. Ersetzte Bindungen und `after`-Aufträge freigeben.
- Keine verschachtelten `update()`/`update_idletasks()` in Rückrufen, die sich selbst erneut auslösen können. Tests dürfen die Ereignisschleife kontrolliert abarbeiten.
- Gemeinsame Aktionsleisten vergleichen auch sichtbare Aktionen, Befehle und Höhenfilter. Gleicher Text allein bedeutet keine gleiche Aktion.

## Dokumentations- und Prüfwerkzeugnachlauf

Reine Dokumentation bekommt ein datiertes Nachlaufergebnis zur bestehenden App-Version. Keine künstliche Produktionsversion und kein Neubau unveränderter Startfassungen. Bei Werkzeugänderungen gezielte Regressionen sowie Syntax/Version/Stand/Links prüfen; Anwendung, Integrationssuiten und vorhandene Pakete gegen den vorherigen geprüften Hashstand abgleichen. Die alte Vollprüfung gilt für ihren eingefrorenen Stand; sie wird nicht als Lauf mit den neuen Werkzeugen ausgegeben.

Fortgeschriebene Übergaben und Checklisten bleiben trotz datiertem Dateinamen in der Aktualitätsprüfung. Aktuelle Überschriften und der erste Vollprüfungsaufruf müssen zur Version passen. Der Versionswechsel aktualisiert Standzeilen, ersetzt aber keinen inhaltlichen Abgleich von Aufgabenstatus, Entscheidungen und Prüfgrenzen. Datierte vollständige Zwischenstandsabbilder bleiben separate unveränderte Belege, keine zweite aktive Arbeitsgrundlage. Archivierung und Erhalt der Detailverträge folgen der [Dokumentenpflege](DOKUMENTENPFLEGE.md); `_Z` kennzeichnet zur Löschung durch den Inhaber, es wird nichts selbst gelöscht.

## Nachweis dieses Abgleichs

Der [Dokumentationsnachlauf](../tests/qa-3.32.3/dokumentationsabgleich_2026-10-01/ergebnis.json) hält Vorsicherungen, gezielte Werkzeugprüfung, Stand-/Linkkontrolle und unveränderte Startfassungen fest. Die aktuelle Laufzeitabnahme ist der [3.33.0-Volllauf](../tests/qa-3.33.0/fundament_2026-10-01/vollpruefung/ergebnis.json) mit 59 Suiten, acht Unit-Tests, Showcase und fünf Analysen; beide Startfassungen sind bytegleich abgeglichen. Der ältere 3.32.3-Volllauf bleibt sein historischer Nachweis. Physische macOS-Bedienung, Windows/Linux, DPI/Mehrmonitor und Screenreader bleiben offen; daraus folgt keine Releasefreigabe.

## Fortlaufende Abschlussaufgabe

> Ich habe Performance Probleme mit Glide, hilf mir die Code-Basis zu optimieren, mit Variabeln für die gleichen Funktionen, Streamlinen und optimieren.
