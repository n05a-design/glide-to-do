# Abnahme am Gerät – Glide 3.23.0

Stand: 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

Pfade und Links in diesem Dokument gelten relativ zum Ordner
`00_Arbeitsvorbereitung` der Arbeitsablage.

## Wozu diese Liste

Die [Manuelle Prüfung](Checklisten/Manuelle_Pruefung_3.23.0.md) prüft, **was
3.23 geändert hat** – sie folgt den Punkten des Master-Arbeitsauftrags. Diese
Liste prüft, **ob Glide auf Windows und macOS ausgeliefert werden kann**. Beides
ist nötig, und beides überschneidet sich absichtlich nicht: Wo ein Schritt dort
bereits steht, verweist diese Liste auf ihn, statt ihn zu wiederholen.

Drei Dinge unterscheiden eine Abnahme von einer Änderungsprüfung:

- **Sie ist protokollpflichtig.** Jeder Schritt hat eine Kennung, die über beide
  Plattformen hinweg dieselbe bleibt, und eine Zeile im
  [Protokoll](Checklisten/Protokoll_Abnahme_3.23.0.md). „Sieht gut aus“ ohne
  Kennung ist kein Nachweis.
- **Sie prüft auch das Unveränderte.** Abgenommen sind bisher ausschließlich
  macOS-Läufe; ein aktueller Windows-Lauf steht aus. Funktionen, die seit
  Monaten stabil sind, sind unter Windows deshalb ungeprüft, nicht bewährt.
- **Sie prüft die Umgebung, nicht nur die Anwendung.** Skalierung, zweiter
  Monitor, Ruhezustand, Systemzeitzone, synchronisierter Ordner und fremde
  Programme sind die Stellen, an denen eine lokal laufende Tk-Anwendung
  scheitert – und alle fehlen in einem automatisierten Lauf.

## 1. Bevor eine Person anfängt

Eine Sichtprüfung vor einem roten Prüflauf ist verlorene Zeit. Diese sechs
Schritte stehen vor dem ersten Klick.

Alle Werkzeuge werden aus `01_Repository/Glide` heraus gestartet; unter Windows
heißt der Aufruf in der Regel `python` statt `python3`. **Der vorhandene Ordner
`tests/qa-3.23.0/abschluss` enthält das Protokoll der Linux-Vorabumgebung und
wird nicht überschrieben** – der Lauf am Arbeitsgerät bekommt einen eigenen
Zielordner je Plattform.

| Nr. | Schritt | Erwartet |
| --- | --- | --- |
| V1 | `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.23.0/abschluss_<plattform>` auf dem Arbeitsgerät | Exitcode 0. **Auch die Dokumentationsprüfung läuft durch** – die Vorabumgebung übersprang sie nur, weil die Archivdateien dort fehlen. Bleibt hier ein Linkziel offen, ist es zu korrigieren und nicht als Umgebungsfolge abzutun. Exitcode 2 heißt unvollständig, nicht bestanden: Dann hat Tk gefehlt oder der Schritt „Zeitzone“ einen Versatz von null gemessen – in beiden Fällen weist der Lauf einen Teil seiner Aussage nicht nach. |
| V2 | SHA-256 von `01_Repository/Glide/src/glide/app.pyw` gegen `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.23.0.pyw` und die Ressourcen | Gleich. Sonst wird eine andere Anwendung abgenommen als die ausgelieferte. |
| V3 | Isolierte Ablage anlegen und `GLIDE_DATA_DIR` darauf setzen | Die gesamte Abnahme läuft darin. Der echte Bestand wird nicht geöffnet – das Wiederherstellen eines App-Backups ersetzt ihn. |
| V4 | Prüfbestände einspielen: Funktionsvorschau und Praxisvorlagen aus `05_Probelisten_Testdaten/` | 12 Listen, 6 Ordner, 166 Punkte, 9 Labels, 3 Papierkorbeinträge, 16 Vorlagen. Der Leistungsbestand entsteht getrennt (siehe L2). |
| V5 | Zweite Ablage mit einem **3.22-Ausgangszustand** vorbereiten: `07_Python-Versionen/Archiv/Glide-Aufgaben-und-Listen_v3.22.0.pyw` darauf starten, Erscheinung einstellen, beenden | Für A5 und A6 brauchbar. Ohne diesen Schritt lässt sich die Designübernahme nicht prüfen, sondern nur behaupten. |
| V6 | Umgebungskopf im Protokoll ausfüllen | Betriebssystem samt Aufbaunummer, Python- und Tk-Fassung, Bildschirme mit Auflösung und Skalierung, Eingabegeräte, Systemzeitzone, Systemsprache. Ein Befund ohne diese Angaben ist nicht nachstellbar. |

