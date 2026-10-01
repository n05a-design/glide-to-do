# Produktgrenzen

Stand 01.10.2026 · Glide 3.32.3 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Glide ist eine deutschsprachige lokale Desktop-Anwendung für Aufgaben, Listen, Notizen, Zeichnungen und Ordner. Kernfunktionen benötigen weder Internet noch Benutzerkonto oder Cloudservice. Laufzeit: Python, Tk und Standardbibliothek, mitgelieferte privat registrierte Schriften. Nutzerdaten liegen außerhalb des Programmordners.

Aufgaben, Gruppen, Long-Tasks, Überschriften, verschachtelte Ordner, Labels, Wichtigkeit, Fälligkeit, Wiederholungen, Benachrichtigungen, Papierkorb, Undo, Suche, Kalender, Startseite, Vorlagen und Backup/Import gehören zum Produkt. Die UI-Änderungen einschließlich einheitlicher Dropdowns und interner App-Aktionen beschreibt der [3.9-Vertrag](archiv/32_UI_UND_BEDIENUNG_3.9.0.md).

Benachrichtigungen werden bei laufender App verarbeitet. Verpasste Hinweise erscheinen gesammelt; Dock oder Taskleiste können hervorgehoben werden. Keine Systemzustellung bei beendetem Programm. Die Umbenennung ändert diese Betriebsgrenze nicht. [Systemintegration](decisions/SYSTEMBENACHRICHTIGUNGEN.md).

Nutzerdaten dürfen in einem extern synchronisierten Ordner liegen. Glide synchronisiert selbst nicht. Die Belegungsdatei verhindert erkannte Fremdnutzung, kann aber nicht zwei noch unsynchronisierte Cloudkopien verriegeln. Nacheinander arbeiten: schließen, vollständig synchronisieren, am anderen Gerät öffnen. [Datenvertrag](06_DATA_BACKUP_MIGRATION.md).

Materialdarstellung verwendet getönte opake Tk-Flächen und Kanten, optional Windows-DWM. Keine echten transparenten oder unscharfen Flächen pro Widget. Symbole stammen aus `ICONS`. Schriftressourcen: DejaVu Sans 2.37 und Pixelify Sans (SIL OFL 1.1, nur Überschriften im Design „Pixel“), jeweils mit Lizenztext und Prüfsummen in `resources/fonts/provenance.json`.

Außerhalb des Produkts bleiben Mehrbenutzerbetrieb, Konfliktzusammenführung, eigener Cloudservice, Telemetrie, Push bei geschlossener App, externe Kalender-/Mailintegration und Mehrsprachigkeit. Notizlisten besitzen seit 3.26 einen lokalen Rich-Text-Editor mit begrenztem Formatumfang; ein allgemeines Textverarbeitungsprogramm ist nicht Ziel. Betriebssystem-Schreibtools werden nicht nachgebildet. Installer, Signatur, Storeveröffentlichung und Markenfreigabe sind gesonderte, offene Schritte.

Historische Funktions- und Detailverträge bleiben im [Dokumentationsindex](00_INDEX.md) erhalten. Aktueller Prüfstand: [QA](07_QA_BERICHT.md).

3.29 ergänzt Zeichnungsseiten: eine feste Fläche mit 128 × 128 Zellen, eine bemalbare Ebene, Pinsel, 4er-Füllung und Pipette, deckend weißer Hintergrund, höchstens 256 Farben je Zeichnung. Ein lokales PNG kann als nicht bemalbare Referenz dienen oder nach Vorschau nachgezeichnet werden. Keine Vektorobjekte, Texte, Ebenenmischung, Transparenz, Stiftdruck oder Touchgesten, kein allgemeiner Fremd-SVG-Import und keine PNG-Ausgabe. Listen- und Ordnerart sind nach der Anlage fest. [Vertrag 3.29](65_ZEICHNUNGSSEITE_3.29.0.md).

3.30 erweitert die Zeichnung zur Pixel-Werkstatt.

- **Neu:**
  - Flächen 16, 32, 64 oder 128 Zellen;
  - Linie, Rechteck, Ellipse, Auswahl, Symmetrie und Muster;
  - Paletten-Import und -Export als `.gpl`/`.hex` (mitgeliefert nur die
    eigene Palette);
  - PNG-Export in ganzzahligen Vergrößerungen bis 2048 px.
- **Weiterhin nicht:** Vektorobjekte, Texte, Ebenen, Transparenz,
  Stiftdruck oder Fremd-SVG.
- **Grenzen bleiben:** Archiv, Pixelsymbole, Spaltenboard, Detailbereich
  und das Design „Pixel“ bleiben lokal und ohne neue Laufzeitabhängigkeit.
  Die Pixelschrift „Pixelify Sans“ ist seit dem Ausbau vom 25.09.2026 eine
  mitgelieferte Ressource unter SIL OFL 1.1: Weitergabe mit Glide erlaubt,
  Verkauf der Schrift allein nicht, Lizenztext liegt bei.

