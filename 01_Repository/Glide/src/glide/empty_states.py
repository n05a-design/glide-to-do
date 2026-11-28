# SPDX-License-Identifier: MPL-2.0
"""Kontextuelle Leerzustände (WA-52, Glide 1.1.0) – Tk-frei nach D17.

Ein Leerzustand nennt, wo man ist (Titel), was hier entsteht (ein Satz) und
den nächsten Schritt: eine Hauptaktion, höchstens eine zweite. Dieses Modul
entscheidet nur Inhalt und Aktionskennungen; die Oberfläche ordnet den
Kennungen ihre vorhandenen Befehle zu. Grenzen aus den Produktentscheidungen:

* U20: Mehrere Zugänge dürfen dieselbe Erstellungsoperation auslösen.
  Direkt editierbare Zeilen ersetzen den Leertext, wo ein eindeutiges Ziel vorliegt.
* N06 (25./27.09.2026): kein Einstieg für neue Nutzer, kein Rundgang, kein
  Pflichtdialog. Leerzustände erscheinen nur, wo tatsächlich nichts ist, und
  verschwinden mit dem ersten Inhalt.
* B06: Mit ausgeschalteten Bedienhinweisen entfällt nur der reine
  Bedienhinweis (etwa „Datum und Labels erkennt Glide im Text“); Titel,
  Erklärung und Aktionen bleiben, denn sie beschreiben den Zustand.
"""
from collections import namedtuple
from dataclasses import dataclass

import i18n as glide_i18n

# Aktionskennungen, die die Oberfläche auf vorhandene Befehle abbildet.
ACTIONS = (
    "home_setup",          # Startseite einrichten (Kachelauswahl)
    "home_restore",        # Standardkacheln wiederherstellen
    "use_template",        # Vorlagenübersicht öffnen
    "plan_day",            # Tagesvorschlag / Arbeitstag planen
    "open_inbox",          # Eingang öffnen (dort entsteht die erste Aufgabe)
    "new_page",            # neue Seite anlegen
    "pin_items",           # Elemente zur Pinnwand hinzufügen
    "clear_filter",        # Filter oder Suche zurücksetzen
    "new_journal_entry",   # ersten Notizbucheintrag anlegen
    "show_all_days",       # Zeitraumfilter des Notizbuchs aufheben
)

CONTEXTS = ("home", "today", "pages", "pinboard", "journal")


@dataclass(frozen=True, slots=True)
class EmptyState:
    """Inhalt eines Leerzustands. Aktionen sind (Kennung, Beschriftung) oder None."""

    context: str
    title: str
    description: str
    primary: tuple[str, str] | None = None
    secondary: tuple[str, str] | None = None

    @property
    def text(self) -> str:
        """Titel und Erklärung als zweizeiliger Text für einzeilige Flächen (Baumzeile)."""
        return f"{self.title}\n{self.description}" if self.description else self.title

    @property
    def action_ids(self) -> tuple[str, ...]:
        return tuple(action[0] for action in (self.primary, self.secondary) if action)


def _t(key, default, **values):
    return glide_i18n.t(f"mod.empty_states.{key}", default, **values)


def _action(action_id):
    labels = {
        "home_setup": ("home_setup", "Startseite einrichten …"),
        "home_restore": ("home_restore", "Standardkacheln zeigen"),
        "use_template": ("use_template", "Vorlage verwenden"),
        "plan_day": ("plan_day", "Arbeitstag planen …"),
        "open_inbox": ("open_inbox", "Erste Aufgabe anlegen"),
        "new_page": ("new_page", "Erste Seite erstellen"),
        "pin_items": ("pin_items", "Element hinzufügen"),
        "clear_filter": ("clear_filter", "Filter aufheben"),
        "new_journal_entry": ("new_journal_entry", "Ersten Eintrag anlegen"),
        "show_all_days": ("show_all_days", "Alle Tage zeigen"),
    }
    key, default = labels[action_id]
    return action_id, _t(f"action.{key}", default)


