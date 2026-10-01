# ARBEITSAUFTRAG: Bestandsanalyse, Dateistruktur und drei Glide-Deliverables

*Vollständig ausformulierter Prompt. Als Nachricht in einen Chat kopieren, in dem
`docs/09_STARTKONTEXT.md` bereits als Kontext gesetzt wurde – oder, falls nicht,
zusammen mit dieser Datei.*

---

## 0 · Deine Rolle

Du bist der verantwortliche Entwickler und Release-Verantwortliche für **Glide**,
eine lokale Desktop-App für Aufgaben und Listen (Python 3.12 + Tkinter,
Zielplattformen Windows und macOS, Version 3.2.0, Datenformat 10).

Du arbeitest in vier Rollen gleichzeitig und musst sie sauber trennen:

1. **Prüfer** – du stellst fest, was tatsächlich da ist, und behauptest nichts,
   was du nicht gelesen hast.
2. **Aufräumer** – du bringst die Dateistruktur in einen Zustand, der ohne
   Erklärung verständlich ist.
3. **Autor** – du erzeugst drei inhaltliche Arbeitsdokumente als
   Glide-Datenbestand.
4. **Berichterstatter** – du sagst am Ende ehrlich, was erledigt ist, was
   ungeprüft blieb und was du bewusst nicht getan hast.

Antworte durchgehend auf Deutsch. Auch Code-Kommentare und erzeugte Dokumente
sind auf Deutsch.

---

## 1 · Pflichtlektüre, bevor du irgendetwas änderst

Lies in dieser Reihenfolge und arbeite **nicht** aus dem Gedächtnis oder aus
Annahmen:

1. `docs/09_PROJECT_HANDOFF.md` – konsolidierter Projektstand, alle
   Nutzeranforderungen, verworfene Ansätze, Fehlerwissen.
2. `AGENTS.md` – verbindliche Arbeitsregeln und Abschlusskriterium.
3. `docs/01_PRODUCT_CONSTRAINTS.md` – Produktgrenzen und ausdrückliche
   Nicht-Ziele.
4. `docs/02_ARCHITECTURE.md` – aktueller technischer Aufbau (Stand 3.2.0).
5. `docs/00_INDEX.md` – Dokumentationsindex.
6. `tests/tools/beispieldaten.py` – das vorhandene Werkzeug, das einen
   Glide-Datenbestand erzeugt. **Dies ist dein Muster für Aufgabenblock E.**

Erst danach beginnst du mit Aufgabenblock A.

---

## 2 · Nicht verhandelbare Randbedingungen

Diese Regeln stehen über jeder Aufgabe in diesem Auftrag. Wenn eine Aufgabe mit
einer Regel kollidiert, gewinnt die Regel, und du meldest den Konflikt.

### 2.1 Datenintegrität

- **Kein Datenverlust, unter keinen Umständen.** In diesem Projekt ist bereits
  ein Punkt beim Auflösen einer Gruppe verschwunden; der Bereich um Gruppen,
  Papierkorb und Rückgängig ist seitdem durch `guarded_structural_change`
  abgesichert. Dort arbeitest du mit besonderer Vorsicht.
- **Du löschst keine Datei.** Nirgends, zu keinem Zeitpunkt. Alles, was weg
  soll, wird **verschoben** (siehe Aufgabenblock B).
- **Du fasst den Datenordner des Nutzers nicht an.** Testisolierung
  ausschließlich über `GLIDE_DATA_DIR`, gesetzt **vor** dem Import des Moduls.
  `%APPDATA%` allein wirkt nur unter Windows und träfe sonst echte Nutzerdaten.

### 2.2 Bestehende Funktionalität

- **Du entfernst keine bestehende Funktion**, die nicht in diesem Auftrag
  ausdrücklich zur Entfernung freigegeben ist.
- Bevor du etwas als „tot" oder „ungenutzt" löschst oder verschiebst, **prüfst
  du gegen den echten Aufrufer im Quelltext**. Die Analysewerkzeuge dieses
  Projekts erzeugen nachweislich Falsch-Positive: `LabelChip.set_colors`,
  `format_file_size`, `_store_pending_attachments` und
  `refresh_scrollbar_state` wurden bereits fälschlich als unerreichbar
  gemeldet und sind **in Benutzung**.
- **Refactoring erhält Verhalten exakt.** Wo eine Vereinheitlichung das
  Verhalten ändern würde, behältst du das alte Verhalten und schreibst den
  Grund als Kommentar dazu.

### 2.3 Architekturregeln (nicht umgehen)

- Jede Änderung an Punkten läuft durch `item_change`, jede an Listen und Ordnern
  durch `sidebar_change`; Wirkung wird über `ChangeRecord.mark()` gemeldet.
- Jede Umbauaktion läuft zusätzlich unter `guarded_structural_change`;
  `item_change` sitzt **innerhalb**, nie darum herum.
- Auswahlprüfung ausschließlich über `selected_items_for_change`.
- Jeder modale Dialog läuft über `run_modal`. Niemals `grab_set` +
  `wait_window` von Hand.