[Vertrag 3.30](66_MODERNISIERUNG_3.30.0.md).

Seit dem 26.09.2026 gelten außerdem:

- **Mindestgröße:** 860 × 700. Dort bleiben die wichtigsten Bestandteile,
  nichts wird gequetscht oder angeschnitten; Weichendes ist über „⋯“,
  Kontextmenü, Menüleiste oder Kürzel erreichbar.
- **Kontrast:** Jeder Text erreicht in allen Designs WCAG AA (4,5:1, große
  Schrift 3:1).
- **Hintergrundverläufe:** Je Design fünf Verläufe zur Wahl, standardmäßig
  aus. Sie sind Atmosphäre, und Text auf dem Verlauf hält 4,5:1.
  - Kacheln, Listen und Fenster tönen sich als Milchglas nach dem Verlauf
    hinter ihnen, soweit die Schrift darauf 4,5:1 hält.
  - Echte Durchsicht kann Tk nicht.
- **Seiten (26.09.2026):**
  - Eine Seite ist zum Lesen und Schreiben da, vor allem für KI-Berichte.
    Eine Notiz (Notizbuch) ist etwas anderes und bleibt getrennt.
  - Aufgaben in Seiten sind vollwertige Punkte.
  - Felder sollen, wenn sie kommen, Glide-weit gelten, nicht je Liste.
  - Seit dem 27.09.2026 haben Seiten einen eigenen Bereich in der
    Seitenleiste und die Funktionen von Listen (Vorlagen, eigenes
    Austauschformat); Aufgaben und Labels teilen sie mit den Listen.
- **Kompakt (27.09.2026):** Der Kopf zeigt Titel und eine Zeile, keine
  zweite Zeile nur für die Beschreibung. Titel von Listen, Seiten und Ordnern
  haben höchstens 40 Zeichen.
- **Galerie (27.09.2026):** Eine Sammlung von Bildern ist eine Galerie. Die
  Bilder sind Anhänge und bleiben lokal.
  - Eine Bildbibliothek (etwa Pillow) ist keine Laufzeitabhängigkeit. JPEG,
    HEIC, WebP, TIFF und BMP zeigt Glide deshalb über das System: unter macOS
    über Tk 9 `nsimage` bzw. `sips`, unter Windows über die
    Windows-Bildkomponenten (WIC; HEIC/WebP nur mit den Store-Erweiterungen).
    Unter Linux bleiben es PNG, GIF und SVG (`image_preview.py`; korrigiert
    01.10.2026).
- **Form folgt Funktion (26.09.2026):** Jede Fläche hat eine eigene Aufgabe.
  - Keine Seitenleistenzeile ist ein zweiter Weg zu denselben Punkten:
    „In Bearbeitung“ steht in „Mein Tag“, der Verlauf ist ein Knopf.
  - Kein Symbol trägt zwei Bedeutungen: ↶ heißt nur „Rückgängig“, „+“ nur
    „Neu anlegen“, ✎ nur „Bearbeiten“.
  - Knöpfe erscheinen dort, wo sie wirken: die Auswahlleiste nur mit
    Auswahl; unter dem Listenbaum steht kein zweiter Weg zum „+“.
  - Farbe trägt Bedeutung: Grün bestätigt, Rot löscht, Lila fügt hinzu (seit 29.09.2026, `BUTTON_ROLE_RULES`), sonst neutral grau.
  - Bedienelemente ohne Wirkung in einer Ansicht werden dort ausgeblendet.
- **Produktprinzipien (Auftrag des Inhabers vom 01.10.2026):** Die
  Weiterentwicklung richtet sich nach sechs Grundsätzen. Sie ergänzen „Form folgt
  Funktion“; prüfbare Kriterien und die Prüfvorlage für neue Funktionen stehen
  in der [UX-Prüfung](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md).
  - Apple-like: Es funktioniert möglichst selbstverständlich.
  - Form follows function: Gestaltung unterstützt die Funktion, nicht umgekehrt.
  - Keine Funktion doppelt.
  - Kein Platz wird unnötig verschwendet.
  - Nur das Wesentliche anzeigen, dieses klar und wirkungsvoll.
  - Möglichst geringe Komplexität für den Nutzer trotz umfangreicher Funktionen.
- **Kennungen:** `de.shaye.glide` und `Shaye.Glide` sind festgelegt und
  ändern sich nie mehr. Ein macOS-Entwicklungsbundle ist ein
  Hilfsmittel für den Eigengebrauch, kein Release.

