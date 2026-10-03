# Produktgrenzen und Produktprinzipien

Stand 03.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

Was Glide ist, was es nicht wird und woran jede neue Funktion gemessen wird. Am 03.10.2026 mit der Produktprinzipien- und UX-Prüfung vom 01.10.2026 zusammengeführt; deren Befunde U01–U24 stehen mit Status im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md). Die Vorfassungen trägt Git.

## Was Glide ist

- Eine deutschsprachige, lokale Desktop-Anwendung für Aufgaben, Listen, Notizen, Seiten, Notizbücher, Pinnwände, Galerien und Pixelzeichnungen. Leitsatz: *der ruhige, lokale Arbeitsplatz für den eigenen Tag – planen, erledigen, festhalten; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.*
- Kernfunktionen brauchen weder Internet noch Benutzerkonto oder Cloudservice. Kein automatischer Datentransfer, keine Telemetrie; nur ein angeklickter Link öffnet den Browser.
- Laufzeit: Python 3.14 mit Tk 9 und Standardbibliothek; mitgeliefert nur tkinterdnd2 und privat registrierte Schriften (DejaVu Sans, Pixelify Sans unter SIL OFL 1.1, Lizenztexte und Prüfsummen in `resources/fonts/provenance.json`). Eine neue Laufzeitabhängigkeit braucht eine dokumentierte Entscheidung.
- Plattformunabhängig: macOS, Windows, Linux; keine Funktion nur für eine Plattform (Antwort des Inhabers vom 30.09.2026). Mobile und ein Toolkit-Wechsel sind zurückgestellt (D03).
- Nutzerdaten liegen außerhalb des Programmordners und dürfen in einem extern synchronisierten Ordner liegen. Glide synchronisiert selbst nicht; die Belegungsdatei verhindert erkannte Fremdnutzung, kann aber zwei unsynchronisierte Cloudkopien nicht verriegeln. Nacheinander arbeiten: schließen, synchronisieren, am anderen Gerät öffnen.
- Erinnerungen und Systemmitteilungen (Option, Vorgabe aus) nur bei laufender App; verpasste Hinweise erscheinen gesammelt ([Systemintegration](decisions/SYSTEMBENACHRICHTIGUNGEN.md)).

## Was Glide nicht wird

| Thema | Grund |
|---|---|
| Konten, eigener Cloudservice, Mehrbenutzerbetrieb, Kommentare, Zuweisung | Produktgrenze |
| Gleichzeitige Bearbeitung auf zwei Geräten, Konfliktzusammenführung (G23) | Produktgrenze |
| Zustellung bei beendetem Programm (Stufe C), externe Kalender-/Mailintegration | Produktgrenze; ICS-Import/-Ausgabe sind Dateien, keine Synchronisierung |
| Mehrsprachigkeit | Produktgrenze |
| Eingebaute Cloud-KI, Spracherfassung, KI-Schnittstelle (MCP) | Q3: Austausch über Dokumente |
| Systemweiter Erfassungs-Hotkey (G07) | nur plattformeigen lösbar (Q2) |
| Einstieg für neue Nutzer, führender Begleiter, Touren | 25./27.09.2026 nicht gewählt; Rundgang und Showcase vorhanden |
| Eigene Felder je Liste, Datenbank-Baukasten | 25.09.2026 nicht gewählt; Felder, wenn sie kommen, Glide-weit |
| Unterseiten, Spalten in Seiten, Verweisgraph | 29./30.09.2026 entschieden |
| Allgemeine Umwandlung zwischen Liste, Notiz und Seite | D05 |
| Echte Transparenz oder Unschärfe je Widget | Tk kann das nicht; Milchglas ist eine Tönung |
| Bildbibliothek (etwa Pillow), allgemeines Textverarbeitungsprogramm | Abhängigkeit bzw. nicht Ziel |
| Gewohnheiten (G06), verschlüsselte Ablage (G22) | vorerst nicht |

Installer, Signatur, Store und Markenfreigabe sind gesonderte, offene Schritte ([Veröffentlichung](10_VEROEFFENTLICHUNG.md)). Die Kennungen `de.shaye.glide` und `Shaye.Glide` ändern sich nie.

## Sechs Produktprinzipien (Auftrag des Inhabers vom 01.10.2026)

| Prinzip | Bedeutung für Glide | Prüffrage | Kriterium |
|---|---|---|---|
| **P1 Funktioniert selbstverständlich** | Die naheliegende Handlung führt zum erwarteten Ergebnis, ohne Hinweistext; Systemkonventionen gelten (Hell/Dunkel, Kürzel, Esc, Entf, Doppelklick). | Geht es ohne Hinweis? | Keine Funktion nur über einen Dauerhinweis erklärbar |
| **P2 Form folgt Funktion** | Farbe = Rolle, Größe = Wichtigkeit, Position = Zusammenhang. | Würde die Funktion ohne dieses Element schlechter verstanden? | Jede Farbe mit genau einer Bedeutung; keine Dekoration im Standard |
| **P3 Keine Funktion doppelt** | Jede Absicht hat einen primären Weg; Menü und Kürzel dürfen ihn spiegeln. | Gibt es eine zweite Oberfläche für dasselbe Ergebnis? | Je Absicht eine Bedienoberfläche |
| **P4 Kein Platz verschwenden** | Inhalt vor Bedienung; Bedienelemente erscheinen dort und dann, wo sie gebraucht werden. | Wie viel Fläche zeigt Inhalt? | Bedienfläche über dem Inhalt ≤ 15 % bei 1280 × 800 |
| **P5 Nur das Wesentliche** | Der Standard zeigt das für die Tagesarbeit Nötige, alles andere ist erreichbar. | Würde man das Element vermissen? | Startseite sieben Kacheln (D12); Kopfzeile ≤ 4 Symbolknöpfe |
| **P6 Geringe Komplexität** | Wenige stabile Grundbegriffe (Aufgabe, Liste, Seite, Notiz, Ordner, Heute); neue Funktionen erweitern bestehende Orte. | Braucht es einen neuen Begriff, eine neue Ansicht, ein neues Fenster? | Neue Seitenleisteneinträge und Ansichten nur mit Entscheidung |

