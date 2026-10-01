from pathlib import Path
from datetime import datetime
import json, shutil
R=Path.cwd();B=Path(__file__).parent;D=R/'50_Ablage/Archiv/Werkzeuge_3.21.4'
result=json.loads((R/'01_Repository/Glide/tests/qa-3.21.4/abschluss/ergebnis.json').read_text())
assert result['exitcode']==0
stamp=datetime.fromisoformat(result['zeitpunkt']).strftime('%d.%m.%Y um %H:%M')
proof=D/'Pruefnachweise';proof.mkdir(exist_ok=True)
for name in ('ausgangsbestand.json','archivpruefung.json','paketabgleich.json','aktive-dateien-sha256.json','standpruefung-gegenprobe.json','standpruefung-gegenprobe-korrigiert.json','erinnerungsabgleich-gegenprobe.json','beispielabgleich-befund.json','manifest-vorpruefung.json','abschluss-dokumente.json','fortschreiben-original-probe.log','uebernahme.log','pruefen.py.diff','standpruefung.py.diff'):
 p=B/name
 if p.exists():shutil.copy2(p,proof/name)
shutil.copytree(B/'baseline-3.21.3',proof/'baseline-3.21.3',dirs_exist_ok=True)
for name in ('uebernehmen_geprueft.py','ergänzungen.json','abschluss_dokumentieren.py','nachweise_ablegen.py','bestand_verifizieren.py'):
 shutil.copy2(B/name,proof/name)
