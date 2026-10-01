from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

out = Path(__file__).resolve().parents[2] / "10_Dokumentation" / "Glide_3.7.0_Auftragsabgleich_QA_Leistung.docx"
doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(.7); sec.bottom_margin = Inches(.7)
sec.left_margin = Inches(.75); sec.right_margin = Inches(.75)
styles = doc.styles
styles['Normal'].font.name = 'Aptos'; styles['Normal'].font.size = Pt(10.5)
styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Aptos')
for name, size, color in [('Title', 24, '15243C'), ('Heading 1', 16, '15243C'), ('Heading 2', 12, '44546A')]:
    st = styles[name]; st.font.name = 'Aptos Display'; st.font.size = Pt(size); st.font.bold = True; st.font.color.rgb = RGBColor.from_string(color)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = tcPr.find(qn('w:shd'))
    if shd is None: shd = OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'), fill)

def borders(table, color='D9E1F2'):
    tblPr = table._tbl.tblPr; b = tblPr.first_child_found_in('w:tblBorders')
    if b is None: b = OxmlElement('w:tblBorders'); tblPr.append(b)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        tag = 'w:' + edge; el = b.find(qn(tag))
        if el is None: el = OxmlElement(tag); b.append(el)
        el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:color'),color)

def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers)); t.alignment = WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'; borders(t)
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=h; shade(c,'15243C'); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in c.paragraphs[0].runs: r.font.bold=True; r.font.color.rgb=RGBColor(255,255,255); r.font.size=Pt(9)
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for i,val in enumerate(row):
            cells[i].text=str(val); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri%2==1: shade(cells[i],'F3F6FA')
            for p in cells[i].paragraphs: p.paragraph_format.space_after=Pt(2); p.paragraph_format.space_before=Pt(2)
    if widths:
        available = (sec.page_width - sec.left_margin - sec.right_margin) / Inches(1)
        widths = [w * available / sum(widths) for w in widths]
        t.autofit = False
        for column, width in zip(t.columns, widths):
            column.width = Inches(width)
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Inches(w)
    repeat_header = OxmlElement('w:tblHeader')
    t.rows[0]._tr.get_or_add_trPr().append(repeat_header)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
    return t

title = doc.add_paragraph(style='Title'); title.alignment=WD_ALIGN_PARAGRAPH.LEFT; title.add_run('Glide 3.7.0 Auftragsabgleich und Prüfnachweis')
p=doc.add_paragraph(); p.add_run('Stand 07.09.2026  ·  ').bold=True; p.add_run('Kanonischer Quellstand, Funktionsabgleich, Windows-QA und Datenformat 12')
doc.add_paragraph('Dieser Bericht führt alle ursprünglichen Gestaltungs- und Funktionswünsche mit den bestätigten Ergänzungen zusammen. Er erklärt, was im lokalen 3.7.0-Quellstand umgesetzt ist, welche Grenzen bewusst gelten und welche Freigaben vor einer Veröffentlichung noch auf echten Zielgeräten erforderlich sind.')

doc.add_heading('Entscheidung und aktueller Stand', 1)
doc.add_paragraph('Glide 3.7.0 ist als lokale Python/Tk-Anwendung mit Aufgabenformat 12 umgesetzt. Listen und Ordner tragen nun ebenfalls verwaltete Anhänge. Die 3.7-Funktionen wurden im vorhandenen Quellstand vervollständigt und mit isolierten Daten geprüft. Der Stand ist ein getesteter Entwicklungsstand; ein signiertes Installationspaket oder ein Store-Release ist nicht Bestandteil dieses Nachweises.')
table(['Bereich','Ergebnis'],[
['Kanonische App','01_Repository/Glide/src/glide/app.pyw · VERSION 3.7.0'],
['Daten','Format 12 · Einstellungen 2 · Vorlagenformat 1'],
['Windows-Prüfumgebung','Windows 11 Build 26200 · Python 3.12.7 · Tk 8.6.13'],
['Schrift','DejaVu Sans, vier TTF-Schnitte, privat registriert; Windows geprüft'],
['Automatische Suiten','10 Suiten plus Syntax, Version, Dokumentation, Fixtures, Analysen und Bilder'],
['Materialoptik','Getönte Flächen, Kontur und Schatten; selektiver Desktop-Blur durch Tk nicht nachgewiesen'],
], [1.6,5.7])

