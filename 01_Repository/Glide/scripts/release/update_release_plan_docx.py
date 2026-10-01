from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from docx import Document


def replace_in_paragraph(paragraph, old: str, new: str) -> None:
    for run in paragraph.runs:
        if old in run.text:
            run.text = run.text.replace(old, new)


def replace_everywhere(document, old: str, new: str) -> None:
    for paragraph in document.paragraphs:
        replace_in_paragraph(paragraph, old, new)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    replace_in_paragraph(paragraph, old, new)
    for section in document.sections:
        for area in (section.header, section.footer):
            for paragraph in area.paragraphs:
                replace_in_paragraph(paragraph, old, new)


def find_paragraph(document, text: str):
    for paragraph in document.paragraphs:
        if paragraph.text == text:
            return paragraph
    raise KeyError(f"Absatz nicht gefunden: {text}")


def find_paragraph_start(document, prefix: str):
    for paragraph in document.paragraphs:
        if paragraph.text.startswith(prefix):
            return paragraph
    raise KeyError(f"Absatz nicht gefunden: {prefix}")


def set_text(paragraph, text: str, *, bold_prefix: str | None = None) -> None:
    for run in list(paragraph.runs):
        paragraph._p.remove(run._r)
    if bold_prefix and text.startswith(bold_prefix):
        first = paragraph.add_run(bold_prefix)
        first.bold = True
        paragraph.add_run(text[len(bold_prefix) :])
    else:
        paragraph.add_run(text)


def set_callout(table, heading: str, body: str) -> None:
    cell = table.cell(0, 0)
    set_text(cell.paragraphs[0], heading)
    cell.paragraphs[0].runs[0].bold = True
    set_text(cell.paragraphs[1], body)


def set_cell_text(cell, text: str) -> None:
    paragraph = cell.paragraphs[0]
    set_text(paragraph, text)
    for extra in list(cell.paragraphs[1:]):
        extra._element.getparent().remove(extra._element)


def insert_after(document, anchor, text: str, style: str = "Normal"):
    paragraph = document.add_paragraph(text, style=style)
    anchor._p.addnext(paragraph._p)
    return paragraph