- Alle Oberflächensymbole stehen in der Tabelle `ICONS` und sind
  **ausschließlich Textzeichen, niemals Emoji**. Ein Test erzwingt das
  (kein Zeichen ≥ U+1F000). Anhang `⊕`, Kalender `▦`, Labels `◈`.
- Nur Python-Standardbibliothek plus Tk. **Keine neue Laufzeitabhängigkeit.**
- Datenformat bleibt **10**.
- `.pyw` wird ausschließlich mit `importlib.machinery.SourceFileLoader`
  geladen, nie mit `spec_from_file_location`.

### 2.4 Verworfene Ansätze – nicht erneut vorschlagen

Dunkelblau im Dunkelmodus (bleibt grau) · selbstgezeichnete
Ordner-Klappdreiecke · Emoji als Symbole · Fixtures oder Formatprüfung
entfernen · Import- und Backup-Wege in den `item_change`-Rahmen zwingen ·
Umbenennen beim Klick auf das Klappdreieck.

### 2.5 Abschlusskriterium für jede Codeänderung

Syntaxprüfung grün **und** alle drei Testsuiten grün **und** Versionsangaben
konsistent **und** verbleibende manuelle Prüfungen ausdrücklich benannt:

```
python3.12 -c "import ast,pathlib; ast.parse(pathlib.Path('src/glide/app.pyw').read_text(encoding='utf-8'))"
xvfb-run -a python3.12 tests/integration/test_glide.py
xvfb-run -a python3.12 tests/integration/test_datenintegritaet.py
xvfb-run -a python3.12 tests/integration/audit_app.py
```

Nach jeder Änderung, die das Layout berühren könnte, zusätzlich:

```
xvfb-run -a --server-args="-screen 0 1400x1100x24" python3.12 tests/tools/screenshots.py --out /tmp/shots
```

und die erzeugten Bilder tatsächlich ansehen. Ein grüner Test hat in diesem
Projekt schon einmal eine kaputte Oberfläche verdeckt: Symbole verschwanden nach
einer Fensterbreiten-Änderung, weil `refresh_sidebar_row_texts` die Texte ohne
Symbole neu baute.

---

## 3 · Aufgabenblock A – Bestandsanalyse

**Ziel:** ein belegter Ist-Zustand, kein Bauchgefühl.

### A.1 Vollständige Inventur

Erfasse jede Datei im Repository (ohne `.git/`) und ordne sie genau einer
Kategorie zu:

| Kategorie | Bedeutung |
|---|---|
| produktiv | wird zur Laufzeit der App gebraucht |
| Test | eine der drei Testsuiten |
| Werkzeug | erzeugt Material, liefert kein Ja/Nein |
| Fixture | Referenz- oder Beispieldaten |
| Dokumentation, aktuell | Stand entspricht 3.2.0 |
| Dokumentation, veraltet | Stand älter als 3.2.0 |
| Dokumentation, historisch | bewusst als Historie geführt (z. B. `exec-plans/`) |
| generiert | aus einem Werkzeug reproduzierbar |
| temporär / Artefakt | z. B. `__pycache__` |
| Status unklar | du konntest es nicht sicher zuordnen |

Für jede Datei: **Pfad → Rolle → Kategorie → Letzter inhaltlicher Stand
(Version) → Besonderheit**.

### A.2 Konsistenzprüfung

Prüfe und dokumentiere jede Abweichung mit Fundstelle:

1. **Versionskonsistenz:** `VERSION`, `APP_VERSION` in `src/glide/app.pyw`,
   die Prüfung in `tests/integration/test_glide.py`, der oberste
   `CHANGELOG.md`-Eintrag und jede Versionsangabe in `docs/`.
2. **Datenformat:** `DATA_SCHEMA_VERSION` gegen jede Nennung in der
   Dokumentation. **Bekannter Fehler:**
   `docs/decisions/PRODUCT_IDENTITY.md` nennt Datenformat 9, tatsächlich ist
   es 10. Diese Datei ist laut `AGENTS.md` eine verbindliche Quelle für Build-
   und Store-Konfigurationen – der falsche Wert ist deshalb nicht kosmetisch.
3. **Index-Vollständigkeit:** Enthält `docs/00_INDEX.md` jede Datei unter
   `docs/`? Gibt es Einträge ohne Datei?
4. **Verweise:** Zeigt jeder Datei-, Pfad- und Funktionsverweis in der
   Dokumentation auf etwas Existierendes? Prüfe insbesondere Verweise auf
   Funktionen, die in 3.1.0 umbenannt oder zusammengeführt wurden.
5. **README-Abdeckung:** `tests/tools/README.md` beschreibt nur
   `screenshots.py`. Nicht beschrieben sind `analyse_statisch.py`,
   `analyse_erreichbarkeit.py` und `beispieldaten.py`.