3.11 ergänzt Schnellerfassung und gespeicherte Filter; 3.12 ergänzt „Mein Tag“ als bewusste Tagesauswahl über vorhandene Punktobjekte; 3.13 ergänzt die Tabellenansicht mit listenspezifischer Spaltenauswahl. `SavedFilters`, `today_plan` und `table_columns` werden additiv in den Einstellungen normalisiert. Aufgabenformat 13 blieb dabei unverändert; Filter, Tagesauswahl, Tabellenlayout, Reiter und Pinnwände sind keine Aufgabenbackups. Bearbeitungen laufen durch `item_change`, modale Auswahl durch `run_modal`. [Bedienung 3.13](archiv/36_TABELLENANSICHT_3.13.0.md) · [Bedienung 3.12](archiv/35_MEIN_TAG_3.12.0.md).

Bearbeitungstag und geschätzter Aufwand sind seit 3.14 freiwillige Aufgabenfelder in Datenformat 14. Sie erzeugen weder Fälligkeiten noch Tagesauswahlen. Gruppen und Überschriften tragen keine Planung. [Bedienung 3.14](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md).

3.21 ergänzt den Kalenderimport: Glide liest eine ICS-Datei, die man ihm gibt – keine Synchronisierung, kein Abonnement, kein Netzzugriff und kein Abgleich, der vorhandene Punkte aktualisiert. Keine Teilnehmer, Anhänge oder Ausnahmetermine, keine VTODO-Einträge, keine Zeitzonendefinitionen aus der Datei. Nicht abbildbare Wiederholungsregeln und Erinnerungen werden verworfen und gezählt statt still vereinfacht; Grenzen sind 2000 Termine und 12 MB je Datei. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

3.20 ergänzt die Kalenderausgabe als ICS-Datei: eine Ausgabe, keine Anbindung. Keine Synchronisierung und kein Rückweg aus dem Kalender, kein Konto, kein Netzzugriff, keine automatische Neuausgabe; keine VTODO-Ausgabe, keine Teilnehmer, Orte oder Ausnahmetermine, keine mitgelieferte Zeitzonentabelle. Punkte ohne Fälligkeit können mit Bearbeitungstag und eingeschalteter Planungsoption als Planungstermin erscheinen; die Ausgabe enthält höchstens 2000 Termine. [Bedienung 3.20](archiv/44_KALENDERAUSGABE_3.20.0.md).

3.19 ergänzt den dauerhaften Änderungsverlauf und hebt das Aufgabenformat auf 15. Protokolliert wird der Aufgabenbestand – nicht Einstellungen, Vorlagen, Reiter, Pinnwände oder gespeicherte Filter. Kein Wiederherstellen alter Werte aus dem Protokoll, keine alten Feldinhalte, keine Verlaufsansicht am einzelnen Punkt, kein Benutzer- oder Gerätebezug, keine Synchronisierung; abschaltbar. Obergrenze seit 3.26.0 höchstens 15 Einträge und 15 Tage (`MAX_HISTORY_ENTRIES`, `HISTORY_RETENTION_DAYS`; ursprünglich 4000 Einträge, korrigiert 01.10.2026). [Bedienung 3.19](archiv/43_AENDERUNGSVERLAUF_3.19.0.md).

3.18 ergänzt den CSV-Import mit Spaltenzuordnung: Trennzeichen und Kodierung werden erkannt und sind umstellbar, jede Spalte wird einem Glide-Feld zugeordnet, eine Vorschau zeigt das Ergebnis vor der Übernahme. Kein XLSX, keine Anhänge, keine Wiederholungen oder Erinnerungen aus einer Spalte, kein Abgleich mit vorhandenen Punkten, kein gespeichertes Zuordnungsprofil; Grenzen sind 5000 Zeilen, 64 Spalten und 12 MB je Datei. [Bedienung 3.18](archiv/42_CSV_IMPORT_3.18.0.md).

3.17 ergänzt die Druck- und PDF-Ausgabe: vier Formate als eigenständige HTML-Druckansicht, geöffnet im Standardprogramm des Systems. Kein eigener PDF-Schreiber, kein Seriendruck, keine Druckerauswahl in Glide, kein DOCX-/XLSX-Export; ab 2000 Punkten wird abgeschnitten. [Bedienung 3.17](archiv/41_DRUCK_UND_PDF_3.17.0.md).

3.16 ergänzt ein vollständiges App-Backup: Aufgaben, Anhänge, Einstellungen, Vorlagenkatalog und Aktivitätsdaten in einem Archiv, wiederherstellbar mit Inhaltsvorschau und einzeln zuschaltbaren Bereichen. Kein Cloudspeicher, kein Zeitplan, kein Zusammenführen zweier Bestände, kein Passwortschutz. [Bedienung 3.16](archiv/40_APP_BACKUP_3.16.0.md).

3.15 fasst diese Angaben je Tag zusammen und vergleicht sie mit einer selbst gesetzten Tageskapazität. Die Anzeige nennt immer Grund und Bezugsgröße. Keine automatische Terminverteilung, keine Auslastungsquote über mehrere Tage und keine Bewertung der arbeitenden Person. Seit 3.30 gibt es Zeiterfassung je Punkt und eine Kapazität je Wochentag; eine Kapazität je Liste weiterhin nicht. [Bedienung 3.15](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).