## 2. Durchgänge

Eine Kennung gilt plattformübergreifend; die Spalte „Gilt für“ sagt, wo sie zu
prüfen ist. Jeder Durchgang führt sein eigenes Protokoll.

| Durchgang | Gerät | Zweck |
| --- | --- | --- |
| **P1** | Windows, Hauptmonitor, 100 % Skalierung, Maus | Vollständiger Durchlauf. Dies ist die ausstehende Windows-Erstabnahme. |
| **P2** | Windows, 150 % Skalierung, zweiter Monitor mit abweichender Skalierung | Blöcke C und D vollständig, sonst stichprobenhaft. |
| **P3** | macOS, Retina, Trackpad | Vollständiger Durchlauf. |
| **P4** | macOS, Retina plus externer Monitor ohne Retina | Blöcke C und D vollständig. |
| **P5** | Frisches Benutzerkonto ohne vorhandenen Datenordner, eine Plattform genügt | Nur Block A sowie K3. Deckt zugleich den Erststart-Einstieg auf. |

Minimum für eine Freigabeempfehlung: **P1, P3 und P5 vollständig**, P2 und P4
mindestens in den Blöcken C, D und K.

## 3. Befundklassen und Abbruch

| Klasse | Bedeutung | Folge |
| --- | --- | --- |
| **S1** | Datenverlust, stiller Datenfehler, Anwendung startet nicht, Funktion ist unbedienbar | Abnahme **anhalten**, Befund sofort aufnehmen, Ursache klären. Kein Weiterprüfen auf demselben Bestand. |
| **S2** | Funktion nur über einen Umweg erreichbar, angezeigter Wert falsch, Bedienung blockiert in einem Zustand | Prüfung fortsetzen, Befund muss vor der Freigabe entschieden sein. |
| **S3** | Darstellung, Abstand, Beschriftung, Ausrichtung – Bedienung nicht betroffen | Sammeln, gebündelt entscheiden. |
| **S4** | Anmerkung, Verbesserungsidee, abweichendes Plattformverhalten ohne Fehlwirkung | Ins Protokoll, nicht in die Freigabefrage. |

**Abbruchkriterien.** Die Abnahme wird abgebrochen und neu angesetzt, wenn V1
oder V2 nicht bestehen, wenn ein S1-Befund den Bestand verändert hat, oder wenn
die geprüfte Fassung während des Durchgangs ausgetauscht wird. Ein
Teilprotokoll wird in diesem Fall als abgebrochen gekennzeichnet und nicht
weiterverwendet.

**Bei jedem Befund festhalten:** Kennung, Durchgang, Handlung, erwartetes und
tatsächliches Verhalten, Reproduzierbarkeit (immer, gelegentlich, einmalig) und
– falls die Oberfläche betroffen ist – ein Screenshot.

---

