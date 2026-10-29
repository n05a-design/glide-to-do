"""Gezielte Dokumentkorrekturen; keine Laufzeitlogik oder historischen Belege ändern."""
from pathlib import Path
import ast
import hashlib
import json

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
changes = {}
reasons = {}


def get(name):
    if name not in changes:
        data = (ROOT / name).read_bytes()
        changes[name] = [data, data.decode('utf-8-sig')]
    return changes[name][1]


def replace(name, before, after, reason):
    text = get(name)
    assert text.count(before) == 1, (name, before[:90], text.count(before))
    changes[name][1] = text.replace(before, after)
    reasons.setdefault(name, []).append(reason)


def line(name, prefix, after, reason):
    matches = [row for row in get(name).splitlines() if row.startswith(prefix)]
    assert len(matches) == 1, (name, prefix, len(matches))
    replace(name, matches[0], after, reason)


def add_top(name, paragraph):
    text = get(name)
    rows = text.splitlines()
    n = next(i for i, row in enumerate(rows) if row.startswith('Stand '))
    rows[n] = rows[n].replace('Stand 28.10.2026', 'Stand 29.10.2026')
    rows[n+1:n+1] = ['', paragraph]
    changes[name][1] = '\n'.join(rows) + '\n'
    reasons.setdefault(name, []).append('Aktuellen Pflegeauftrag und Abgleichstand an der zuständigen Quelle eintragen')


plan = '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md'
manual = '00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md'
analysis = '00_Arbeitsvorbereitung/Glide_Analyse.md'
handoff = '00_Arbeitsvorbereitung/Glide_Uebergabe.md'
direction = '01_Repository/Glide/docs/ARBEITSRICHTUNG.md'
index = '01_Repository/Glide/docs/00_INDEX.md'
architecture = '01_Repository/Glide/docs/02_ARCHITECTURE.md'
data = '01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md'
qa = '01_Repository/Glide/docs/07_QA_BERICHT.md'
proof_root = '../01_Repository/Glide/tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md'

