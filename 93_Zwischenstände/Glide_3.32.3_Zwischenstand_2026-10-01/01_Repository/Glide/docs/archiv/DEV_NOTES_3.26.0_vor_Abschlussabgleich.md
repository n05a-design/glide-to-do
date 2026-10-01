# Entwicklungsnotizen 3.26.0

Stand 20.09.2026 · Glide 3.26.0 · Datenformat 17


Standard-Tk bleibt die Laufzeitbasis. Der neue RichNoteEditor speichert Text und semantische Spannen statt HTML; die Positionen im Dateiformat sind Python-Zeichenindizes. Tk-Indizes werden beim Laden aus Zeilen und nativen Tcl-Spalten erzeugt. Ein lokaler Undo-Stapel umfasst Text und Formatierung gemeinsam.

Pinnwand-Vorschau und echte Pinnwandpositionen sind getrennt. Eine verdichtete Vorschau darf niemals die Modellkoordinaten zurückschreiben. Verbindungen werden über Punktkennungen gespeichert; Änderungen an ausgewählten Verbindungen ändern beide Endpunkte gemeinsam, nicht fremde Kanten.

Migrationen sichern unveränderte Originaldateien, bevor der neue Aufgabenstand geschrieben wird. Der Verlaufszeitraum wird beim Normalisieren sowie vor dem Speichern begrenzt. Benutzerdefinierte Startseitenanordnungen werden nicht durch die neue Standardreihenfolge überschrieben.
