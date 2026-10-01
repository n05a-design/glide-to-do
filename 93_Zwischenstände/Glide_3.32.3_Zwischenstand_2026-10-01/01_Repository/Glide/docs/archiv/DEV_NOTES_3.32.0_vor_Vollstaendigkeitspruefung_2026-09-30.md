# Entwicklungsnotizen 3.28.0 bis 3.30.0

Stand 30.09.2026 · Glide 3.32.0 · Datenformat 20


Standard-Tk bleibt die Laufzeitbasis. Der neue RichNoteEditor speichert Text und semantische Spannen statt HTML; die Positionen im Dateiformat sind Python-Zeichenindizes. Tk-Indizes werden beim Laden aus Zeilen und nativen Tcl-Spalten erzeugt. Ein lokaler Undo-Stapel umfasst Text und Formatierung gemeinsam.

Pinnwand-Vorschau und echte Pinnwandpositionen sind getrennt. Eine verdichtete Vorschau darf niemals die Modellkoordinaten zurückschreiben. Verbindungen werden über Punktkennungen gespeichert; Änderungen an ausgewählten Verbindungen ändern beide Endpunkte gemeinsam, nicht fremde Kanten.

Migrationen sichern unveränderte Originaldateien, bevor der neue Aufgabenstand geschrieben wird. Der Verlaufszeitraum wird beim Normalisieren sowie vor dem Speichern begrenzt. Benutzerdefinierte Startseitenanordnungen werden nicht durch die neue Standardreihenfolge überschrieben.


## Geometrie und Ereignisse 3.26

ButtonFlow verwendet je Umbruchzeile einen eigenen Frame. Gemeinsame Grid-Spalten über mehrere Zeilen würden sonst die jeweils größte Spaltenbreite erzwingen und trotz passender Summen Buttons abschneiden. Im übergeordneten Frame angelegte Buttons müssen über den Zeilenframes angehoben werden.

Die Aufgaben-Scrollbar einer Notizliste hat Anforderungshöhe 1; sonst vergrößert ihre Standardhöhe den auf sechs Zeilen begrenzten Treeview. FieldPairGrid entfernt bei einspaltigem Layout die gemeinsame Spaltenuniformität. Zoom verändert ausschließlich die Darstellung; Druck und gespeicherte Kartenpositionen verwenden logische Koordinaten.


## Muster aus 3.30

- **Tk 9 und `place` im Textfeld (27.09.2026):** Kinder eines Textfelds, die
  mit `place` stehen, setzen unter Tk 9 am Innenabstand (padx/pady) an, unter
  Tk 8.6 am Rand. `PageEditor.place_origin` misst den Ursprung einmal je
  Innenabstand. Anzeigezeilen misst `count -update -ypixels`; `dlineinfo`
  liefert für eine unsichtbare Zeile nichts.
- **Umfluss mit Rändern:** `lmargin1`/`lmargin2`/`rmargin` wirken je
  Anzeigezeile nach dem Tag ihres ersten Zeichens. Ein Tag über genau den
  Zeichen neben dem Bild ergibt Umfluss; eine unsichtbare Ankerzeile
  (`elide`) verschmilzt mit der folgenden Zeile.
- **Nichts auspacken, was sich andere merken:** Pinnwand und Reiter merken
  sich `pack_slaves()` samt Optionen. Ein Widget, das dazwischen ausgepackt
  wird, fehlt nach dem Zurückwechseln. Zum Verstecken leeren statt
  auspacken (`_hint_blank`).

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
- **Tk-Tempo unter macOS** (Messungen 26.09.2026):
  - Jedes eingebettete Widget ist ein eigenes natives Fenster. Beim Scrollen
    einer Canvas bewegt Tk alle, und jedes bekommt `<Configure>`. Neu
    gezeichnet wird deshalb nur bei Größenänderung (`bind_resize`).
  - Ein Bild in einem Label oder Canvas wird bei jedem Neuzeichnen komplett
    umgewandelt. Große Bilder, die zum Großteil verdeckt sind, kosten trotzdem
    ihre volle Fläche. Nur sichtbare Stücke zeichnen.
  - `photo copy -from … -zoom f f` vergrößert beim Kopieren; ein
    vorvergrößertes Vollbild braucht es nicht.
  - Ein direkt gestartetes Skript übersetzt Python bei jedem Start neu (bei
    Glide rund 0,5 s). Als Modul geladen nutzt es den Bytecode-Cache.