replace(plan, 'App-Vorlagen/`template_helpers.py`', 'Vorlagenlogik in `app.pyw` (`default_template_records`, Vorlagenanwendung)', 'Nicht existentes template_helpers.py durch den vorhandenen Einstieg ersetzen')
replace(plan, '`drawing.py`, `drawing_import.py`, `drawing_palette.py`', '`drawing.py` (Palettenparser, Import-/Exportregeln), Pixeladapter in `app.pyw`', 'Nicht existente Import-/Palettenmodule durch tatsächliche Zuständigkeit ersetzen')
replace(plan, '`drawing_animation.py`, `drawing.py`', '`animation.py`, `animation_export.py`, `drawing.py`; UI in `app.pyw`', 'Nicht existentes Animationsmodul durch aktuelle Module ersetzen')
replace(plan, 'aktuellen 3.43.x-UI-Stand mit Vorbereitung abgleichen', 'aktuellen 3.49.0-UI-Stand mit Vorbereitung abgleichen', 'P8-Abgleich auf den tatsächlichen Kandidaten beziehen')
replace(plan, 'P8 zuerst gesichert abschließen; bestehender Rahmen gewählt, keine neue Stufenfrage', 'P8 nach D50 pausiert; vor einer 4.0-Abnahme gesichert abschließen, bestehender Rahmen gewählt', 'Pausierung und Abnahmetor von einer unmittelbaren Startfolge trennen')
replace(plan, 'Für alle gelieferten Bestandsgruppen bleibt **M offen gemäß I6**,', 'Die Versionsangaben in den Bestandszeilen bezeichnen historische Einführung bzw. damalige Lieferung. **Aktuell: Quelle 3.49.0, Python/Showcase 3.47.0, native Pakete 3.45.0; neue 3.48-/3.49-Funktionen noch nicht geliefert.** Aktuelle Einzelgrenzen und der rote FP-01-Pflichtfall stehen in §21.29; für die Bestandskerne liegt die 3.45.0-Paketlieferung vor, ihre native/Menschenabnahme bleibt davon getrennt. Für alle gelieferten Bestandsgruppen bleibt **M offen gemäß I6**,', 'Historische Tabellenwerte von aktuellem Liefer- und Abnahmestand abgrenzen')
replace(plan, 'optional der Grund WA-12', 'der umgesetzte Grund WA-12', 'Ausgewählten WA-12-Umfang nicht mehr als Option führen') if 'optional der Grund WA-12' in get(plan) else None
replace(plan, 'neue Regeln FP-02, optionaler Grund WA-12', 'neue Regeln FP-02, umgesetzter Grund WA-12 (§21.16/§21.20)', 'WA-12-Auswahl und Lieferung in Bestandszeile nachziehen')
replace(plan, 'I im Quellkandidaten umgesetzt; P 14 Fachfälle und zehn echte Tagespaket-Prüfgruppen grün; L noch nicht, letzte Lieferung 3.45.0 unverändert; M offen', 'I umgesetzt; P 14 Fachfälle und zehn Tagespaket-Prüfgruppen historisch grün; L im 3.45.0-Paketabschluss §21.20 enthalten, Python heute 3.47.0; M offen', 'WA-12-Lieferwiderspruch A05 gegen den späteren Liefernachweis berichtigen')
start = get(plan).index('### 18.3 ')
end = get(plan).index('### 18.4 ', start)
before = get(plan)[start:end]
after = before.replace('I integriert; P gezielte Wiederhol-/Schutzfälle grün, eingefrorene Vollprüfung 3.44.0; L 3.44.0 Python-Lieferung, Mac/Pakete offen; M offen', 'I integriert; P historisch grün, neuer Pflichtlauf 28.10.2026 nur 8/9 (Prüfadapter/Sitzungsabschluss, §21.29); L Kern Python 3.47.0/native 3.45.0; M offen')
after = after.replace('L 3.44.0 nach 07 geliefert, Mac/Pakete offen', 'L seit 3.44.0 nach 07, Kern heute Python 3.47.0/native 3.45.0')
after = after.replace('L 3.44.0 (Python)', 'L seit 3.44.0 Python, Kern heute Python 3.47.0/native 3.45.0')
after = after.replace('Mac-Bundle/Pakete und native Abnahmen getrennt offen; nicht erneut implementieren', 'Prüfadapter korrigieren und Originalsuite/Folgematrix bestehen; native/Menschenabnahmen offen, nicht erneut implementieren')
after = after.replace('kein freier Feldbaukasten; Mac/Pakete und native Abnahme offen (§21.10)', 'kein freier Feldbaukasten; native Abnahme offen, 3.45.0-Pakete geliefert (§21.20)')
after = after.replace('implementierte Teile nicht neu planen; Mac/Pakete und Abnahmen offen (§21.10)', 'implementierte Teile nicht neu planen; 3.45.0-Pakete geliefert, native/Menschenabnahmen offen')
after = after.replace('L Python 3.43.1, vollständiger Mac-/Paketabschluss fehlt', 'L Bestandskern Python 3.47.0/native 3.45.0, 3.49.0 noch nicht geliefert')
replace(plan, before, after, 'Operative Statusmatrix mit Lieferungen und aktuellem FP-01-Rotbefund abgleichen')
line(plan, '| FP-01 / Schutz WA-27–30 |', '| FP-01 / Schutz WA-27–30 | D49-Auslegung und konkrete Schutzaufträge | Implementiert; Bestandskern Python 3.47.0/native 3.45.0 geliefert. Historische grüne Belege bleiben datiert; neue Originalsuite FP-01 8/9, Prüfadapter/Sitzungsabschluss offen und zwölf Folgesuiten gestoppt (§21.29). Native/Menschenabnahme bleibt offen |', 'Aktuelle Roadmap führt den neuen Pflichtbefund statt ausschließlich früherer grüner Tests')
line(plan, '| WA-26 Bildkonversion |', '| WA-26 Bildkonversion | konkret fortgesetzt | Gemeinsamer Hintergrunddienst, seit 3.44.0 geliefert; im nativen 3.45.0-Bestand enthalten. Native Konverter-/Großbild- und Menschenabnahme offen |', 'Paketlieferung und native Abnahme unterscheiden')
replace(plan, '**Veränderte Reihenfolge [Empfehlung, durch Codevalidierung präzisiert; Kandidat inzwischen als 3.44.0 abgeschlossen, §21.10]:**', '**Historische technische Reihenfolge vom 21.10.2026 [Empfehlung; damaliger Kandidat später als 3.44.0 abgeschlossen, §21.10; aktuelle Priorität und Rest §21.29]:**', 'Überholte Startfolge eindeutig als historischen Kontext markieren')
for file in [plan, index, architecture]:
    text = get(file)
    old_anchor = '#abgesicherter-wiederanlauf-nach-absturz-geplant'
    assert old_anchor in text
    changes[file][1] = text.replace(old_anchor, '#abgesicherter-wiederanlauf-nach-absturz-lokaler-kandidat-3490')
    reasons.setdefault(file, []).append('Drei defekte Abschnittsverweise auf den bestehenden Wiederanlaufvertrag korrigieren')

