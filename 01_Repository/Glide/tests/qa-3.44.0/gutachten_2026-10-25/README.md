# Einordnung des Sicherheits- und Architekturgutachtens – 25.10.2026

Dokumentationsnachlauf für Glide 3.44.0 / Aufgabenformat 26 mit lokalem D55-Kandidaten. Auftrag: den eingereichten Bericht über die aktuelle Codebasis analysieren und einordnen, in die aktuelle Dokumentation einarbeiten und diese aufräumen. Fachliche Ergebnisse stehen ausschließlich in [Analyse §13.12](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1312-sicherheits--und-architekturgutachten-vom-25102026), Aufgaben in [Plan §21.12](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2112-technische-folge-aus-dem-sicherheits--und-architekturgutachten) und im Register §21.2; dieser Ordner enthält die Prüfprovenienz.

## Eingang

Der als Textanhang eingereichte Bericht „Technisches Gutachten: Glide – Security, Architektur, Wartbarkeit und Roadmap-Gaps“ hat 49.035 Byte und SHA-256 `7f83b5b0bd0a2e48331021875bfa6993d41a078e3ddaeb03f69b83a03096ee79`. Nicht mitgeliefert sind die darin verlinkten PDF-/Markdown-Fassungen, der Executive One-Pager und die Quellen hinter den internen Zitatmarken des erzeugenden Werkzeugs; sie werden nicht rekonstruiert. Die Fachzusammenfassung ist in die bestehenden Dokumente eingearbeitet, kein eigenes Gutachtendokument angelegt.

Der Bericht nennt zwei Stände: Git-Freeze `2ac339e29e90505930092035bd06e4b256612af0` und eine hochgeladene Hauptdatei mit SHA-256 `bd21317e8ab5fbaf5530973cee664ed5bbe1bac89ce09f245863f3fdbe380e6a`. Die heutige lokale Hauptdatei `src/glide/app.pyw` trägt genau diesen Hash (D55-Kandidat nach der Startfensterkorrektur).

## Gegenprobe

- **Struktur:** AST und Kompilierung im Speicher, ohne App-Import und ohne Bytecodeausgabe; Werte in [kennzahlen.json](kennzahlen.json). Alle Strukturzahlen des Berichts sind bestätigt; die Komplexitätswerte folgen einer eigenen, dort dokumentierten Zählregel.
- **Gelesene Codewege:** `read_save_file`, `autosave_tick`, `save_items_result`, `save_settings`, `write_complete_backup`, `inspect_backup_archive`, `validate_attachment_storage`, `safe_attachment_filename`, `remap_import_attachments`, `store_attachment`, `open_external_path`, `open_attachment`, `import_templates_file`, `safe_csv_cell`, `escape_print_text`, Linkfilter des Notizeditors, Modulkopf von `app.pyw` (Ordneranlage beim Import), `glide_start.py`, `calendar_service.py`, `image_conversion.py`, `preview_tools.py`.
- **Konfiguration:** `.github/workflows/python-app.yml` und `codeql.yml` (alle Actions über Versionstags, Rechte, Geheimnisse), `.github/dependabot.yml`, `requirements/*.txt` (Versionen ohne Hashes), `src/glide/vendor/provenance.json`, `LICENSE.md`, `scripts/pflege/abgleich_07.py`.
- **Vorhandene Belege:** [GitHub-Prüfung #138–#148](../github_pruefung_2026-10-23/README.md), [Phasennachweis](../phasenabschluss_2026-10-22/README.md) und die lokale Windows-Vollprüfung vom 25.10.2026 (Zusammenfassung `ergebnis.json` des Laufordners `windows_2026-10-25_1345`: 121 Schritte, rot nur `test_ui39`, Sichtprüfung übersprungen; `test_speicherlast330` grün mit 26.420 Punkten und 28,5 MB laut Suitenprotokoll).
- **Primärquellen, abgerufen 25.10.2026:** [PyPI tkinterdnd2](https://pypi.org/project/tkinterdnd2/) (0.6.4 vom 11.10.2026 ohne Provenance-Metadaten; SHA-256 des Rads 0.6.3 auf der [Versionsseite](https://pypi.org/project/tkinterdnd2/0.6.3/) gleich `provenance.json`), [PyInstaller-Änderungsverlauf](https://pyinstaller.org/en/stable/CHANGES.html) (6.22.3 vom 12.09.2026 ist die neueste Fassung), [CodeQL-Regel zu ungepinnten Actions](https://codeql.github.com/codeql-query-help/actions/actions-unpinned-tag) und [GitHub-Richtlinie für SHA-Pinning](https://github.blog/changelog/2025-08-15-github-actions-policy-now-supports-blocking-and-sha-pinning-actions/), [PowerShell about_Quoting_Rules](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_quoting_rules?view=powershell-5.1) (typografische Anführungszeichen gelten als normale).

Nicht möglich aus dieser Umgebung: Abruf der GitHub-Einstellungen und Code-Scanning-Ergebnisse (kein API-Zugang); der CodeQL-Befund stützt sich deshalb auf die dokumentierte Deaktivierung des eigenen Workflows, den 18.10.2026 beobachteten dynamischen Lauf und die Angabe des Berichts.

## Ergebnis der Einarbeitung

Bearbeitete Dokumente und ihre Hashes vor und nach der Runde stehen in [ergebnis.json](ergebnis.json), ebenso die tatsächlich ausgeführten Prüfungen (Standregeln, relative Links und Überschriftenanker der bearbeiteten Dokumente). Unverändert sind App, alle Module unter `src/glide`, `07_Python-Versionen`, Showcase, Fixtures, Datenformat und Lieferpakete.

Nicht Teil dieser Runde: CI-Grundstufe über den gesamten Baum, neue Integrations- oder Vollprüfung, native Plattform-, Reader- oder Menschenabnahme, Commit oder Push. Empfohlene Aufgaben im Plan sind keine ausgeführten Tests.