- **Tk-Text und Formate beim Tippen:** Eingefügter Text erbt nur die
  Formate, die beide Nachbarzeichen tragen. Zeilenformate schließen deshalb
  den Zeilenumbruch ein, und `spread_line_tags` überträgt sie nach jedem
  Tastendruck auf die ganze Zeile.
  - Eingebettete Fenster (die Kästchen) zählen als ein Index, fehlen aber
    in `get()`.
- **`copy.deepcopy` für Schnappschüsse:** gleich schnell wie
  `zlib`-komprimiertes JSON, aber rund zehnmal so viel Speicher.

## Muster aus der Runde vom 27.09.2026

- **Widgets in eine andere Zeile packen:** Tk kann Widgets nicht umhängen.
  Sollen Knöpfe je nach Breite in Zeile 1 oder 2 stehen, gehören sie dem
  gemeinsamen Elternrahmen und werden mit `pack(in_=zeile)` gesetzt. Da sie
  vor den Zeilen entstanden sein können, hebt `tk.call("raise", w._w)` sie
  darüber – `Canvas.lift` hebt nur Zeichenelemente.
- **Ansichtsleisten nach dem Neuaufbau prüfen:** Mehrere Stellen packen
  Eingabe-, Such- und Knopfzeile wieder ein (Zeichnung, Notiz, Pinnwand,
  Startseite). Die Regel, was eine Ansicht zeigt, läuft deshalb zuletzt
  (`sync_view_chrome` am Ende von `_refresh_tree`). Beim Wiedereinpacken
  richtet sie sich am nächsten sichtbaren Nachbarn im selben Elternrahmen aus –
  `list_frame_outer`, nicht `list_frame`.
- **Neue Kennungen ziehen alle Verweise nach:** Außer `links` und
  `blocked_by` verweisen auch Formatbereiche im Text auf Punkte (`item:<id>`).
  Wer Kennungen neu vergibt, ruft `remap_item_references` und
  `remap_rich_note_items`.
- **Kurze Animationen in Tests:** Die Fahne lebt eine halbe Sekunde. Ein
  langsamer erster Neuaufbau lässt sie schon im nächsten `update()` ablaufen;
  geprüft wird direkt nach dem Auslösen.
- **Hinweise nur einmal anmelden:** `bind(…, add="+")` hängt bei jedem
  Aufruf eine weitere Bindung an. Wer `add_tooltip` bei jeder Aktualisierung
  ruft, bekam früher mehrere Hinweisfenster übereinander. Der Zustand hängt
  deshalb am Widget, ein zweiter Aufruf tauscht nur den Text.
- **Schwebende Fenster erst platzieren, dann zeigen:** Ein `Toplevel`
  erscheint unter macOS sichtbar an seiner ersten Position und wandert beim
  `geometry()` animiert weiter. Deshalb `withdraw()`, positionieren,
  `deiconify()`.
- **Überlagerungen folgen ihrem Ziel:** Eine per `place` über eine
  Baumzeile gelegte Beschriftung bleibt stehen, wenn der Baum seine Höhe
  ändert. Sie wird bei `<Configure>` nachgezogen – aber nur, solange sie
  gerade gezeigt wird.
- **Fensteraufnahmen ohne fremde Fenster:** `screencapture -R` nimmt den
  Bildschirmbereich auf, also auch darüberliegende Fenster anderer
  Programme. `screencapture -l <Fensternummer>` nimmt nur das Fenster auf;
  die Nummer liefert `CGWindowListCopyWindowInfo` (etwa über JXA). Ein
  Fenster mit `-topmost` liegt auf einer anderen Ebene und fällt aus einem
  Filter auf Ebene 0 heraus.
