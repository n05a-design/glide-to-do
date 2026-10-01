# Prüfplan – Glide 3.16.0

Stand 13.09.2026 · alle App-Tests mit isoliertem `GLIDE_DATA_DIR`

Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.16.0/abschluss`. Zwanzig Suiten, Syntax, Versions-/Dokument-/Fixtureprüfung, statische Analysen sowie reproduzierte Beispiel- und Releasedaten.

Die bisherigen Prüfungen für Datenintegrität, Migration, Vorlagen, Wiederholung, Benachrichtigungen und 3.9-Oberfläche bleiben erhalten. `test_workspace310.py` ergänzt:

- Aufgabenbackup vor/nach Öffnen, Schließen, Anheften, Bewegen und Abheften inhaltlich identisch.
- Globale Reitergrenze, LRU, Dubletten, Umordnung ohne Aufgabenumsortierung.
- Bearbeitung derselben Objekte, Erledigen/Undo, Gruppenunterpunkte, wiederkehrende Termine.
- Tatsächliche Tk-Tastatur- und Drag-Ereignisse, Label-/Textfilter und Wiederfinden weit entfernter Karten.
- Neustart mit gespeichertem Sichtzustand; Papierkorb entfernt Referenzen, Undo öffnet sie nicht erneut.
- Ordnerpinnwand mit Punkten aus Unterlisten und Wechsel zur richtigen Quellliste.
- Hell/Dunkel, 860×700 und 1440×1000, ein-/ausgeblendete Seitenleiste, Rückkehr von Startseite/Vorlagen, lange Texte.
- Ungültige Einstellungen und Schreibfehler ohne Verlust vorheriger Ansichtseinstellungen; keine Tk-Callbackfehler.
- Schnellerfassung mit deutscher Fristvorschau, Zielliste, Mehrfacherfassung und Undo; gespeicherte Filter mit dynamischen Zeiträumen, entfernten Referenzen, Trefferzahl und Einstellungs-Rollback.
- „Mein Tag“ mit listenübergreifender Auswahl, stabiler Reihenfolge, unabhängiger Fälligkeit, Persistenz und Schutz vor entfernten oder strukturellen Punkten.
- Tabellenansicht mit flacher Darstellung verschachtelter Aufgaben, identischen Punktaktionen, Such-/Offenfilter und listenspezifischer Spaltenauswahl in den Einstellungen.

Zusätzliche manuelle Abnahme: native Windows- und macOS-Eingabegeräte, Screenreader, mehrere Monitore/DPI, Schlafen/Aufwachen und Langzeitbetrieb. [QA-Bericht](07_QA_BERICHT.md) dokumentiert tatsächlich ausgeführte Nachweise.

`test_features316.py` prüft Archivaufbau und Abschnittstrennung, den Rundlauf über echte Dateien, die Verträglichkeit mit dem Aufgabenimport, alle Vorschauwerte, sieben Varianten ungültiger Zusatzabschnitte, Nicht-Archiv und fremdes Archiv, die vier Teilbereiche einzeln und gemeinsam, das Verwerfen der Ansichtsverweise, die drei Rückfallsicherungen, leere Auswahl, Abbruch, gesperrte Bereiche und den Dialog in beiden Themes. [Bedienung 3.16](40_APP_BACKUP_3.16.0.md).

`test_features315.py` prüft die Rechenregeln der Aufwandsbilanz samt Grenzwerten, die Normalisierung und den Rückfall der Tageskapazität, Menge, Reihenfolge, Zähler und Leertext der Tagesplanung, den Tageswechsel, Such- und Offenfilter, Punktaktionen mit Rückgängig, ungültige Bearbeitungstage, das Serienvorrücken, die von Filtern abhängige Tabellensumme, die Startseitenzeile sowie den Einstellungsdialog in Hell/Dunkel bei 780×640. [Bedienung 3.15](39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

`test_features314.py` prüft leere Altwerte, ungültige Datums-/Minutenwerte und Grenzen, Originaldateisicherung und Sicherungsfehler, Neuladen, Vollbackup, Papierkorb, Vorlagen mit relativen Terminen, TXT-Rundlauf, Markdown/CSV, Mehrfachbearbeitung mit Erhalten/Löschen, Undo, Artwechsel und Wiederholungen. Echte Dialoge prüfen Speichern, Validierung und Abbruch in Hell/Dunkel bei 780×640. [Bedienung 3.14](37_PLANUNG_UND_AUFWAND_3.14.0.md).