line(manual, '**Aktuelle Prüfgrenze ', '**Aktuelle Prüfgrenze 29.10.2026:** Quellkandidat 3.49.0/Format 26 hat eine grüne CI-Grundstufe, aber keine vollständige Gesamtabnahme. Originale FP-01-Suite 8/9, zwölf Folgesuiten nach Fehlerstopp nicht ausgeführt; der Diagnoseadapter ersetzt keinen grünen Pflichtnachweis. WA-41A/B bleiben offen. B1 unten ist ein historischer automatischer Erfolg. Python/Showcase 3.47.0, native Pakete 3.45.0. Diese Dokumentpflege startet keine neue App-/Lastprüfung; BIOS/CPU vorerst unverändert. [Abnahmebericht](../01_Repository/Glide/tests/qa-3.49.0/abnahme_2026-10-28/README.md).', 'A05: Prüfgrenze auf tatsächliche Version und Auditbefund nachführen')
add_top(manual, '**Zusätzliche Menschenabnahme für 3.49.0, offen:** Wochen-Schnellwahl mit Tastatur/Filter, Tageswechsel und Heute-Markierung bedienen; gemeinsame Fälligkeit mit individuellen Uhrzeiten, Entfernen und Aufwand je Aufgabe einschließlich Undo/Redo prüfen. Verweise kopieren, bewusst im Hauptbereich öffnen und nach Dialog gezielt verknüpfen; Hauptentwurf erhalten. Wiederanlauf nach echtem Abbruch, lesender Schutz, bewusste Freigabe mit Originalvorsicherung, Restorefehler und Diagnoseanzeige getrennt am nativen Gerät abnehmen. Kleine Fenster/große Schrift, Hell/Dunkel, Kompaktmodus, DPI und Reader berücksichtigen. Automatische Belege und verbleibende Grenzen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).')