**Hausregeln** (seit 26./29.09.2026, gelten weiter):

- Keine Seitenleistenzeile ist ein zweiter Weg zu denselben Punkten; kein Symbol trägt zwei Bedeutungen (Bewegungspfeile ausgenommen); Knöpfe erscheinen, wo sie wirken; Bedienelemente ohne Wirkung werden ausgeblendet.
- Seitenleiste, Kopf und Inhalt springen nie; Kanten fluchten. Funktionen leben eingebettet in der Ansicht, nicht in Zusatzfenstern.
- Farben nach `BUTTON_ROLE_RULES`: Rot nur Löschen, Grün nur Bestätigen, festes Lila für Hinzufügen und Neu, Gelb für Hinweise, sonst neutral. Knöpfe nie von Hand einfärben.
- Mindestgröße 860 × 700 ohne Quetschen oder Anschneiden; jeder Text erreicht WCAG 2.2 AA in allen Designs.
- Hinweisblöcke in Seiten bleiben gestalterisch unverändert (D06); Hinweiszeilen der Ansichten werden einklappbar (D11).

**Was gut ist und bleiben soll:** Symbolfamilie aus einem Unicode-Block, berechneter Kontrast, Farbregeln nach Bedeutung, Rückgängig überall, Tagesnavigation, klappbare Seitenleistenbereiche, Leerzustände mit Gismo, Bibliothekskarten mit nächsten Aufgaben, Datensicherheit mit Vorsicherungen.

## Prinzipien-Check für neue Funktionen

Vor der Umsetzung in den Abschnitt der Version (Funktionen, Entwicklungsplan) aufnehmen und beantworten:

0. **Vorgeschichte:** schon entschieden, verworfen oder zurückgestellt? In dieser Datei, der [Arbeitsrichtung](ARBEITSRICHTUNG.md) und dem Entwicklungsplan prüfen; Entschiedenes nicht erneut vorlegen.
1. **Absicht** in einem Satz.
2. **Ort:** welcher bestehende Ort (Ansicht, Inspektor, Befehlspalette, Menü)? Wenn keiner: Begründung und Entscheidung.
3. **Doppelung:** gibt es schon einen Weg? Welcher entfällt?
4. **Sichtbarkeit:** was im Standard sichtbar, was bei Bedarf? Zusätzliche Dauerfläche in px bei 1280 × 800?
5. **Selbstverständlichkeit:** ohne Hinweistext? Welche Plattformkonvention?
6. **Farbe und Form:** Rolle aus `BUTTON_ROLE_RULES`, Symbol aus `ICONS`.
7. **Begriffe:** neue Wörter mit dem Glossar abgleichen (Aufgabe, Langtext, Zwischenüberschrift, Gruppe; „Punkt“ nur als Oberbegriff).
8. **Rücknahme:** ein Undo-Schritt; Wirkung vor dem Loslassen sichtbar (D02).
9. **Daten:** neues Feld oder Format? Datenformat-Tor, Altleser, Migration.
10. **Tempo:** Kosten je Aktion abhängig vom Bestand; Messung mit 1.000 und 10.000 Punkten.

## Grenzen einzelner Funktionen

| Bereich | Grenze |
|---|---|
| Zeichnung | 16–128 Zellen, eine bemalbare Ebene, höchstens 256 Farben, deckend weißer Grund; keine Vektorobjekte, Texte, Ebenen, Transparenz, Stiftdruck, Touchgesten, kein allgemeiner Fremd-SVG-Import. Mitgeliefert nur die eigene Palette |
| Seiten | ein Blatt ohne Unterseiten; Tabellen als ausgerichteter Text; Blöcke nicht einzeln mit der Maus ziehbar |
| Galerie und Vorschauen | Bilder sind lokale Anhänge; JPEG, HEIC, WebP, TIFF, BMP über das System (macOS `nsimage`/`sips`, Windows WIC, HEIC/WebP nur mit Store-Erweiterungen), unter Linux nur PNG, GIF, SVG |
| Kalender (ICS) | Import einer gegebenen Datei und Ausgabe als Datei; keine Synchronisierung, kein Abonnement, keine Teilnehmer, Ausnahmetermine oder VTODO; höchstens 2.000 Termine, 12 MB |
| CSV | Import mit Spaltenzuordnung; kein XLSX, keine Anhänge, Wiederholungen oder Erinnerungen aus Spalten, kein Abgleich mit Vorhandenem; 5.000 Zeilen, 64 Spalten, 12 MB |
| Druck und PDF | HTML-Druckansicht im Standardprogramm; kein eigener PDF-Schreiber, keine Druckerauswahl, ab 2.000 Punkten abgeschnitten |
| App-Backup | kein Cloudspeicher, kein Zeitplan, kein Zusammenführen, kein Passwortschutz |
| Änderungsverlauf | Aufgabenbestand, höchstens 15 Einträge und 15 Tage, abschaltbar; kein Wiederherstellen alter Werte |
| Planung | Bearbeitungstag und Aufwand erzeugen keine Fälligkeit; Kapazität je Wochentag, keine automatische Terminverteilung und keine Bewertung der arbeitenden Person |
| Gismo | spiegelt den Bestand, nie den Menschen; leitet aus Abschlüssen keine Bewertung ab |
