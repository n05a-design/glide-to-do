# SPDX-License-Identifier: MPL-2.0
"""Deutsche Aufgabenwerte und Tk-9.1-Attribute ohne Import einer Tk-Laufzeit.

Gesetzte Attribute sind kein Nachweis tatsächlicher Screenreader-Bedienung.
Die UI setzt sie nach dem Mapping erneut, weil Tk Klassenbindungen ausführt.
"""
from dataclasses import dataclass
from datetime import date
import i18n as glide_i18n

ROLES = frozenset(("Button", "Canvas", "Checkbutton", "Combobox", "Entry", "Label",
                   "Listbox", "Menu", "Notebook", "Progressbar", "Scale", "Scrollbar",
                   "Spinbox", "Table", "Text", "Tree"))


def plain(value):
    return " ".join(str(value or "").split())


def day(value):
    if not value:
        return ""
    try:
        return date.fromisoformat(value).strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        raise ValueError("Ungültiger Tag im zugänglichen Aufgabenwert.") from None


def task_value(item, *, label_names=(), blocked_titles=()):
    """Fälligkeit und Bearbeitungstag getrennt benennen; keine IDs vorlesen."""
    parts = [plain(item.get("text")) or glide_i18n.t("ui.page_card_blocks.untitled", "Ohne Titel")]
    kind = item.get("kind", "task")
    if kind in ("group", "heading"):
        parts.append(glide_i18n.t("inspector.kind.group", "Gruppe") if kind == "group" else glide_i18n.t("ui.apply_sidebar_rename.heading", "Überschrift"))
    else:
        parts.append(glide_i18n.t("inspector.done", "Erledigt") if item.get("done") else glide_i18n.t("ui.refresh.open", "Offen"))
        if kind == "long":
            parts.append(glide_i18n.t("inspector.kind.long", "Langtext"))
        planned, due = day(item.get("planned_date")), day(item.get("due"))
        for title, value, time_key, empty in ((glide_i18n.t("calendar.title.planned", "Bearbeitungstag"), planned, "planned_time", glide_i18n.t("mod.accessibility.task_value.not_planned", "Nicht eingeplant")),
                                              (glide_i18n.t("ui.create_ui.due", "Fällig"), due, "due_time", glide_i18n.t("saved_view.choice.due_none", "Ohne Fälligkeit"))):
            time = plain(item.get(time_key))
            parts.append(title + " " + value + (" um " + time if time else "") if value else empty)
        importance = item.get("importance", 0)
        if type(importance) is not int or not 0 <= importance <= 3:
            raise ValueError("Ungültige Wichtigkeit im zugänglichen Aufgabenwert.")
        parts.append(glide_i18n.t("saved_view.choice.importance_none", "Keine Wichtigkeit") if importance == 0 else
                     glide_i18n.t("mod.accessibility.task_value.importance", 'Wichtigkeit {wert}', wert=("", "niedrig", "mittel", "hoch")[importance]))
        minutes = item.get("estimated_minutes")
        if minutes is not None and (type(minutes) is not int or minutes < 0):
            raise ValueError("Ungültiger Aufwand im zugänglichen Aufgabenwert.")
        parts.append(glide_i18n.t("mod.accessibility.task_value.effort_not_estimated", "Aufwand nicht geschätzt") if minutes is None else glide_i18n.t("mod.accessibility.task_value.effort_minutes", 'Aufwand {minutes} Minuten', minutes=minutes))
        if item.get("repeat"):
            parts.append(glide_i18n.t("mod.accessibility.task_value.recurring", "Wiederkehrend"))
        if item.get("reminder"):
            parts.append(glide_i18n.t("mod.accessibility.task_value.reminder_set", "Erinnerung gesetzt"))
        blockers = [plain(value) for value in blocked_titles if plain(value)]
        if blockers:
            parts.append(glide_i18n.t("mod.accessibility.task_value.waits_for", 'Wartet auf {join}', join=", ".join(blockers)))
    labels = [plain(value) for value in label_names if plain(value)]
    if labels:
        parts.append(glide_i18n.t("mod.accessibility.task_value.labels", 'Labels {join}', join=", ".join(labels)))
    children = item.get("children") or ()
    if children:
        parts.append(glide_i18n.t("mod.accessibility.task_value.subitem_s", '{len} Unterpunkt(e)', len=len(children)))
    return ". ".join(parts) + "."


@dataclass(frozen=True, slots=True)
class Attributes:
    role: str
    name: str
    description: str = ""
    value: str = ""
    state: str = "normal"
    action: tuple = ()
    help: str = ""

    def __post_init__(self):
        if self.role not in ROLES or not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Rolle und zugänglicher Name müssen bekannt und benannt sein.")
        if self.role == "Checkbutton" and self.value not in ("0", "1"):
            raise ValueError("Der native Checkboxzustand muss 0 oder 1 sein.")
        if any(not isinstance(getattr(self, key), str) for key in ("description", "value", "state", "help")):
            raise ValueError("Zugängliche Werte müssen Text sein.")
        if not isinstance(self.action, tuple) or any(not isinstance(value, str) for value in self.action):
            raise ValueError("Die Bedienaktion muss eine Tcl-Argumentliste sein.")


def set_attributes(call, window, attributes):
    """Direkte native Kommandos vermeiden das inaktive Tcl-Ensemble ohne Reader.

    Tk legt die Attributtabelle erst mit der Rolle an. Keine Tcl-Skripte aus
    Aufgabentexten bilden; eine Aktion bleibt ein einzelnes Listenargument.
    """
    if not isinstance(attributes, Attributes):
        raise TypeError("Zugänglichkeitsattribute fehlen.")
    role = attributes.role
    system = call("tk", "windowingsystem")
    # Tk 9.1 verwendet unter X11 in seiner ATK-Tabelle den Namen Checkbox;
    # Aqua und Windows verwenden Checkbutton. Die Fachrolle bleibt einheitlich.
    if role == "Checkbutton" and system == "x11":
        role = "Checkbox"
    description = attributes.description
    # Aqua leitet den Titel einer Schaltfläche aus accessibilityLabel ab,
    # das in Tk 9.1 den Beschreibungseintrag statt des Namens ausliest.
    if attributes.role == "Button" and system == "aqua":
        description = attributes.name + (". " + description if description else "")
    for key in ("role", "name", "description", "value", "state", "action", "help"):
        value = role if key == "role" else description if key == "description" else getattr(attributes, key)
        call("::tk::accessible::set_acc_" + key, str(window), value)


def screenreader_active(call):
    # Das öffentliche Ensemble kann ohne Reader alle Unterbefehle mit 0
    # beantworten. Der native Prüfaufruf bleibt der maßgebliche Status.
    # Ein ohne ATK gebautes Tk 9.1 liefert einmal eine Warnung, danach leer.
    # Ausschließlich der native boolesche Wert 1 meldet einen aktiven Reader.
    return call("::tk::accessible::check_screenreader") in (1, "1")
