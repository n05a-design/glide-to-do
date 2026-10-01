# Entwicklungsnotizen 3.28.0

Stand 24.09.2026 · Glide 3.29.0 · Datenformat 19


Standard-Tk bleibt die Laufzeitbasis. Der neue RichNoteEditor speichert Text und semantische Spannen statt HTML; die Positionen im Dateiformat sind Python-Zeichenindizes. Tk-Indizes werden beim Laden aus Zeilen und nativen Tcl-Spalten erzeugt. Ein lokaler Undo-Stapel umfasst Text und Formatierung gemeinsam.

Pinnwand-Vorschau und echte Pinnwandpositionen sind getrennt. Eine verdichtete Vorschau darf niemals die Modellkoordinaten zurückschreiben. Verbindungen werden über Punktkennungen gespeichert; Änderungen an ausgewählten Verbindungen ändern beide Endpunkte gemeinsam, nicht fremde Kanten.

Migrationen sichern unveränderte Originaldateien, bevor der neue Aufgabenstand geschrieben wird. Der Verlaufszeitraum wird beim Normalisieren sowie vor dem Speichern begrenzt. Benutzerdefinierte Startseitenanordnungen werden nicht durch die neue Standardreihenfolge überschrieben.


## Geometrie und Ereignisse 3.26

ButtonFlow verwendet je Umbruchzeile einen eigenen Frame. Gemeinsame Grid-Spalten über mehrere Zeilen würden sonst die jeweils größte Spaltenbreite erzwingen und trotz passender Summen Buttons abschneiden. Im übergeordneten Frame angelegte Buttons müssen über den Zeilenframes angehoben werden.

Die Aufgaben-Scrollbar einer Notizliste hat Anforderungshöhe 1; sonst vergrößert ihre Standardhöhe den auf sechs Zeilen begrenzten Treeview. FieldPairGrid entfernt bei einspaltigem Layout die gemeinsame Spaltenuniformität. Zoom verändert ausschließlich die Darstellung; Druck und gespeicherte Kartenpositionen verwenden logische Koordinaten.
