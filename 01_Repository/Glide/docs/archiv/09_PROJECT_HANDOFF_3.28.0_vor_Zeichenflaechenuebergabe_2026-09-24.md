# Projektübergabe – Glide 3.28.0

Stand 23.09.2026 · App 3.28.0 · Aufgabenformat 18 · Einstellungen 2 · Vorlagen 2

Kanonisch ist `src/glide/app.pyw`. Die startbare Kopie liegt unter
`07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.28.0.pyw`; 3.27.0 ist im
Unterordner `Archiv` erhalten. Der äußere Projektordner ist kein Git-Checkout.

## Umgesetzter Stand

Der undokumentierte 3.27-UI-Stand wurde als tatsächliche Ausgangsbasis
übernommen. 3.28 ergänzt Tagebuch-Ordner, datierte Notizseiten,
Tagebuch-Metadaten, Suche, Sortierung, Schreibimpulse und vier Vorlagen. Gismo
hat pflegbare Zustände. Pinnwandvorschau, schmale Fenster, Menüschaltflächen,
Notizwerkzeuge, Punktmaske und mittlere Maustaste sind funktional nachgebessert.
Neutrale Nebenaktionen sind app-weit zurückgenommen; semantische Farben bleiben
für Ergebnis, Gefahr, Fälligkeit und Wichtigkeit reserviert.

Nach einer Pflegeaktion von Gismo wird die Startseite nicht mehr vollständig
neu aufgebaut. Die drei Balken ändern sich am vorhandenen Widget, danach setzt
sich nur Gismos Zeichenzustand zurück. Damit ist der besonders im Dopamin-
Design sichtbare weiße Blitz strukturell beseitigt. Recherche, Ursache und Test:
[Flackern und Ablageprüfung 3.28](60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Das Datenformat 18 sichert vor der ersten Migration die unveränderte Datei als
`liste_vor_format18_<Zeitstempel>.json`. Apple Journal war eine
Recherchegrundlage, aber Glide bleibt lokal und behauptet keine Biometrie,
gerätebasierte Vorschläge, Audiotranskription oder iCloud-E2E-Verschlüsselung.
Details: [Tagebuch und UI 3.28](59_TAGEBUCH_UND_UI_3.28.0.md).

## Weiterarbeit und Prüfung

Zuerst [QA-Bericht](07_QA_BERICHT.md), [Release-Checkliste](10_RELEASE_CHECKLIST.md)
und [Daten/Migration](06_DATA_BACKUP_MIGRATION.md) lesen. Bereits erledigte
3.28-Punkte nicht erneut öffnen. Tests immer mit isoliertem `GLIDE_DATA_DIR`.

Wiederholbarer Vollaufruf:

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.28.0/<neuer-Ordner> --timeout 900`

Der Schnelllauf vom 23.09.2026 ist kein vollständiger Abschluss: mehrere alte
OneDrive-Platzhalter sind lokal nicht lesbar, `test_ui_followup36.py` und der
ältere Sammeltest überschritten die verkürzte Laufzeit. Haupttest,
3.28-Funktionstest und Vorlagenworkflow bestanden gezielt. Vor einer Freigabe
zuerst die im QA-Bericht benannten Platzhalter lokal herunterladen und den
Gesamtlauf wiederholen.

Automatisierte Prüfungen ersetzen keine menschliche Freigabe von Installer,
Signatur, macOS, DPI/Mehrmonitor, Screenreader oder realer Mausbedienung. Diese
Grenzen stehen im QA-Bericht und dürfen nicht als abgeschlossen ausgegeben
werden.
