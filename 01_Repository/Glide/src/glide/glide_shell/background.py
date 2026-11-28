# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 29: bounded background work with delivery on the Tk thread (Shell 0.11.0).

Long file, conversion or computation work runs in worker threads; results
come back to the Tk thread through the owner widget's `AfterScope` (polling
a thread-safe queue), so widgets are only touched on the Tk thread and never
after their owner is destroyed. Jobs have a priority, can be cancelled, and a
newer job with the same `key` makes older results stale (they are dropped,
not delivered). The queue is bounded; `submit` refuses work when full.

Public interface:

- `TaskQueue(owner, workers=2, max_pending=64, poll_ms=30)`:
  `submit(fn, *args, on_done=None, on_error=None, priority=0, key=None)` →
  `Job` or None when full/closed; `cancel(job)`; `cancel_key(key)`;
  `pending()`; `close(wait=False)` (also on owner destroy); `stats()`.
- `Job` with `id`, `key`, `priority`, `cancelled`, `state`
  (``queued``/``running``/``done``/``failed``/``cancelled``/``stale``).

`fn` must not touch Tk. `on_done(result)` and `on_error(exc)` run on the Tk
thread. Exceptions without `on_error` are counted in `stats()["errors"]`.
"""
from __future__ import annotations

import heapq
import itertools
import queue
import threading

from glide_shell import window_lifetime


class Job:
    __slots__ = ("id", "key", "priority", "fn", "args", "on_done", "on_error", "cancelled", "state", "generation")

    def __init__(self, job_id, fn, args, on_done, on_error, priority, key, generation):
        self.id, self.fn, self.args = job_id, fn, args
        self.on_done, self.on_error = on_done, on_error
        self.priority, self.key, self.generation = priority, key, generation
        self.cancelled = False
        self.state = "queued"


class TaskQueue:
    def __init__(self, owner, workers=2, max_pending=64, poll_ms=30):
        self.owner = owner
        self.max_pending = int(max_pending)
        self.poll_ms = int(poll_ms)
        self.scope = window_lifetime.scope_for(owner)
        self._heap = []
        self._lock = threading.Condition()
        self._results = queue.Queue()
        self._ids = itertools.count(1)
        self._generations = {}
        self._closed = False
        self._poll = None
        self.counts = {"submitted": 0, "done": 0, "errors": 0, "cancelled": 0, "stale": 0, "refused": 0}
        self._threads = [threading.Thread(target=self._work, name=f"glide-shell-task-{i}", daemon=True)
                         for i in range(max(1, int(workers)))]
        for thread in self._threads:
            thread.start()
        owner.bind("<Destroy>", self._destroyed, add="+")

    # --- Tk-Seite ---------------------------------------------------------------
    def submit(self, fn, *args, on_done=None, on_error=None, priority=0, key=None):
        with self._lock:
            if self._closed or len(self._heap) >= self.max_pending:
                self.counts["refused"] += 1
                return None
            generation = None
            if key is not None:
                generation = self._generations.get(key, 0) + 1
                self._generations[key] = generation
            job = Job(next(self._ids), fn, args, on_done, on_error, priority, key, generation)
            heapq.heappush(self._heap, (-priority, job.id, job))
            self.counts["submitted"] += 1
            self._lock.notify()
        self._ensure_poll()
        return job

    def cancel(self, job):
        if job is not None and job.state in ("queued", "running"):
            job.cancelled = True
            return True
        return False

    def cancel_key(self, key):
        with self._lock:
            self._generations[key] = self._generations.get(key, 0) + 1
            treffer = [j for _p, _i, j in self._heap if j.key == key]
        for job in treffer:
            self.cancel(job)
        return len(treffer)

    def pending(self):
        with self._lock:
            return sum(1 for _p, _i, j in self._heap if not j.cancelled)

    def stats(self):
        return {**self.counts, "pending": self.pending(), "workers": len(self._threads), "closed": self._closed}

    def _ensure_poll(self):
        if self._poll is None and not self.scope.closed:
            self._poll = self.scope.after(self.poll_ms, self._deliver)

    def _deliver(self):
        self._poll = None
        while True:
            try:
                job, ok, wert = self._results.get_nowait()
            except queue.Empty:
                break
            if job.cancelled:
                job.state = "cancelled"
                self.counts["cancelled"] += 1
                continue
            if job.key is not None and self._generations.get(job.key) != job.generation:
                job.state = "stale"
                self.counts["stale"] += 1
                continue
            if ok:
                job.state = "done"
                self.counts["done"] += 1
                if callable(job.on_done):
                    job.on_done(wert)
            else:
                job.state = "failed"
                self.counts["errors"] += 1
                if callable(job.on_error):
                    job.on_error(wert)
        erledigt = sum(self.counts[k] for k in ("done", "errors", "cancelled", "stale"))
        if self.counts["submitted"] > erledigt and not self._closed:
            self._ensure_poll()

    def close(self, wait=False):
        with self._lock:
            self._closed = True
            for _p, _i, job in self._heap:
                job.cancelled = True
            self._lock.notify_all()
        if self._poll is not None:
            self.scope.cancel(self._poll)
            self._poll = None
        if wait:
            for thread in self._threads:
                thread.join(timeout=5)

    def _destroyed(self, event):
        if event.widget is self.owner:
            self.close()

    # --- Arbeiter ---------------------------------------------------------------
    def _work(self):
        while True:
            with self._lock:
                while not self._heap and not self._closed:
                    self._lock.wait()
                if self._closed and not self._heap:
                    return
                _p, _i, job = heapq.heappop(self._heap)
                if self._closed:
                    job.cancelled = True
            if job.cancelled:
                self._results.put((job, True, None))
                continue
            job.state = "running"
            try:
                self._results.put((job, True, job.fn(*job.args)))
            except BaseException as error:  # noqa: BLE001 – delivered to on_error on the Tk thread
                self._results.put((job, False, error))