## Block A · Start, Ablage und Migration

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| A1 | P5 | Erststart ohne vorhandenen Datenordner und ohne `GLIDE_DATA_DIR` | Der Ordner entsteht am Plattformstandard, außerhalb des Programmordners. Pfad ins Protokoll. |
| A2 | beide | Start mit gesetztem `GLIDE_DATA_DIR` | Die Variable hat Vorrang vor Plattformstandard und `datenordner.json`. |
| A3 | beide | Datenordner mit Umlauten und Leerzeichen im Pfad | Anlegen, Speichern, Anhänge und Backup funktionieren. |
| A4 | Windows | Datenordner in einem Pfad über 260 Zeichen | Entweder vollständig nutzbar oder verständlich abgewiesen – kein halb geschriebener Bestand. |
| A5 | beide | 3.23 auf der 3.22-Ablage aus V5 starten | Designübernahme nach [Manuelle Prüfung, Abschnitt 1](Checklisten/Manuelle_Pruefung_3.23.0.md). Hier zusätzlich: Es entsteht **keine** Formatsicherung, da 3.23 kein Datenformat ändert. |
| A6 | beide | 3.23 beenden, danach die 3.22-Fassung auf derselben Ablage starten | 3.22 liest `theme`, `color_mode` und `glass_mode` und fällt nicht auf seine Vorgaben zurück. `connections` und `list_detail_mode` werden ignoriert, nicht verworfen. Danach wieder 3.23 starten: Verbindungen und Anzeigemodus stehen noch. |
| A7 | beide | Zweite Glide-Instanz auf demselben Datenordner öffnen | Die Belegung wird erkannt, die zweite Instanz speichert nicht. |
| A8 | beide | Datenordner in einen synchronisierten Ordner legen: schließen, vollständig synchronisieren, am zweiten Gerät öffnen, dort ändern, zurücksynchronisieren | Der Bestand kommt vollständig an. Bekannte Grenze: zwei noch unsynchronisierte Kopien lassen sich nicht verriegeln – geprüft wird der nacheinander laufende Weg. |
| A9 | beide | Eine Backupdatei mit abweichender Groß-/Kleinschreibung im Namen öffnen | Verhalten je Plattform ins Protokoll. Unter Windows und macOS gleichbedeutend, unter Linux nicht – das war bereits ein Befund. |
| A10 | beide | Ablage während des Betriebs schreibgeschützt setzen, dann speichern | Verständliche Meldung, kein Verlust des bereits geladenen Bestands. |

## Block B · Erscheinung am Gerät

Die sieben Designs selbst stehen in
[Manuelle Prüfung, Abschnitt 2](Checklisten/Manuelle_Pruefung_3.23.0.md). Hier
steht, was nur die Plattform beantwortet.

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| B1 | beide | Systemdesign hell/dunkel umschalten, während Glide läuft | Glide bleibt in seinem gewählten Design. Kein Flackern, kein halb umgestelltes Fenster. |
| B2 | Windows | Ein Liquid-Glass-Design bei aktiver Materialoptik | Die Titelleiste folgt dem Design, auch an Dialogen und an der Schnellerfassung. Bietet die Plattform den nativen Backdrop nicht, bleibt die Oberfläche als lesbare Farbvariante vollständig bedienbar. |
| B3 | macOS | Systemerscheinungsbild auf „Automatisch“, Systemakzentfarbe ändern | Glide bleibt bei seiner eigenen Akzentfarbe; Auswahlflächen bleiben lesbar. |
| B4 | beide | `python3 tests/tools/symbolpruefung.py` | Die privat registrierte Schrift wird gefunden, die gemessenen Glyphenfamilien stimmen. Danach in der Oberfläche prüfen: kein Ersatzzeichen, keine Kästchen. |
| B5 | beide | Alle drei Schriftgrößen mit langen Listen- und Ordnernamen | Nichts wird abgeschnitten, keine Zeile überlappt, die Seitenleiste bleibt bedienbar. |
| B6 | beide | Liquid Glass an einer Karte aus nächster Nähe ansehen | Verlauf ohne Streifenkanten, gerundete Ecke ohne Treppe – auch bei hoher Pixeldichte, wo Zwischenschritte sichtbarer werden. |

