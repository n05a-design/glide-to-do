from dokumente_abgleichen import ROOT, save
import re

path = ROOT / 'docs/09_PROJECT_HANDOFF.md'
text = path.read_text(encoding='utf-8')
text = text.replace('14.590', '14.591')
text = text.replace('| Testsuiten | 3, alle grün (Python 3.12 / Tk 8.6 unter Xvfb) |', '| Testsuiten | 3; Windows-Prüfung mit Python 3.12.12 / Tk 8.6.17 bestanden; aktueller Nachweis im QA-Bericht |')
text = text.replace('| Sichtprüfung | hell und dunkel erzeugt, unauffällig |', '| Sichtprüfung | vorhandene Linux-Aufnahmen plus neue Windows-Aufnahmen der Arbeitslisten; Nachweis in Bestandsanalyse |')
text = text.replace('Hauptsuite, 3.167 Z., linear geschriebenes Skript', 'Hauptsuite, linear geschriebenes Skript')
text = text.replace('Aufruf jeweils: `xvfb-run -a python3.12 <datei>`', 'Gemeinsamer Aufruf: `python tests/tools/pruefen.py --modus schnell`. Unter Linux ohne Display mit Xvfb; unter Windows und macOS mit einer funktionierenden Python/Tk-Installation. Siehe `tests/README.md`.')
text = text.replace('| `docs/decisions/PRODUCT_IDENTITY.md` | **VERALTET** – nennt 2.11.0 und Datenformat 9 |', '| `docs/decisions/PRODUCT_IDENTITY.md` | aktuell: 3.2.0 / Schema 10; offene Inhaberentscheidungen |')
text = text.replace('| `docs/07_QA_BERICHT.md` | **VERALTET** – Stand 2.11.0 |', '| `docs/07_QA_BERICHT.md` | aktuelle Windows-Ausgangs- und Abschlussprüfung, historische Linux-Nachweise getrennt |')
text = text.replace('| `docs/10_RELEASE_CHECKLIST.md` | **VERALTET** – Stand 2.11.0 |', '| `docs/10_RELEASE_CHECKLIST.md` | aktuell: Freigabegates für 3.2.0 |')
text = text.replace('| `docs/05_QA_TESTPLAN.md`, `docs/06_DATA_BACKUP_MIGRATION.md` | STATUS UNKLAR, in dieser Sitzung nicht geprüft |', '| `docs/05_QA_TESTPLAN.md`, `docs/06_DATA_BACKUP_MIGRATION.md` | abgeglichen: Schema 10, Long-Task-Zeilen, aktuelle Normalisierung |')
text = text.replace('| `tests/tools/README.md` | **unvollständig** – beschreibt nur `screenshots.py`, nicht die drei neueren Werkzeuge |', '| `tests/tools/README.md` | vollständig; enthält auch `pruefen.py` und `releasedaten.py` |')
start = text.index('### Außerhalb des Repositorys')
end = text.index('---', start)
text = text[:start] + '''### Äußerer Workspace

`00_Arbeitsvorbereitung/`, `10_Dokumentation/`, `30_Release_Exports/` und
`40_Store_Material/` sind erreichbar und wurden geprüft. Aktive Unterlagen
einschließlich Word-Arbeitsgrundlage und `Produktdatenblatt_3.2.0.md` wurden
abgeglichen; alte Fassungen bleiben im dezentralen Archiv.

Neue Nachweise: `docs/11_BESTANDSANALYSE.md`, `tests/README.md` sowie ein
gemeinsames `glide_releaseplanung_3.2.0.glidebackup` für die drei Arbeitslisten.
Das Einlesen eines Komplettbackups ersetzt den ganzen Bestand; vor einem
manuellen Import eigene Daten vollständig sichern oder einen isolierten
Testdatenordner verwenden.

''' + text[end:]
text = text.replace('- Alle Emoji durch Textzeichen ersetzt:', '- Zentrale Anhangs- und Fälligkeitssymbole durch Textzeichen ersetzt:')
text = text.replace('- **Verhalten auf Windows und macOS insgesamt.** Alle Prüfungen liefen unter\n  Linux/Xvfb.', '- **Manuelles Verhalten auf Windows und macOS insgesamt.** In dieser Runde\n  liefen alle drei automatisierten Suiten auf Windows; die vollständige manuelle\n  Matrix und macOS sind weiterhin offen.')
text = text.replace('Der gemeldete Einfrier-Fehler hat eine\nbehobene Ursache, ist aber unbestätigt', 'Der gemeldete Einfrier-Fehler wurde durch eine\nplausible Grab-Korrektur adressiert, seine Behebung ist aber unbestätigt')
start = text.index('2. **Dokumentation auf 3.2.0 nachziehen.**')
end = text.index('3. **Produktidentität', start)
text = text[:start] + '2. **Dokumentation auf 3.2.0 abgeglichen.** Erledigt einschließlich äußerer\n   Unterlagen. Die Bestandsanalyse hält frühere Widersprüche und Maßnahmen fest.\n' + text[end:]
text = text.replace('`insert_tree_items` 144', '`insert_tree_items` 146')
text = text.replace('- 144 Zeilen, tiefste Verschachtelung', '- 146 Zeilen, tiefste Verschachtelung')
text = text.replace('9. **`tests/tools/README.md` ergänzen** um `analyse_statisch.py`,\n   `analyse_erreichbarkeit.py`, `beispieldaten.py`.', '9. **Prüf- und Erzeugungswerkzeuge dokumentiert.** Erledigt; gemeinsamer\n   Prüfaufruf in `tests/README.md`.')
text = text.replace('11. Arbeitsvorbereitung und Produktdatenblatt stehen auf 2.11.0.', '11. Arbeitsvorbereitung, Word-Dokument und Produktdatenblatt sind auf 3.2.0 abgeglichen.')
text = text.replace('4. **Externe Ordner** (`10_Dokumentation/`, `30_Release_Exports/`,\n   `40_Store_Material/`): Inhalt und Aktualität → `STATUS UNKLAR`', '4. **Externe Ordner:** geprüft; aktive Unterlagen auf 3.2.0 abgeglichen.\n   Fertige signierte Release-Pakete fehlen weiterhin.')
text = text.replace('- **Tests brauchen `xvfb-run`** und ImageMagick (`import`) für Screenshots.', '- **Linux ohne Display braucht `xvfb-run`.** Das bisherige Linux-Screenshotwerkzeug\n  braucht ImageMagick (`import`); Windows-/macOS-Suiten brauchen kein Xvfb.')
start = text.index('## 18. Empfohlener nächster Arbeitsschritt')
text = text[:start] + '''## 18. Empfohlener nächster Arbeitsschritt

Die drei Release-Arbeitslisten aus `glide_releaseplanung_3.2.0.glidebackup`
zuerst in einem isolierten Testdatenordner ansehen. Danach die Windows-Matrix
mit längerer Dialogbenutzung abarbeiten und Produktidentität sowie Vertriebsweg
entscheiden. Vor einem Release sind die im Bestandsbericht belegten Lücken bei
Punkttiefe und Systemlabel-Limit gezielt abzusichern; ein bloß grüner Testlauf
deckt diese Randfälle derzeit nicht ab.

Die Dokumentationskonsolidierung ist erledigt. Der nächste Bearbeiter findet
Inventur, Fundstellen, Maßnahmen und offene Punkte in `docs/11_BESTANDSANALYSE.md`.
'''
text = text.replace('Erstellt für die Übergabe an einen neuen Agenten.', 'Nach der Bestandsanalyse aktualisiert. Die archivierte Vorgängerfassung\nenthält den ursprünglichen Übergabetext. Erstellt für die Übergabe an einen neuen Agenten.')
text = text.replace('Kein Symbolliteral außerhalb der Tabelle.', 'Das ist die Zielregel. Abweichungen im Ist-Code: `GROUP_MARKER` (📁),\n   `IMPORTANCE_MARKERS[3]` (🚩) und `description_suffix` (📝, zwei Ansichten);\n   die reine `ICONS`-Prüfung erkennt sie nicht.')
text = text.replace('`ICONS` (verbindlich, nur Textzeichen)', '`ICONS` (Textzeichen; weitere Marker außerhalb der Tabelle sind noch offen)')
text = text.replace('Die Einfrier-Ursache ist behoben', 'Ein plausibler Einfrier-Mechanismus wurde adressiert')
save('docs/09_PROJECT_HANDOFF.md', text)