line(architecture, '**Geplanter Robustheitsnachlauf,', '**Robustheitsrahmen, aktualisiert 29.10.2026:** Die zunächst am 27.10. geplanten Schutzpakete sind im lokalen Kandidaten 3.49.0 implementiert; [Umfang §21.27](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2127-vorbeugung-absturzdiagnose-und-abgesicherter-wiederanlauf), [aktueller Abnahmerest §21.29](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2129-abnahmeprüfung-des-begonnenen-umfangs). Tk-freie Sitzungsregeln und technische Prozessdiagnose ergänzen SaveResult, Sperrbesitz und atomare Commitgrenze. Breite/native Abnahme und Lieferung bleiben offen; FP-01 benötigt den korrekten Prüf-Sitzungsabschluss. Keine neue Architekturentscheidung D58, CPU-Sonderlogik oder Lastgrenze. Umfangreiche Prüfungen gehören an Wiederanlauf-/Import-/Restoregrenzen. [Datenvertrag](06_DATA_BACKUP_MIGRATION.md#abgesicherter-wiederanlauf-nach-absturz-lokaler-kandidat-3490), ausgeführte Ergebnisse im [QA-Bericht](07_QA_BERICHT.md).', 'Bereits implementierte Architektur nicht weiter als unbegonnen führen')
line(index, '- **Aktueller Quellkandidat ', '- **Aktueller Quellkandidat 3.49.0:** [Funktionsausbau §21.28](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2128-funktionaler-ausbau-der-ursprünglichen-drei-pakete), [Schutzpakete §21.27](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2127-vorbeugung-absturzdiagnose-und-abgesicherter-wiederanlauf), [Abnahmebericht](../tests/qa-3.49.0/abnahme_2026-10-28/README.md). CI-Grundstufe grün; FP-01 8/9 und zwölf Folgesuiten gestoppt. WA-41, aktuelle Lieferung und native/Menschenabnahmen offen; Python/Showcase 3.47.0, native Pakete 3.45.0.', 'Index auf aktuellen Quell-, Prüf- und Lieferstand stellen')
line(index, '- **Vorbeugung und Wiederanlauf,', '- **Vorbeugung und Wiederanlauf, implementiert mit offenen Abnahmetoren:** [Plan §21.27](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2127-vorbeugung-absturzdiagnose-und-abgesicherter-wiederanlauf), [Datenvertrag](06_DATA_BACKUP_MIGRATION.md#abgesicherter-wiederanlauf-nach-absturz-lokaler-kandidat-3490), [Prüfziele](05_QA_TESTPLAN.md#vorbeugung-und-wiederanlauf-geplante-abnahme). Gezielte Prüfungen liegen vor; Ursachenklärung, vollständige Matrix und aktuelle Lieferung sind offen.', 'Planung, Umsetzung und noch offene Abnahme konsistent trennen')
replace(index, 'Prüfkandidat 3.48.0, offene WA-41-Diagnose, aktuelle Liefergrenzen und Datei-/Dokumentaudit', 'Prüfkandidat 3.49.0, Abnahmeaudit mit FP-01-Rotbefund, WA-41-Diagnose, Liefergrenzen und Datei-/Dokumentabgleich', 'Beschreibung des QA-Berichts aktualisieren')
line(data, '**3.44.0 (22.10.2026):**', '**Historischer Formatwechsel 3.44.0 (22.10.2026):** Aufgabenformat 26 (FP-02), FP-01 und WA-27–WA-30 sowie die obersten Einstellungsnamespaces von FP-03/FP-04 wurden als Python-Fassung geliefert. [Datierter Schutznachweis](../tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). Damals konnten Pakete 3.42.0 Format 26 nur lesend öffnen. **Heute unterstützen die gelieferten nativen 3.45.0-Pakete und Python 3.47.0 Format 26; Quelle 3.49.0 ist noch nicht geliefert.** Aktuelle native/Menschenabnahmen und FP-01-Prüfadapterbefund getrennt im [QA-Bericht](07_QA_BERICHT.md).', 'Historische Altlesergrenze nicht als gegenwärtigen Paketstand darstellen')
replace(data, 'WA-40/WA-47, Quellkandidat 25.10.2026, noch keine Lieferung:', 'WA-40/WA-47: am 25.10.2026 als Quellkandidat umgesetzt, im späteren 3.45.0-Paketabschluss enthalten; native/Menschenabnahme bleibt offen.', 'Speicherstatus-Liefergrenze gegen späteren Lieferabschluss berichtigen')

