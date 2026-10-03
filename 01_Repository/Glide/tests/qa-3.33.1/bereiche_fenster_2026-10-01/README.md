# Bereiche und Fenster 3.33.1 – Messungen und Vorläufe

01.10.2026 · App 3.33.1 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten

Arbeitsnachweise zum Schnitt „Vier Bereiche und Fensterbedienung“. Die bestandene Abnahme steht in [abschluss_2026-10-01](../abschluss_2026-10-01/README.md); der Volllauf hier (`vollpruefung/ergebnis.json`, Exitcode 1) ist ein Vorlauf.

| Datei | Inhalt |
|---|---|
| `fenstervergleich_final_isoliert.json` | maßgebliche Messung Dialogöffnen/-schließen alt gegen neu, zwölf getrennte Python-Prozesse, erste Runde ausgeschlossen; Werkzeug `fenstervergleich_isoliert.py` |
| `fenstervergleich*.json`, `fenstervergleich.py` | frühere Serien im selben Prozess |
| `fenster_vorher.json`, `fenster_nachher_*.json`, `*.profile.txt` | Einzelmessungen mit Profil; Werkzeug `fenster_probe.py` |
| `features330_stack.txt` | Stack-Sample des Hängers beim Bibliotheks-Archivwechsel (behoben) |
| `svg_varianten.json` | geprüfte SVG-Exportvarianten des Logos |
| `showcase_bereiche_probe.py` | Probe des Showcase im neuen Zeichnungsbereich |
| `pruefverlauf.json`, `vollpruefung*/`, `quellstand*.json` | Vorläufe und Abbrüche mit Ursache; die Rohprotokolle bleiben lokal |

Am 03.10.2026 entfernt: einmalige Bearbeitungs- und Aufräumskripte der Sitzung, ihre Protokolle über damalige Archivkopien und eine Archivkopie des alten Logos. Die Änderungen selbst trägt Git.
