"""Kurze, unterbrechbare Übergänge; Uhr und Zeitplanung werden injiziert."""
from dataclasses import dataclass
from time import monotonic


def progress(elapsed, duration_ms):
    duration = max(0, min(150, duration_ms)) / 1000
    value = 1.0 if not duration else max(0.0, min(1.0, elapsed / duration))
    return 1.0 - (1.0 - value) ** 3


@dataclass
class Flight:
    update: object
    finish: object
    started: float
    duration: int
    job: object = None


class Transitions:
    def __init__(self, schedule, unschedule, clock=monotonic):
        self.schedule, self.unschedule, self.clock = schedule, unschedule, clock
        self.active = {}
        self.closed = False

    def start(self, key, update, finish=lambda: None, *, enabled=True, duration_ms=120):
        self.cancel(key)
        if self.closed or not enabled or duration_ms <= 0:
            try:
                update(1.0)
            finally:
                finish()
            return
        flight = Flight(update, finish, self.clock(), min(150, int(duration_ms)))
        self.active[key] = flight
        self._step(key, flight)

    def _step(self, key, flight):
        if self.active.get(key) is not flight:
            return
        flight.job = None
        elapsed = max(0.0, self.clock() - flight.started)
        complete = elapsed * 1000 + 1e-7 >= flight.duration
        try:
            flight.update(1.0 if complete else progress(elapsed, flight.duration))
        except Exception:
            self.cancel(key)
            raise
        if self.active.get(key) is not flight:
            return
        if complete:
            del self.active[key]
            flight.finish()
        else:
            delay = max(1, min(16, int(flight.duration - elapsed * 1000 + .999)))
            flight.job = self.schedule(delay, lambda: self._step(key, flight))

    def cancel(self, key):
        flight = self.active.pop(key, None)
        if flight is None:
            return
        try:
            if flight.job is not None:
                self.unschedule(flight.job)
        finally:
            flight.finish()

    def close(self):
        self.closed = True
        error = None
        for key in tuple(self.active):
            try:
                self.cancel(key)
            except Exception as exc:
                error = error or exc
        if error is not None:
            raise error