line(analysis, '**Neuester Datei-/Dokumentabgleich ', '**Neuester Datei-/Dokumentabgleich 29.10.2026:** [§13.20](#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026) führt den Abnahmebericht lokal ein und berichtigt Status-/Modul-/Abschnittsverweise. Quelle 3.49.0, Python/Showcase 3.47.0, native Pakete 3.45.0. Historische Befunde, einschließlich §13.17 zu 3.48.0, bleiben an ihre damaligen Bytes gebunden. Der Dokumentabschluss ersetzt keine neue Funktions-, Markt- oder Releasefreigabe.', 'Neueste Analyse auf tatsächlichen Stand und Bericht beziehen')
changes[analysis][1] += '\n### 13.20 Einarbeitung des Abnahmeaudits und Dateiabgleich vom 29.10.2026\n\nDer [Abnahmebericht zum Prüfstand 28.10.2026](../01_Repository/Glide/tests/qa-3.49.0/abnahme_2026-10-28/README.md) bleibt als datierter Word-/PDF-Nachweis unverändert. Seine 52 überlappenden Abnahmeeinheiten und B01–B22 sind keine neue Roadmap. A01 bleibt offen: originale Wiederholen-Suite 8/9; saubere Sitzungsfreigabe besteht nur in der isolierten Diagnose, zwölf Folgesuiten wurden nicht gestartet. A02/A03/A04 bleiben unter den vorhandenen Kennungen offen: P8/4.0 und technische Restumfänge, WA-41A/B sowie aktuelle Lieferung und native/Menschenabnahmen. Aufgaben und Abnahmereihenfolge allein in [Plan §21.29](Glide_Entwicklungsplan.md#2129-abnahmeprüfung-des-begonnenen-umfangs).\n\n**A05 eingearbeitet:** Manuelle Prüfgrenze auf 3.49.0 aktualisiert, WA-12 anhand des späteren 3.45.0-Lieferabschlusses berichtigt, vier nicht existente Modulnamen durch die tatsächlichen Vorlagen-/Zeichen-/Animationszuständigkeiten ersetzt. Weitere widersprüchliche Einleitungen in Index, Architektur, Paket-/Prüf-/Quell-README und Arbeitsvorbereitung bereinigt; drei defekte Wiederanlauf-Abschnittsverweise korrigiert. Historische Tabellenwerte als Einführungs-/damalige Lieferwerte bezeichnet, aktuelle Statuszeilen nachgezogen. Der Bestand umfasst 89 direkte .py-Dateien sowie app.pyw und den separaten drawing_prototype.pyw, also 90 Laufzeitdateien plus einen Prototyp; die frühere Kurzform „89 .py einschließlich Prototyp“ war ungenau.\n\n[Dateiinventar, Dokumentregister, Verweise, Hashes und Schlusskontrollen](../01_Repository/Glide/tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md) trennen formale Vollständigkeit von offenem Funktions-/Lieferabschluss. Ein alter gefährlich missverständlicher Mac-Bauhinweis im Docstring des Python-Abgleichers wurde auf die separate Vorstufe und den nativen Paketbau präzisiert; ausführbare Logik ist AST-identisch. Keine App-/Lastprüfung, Änderung von Nutzerdaten, Paketneubau, Gitaktion oder Releasefreigabe aus diesem Pflegeauftrag.\n'