doc.add_heading('Vollständiger Auftragsabgleich',1)
rows=[
('1–3','Seitenleiste, Logo, Konturen','Umgesetzt','Zweispaltige Systemnavigation, optisch zentriertes Monogramm und farbige Startseitenkonturen.'),
('4–6','Farbige Arten/Ziele, vollständige Anlage','Umgesetzt','Artlabels und Listen-/Ordnerfarben in allen Auswahlwegen; Liste/Ordner mit Titel, Farbe, Elternordner, Labels, Beschreibung und Vorlage.'),
('7–8','TTF ohne Installation, Datenordner','Umgesetzt mit Grenze','Private Fontregistrierung; Datenordner öffnen/kopieren, Zeiger, Fremdsperre und Schreibschutz. Kein Synchronisationsdienst.'),
('9–10','Einstellungen und verzögertes Umbenennen','Umgesetzt','Scrollbarer Dialog; Akzent, Schrift, Startansicht, Wochenbeginn, Schalter; einzeilige Punkte per verzögertem Klick, F2/Doppelklick Details.'),
('11','Runde Auswahl','Teilbereich bewusst','Labelchips und Kalendertage selbst gezeichnet; native Treeview-Auswahl und Tk-Menüs bleiben rechteckig.'),
('12–14','Vorlagenseite, Export/Import, Startseitenverweis','Umgesetzt','Bearbeiten/Speichern-Gate, 10 Listen- und 2 Ordnervorlagen, glidetemplates, Teilbackup mit Anhängen und ergänzender Import.'),
('15–16','Scrollbar und Kontext-Export','Umgesetzt','Startseiten-Scrollbar nach rechts; Liste/Ordner als TXT, Markdown oder Glide-Teilformat.'),
('17–18','Analoge Elemente und Mondphase','Mond umgesetzt','Geometrische Mondsichel mit Name/Prozent; weitere Analogieideen bewertet.'),
('19–20','Jahresanzeige und Personalisierung','Umgesetzt','Rollierende Tageshistorie, Raster in der gewählten Akzentfarbe, Statistik; Schriftstufen, Startansicht, Wochenbeginn und Anzeige-Schalter.'),
('21–22','Glasprüfung und Dokumentation','Umgesetzt','Materialbericht mit nativen Alternativen, Leistungsdaten und klare Tk-/Plattformgrenzen; alle aktuellen Einstiege fortgeschrieben.'),
]
table(['Nr.','Thema','Status','Nachweis'],rows,[.55,1.55,1.25,3.95])

doc.add_heading('Windows-Prüfung',1)
doc.add_paragraph('Alle zehn automatisierten Suiten beendeten den aktuellen Lauf mit Exitcode 0: Kernfunktion, Datenintegrität, App-Audit, Dialog-Theme, UI-Erweiterungen, 3.7-Bausteine und End-to-End-Release. Zusätzlich waren statische und Erreichbarkeitsanalyse, Fixture-Reproduktion, Release-Abgleich und Windows-Screenshots erfolgreich. Der Lauf bestätigt den Quellstand; die getrennte manuelle Zielplattformprüfung bleibt offen.')
doc.add_heading('Erweiterungen in 3.7.0', 1)
feature_source = Path(__file__).parent / 'docs' / '25_FEATURE_ABGLEICH_3.7.0.md'
feature_section = feature_source.read_text(encoding='utf-8').split('## Nachfolgende UI-Korrekturen und Ergänzungen', 1)[1].split('## Personalisierung und weitere Gestaltungsideen', 1)[0]
feature_rows = []
for line in feature_section.splitlines():
    if line.startswith('| ') and not line.startswith('| Bereich '):
        parts = [part.strip().replace('`', '') for part in line.strip('|').split('|')]
        if len(parts) == 3:
            feature_rows.append(parts[:2])
