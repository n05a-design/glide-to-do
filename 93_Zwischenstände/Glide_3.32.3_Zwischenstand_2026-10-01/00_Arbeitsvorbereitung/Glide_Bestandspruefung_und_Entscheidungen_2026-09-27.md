# Glide – Bestandsprüfung, offene Aufgaben und Entscheidungsvorlage

Stand 27.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · entschieden und umgesetzt (Abschnitt 6)

Auftrag: den Ordner auf Vollständigkeit prüfen, offene Aufgaben suchen, sie mit
dem Code abgleichen, weitere Änderungen recherchieren und alles als
Entscheidungsvorlage zusammenstellen.

## 1. Ergebnis in Kürze

- **Der Code ist vollständig und geprüft.** Seit der letzten Vollprüfung
  (27.09.2026, 12:02–12:21 Uhr, Exitcode 0) hat sich keine Quelldatei mehr
  geändert, nur Dokumente.
- **Die startbare Kopie ist bytegleich** mit dem Repository, alle zwölf
  Zwischenstände von 3.30 liegen startfähig im Archiv.
- **Die Doku ist verlinkt und indexiert:** 1.409 lokale Links in aktuellen
  Dokumenten, keiner defekt; jedes Dokument steht im Index.
- **Sieben kleine Doku-Lücken** (Abschnitt 2.2), keine davon betrifft den Code.
- **Offen sind vor allem Dinge, die nur du tun kannst:** 151 manuelle
  Prüfpunkte, das Logo als PNG, Inhaberangaben, Signatur und Store.
- **Die Recherche hat einen neuen Weg gefunden:** Das Python 3.14, mit dem
  Glide geprüft wird, bringt Tk 9 mit. Tk 9 kann Systembenachrichtigungen und
  SVG selbst, ohne zusätzliches Paket (Abschnitt 4).

## 2. Vollständigkeitsprüfung

### 2.1 Was geprüft wurde

| Prüfpunkt | Ergebnis |
|---|---|
| Code gegen letzten Prüflauf | `app.pyw` zuletzt 11:57 geändert, Vollprüfung `kompression_2026-09-27` ab 12:02: 60 Schritte ausgeführt, 2 plattformbedingt übersprungen (Bilder, Sichtprüfung), Exitcode 0 |
| Syntax | alle Quell- und Testdateien fehlerfrei lesbar |
| Versionen | `VERSION`, `APP_VERSION`, Changelog: 3.30.0; `DATA_SCHEMA_VERSION` 20 |
| Startbare Kopie `07_Python-Versionen` | `app.pyw`, `drawing.py`, `drawing_image.py`, `backdrop.py`, `page_markdown.py` bytegleich; `Schnellstart.pyw` = `glide_start.py` |
| Archivstände | 3.29.0 und alle 12 Zwischenstände von 3.30 (vor Ausbau … vor Kompression) samt README |
| Ressourcen | Schriften und Vorlagen gleich; nur alte Archivvorlagen (3.20–3.26) weichen zwischen Repository und Kopie ab – ohne Wirkung |
| Links und Index | 1.409 Links, 0 defekt; alle Dokumente in `docs/00_INDEX.md` |
| Paketierung | `baue_app.py` nimmt alle sechs Dateien mit (einschließlich `backdrop.py`, `page_markdown.py`, `glide_start.py`) |
| Probedaten `05_Probelisten_Testdaten` | Format 20, aber nur Aufgabenlisten und eine Zeichnung (siehe B-06) |
| Grafik, Store, Release | `20_Grafik_Master` und `30_Release_Exports` enthalten nur README und Archiv; `40_Store_Material` nur den Datenblatt-Entwurf |
| Handbuch in der App (F1) | deckt Seiten, Galerie, Bibliothek, Notizbuch, Hintergrund ab; die Auswahl-/Aktionsleiste vom 27.09. fehlt (B-07) |