prep = '00_Arbeitsvorbereitung/README.md'
line(prep, '**Aktuell 27.10.2026:**', '**Aktuell 29.10.2026:** Quelle 3.49.0 als uncommitteter Prüfkandidat, Python/Showcase 3.47.0, native Pakete 3.45.0. [Abnahmeaudit](../01_Repository/Glide/tests/qa-3.49.0/abnahme_2026-10-28/README.md) und [lokaler Dokumentabgleich](../01_Repository/Glide/tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md): nicht alle begonnenen Arbeiten geschlossen, FP-01-Pflichtnachweis 8/9. Einstieg [Übergabe](Glide_Uebergabe.md), aktueller Rest [Plan §21.29](Glide_Entwicklungsplan.md#2129-abnahmeprüfung-des-begonnenen-umfangs). Die folgenden datierten Abschlüsse sind historisch.', 'Einstieg auf den aktuellen Dokument-/Abnahmestand bringen')
replace(prep, 'Der heutige Abstand 3.48.0/3.47.0', 'Der heutige Abstand Quelle 3.49.0 / Python 3.47.0 / native Pakete 3.45.0', 'Veraltete aktuelle Versionsgegenüberstellung korrigieren')
pkg = '01_Repository/Glide/packaging/README.md'
line(pkg, '**Aktueller Quellkandidat 3.48.0:**', '**Aktueller Quellkandidat 3.49.0:** Die 3.48.0-Bereiche sind um Wochenwahl, gemeinsame Fälligkeit/Aufwand, Verweisaktionen und die Schutzmodule ergänzt. Kopier-/Baulisten führen alle 90 Laufzeitdateien, einschließlich `session_guard.py` und `runtime_diagnostics.py`. Python/Showcase 3.47.0; native Pakete bleiben 3.45.0. Neue CI-Grundstufe grün, Originalsuite FP-01 8/9 und zwölf Folgesuiten gestoppt; WA-41 und aktuelle Lieferung/Abnahme bleiben offen. [Abnahmebericht](../tests/qa-3.49.0/abnahme_2026-10-28/README.md).', 'Aktuelle Paketquelle, Dateizahl und Liefergrenzen korrekt beschreiben')
src = '01_Repository/Glide/src/glide/README.md'
line(src, 'Lokaler Quellkandidat 3.48.0:', 'Bestandsumfang aus 3.48.0: Tagesnavigation, gemeinsame Wichtigkeit/Labels und Verweisnavigation; 3.49.0 ergänzt Wochenwahl, Fälligkeit/Aufwand, Verweisaktionen und Schutzmodule. Aktuell 90 Laufzeitdateien plus separater Zeichenprototyp, Format 26 unverändert. Python/Showcase 3.47.0, native Pakete 3.45.0; WA-41, FP-01-Prüfadapter und aktueller Liefer-/Abnahmeabschluss offen. [Abnahmebericht](../../tests/qa-3.49.0/abnahme_2026-10-28/README.md).', 'Aktuelle Quellstruktur und Abnahmegrenzen aktualisieren')
tests = '01_Repository/Glide/tests/README.md'
line(tests, 'Aktuell 3.48.0:', '**Aktuell 3.49.0:** [Abnahmeaudit](qa-3.49.0/abnahme_2026-10-28/README.md) auf eingefrorener Quelle: 220 Werkzeugtests (ein Skip), zweimal 1060 Fachtests und fünf Analysen grün; originale Wiederholen-Suite 8/9, zwölf Folgesuiten nach Fehlerstopp nicht ausgeführt. Korrektur des Prüf-Sitzungsabschlusses und erneuter Original-/Folgenachweis offen. Die 105 registrierten Suiten sind kein neuer bestandener Volllauf. Die 3.48.0-Belege mit 986 Fachtests/26 Arbeitsmodifällen bleiben [historisch](qa-3.48.0/dreierpaket_2026-10-27/README.md). Python/Showcase 3.47.0, native Pakete 3.45.0.', 'Aktuelle Testzahlen und roten Originalbefund statt alter grüner Teilmenge nennen')

