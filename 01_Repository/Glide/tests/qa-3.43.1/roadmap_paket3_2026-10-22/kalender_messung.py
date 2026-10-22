"""Kontrollierter Vorher-/Nachherablauf für WA-36, keine native Latenzmessung.

Der echte CalendarService arbeitet mit injiziertem Reader/Expander. Events
erzwingen den Quellwechsel während des alten Reads. Die Kosten sind ausdrücklich
simulierte, feste Recheneinheiten: Restlesen alt 40, Expansion alt 200, Lesen neu
20, Expansion neu 30. Es gibt keine Sleeps oder zeitabhängigen Erfolgskriterien.

Aufruf vom Projektordner:
  python tests/qa-3.43.1/roadmap_paket3_2026-10-22/kalender_messung.py \
      --before PFAD_ZUR_GESICHERTEN_calendar_service.py --output ergebnis.json

Ohne --before wird allein der aktuelle Ablauf ausgeführt. Der vorherige Stand
wird weder im Skript nachgebaut noch als zweite Laufzeitdatei im Repo abgelegt.
"""
import argparse
from datetime import date, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from threading import Event, get_ident
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src" / "glide"))


def load_service(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module.CalendarService


def run(path, name):
    service_type = load_service(path, name)
    started, release = Event(), Event()
    clock = 0
    trace, worker_ids, expansions = [], set(), []
    latest_reader_start = None

    def step(operation, cost=0):
        nonlocal clock
        worker_ids.add(get_ident())
        clock += cost
        trace.append({"event": operation, "simulated_units": clock})

    def reader(label, zone, resolver):
        nonlocal latest_reader_start
        step("read_" + label + ":start")
        if label == "old":
            started.set()
            if not release.wait(5):
                raise TimeoutError("Alter Leser wurde nicht freigegeben")
            step("read_old:end", 40)
        else:
            latest_reader_start = clock
            step("read_latest:end", 20)
        return SimpleNamespace(sha256=label, zone=zone)

    def expander(source, first, last, margin):
        expansions.append(source.sha256)
        step("expand_" + source.sha256 + ":start")
        step("expand_" + source.sha256 + ":end", 200 if source.sha256 == "old" else 30)
        return SimpleNamespace(sha256=source.sha256, first=first, last=last,
                               issues=(), day_blocks=lambda day, zone: ())

    service = service_type(reader=reader, expander=expander)
    try:
        day = date(2026, 10, 11)
        service.load("old", timezone.utc, day)
        if not started.wait(5):
            raise TimeoutError("Alter Leser startet nicht")
        worker = service._thread
        # Die Freigabe liegt nach der neuen Generation, ohne Schedulerannahme.
        service.load("latest", timezone.utc, day)
        release.set()
        service._jobs.put(None)
        worker.join(5)
        if worker.is_alive():
            raise TimeoutError("Kalenderarbeiter beendet sich nicht")
        service.poll()
        if service.view(day).status != "ready" or service.source.sha256 != "latest":
            raise AssertionError("Neueste Quelle wurde nicht korrekt übernommen")
        if service._thread is not worker or len(worker_ids) != 1 or get_ident() in worker_ids:
            raise AssertionError("Arbeit muss seriell in einem Hintergrundthread bleiben")
        return {
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "expansions": expansions,
            "obsolete_expansions": expansions.count("old"),
            "latest_reader_start_simulated_units": latest_reader_start,
            "latest_ready_simulated_units": clock,
            "latest_status": service.view(day).status,
            "background_worker_count": len(worker_ids),
            "trace": trace,
        }
    finally:
        release.set()
        service.close()
        if service._thread is not None:
            service._thread.join(5)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--after", type=Path, default=ROOT / "src" / "glide" / "calendar_service.py")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "kind": "controlled_worker_trace_with_simulated_costs",
        "native_latency_measurement": False,
        "cost_unit": "simulated_work_unit_without_wall_time_claim",
        "budget": {"old_read_remaining": 40, "old_expansion": 200,
                   "latest_read": 20, "latest_expansion": 30},
    }
    if args.before:
        result["before"] = run(args.before.resolve(), "calendar_service_before_measurement")
    result["after"] = run(args.after.resolve(), "calendar_service_after_measurement")
    if args.before:
        result["avoided_simulated_units"] = (
            result["before"]["latest_ready_simulated_units"]
            - result["after"]["latest_ready_simulated_units"])
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    print(output, end="")


if __name__ == "__main__":
    main()