old = (ROOT / 'docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md').read_text(encoding='utf-8')
first, rest = old.split('\n', 1)
save('docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md', first + '''

> Referenzauftrag, Ausgangsstand 3.2.0. Am 04.09.2026 anhand des tatsächlichen
> Workspace bearbeitet. Die folgenden ursprünglichen Zustandsannahmen sind
> historisch: Archivordner und aktualisierte 3.2-Dokumente waren bereits
> vorhanden; `tests/tools/README.md` beschrieb schon vier Werkzeuge;
> `PRODUCT_IDENTITY.md` enthielt bereits Schema 10. Windows-Prüfungen wurden
> inzwischen ausgeführt. Die Aufträge und Abnahmekriterien bleiben hier erhalten;
> maßgeblich für Ergebnis und offene Punkte ist `11_BESTANDSANALYSE.md`.
> Die Nummern 03/04 werden nicht künstlich gefüllt; ohne Git-Historie lässt
> sich ihre frühere Belegung nicht feststellen.
''' + rest)

old = (ROOT / 'docs/08_CODE_BEFUND.md').read_text(encoding='utf-8')
first, rest = old.split('\n', 1)
save('docs/08_CODE_BEFUND.md', first + '''

Stand des Abgleichs: 04.09.2026 · App 3.2.0 · Schema 10.
Der folgende Befund erhält die Ergebnisse von 3.0.2/3.1.0 als Historie.
Aktuell gemessen: 14.591 Zeilen, 539 Funktionen/Methoden, 133 Konstanten,
508/520 Methoden erreichbar, 25 Funktionen über 80 Zeilen, 102 doppelte Blöcke,
0 strukturgleiche Methodenpaare, 18 breite `except Exception`.
Die Verzeichnis-Migration ist seit 3.2.0 entfernt. Alle acht Schema-Fixtures
(2 und 4 bis 10) bleiben erhalten. Drei Symbolarten außerhalb `ICONS` sind
noch Emoji. Ein behaupteter Verlust von „Phase 11“ ist aus dem vorliegenden
Bestand ohne Git-Historie nicht nachweisbar. Aktuelle Einzelbefunde und offene
Grenzwerte stehen in `11_BESTANDSANALYSE.md`; historische Kennzahlen unten
sind keine erneuten Prüfnachweise.
''' + rest)