### 2.2 Gefundene Lücken (nur Doku und Probedaten)

| Nr. | Befund | Ort |
|---|---|---|
| B-01 | „Kanonisch“ nennt nur `app.pyw`, `drawing.py`, `drawing_image.py`; es fehlen `backdrop.py`, `page_markdown.py`, `glide_start.py` | `docs/09_PROJECT_HANDOFF.md`, Abschnitt „Code und startbare Kopie“; dazu „samt beiden Modulen“ |
| B-02 | Gleiche Lücke in „Kanonische Dateien …“ und „Paket enthält …“ | `docs/10_RELEASE_CHECKLIST.md` |
| B-03 | „In der Agentenumgebung waren keine Bildschirmaufnahmen möglich“ – seit dem 27.09. gibt es Aufnahmen des eigenen Fensters | `Checklisten/Manuelle_Pruefung_3.30.0.md`, Rahmen |
| B-04 | Kopf „Stand 26.09.2026“, obwohl Läufe vom 27.09. drinstehen; die Zeilen stehen nicht zeitlich geordnet | `tests/qa-verlauf.md` |
| B-05 | Kopfzeilen mit „Stand 26.09.2026“ | `10_Dokumentation`, `20_Grafik_Master`, `40_Store_Material`, `Fehlerprotokolle` (README) |
| B-06 | Die Beispielbackups zeigen nichts von 3.30: keine Seite, Bibliothek, Galerie, kein Notizbuch, keine Pinnwand | `Glide-Funktionsvorschau_3.30.0.glidebackup` (14 Aufgabenlisten, 1 Zeichnung, 6 Ordner „standard“) |
| B-07 | Das Handbuch in der App nennt die Auswahl-/Aktionsleiste nicht | `MANUAL_SECTIONS` in `app.pyw` |

Außerdem: Das Konzept „Seiten wie Notion“ sagt in 3.5 noch „Aufgabenformat
21“; umgesetzt wurde additiv in Format 20 (Vertrag 66). Als Vorschlagsteil
darf das stehen bleiben, sollte aber einen Hinweis bekommen.

## 3. Offene Aufgaben und Abgleich mit dem Code

### 3.1 Bereits erledigt (Doku oder Gedächtnis nannten sie noch als „nächste Stufe“)

| Aufgabe | Stand im Code |
|---|---|
| Glide-weite Felder für Seiten | umgesetzt: Titel, Beschreibung, Farbe, Labels, Checkliste, Erstellt |
| Bibliothek als Tabelle | umgesetzt |
| „Notizbuch“ statt „Tagebuch“ überall | umgesetzt; „Tagebuch“ steht nur noch in Kommentaren, der Umbenennung alter Titel und dem Hinweis „Früher …“ im Handbuch |
| Titel höchstens 40 Zeichen | umgesetzt (`CONTAINER_TITLE_MAX = 40`) |
| Tooltip-Stapel, „fliegendes“ Fenster | behoben |

### 3.2 Wirklich offen

