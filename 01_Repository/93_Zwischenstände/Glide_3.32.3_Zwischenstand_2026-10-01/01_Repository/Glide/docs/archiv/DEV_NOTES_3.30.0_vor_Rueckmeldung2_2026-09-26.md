# Entwicklungsnotizen 3.28.0 bis 3.30.0

Stand 26.09.2026 · Glide 3.30.0 · Datenformat 20


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


## Muster aus den Runden vom 26.09.2026

- **Leere Rahmen schrumpfen nicht:** Ein Grid- oder Pack-Rahmen ohne Kinder
  behält in Tk seine letzte Größe. Wer alle Kinder entfernt, schaltet
  `grid_propagate(False)` und setzt `height=1`.
- **Wunschbreiten nach Änderungen:** `winfo_reqwidth()` eines Rahmens stimmt
  erst nach dem Leerlauf. Direkt nach einer Änderung die Kinder messen
  (`packed_width`).
- **Packreihenfolge entscheidet:** Wer vor einem dehnbaren Widget gepackt
  ist, bekommt zuerst Platz. Feste Knöpfe gehören vor dehnbare Felder
  (`search_row_anchor`, Kalenderknöpfe `before=border`).
- **Kurzlebige Konfigurationsereignisse:** Beim Neuaufbau meldet das
  Hauptfenster kurz 1 px; Höhenstufen ignorieren das.
- **Farben als Rollen:** Schrift nur über Designrollen setzen. Die
  Nachkorrektur und `test_kontrast330` erfassen nur Rollen und Knöpfe.
- **Mehrfachschlüssel in Dialogen:** `themed_choice_dialog` nimmt Farben als
  Liste nach Position oder als Wörterbuch nach Wert.
- **Prüfwerkzeuge:** In Messungen nur erwartete Tk-Fehler abfangen. Ein
  abgefangener `AttributeError` lieferte einmal eine falsche Null.
- **Durchsicht in Tk:** Es gibt keine transparenten Flächen.
  - Ein `Frame` mit `bg=""` zeichnet unter macOS nichts und lässt den
    Untergrund sehen. Unter Windows zeigt er Bildreste, weil Kindfenster
    geclippt werden – nicht verwenden.
  - Plattformunabhängig: Jede Fläche zeichnet ihren Ausschnitt selbst, etwa
    ein Bild-Label an negativer Position oder ein Canvas-Bildelement.
  - Große Bild-Labels kosten bei jedem Neuzeichnen die volle Bildgröße. Rahmen
    bekommen deshalb einen passgenauen Ausschnitt
    (`photo copy -from … -shrink`).
- **Eigene Label-Ersatzwidgets messen wie Labels:** Ein Tk-Label ist Zeilenhöhe
  plus 2 × (Rand 2 + pady) hoch. Die Textbox einer Canvas ist senkrecht genau
  die Zeilenhöhe, waagrecht 2 Pixel breiter als die Schrift. `CanvasLabel`
  gleicht beides aus (`LABEL_INSET_X/Y`); sonst verrutschen getestete Höhen.
- **Weiterleitung statt fremder Bindtags:** Ein Hintergrund-Label mit
  `bindtags((rahmen, "all"))` reichte Klicks an den Rahmen weiter – aber auch
  seine eigenen `<Configure>`-Meldungen. Handler, die `event.width` lesen,
  rechneten dann mit den Maßen des Bildes. Unter macOS stürzte Tk dabei ab
  (`XMoveResizeWindow`, 26.09.2026).
  - Richtig ist ein eigenes Bindtag mit `event_generate` für die
    Mausereignisse (`GlideBackdrop`).
- **Neu packen hängt hinten an:** `pack()` auf ein vergessenes Widget reiht
  es am Ende ein – bei `side="right"` also links. Wer Knöpfe ein- und
  ausblendet, packt die ganze Reihe in fester Reihenfolge neu.
- **ttk-Stile ableiten:** `Name.Basisstil` erbt Optionen und Layout. So
  bekommt eine einzelne Liste eine eigene Hintergrundfarbe, ohne den
  gemeinsamen Stil zu ändern.
- **Veraltete Objekte in Tests:** Nach Rückgängig sind Listenobjekte neu.
  Referenzen frisch aus `app.lists` holen.