6. **Externe Verweise:** Die Dokumentation nennt Ordner außerhalb des
   Repositorys (`10_Dokumentation/`, `30_Release_Exports/`,
   `40_Store_Material/Produktdatenblatt_2.11.0.md`). Stelle fest, ob du sie
   erreichen kannst. Wenn nein: als `STATUS UNKLAR` führen, **nicht** raten und
   **nicht** neu anlegen.

### A.3 Codeanalyse

Führe die vorhandenen Werkzeuge aus und werte sie aus:

```
python3.12 tests/tools/analyse_statisch.py
python3.12 tests/tools/analyse_erreichbarkeit.py
```

Vergleiche das Ergebnis mit `docs/08_CODE_BEFUND.md`. Nenne jede Abweichung.
**Behandle jeden Fund als Verdacht, nicht als Tatsache**, bis du ihn im
Quelltext belegt hast (siehe Regel 2.2).

### A.4 Abnahmekriterium für Block A

Eine Datei `docs/11_BESTANDSANALYSE.md` mit: Inventurtabelle, Liste aller
Inkonsistenzen mit Fundstelle, Bewertung nach Schwere (blockierend / wichtig /
kosmetisch), und ausdrücklich einer Liste dessen, was du **nicht** feststellen
konntest.

---

## 4 · Aufgabenblock B – Dateistruktur und Archiv

**Ziel:** eine Struktur, die sich selbst erklärt, ohne dass Historie verloren
geht.

### B.1 Archivkonzept festlegen

Es existiert derzeit **kein** Archivordner. Lege fest und begründe kurz:

- Wo liegt das Archiv? (Vorschlag zur Prüfung: ein `archiv/`-Unterordner je
  betroffenem Bereich, also `docs/archiv/`, statt eines einzigen Sammelordners
  auf oberster Ebene. Entscheide begründet.)
- Wie wird ein archivierter Stand benannt, damit erkennbar bleibt, aus welcher
  Version er stammt?
- Woran erkennt jemand später, **warum** etwas archiviert wurde?

Lege dazu eine `archiv/README.md` an, die diese drei Fragen beantwortet.

### B.2 Was archiviert wird

**Archiviere nur, was du in Block A belegt als veraltet eingestuft hast.**

Kandidaten aus dem bekannten Stand – jeweils erst prüfen, dann handeln:

- `docs/07_QA_BERICHT.md` (Stand 2.11.0)
- `docs/10_RELEASE_CHECKLIST.md` (Stand 2.11.0)
- `docs/decisions/PRODUCT_IDENTITY.md` (Stand 2.11.0, falsches Datenformat)

**Wichtig:** Bei diesen dreien ist Archivieren allein die falsche Antwort. Sie
werden weiterhin gebraucht. Richtig ist: **alten Stand archivieren und eine
fortgeschriebene Fassung auf 3.2.0 an den ursprünglichen Ort legen.** Ein
Verweis in der Dokumentation darf nach deiner Arbeit nicht ins Leere zeigen.

**Nicht archivieren:**

- `docs/exec-plans/*` – bewusst geführte Historie, kein Altbestand.
- `tests/fixtures/current_v4` bis `current_v10` und `legacy_v2` – sie sichern,
  dass ältere Backups lesbar bleiben. Ihre Entfernung wurde geprüft und
  **abgelehnt**.
- `docs/08_CODE_BEFUND.md` – aktuell.

### B.3 Wie verschoben wird

- **Verschieben, niemals löschen.**
- Verschiebe mit `git mv`, falls das Repository unter Git steht; sonst mit
  `mv`. Prüfe das vorher mit `git status`.
- **Nach jedem Verschiebevorgang** prüfst du, ob ein Verweis darauf existiert,
  und ziehst ihn nach: `docs/00_INDEX.md`, `AGENTS.md`, `README.md`,
  Querverweise zwischen Dokumenten, Pfadangaben in Test- und Werkzeugdateien
  (`TEST_FILES`, `USAGE_SEARCH` in den Analysewerkzeugen).
- **Prüfe, ob eine verschobene Datei von Code gelesen wird**, bevor du sie
  bewegst. Ein verschobenes Fixture bricht die Testsuite.

### B.4 Fehlende Dateien ergänzen

Ergänze, was für ein Repository dieses Reifegrads fehlt, aber **nur, wenn du
begründen kannst, wozu es dient**. Keine Dateien „weil man das so macht".

Prüfe mindestens, ob vorhanden und sinnvoll:

- `tests/tools/README.md` – auf alle vier Werkzeuge erweitern (siehe A.2.5).
- `tests/README.md` – wie die drei Suiten aufgerufen werden und was jede prüft.
- `docs/03_*` und `docs/04_*` – im Index fehlen die Nummern 3 und 4. Stelle
  fest, ob dort einmal etwas existierte (`git log`) oder ob die Nummerierung
  schlicht Lücken hat. **Erfinde keine Dokumente, um Lücken zu füllen.**
- Fortgeschriebene Fassungen der drei veralteten Dokumente aus B.2.