| Aufgabe | Quelle | Stand im Code | Wer |
|---|---|---|---|
| Manuelle Prüfung: 109 Punkte (3.30), 23 (3.29), 14 (3.28), 5 (Windows) | Checklisten | – | du |
| Windows-Vollprüfung mit `windows_vollpruefung.cmd` | Windows-Prüfliste | Paket liegt bereit | du (Windows-Rechner) |
| Logo als PNG ab 1024 px | Sitzungsprotokoll 6 | Bundle nutzt `Glide_Platzhaltersymbol.png` | du (Affinity) |
| Inhaberangaben: Copyright, Datenschutz-URL, Windows-Architektur, Inno-AppId, macOS-Mindestversion und -Architektur, Sicherheitskontakt | Produktregister | – | du (E-10, E-11) |
| Markenprüfung „Glide“ | Produktregister | – | Fachanwalt |
| Release-Build (PyInstaller), Signatur, Notarisierung, Installer | Release-Checkliste | nur ad-hoc-signiertes Entwicklungsbundle | du (Apple-Developer-Konto) + ich |
| Systembenachrichtigungen, Stufe B | Entscheidung Systembenachrichtigungen | Kennungen gesetzt, kein Aufruf vorhanden | E-04 |
| Seiten: Titelbild und Unterseiten | Konzept, Vertrag 66 §11 | nicht vorhanden | E-07 |
| Bibliothek zusätzlich als Galerie mit Titelbild | Konzept, Frage 2 (Rest) | nur Tabelle | E-07 |
| Galerie: JPEG/HEIC/WebP-Vorschau unter Windows und Linux | Vertrag 66 §11 | nur macOS über `sips` | E-05 |
| Galerie: Bilder aus Finder/Explorer ziehen | Vertrag 66 §11 | nicht möglich ohne Tk-Erweiterung | E-06 |
| Seiten: Blöcke mit der Maus ziehen, echte Tabellenzellen, mehrzeiliger Titel, Seite per Ziehen in Bibliothek | Vertrag 66 §11 | Grenzen von Weg A | E-07 (Vorrat) |
| Pixelschrift auf echtem Linux | Vertrag 66 §11 | nur mit nachgebildeter Bibliothek geprüft | offen, niedrig |
| Einmaliger Befund `test_glide` (Ordneransicht, Ziehen) | QA-Bericht | 4 Wiederholungen grün | E-12 |
| Optimierungen aus Konzept §5 (5 Vorschläge) | Konzept | nicht entschieden | E-08 |
| Funktionsvorschläge aus Konzept §6 (7 Vorschläge) | Konzept | nicht entschieden | E-09 |
| Rückfallwarnung (3.29 überschreibt Format 20) in Store-Texte | Release-Checkliste | steht in README und Datenblatt-Entwurf | mit Store |

Bewusst nicht gewählt und deshalb nicht offen: Einstieg für neue Nutzer,
eigene Felder je Liste, führender Begleiter, ZF-300 (Text, Vektor, Ebenen,
Animation), Stufe C der Benachrichtigungen.

## 4. Recherche: neue Möglichkeiten

### R-1 Tk 9 ist schon da

Geprüft auf diesem Mac: Python 3.14.5 bringt **Tk 9.0.3** mit. Der
Windows-Installer von Python 3.14 enthält Tk 9.0.4. Die Windows-Prüfläufe
bis 3.26 liefen noch mit Python 3.13 und damit Tk 8.6.

Was Tk 9 ohne zusätzliches Paket kann und Glide heute nicht nutzt:

- **`tk sysnotify` und `tk systray`:** echte Systembenachrichtigungen und ein
  Symbol in Menüleiste bzw. Infobereich. Unter macOS und Windows nutzt Tk die
  Systemschnittstellen, unter Linux libnotify mit Rückfall. macOS fragt beim
  ersten Mal um Erlaubnis. Auf diesem Mac ist der Befehl vorhanden
  (`::tk::systray`, `::tk::sysnotify`).
- **SVG als Bild:** `PhotoImage(format="svg")` funktioniert hier. Glide-SVGs
  und andere SVGs könnten in Galerie und Anhängen als Vorschau erscheinen.
- **`nsimage` unter macOS:** Tk kann Bilder über das System laden; das könnte
  den Umweg über `sips` (Unterprozess und Zwischendatei) ersetzen.

**Folge für die Entscheidung von 2026:** „Weder Stufe A noch Stufe B verlangen
ein zusätzliches Python-Paket“ bleibt wahr, und Stufe B braucht jetzt keinen
eigenen Systemaufruf mehr. Die Kopplung an die Paketierung bleibt, weil macOS
Mitteilungen einer registrierten App zuordnet; im ad-hoc-signierten
Entwicklungsbundle muss das am Gerät geprüft werden.