def update_document(source: Path, output: Path) -> None:
    document = Document(source)

    # Versions- und Kapitelbezeichnungen anpassen, ohne vorhandene Hyperlinks
    # und Run-Formatierungen unnötig anzutasten.
    replace_everywhere(document, "2.5.0", "2.5.1")
    replacements = {
        "6. Empfohlene Gesamt- und Ordnerstruktur": "6. Umgesetzte Gesamt- und Ordnerstruktur",
        "9. Empfohlene AGENTS.md für Glide": "9. Eingearbeitete AGENTS.md für Glide",
        "10. Empfohlenes Dokumentationssystem": "10. Eingerichtetes Dokumentationssystem",
        "14. Referenz-Testdaten jetzt vorbereiten": "14. Referenz-Testdaten und Migration",
        "18. Arbeitsvorbereitung während fehlender Codex-Credits": "18. Nachgeholte Arbeitsvorbereitung und verbleibende Punkte",
    }
    for old, new in replacements.items():
        replace_everywhere(document, old, new)

    set_text(find_paragraph(document, "Dokumentversion 1.0 · Stand 31.08.2026"), "Dokumentversion 2.5.1 · Stand 31.08.2026")
    set_text(
        find_paragraph(document, "Arbeitsstatus: Planung / Pre-Release"),
        "Arbeitsstatus: Source 2.5.1 implementiert und getestet · Packaging/Release weiterhin Pre-Release",
    )

    set_callout(
        document.tables[0],
        "Zweck und Abgrenzung dieses Dokuments",
        "Diese Revision dokumentiert den tatsächlich erreichten Source- und Strukturstand von Glide 2.5.1 sowie die weiterhin offenen Build-, Signing- und Store-Arbeiten. Codeblöcke, Buildbefehle und die Arbeitspakete C01–C08 sind Referenzmaterial beziehungsweise Vorlagen; sie sind keine eigenständigen Arbeitsanweisungen und werden nur nach einem separaten Auftrag ausgeführt.",
    )
    set_callout(
        document.tables[2],
        "Kernaussage 2.5.1",
        "Die gewünschte Quality-of-Life-Erweiterung ist im Source umgesetzt und automatisiert geprüft. Die Repository-Grundlage, technische Markdown-Dokumentation und getrennten Arbeitsbereiche sind angelegt. Noch nicht nachgewiesen sind reproduzierbare EXE-/DMG-Builds, Installer, Signing, Notarisierung, Clean-Machine-Tests und Store-Reife.",
    )

    set_text(
        find_paragraph_start(document, "Gesamtbewertung."),
        "Gesamtbewertung. Glide 2.5.1 liegt als lauffähiger, getesteter Source-Stand vor. Ordnerübersicht, fester Eingang, listenübergreifendes Drag & Drop, freie Notizen, Aufgabenbeschreibungen, lokale Anhänge, Dark-Mode-Chrome und sichere Komplettbackups sind umgesetzt. Der zuvor abgebrochene 2.5.0-Stand wurde nachvollzogen und stabilisiert.",
        bold_prefix="Gesamtbewertung.",
    )
    set_text(
        find_paragraph_start(document, "Der nächste Qualitätssprung besteht"),
        "Der nächste Qualitätssprung liegt nun außerhalb der reinen Feature-Implementierung: manuelle Plattform-QA, verbindliche Produktidentitäten, reproduzierbares Packaging, Signing/Notarisierung und Clean-Machine-Tests. Die neue Struktur trennt dafür Source, Tests, Fixtures, technische Dokumentation, Grafik-Master, Store-Material und finale Release-Artefakte.",
    )
    set_text(find_paragraph(document, "Die drei sinnvollsten Arbeiten während einer Codex-Pause sind:"), "Die drei wichtigsten nächsten Arbeiten sind:")
    set_text(find_paragraph_start(document, "Produkt-, Publisher-"), "Produkt-, Publisher-, Lizenz- und Plattformidentitäten verbindlich festlegen.")
    set_text(find_paragraph_start(document, "Branding-Master einschließlich"), "Die manuelle Windows-/macOS-QA-Matrix auf realen Zielsystemen abschließen.")
    set_text(find_paragraph_start(document, "Workspace, Dokumentationsgerüst"), "Reproduzierbare unsigned Builds vorbereiten; erst danach Signing, Notarisierung und Stores angehen.")

    # Der alte Screenshot bleibt als Beleg der Ausgangslage erhalten.
    set_text(
        find_paragraph_start(document, "Abbildung 1:"),
        "Abbildung 1: Historische Ausgangslage vor der Strukturüberarbeitung (Stand 31.08.2026).",
    )
    old_structure = find_paragraph_start(document, "Sichtbar sind unter anderem:")
    set_text(
        old_structure,
        "Der Screenshot zeigt den Zustand, an dem der vorherige Lauf abbrach: Versionsdateien lagen unter 07_Python-Versionen, der Test noch im Workspace-Root und ein generierter __pycache__ daneben. Dieser Zustand wurde nicht überschrieben, sondern nachvollziehbar in eine kanonische Repository-Struktur überführt; historische Versionen und Testdaten bleiben separat erhalten.",
    )
    anchor = old_structure
    anchor = insert_after(document, anchor, "2.4 Umgesetzter Arbeitsstand 2.5.1", "Heading 2")
    anchor = insert_after(
        document,
        anchor,
        "Die neue Struktur wurde nicht-destruktiv angelegt. Der getestete Source besitzt jetzt einen stabilen Pfad ohne Versionsnummer, während die leicht startbaren Versionskopien als Historie erhalten bleiben.",
    )
    anchor = insert_after(
        document,
        anchor,
        "Glide_Workspace/\n├─ 00_Arbeitsvorbereitung/\n├─ 01_Repository/Glide/\n│  ├─ src/glide/app.pyw\n│  ├─ tests/integration/test_glide.py\n│  ├─ tests/fixtures/{current_v4,legacy_v2}/\n│  ├─ docs/ · assets/ · packaging/ · scripts/ · requirements/\n│  └─ AGENTS.md · README.md · CHANGELOG.md · VERSION\n├─ 05_Probelisten_Testdaten/          (historische Quelle)\n├─ 07_Python-Versionen/               (historische Einzeldateien)\n├─ 10_Dokumentation/                  (Word-Arbeitsgrundlagen)\n├─ 20_Grafik_Master/\n├─ 30_Release_Exports/2.5.1/          (noch ohne Build)\n├─ 40_Store_Material/\n├─ 90_Testdaten_Extern/\n└─ 100_Archiv/",
        "CodeBlock",
    )
    insert_after(
        document,
        anchor,
        "Der frühere Root-Test wurde in die Repository-Tests überführt; der generierte Python-Cache wurde entfernt. Es wurde bewusst noch kein Git-Repository initialisiert und kein Packaging- oder Signingwert erfunden.",
    )

    set_text(
        find_paragraph_start(document, "Empfohlen ist eine Zweiteilung:"),
        "Die empfohlene Zweiteilung ist für 2.5.1 angelegt: ein persönlicher Workspace für Arbeitsmaterialien und ein technisch kontrollierter Repository-Bereich für Source, Tests, Packaging-Vorbereitung und code-nahe Dokumentation.",
    )
    structure_block = find_paragraph_start(document, "Glide_Workspace/")
    set_text(
        structure_block,
        "Glide_Workspace/\n│\n├─ 00_Arbeitsvorbereitung/{Entscheidungen,Research,Checklisten,Notizen}/\n├─ 01_Repository/Glide/\n│  ├─ AGENTS.md · README.md · CHANGELOG.md · LICENSE.md · SECURITY.md\n│  ├─ .gitignore · .gitattributes · .editorconfig · VERSION\n│  ├─ src/glide/{app.pyw,resources/}\n│  ├─ tests/{unit,integration,smoke,packaging,fixtures/}\n│  ├─ assets/{branding,runtime,installer}/\n│  ├─ packaging/{pyinstaller,windows,macos}/\n│  ├─ scripts/{build,assets,test,release,verify}/\n│  ├─ requirements/\n│  └─ docs/{00_INDEX,01_PRODUCT_CONSTRAINTS,02_ARCHITECTURE,05_QA_TESTPLAN,06_DATA_BACKUP_MIGRATION,10_RELEASE_CHECKLIST,decisions,exec-plans}/\n├─ 05_Probelisten_Testdaten/          (Legacy-Quelle)\n├─ 07_Python-Versionen/               (Versionshistorie)\n├─ 10_Dokumentation/                  (Word/PDF)\n├─ 20_Grafik_Master/\n├─ 30_Release_Exports/<VERSION>/      (einziger Ort finaler Binärartefakte)\n├─ 40_Store_Material/\n├─ 90_Testdaten_Extern/\n└─ 100_Archiv/",
    )

    # Ist-/Soll-Tabelle in Kapitel 6 auf den realen Stand bringen.
    status_rows = {
        1: "erledigt: generierten Cache entfernt; im Repository per .gitignore ausgeschlossen",
        2: "aufgearbeitet: Legacy-v2-Fixture unter tests/fixtures; TXT-Beispiele unter 90_Testdaten_Extern",
        3: "als Historie beibehalten; kanonischer Source ist src/glide/app.pyw ohne Versionsnummer",
        4: "umgesetzt: technische Markdown-Doku im Repository; Word-Dokumentation bleibt außerhalb",
        5: "bleibt außerhalb des produktiven Repository-Bereichs",
        6: "erledigt: kanonischer Integrationstest unter tests/integration/test_glide.py; alte Testkopie archiviert",
    }
    for row_index, value in status_rows.items():
        set_cell_text(document.tables[7].cell(row_index, 1), value)
    set_callout(
        document.tables[8],
        "Wichtig für den nächsten Schritt",
        "Der funktionsfähige Monolith wurde gesichert und geprüft; die neue Struktur enthält eine bytegleiche kanonische Source-Kopie. Eine inhaltliche Modulzerlegung ist weiterhin ein separates Refactoring und darf erst mit zusätzlichen Regressionstests erfolgen.",
    )

    set_text(
        find_paragraph_start(document, "Der bisherige umfassende KI-Arbeitsauftrag"),
        "Die folgenden Blöcke C01–C08 sind wiederverwendbare Ticketvorlagen und Statusreferenzen. Sie sind Inhalt dieses Dokuments, keine automatisch auszuführenden Anweisungen. C01 wurde für den vorhandenen Workspace lesend nachvollzogen; die Grundlage aus C02 ist teilweise umgesetzt. C03 ist teilweise umgesetzt, C04–C08 sind nicht begonnen und benötigen jeweils einen separaten Auftrag.",
    )
    ticket_status = {
        "C01 – Repository Audit": "C01 – Repository Audit (für 2.5.1 abgeschlossen)",
        "C02 – Repository Foundation": "C02 – Repository Foundation (Grundlage umgesetzt)",
        "C03 – Release-Härtung": "C03 – Release-Härtung (teilweise umgesetzt)",
        "C04 – Asset Pipeline": "C04 – Asset Pipeline (nicht begonnen)",
        "C05 – Windows Build": "C05 – Windows Build (nicht begonnen)",
        "C06 – macOS Build": "C06 – macOS Build (nicht begonnen)",
        "C07 – QA": "C07 – QA (Source-/Integrationstest vorhanden; Release-QA offen)",
        "C08 – Release Automation": "C08 – Release Automation (nicht begonnen)",
    }
    for old, new in ticket_status.items():
        set_text(find_paragraph(document, old), new)

    set_text(
        find_paragraph_start(document, "AGENTS.md sollte als kurze"),
        "Eine kurze, verbindliche AGENTS.md ist jetzt unter 01_Repository/Glide/AGENTS.md vorhanden. Der folgende Block bleibt ein historisches Beispiel; maßgeblich ist die lokale Datei zusammen mit den verlinkten Markdown-Dokumenten.",
    )
    set_text(
        find_paragraph_start(document, "Die vorhandene Word-Buildanleitung"),
        "Das Markdown-Grundgerüst ist unter 01_Repository/Glide/docs/ eingerichtet. Diese Word-Datei bleibt die ausführliche menschlich lesbare Arbeitsgrundlage; die Markdown-Dateien bilden die knappen code-nahen Quellen. Noch nicht angelegte Spezialdokumente folgen erst zusammen mit Packaging, Signing und Store-Arbeit.",
    )

    identity = find_paragraph_start(document, "Produktname:\nGlide")
    set_text(
        identity,
        "Datei:\n01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md\n\nProduktname:\nGlide\n\nLangname:\nGlide – Aufgaben und Listen\n\nAktuelle App-Version:\n2.5.1\n\nDatenformat-Version:\n4\n\nRelease-Kanal:\ninternal / pre-release\n\nPublisher, Copyright, Support-E-Mail, Website, Datenschutz-URL und Lizenzmodell:\noffen – nicht durch Annahmen ersetzen\n\nWindows:\nZiel Windows 10/11; Architektur, AppUserModelID und Inno-Setup-AppId final festlegen\n\nmacOS:\nBundle Identifier, Mindestversion und Architektur final festlegen",
    )

    set_text(
        find_paragraph_start(document, "Die vorhandene Release-Anleitung enthält bereits"),
        "Die QA-Grundlage ist jetzt operationalisiert: Der Integrationstest startet Glide mit einem isolierten temporären Datenordner und prüft Kernfunktionen, Migration, Backup/Restore sowie mehrere Fehlerfälle. Unit-, Packaging- und reale Clean-Machine-Tests bleiben als nächste Ebenen offen.",
    )
    test_tree = find_paragraph(document, "tests/\n├─ unit/\n├─ integration/\n├─ smoke/\n└─ packaging/")
    set_text(
        test_tree,
        "tests/\n├─ unit/                         (vorbereitet)\n├─ integration/test_glide.py    (grün)\n├─ smoke/                        (vorbereitet)\n├─ packaging/                    (vorbereitet)\n└─ fixtures/{current_v4,legacy_v2}/",
    )
    insert_after(
        document,
        test_tree,
        "Nachweis am 31.08.2026: „Glide v2.5.1 Kern-, Backup- und Migrationstests: OK“. Die nachfolgende Matrix ist eine Soll-Matrix; „Ja“ bedeutet erforderlich, nicht bereits für einen Installer oder DMG nachgewiesen.",
    )

    set_text(
        find_paragraph_start(document, "Ein kleines, bewusst konstruiertes Referenzset"),
        "Die Referenzdaten sind nun getrennt: ein kleines aktuelles Format-4-Fixture sowie ein vorhandener größerer Format-2-Bestand für Migration. Manuelle TXT-Importbeispiele liegen außerhalb der automatisierten Tests.",
    )
    set_text(
        find_paragraph_start(document, "Liste 1\n├─ Aufgabe normal"),
        "01_Repository/Glide/tests/fixtures/\n├─ current_v4/reference_v4.json\n└─ legacy_v2/probelisten_5_listen_v2.json\n\n90_Testdaten_Extern/Legacy_Probelisten/\n└─ manuelle TXT-Importbeispiele",
    )
    set_text(
        find_paragraph_start(document, "Die Referenzdaten sollten versioniert"),
        "Das aktuelle Fixture enthält Eingang, Ordner, Seitennotiz, Beschreibung, Fälligkeit, Wichtigkeit und Unterpunkt. Der größere Altbestand ist ausdrücklich als Legacy-Migrationsfixture gekennzeichnet. Reale personenbezogene oder vertrauliche Unternehmensdaten gehören nicht in automatisierte Fixtures.",
    )

    set_text(
        find_paragraph_start(document, "Finale Veröffentlichungen sollten pro Version"),
        "Finale Veröffentlichungen werden ausschließlich außerhalb des Repository-Bereichs unter 30_Release_Exports/<VERSION>/ abgelegt. Für 2.5.1 ist die Struktur vorbereitet, aber noch kein EXE-, Installer-, App- oder DMG-Artefakt als freigegeben vorhanden. Das folgende Schema ist daher eine Vorlage.",
    )
    set_text(
        find_paragraph_start(document, "release/\n└─ 2.5.1/"),
        "30_Release_Exports/\n└─ <VERSION>/\n   ├─ Windows/Glide-Setup-<VERSION>-<ARCH>.exe\n   ├─ macOS/Glide-<VERSION>-<ARCH>.dmg\n   ├─ RELEASE_NOTES.md\n   ├─ release-manifest.json\n   └─ Hashes/SHA256SUMS.txt",
    )
    set_text(
        find_paragraph_start(document, '{\n  "product": "Glide"'),
        '{\n  "product": "Glide",\n  "version": "<VERSION>",\n  "channel": "<CHANNEL>",\n  "build_date": "<YYYY-MM-DD>",\n  "windows": {"architecture": "<ARCH>"},\n  "macos": {"architecture": "<ARCH>"}\n}',
    )
    installer_example = find_paragraph_start(document, "Glide-Setup-2.5.1.exe")
    set_text(installer_example, "Glide-Setup-<VERSION>.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART")

    set_text(
        find_paragraph_start(document, "Eine vollständige Sicherheitskopie des aktuell"),
        "Abgeschlossen: Der lauffähige Source-Stand 2.5.1 ist unter 07_Python-Versionen erhalten und bytegleich in den kanonischen Repository-Pfad übernommen.",
    )
    set_text(find_paragraph_start(document, "Glide_PreRelease_2.5.1"), "Glide_PreRelease_2.5.1_2026-08-31")
    set_text(
        find_paragraph(document, "Noch keine strukturellen Refactorings durchführen."),
        "Der Monolith wurde nicht in Module zerlegt; die Strukturänderung beschränkt sich auf eine getestete kanonische Kopie und begleitende Projektdateien.",
    )
    doc_tree = find_paragraph_start(document, "AGENTS.md\ndocs/")
    set_text(
        doc_tree,
        "AGENTS.md                              vorhanden\ndocs/\n├─ 00_INDEX.md                         vorhanden\n├─ 01_PRODUCT_CONSTRAINTS.md           vorhanden\n├─ 02_ARCHITECTURE.md                  vorhanden\n├─ 05_QA_TESTPLAN.md                   vorhanden\n├─ 06_DATA_BACKUP_MIGRATION.md         vorhanden\n├─ 10_RELEASE_CHECKLIST.md             vorhanden\n├─ decisions/PRODUCT_IDENTITY.md       vorhanden\n├─ exec-plans/2.5.1-stabilisierung.md  vorhanden\n└─ Build/Branding/Signing/Store-Details folgen mit den jeweiligen Arbeitspaketen",
    )

    phase_updates = {
        1: "teilweise abgeschlossen: Projekt gesichert, Testdaten und Dokumentationsgerüst vorhanden; Identität und Branding offen",
        2: "für den vorhandenen Stand abgeschlossen: Source, Abhängigkeiten, Pfade, Daten, Risiken und Abbruchpunkt geprüft",
        3: "teilweise abgeschlossen: Struktur, AGENTS, Doku und Integrationstest vorhanden; Git-Initialisierung und Modulzerlegung offen",
        4: "nicht begonnen: freigegebenes Artwork fehlt",
        5: "nicht begonnen: Packaging-/Installer-Konfiguration fehlt",
        6: "nicht begonnen: macOS-Buildumgebung und Identitäten fehlen",
        7: "teilweise: Source-/Integrationstest grün; Packaging-, Clean-Machine- und Plattform-QA offen",
    }
    for row_index, value in phase_updates.items():
        set_cell_text(document.tables[14].cell(row_index, 2), value)

    set_text(
        find_paragraph_start(document, "Die bestehende Vorbereitung ist technisch belastbar"),
        "Der zuvor unterbrochene Entwicklungsstand ist als Glide 2.5.1 stabilisiert, getestet und dokumentiert. Die gewünschte Bedienungsverbesserung ist umgesetzt; die verbleibenden Risiken liegen nicht mehr im Kern-Source, sondern vor allem in manueller Plattform-QA, Produktidentität, Branding, Packaging, Signing, Notarisierung und Store-Prozessen.",
    )
    set_text(find_paragraph(document, "Empfohlene Reihenfolge ab jetzt:"), "Empfohlene Reihenfolge nach Abschluss von 2.5.1:")
    next_steps = [
        "1. Den neuen 2.5.1-Stand mit realen Arbeitsdaten in einer Kopie manuell prüfen.",
        "2. Windows 10/11: NumLock, CapsLock, Dark Mode, Menüs, Dialoge und Drag & Drop vollständig testen.",
        "3. Produktidentität, Lizenz, Supportkontakt und Plattform-IDs verbindlich festlegen.",
        "4. Branding-Master und Apple-Layer liefern und validieren.",
        "5. PyInstaller-OneDir-Build reproduzierbar und zunächst unsigned erstellen.",
        "6. Windows-Installer und macOS-App/DMG auf Clean Machines testen.",
        "7. Erst danach Signing, Notarisierung, Hashes und Release-Manifest umsetzen.",
        "8. Store-Material erst auf Basis eines nahezu eingefrorenen Release Candidates erstellen.",
        "9. Eine Modulzerlegung des Monolithen als eigenes, testgestütztes Refactoring planen.",
    ]
    old_steps = [
        "1. Arbeitsstand sichern und nicht manuell refactoren.",
        "2. Produktidentität und Plattformentscheidungen ausfüllen.",
        "3. Icon-/Branding-Master und Apple-Layer vorbereiten.",
        "4. Referenz-Testdaten definieren.",
        "5. Workspace- und Dokumentationsstruktur anlegen.",
        "6. Bei wieder verfügbaren Codex-Credits mit C01 – Repository Audit starten.",
        "7. Erst nach freigegebenem Audit produktive Dateien umstrukturieren.",
        "8. Windows und macOS zunächst unsigned reproduzierbar bauen und testen.",
        "9. Signing und Store-Veröffentlichung erst auf einen stabilen Releaseprozess setzen.",
    ]
    for old, new in zip(old_steps, next_steps):
        set_text(find_paragraph(document, old), new)
    set_callout(
        document.tables[16],
        "Nächster sinnvoller Arbeitsauftrag",
        "Nach fachlicher Prüfung von 2.5.1 sollte C03 als klar begrenztes Packaging-/Release-Härtungs-Ticket folgen: zuerst Produktidentitäten festlegen, dann einen reproduzierbaren unsigned PyInstaller-OneDir-Build und passende Smoke Tests erstellen. C04–C08 bleiben separate Aufträge.",
    )

    set_text(find_paragraph(document, "Interne Projektgrundlagen:"), "Interne, in dieser Revision tatsächlich geprüfte Projektgrundlagen:")
    set_text(
        find_paragraph_start(document, "Glide – Funktionskatalog"),
        "Ursprüngliche Benutzeranforderung, UI-Screenshots und gewünschte Quality-of-Life-Funktionen, Stand 31.08.2026.",
    )
    set_text(
        find_paragraph_start(document, "Glide – Build-, Packaging-"),
        "Glide-Source v2.4.1, angefangener Zwischenstand v2.5.0 und stabilisierter Source v2.5.1.",
    )
    set_text(
        find_paragraph_start(document, "Aktuelle sichtbare Ordnerstruktur"),
        "Lokaler Workspace, neue Struktur unter 01_Repository/Glide sowie grüner Integrationstest für v2.5.1.",
    )
    source_anchor = find_paragraph_start(document, "Lokaler Workspace, neue Struktur")
    source_anchor = insert_after(
        document,
        source_anchor,
        "Technische Markdown-Dokumentation unter 01_Repository/Glide/docs/ und Versions-/Änderungsdateien im Repository-Root.",
        "List Bullet",
    )
    insert_after(
        document,
        source_anchor,
        "Hinweis: Im Workspace lagen keine eigenständige Build-/Release-Anleitung und kein separater Funktionskatalog als lokale Datei vor; Aussagen dazu aus der Vorversion sind daher Planungsbezug, kein in dieser Revision reproduzierter Buildnachweis.",
        "List Bullet",
    )
    set_text(
        find_paragraph_start(document, "Prüfstand: 31.08.2026."),
        "Prüfstand: 31.08.2026. Source, Struktur und automatisierter Integrationstest entsprechen App-Version 2.5.1 und Datenformat 4. Store-, Signierungs- und Plattformanforderungen können sich ändern und müssen unmittelbar vor einer Einreichung oder Zertifikatsbeschaffung anhand offizieller Quellen erneut geprüft werden.",
    )

    properties = document.core_properties
    properties.title = "Glide 2.5.1 – Arbeitsvorbereitung für Codex, Build, Release und Dokumentation"
    properties.subject = "Implementierter Source-Stand 2.5.1, Repository-Grundlage und verbleibender Release-Plan"
    properties.keywords = "Glide, 2.5.1, Tkinter, QA, Backup, Repository, Packaging, Release"
    properties.comments = "Überarbeitete Revision auf Basis des geprüften lokalen Source- und Workspace-Stands."
    properties.last_modified_by = "OpenAI Codex"
    properties.revision = 2
    properties.modified = datetime.now(timezone.utc).replace(tzinfo=None)

    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    update_document(args.source, args.output)


if __name__ == "__main__":
    main()