add_top(plan, '**Lokale Einarbeitung 29.10.2026:** Abnahmebefunde und A05-Dokumentkorrekturen im bestehenden Aufgabenregister nachgeführt; [Analyse §13.20](Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026), [Bestands-/Dokumentnachweis](' + proof_root + '). §21.29 bleibt zuständig für den Abnahmerest; keine neue Featureauswahl oder Implementierung aus diesem Pflegeauftrag.')
changes[plan][1] += '\n**Einarbeitung 29.10.2026 zu §21.29:** A05 an den zuständigen Quellen berichtigt; [Analyse §13.20](Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026) und [Datei-/Dokumentnachweis](' + proof_root + '). A01–A04 bleiben offen. Der datierte Abnahmebericht wird nicht nachträglich auf grün umgeschrieben.\n'
add_top(handoff, '**Aktueller Pflegeauftrag 29.10.2026:** Abnahmebericht lokal in die Dokumentation eingearbeitet; [Ergebnis und vollständiger Dateiabgleich](' + proof_root + '), [inhaltliche Korrekturen Analyse §13.20](Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026). Quelle 3.49.0, Python/Showcase 3.47.0, native Pakete 3.45.0. A05 berichtigt; A01–A04, insbesondere FP-01-Prüfadapter, technische Restarbeiten, WA-41 und Liefer-/Abnahmetore offen. Nächste Entwicklungsarbeit erst mit dem korrekten Prüf-Sitzungsabschluss und unveränderten Originalkriterien beginnen; diese Runde ist Dokumentpflege.')
replace(handoff, 'Neue Schutzfunktionen offen; kein weiterer Test-/Code-/BIOS-/Git-/Lieferauftrag aus diesem Dokumentationsnachlauf.', 'Damals waren die Schutzfunktionen offen; inzwischen gezielt in 3.49.0 umgesetzt, siehe §21.27 und Abnahmegrenzen oben. Aus jenem Dokumentationsnachlauf selbst entstand kein Test-/Code-/BIOS-/Git-/Lieferabschluss.', 'Alte Auftragsgrenze nicht als aktuellen Implementierungsstatus stehen lassen')
replace(handoff, 'Wiederanlaufprüfung mit Originalvorsicherung und lesendem Fehlerzustand entwerfen', 'implementierte Wiederanlaufprüfung mit Originalvorsicherung und lesendem Fehlerzustand bewahren', 'Bereits implementierten Wiederanlauf nicht erneut als Entwurf beauftragen')
replace(handoff, '**3.48.0 ist nicht geliefert oder freigegeben.**', '**Quelle 3.49.0 einschließlich der 3.48.0-Funktionen ist nicht aktuell geliefert oder freigegeben.**', 'Sofortübergabe auf aktuelle Quellversion beziehen')
add_top(direction, '**Aktueller Pflegeauftrag 29.10.2026 (Wortlaut):** „bitte lokal ein arbeiten und prüfen dass die Dokumentation und alle Dateien uktuell und vollständig sind.“ [Inhaltlicher Abgleich](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026), [Datei-/Dokumentnachweis](../tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Abnahmebericht an zuständigen Quellen eingearbeitet, historische Prüfergebnisse erhalten. Keine Appreparatur, neue Version, Lieferung oder Git-/Releaseaktion aus diesem Auftrag.')
add_top(qa, '**Lokaler Dokumentabgleich 29.10.2026:** A05 des Abnahmeberichts an den zuständigen Quellen berichtigt; Index, aktuelle Statusmatrizen, Modulnamen, Wiederanlaufverweise und manuelle Prüfgrenzen abgeglichen. [Inventar, Register und tatsächlich ausgeführte Kontrollen](../tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Der datierte Abnahmebericht bleibt unverändert; A01–A04 und Originalsuite FP-01 8/9 bleiben offen. Dieser Dokumentnachlauf ist keine erneute App-/Last-/Native-Prüfung.')
add_top(index, '**Lokaler Standabgleich 29.10.2026:** [Dokument-/Dateinachweis](../tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md); [Abnahmebericht zum 28.10.2026](../tests/qa-3.49.0/abnahme_2026-10-28/README.md) mit weiter offenen Funktions-/Liefer-/Abnahmetoren.')
changelog = '01_Repository/Glide/CHANGELOG.md'
replace(changelog, '## 3.49.0 (28.10.2026) – Tagesplanung, Verweise und geschützter Wiederanlauf\n', '## 3.49.0 (28.10.2026) – Tagesplanung, Verweise und geschützter Wiederanlauf\n\n- **Dokumentpflege 29.10.2026:** Abnahmeaudit lokal eingearbeitet, überholte Modul-/Versions-/Lieferangaben und drei Wiederanlauf-Abschnittsverweise korrigiert; aktuelle Statusmatrizen und manuelle Prüfliste nachgeführt. Datierter Bericht unverändert, FP-01-Prüfadapter und weitere Abnahmetore offen. [Datei-/Dokumentnachweis](tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Keine Laufzeitänderung oder neue Lieferung.\n', 'Dokumentnachlauf ohne Versionswechsel im Änderungsverlauf verzeichnen')
docpolicy = '01_Repository/Glide/docs/DOKUMENTENPFLEGE.md'
add_top(docpolicy, '**Lokaler Abgleich 29.10.2026:** Abnahmebefunde in den zuständigen Quellen eingearbeitet; [Analyse §13.20](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026), [Dateiinventar/Dokumentregister/Schlusskontrollen](../tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Der Word-/PDF-Bericht bleibt ein unveränderter datierter Prüfbeleg. Historische QA-Rohdaten, Originalreferenzen und Lieferstände werden nicht umetikettiert oder aus diesem Abgleich gelöscht.')
root_readme = 'README.md'
line(root_readme, '**Aktueller Arbeitsstand:**', '**Aktueller Arbeitsstand 29.10.2026:** Quelle 3.49.0 mit Funktionsausbau und Schutzpaketen; Python/Showcase 3.47.0, native Pakete 3.45.0. [Abnahmebericht](01_Repository/Glide/tests/qa-3.49.0/abnahme_2026-10-28/README.md) lokal eingearbeitet; [Dokument-/Dateiabgleich](01_Repository/Glide/tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Nicht alle begonnenen Arbeiten abgeschlossen: FP-01-Pflichtnachweis 8/9, WA-41 und technische Restumfänge sowie aktuelle Lieferung/native/Menschenabnahme offen. BIOS-/CPU-Einstellungen unverändert.', 'Projektstart auf tatsächlichen aktuellen Arbeits-/Abnahmestand bringen')

