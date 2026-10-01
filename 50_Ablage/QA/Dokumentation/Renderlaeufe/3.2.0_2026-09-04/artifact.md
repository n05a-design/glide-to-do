# Ausführungskontrakt der DOCX-Fortschreibung

Referenz: `10_Dokumentation/2.6.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx`, vor Bearbeitung unverändert nach `10_Dokumentation/Archiv/` kopiert. Hash und vollständige Teileliste werden in `docx_revision_manifest.json` erfasst. 22 Referenzseiten mit Microsoft Word schreibgeschützt als PDF exportiert und über den canonical `render_docx.py`-Rasterprozess als PNG geprüft. LibreOffice ist auf diesem Host nicht verfügbar.

## Seite und Gestaltung

A4 Hochformat, eine Section, 11906 × 16838 twips. Ränder oben/unten 964, links/rechts 1134 twips. Kopf-/Fußabstand je 720 twips. Eine Spalte; zweispaltiges Inhaltsverzeichnis als vorhandene Tabellenstruktur. Alle 17 Tabellen, wiederholte Kopfzeilen, Zeilenschutz, Zellbreiten und Füllungen bleiben in ihrer Struktur erhalten. Arial Normal 9,5 pt; Heading 1 18 pt, Heading 2 13 pt, Heading 3 10,5 pt, Title 28 pt, Subtitle 12 pt. Codeblöcke Consolas. Direkte Titelgestaltung, blaue Überschriften, farbige Hinweise, Linien und Kopf-/Fußzeilen werden aufgrund der Vorlagenbindung beibehalten.

## Inhaltsstruktur und Slots

23 Kapitel in unveränderter Reihenfolge: Management, Ausgangslage, Vorbereitung, offene Punkte, Branding, Struktur, Zuständigkeiten, Ticketvorlagen, Regeln, Dokumentationssystem, Identität, Accounts, QA, Fixtures, Release-Artefakte, Security, Grafikworkflow, Vorbereitung, Phasen, Prinzipien, Releaseworkflow, nächste Schritte, Quellen.

Editable Slots sind die indizierten Absätze in `revise_docx.py`, bezogen auf `word/document.xml` `.//w:p`. Ersetzt werden Version/Schemabezug, aktuelle Funktionen, reale Dateistruktur, Prüfstatus, Bindung an aktuelle AGENTS, offene Identitäten und nächste Arbeit. Historischer Screenshot, Bildbeschriftung, frühere Abbruchrekonstruktion und Ticketvorlagentexte bleiben historische Referenzen. Alte aktive Fantasie-Dateistruktur wird durch reale Dateien ersetzt; der kürzere Umfang darf den Seitenfluss verändern. Überschriften-Bookmarks bleiben erhalten.

## Erhalt und Navigation

Unverändert: Styles, stylesWithEffects, theme, numbering, Bilder, Schriftentabelle, Custom XML, alle Relationships, Content Types, WebSettings und sämtliche nicht explizit geänderten Paketbestandteile. Geändert: document.xml, Fußzeilendatum und Core-Metadatum. Die Endfassung aktualisiert die statischen TOC-Seitenzahlen anhand tatsächlich in Word paginierter Bookmarks. PAGE-Felder bleiben native Felder.

## Prüfgates

Archivhash unverändert; alle Preserve-only-Paketteile bytegleich; gleiche Section-Geometrie; gleiche Tabellen-/Bild-/Bookmark-Anzahl. Jede Endseite bei vollständiger Ansicht auf Überlauf, falsche Umbrüche, Tabellen- und Fußzeilenlage prüfen. Gegenüber Referenz sind nur durch aktualisierte Textslots verursachte Flussänderungen erlaubt. Interne TOC-Ziele und Seitenzahlen müssen zum finalen Render passen.

Gezielte Layoutkorrektur nach Sichtprüfung: Kapitel 4 beginnt auf neuer Seite; der Produktgrenzen-Codeblock bleibt zusammen mit seiner Einleitung. Dies beseitigt zwei tatsächlich im Zwischenrender festgestellte verwaiste Teilblöcke.
