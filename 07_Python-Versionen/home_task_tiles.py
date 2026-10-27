"""Heute-/Nächste-Aufgabe-Kacheln über explizite Daten und UI-Operationen.

Kein Zugriff auf ListApp, Tk oder persistente Daten. Der Host liefert die
bestehenden Karten-/Text-/Aktionsbausteine und verwaltet ihre Lebensdauer.
Callbacks halten nur IDs und die jeweilige vorhandene Aktion.
"""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True, slots=True)
class TaskLink:
    title: str
    list_id: str
    item_id: str
    color: str
    selected: bool = False


@dataclass(frozen=True, slots=True)
class TodayContent:
    planned_total: int
    open_total: int
    planning: str
    tasks: tuple
    next_task: TaskLink | None
    show_goal: bool
    inbox_total: int
    due_lists: tuple
    writable: bool
    selecting: bool = False
    selected_total: int = 0
    available_total: int = 0
    page: int = 0
    pages: int = 1


@dataclass(frozen=True, slots=True)
class FocusContent:
    task: TaskLink | None
    details: str = ''
    writable: bool = True


@dataclass(frozen=True, slots=True)
class TileUI:
    card: Callable
    label: Callable
    action: Callable
    flow: Callable
    goal: Callable
    task_row: Callable


@dataclass(frozen=True, slots=True)
class TileCommands:
    open_task: Callable
    complete: Callable
    open_list: Callable
    today: Callable
    upcoming: Callable
    next_task: Callable
    focus: Callable | None = None
    plan: Callable | None = None
    proposal: Callable | None = None
    selection_start: Callable | None = None
    selection_toggle: Callable | None = None
    selection_all: Callable | None = None
    selection_clear: Callable | None = None
    selection_plan: Callable | None = None
    selection_end: Callable | None = None
    selection_page: Callable | None = None