## Block C · Skalierung, Auflösung und mehrere Monitore

Dieser Block ist neu und der risikoreichste. Die Dichtestufen von 3.23 sind in
Pixeln festgelegt – 1120, 900, 700 für die Kopf- und Aktionsreihen, 616 und 932
für die Spalten der Startseite. Ob diese Werte bei 150 % Skalierung noch das
Richtige bedeuten, ist ungeprüft.

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| C1 | Windows | Skalierung nacheinander auf 100, 125, 150 und 200 % stellen, Glide jeweils neu starten | Text bleibt scharf, keine Beschriftung ist abgeschnitten, keine Schaltfläche überlappt. Unscharfer Text ist ein Befund, kein Systemverhalten. |
| C2 | P2 | Glide-Fenster von einem Monitor auf einen mit anderer Skalierung ziehen | Das Fenster stellt sich um, ohne dass Bedienelemente verschwinden. Nach dem Ziehen einmal die Ansicht wechseln – die Dichtestufe muss zur tatsächlichen Breite passen. |
| C3 | P4 | Fenster zwischen Retina und externem Monitor ohne Retina bewegen | Symbole und Schrift bleiben lesbar, Kartenverläufe zeigen keine Stufen. |
| C4 | P2, P4 | Bei 150 % beziehungsweise auf dem externen Monitor die Kopfzeile langsam schmaler ziehen | Die drei Stufen treten bei derselben **wahrgenommenen** Breite ein wie bei 100 %. Treten sie zu früh ein, sind die Schwellen an die Skalierung zu binden. |
| C5 | beide | Fenster auf die Bildschirmhälfte legen, Startseite öffnen | Zweispaltig. Bei hoher Skalierung gesondert prüfen. |
| C6 | beide | Auf 1366 × 768 arbeiten | Alle Dialoge passen auf den Bildschirm, kein Knopf liegt unterhalb des sichtbaren Bereichs. |
| C7 | P2, P4 | Den Monitor abziehen, auf dem Glide gerade liegt | Das Fenster kommt auf dem verbleibenden Bildschirm zurück und ist bedienbar. |
| C8 | beide | Bildschirmlupe über Auswahl, Tabellenkopf und Kartenverlauf | Kein Textverlust, keine unerwartete Farbe unter Vergrößerung. |

## Block D · Fensterzustände und Dichte

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| D1 | beide | Maximieren, Wiederherstellen, an den Rand snappen | Der Aufbau folgt sofort, keine leere Fläche bleibt stehen. |
| D2 | macOS | Vollbild über den grünen Knopf | Eigener Bereich, Menüleiste erreichbar, Rückkehr ohne Verlust der Ansicht. |
| D3 | beide | Fenstergröße und -position ändern, beenden, neu starten | Beides wird wiederhergestellt; auf dem Monitor, auf dem es zuletzt stand. |
| D4 | beide | Kopfbereich unter 1120, unter 900 und Aktionsreihe unter 700 Pixel bringen | Die drei Stufen aus dem Bedienvertrag treten ein. Alle ausgeblendeten Aktionen bleiben über Kontextmenü, Menüleiste, Tastenkürzel und Überlaufmenü erreichbar – das war die Bedingung für das Ausblenden. |
| D5 | beide | Fenster unter die Mindestbreite ziehen | Das Fenster lässt sich nicht kleiner ziehen als bedienbar, oder der Inhalt bleibt erreichbar. Kein Tk-Fehler im Zeilenaufbau. |
| D6 | beide | Schnell mehrfach zwischen breit und schmal wechseln | Nichts bleibt hängen, keine Schaltfläche fehlt danach. |

## Block E · Eingabegeräte und Tastenkürzel

