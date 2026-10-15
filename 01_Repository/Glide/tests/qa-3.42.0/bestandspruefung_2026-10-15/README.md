# Bestands- und Dokumentationsprüfung vor dem UI-/UX-Paket

Stand 15.10.2026 · Glide 3.42.0 · lokale Lieferbasis `05483a8` · keine Feature-Umsetzung

Auftrag: vor der künftigen Claude-Ausführung Dokumentation, Version, Aktualität, Vorlagen und alle Projektbestandteile prüfen, überholte Dateien aktualisieren oder entfernen und anschließend einen Claude-Startprompt formulieren. Diese Prüfung ist ein Dokumentations-/Werkzeugnachlauf; App-Version und Datenformat werden nicht geändert.

## Umfang und tatsächlicher Ausgangspunkt

- Vollständige Dateiinventur: 3.019 Dateien / 1.051.504.292 Bytes ohne `.git`-Inhalt, einschließlich ignorierter Dateien, Builds, importierter Skillquellen und separater Claude-Arbeitskopien. Der Hauptcheckout umfasst 1.603 Dateien / 348.497.448 Bytes; die separaten Arbeitskopien werden getrennt bewertet, keine pauschale Löschung aufgrund ihrer Größe.
- Alle Projektbereiche erfasst: Wurzel/Arbeitsregeln, `.github`, Arbeitsvorbereitung, Quellbaum/Tests/Dokumente/Packaging, 05-Showcase, 07-Lieferung/Archiv, Grafikmaster und Skills. Automatische Stand-/Linkprüfung durch semantische Dokumentprüfung und tatsächliche Bestands-/Manifestprüfung ergänzt.
- Lokaler Git-HEAD `05483a8c078bf669b09cb4a427f76c011ed828ec`, Zweig `codex/glide-fortsetzung-3410`: gelieferte 3.42.0-Basis. Nach `git fetch --no-tags origin main`: Upstream `a7f80b828306a6f7e75b0cab593e6f536938e443`, 13 Commits voraus, kein lokaler eigener Commit dazwischen. Upstream ergänzt bereits 4.0-Zugänglichkeit und Packaging, trägt aber weiterhin VERSION 3.42.0.
- Diese Upstream-Vorbereitung wurde während der Vorabprüfung nicht in die gelieferte Appbasis integriert. Eine bloße Versionsgleichheit beweist keinen gleichen Quell-/Lieferstand. Vor der vollständigen Feature-Ausführung aktuelle Upstream-Änderungen mit den lokalen Dokumentkorrekturen und Referenzen kontrolliert integrieren, anschließend eine neue Baseline prüfen.

## Inhaltliche Korrekturen

| Bereich | Gefundener veralteter Inhalt | Korrigierter Stand |
|---|---|---|
| Regeln/Indizes/Übergabe | Entscheidungsregister nur D01–D17 bzw. D01–D48 | D01–D49, D49 unter dokumentiertem Korrekturvorbehalt; neue Produktentscheidungen ab D50 |
| QA-Index/Identitätsregister | geprüfte Lieferung nur bis 3.35.0 bzw. 3.38.0 | gelieferte Basis 3.42.0 mit tatsächlichen lokalen Prüfgrenzen |
| D44/Plan/Analyse/Markt/manuelle Prüfung | Paket 7 noch offen, native 3.39-/3.41-Matrix noch ausstehend | Pakete 1–7 und FP-00 geliefert; Paket 8 vorbereitet, Menschenabnahme getrennt offen |
| Git-/Workspace-Übergabe | veralteter Main- und sitzungsgebundener Arbeitsstand | lokal `05483a8`, Upstream `a7f80b8`, 13 zusätzliche Commits; private Vorbereitungen nicht als hier verifiziert ausgeben |
| Archivübersicht | aktuelle Version 3.35.0, Archiv 3.33.17–3.34.0 | sechs Archivfassungen 3.37.0, 3.38.0, 3.39.0, 3.39.1, 3.40.0, 3.41.0 plus aktuelle 3.42.0 |
| Vorlagenpraxis/05-Index | nicht mehr vorhandene Nutzerdateien aus 3.30.0/Releaseplanung 3.35.0, Teilpayloadformat 18 | aktuelle kanonische Dateien, Releaseplanung 3.42.0, Aufgabenformat 25 und Vorlagencontainerformat 2 |
| Showcase | Bearbeitungstag 01.10.2026, falscher heutiger Originalbildort, alte UI-Begriffe/Richtungswahl | Manifesttag 13.10.2026, Originale ausschließlich `tests/fixtures/showcase/bilder`, Heute/Notizbuch; Fixture und Liefer-README bytegleich |
| Architektur/Arbeitsbegleiter | Tk ausschließlich 8.6, SVG unmöglich, ungeglätteter Logo-Rückfall, Ein-Datei-Codeprompt | Python 3.14/Tk 9, geglätteter Tk-8.6-Rückfall, modulare Architektur; doppelte Assetlisten/überholte Einbauprompts zusammengeführt |
| QA-Ablauf/DND | alte Testumfänge; Windows-DND pauschal ungeprüft | lokale Basis 90 Suiten/638 Fachlogiktests; Windows-Paket-Laden belegt, physisches Ziehen und nicht belegte Linux-Proben getrennt offen |
| Produktdatenblatt/Grafikmaster | Entwurf 3.33.6, alte Herkunfts- und Assetangaben | technischer Entwurf 3.42.0 ohne Releasefreigabe; aktuelle Master, Herkunft und verbliebener alter Affinity-Stand klar gekennzeichnet |
| Dokumentations-Werkzeugtest | feste Pfadreihenfolge setzt POSIX-Sortierung voraus | Bestand mit `assertCountEqual` prüfen; Umfang/Unterverzeichnis bleiben geprüft, Laufzeitcode unverändert |