def planning_selection(entries, selected=(), page=0, page_size=10):
    """Offene Tageszeilen und stabile Auswahl über Seiten, ohne Mutation.

    Der Aufrufer liefert den aktuellen Tag ohne Archivlisten. Die Projektion
    verwirft inzwischen erledigte/fehlende IDs und zählt jede ID einmal.
    """
    rows, seen = [], set()
    for entry in entries:
        item = entry[-1]
        identity = item.get('id')
        if not isinstance(identity, str) or not identity or identity in seen or item.get('done'):
            continue
        seen.add(identity)
        rows.append(entry)
    available = tuple(entry[-1]['id'] for entry in rows)
    selected = set(selected)
    chosen = tuple(identity for identity in available if identity in selected)
    page_size = max(1, page_size)
    pages = max(1, (len(rows) + page_size - 1) // page_size)
    page = max(0, min(page, pages - 1))
    return dict(rows=tuple(rows[page * page_size:(page + 1) * page_size]),
                available=available, selected=chosen, page=page, pages=pages)


@dataclass(frozen=True, slots=True)
class HomeTaskTiles:
    ui: TileUI
    commands: TileCommands
    icons: dict
    spacing: tuple

    def open_link(self, parent, task):
        # Keine Callbackbindung an diese kurzlebige Rendererinstanz: Die
        # Retention kann die eigentlichen Aktionen anhand Funktion/IDs abgleichen.
        open_task = self.commands.open_task
        return self.ui.action(parent, task.title,
                              lambda lid=task.list_id, iid=task.item_id: open_task(lid, iid), task.color)

    def render_today(self, parent, content):
        ui = self.ui
        tile = ui.card(parent, f"{self.icons['today']}  Heute")
        if content.show_goal:
            ui.goal(tile)
        if content.next_task is not None:
            ui.label(tile, 'Als Nächstes', 10, True, 'muted', pady=(self.spacing[0], self.spacing[3]))
            self.open_link(tile, content.next_task)
        ui.label(tile, 'Eingeplant', 10, True, 'muted',
                 pady=(self.spacing[10] if content.next_task else self.spacing[0], self.spacing[3]))
        self.render_planned(tile, content)
        ui.label(tile, 'Heute fällig', 10, True, 'muted', pady=(self.spacing[10], self.spacing[3]))
        self.render_due(tile, content.due_lists)
        ui.action(tile, f"{self.icons['today']}  Heute öffnen", self.commands.today, 'accent')
        if content.writable and self.commands.proposal is not None:
            ui.action(tile, 'Was passt heute?', self.commands.proposal, 'muted')
        return tile

    def render_planned(self, tile, content):
        ui = self.ui
        if content.planned_total or content.selecting:
            ui.label(tile, f'{content.planned_total} eingeplant · {content.open_total} offen'
                     + (f'\n{content.planning}' if content.planning else ''), color='muted')
            if content.tasks and not content.writable:
                ui.label(tile, 'Schreibgeschützt · Aufgaben lassen sich öffnen.', color='muted')
            if content.selecting:
                ui.label(tile, 'Auswahlmodus · Kästchen wählen Aufgaben, ohne sie zu erledigen.', color='muted')
                ui.label(tile, f'{content.selected_total} ausgewählt · {content.available_total} offene Tagesaufgaben',
                         color='muted')
                controls = ui.flow(tile, pady=(self.spacing[0], self.spacing[4]))
                for title, command in (('Alle auswählen', self.commands.selection_all),
                                       ('Auswahl leeren', self.commands.selection_clear),
                                       ('Auswahl planen …', self.commands.selection_plan if content.selected_total else None),
                                       ('Auswahl beenden', self.commands.selection_end)):
                    if command is not None:
                        ui.action(controls, title, command, 'muted', side='left')
            open_task = self.commands.open_task
            complete = self.commands.selection_toggle if content.selecting else self.commands.complete
            for task in content.tasks:
                ui.task_row(tile, task,
                            lambda lid=task.list_id, iid=task.item_id: open_task(lid, iid),
                            (lambda iid=task.item_id: complete(iid)) if content.writable and complete else None)
            if content.selecting and content.pages > 1:
                ui.label(tile, f'Seite {content.page + 1} von {content.pages}', color='muted')
                controls = ui.flow(tile, pady=(self.spacing[0], self.spacing[4]))
                turn = self.commands.selection_page
                for title, step in (('Vorige Seite', -1), ('Weitere Seite', 1)):
                    if turn is not None:
                        ui.action(controls, title, lambda value=step: turn(value), 'muted', side='left')
            if content.writable and content.tasks and not content.selecting and self.commands.selection_start:
                ui.action(tile, 'Mehrere auswählen …', self.commands.selection_start, 'muted')
        else:
            ui.label(tile, 'Für heute ist noch nichts eingeplant.', color='muted')
        if content.inbox_total:
            ui.label(tile, f'{content.inbox_total} Aufgabe(n) liegen ohne Tag im Eingang.', color='muted')

    def render_due(self, tile, due_lists):
        open_list = self.commands.open_list
        for title, identity, color in due_lists:
            self.ui.action(tile, title, lambda lid=identity: open_list(lid), color)
        if not due_lists:
            self.ui.label(tile, 'Für heute sind keine offenen Aufgaben fällig.', color='muted')

    def render_focus(self, parent, content):
        ui = self.ui
        tile = ui.card(parent, f"{self.icons['next']}  Nächste Aufgabe")
        task = content.task
        if task is None:
            ui.label(tile, 'Nichts steht an. Ein guter Moment, um zu planen oder Feierabend zu machen.', color='muted')
            ui.action(tile, f"{self.icons['in_progress']}  Demnächst öffnen", self.commands.upcoming, 'due_action')
            return tile
        ui.label(tile, task.title, 12, True)
        ui.label(tile, content.details, color='muted')
        if not content.writable:
            ui.label(tile, 'Schreibgeschützt · Aufgaben lassen sich öffnen.', color='muted')
        row = ui.flow(tile, pady=(self.spacing[4], self.spacing[0]))
        open_task, complete = self.commands.open_task, self.commands.complete
        ui.action(row, 'Öffnen', lambda lid=task.list_id, iid=task.item_id: open_task(lid, iid), task.color, side='left')
        if content.writable:
            ui.action(row, f"{self.icons['check']}  Erledigt", lambda iid=task.item_id: complete(iid), 'confirm', side='left')
            focus, plan = self.commands.focus, self.commands.plan
            if focus is not None:
                ui.action(row, 'Fokus starten', lambda iid=task.item_id: focus(iid), 'due_action', side='left')
            if plan is not None:
                ui.action(row, 'Einplanen …', lambda iid=task.item_id: plan(iid), 'muted', side='left')
        ui.action(row, f"{self.icons['next']}  Im Abschnitt zeigen", self.commands.next_task, 'due_action', side='left')
        return tile