Die Grundfälle stehen in
[Manuelle Prüfung, Abschnitt 3](Checklisten/Manuelle_Pruefung_3.23.0.md).

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| E1 | beide | Alle Kürzel der Menüleiste einmal auslösen | Unter Windows mit Strg, unter macOS mit Cmd. Kein Kürzel greift ins Leere, keines kollidiert mit einer Systembelegung. |
| E2 | macOS | **F11 auf der Pinnwand** | Der Bedienvertrag nennt F11 für das Vollbild. Unter macOS ist diese Taste standardmäßig systembelegt, und je nach Einstellung der Funktionstasten braucht es zusätzlich fn. Tatsächliches Verhalten ins Protokoll; **„Fläche“ in der Reiterzeile muss in jedem Fall funktionieren.** Ist F11 nicht erreichbar, ist zu entscheiden, ob die Dokumentation die Plattformgrenze nennt oder ein zweites Kürzel dazukommt. |
| E3 | beide | Escape auf der Pinnwand in allen drei Zuständen | Bricht zuerst das Verbinden ab, dann das Vollbild, dann die Pinnwand – in dieser Reihenfolge. |
| E4 | macOS | Menüleiste in der Systemleiste, Anwendungsmenü, Cmd+Q, Cmd+W | Glide verhält sich wie eine macOS-Anwendung; Beenden speichert. |
| E5 | beide | Umlaute, ß und tote Tasten in Titel, Beschreibung und Suche | Kommen vollständig an, auch in der Schnellerfassung. |
| E6 | beide | Trackpad: zwei Finger senkrecht und waagerecht, Pinch, Drei-Finger-Wischen | Scrollen wie erwartet; Pinch und Wischen verändern den Bestand nicht. |
| E7 | beide | Kontextmenü über Rechtsklick, Ctrl-Klick und Menütaste | Öffnet an der Zeigerposition, schließt mit Escape, wählt keine Zeile unbeabsichtigt aus. |
| E8 | beide | Ziehen in Baum und Seitenleiste mit Maus und mit Trackpad | Ziel wird angezeigt, Abbruch mit Escape lässt den Bestand unverändert. |
| E9 | beide | Mausrad gedrückt halten und ziehen, Shift und Mausrad | In Baum, Seitenleiste, Startseite und Pinnwand. |

## Block F · Pinnwand am Gerät

Die Grundfälle stehen in
[Manuelle Prüfung, Abschnitt 4](Checklisten/Manuelle_Pruefung_3.23.0.md).

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| F1 | beide | Eine Pinnwand bis an die Grenze von 200 Verbindungen füllen | Die Grenze greift verständlich; das Zeichnen bleibt flüssig. |
| F2 | beide | 500 Karten anheften | Die Grenze greift; Aufbau und Scrollen bleiben bedienbar. |
| F3 | beide | Bildanhänge als PNG, GIF, PPM und als JPEG | Die ersten drei zeigen eine Vorschau, JPEG zeigt erwartungsgemäß nur den Anhangzähler. |
| F4 | beide | Eine breite Fläche drucken | Das Papierformat folgt dem Seitenverhältnis der belegten Fläche; eine breite Fläche wird nicht ins Hochformat gezwängt. |
| F5 | beide | Ordnerpinnwand: „Neue Aufgabe“ versuchen | Der Hinweis erklärt, warum hier kein Punkt entsteht. |