Historische Messwerte, rote Vorläufe, Migrationsfixtures, direkte Nutzeraufträge und Entscheidungswortlaut wurden nicht nachträglich auf aktuelle Versionen umetikettiert. Eine reine Standzeilenprüfung hatte mehrere dieser Fehler nicht erkannt, insbesondere die gepflegte Archivübersicht.

## Vorlagen, Daten, Ressourcen und Pakete

- Version 3.42.0, Aufgabenformat 25, Einstellungen/Vorlagencontainer 2.
- `07_Python-Versionen`: 63 Code- und 146 Ressourcen-/Vendordateien bytegleich zur lokalen Quelle.
- Vorlagen: 16 portable Vorlagen reproduzierbar und mit Payloadversion 3.42.0/Format 25; vier integrierte Notizbuchvorlagen ergeben 20, Showcase ergänzt zwei auf 22.
- Alle 20 aktuellen bzw. bewusst historischen Backupfixtures und Format-4–25-Referenzen vorhanden. Alte Migrationsbelege sind notwendige Prüfbestandteile.
- Showcase: sechs Lieferdateien, drei Manifestdateien und sechs Originalbild-Prüfsummen korrekt; freigegebene Logo-/Appsymbolmaster mit ihren sechs Laufzeitkopien verglichen.
- Windows-Paket: 102/102 Dateien manifest- und hashgleich. Acht Bauinput-Textressourcen unterscheiden sich vom Windows-Arbeitsbaum ausschließlich LF/CRLF; kein Inhaltsdrift.
- **Lokales Mac-Bundle unvollständig:** 327/330 Manifestdateien vorhanden und hashgleich. Es fehlen `Contents/Frameworks/Python.framework/Versions/3.14/Python`, `.../Resources/Info.plist` und `.../_CodeSignature/CodeResources`. Die früheren nativen Mac-Liefer-/Signaturnachweise bleiben historische Belege, bestätigen aber nicht die heutige Windows-Kopie. Mac-Reparatur/Neubau mit tatsächlicher Paket-/Signaturprüfung bleibt vor einer neuen Mac-Lieferung erforderlich.

Die detaillierte Ressourcenprüfung steht in [ressourcenpruefung.json](ressourcenpruefung.json).

## Bereinigung und bewusst erhaltener Bestand

[Bereinigungsmanifest](bereinigung.json) enthält Pfade, Größen, SHA-256 und Gründe. **Fünf Dateien / 67.421 Bytes entfernt:** lose bytegleiche Design-Skillkopie, zwei unreferenzierte alte `.tmp`-Gegenproben, leere `skills-main/.pl` und doppelte alte Affinity-SVG. Aktiver Skill, zugehörige MIT-Lizenz und aktuelle SVG-Master bleiben erhalten.

**Drei weitere geprüfte Löschungen wurden automatisch blockiert:** zwei regenerierbare `.pyc`-Dateien und der nicht auf D45 nachgeführte alte `Glide-Logo.af`-Stand. Sowohl der gebündelte als auch der vereinfachte Befehl mit ausdrücklich benannten Dateipfaden wurde mit „blocked by policy“ abgewiesen; keine weitere Begründung wurde geliefert. Diese Dateien sind noch vorhanden, ebenso der leere Ordner `docs/diagnosen`. Keine vollständige Bereinigung behaupten und die Richtlinie nicht durch einen anderen Löschweg umgehen.

Erhalten bleiben:

- 28 offene Nutzer-Screenshotreferenzen mit Manifest; unverändert, lokal vom Git-Upload ausgeschlossen.
- Importierte `skills-main`-Quellen mit 14 eigenständigen Skills und Lizenz; keine pauschale Installation oder Löschung. B20 integriert passende Inhalte später neutral.
- Erwartete App-/Showcase-/Lizenzlieferkopien, freigegebene Grafikmaster, D45-Abnahmetafeln und der vom Synchronisationswächter benötigte alte Logo-Sentinel.
- Historische QA-/Formatbelege innerhalb der Regeln. Hauptcheckout einschließlich ignorierter Dateien: keine abgelaufenen Archive oder alten QA-Bilder; sieben Versionsstände, keine aktuellen QA-Fensterbilder. Kürzwerkzeug meldet null Kandidaten.
- Separate Claude-Arbeitskopien und ihre Git-Metadaten. Zwei lokale Arbeitskopien enthalten zusammen etwa 703 MB. Ihre Verweisdateien nennen einen früheren Benutzerpfad und `git worktree list` meldet dazu alte Pfade als `prunable`; das beweist keine sichere Löschbarkeit. Keine Worktree-/Stash-/Branchbereinigung aus diesem Auftrag ableiten.

## Abschlussprüfung und Ausführung

Maschinenlesbare Zusammenfassung: [ergebnis.json](ergebnis.json). Die [CI-Grundstufe](grundstufe/ergebnis.json) wird nach den Korrekturen erneut ausgeführt, außerdem Stand-/Linkprüfung für neue und aktive Archivdokumente, unveränderte App-/Lieferhashes, Screenshotmanifest und Dateireste geprüft. Die vorherige rote Grundprüfung im Prompt-Nachweis bleibt als historischer Lauf erhalten.

Nach Abschluss dieser Vorabprüfung wird der zusätzliche Claude-Startprompt im bestehenden UI-/UX-Paket abgelegt. Das Formulieren startet keine App-Umsetzung und führt keinen Commit/Push/Merge aus. Der spätere Ausführungsauftrag umfasst den vollständigen vorhandenen Prompt, die bereinigten Quellen und die hier ausdrücklich genannten Startbedingungen und Grenzen.
