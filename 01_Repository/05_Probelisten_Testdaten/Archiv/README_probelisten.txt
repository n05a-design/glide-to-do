PROBELISTEN UND TESTDATEN FÜR GLIDE
Stand: 01.09.2026 · passend zu App-Version 2.6.0 / Datenformat 6

Alle Dateien mit dem Namensteil "2.6.0" wurden mit dem produktiven App-Code
erzeugt und anschliessend durch dieselbe Normalisierung und Backup-Prüfung
geschickt, die die Anwendung beim Laden verwendet. Sie können deshalb nicht
schemawidrig sein.


AKTUELLER SATZ (2.6.0)
──────────────────────────────────────────────────────────────────────────────

1. probelisten_2.6.0_liste_speicher.json
   Vollständiger Bestand im Datenformat 6:
   - Eingang mit 3 Aufgaben
   - 2 Ordner ("Projekt Parkallee", "Intern") mit Beschreibungstext
   - 5 Listen, davon 3 in Ordnern, mit Listenfarben
   - 41 Aufgaben und 10 Gruppen, bis zu drei Ebenen tief
   - Gruppen mit Beschreibungstext, Farbe und verschachtelten Untergruppen
   - Fälligkeiten in Vergangenheit, Gegenwart und Zukunft
   - Wichtigkeitsstufen 0 bis 3, erledigte und offene Punkte
   - ein referenzierter Anhang an "Exposé Layout"

   Damit lassen sich prüfen: Gruppenlogik, Fortschrittsrechnung ohne Gruppen,
   Ansicht "In Bearbeitung", Ordnerübersicht, Statusfilter, Suche, alle
   Kontextmenüs und die Farbdarstellung in Hell und Dunkel.

2. probelisten_2.6.0_komplettbackup.glidebackup
   Derselbe Bestand als portables Komplettbackup einschliesslich der
   Anhangsdatei. Für den Restore-Pfad die bevorzugte Datei: sie ersetzt den
   Bestand über "Datei > Komplettbackup laden" und legt vorher automatisch eine
   Sicherung des vorherigen Stands an.

3. probeliste_2.6.0_*.txt
   Fünf Einzellisten für den TXT-Import über "Import: TXT" beziehungsweise
   "Liste importieren":
   - vermarktung_gruppen   13 Aufgaben / 4 Gruppen, drei Ebenen, Beschreibungen
   - weg_verwaltung         8 Aufgaben / 2 Gruppen
   - tagesgeschaeft         7 Aufgaben / 2 Gruppen
   - website_design         6 Aufgaben / 1 Gruppe
   - baustelle_termine      4 Aufgaben / 1 Gruppe

   Gruppen tragen im TXT das Ordnersymbol an derselben Stelle wie die
   Wichtigkeitsmarker. Der Import erkennt es und legt wieder Gruppen an.


EINBAU DER JSON-DATEI
──────────────────────────────────────────────────────────────────────────────

Vorher immer ein .glidebackup des eigenen Stands erstellen.

1. Glide schliessen.
2. Vorhandene 'liste_speicher.json' sichern.
3. Diese Datei in 'liste_speicher.json' umbenennen.
4. In den App-Datenordner kopieren:
   Windows: %APPDATA%\Glide\
   macOS:   ~/Library/Application Support/Glide/
   Linux:   ~/.local/share/Glide/

Der Anhang der JSON-Datei zeigt auf attachments/ im selben Ordner. Er fehlt
nach dem reinen JSON-Einbau; die Aufgabe zeigt den Anhang dann als "nicht
gefunden". Wer den Anhang mit haben will, nimmt stattdessen das
Komplettbackup — dort ist die Binärdatei enthalten.

Für Tests, die den echten Datenordner nicht anfassen sollen, setzt man
GLIDE_DATA_DIR auf ein leeres Verzeichnis und startet die App damit.


HISTORISCHER SATZ
──────────────────────────────────────────────────────────────────────────────

Die Dateien ohne Versionsangabe im Namen stammen aus dem Stand vor 2.5.0 und
kennen weder Gruppen noch Fälligkeiten, Beschreibungen, Farben oder Anhänge:

  probelisten_5_listen_liste_speicher.json   Datenformat 2, für Migrationstests
  probeliste_funktionstest___scrollen.txt    Scroll- und Mengenverhalten
  probeliste_projektmarketing_neubau.txt     einfache TXT-Struktur
  probeliste_tagesgeschäft.txt               einfache TXT-Struktur
  probeliste_website___design.txt            einfache TXT-Struktur
  probeliste_weg_verwaltung.txt              einfache TXT-Struktur
  funktionstest_2026-05-28_10-38.txt         historischer Exportnachweis

Sie bleiben bewusst erhalten: Datenformat 2 ist der älteste Bestand, gegen den
die Migration weiterhin geprüft wird. Sobald der 2.6.0-Satz produktiv genutzt
wird, gehören sie nach 'Archiv'.


ABGRENZUNG
──────────────────────────────────────────────────────────────────────────────

- Kanonische, automatisierte Fixtures liegen unter
  01_Repository\Glide\tests\fixtures. Sie sind klein und versioniert und
  werden vom Integrationstest gelesen.
- Grosse manuelle Importbeispiele liegen unter
  90_Testdaten_Extern\Legacy_Probelisten.
- Dieser Ordner enthält den Satz für die manuelle Prüfung mit realistischem
  Umfang.