## Block G · Ausgaben an fremde Programme

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| G1 | beide | Alle vier Druckformate öffnen und **tatsächlich drucken** | Nicht nur die Vorschau. Seitenumbrüche bei langen Listen ansehen. |
| G2 | beide | Dieselben vier Formate als PDF sichern | Umlaute und Sonderzeichen stehen richtig, nichts ist abgeschnitten. |
| G3 | beide | Die erzeugte HTML-Datei in einem zweiten Browser öffnen | Gleiches Bild, keine externen Verweise, kein Nachladen. |
| G4 | beide | Schriftbild im Anzeigeprogramm prüfen | Die mitgelieferte Schrift ist nur prozesslokal registriert und steht dem Browser nicht zur Verfügung. Erwartet wird ein lesbarer Systemfallback – kein Fehler, aber im Protokoll festzuhalten. |
| G5 | beide | ICS-Ausgabe in Apple Kalender, Outlook und Thunderbird einlesen | Ganztags- und Zeittermine, Dauer, Wiederholungen und Alarme kommen an. Dieselbe Datei ein zweites Mal einlesen und das tatsächliche Verhalten des Zielkalenders festhalten: Ersetzen, Überspringen oder Kopie. |
| G6 | beide | `.glideexchange` im Texteditor der Plattform öffnen | Lesbar, Umlaute richtig, keine 32-stelligen internen Kennungen. |
| G7 | beide | Einen Anhang aus Glide heraus öffnen | Startet im Standardprogramm; der Pfad bleibt gültig, auch mit Leerzeichen und Umlauten. |
| G8 | beide | Als Ausgabeziel einen Ordner ohne Schreibrecht wählen | Verständliche Meldung, keine halbe Datei, keine Nutzdatendatei als Ziel möglich. |

## Block H · Fremde Dateien einlesen

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| H1 | beide | CSV aus Excel gespeichert (Semikolon, mit BOM) | Trennzeichen und Kodierung werden erkannt, Umlaute stimmen. |
| H2 | macOS | CSV aus Numbers gespeichert (Komma) | Dasselbe. |
| H3 | beide | Je eine ICS-Datei aus Apple Kalender, Outlook und einem Webkalender | Wird gelesen; der Bericht nennt die Übersprungsgründe und stimmt mit der Datei überein. |
| H4 | beide | Kalenderrundlauf in vier Schritten nach `05_Probelisten_Testdaten/README.md` | Der zweite Import überspringt **alle** Termine als Duplikate. Mit ersetzten UIDs entstehen Aufgaben, das Serienende bleibt erhalten. |
| H5 | beide | Systemzeitzone auf eine westliche und eine östliche Zone stellen, Rundlauf wiederholen | Das Enddatum der Wochentagsserie verschiebt sich nicht. Genau dieser Fehler war in einer UTC-Umgebung unsichtbar. |
| H6 | beide | Eine Markdown-Gliederung importieren | Überschriften, Punkte, Unterpunkte und Checklistenschritte werden erkannt. |
| H7 | beide | Eine Austauschdatei mit einem erfundenen Feld importieren | Die Vorschau nennt das Feld, der Fokus liegt auf „Abbrechen“. |
| H8 | beide | Grenzen anfahren: über 12 MB, über 5000 Punkte, über 12 Ebenen | Verständlich abgewiesen, Bestand unverändert. |
| H9 | beide | Nach jedem Import einmal Rückgängig | Die angelegten Listen, Ordner und Labels sind wieder weg; vorhandene Punkte wurden nie verändert. |

## Block I · Backup und Wiederherstellung

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| I1 | beide | Vollständiges App-Backup schreiben, **in einer getrennten Ablage** wiederherstellen | Aufgaben, Anhänge, Einstellungen, Vorlagen und Aktivitätsdaten kommen an. |
| I2 | beide | Inhaltsvorschau vor dem Wiederherstellen mit dem tatsächlichen Inhalt vergleichen | Die Zahlen stimmen. |
| I3 | beide | Die Rückfallsicherungen im Backup-Ordner prüfen | `vor_import_*`, `settings_vor_restore_*` und `vorlagen_vor_restore_*` liegen vor. |
| I4 | beide | Ein reines Aufgabenbackup schreiben und in leerer Ablage öffnen | Design, Pinnwandverbindungen, Anzeigemodus, Spaltenbreiten und „Mein Tag“ sind erwartungsgemäß **nicht** enthalten. |
| I5 | beide | Ein auf der einen Plattform erzeugtes App-Backup auf der anderen wiederherstellen | Anhänge, Pfadtrennzeichen und Umlaute in Dateinamen kommen unverändert an. |
| I6 | beide | Eine fremde oder beschädigte Archivdatei anbieten | Abweisung mit Begründung, vorhandener Bestand unangetastet. |