table(['Rückmeldung', 'Aktuelles Verhalten'], feature_rows, [1.8, 5.5])
table(['Bereich','Umsetzung'], [
['Kachelübersicht','Listen und Ordner nutzen die volle Hauptbreite, werden kompakter dargestellt und bieten jeweils „Öffnen“ und „Bearbeiten“.'],
['Seitendetails','Zweispaltiges Fenster für Titel, Beschreibung, Farbe, Labels und lokale Anhänge an Listen und Ordnern.'],
['Datenformat 12','Containeranhänge werden in Backup, Import, Vorlagen, Kopien und Papierkorb übernommen; vor Migration entsteht eine unrotierte Originalkopie.'],
['Scrollen und Jahresraster','Diagramme und Label-Chips nehmen das Mausrad zuverlässig auf. Ein Tagesfeld zeigt beim Darüberfahren Wochentag, Datum und Bearbeitungszahl.'],
['Statistik','Gebuchte Erledigungen bleiben nach Löschen erhalten; die Bestandsanzeige zählt nur vorhandene Aufgaben.'],
], [1.7, 5.6])
doc.add_paragraph('Die Tageshistorien liegen in settings.json und werden rollierend aufbewahrt. Aufgabenbackups enthalten sie nicht; zur Übertragung dient die Kopie des gesamten Datenordners bei geschlossener App. Fehlende ältere Erledigungsereignisse lassen sich aus bereits gelöschten Aufgaben nicht rekonstruieren.')
table(['Prüfung','Ergebnis'],[
['Kern- und Datenintegrität','OK'],['App-Audit','OK · keine Befunde'],['Dialoge und UI','OK'],['3.7 End-to-End','OK · Anhänge, Labels, Vorlagen, Font, Rename, Tiefe, Datenordner'],['Fixtures und Releaseplanung','OK · Inhalt und relative Fristen abgeglichen'],['Sichtprüfung','Windows-Bilder erzeugt und angesehen; macOS/DPI/Accessibility/Langzeit offen'],
],[2.5,4.8])

doc.add_heading('Historische Leistungsmessung aus Version 3.6',1)
doc.add_paragraph('Die folgenden Zahlen stammen unverändert aus der Messung von Glide 3.6.0 vom 06.09.2026. Sie sind keine neue Leistungsmessung für 3.7.0. Die damalige lokale Messung nutzte flache synthetische Listen ohne Anhänge und drei Wiederholungen je Szenario. Sie dokumentiert die damalige Größenordnung und keine zugesicherten Antwortzeiten.')
table(['Aufgaben','Materialoptik','Render Median','Speichern'],[
['100','aus','28,33 ms','53,87 ms'],['100','an','8,39 ms','31,80 ms'],['1.000','aus','26,65 ms','81,43 ms'],['1.000','an','29,67 ms','69,34 ms'],['5.000','aus','137,26 ms','256,21 ms'],['5.000','an','144,73 ms','243,82 ms'],
],[1.1,1.5,1.6,1.6])
doc.add_paragraph('Startup der getesteten Instanz: 1.193,04 ms. Die Materialoptik erzeugt keine dauernden Desktopaufnahmen und keinen Blur pro Bild. Einzelne niedrigere Werte mit Materialoptik sind wegen Cache und Messrauschen kein Geschwindigkeitsvorteil.')

doc.add_heading('Glas- und Liquid-Glass-Entscheidung',1)
doc.add_paragraph('Apple Liquid Glass und Windows Mica/Acrylic beschreiben native Kompositions- und Materialebenen. Tkinter besitzt keine regionenbezogene Blur-Ebene für einen bereits gerenderten Desktop. Eine globale Fenstertransparenz würde auch Texte und Eingaben schwächen. Glide verwendet deshalb getönte deckende Ebenen, feine Licht-/Schattenkanten, klare Akzentfarben und einen optionalen Windows-DWM-Aufruf als best-effort Ergänzung. Die Arbeitsfläche bleibt ruhig und solid, die Navigation erhält Tiefe. Ein echter selektiver Blur wäre ein eigener WinUI-, AppKit- oder WebView-Kompositionszweig.')

doc.add_heading('Vor Veröffentlichung noch auszuführen',1)
doc.add_paragraph('Offen bleiben Anbieter- und Markenfreigaben, Support- und Datenschutzadressen, Lizenzmodell und Preis, Installer und Signierung, Zielarchitektur und Mindestbetriebssystem, reale DPI-/Mehrmonitor-/Accessibility-Prüfung, lange Nutzung, macOS sowie ein sequentieller Zwei-Rechner-Test mit synchronisiertem Datenordner. Die Sperrdatei warnt vor einem bekannten Fremdprozess, führt aber keine Offline-Konflikte zusammen.')
doc.add_paragraph('Die aktuellen technischen Details stehen in docs/24_VERSION_3.7.0.md, docs/25_FEATURE_ABGLEICH_3.7.0.md, docs/06_DATA_BACKUP_MIGRATION.md und docs/07_QA_BERICHT.md. Versionsgebundene Berichte für 3.6 und archivierte Vorfassungen bleiben historische Nachweise.')

doc.core_properties.title='Glide 3.7.0 Auftragsabgleich und Prüfnachweis'
doc.core_properties.subject='Funktionsabgleich, Windows-QA, Glasoberfläche und Leistung'
doc.core_properties.author='Glide Projekt'
doc.save(out)
print(out)