text = (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8')
text = text.replace('Alle Symbole kommen jetzt aus einer Tabelle und sind ausnahmslos Textzeichen.', 'Anhangs- und Fälligkeitssymbole kommen jetzt aus der zentralen Textzeichentabelle.\nDrei weitere Symbolarten sind noch Emoji; siehe Bestandsanalyse.')
text = text.replace('### Symbole: nur noch Textzeichen', '### Symbole: zentrale Textzeichen und dokumentierte Reststellen')
text = text.replace('- **Alle Symbole kommen aus `ICONS`.**', '- **Zentrale Symbole kommen aus `ICONS`.**')
text = text.replace('Im\n  Quelltext steht kein Symbolliteral mehr außerhalb der Tabelle.', 'Außerhalb der Tabelle\n  bestehen noch Gruppen-, Wichtigkeits- und Beschreibungsmarker. Ihre Änderung\n  ist offen; insbesondere beim Gruppenmarker ist TXT-Kompatibilität betroffen.')
marker = '### Entfernt: die Verzeichnis-Migration'
text = text.replace(marker, '''### Bestandsanalyse und Dokumentationsabgleich – 04.09.2026

- Repository-Dokumentation, Startkontext, Übergabe, Produktdaten und Word-
  Arbeitsgrundlage auf den tatsächlichen Stand 3.2.0 / Schema 10 abgeglichen.
  Vorherige Fassungen dezentral archiviert; historische Fixtures bleiben erhalten.
- Windows-Prüfung ausgeführt. Haupttest vom entfernten `system_box` auf die
  reale Baumgeometrie umgestellt; ein Pixel native Schriftmetrik-Toleranz beim
  Kopfblock, unverändert exakte Höhenprüfung mit/ohne Labels. Datenintegritätstest
  wartet beim Start auf Windows-Fenstermapping. Keine Änderung an `app.pyw`.
- `tests/tools/pruefen.py` bündelt Syntax, Versions-/Dokumentabgleich, Fixtures,
  drei Suiten, Analysen und im Vollmodus Reproduktion/Screenshotversuch.
- `tests/tools/releasedaten.py` erzeugt ein gemeinsames importierbares Backup
  mit Unterlagen & Assets, Vermarktungsstrategie und belegter Feature-Übersicht;
  recherchierte Vorgaben tragen Quelle und Abrufdatum.
- `docs/11_BESTANDSANALYSE.md` enthält Inventur, Widersprüche, belegte
  Grenzwertlücken und manuelle Restprüfungen. Die ursprüngliche Einfriermeldung
  bleibt nicht verifiziert; offene Fehler werden nicht als behoben ausgegeben.

''' + marker, 1)
save('CHANGELOG.md', text)

save('requirements/runtime.txt', '# Glide 3.2.0 verwendet ausschließlich die Python-Standardbibliothek.\n# Tk/Tcl muss Bestandteil der verwendeten Python-Installation sein.\n')
print('Übergaben, Referenzstatus und Changelog abgeglichen.')