**Vor jeder neuen Datei:** prüfe, ob ihr Inhalt nicht bereits woanders steht.
Doppelte Dokumentation ist schlimmer als fehlende, weil sie auseinanderdriftet.

### B.5 Abnahmekriterium für Block B

- Alle drei Testsuiten weiterhin grün.
- Kein Verweis in der Dokumentation zeigt ins Leere.
- `docs/00_INDEX.md` ist vollständig und korrekt.
- Jede verschobene Datei ist im Archiv auffindbar und ihr Archivierungsgrund
  dokumentiert.
- Keine einzige Datei wurde gelöscht.

---

## 5 · Aufgabenblock C – Fehlerprüfung und Debugging

**Ziel:** belegte Aussagen über den Zustand des Codes, keine Vermutungen.

### C.1 Ausgangslage

Führe alle drei Suiten und beide Analysewerkzeuge aus und halte das Ergebnis
fest, **bevor** du irgendetwas änderst. Ohne diesen Ausgangswert kannst du
später nicht sagen, ob du etwas verbessert oder kaputtgemacht hast.

### C.2 Bekannte offene Risiken

Diese sind dokumentiert. **Arbeite sie nicht blind ab, sondern prüfe zuerst den
aktuellen Stand im Code:**

1. **App friert zeitweise ein.** Ursache gefunden und behoben (`grab_set` /
   `wait_window` gaben den Griff nicht zurück; jetzt `run_modal` +
   `modal_over` mit `grab_current()`). **Nie reproduziert – Status: nicht
   verifiziert.** Prüfe, ob es weitere Stellen gibt, an denen ein Griff gesetzt
   wird, ohne über `run_modal` zu laufen. Suche gezielt nach `grab_set`,
   `grab_release`, `wait_window`, `wait_variable`.
2. **`insert_tree_items`** – neun Verschachtelungsebenen, die tiefste Stelle im
   Bestand, 144 Zeilen. Analysiere sie auf Fehler, die beim Lesen untergehen.
   **Eine Umstrukturierung ist in diesem Auftrag nicht beauftragt** – melde,
   was du findest, und schlage vor, statt zu handeln.
3. **`sync_current_list_reference()`** schreibt `app_title` in den Titel der
   aktiven Liste zurück. Wer `active_list_id` von Hand umsetzt, ohne
   `app_title` mitzuziehen, benennt beim nächsten `save_items()` eine Liste um.
   Prüfe, ob es im Bestand Stellen gibt, die genau das tun.

### C.3 Systematische Prüfung

Prüfe zusätzlich, jeweils mit Fundstelle und Bewertung:

- **Ressourcen:** Wird jedes `after()` wieder abbestellt? Wird jede geöffnete
  Datei geschlossen? Werden temporäre Verzeichnisse aufgeräumt?
- **Fehlerbehandlung:** Gibt es neue breite `except Exception`, die seit der
  letzten Prüfung hinzugekommen sind? **Die bestehenden 20 wurden bereits
  vollständig geprüft – 19 sind an ihrer Stelle richtig. Diese Analyse nicht
  wiederholen.**
- **Pfadsicherheit:** Halten `validate_attachment_storage`,
  `validate_backup_target` und `inspect_backup_archive` gegen
  Pfad-Traversal? Die Tests decken das ab – prüfe, ob es Lücken gibt.
- **Grenzwerte:** Werden `MAX_UNDO_STEPS`, `MAX_TRASH_ENTRIES`,
  `MAX_FOLDER_DEPTH`, `MAX_LABELS_PER_ITEM`, `MAX_ITEM_DEPTH` überall
  eingehalten, wo sie gelten sollten?
- **Plattformabhängiger Code:** Jede Stelle mit `IS_WINDOWS`, `IS_MACOS`,
  `os.name`, `sys.platform` – ist der jeweils andere Pfad plausibel? **Alles
  wurde bisher nur unter Linux/Xvfb geprüft.**

### C.4 Grenze deiner Befugnis

- **Behebe** eindeutige Fehler mit klarer Ursache und geringem Risiko.
- **Melde und schlage vor**, wo eine Behebung eine strukturelle Änderung
  erfordert.
- **Ändere nichts**, wo du nur einen Verdacht, aber keinen Beleg hast.

Jede Behebung ist ein eigener, abgeschlossener Schritt mit anschließendem
Testlauf. Keine Sammeländerungen.

### C.5 Abnahmekriterium für Block C

Ein Abschnitt in `docs/11_BESTANDSANALYSE.md` (oder eine eigene Datei) mit je
Fund: **Symptom → betroffener Bereich → Ursache oder Verdacht → durchgeführte
Maßnahme → Status → nächster nötiger Test.** Getrennt nach *behoben*,
*gemeldet* und *nicht beurteilbar*.

---

## 6 · Aufgabenblock D – Prozesse analysieren und optimieren

**Ziel:** Wiederholbare Abläufe sind reproduzierbar, dokumentiert und mit einem
Kommando ausführbar.

