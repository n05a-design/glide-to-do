# QA-Bericht – Glide 3.12.0

Stand 13.09.2026 · macOS · Python 3.14.5

Alle App-Importe verwenden temporäre `GLIDE_DATA_DIR`; echte Nutzerdaten wurden nicht als Testbestand geöffnet.

Der abschließende Gesamtlauf mit sechzehn Testsuiten war erfolgreich: [Protokoll](../tests/qa-3.12.0/abschluss/ergebnis.json). Die neue Suite prüft „Mein Tag“ mit listenübergreifender Auswahl, Persistenz, Objektidentität und Schutzregeln.

Die bestehenden Funktionssuiten prüfen identische Aufgabenbackup-Inhalte vor/nach Ansichtshandlungen, globale Reitergrenze und LRU, Gruppenunterpunkte, Wiederholung, Erledigen/Undo, Neustart, Papierkorb, Ordnerquellen, Drag-/Tastaturbewegung, Filter, tatsächliche Dropdown-Auswahl und Anheften-Dialog, Schreibfehler sowie Hell/Dunkel bei 860×700 und 1440×1000. Die 3.11-Suite ergänzt Schnellerfassung und gespeicherte Filter, die 3.12-Suite „Mein Tag“. Keine Tk-Callbackfehler in den geprüften Läufen.

In einer separaten temporären macOS-Testinstanz wurden Pinnwand und Reiter zusätzlich angesehen; Light/Dark-Wechsel und Reiterwechsel per Tastatur wurden sichtbar geprüft. Dies ersetzt keine vollständige native Bedien- oder Barrierefreiheitsabnahme. Bei der anschließenden Ausarbeitung wurden Kartenbreite und Labeldarstellung verbessert; automatische Geometrie-/Funktionstests sind auf dem finalen Quellstand gelaufen.

Die startbare Python-Kopie und sieben Ressourcen stimmen bytegenau mit dem kanonischen Stand überein. [SHA-256-Nachweis](../tests/qa-3.12.0/gepruefter_quellstand_sha256.json). Frühere Arbeitskopien und Dokumentvorfassungen bleiben erhalten.

Native Windows-Abnahme, Screenreader, physisches Trackpad, DPI/Mehrmonitor, realer Ruhezustand und Langzeitbetrieb bleiben offen. Ein erfolgreicher Quelltest ist keine signierte oder veröffentlichte Anwendung.