## Block J · Benachrichtigungen, Ruhezustand, Dauerbetrieb

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| J1 | beide | Eine Benachrichtigung während der Laufzeit auslösen | Erscheint innerhalb des Takts; Aufschub und Zustellbeleg funktionieren. |
| J2 | beide | Dock- beziehungsweise Taskleistenaufmerksamkeit | Wird sichtbar hervorgehoben und lässt sich zurücksetzen. |
| J3 | beide | Gerät in den Ruhezustand versetzen, über einen fälligen Termin hinweg, aufwecken | Der verpasste Hinweis erscheint gesammelt. Keine Sturzflut, kein stiller Verlust. |
| J4 | beide | Geräteuhr über Mitternacht stellen | „Mein Tag“, Bearbeitungstag, Tagesplanung und die Kachel „Heute“ rechnen auf den neuen Tag um. |
| J5 | beide | Sommerzeitwechsel nachstellen | Feste und relative Benachrichtigungen verschieben sich nicht um eine Stunde. |
| J6 | beide | `python3 tests/tools/dauerlauf.py --minuten 10 --aufgaben 4000 --ziel <datei>.json` | Exitcode 0. Zehn Minuten sind das Minimum, damit der Takt oft genug feuert. |
| J7 | beide | Glide mehrere Stunden offen lassen, dabei arbeiten, danach Speicherbedarf und Bedienbarkeit prüfen | Kein stetiges Wachstum, keine Verlangsamung, Bestand nach dem Neuladen unversehrt. |
| J8 | beide | Anwendung wechseln und zurückkehren, mehrfach, mit offenem modalem Dialog | Der Dialog bleibt vorn und bedienbar; kein verwaistes Fenster. |

## Block K · Barrierefreiheit

Der Kontrast ist rechnerisch geprüft – alle Kombinationen aus Design und
Akzentfarbe erreichen den Mindestwert. Eine Prüfung mit echten Hilfsmitteln
ersetzt das nicht; dieser Block holt sie nach.

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| K1 | Windows | Mit NVDA durch Seitenleiste, Liste, Tabelle und einen Dialog | Zeilen, Zustände und Schaltflächen werden angesagt. Befunde festhalten, auch wenn sie nicht behebbar sind – sie gehören in die Produktgrenzen. |
| K2 | macOS | Dasselbe mit VoiceOver | Dasselbe. |
| K3 | beide | Einen vollständigen Arbeitsweg **ohne Maus**: erfassen, Termin setzen, Label vergeben, erledigen, rückgängig | Durchgehend mit Tastatur bedienbar; der Fokus ist jederzeit sichtbar. |
| K4 | Windows | Hochkontrastmodus des Systems einschalten | Glide bleibt lesbar oder weist verständlich auf sein eigenes Kontrastdesign hin. |
| K5 | beide | Beide Kontrastdesigns mit Lupe und Vorlesefunktion | Text gegen Fläche bleibt deutlich, gedämpfter Text bleibt lesbar. |
| K6 | Windows | Eine Sitzung über Remotedesktop | Darstellung und Bedienung bleiben brauchbar; Materialoptik fällt sauber zurück. |

## Block L · Leistung am Gerät