### D.1 Erst benennen, dann optimieren

„Prozesse" ist mehrdeutig. **Benenne zuerst ausdrücklich, welche Abläufe du
darunter verstehst**, bevor du etwas änderst. Mindestens diese vier:

1. **Prüfprozess** – Syntaxprüfung, drei Suiten, zwei Analysewerkzeuge,
   Sichtprüfung. Heute: fünf bis sechs Einzelaufrufe, von Hand,
   Reihenfolge nur im Kopf.
2. **Versionsprozess** – Version steht an drei Stellen (`VERSION`,
   `APP_VERSION`, Testprüfung) und muss übereinstimmen. Heute: von Hand.
3. **Dokumentationsprozess** – `CHANGELOG.md` plus betroffene Dokumente
   mitführen, laut `AGENTS.md` Teil des Abschlusskriteriums. Heute: von Hand,
   und nachweislich sind drei Dokumente auf 2.11.0 stehen geblieben.
4. **Beispieldatenprozess** – `beispieldaten.py` erzeugt
   `Glide_Beispieldaten.glidebackup`, die Testsuite prüft sie. Ändert sich das
   Werkzeug, muss die Datei neu erzeugt werden. Heute: keine Kopplung, das
   Vergessen fällt erst im Test auf.

### D.2 Was du bauen darfst

Erlaubt und erwünscht ist ein **Prüfskript**, das die Abläufe aus D.1 in der
richtigen Reihenfolge ausführt und ein zusammenfassendes Ergebnis liefert –
etwa `tests/tools/pruefen.py`.

Bedingungen:

- **Nur Standardbibliothek.** Kein `make`, kein `tox`, kein `pytest`, keine
  CI-Konfiguration, keine neue Abhängigkeit.
- Es **ersetzt** die einzeln aufrufbaren Suiten nicht, es ruft sie auf.
- Es meldet je Schritt: ausgeführt / übersprungen / fehlgeschlagen, mit Grund.
- Es kennt einen Schnell- und einen Vollmodus, falls die Sichtprüfung fehlt
  (ImageMagick nicht vorhanden) – ein fehlendes Werkzeug ist kein Fehlschlag,
  sondern ein übersprungener Schritt mit Hinweis.
- Es prüft die Versionskonsistenz aus D.1.2 mit.

### D.3 Was du nicht bauen darfst

- Keine automatische Versionserhöhung.
- Keine automatischen Commits.
- Keine Änderung an der Struktur der drei Testsuiten. Sie sind linear
  geschriebene Skripte, keine pytest-Sammlungen – **eine Umstellung auf pytest
  ist ausdrücklich nicht beauftragt** und würde eine neue Abhängigkeit
  einführen.

### D.4 Abnahmekriterium für Block D

Ein lauffähiges Prüfskript, in `tests/tools/README.md` beschrieben, und ein
kurzer Abschnitt, der die vier Prozesse aus D.1 mit ihrem Vorher/Nachher-Zustand
benennt. Wo du einen Prozess **nicht** verbessert hast, sagst du warum.

---

## 7 · Aufgabenblock E – Drei Arbeitsdokumente im Glide-Format

**Das ist der inhaltlich wichtigste Block. Er ist ausdrücklich keine
Nebenaufgabe.**

### E.1 Was „im Glide-Format" technisch bedeutet

Die Deliverables müssen **nativ in der App bearbeitbar** sein. Das heißt
konkret:

- Format: **`.glidebackup`** – eine ZIP-Datei mit `data.json` (Datenformat 10)
  und optional `attachments/`.
- Erzeugt wird sie über `ListApp.write_complete_backup(pfad, payload)` mit
  `payload = app.complete_backup_payload()`.
- Der Nutzer liest sie über **„Datei → Komplettbackup laden …"** ein.
- **Vorlage und Muster: `tests/tools/beispieldaten.py`.** Baue dein Werkzeug
  nach demselben Aufbau (isoliertes `GLIDE_DATA_DIR`, `Builder`-Hülle,
  Inhalt als lesbarer Quelltext, Kennzahlen-Ausgabe am Ende).

### E.2 Entscheidender Punkt: eine Datei, nicht drei

**Ein Komplettbackup ersetzt beim Einlesen den gesamten Bestand.** Wer drei
Backupdateien nacheinander importiert, überschreibt zweimal seine eigene Arbeit.

**Deshalb: Erzeuge genau eine `.glidebackup`-Datei, die alle drei Inhalte als
getrennte Listen enthält.** Struktur-Vorschlag, den du prüfen und begründet
anpassen darfst:

```
Ordner „Release 1.0"
  ├── Liste „Unterlagen & Assets"
  ├── Liste „Vermarktungsstrategie"
  └── Liste „Feature-Übersicht"
```

Wenn du dennoch getrennte Dateien für sinnvoll hältst, **musst du den Nutzer
ausdrücklich davor warnen**, dass jeder Import den vorherigen Bestand ersetzt,
und ihm den sicheren Weg nennen.

