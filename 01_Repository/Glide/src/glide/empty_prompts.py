# SPDX-License-Identifier: MPL-2.0
"""Leerzustände als Handlungsaufforderung (UX-05, 27.11.2026).

Ein leerer Bereich nennt, was man jetzt tun kann, statt nur festzustellen,
dass nichts da ist – nach dem Vorbild „Schreiben oder „/“ für Blöcke“ der
Seiten. Der Text selbst ist die Handlung: Ein Klick führt in genau den einen
Anlegeweg, den der Bereich ohnehin hat (U20: kein zweiter Anlegen-Knopf).

Regeln:
1. Leer ohne Filter → Aufforderung im Imperativ, Klick löst den Anlegeweg aus.
2. Leer durch Filter oder Suche → Grund nennen, Klick setzt den Filter zurück.
3. Schreibgeschützt oder ohne Anlegeweg → Grund nennen, keine Handlung.
4. „…“ nur, wenn danach ein Dialog folgt (wie in Menüs).

Liefert Schlüssel, deutsche Rückfalltexte und Handlungskennungen; was eine
Kennung tut, entscheidet der Aufrufer. Tk-frei, ohne Glide-Abhängigkeit.
"""

from collections import namedtuple

EmptyState = namedtuple("EmptyState", "key fallback action")

FOCUS_ENTRY = "focus_entry"
RESET_FILTER = "reset_filter"
CREATE_PAGE = "create_page"
CREATE_NOTE = "create_note"
CREATE_DRAWING = "create_drawing"
CREATE_NOTEBOOK = "create_notebook"
CREATE_LIST = "create_list"
CREATE_GALLERY = "create_gallery"
CREATE_JOURNAL_ENTRY = "create_journal_entry"
CREATE_AREA = "create_area"
OPEN_GLOBAL_BOARD = "open_global_board"
MANAGE_LABELS = "manage_labels"
IMPORT_TEMPLATES = "import_templates"
ADD_IMAGES = "add_images"
SHOW_ALL_DAYS = "show_all_days"

ACTIONS = frozenset({FOCUS_ENTRY, RESET_FILTER, CREATE_PAGE, CREATE_NOTE, CREATE_DRAWING, CREATE_NOTEBOOK,
                     CREATE_LIST, CREATE_GALLERY, CREATE_JOURNAL_ENTRY, CREATE_AREA, OPEN_GLOBAL_BOARD,
                     MANAGE_LABELS, IMPORT_TEMPLATES, ADD_IMAGES, SHOW_ALL_DAYS})
# Handlungen, nach denen ein Dialog oder Fenster folgt: nur ihre Texte tragen „…“.
DIALOG_ACTIONS = frozenset({CREATE_NOTEBOOK, CREATE_LIST, CREATE_AREA, MANAGE_LABELS, IMPORT_TEMPLATES, ADD_IMAGES})


def list_state(accepts_items=True, filtered=False, read_only=False):
    """Leerzustand einer Aufgaben- oder Notizliste."""
    if filtered:
        return EmptyState("ui.refresh_tree_contents.no_matches_for_the",
                          "Keine Treffer für den aktuellen Filter.", RESET_FILTER)
    if read_only:
        return EmptyState("empty.list.read_only",
                          "Noch keine Punkte – die Daten sind gerade schreibgeschützt.", None)
    if not accepts_items:
        return EmptyState("ui.refresh_tree_contents.no_items_yet", "Noch keine Punkte vorhanden.", None)
    return EmptyState("empty.list.add_first",
                      "Einen neuen Punkt hinzufügen – oben eingeben, Enter legt ihn an.", FOCUS_ENTRY)


OVERVIEWS = {
    "pages": EmptyState("empty.pages.create", "Eine neue Seite anlegen", CREATE_PAGE),
    "notes": EmptyState("empty.notes.create", "Eine neue Notiz schreiben", CREATE_NOTE),
    "drawings": EmptyState("empty.drawings.create", "Eine neue Zeichnung anlegen", CREATE_DRAWING),
    "notebooks": EmptyState("empty.notebooks.create",
                            "Ein Notizbuch für datierte Einträge anlegen …", CREATE_NOTEBOOK),
    # Startseitenkacheln und Bibliothek
    "galleries": EmptyState("empty.galleries.create", "Eine neue Galerie für Bilder anlegen", CREATE_GALLERY),
    "boards": EmptyState("empty.boards.open_global", "Die globale Pinnwand öffnen und erste Karten anlegen",
                         OPEN_GLOBAL_BOARD),
    "labels": EmptyState("empty.labels.manage", "Labels anlegen und verwalten …", MANAGE_LABELS),
    "library": EmptyState("empty.library.create_list", "Eine neue Liste anlegen …", CREATE_LIST),
    "templates": EmptyState("empty.templates.import", "Vorlagen hinzufügen …", IMPORT_TEMPLATES),
    "gallery_images": EmptyState("empty.gallery.add_images",
                                 "Bilder hinzufügen … – sie werden wie Anhänge dieser Galerie gesichert.",
                                 ADD_IMAGES),
}

MENUS = {
    "labels": EmptyState("empty.menu.create_label", "Neues Label anlegen …", MANAGE_LABELS),
    "areas": EmptyState("empty.menu.create_area", "Neuen Bereich anlegen …", CREATE_AREA),
}


def folder_state(kind="folder", searched=False, period_filtered=False, read_only=False):
    """Leerzustand eines Ordners, Notizbuchs (`journal`) oder Buchs (`book`)."""
    if searched:
        return EmptyState("ui.refresh_folder_overview.no_lists_or_content",
                          "Keine Listen oder Inhalte passen zur aktuellen Suche.", RESET_FILTER)
    if kind == "journal" and period_filtered:
        return EmptyState("ui.refresh_folder_overview.there_are_no_entries",
                          "Im gewählten Zeitraum gibt es keine Einträge.", SHOW_ALL_DAYS)
    if read_only:
        return EmptyState("empty.overview.read_only",
                          "Noch nichts angelegt – die Daten sind gerade schreibgeschützt.", None)
    if kind == "journal":
        # Die Eingabezeile legt dort nur eine gewöhnliche Liste an; der Eintrag hat seinen eigenen Weg.
        return EmptyState("empty.journal.first_entry", "Den ersten Eintrag dieses Notizbuchs anlegen",
                          CREATE_JOURNAL_ENTRY)
    if kind == "book":
        return EmptyState("empty.book.add_page", "Eine neue Seite anlegen – oben eingeben, Enter legt sie an.",
                          FOCUS_ENTRY)
    return EmptyState("empty.folder.add_list", "Eine neue Liste anlegen – oben eingeben, Enter legt sie an.",
                      FOCUS_ENTRY)


def menu_state(kind):
    """Eintrag für ein leeres Untermenü; None für unbekannte Arten."""
    return MENUS.get(kind)


def overview_state(kind, read_only=False):
    """Leerzustand des Abschnitts „Alle …“ einer Übersicht; None für unbekannte Arten."""
    state = OVERVIEWS.get(kind)
    if state is None:
        return None
    if read_only:
        return EmptyState("empty.overview.read_only", "Noch nichts angelegt – die Daten sind gerade schreibgeschützt.", None)
    return state