(D/'ABLAGE.txt').write_text('Originalpaket: ../Uebertragungspakete/glide-3.21.4-ablagepaket.zip\nOriginalwerkzeuge und quellstand/ bleiben als Eingangsstand unverändert.\nDie ausgeführten Nacharbeiten und Prüfergebnisse liegen unter Pruefnachweise/.\nMaßgeblich ist der eingeordnete Repository-Stand, einschließlich der Korrektur in standpruefung.py.\nDie Original-Ablageskripte sind historische Werkzeuge; ein erneuter Lauf würde spätere Korrekturen überschreiben.\n')
text=f'''# Ablageprotokoll – Glide 3.21.4

Abgeschlossen am {stamp} · macOS · Python 3.14.5

## Ergebnis

Das Paket aus „Claude outputs“ ist vollständig in die bestehende Arbeitsablage
eingearbeitet. Der Eingangsordner ist leer. Quellstand, Arbeitskopie,
Beispieldaten und Dokumentation führen Version 3.21.4.

- **Repository:** `01_Repository/Glide`, Aufgabenformat 15, Einstellungen 2, Vorlagenformat 2.
- **Startbare Arbeitskopie:** `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.21.4.pyw`; Anwendung und sieben Ressourcendateien bytegenau mit dem Repository abgeglichen.
- **Beispieldaten:** die drei Dateien für 3.21.4 unter `05_Probelisten_Testdaten`.
- **Dokumentation:** aktuelle Fassungen unter `00_Arbeitsvorbereitung`, `10_Dokumentation`, `40_Store_Material` und im Repository aktualisiert; Abschlussbefund in derselben Version nachgetragen.

## Prüfung

Der vollständige macOS-Lauf bestand mit **Exitcode 0**: **39 Schritte, 37 ausgeführt**,
alle **25 Testsuiten**, drei Analysen, Syntax-, Versions-, Dokument- und Fixtureprüfung
sowie die Reproduktion der Beispiel- und Releasedaten.

[Abschlusslauf](../../../01_Repository/Glide/tests/qa-3.21.4/abschluss/ergebnis.json).
Der Ausgangsstand 3.21.3 bestand zuvor den Schnelllauf mit allen 25 Testsuiten
und drei Analysen: [Ausgangstest](Pruefnachweise/baseline-3.21.3/ergebnis.json).
Zusätzlich wurden lokale Verweise außerhalb des Repositorys und alle Archivkopien geprüft.

## Ergänzende Korrekturen bei der Übernahme

- Das Original-Ablageskript sicherte nicht alle ersetzten Quelldateien. Die Übernahme archivierte auch Quellcode, VERSION, Tests, Prüfwerkzeuge und CHANGELOG im jeweiligen Ordner.
- Die neue Regel R6 erfasste irrtümlich das Wortende in „Vorlagenformat 2“. Eine Wortgrenze trennt Aufgabenformat 15 von Vorlagen- und Einstellungsformat 2. Gültige und absichtlich ungültige Angaben wurden geprüft; R6 bis R8 reagieren wie erwartet.
- Der erste Gesamtlauf bestand alle 25 Suiten und drei Analysen, scheiterte aber am Beispielabgleich nach dem Tageswechsel. `pruefen.py` vergleicht feste Erinnerungen jetzt nach Tagesabstand und Ortszeit; echte Zeitabweichungen bleiben Fehler. Die mitgelieferten Beispieldaten bleiben unverändert. [Erster Prüflauf](../../../01_Repository/Glide/tests/qa-3.21.4/vor_Korrektur_Erinnerungsabgleich/ergebnis.json).
- Verbliebene falsche Angaben zu Aufgabenformat, Planungsterminen ohne Fälligkeit, garantierten Kalenderaktualisierungen und historischen Prüfläufen korrigiert. Falsche Produktdatenblatt-Verweise und widersprüchliche Archivhinweise bereinigt.
- Das Produktdatenblatt hätte einen noch nicht ausgeführten Test als bestanden bezeichnet. Es nennt jetzt Datum und Ergebnis des tatsächlich abgeschlossenen Laufs.
- Die Befundtabelle führt zehn Codeaussagen auf; die nicht belegte Überschrift mit zwölf Aussagen wurde in den aktuellen Übergabedokumenten berichtigt. Originalpaket und historische Fassungen bleiben erhalten.
- Das QA-Dateimanifest wurde auf den tatsächlichen Bestand aktualisiert; das vorherige Manifest ist archiviert. Historische Renderdateien wurden nicht bearbeitet.

**Anwendungscode:** Gegenüber 3.21.3 wurde ausschließlich `APP_VERSION` geändert.
Keine neue Laufzeitabhängigkeit, kein neues Datenfeld und kein Formatsprung.

## Archivierung und Nachvollziehbarkeit

**70 ersetzte oder verschobene Ausgangsdateien** sind mit unverändertem Inhalt in
Archiven nachgewiesen. Weitere Zwischenfassungen der Abschlussdokumentation und
das bisherige QA-Dateimanifest sind ebenfalls erhalten. Historische versionierte
Release-Fixtures bleiben bewusst aktiv: Sie prüfen die Lesbarkeit alter Daten.

- [Prüfsummen der Ausgangsdateien und Archivziele](Pruefnachweise/archivpruefung.json)
- [Abgleich der 15 Paketziele](Pruefnachweise/paketabgleich.json)
- [Prüfsummen der aktuellen Arbeitsdateien](Pruefnachweise/aktive-dateien-sha256.json)
- [Gegenproben der korrigierten Standprüfung](Pruefnachweise/standpruefung-gegenprobe-korrigiert.json)
- [Unverändertes Originalpaket](../Uebertragungspakete/glide-3.21.4-ablagepaket.zip)

Alle Tests liefen mit temporärem `GLIDE_DATA_DIR`. Echte Nutzerdaten wurden nicht geöffnet oder importiert.

## Verbleibende manuelle Prüfungen

Die automatische Screenshot-Erzeugung und die Sichtprüfung wurden im Prüflauf
übersprungen. Native Sichtabnahme auf macOS/Windows, DPI-/Mehrmonitorprofile,
Screenreader, Langzeitbetrieb, Installer und Signierung bleiben offen.
Die Ablage- und automatisierte Quellprüfung sind abgeschlossen; es wurde kein
signiertes Veröffentlichungspaket erzeugt.
'''
(D/'Ablageprotokoll_2026-09-15.md').write_text(text)
print('Ablageprotokoll und Nachweise im Werkzeugarchiv abgelegt.')