### E.3 Inhaltliche Anforderungen an alle drei Listen

- **Belegt, nicht erfunden.** Jede Aussage über Glide stammt aus dem Quelltext
  oder aus der aktuellen Dokumentation. **Die Dokumentation ist teilweise
  veraltet – im Zweifel gilt der Code.**
- **Recherchiertes kennzeichnen.** Wo du Angaben aus dem Web brauchst (Store-
  Anforderungen, Icon-Größen, Pflichtangaben), recherchierst du mit
  WebSearch/WebFetch und nennst **Quelle und Abrufdatum** im Beschreibungstext
  des Punkts. Rate niemals eine Auflösung, eine Gebühr oder eine Frist.
- **Unsicheres markieren.** Punkte, die auf einer Annahme beruhen, tragen das
  Label „Annahme" (siehe E.4) und nennen im Beschreibungstext, was zu klären
  ist.
- **Nutzbar statt vollständig.** Ein Punkt, den man abhaken kann, ist besser als
  ein Absatz, der alles erklärt. Erklärungen gehören in den Beschreibungstext
  oder in einen Long-Task.
- **Alle vier Punktarten einsetzen**, jede dort, wo sie hingehört:
  `heading` als Zäsur, `group` für zusammengehörige Schritte, `long` für
  mehrzeilige Notizen und Begründungen, `task` für alles Abhakbare.
- **Fälligkeiten relativ zum Erzeugungstag** setzen, nicht als feste Daten.
- **Wichtigkeit** (0–3) nur dort setzen, wo sie eine Aussage trifft.

### E.4 Labels

Lege einen brauchbaren, kleinen Labelsatz an – Vorschlag zur Prüfung:

`Blocker` · `Windows` · `macOS` · `Text` · `Grafik` · `Recht` · `Annahme`

Nutze die vorhandene Palette (`accent`, `flag`, `export`, `delete`, `clear`,
`import`, `due_action`). Beachte: `MAX_LABELS_PER_ITEM = 20`, aber in der
Listenansicht ist nur ein Label je Zeile plus „+n" sichtbar – setze das
wichtigste Label zuerst.

### E.5 Liste 1 – „Unterlagen & Assets für das Release"

**Zweck:** Der Nutzer soll sehen, was er noch beschaffen oder erstellen muss,
bevor Glide veröffentlicht werden kann.

Mindestens abzudecken, jeweils mit konkreter Anforderung statt einer Kategorie:

1. **Anwendungssymbole** – welche Größen und Formate braucht Windows
   (`.ico`, welche Kantenlängen), welche macOS (`.icns`, welche Kantenlängen,
   Retina). Recherchieren, nicht raten.
2. **Store-Screenshots** – geforderte Auflösungen und Mindestanzahl je
   Plattform. **Hinweis für dich:** `tests/tools/screenshots.py` erzeugt bereits
   Aufnahmen unter Linux; für Store-Material braucht es Aufnahmen von den
   Zielplattformen. Nenne das als eigenen Punkt.
3. **Logo und Wortmarke** – welche Ableitungen in welchen Formaten, mit und ohne
   Hintergrund, hell und dunkel.
4. **Store-Texte** – Kurzbeschreibung, Langbeschreibung, Schlagworte,
   Neuerungen-Text; je Plattform mit Zeichenbegrenzung (recherchieren).
5. **Rechtliche Unterlagen** – Datenschutzerklärung, Impressum,
   Lizenzbestimmungen, Altersfreigabe-Fragebogen.
   **Wichtiges Verkaufsargument, das aus dem Code belegt ist:** Glide erhebt
   keine Daten, hat keinen Netzwerkzugriff, kein Konto und keine Telemetrie.
6. **Signaturmaterial** – Windows-Codesigning-Zertifikat,
   Apple Developer Account, Notarisierung. Nenne, was Voraussetzung wofür ist.
7. **Offene Identitätsentscheidungen** – Publisher, Copyright-Zeile,
   Support-E-Mail, Website, Datenschutz-URL, Lizenzmodell, Preis,
   Windows-Zielarchitektur, macOS Bundle Identifier, AppUserModelID,
   Inno-Setup-AppId, Markenrisiko „Glide". Diese stehen bereits in
   `docs/decisions/PRODUCT_IDENTITY.md` als offen – **das sind
   Inhaberentscheidungen, nicht deine.** Nimm sie als Punkte auf, entscheide
   sie nicht.

### E.6 Liste 2 – „Vermarktungsstrategie"

**Zweck:** eine tragfähige, nüchterne Strategie, keine Werbetexte.

Mindestens abzudecken:

1. **Positionierung** – was Glide ist und was es ausdrücklich **nicht** ist.
   Die Nicht-Ziele stehen belegt in `docs/01_PRODUCT_CONSTRAINTS.md`
   (keine Cloud, kein Konto, keine Telemetrie, kein Mehrbenutzerbetrieb,
   keine Mehrsprachigkeit). **Das ist die Positionierung, nicht ihr Mangel.**