| Nr. | Gilt für | Handlung | Erwartet |
| --- | --- | --- | --- |
| L1 | beide | `python3 tests/tools/leistungspruefung.py --ziel <datei>.json` | Läuft durch; Werte ins Protokoll. |
| L2 | beide | Einen Bestand in der Größenordnung des Leistungsbefunds aufbauen und zwanzig Ansichtswechsel messen | Der gemessene Wert liegt in der Größenordnung des Referenzwerts aus dem Leistungsbericht. Gemessen wird, nicht geschätzt – „fühlt sich flüssig an“ ist kein Ergebnis. |
| L3 | beide | Eine Liste mit 200 Punkten im Anzeigemodus „Erweitert“ scrollen | Bleibt flüssig bedienbar; die Grenze von zwölf Detailzeilen je Punkt greift. |
| L4 | beide | Zeit vom Start bis zur bedienbaren Oberfläche, dreimal | Wert ins Protokoll, auf beiden Plattformen vergleichbar. |
| L5 | beide | Nach einer Änderung sofort die Seitenleiste ansehen | Die Zähler stimmen. Der Aufbau-Zwischenspeicher darf außerhalb eines Aufbaus keinen alten Wert liefern. |

## Block M · Regression, insbesondere Windows-Erstabnahme

Diese Funktionen sind seit Längerem unverändert – aber unter Windows nicht
abgenommen. Unter macOS genügt eine Stichprobe, unter Windows sind sie
vollständig zu prüfen.

| Nr. | Gilt für | Handlung |
| --- | --- | --- |
| M1 | Windows voll | Vorlagen hinzufügen, anwenden, eigene Vorlage anlegen; relative Fristen prüfen. |
| M2 | Windows voll | Suche, Offen-Filter, gespeicherte Filter mit dynamischem Zeitraum. |
| M3 | Windows voll | Papierkorb: Liste, Ordner und einzelnen Punkt wiederherstellen. |
| M4 | Windows voll | Rückgängig über mehrere Schritte, auch nach einem Import. |
| M5 | Windows voll | Ziehen in Baum, Seitenleiste und zwischen Ordnern; Mehrfachauswahl. |
| M6 | Windows voll | Reiter: Anlegen, Umordnen, Grenze und Wiederverwendung. |
| M7 | Windows voll | Änderungsverlauf: Vorgänge, Sammeleinträge, Filter, Leeren, Abschalten. |
| M8 | Windows voll | Schnellerfassung mit Zielliste, Fristvorschau und Mehrfacherfassung. |
| M9 | Windows voll | „Mein Tag“, Tabellenansicht, Kalenderansicht und Tagesplanung mit Kapazität. |
| M10 | Windows voll | Alle sechs Wiederholungsarten einschließlich Serienende anlegen und vorrücken lassen. |

## Screenshots

Erzeugen und ansehen, nicht nur erzeugen. Unter Windows über
`pruefen.py --screenshots` oder die entsprechende Option der
Integrationssuiten; `screenshots.py` selbst ist der Linux/X11-Weg. Die
Erzeugung braucht die Zielplattform und ImageMagick. Die Bilder gehören zum
Nachweis – ein Befund an der Oberfläche wird mit Bild aufgenommen.

## Nach der Abnahme

1. Protokolle je Durchgang ablegen und im
   [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) mit Datum,
   Plattform, Python-Fassung und Exitcode eintragen.
2. Ergebnis in [Weitergabe](Glide_Weitergabe_neuer_Chat_2026-09-18.md) und
   [Technische Fakten](Notizen/Technische_Fakten_3.23.0.md) **derselben**
   Version nachziehen.
3. Befunde der Klassen S1 und S2 in
   [Offene Entscheidungen](Entscheidungen/Offene_Entscheidungen_3.23.0.md)
   überführen, bevor der nächste Stand beginnt.
4. Was hier als Plattformgrenze bestätigt wurde – und nicht behoben wird –,
   gehört in die
   [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md), nicht
   in eine Fußnote.

**Eine bestandene Abnahme ist keine Veröffentlichung.** Installer, Signatur,
Notarisierung, Prüfung auf einem frisch aufgesetzten Gerät und Storematerial
bleiben eigene Schritte.
