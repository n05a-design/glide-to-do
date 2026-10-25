"""Expliziter Ausgang einer Speicherung, unabhängig von Tk und Dateisystem."""
from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class SaveResult:
    data_written: bool = False
    lock_verified: bool = False
    backup_checked: bool = False
    backup_warning: str | None = None
    history_updated: bool = False
    error: str | None = None
    followup_errors: tuple[str, ...] = ()
    settings_pending: bool = False
    settings_saved: bool | None = None

    @property
    def success(self):
        # Folgefehler können einen bereits geschriebenen Bestand nicht
        # ungeschehen machen. Alte Bool-Aufrufer dürfen ihn nicht zurückrollen.
        return self.data_written

    def __bool__(self):
        raise TypeError('SaveResult.success auswerten; save_items liefert weiterhin bool.')

    def with_followup_error(self, detail):
        return replace(self, followup_errors=self.followup_errors + (str(detail),))

    def finish_settings(self, saved):
        if not self.settings_pending:
            return self
        errors = self.followup_errors
        if saved is False:
            errors += ('Die zusätzlichen Einstellungen konnten nicht gespeichert werden.',)
        return replace(self, settings_pending=False, settings_saved=saved, followup_errors=errors)