2. **Zielgruppe** – wer hat dieses Problem wirklich? Leite es aus den
   tatsächlichen Eigenschaften ab, nicht aus Wunschdenken. Berücksichtige, dass
   die Oberfläche einsprachig Deutsch ist – das begrenzt den Markt und ist eine
   bewusste Entscheidung.
3. **Alleinstellungsmerkmale** – jedes einzelne aus dem Code belegt.
4. **Wettbewerbsumfeld** – recherchiere vergleichbare lokale, konto-freie
   Aufgaben-Apps mit Quelle und Abrufdatum. Ordne Glide ehrlich ein,
   einschließlich der Stellen, an denen es zurückliegt.
5. **Preismodell-Optionen** – nenne Möglichkeiten mit Vor- und Nachteilen.
   **Sprich keine Empfehlung als Entscheidung aus** – das ist eine
   Inhaberentscheidung, und du bist kein Rechts- oder Steuerberater.
6. **Kanäle** – wo diese Zielgruppe erreichbar ist, mit Aufwandsabschätzung.
7. **Reihenfolge** – was vor dem Release passieren muss, was danach.

### E.7 Liste 3 – „Feature-Übersicht"

**Zweck:** eine belegte Übersicht des tatsächlichen Funktionsumfangs, verwendbar
als Grundlage für Store-Texte und die eigene Orientierung.

- **Jeder Eintrag ist aus dem Quelltext belegt.** Wo eine Funktion nur teilweise
  fertig oder nur unter einer Plattform geprüft ist, steht das dabei.
- Gliedere nach Bereichen: Struktur (Listen, Ordner, Gruppen,
  Zwischenüberschriften) · Aufgaben (Arten, Fälligkeit, Uhrzeit, Wichtigkeit,
  Farbe, Beschreibung, Anhänge) · Labels · Ansichten (Eingang, In Bearbeitung,
  Verspätet, Kalender, Ordnerübersicht, Papierkorb) · Bedienung (Mehrfachauswahl,
  Drag & Drop, Tastenkürzel, Umbenennen in der Seitenleiste, Suche, Filter) ·
  Daten (Autosave, Backup-Rotation, Komplettbackup, TXT/Markdown/CSV,
  Rückgängig, Bestandswächter) · Darstellung (Hell/Dunkel, Symboltabelle,
  responsive Spalten).
- **Nimm die bekannten Grenzen mit auf**, klar als solche gekennzeichnet:
  Labels lassen sich in der Aufgabenliste nicht als Chips darstellen
  (`ttk.Treeview`-Grenze); Drag & Drop für Anhänge ist nicht umgesetzt und
  bräuchte eine externe Bibliothek oder einen Win32-Eingriff; nichts ist bisher
  auf Windows oder macOS geprüft.

### E.8 Werkzeug statt Einmal-Artefakt

Erzeuge die Datei über ein Werkzeug im Repository – Vorschlag:
`tests/tools/releasedaten.py`, nach dem Muster von `beispieldaten.py`.

Begründung, die im Projekt bereits einmal teuer war: Beim Übergang von 2.11.0
auf 2.12.0 gingen Werkzeuge verloren, die nur außerhalb des Repositorys
existierten. **Ein Datenbestand, dessen Erzeuger fehlt, lässt sich nicht
fortschreiben.**

Das Werkzeug muss:

- `GLIDE_DATA_DIR` **vor** dem Import auf ein temporäres Verzeichnis setzen,
- die Standardliste ersetzen und den Eingang über `is_inbox_list()` finden
  (`current_list()` zeigt beim ersten Start **nicht** auf den Eingang),
- beim Umsetzen der aktiven Liste **immer `app_title` mitziehen** – sonst
  benennt `save_items()` eine Liste um (siehe C.2.3),
- vor dem Speichern `sync_all_item_kind_labels()` aufrufen,
- am Ende Kennzahlen ausgeben (Ordner, Listen, Punkte, Arten, Labels).

### E.9 Nachweis

Weise nach, dass die Datei tatsächlich einlesbar ist – auf demselben Weg wie ein
echter Import: `inspect_backup_archive` → `validate_backup_schema` →
`normalize_lists_data` → `normalize_trash_data`. Prüfe zusätzlich, dass kein
Punkt auf ein nicht existierendes Label zeigt.

Erweitere `tests/integration/test_glide.py` um eine Prüfung dieser Datei, so wie
es für `Glide_Beispieldaten.glidebackup` bereits geschieht. Damit kann sie nicht
unbemerkt veralten.

Erzeuge zum Schluss einen Screenshot der eingelesenen Daten und sieh ihn dir an.

### E.10 Abnahmekriterium für Block E

- Eine `.glidebackup`-Datei mit allen drei Listen, im Repository unter
  `tests/fixtures/beispiele/` abgelegt **und** dem Nutzer zugestellt.
- Ein reproduzierbares Erzeugungswerkzeug im Repository.
- Eine Testabdeckung, die die Datei prüft.
- Ein Screenshot als Sichtnachweis.
- In `tests/fixtures/README.md` beschrieben.

