# Entwicklungsnotizen 3.28.0

Stand 25.09.2026 · Glide 3.30.0 · Datenformat 20


Standard-Tk bleibt die Laufzeitbasis. Der neue RichNoteEditor speichert Text und semantische Spannen statt HTML; die Positionen im Dateiformat sind Python-Zeichenindizes. Tk-Indizes werden beim Laden aus Zeilen und nativen Tcl-Spalten erzeugt. Ein lokaler Undo-Stapel umfasst Text und Formatierung gemeinsam.

Pinnwand-Vorschau und echte Pinnwandpositionen sind getrennt. Eine verdichtete Vorschau darf niemals die Modellkoordinaten zurückschreiben. Verbindungen werden über Punktkennungen gespeichert; Änderungen an ausgewählten Verbindungen ändern beide Endpunkte gemeinsam, nicht fremde Kanten.

Migrationen sichern unveränderte Originaldateien, bevor der neue Aufgabenstand geschrieben wird. Der Verlaufszeitraum wird beim Normalisieren sowie vor dem Speichern begrenzt. Benutzerdefinierte Startseitenanordnungen werden nicht durch die neue Standardreihenfolge überschrieben.


## Geometrie und Ereignisse 3.26

ButtonFlow verwendet je Umbruchzeile einen eigenen Frame. Gemeinsame Grid-Spalten über mehrere Zeilen würden sonst die jeweils größte Spaltenbreite erzwingen und trotz passender Summen Buttons abschneiden. Im übergeordneten Frame angelegte Buttons müssen über den Zeilenframes angehoben werden.

Die Aufgaben-Scrollbar einer Notizliste hat Anforderungshöhe 1; sonst vergrößert ihre Standardhöhe den auf sechs Zeilen begrenzten Treeview. FieldPairGrid entfernt bei einspaltigem Layout die gemeinsame Spaltenuniformität. Zoom verändert ausschließlich die Darstellung; Druck und gespeicherte Kartenpositionen verwenden logische Koordinaten.


## Muster aus 3.30

- **Tk-Canvas heben:** `Canvas.lift` hebt Zeichenelemente (`tag_raise`),
  nicht das Widget. Ein Canvas-Widget (etwa `RoundedButton`) über andere
  Widgets zu heben geht mit `widget.tk.call("raise", widget._w)`.
- **Canvas-Neuaufbau:** `<FocusIn>` und `<Configure>` der Pinnwand rufen
  `draw_board` auf, und `delete("all")` leert die Fläche. Was dauerhaft zu
  sehen sein soll (Folienangabe, Ziehpunkte, Hintergrund), gehört deshalb in
  `draw_board` selbst.
- **Wiederholtes Zeichnen:** Linien, die bei jeder Mausbewegung neu gezeichnet
  werden, vorher löschen (`delete("connection")`).
- **Widgets beim Schließen:** Rückrufe von `<Configure>` laufen beim Schließen
  noch einmal. Vor dem Anlegen von Kind-Widgets `winfo_exists()` des Rahmens
  prüfen.
- **`after`-Aufträge:** an `<Destroy>` des Hauptfensters binden und dort
  abbrechen – sonst meldet Tk später „invalid command name“.
- **`item_change(item_ids)`:** Die Methode wählt nach dem Neuaufbau die
  übergebenen Punkte aus. Wer die Auswahl dort lassen will, wo sie ist (etwa
  der Detailbereich), übergibt `()` und ruft `change.mark()`.
- **Tastenereignisse in Tests:** `event_generate("<Return>")` erreicht ein
  Feld nur, wenn es den Tastaturfokus hat. `focus_force()` davor macht den
  Test unabhängig vom Vordergrundprogramm.
- **Modale Dialoge in Tests:** Neue Dialoge auf bestehenden Wegen (etwa die
  Importvorschau seit 3.30) lassen ältere Tests auf Eingaben warten.
  `run_modal` durch `press(beschriftung)` ersetzen.