tool = '01_Repository/Glide/scripts/pflege/abgleich_07.py'
replace(tool, '- Danach `python3 packaging/macos/baue_app.py --ziel build/macos` für das Bundle.', '- Eine reine Mac-Vorstufe mit externem Python ausschließlich nach\n  `build/macos-vorstufe` bauen: `python3 packaging/macos/baue_app.py --ziel build/macos-vorstufe`.\n  Eigenständige Pakete entstehen über `packaging/paket/baue_paket.py` bzw.\n  nativ `packaging/paket/baue_und_pruefe_macos.sh`; niemals die Vorstufe über\n  die geprüfte eigenständige Lieferung unter `build/macos` schreiben.', 'Veralteten Mac-Bauhinweis im Werkzeugdocstring an den verbindlichen Paketvertrag anpassen')
old_tree = ast.parse(changes[tool][0])
new_tree = ast.parse(changes[tool][1])
old_tree.body[0].value.value = new_tree.body[0].value.value = ''
assert ast.dump(old_tree) == ast.dump(new_tree)

# Geänderte aktuelle Dokumente erhalten den Pflegestichtag; historische Einträge behalten ihr Datum.
manifest = []
for name, (original, content) in changes.items():
    if name.endswith('.md'):
        content = content.replace('Stand 28.10.2026 · Glide 3.49.0', 'Stand 29.10.2026 · Glide 3.49.0', 1)
    result = content.encode('utf-8')
    assert result != original, name
    (ROOT / name).write_bytes(result)
    manifest.append({'path': name, 'before_sha256': hashlib.sha256(original).hexdigest(),
                     'after_sha256': hashlib.sha256(result).hexdigest(), 'reasons': reasons.get(name, []),
                     'runtime_ast_unchanged_except_module_docstring': True if name == tool else None})
(OUT / 'dokumentkorrekturen.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'{len(manifest)} Dateien gezielt korrigiert; Werkzeuglogik AST-identisch.')
