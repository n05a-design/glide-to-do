"""Ergebnisvertrag der Editorübernahme ohne Tk (WA-29, Befund A35).

`ListApp.flush_rich_note` übernimmt vor Navigation, Export und Ende den
offenen Notiz- oder Seiteneditor und die offene Zeichnung in den Bestand. Bis
18.10.2026 lieferte sie immer None. Die Aufrufer, die mit `is False` abbrechen
wollten – Seitenfunktionen, Vorlagen, Markdown, Notion, Wiederherstellen –,
liefen deshalb auch dann weiter, wenn ein Editor nicht übernommen hatte.

Vertrag:

- `combine` fasst die Rückgaben beider Editoren zusammen: False, sobald einer
  scheitert; None (nichts offen, ältere Rückgabe) zählt als Erfolg.
- `switch_allowed` entscheidet vor einem Kontextwechsel, ob der Editor
  abgebaut werden darf. Nein nur, wenn er Inhalt hält, den der Bestand nicht
  übernommen hat – etwa eine Notiz über der Größengrenze. Ein Schreibfehler
  darf den Wechsel nur bei nachweislich übernommenem Editorinhalt erlauben;
  `dirty` allein beweist das nicht. Autospeichern und Beenden
  fragen nach; ein schreibgeschützter Bestand speichert ohnehin nichts; und
  ein Editor, dessen Seite nicht mehr zum geladenen Bestand gehört, hat
  nichts mehr zu bewahren.
"""

NOT_ADOPTED = ("Nicht übernommen",
               "Die geöffnete Notiz oder Zeichnung ließ sich nicht übernehmen; der Hinweis im Editor "
               "nennt den Grund. Glide bleibt hier, damit nichts verloren geht.")


def combine(*results):
    """True, wenn kein Editor einen Fehlschlag meldet."""
    return not any(result is False for result in results)


def switch_allowed(flushed, *, read_only, adopted, editor_in_dataset):
    """Darf ein Kontextwechsel den offenen Editor abbauen?

    `editor_in_dataset` darf ein Aufruf sein; er wird nur ausgewertet, wenn
    die Übernahme scheiterte.
    """
    if flushed is not False or read_only:
        return True
    belongs = editor_in_dataset() if callable(editor_in_dataset) else editor_in_dataset
    if not belongs:
        return True
    return bool(adopted() if callable(adopted) else adopted)