- **Veraltete Objekte in Tests:** Nach Rückgängig sind Listenobjekte neu.
  Referenzen frisch aus `app.lists` holen.
- **`Treeview.see` öffnet Vorfahren** (29.09.2026): Wer nach einem Neuaufbau
  die markierte Zeile mit `see` zeigt, klappt jeden Ordner darüber wieder auf.
  Deshalb ruft die Seitenleiste `reveal_sidebar_row`; es klappt nur für eine
  neu geöffnete Zeile auf.
- **Tk 9 blendet eingebettete Rahmen wieder ein** (29.09.2026): Eine Leinwand
  wird ausgepackt, ihr Rahmen (`create_window`) ist dann ausgeblendet. Ändert
  sich im Rahmen danach etwas, etwa durch Auspacken eines Kinds, blendet Tk
  9.0.3 ihn im nächsten Leerlauf wieder ein. Die Leinwand selbst bleibt
  ausgeblendet. Sichtbar wird davon nichts, aber `winfo_ismapped` meldet 1.
  Nachstellen mit reinem Tk: Leinwand, Rahmen per `create_window`, darin ein
  gepacktes Kind; Leinwand auspacken, Kind auspacken, `update()`.
- **Pack-Reihenfolge entscheidet bei Platzmangel:** Wer zuerst gepackt ist,
  bekommt seine angeforderte Höhe zuerst; `expand` verteilt nur den Rest nach
  Abzug aller späteren Anforderungen. Soll ein unten stehendes Element bei
  kleinem Fenster Vorrang haben (Notiztext unter der Punktliste), packt man
  es mit `side="bottom"` vor das obere.
- **Menübefehle unter Tk 9 auf macOS** (29.09.2026): Der Befehl eines
  Menüeintrags läuft, während das Menü noch verfolgt wird. Ein nativer
  Dateidialog oder ein neues Fenster erscheint dann nicht oder hinter dem
  Hauptfenster. Glide legt deshalb **jeden** Menübefehl auf `after_idle`
  (bis 30.09.2026 nur Einträge mit „…“). Ein modales Fenster, das direkt aus
  dem Menübefehl mit `wait_window` wartet, friert die App ein: macOS schließt
  die Menüverfolgung erst nach der Rückkehr des Befehls ab (Hang-Berichte
  vom 29. und 30.09.2026). Das gilt auch für `::tk::mac::Quit`.
- **Eingebettete Fenster in Leinwänden** (29.09.2026): Ein per
  `create_window` eingebetteter Rahmen wird unter Tk 9 nicht beschnitten und
  kann versetzt erscheinen. Für schwebende Flächen (Suche, Formatleiste)
  einen gewöhnlichen Rahmen mit `place` nehmen; im Textfeld über
  `place_at`, weil der Ursprung dort verschoben ist.
- **Stehengebliebene Bilder nach `pack_forget`** (29.09.2026): macOS malt
  die frei gewordene Fläche nicht immer neu. Die Hintergrundfarbe des
  Elternrahmens neu setzen erzwingt es (`repaint_sidebar`).
- **`<TouchpadScroll>`** (Tk 9, TIP 684): `delta` trägt X in den oberen und
  Y in den unteren 16 Bit, jeweils mit Vorzeichen.
- **Tempo-Untergrenze:** Ein Bild der Oberfläche kostet in reinem Tk auf dem
  Prüfrechner rund 50 ms (Treeview, 85 Zeilen). Messungen immer dagegen
  setzen (`test_tempo330`).
- **Ausblenden im Textfeld:** Ein Format mit `elide=True` (`folded`) blendet
  Zeilen aus, ohne den Text zu ändern. Es darf nie gespeichert werden; nach
  dem Laden stellt `apply_folds` es aus `toggle_closed` her.