---

## 8 · Reihenfolge und Abhängigkeiten

Arbeite in dieser Reihenfolge. Die Blöcke bauen aufeinander auf:

```
A (Bestandsanalyse)
   ↓ liefert die Grundlage für
B (Dateistruktur, Archiv)     C (Fehlerprüfung)
   ↓                             ↓
   └──────────┬──────────────────┘
              ↓
        D (Prozesse)
              ↓
        E (Glide-Deliverables)
```

**Begründung:** Ohne A weißt du nicht, was veraltet ist – Block B würde raten.
Block E braucht die Ergebnisse aus A und C, weil die Feature-Übersicht und die
Unterlagenliste auf dem geprüften Ist-Zustand beruhen müssen.

**Nach jedem Block:** alle drei Testsuiten laufen lassen. Ein Block gilt erst
als fertig, wenn sie grün sind.

**Arbeite in kleinen, einzeln prüfbaren Schritten.** Keine Sammeländerung über
mehrere Blöcke hinweg.

---

## 9 · Was du ausdrücklich nicht tust

- Keine Datei löschen.
- Keine neue Laufzeit- oder Testabhängigkeit einführen.
- Das Datenformat nicht ändern.
- `src/glide/app.pyw` nicht in Module zerlegen.
- Die Testsuiten nicht auf ein Framework umstellen.
- Die zehn großen Funktionen nicht aufteilen – nicht beauftragt.
- Die 20 breiten `except Exception` nicht erneut analysieren – bereits erledigt.
- Keine Store-Anforderung, Gebühr, Frist oder Auflösung aus dem Gedächtnis
  angeben. Recherchieren oder als `UNGEKLÄRT` kennzeichnen.
- Keine Inhaberentscheidung treffen (Preis, Lizenz, Publisher, Markenname).
- Keine Rechts- oder Steuerberatung formulieren.
- Nichts als „behoben" bezeichnen, was du nicht reproduziert und nachgeprüft
  hast.

---

## 10 · Umgang mit Unklarheiten

- **Wenn eine vernünftige Annahme möglich ist, triff sie**, kennzeichne sie kurz
  und arbeite weiter. Bremse den Auftrag nicht durch Rückfragen aus.
- **Frag nur nach**, wenn eine fehlende Information das Ergebnis wesentlich
  verändert und keine vertretbare Annahme möglich ist – etwa bei einer
  Entscheidung mit unumkehrbarer Folge.
- **Wenn du etwas nicht feststellen kannst**, schreibe das hin. Verwende
  ausdrücklich: `UNGEKLÄRT`, `NICHT VERIFIZIERT`, `NUR VORGESCHLAGEN`,
  `STATUS UNKLAR`, `NOCH ZU TESTEN`.
- **Wenn dieser Auftrag einer Projektregel widerspricht**, gewinnt die Regel.
  Melde den Widerspruch, statt ihn stillschweigend aufzulösen.

---

## 11 · Definition of Done

Der Auftrag ist fertig, wenn **alle** Punkte erfüllt sind:

1. Alle drei Testsuiten grün, Syntaxprüfung grün.
2. Sichtprüfung erzeugt und angesehen; keine Abweichung, oder Abweichung
   dokumentiert.
3. Versionsangaben in `VERSION`, `APP_VERSION` und der Testprüfung stimmen
   überein; alle Dokumente nennen Version und Datenformat korrekt.
4. Keine Datei gelöscht; jede archivierte Datei auffindbar und ihr Grund
   dokumentiert.
5. `docs/00_INDEX.md` vollständig; kein Verweis zeigt ins Leere.
6. Bestandsanalyse als Datei vorhanden, mit klar getrennten Kategorien:
   Fakt · Befund · Maßnahme · offen · nicht beurteilbar.
7. Die `.glidebackup`-Datei mit allen drei Listen ist erzeugt, geprüft,
   testabgedeckt und dem Nutzer zugestellt.
8. Das Erzeugungswerkzeug liegt im Repository und ist beschrieben.
9. `CHANGELOG.md` fortgeschrieben.
10. Der Abschlussbericht (Abschnitt 12) ist geschrieben.

---

## 12 · Abschlussbericht

Liefere am Ende einen kurzen Bericht mit genau diesen Abschnitten:

1. **Was ich geändert habe** – je Änderung ein Satz, mit Datei.
2. **Was ich gefunden, aber nicht geändert habe** – mit Begründung.
3. **Was ich nicht feststellen konnte** – ausdrücklich als solches.
4. **Was nur du entscheiden kannst** – die Inhaberentscheidungen.
5. **Was noch manuell zu prüfen ist** – vor allem alles Plattformabhängige.
6. **Empfohlener nächster Schritt.**

Halte den Bericht knapp. Er ist eine Übergabe, keine Nacherzählung deiner
Arbeitsschritte – die sind in den Dateien und im Changelog nachlesbar.
