# Schutzrunde WA-27–WA-30 – Nachprüfung und Fortsetzung

Stand 18.10.2026 · Entwicklungskandidat auf `9ec474b` mit FP-01 · Version 3.43.1 und Datenformat 25 unverändert · keine Lieferung

Der Inhaber beauftragte die Fortsetzung der durch das Tokenlimit unterbrochenen Claude-Arbeit und die Prüfung ihres tatsächlichen Abschlusses. Die Umsetzung liegt uncommittet in der getrennten Arbeitskopie `jolly-noether-593099`. Die Hauptarbeitskopie auf `c0252ba` mit 22 Dokumentänderungen und einem Analyseordner bleibt erhalten; es wurde nichts dorthin zusammengeführt.

## Gefundener Ausgangsstand

Die vier Tk-freien Module, deren Unit-Tests, App-Adapter und die Pflichtsuite waren vorhanden. Die vorhandenen sieben Schutzfälle und 751 Unit-Tests bestanden auch bei der Wiederholung unter Windows. Ein vollständiger dauerhafter Nachweis und der Abschluss der roten Prozessgegenprobe fehlten. [Ausgangsmanifest](ausgangsmanifest.json), [wiederholte Claude-Pflichtsuite](baseline_claude.json).

Drei ergänzte Gegenproben waren im Claude-Entwurf rot:

- Export, Backup, Markdown, Druck und Bestandsvergleich übergingen teilweise eine gescheiterte Editorübernahme und verwendeten den alten Bestand.
- `dirty=True` aus einem vorherigen Schreibfehler erlaubte den Seitenwechsel auch mit anderem, noch nicht übernommenem Text.
- Nach erfolgreichem Zwischenspeichern im Wächter schrieb dessen Rückweg neue JSON-/Verlaufswerte; die Datei war danach nicht bytegleich zum Stand vor dem Vorgang.

Die konkreten roten Ergebnisse stehen in [nachpruefung_vor_korrektur.json](nachpruefung_vor_korrektur.json). Weitere Vorläufe bleiben als solche erhalten; sie sind keine Abschlussnachweise.

## Fertiggestellte Korrekturen

| Auftrag | Ergebnis |
|---|---|
| WA-27 / A32 | Stapelmarke bleibt auch bei 20 Schritten erhalten; der Wächter prüft vor jedem Schreiben auf fehlende IDs, wertet den Rückweg aus und meldet dessen tatsächliches Ergebnis. Nach einem späten Abbruch stellt der interne atomare Rückweg die Originalbytes wieder her. Bereits vorher ungespeicherte Änderungen bleiben erkennbar. |
| WA-28 / A34 | Lesen/Normalisieren und Übernehmen/Darstellen sind getrennt. Tcl-/Darstellungsfehler nach erfolgreichem Lesen behalten den Bestand und erzeugen weder eine Schadenskopie noch einen leeren schreibfähigen Bestand. Echte JSON- und neuere Formatfehler behalten ihren bisherigen Schutzweg. |
| WA-29 / A35 | Gemeinsamer True/False-Vertrag beider Editoren; Navigation prüft tatsächliche Inhaltsübernahme. Ausgabe-/Backupwege stoppen vor Dateiauswahl oder Ausgabe beziehungsweise melden einen Fehler an ihren Aufrufer. Inventar der direkten und gemeinsamen Aufrufer: [aufrufer.json](aufrufer.json). |
| WA-30 / A36 | Defekte/unlesbare Sperre öffnet schreibgeschützt mit bewusster Übernahme. Exklusiver Erwerb umfasst auch verwaiste Sperren, mit automatisch vom Betriebssystem freigegebener kurzer Erwerbssperre. Eine überholte Bestätigung überschreibt keine inzwischen gültige Sperre. Einstellungen, Fenstergröße und Vorlagen nutzen die gemeinsame Schreibschranke; fehlende Sperren werden neu angelegt oder verhindern das Schreiben. |

Der Prozesstest verwendet Bereitschafts- und Endfreigaben statt einer geschätzten Importzeit. Er prüft fehlende und verwaiste Sperren in jeweils drei Runden und hält beide Prozesse bis zur Auswertung am Leben. Ein schreibgeschützter Zweitstart mit laufendem Fokus beendet sich ohne Einstellungsänderung. Der künstliche Interpreterneustart der Pflichtsuite löst vor dem Abbau seine Bindungen und Timer; Fehler während aktiver Testschritte bleiben prüfwirksam.

## Prüfungen

Die maschinenlesbaren Ergebnisse enthalten Quellhash, Rückgabecode und Laufzeit. Ausschließlich künstliche Daten; `GLIDE_DATA_DIR` wird vor dem Import gesetzt. Plattform: Windows, Python 3.14.7.

- [Pflichtsuite](pflichtsuite.json): zehn Fälle, einschließlich der drei ergänzten Regressionen.
- [Betroffene Bestandssuiten](bereiche.json): Schutzrunde, Wiederholen, Datenintegrität, Editorabbau, Vorlagen, Notion/Einzelrestore und Seiten.
- [Units und Werkzeugtests](units.json), [CI-Grundstufe](grundstufe.json).
- [Rote Gegenprobe gegen den unkorrigierten Stand](gegenprobe_9ec474b.json).