### R-2 JPEG-Vorschau unter Windows ohne Bildbibliothek

Wie `sips` unter macOS kann Windows selbst umwandeln: PowerShell mit
`System.Drawing` oder den Windows-Bildkomponenten (WIC). Das liest JPEG, BMP,
TIFF und GIF zuverlässig; HEIC und WebP nur, wenn die Microsoft-Erweiterungen
installiert sind. Keine neue Abhängigkeit, aber ein Unterprozess und ein Test
am Windows-Gerät.

### R-3 Ziehen aus Finder und Explorer

Tk hat dafür keinen eingebauten Weg; `tkinter.dnd` wirkt nur innerhalb der
App. Der übliche Weg ist die Tk-Erweiterung tkDnD über `tkinterdnd2`, mit
fertigen Bibliotheken für Windows, macOS (auch Apple Silicon) und Linux. Das
ist eine **neue Laufzeitabhängigkeit** mit nativem Code, also eine
Entscheidung nach AGENTS.md Regel 4. Im späteren Release-Build ließe sie sich
mitliefern; beim Start aus der `.pyw` müsste sie installiert sein.

### R-4 Release-Build

PyInstaller 6.22.3 (September 2026) unterstützt Python 3.8 bis 3.14 und
sammelt Tcl/Tk mit. Wichtig für die Vertriebsentscheidung: Eine
Einzeldatei-App funktioniert nicht mit aktivierter Sandbox, die der Mac App
Store verlangt. Für den Direktvertrieb (Developer-ID-Signatur und
Notarisierung) ist ein `.app`-Ordnerbundle der passende Weg.

### R-5 Ausblick

In CPython ist ein Modul `tkinter.systray` vorgeschlagen (Pull Request
gh-153260). Glide kann den Tk-Befehl schon heute direkt aufrufen und später
umsteigen.

## 5. Entscheidungen für dich

Jede Entscheidung hat eine Empfehlung. „Alle Empfehlungen“ reicht als Antwort.

### E-01 Doku-Lücken B-01 bis B-05 beheben

- **Empfehlung: ja, sofort.** Reine Textkorrektur, Archivkopie vorher,
  keine Produktwirkung.
- Alternative: mit der nächsten Runde erledigen.

### E-02 Probedaten auf 3.30 bringen (B-06) und Handbuch ergänzen (B-07)

- **Empfehlung: ja.** Die Funktionsvorschau bekommt je eine Seite (mit
  Aufgaben), Bibliothek, Galerie (mit PNG), ein Notizbuch und eine Pinnwand
  mit Bereichen. Das Handbuch bekommt einen Eintrag „Auswahlleiste“.
  `beispieldaten.py` und der Erzeugerabgleich werden angepasst.
- Alternative: Probedaten so lassen.

### E-03 Python 3.14 und Tk 9 als Grundlage

- **Empfehlung:** Release-Build mit Python 3.14 (Tk 9). Der Start aus der
  `.pyw` bleibt auch mit Tk 8.6 lauffähig; neue Tk-9-Funktionen greifen nur,
  wenn vorhanden, sonst bleibt das heutige Verhalten.
- Alternative A: Python 3.14 als Mindestvoraussetzung für alles.
- Alternative B: bei Tk 8.6 als Maßstab bleiben und Tk 9 nicht nutzen.

### E-04 Systembenachrichtigungen, Stufe B

- **Empfehlung: jetzt vorbereiten, standardmäßig aus.** Über `tk sysnotify`
  eine Sammelmeldung je Prüflauf („3 Erinnerungen fällig“), nur nach dem
  Zustellbeleg, mit Schalter in den Einstellungen und Hinweis, wenn das System
  die Erlaubnis verweigert. Im Entwicklungsbundle am Mac prüfen, unter Windows
  mit der Verknüpfung.
