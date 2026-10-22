"""Hintergrundarbeit für lokale Kalender; keine Tk-Aufrufe oder Nutzerdateischreibzugriffe.

Die UI pumpt poll() und liest view(day). Generation und Quellhash verwerfen
veraltete Ergebnisse. Eine fehlende Auswertung ist ausdrücklich unbekannt.
"""
from collections import OrderedDict
from dataclasses import dataclass
from datetime import date
from queue import Empty, Queue
from threading import Lock, Thread
import busy_calendar


@dataclass(frozen=True)
class View:
    status: str
    blocks: tuple = ()
    issues: tuple = ()
    message: str = ""
    sha256: str = ""


def bounds(year):
    if type(year) is not int or not 1 <= year < 9999:
        raise ValueError("Kalenderauswertung benötigt ein Jahr zwischen 1 und 9998.")
    return date(year, 1, 1), date(year, 12, 31)


class CalendarService:
    def __init__(self, *, reader=busy_calendar.read_source,
                 expander=busy_calendar.expand_window, cache_size=4):
        self.reader, self.expander = reader, expander
        self.cache_size = max(1, cache_size)
        self.source = None
        self.error = ""
        self.windows = OrderedDict()
        self.failures = {}
        self.pending = set()
        self.generation = 0
        self.closed = False
        self.loading = False
        self._lock = Lock()
        self._jobs = Queue()
        self._results = Queue()
        self._thread = None

    def _submit(self, job):
        if self._thread is None:
            self._thread = Thread(target=self._work, name="glide-kalender", daemon=True)
            self._thread.start()
        self._jobs.put(job)

    def _work(self):
        while True:
            job = self._jobs.get()
            if job is None:
                return
            token, operation, payload, year = job
            with self._lock:
                current = not self.closed and token == self.generation
            if not current:
                continue
            try:
                source = self.reader(*payload) if operation == "load" else payload
                # Lesen kann bis nach Quellwechsel, Übernahme oder Schließen
                # laufen. Überholte Arbeit vor der teureren Expansion beenden;
                # eine bereits gestartete Expansion hat keinen Abbruchvertrag.
                with self._lock:
                    current = not self.closed and token == self.generation
                if not current:
                    continue
                first, last = bounds(year)
                # Floating-Termine werden in source.zone gelesen. Tagesgrenzen
                # dürfen in einer anderen lokalen Zone liegen, auch am Jahresrand.
                window = self.expander(source, first, last, 2)
                result = (source, window)
                error = ""
            except Exception as exc:
                result, error = None, str(exc) or type(exc).__name__
            self._results.put((token, operation, year, result, error))

    def _reset(self):
        with self._lock:
            self.generation += 1
        self.windows.clear()
        self.failures.clear()
        self.pending.clear()
        self.source = None
        self.error = ""
        self.loading = False

    def load(self, path, zone, day, resolver=None, date_zone=None):
        if self.closed:
            raise RuntimeError("Kalenderdienst ist geschlossen.")
        bounds(day.year)
        self._reset()
        self.loading = True
        self.pending.add(day.year)
        payload = (path, zone, resolver) if date_zone is None else (path, zone, resolver, date_zone)
        self._submit((self.generation, "load", payload, day.year))
        return self.generation

    def adopt(self, source, window):
        if self.closed:
            raise RuntimeError("Kalenderdienst ist geschlossen.")
        if (window.sha256 != source.sha256 or window.first.year != window.last.year
                or (window.first, window.last) != bounds(window.first.year)):
            raise ValueError("Kalenderfenster passt nicht zur gewählten Quelle.")
        self._reset()
        self.source = source
        self.windows[window.first.year] = window

    def disable(self):
        self._reset()

    def poll(self):
        """Alle fertigen Ergebnisse übernehmen; Rückgabe zeigt eine Zustandsänderung."""
        changed = False
        while True:
            try:
                token, operation, year, result, error = self._results.get_nowait()
            except Empty:
                break
            if self.closed or token != self.generation:
                continue
            self.pending.discard(year)
            changed = True
            if operation == "load":
                self.loading = False
                self.error = error
            if error:
                self.failures[year] = error
                continue
            source, window = result
            if window.sha256 != source.sha256:
                self.failures[year] = "Kalenderfenster passt nicht zur Quelle."
                if operation == "load":
                    self.error = self.failures[year]
                continue
            if operation == "load":
                self.source = source
            if self.source is None or self.source.sha256 != source.sha256:
                continue
            self.windows[year] = window
            self.windows.move_to_end(year)
            while len(self.windows) > self.cache_size:
                self.windows.popitem(last=False)
        return changed

    def view(self, day, zone=None):
        if self.closed:
            return View("closed", message="Kalenderdienst ist geschlossen.")
        if type(day) is not date:
            return View("error", message="Ungültiger Kalendertag.")
        if self.error:
            return View("error", message=self.error)
        if self.loading:
            return View("loading", message="Kalender wird gelesen …")
        if self.source is None:
            return View("disabled")
        year = day.year
        if year in self.failures:
            return View("error", message=self.failures[year], sha256=self.source.sha256)
        window = self.windows.get(year)
        if window is not None:
            self.windows.move_to_end(year)
            try:
                blocks = window.day_blocks(day, zone or self.source.zone)
            except (ValueError, OverflowError):
                return View("error", message="Dieser Kalendertag liegt außerhalb der darstellbaren Tagesgrenzen in der lokalen Zeitzone.",
                            sha256=self.source.sha256)
            return View("ready", blocks, window.issues, sha256=self.source.sha256)
        try:
            bounds(year)
        except ValueError as exc:
            return View("error", message=str(exc), sha256=self.source.sha256)
        if year not in self.pending:
            self.pending.add(year)
            self._submit((self.generation, "expand", self.source, year))
        return View("loading", message="Kalenderzeitraum wird berechnet …", sha256=self.source.sha256)

    def close(self):
        with self._lock:
            self.closed = True
            self.generation += 1
        self.windows.clear()
        self.pending.clear()
        self._jobs.put(None)
