# SPDX-License-Identifier: MPL-2.0
"""Kontextuelle Leerzustände (WA-52, Glide 1.1.0) – Tk-frei nach D17.

Ein Leerzustand nennt, wo man ist (Titel), was hier entsteht (ein Satz) und
den nächsten Schritt: eine Hauptaktion, höchstens eine zweite. Dieses Modul
entscheidet nur Inhalt und Aktionskennungen; die Oberfläche ordnet den
Kennungen ihre vorhandenen Befehle zu. Grenzen aus den Produktentscheidungen:

* U20 (3.33.20): Steht eine Eingabezeile sichtbar darüber, ist sie der eine
  Anlegeweg – der Leerzustand verweist auf sie statt einen zweiten
  Anlegeknopf zu zeigen.
* N06 (25./27.09.2026): kein Einstieg für neue Nutzer, kein Rundgang, kein
  Pflichtdialog. Leerzustände erscheinen nur, wo tatsächlich nichts ist, und
  verschwinden mit dem ersten Inhalt.
* B06: Erklärende Sätze dürfen mit ausgeschalteten Bedienhinweisen kürzer
  werden; Titel und Aktionen bleiben.
"""
from dataclasses import dataclass

import i18n as glide_i18n

# Aktionskennungen, die die Oberfläche auf vorhandene Befehle abbildet.
ACTIONS = (
    "home_setup",          # Startseite einrichten (Kachelauswahl)
    "home_restore",        # Standardkacheln wiederherstellen
    "focus_entry",         # Eingabezeile der Liste fokussieren
    "use_template",        # Vorlagenübersicht öffnen
    "plan_day",            # Tagesvorschlag / Arbeitstag planen
    "open_inbox",          # Eingang öffnen (dort entsteht die erste Aufgabe)
    "new_page",            # neue Seite anlegen
    "pin_items",           # Elemente zur Pinnwand hinzufügen
    "clear_filter",        # Filter oder Suche zurücksetzen
    "new_journal_entry",   # ersten Notizbucheintrag anlegen
    "show_all_days",       # Zeitraumfilter des Notizbuchs aufheben
)

CONTEXTS = ("home", "list", "today", "pages", "pinboard", "journal")


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
        "home_restore": ("home_restore", "Standard wiederherstellen"),
        "use_template": ("use_template", "Vorlage verwenden"),
        "plan_day": ("plan_day", "Arbeitstag planen …"),
        "open_inbox": ("open_inbox", "Erste Aufgabe anlegen"),
        "new_page": ("new_page", "Erste Seite erstellen"),
        "pin_items": ("pin_items", "Element hinzufügen"),
        "clear_filter": ("clear_filter", "Filter aufheben"),
        "new_journal_entry": ("new_journal_entry", "Ersten Eintrag anlegen"),
        "show_all_days": ("show_all_days", "Alle Tage zeigen"),
        "focus_entry": ("focus_entry", "Erste Aufgabe anlegen"),
    }
    key, default = labels[action_id]
    return action_id, _t(f"action.{key}", default)


def empty_state(context, *, filtered=False, entry_visible=False, other_day=False, has_cards=False,
                date_range=False, hints=True, has_tasks=True):
    """Leerzustand für ``context`` (siehe ``CONTEXTS``) oder ``None``.

    ``filtered``: Suche/Filter blendet vorhandene Inhalte aus – dann ist
    Zurücksetzen der nächste Schritt, nicht Anlegen. ``entry_visible``: eine
    Eingabezeile steht darüber (U20). ``other_day``: Heute zeigt einen
    anderen Tag. ``has_cards``: die Pinnwand hat Karten, nur keine im Filter.
    ``date_range``: das Notizbuch ist auf einen Zeitraum eingeschränkt.
    ``has_tasks``: es gibt überhaupt offene Aufgaben (für „Arbeitstag planen“).
    ``hints``: Bedienhinweise an (B06); aus, entfällt der erklärende Zusatz.
    """
    if context not in CONTEXTS:
        raise ValueError(f"unknown empty-state context {context!r}")
    if context == "home":
        state = EmptyState(context, _t("home.title", "Alle Kacheln sind ausgeblendet"),
                           _t("home.description", "Wähle aus, was die Startseite zeigen soll – Aufgaben, Kalender, Seiten oder Pinnwände."),
                           _action("home_setup"), _action("home_restore"))
    elif context == "list":
        if filtered:
            state = EmptyState(context, _t("list.filtered_title", "Keine Treffer"),
                               _t("list.filtered_description", "Die Liste hat Inhalte, die Suche oder der Filter blendet sie aus."),
                               _action("clear_filter"))
        elif entry_visible:
            state = EmptyState(context, _t("list.title", "Diese Liste ist noch leer"),
                               _t("list.entry_description", "Schreib oben die erste Aufgabe und drück Enter. Datum und Labels erkennt Glide im Text."),
                               None, _action("use_template"))
        else:
            state = EmptyState(context, _t("list.title", "Diese Liste ist noch leer"),
                               _t("list.description", "Hier entstehen Aufgaben, Notizen und Unterpunkte."),
                               _action("focus_entry"), _action("use_template"))
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
    if not hints and state.description:
        state = EmptyState(state.context, state.title, "", state.primary, state.secondary)
    return state