- Zusatzfrage: Soll Glide auch ein Symbol in Menüleiste bzw. Infobereich
  bekommen (`tk systray`)? **Empfehlung: nein**, nur als Voraussetzung, wo
  Tk es verlangt; ein ständiges Symbol wäre eine neue Form ohne eigene
  Funktion.
- Alternative: erst mit dem signierten Release.

### E-05 Bildvorschau in der Galerie

- **Empfehlung: ohne Abhängigkeit.** macOS über Tk (`nsimage`) mit `sips`
  als Rückfall, Windows über PowerShell/WIC, SVG über Tk 9. Linux zeigt
  weiter die Endung.
- Alternative A: Pillow als Laufzeitabhängigkeit (alle Formate, alle Systeme,
  aber Regel 4 und größere Pakete).
- Alternative B: so lassen.

### E-06 Bilder aus Finder/Explorer in die Galerie ziehen

- **Empfehlung: noch nicht.** Erst mit dem Release-Build entscheiden, weil
  `tkinterdnd2` native Bibliotheken mitbringt, die signiert und geprüft werden
  müssen.
- Alternative: jetzt aufnehmen, mit Rückfall auf „Bilder hinzufügen …“, wenn
  die Erweiterung fehlt.

### E-07 Seiten, nächste Stufe

- **Empfehlung: Titelbild zuerst, dann Unterseiten.**
  - Titelbild: lokales Bild, eigene Pixelzeichnung oder ein
    Hintergrundverlauf von Glide (Pixel-Nische). Es erscheint auch als
    Galerieansicht der Bibliothek (Umschalter Tabelle · Galerie, Rest von
    Frage 2).
  - Unterseiten: Seiten unter einer Seite im Bereich „Seiten +“, mit Pfad
    oben und „Hier erwähnt in …“.
- Offene Teilfragen:
  1. Wie tief dürfen Unterseiten reichen? Vorschlag: 5 Ebenen wie Ordner.
  2. Lesebreite umschaltbar auf volle Breite? Vorschlag: ja.
- Alternativen: nur Titelbild; nur Unterseiten; später.
- Vorrat, nicht empfohlen: Blöcke mit der Maus ziehen und echte
  Tabellenzellen (Weg B, in Tk bei langen Seiten träge).

### E-08 Leistung (Konzept, Abschnitt 5)

- **Empfehlung: die drei kleinen zuerst:**
  - Speichern im Hintergrund bündeln;
  - Bildvorschauen zwischenspeichern;
  - Fenster sofort zeigen, Daten danach laden.
- Danach, mittlerer Aufwand: Startseite auf einer einzigen Fläche (Scrollen
  etwa doppelt so schnell) und lange Listen nur mit sichtbaren Zeilen.
- Alternative: alle fünf; keine.

### E-09 Funktionsvorschläge (Konzept, Abschnitt 6) – Mehrfachwahl

| Vorschlag | Empfehlung |
|---|---|
| Schnellerfassung legt wahlweise eine Seite an | ja – passt zu „Seiten für KI-Berichte“ |
| Wiederkehrende Checklisten setzen sich nach dem Erledigen zurück | ja – klein, alltagsnah |
| Import aus Notion (Markdown/CSV) und Todoist, Export als Markdown | ja, zuerst Notion-Markdown – `page_markdown.py` liest Markdown schon |
| Tagesseite: Notizspalte in „Mein Tag“ | nein – würde „Mein Tag“ und das Notizbuch doppeln (Form folgt Funktion) |
| „/“-Befehle auch in Aufgabenlisten („/morgen“, „/wichtig“) | später – die Schnellerfassung erkennt Fristen schon |
| Fokusansicht: eine Aufgabe groß mit laufender Zeiterfassung | offen, deine Wahl |

### E-10 Vertriebsweg und Plattformen

- **Empfehlung: zuerst Direktvertrieb** (eigene Website, macOS mit
  Developer-ID-Signatur und Notarisierung, Windows mit Installer), Stores
  später. Der Mac App Store verlangt die Sandbox; das ist mit dem
  lokalen Datenordner und OneDrive-Ablage eine eigene Prüfung.
