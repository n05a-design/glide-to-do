"""Ein Speicherablauf mit expliziter Commitgrenze, ohne Tk oder Appzustand.

Der Adapter liefert die vorhandenen Operationen; nur dieser Koordinator
bestimmt ihre Reihenfolge und unterscheidet Schreib- von Folgefehlern.
Er erzeugt weder einen zweiten Schreibweg noch einen Undo-Schritt.
"""
from dataclasses import dataclass
from typing import Callable, Iterable

from save_result import SaveResult


@dataclass(frozen=True, slots=True)
class PersistencePlan:
    prepare: Callable[[], object]
    backup: Callable[[], str | None]
    write: Callable[[], None]
    accept: Callable[[object], None]
    reject: Callable[[], None]
    followups: Callable[[object], Iterable[tuple[str, Callable[[], None]]]]
    settings: Callable[[], tuple[bool, bool | None]]


class PersistenceCoordinator:
    """Nach bestandener Besitz-/Wächterprüfung genau einmal atomar schreiben."""

    @staticmethod
    def save(plan):
        backup_warning = None
        backup_checked = False
        try:
            comparison = plan.prepare()
            backup_warning = plan.backup()
            backup_checked = True
            plan.write()
        except Exception as exc:
            plan.reject()
            return SaveResult(lock_verified=True, backup_checked=backup_checked,
                              backup_warning=backup_warning, error=str(exc))

        # Ab hier kann auch ein fehlerhafter Nachlauf die Datei nicht
        # zurücknehmen. Alle unabhängigen Folgeaktionen werden weiter versucht.
        errors = []

        def attempt(name, operation):
            try:
                operation()
            except Exception as exc:
                errors.append(f'{name}: {exc}')

        attempt('Speicherstand', lambda: plan.accept(comparison))
        try:
            for name, operation in plan.followups(comparison):
                attempt(name, operation)
        except Exception as exc:
            errors.append(f'Folgeaktionen: {exc}')
        pending, saved = False, None
        try:
            pending, saved = plan.settings()
        except Exception as exc:
            errors.append(f'Einstellungsstatus: {exc}')
        return SaveResult(data_written=True, lock_verified=True,
                          backup_checked=backup_checked, backup_warning=backup_warning,
                          history_updated=True, followup_errors=tuple(errors),
                          settings_pending=pending, settings_saved=saved)