def empty_state(context, *, filtered=False, other_day=False, has_cards=False,
                date_range=False, hints=True, has_tasks=True):
    """Leerzustand für ``context`` (siehe ``CONTEXTS``) oder ``None``.

    ``filtered``: Suche/Filter blendet vorhandene Inhalte aus – dann ist
    Zurücksetzen der nächste Schritt. Bei einem anderen Tag gelten dessen
    geplante Aufgaben. Eine Pinnwand kann Karten außerhalb des Filters haben.
    ``date_range``: das Notizbuch ist auf einen Zeitraum eingeschränkt.
    ``has_tasks``: es gibt überhaupt offene Aufgaben (für „Arbeitstag planen“).
    ``hints``: Bedienhinweise an (B06); aus, entfällt nur der reine Bedienhinweis.
    """
    if context not in CONTEXTS:
        raise ValueError(f"unknown empty-state context {context!r}")
    if context == "home":
        state = EmptyState(context, _t("home.title", "Alle Kacheln sind ausgeblendet"),
                           _t("home.description", "Wähle aus, was die Startseite zeigen soll – Aufgaben, Kalender, Seiten oder Pinnwände."),
                           _action("home_setup"), _action("home_restore"))
    elif context == "today":
        if filtered:
            state = EmptyState(context, _t("today.filtered_title", "Nichts passt zum Filter"),
                               _t("today.filtered_description", "Für diesen Tag sind Aufgaben eingeplant, der Filter blendet sie aus."),
                               _action("clear_filter"))
        elif other_day:
            state = EmptyState(context, _t("today.other_day_title", "An diesem Tag ist nichts eingeplant"),
                               _t("today.other_day_description", "Plane Aufgaben über ihr Menü auf diesen Tag oder lass dir einen Vorschlag machen."),
                               _action("plan_day") if has_tasks else _action("open_inbox"))
        else:
            state = EmptyState(context, _t("today.title", "Heute ist noch nichts eingeplant"),
                               _t("today.description", "Wähle aus deinen offenen Aufgaben, was heute dran ist – Fristen bleiben dabei unverändert."),
                               _action("plan_day") if has_tasks else _action("open_inbox"))
    elif context == "pages":
        state = EmptyState(context, _t("pages.title", "Noch keine Seiten"),
                           _t("pages.description", "Seiten halten Projekte, Notizen und Aufgaben zusammen. Beginne leer oder mit einer Vorlage."),
                           _action("new_page"), _action("use_template"))
    elif context == "pinboard":
        if has_cards:
            state = EmptyState(context, _t("pinboard.filtered_title", "Keine Karten für diesen Filter"),
                               _t("pinboard.filtered_description", "Die Pinnwand hat Karten, der Filter blendet sie aus."),
                               _action("clear_filter"))
        else:
            state = EmptyState(context, _t("pinboard.title", "Die Pinnwand ist leer"),
                               _t("pinboard.description", "Hefte vorhandene Aufgaben, Seiten oder Zeichnungen an oder klicke doppelt auf die Fläche für eine neue Karte."),
                               _action("pin_items"))
    else:  # journal
        if date_range:
            state = EmptyState(context, _t("journal.range_title", "Keine Einträge in diesem Zeitraum"),
                               _t("journal.range_description", "Ältere oder spätere Einträge erscheinen, wenn der Zeitraum aufgehoben wird."),
                               _action("show_all_days"))
        elif filtered:
            state = EmptyState(context, _t("journal.filtered_title", "Keine Treffer"),
                               _t("journal.filtered_description", "Das Notizbuch hat Einträge, die Suche blendet sie aus."),
                               _action("clear_filter"))
        else:
            state = EmptyState(context, _t("journal.title", "Das Notizbuch ist noch leer"),
                               _t("journal.description", "Ein Eintrag trägt seinen Tag, Stimmung und Ort. Schreib den ersten für heute."),
                               _action("new_journal_entry"))
    return state


EmptyPrompt = namedtuple("EmptyPrompt", "key fallback action")

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

PROMPT_ACTIONS = frozenset({FOCUS_ENTRY, RESET_FILTER, CREATE_PAGE, CREATE_NOTE, CREATE_DRAWING, CREATE_NOTEBOOK,
                     CREATE_LIST, CREATE_GALLERY, CREATE_JOURNAL_ENTRY, CREATE_AREA, OPEN_GLOBAL_BOARD,
                     MANAGE_LABELS, IMPORT_TEMPLATES, ADD_IMAGES, SHOW_ALL_DAYS})