- Architektur: Windows x64; macOS Apple Silicon (arm64), Universal 2 nur
  wenn Intel-Macs gebraucht werden.
- macOS-Mindestversion: folgt aus dem gewählten Python 3.14; wird beim
  Build festgestellt.
- Voraussetzung, die nur du schaffen kannst: ein Apple-Developer-Konto
  (Developer-ID-Zertifikat) und für Windows ein Code-Signing-Zertifikat.

### E-11 Inhaberangaben im Produktregister

Vorschläge zum Bestätigen oder Ändern:

| Feld | Vorschlag |
|---|---|
| Copyright-Zeile | „© 2026 Tim von Trostorff“ |
| Datenschutz-URL | eine Seite unter shaye.de, z. B. `shaye.de/glide/datenschutz` (Inhalt: keine Datenerhebung, alles lokal) |
| Sicherheitskontakt | mailme@shaye.de, wie der Support |
| Inno-Setup-AppId | einmal erzeugen, danach nie ändern – kann ich anlegen, sobald du zustimmst |
| Logo | PNG-Export aus `Glide-Logo.af`, 1024 × 1024, transparent, nach `20_Grafik_Master` |

### E-12 Einmaliger Testbefund `test_glide`

- **Empfehlung: absichern** wie bei `test_ui_followup36`: die Stelle unter
  Last wiederholen und die Prüfung auf den stabilen Endzustand ausrichten,
  falls sie wieder auftritt.
- Alternative: weiter beobachten.

### E-13 Manuelle Prüfung verdichten

- **Empfehlung: ja.** Aus 151 Punkten in vier Listen wird eine
  priorisierte Kurzabnahme von etwa 30 Punkten: zuerst Datensicherheit und
  Umstellung, dann tägliche Bedienung, dann Darstellung. Überholte Punkte
  der 3.29-Liste fallen weg. Die langen Listen bleiben als Nachschlagewerk.
- Alternative: Listen unverändert abarbeiten.

## 6. Antworten des Inhabers und Umsetzung (27.09.2026)

