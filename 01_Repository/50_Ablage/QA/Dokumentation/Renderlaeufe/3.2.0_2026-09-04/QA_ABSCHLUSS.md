# Nachweis Dokumentation und externe Dateien

Stand: 04.09.2026 · App 3.2.0 · Datenformat 10

## Word-Endfassung

`10_Dokumentation\3.2.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx`

22 Seiten, alle finalen PNG-Seiten 1 bis 22 vollständig visuell geprüft.
Keine abgeschnittenen Texte oder Bilder, keine unlesbaren Zeichen, Tabellenköpfe
wiederholt, Fußzeilen unverändert positioniert. Zwei im Zwischenrender erkannte
Umbruchprobleme gezielt korrigiert. Historische Vorlage, Farben, Schriften,
17 Tabellen, Bild und 23 Navigationsziele erhalten. Titel-/Kapitelformat bleibt
auf Nutzerwunsch vorlagengetreu; keine generische Neugestaltung.

Export: installiertes Microsoft Word, unsichtbar und schreibgeschützt; kein
Save durch Word. Canonical `render_docx.py` mit vorhandenem Word-PDF als
Konverterfallback rasterisiert. LibreOffice ist nicht installiert. Die
Sandbox-Freigabe erlaubte den lokalen Word-Export; keine Ablehnung offen.

Endhash SHA-256: `cda607249da26745556f0efd597cae5d43214868e8b825adc99ee008a3a4f4e9`.
Referenzhash SHA-256: `9d436d134e9e52f9e6628c81e139ad7b3aaa5c8b20e4582ce1cf0c4cd7155cca`.
Strukturzählung Referenz/Final: `{'sectPr': [1, 1], 'tbl': [17, 17], 'drawing': [1, 1], 'bookmarkStart': [23, 23]}`.
23 TOC-Seitenzahlen stimmen mit den tatsächlichen Word-Bookmarks überein.
Alle nicht zur Bearbeitung freigegebenen Paketbestandteile sind bytegleich.
`docx_revision_manifest.json` nennt die gezielten Absatz- und Paketänderungen.

## Externe Fortschreibung

Entscheidungen 3.2.0 neu erstellt; Vorgänger 2.6.0/2.11.0 aus den aktiven
Bereichen in das jeweilige Archiv verschoben. Technische Fakten, manuelle
Prüfliste, importierbare TXT-Liste, Produktdatenblatt, Microsoft-/Apple-Angaben
und Bereichs-README sachlich fortgeschrieben. Alle Änderungen haben vorab
verifizierte Archivkopien, siehe `external_archive_manifest.json`.

Wesentliche Korrekturen: Schema 10; tatsächliche Dateien statt geplanter Module;
TXT kein vollständiges Backup; automatische Dateizugriffe korrekt beschrieben;
Systemanforderungen und gebündelte Laufzeit bis zum Build offen; Altersfreigabe
und Barrierefreiheit nicht als Codefakt behauptet; Einfrieren NICHT VERIFIZIERT;
Emoji-Ausnahmen und die reproduzierten Grenzen 21 Labels/Tiefe 101 offengelegt.

Store-Recherche unterscheidet MSI/EXE von MSIX und Mac Store von Direktvertrieb.
Quellen und Abrufdatum stehen direkt in den Plattformdokumenten. Die aktuelle
MSI/EXE-Quelle nennt keine Pixelgrenzen; diese bleiben UNGEKLÄRT. Preis,
Lizenz, Publisher, Kennungen und Vertriebsweg bleiben Inhaberentscheidungen.

Historische Daten, Python-Versionen, Dokumente, Bilder und Testeingaben behalten
ihren tatsächlichen alten Stand. Es wurde keine Datei gelöscht. Kein App-Code
und keine Repository-Datei wurde durch diesen Teilauftrag geändert.