**Abschluss:** [Ergebnis und Prüfstände](ergebnis.json), [Kandidatenmanifest](kandidat_manifest.json). App-SHA256: `f74af723e3fe1fc18aae5beafcef3d026a3a9c39d8eb16c90b68fb3ae7ddec26`.

| Prüfung | Ergebnis und Geltungsbereich |
|---|---|
| Schutzrunde | **10/10 grün auf dem Endstand**, einschließlich unverändert schreibgeschützter Ausgabe und sechs synchron gestarteter Prozesspaare |
| Gegenprobe `9ec474b` | **10/10 erwartete rote Fälle**; Original-Apphash `61f7b963…` bestätigt |
| Fachlogik | **754/754 grün auf dem Endstand** |
| Werkzeugtests | **152/152 grün auf dem Endstand** |
| Betroffene Bestandssuiten | **6/6 grün während der Entwicklung**: Wiederholen (9 Fälle, einschließlich 10.001 Punkten), Datenintegrität, Editorabbau, Vorlagen, Notion/Einzelrestore und Seiten |
| CI-Grundstufe | **Exitcode 0, 19 Schritte, kein fehlgeschlagener Schritt**; ein erwarteter Hinweis auf den nicht abgeglichenen Lieferstand. Gelaufen vor der letzten begrenzten Flush-Präzisierung; danach Schutzsuite, Units und Formalprüfungen auf dem Endstand erneut bestanden. |
| Abschließende Formalprüfung | Syntax, Versionskonsistenz, Dokumentverweise, Standprüfung und `git diff --check` bestanden |

Der Bereichslauf enthält noch den roten Vorlauf des künstlichen Interpreterneustarts. Er wurde durch den endgültigen grünen Schutzlauf ersetzt, ohne den Vorlauf umzudeuten. Die Bereichsläufe sind gezielte Entwicklungsprüfungen nach D51; eine eingefrorene Vollprüfung wurde nicht beauftragt oder behauptet. Die letzte zusätzliche [rote Schreibschutzprobe](schreibschutz_ausgabe_vorlauf.json) führte zur Präzisierung: Nachweislich übernommener unveränderter Inhalt liefert auch ohne Schreibrecht Erfolg und bleibt lesend exportierbar; unübernommener Inhalt wird weiter abgewehrt.

## Gegenprüfung der Hauptarbeitskopie

[Hashvergleich](hauptkopie_unveraendert.json): Sämtliche 44 zu Beginn geänderten/neuen Dateien sind erhalten und inhaltlich unverändert; HEAD bleibt `c0252ba`. Das umfasst die 22 Dokumentänderungen und die Dateien des einen neuen QA-Ordners. [Erneute Prüfungen](hauptkopie_pruefungen.json): Syntax, Versionen, Dokumentverweise und Bytegleichheit zum vorhandenen 07-Stand bestanden. Apphash weiterhin `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`.

[Linkprüfung](hauptkopie_links.json): 62 Markdown-Dateien, 795 lokale Links und 125 Anker geprüft; einziger Fehler ist der bekannte fehlende historische Nachweis `qa-3.42.0/bestandspruefung_2026-10-15/grundstufe/ergebnis.json`. Die Zählweise dieser erneuten Prüfung unterscheidet sich von der früheren Prüfung; der Fehlerbefund stimmt überein. Historische Nachweise wurden nicht umgeschrieben.

[Redaktionelle Stichprobe](redaktion_stichprobe.json): Die im Abschlussbericht genannten Wortklebungen und falschen Kennungen kommen in Plan/Marktdokument nicht mehr vor. Die 157 und 13 Ersetzungen sind historische Protokollzahlen aus `gegenpruefung.json`; die damalige kuratierte Ersetzungsliste und externe Sicherung wurden hier nicht unabhängig rekonstruiert. Eine Wörterbuchprüfung sämtlicher Wörter wurde nicht durchgeführt.

## Offene Tore

Kein Versionswechsel, keine Datenformatänderung, kein 07-/Showcase-Abgleich, kein Paketbau und keine Lieferung. Keine eingefrorene Vollprüfung oder vollständige native Plattformmatrix. Mac-/Linux-/Reader-/DPI-/Mehrmonitor- und Menschenabnahme bleiben offen. Die lokale Prozesssperre ersetzt keinen verteilten Konsens zwischen zwei Rechnern über Cloud-Abgleich. Keine Aussage über die natürliche Häufigkeit der per Fehlerinjektion geprüften Fehler.

Kein Commit, Push oder Merge. Die Integration des Kandidaten mit den uncommitteten Analysedokumenten der Hauptarbeitskopie gehört zu einem gesondert beauftragten Zusammenführungsschritt. Die Schutzrunde trifft keine neue Produktwahl und erklärt keine Veröffentlichung für freigegeben.