Der Inhaber hat jede Entscheidung beantwortet. Umgesetzt ist alles in
[Vertrag 66, Abschnitt 2.14](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

| Nr. | Antwort | Umsetzung |
|---|---|---|
| E-01 | Doku-Lücken erst nach der Umsetzung schließen | erledigt nach der Umsetzung: B-01 Übergabe, B-02 Release-Checkliste, B-03 Prüfliste, B-04 QA-Verlauf (Stand, Reihenfolge), B-05 Standzeilen; B-07 Handbuch |
| E-02 | Probedaten danach: je Liste, Notiz, Seite (Funktionen mit Bildern) und Zeichnung | „Rundgang“ in `05_Probelisten_Testdaten` (Teilbackup, Erzeuger `tests/tools/rundgang.py`). Die Funktionsvorschau (B-06) bleibt unverändert, weil der Vollmodus sie gegen ihren Erzeuger prüft |
| E-03 | neueste Version nach Tests | Alle Prüfungen laufen mit Python 3.14.5 und Tk 9.0.3, der neuesten installierten Fassung. Python 3.14.7 (Tk 9.0.4) ist erschienen; die Installation braucht das Passwort des Inhabers (offen) |
| E-04 | Systembenachrichtigungen einbauen, mit Recherche | über `tk sysnotify`, Option, standardmäßig aus; Recherche in Abschnitt 4 und im Vertrag |
| E-05 | Recherche zur Vorschau in Tk 9 | recherchiert und umgesetzt (`image_preview.py`: `nsimage`, SVG, WIC) |
| E-06 | Ziehen aus Finder/Explorer schon jetzt | tkinterdnd2 0.6.3 im Projekt, mit Freigabe heruntergeladen; Galerie und Seiten |
| E-07 | Bilder in Seiten: einfügen, Text davor und dahinter, eingepasst, verschiebbar, Text drumherum, Größe veränderbar | alle sechs Eigenschaften umgesetzt und getestet (`test_bilder330`) |
| E-08 | gerne Leistungsverbesserungen | die drei kleinen: Speichern 3,3× schneller, Vorschauen im Zwischenspeicher, Fenster sofort. **Abweichung:** statt gebündeltem Speichern im Hintergrund wird weiter sofort gespeichert, nur schneller – so bleibt jede Änderung sofort auf der Platte. Die beiden mittleren (Startseite auf einer Fläche, lange Listen) sind offen |
| E-09 | keine Schnellerfassung für Seiten | nicht umgesetzt, wie gewünscht; auf Nachfrage gewählt und umgesetzt: wiederkehrende Checklisten und „/“-Befehle |
| E-10 | Direktvertrieb: ja | im Produktregister entschieden (Windows x64, macOS arm64) |
| E-11 | Vorschläge generieren | [Vorschläge Inhaberangaben](../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md), warten auf Bestätigung |
| E-12 | unklar, was gemeint ist | erklärt (siehe unten); die Prüfung in `test_glide` wartet jetzt auf den stabilen Endzustand |
| E-13 | Prüfpunkte gerne ausführlich | nicht verdichtet, sondern erweitert: 160 offene Punkte in der Prüfliste 3.30 |

**Nachträge während der Arbeit:**

- **Kein Ordnerpfad über dem Titel, feste Bestandteile:** umgesetzt. Kopfzeile,
  Seitenleiste, Suchzeile sowie Ober- und Unterkante der Fläche stehen in
  jeder Ansicht still, auch beim Markieren; `test_festlayout330` misst es.
- **Feste Leiste über der Fläche:** „eine Mischung aus Werkzeugen und
  Abstand“ – Seite, Zeichnung und Galerie legen dort ihre Werkzeuge ab.
- **Globale Suche:** erreichbar mit Strg/Cmd+O oder Ansicht › Ansichten ›
  „Seite oder Aktion suchen …“; jetzt mit runden Ecken und Schlagschatten.

**Zu E-12:** Eine automatische Prüfung (`test_glide`) war am 27.09.2026 einmal
gescheitert und danach viermal grün. „Absichern“ heißt: die Prüfung so
bauen, dass sie auf den fertigen Bildschirmaufbau wartet, statt zu früh zu
messen. Am Programm ändert das nichts.

**Weiter offen:** Titelbild und Unterseiten für Seiten; die mittleren
Leistungsvorschläge; Python 3.14.7; alles unter „Was ich ohne dich nicht
erledigen kann“.

## 7. Was ich ohne dich nicht erledigen kann

- manuelle Prüfung am echten Gerät, Windows-Rechner, Bildschirmleser, DPI;
- Logo-Export aus Affinity;
- Apple-Developer-Konto, Zertifikate, Notarisierung;
- Markenprüfung.

## Quellen der Recherche

- [Tk 9.0: sysnotify](https://www.tcl-lang.org/man/tcl9.0/TkCmd/sysnotify.html)
- [TIP 325: System Tray and System Notification Access](https://core.tcl-lang.org/tips/doc/trunk/tip/325.md)
- [CPython: tkinter.systray (gh-153260)](https://github.com/python/cpython/pull/153260)
- [Nuitka-Issue zu Tcl/Tk 9.0.4 im Windows-Python 3.14](https://github.com/Nuitka/Nuitka/issues/3993)
- [PyInstaller Changelog 6.22.3](https://pyinstaller.org/en/stable/CHANGES.html)
- [tkinterdnd2](https://github.com/pmgagne/tkinterdnd2)
- [tkinter.dnd](https://docs.python.org/3/library/tkinter.dnd.html)
