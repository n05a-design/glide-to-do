# Übergabe Glide 3.6.0

Neuerer Stand vom 07.09.2026: [Kachelübersicht, Vorlagenlayout und Jahresanzeige](23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0.md). Die folgenden Prüfstände bleiben als Nachweis ihrer jeweiligen Fassung erhalten.

Stand: 06.09.2026 · Repository: `C:\Users\Timvo\OneDrive\Glide ToDo\01_Repository\Glide`

## Aktuellster Nachtrag: 14 UI-Rückmeldungen

Die danach beauftragte Oberflächenkorrektur ist unter
[UI-Nachbesserung mit Abgleich aller 14 Punkte](22_UI_NACHBESSERUNG_3.6.0.md)
beschrieben. Dazu gehören die feste untere Vorlagenaktionsleiste, einheitliche
Buttons, schmale Ansichten, Labelhover, zweispaltige Einstellungen,
Akzent-Auswahlfarben, Hauptmondphasen und angehobene Navigationssymbole.
Die neuen Belege liegen separat unter `tests/qa-3.6.0/ui-nachbesserung/`;
der frühere Vollabschluss unter `abschluss/` bleibt historisch unverändert.


## Aktueller Arbeitsstand

Die ursprünglichen Wünsche und die bestätigten Ergänzungen sind in
[20_FEATURE_ABGLEICH_3.6.0.md](20_FEATURE_ABGLEICH_3.6.0.md) einzeln abgeglichen.
Die kanonische App liegt in `src/glide/app.pyw`, Version in `VERSION`.
Aufgabendaten bleiben Format 11. Einstellungen verwenden Format 2, der
Vorlagenkatalog Format 1.

Die 3.6-Arbeit wurde aus dem vorhandenen lokalen Stand vervollständigt. Die
überlieferten Shellausgaben aus Claudes `/tmp/glide` sind historische Hinweise
und kein Nachweis des Windows-Quellstands. Die frühere 3.5-Prüfung bleibt unter
`tests/qa-3.6.0/ausgang-3.5.0` erhalten.

## Fertige Bereiche

Die Systemseitenleiste hat getrennte Symbol-/Titelspalten und einen Zähler.
Startseitenlogo, Aktionskonturen, Scrollabstand, Mondphase und Jahresraster sind
angepasst. Punktarten und Listenziele werden farbig angeboten; neue Listen und
Ordner besitzen eine vollständige Maske. Einzeilige Punkte lassen sich per
verzögertem Klick umbenennen. Einstellungen enthalten Schriftgröße, Akzent,
Startansicht, Wochenbeginn und getrennte Darstellungsoptionen.

Vorlagen besitzen eine eigene Seite, Bearbeiten-/Speichern-Modus und Austausch
als `.glidetemplates`. Eigene Listen/Ordner können mit Struktur und Anhängen als
Vorlage gespeichert werden. Teilbackups verwenden den geprüften portablen
Backupweg und werden ergänzend importiert. Datenordner können geöffnet oder in
eine leere Ablage kopiert werden. Eine bekannte Fremdsperre führt zum Schreibschutz.

Vier DejaVu-Sans-TTF-Schnitte mit Lizenz liegen unter `src/glide/resources/fonts`.
Windows registriert sie privat; macOS-Code ist vorhanden, aber auf diesem Rechner
nicht nativ geprüft. Die Materialoptik aus getönten Flächen und Glaskanten ist
abschaltbar. Ein echter Blur durch die Tk-Seitenleiste ist nicht umgesetzt.

## Prüfen und Belege

```powershell
C:\Python312\python.exe tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.6.0/abschluss
```

Die Suiten isolieren die Daten vor dem Import über `GLIDE_DATA_DIR`.
Sieben Suiten, statische Prüfung, Versions-/Dokumentationsprüfung und
Fixture-Reproduktion gehören zum vollständigen Lauf. Den verbindlichen
Abschlussstatus und verbleibende manuelle Grenzen nennen
[18_QA_3.6.0.md](18_QA_3.6.0.md) und die dort verlinkten Rohlogs.

Zusätzlich: `tests/integration/test_release36.py --screenshots PFAD` prüft
Teilbackup mit echten Dateibytes, Vorlagenbearbeitung, Anlage, Fonts, Rename,
Labelgrenze, Punkttiefe, Datenordner und generiert ergänzende Windows-Bilder.
`tests/tools/leistungspruefung.py` erzeugt die Rohmessung zum Leistungsbericht.

## Nicht erneut als offen beginnen

Die vollständigen Anlegemasken, private Schriftregistrierung, Vorlagenseite,
Dateianhänge in Teilbackups, Mondphase, Jahresanzeige und Datenordner-Menüs
sind implementiert. Ihre Bedienwege weiterprüfen, aber nicht mit den alten
Platzhaltern aus der Übergabe gleichsetzen.

Historische Markdown-Berichte sind versioniert oder als historische Analysen
markiert. Aktuelle Einstiege sind der [Index](00_INDEX.md), diese Übergabe,
Funktionsmatrix, QA- und Leistungsbericht.

## Verbleibende Freigaben

Offen sind echte macOS-Ausführung, Signierung/Installer/Store, Anbieteridentitäten,
komplette DPI-/Mehrmonitor-/Accessibility-Matrix, Langzeitnutzung und ein realer
OneDrive-Zweirechnerlauf. Die Sperrdatei ersetzt keinen verteilten Abgleich.
Native rechteckige Treeview-Auswahl ist die ausdrücklich akzeptierte UI-Grenze.
Für echten selektiven Desktop-Blur wäre ein anderer Kompositionsaufbau nötig;
Details im [Glasbericht](19_GLASS_SURFACE_3.6.0.md).

Für weitere Änderungen zuerst die Funktionsmatrix und das Abschlussprotokoll
lesen, danach gezielt den betroffenen Bedienweg mit isolierten Daten prüfen.