# Handlungen, nach denen ein Dialog oder Fenster folgt: nur ihre Texte tragen „…“.
DIALOG_ACTIONS = frozenset({CREATE_NOTEBOOK, CREATE_LIST, CREATE_AREA, MANAGE_LABELS, IMPORT_TEMPLATES, ADD_IMAGES})


def list_state(accepts_items=True, filtered=False, read_only=False):
    """Leerzustand einer Aufgaben- oder Notizliste."""
    if filtered:
        return EmptyPrompt("ui.refresh_tree_contents.no_matches_for_the",
                          "Keine Treffer für den aktuellen Filter.", RESET_FILTER)
    if read_only:
        return EmptyPrompt("empty.list.read_only",
                          "Noch keine Punkte – die Daten sind gerade schreibgeschützt.", None)
    if not accepts_items:
        return EmptyPrompt("ui.refresh_tree_contents.no_items_yet", "Noch keine Punkte vorhanden.", None)
    return None


OVERVIEWS = {
    "pages": EmptyPrompt("empty.pages.create", "Eine neue Seite anlegen", CREATE_PAGE),
    "notes": EmptyPrompt("empty.notes.create", "Eine neue Notiz schreiben", CREATE_NOTE),
    "drawings": EmptyPrompt("empty.drawings.create", "Eine neue Zeichnung anlegen", CREATE_DRAWING),
    "notebooks": EmptyPrompt("empty.notebooks.create",
                            "Ein Notizbuch für datierte Einträge anlegen …", CREATE_NOTEBOOK),
    # Startseitenkacheln und Bibliothek
    "galleries": EmptyPrompt("empty.galleries.create", "Eine neue Galerie für Bilder anlegen", CREATE_GALLERY),
    "boards": EmptyPrompt("empty.boards.open_global", "Die globale Pinnwand öffnen und erste Karten anlegen",
                         OPEN_GLOBAL_BOARD),
    "labels": EmptyPrompt("empty.labels.manage", "Labels anlegen und verwalten …", MANAGE_LABELS),
    "library": EmptyPrompt("empty.library.create_list", "Eine neue Liste anlegen …", CREATE_LIST),
    "templates": EmptyPrompt("empty.templates.import", "Vorlagen hinzufügen …", IMPORT_TEMPLATES),
    "gallery_images": EmptyPrompt("empty.gallery.add_images",
                                 "Bilder hinzufügen … – sie werden wie Anhänge dieser Galerie gesichert.",
                                 ADD_IMAGES),
}

MENUS = {
    "labels": EmptyPrompt("empty.menu.create_label", "Neues Label anlegen …", MANAGE_LABELS),
    "areas": EmptyPrompt("empty.menu.create_area", "Neuen Bereich anlegen …", CREATE_AREA),
}


def folder_state(kind="folder", searched=False, period_filtered=False, read_only=False):
    """Leerzustand eines Ordners, Notizbuchs (`journal`) oder Buchs (`book`)."""
    if searched:
        return EmptyPrompt("ui.refresh_folder_overview.no_lists_or_content",
                          "Keine Listen oder Inhalte passen zur aktuellen Suche.", RESET_FILTER)
    if kind == "journal" and period_filtered:
        return EmptyPrompt("ui.refresh_folder_overview.there_are_no_entries",
                          "Im gewählten Zeitraum gibt es keine Einträge.", SHOW_ALL_DAYS)
    if read_only:
        return EmptyPrompt("empty.overview.read_only",
                          "Noch nichts angelegt – die Daten sind gerade schreibgeschützt.", None)
    if kind == "journal":
        # Die Eingabezeile legt dort nur eine gewöhnliche Liste an; der Eintrag hat seinen eigenen Weg.
        return EmptyPrompt("empty.journal.first_entry", "Den ersten Eintrag dieses Notizbuchs anlegen",
                          CREATE_JOURNAL_ENTRY)
    if kind == "book":
        return EmptyPrompt("empty.book.add_page", "Eine neue Seite anlegen – oben eingeben, Enter legt sie an.",
                          FOCUS_ENTRY)
    return EmptyPrompt("empty.folder.add_list", "Eine neue Liste anlegen – oben eingeben, Enter legt sie an.",
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
        return EmptyPrompt("empty.overview.read_only", "Noch nichts angelegt – die Daten sind gerade schreibgeschützt.", None)
    return state
