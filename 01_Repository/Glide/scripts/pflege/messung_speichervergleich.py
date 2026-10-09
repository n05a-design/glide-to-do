"""P08a: unprofilierte, abwechselnde Vergleichsmessung gegen einen Git-Stand.

Kein Tk-Fenster, keine echten Daten. Gleiche synthetische Aufgaben mit stabilen
IDs, flach und mit Unteraufgaben. Gemessen wird nur die Vergleichsarbeit vor/
nach dem Schreiben, nicht die Dateispeicherung oder die Bedienlatenz.

    python -B scripts/pflege/messung_speichervergleich.py --baseline-ref <SHA> --json <Ausgabe>
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

from messung_speicherweg import verteilung

REPO = Path(__file__).resolve().parents[2]


def load(path, name):
    loader = importlib.machinery.SourceFileLoader(name, str(path))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(name, loader))
    sys.modules[name] = mod
    loader.exec_module(mod)
    return mod


def fixture(count, nested):
    lists = []
    for start in range(0, count, 200):
        items = [{"id": f"i{number}", "text": f"Aufgabe {number} ä",
                  "kind": "task", "done": False, "description": "Beschreibung " * (number % 20),
                  "labels": [], "attachments": [], "repeat": {}, "children": []}
                 for number in range(start, min(start + 200, count))]
        if nested:
            for index in range(0, len(items), 10):
                items[index]["children"] = items[index + 1:index + 10]
            items = items[::10]
        lists.append({"id": f"l{start}", "title": f"Liste {start}", "items": items})
    return lists


def state(mod, lists):
    app = object.__new__(mod.ListApp)
    app.lists = copy.deepcopy(lists)
    app.folders, app.labels, app.trash = [], [], []
    app._history_baseline = app.history_snapshot()
    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--baseline-ref", required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=21)
    args = parser.parse_args()
    if args.rounds < 2:
        parser.error("Mindestens zwei warme Runden")
    results = []
    sys.path.insert(0, str(REPO / "src/glide"))
    with tempfile.TemporaryDirectory(prefix="glide-vergleich-messung-") as folder:
        os.environ["GLIDE_DATA_DIR"] = folder
        os.environ["GLIDE_TEST_MODE"] = "1"
        old_source = Path(folder) / "baseline.pyw"
        old_source.write_bytes(subprocess.check_output([
            "git", "show", f"{args.baseline_ref}:01_Repository/Glide/src/glide/app.pyw"], cwd=REPO))
        old_mod = load(old_source, "glide_comparison_old")
        new_mod = load(REPO / "src/glide/app.pyw", "glide_comparison_new")
        for nested in (False, True):
            for count in (100, 1000, 10000):
                lists = fixture(count, nested)
                old, new = state(old_mod, lists), state(new_mod, lists)

                def previous():
                    old.stamp_done_times(old._history_baseline)
                    history = old.history_snapshot()
                    list_values = old.list_edit_signatures()
                    item_values = {item["id"]: old_mod.hashlib.sha256(old_mod.json.dumps(
                        item, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
                        for entry in old.lists for item in old.walk_items(entry.get("items", []))
                        if old.is_schedulable_item(item)}
                    return history, list_values, item_values

                def current():
                    compared = new.list_comparison(stamp_done=True)
                    return new.history_snapshot(comparison=compared), compared.list_signatures, compared.item_signatures

                assert previous()[0] == current()[0]
                measurements = {"vorher": [], "nachher": []}
                for number in range(args.rounds):
                    # Paarweise abwechseln; gleiche Feldänderung auf beiden Beständen.
                    for app in (old, new):
                        app.lists[0]["items"][0]["description"] = f"Änderung {number}"
                    actions = [("vorher", previous), ("nachher", current)]
                    if number % 2:
                        actions.reverse()
                    snapshots = {}
                    for name, action in actions:
                        start = time.perf_counter()
                        snapshots[name] = action()
                        measurements[name].append((time.perf_counter() - start) * 1000)
                    assert snapshots["vorher"][0] == snapshots["nachher"][0]
                result = {"punkte": count, "struktur": "Unteraufgaben" if nested else "flach",
                          **{name: verteilung(values) for name, values in measurements.items()}}
                result["median_gewinn_prozent"] = round(
                    100 * (1 - result["nachher"]["median_ms"] / result["vorher"]["median_ms"]), 1)
                results.append(result)
                print(f"{count:5d} {result['struktur']}: {result['vorher']['median_ms']} -> "
                      f"{result['nachher']['median_ms']} ms ({result['median_gewinn_prozent']} %)")
    report = {"werkzeug": "messung_speichervergleich.py", "baseline_ref": args.baseline_ref,
              "baseline_version": old_mod.APP_VERSION, "app_version": new_mod.APP_VERSION,
              "python": platform.python_version(), "plattform": platform.platform(),
              "runden_warm": args.rounds, "bereich": "Vergleichsarbeit ohne I/O oder Oberfläche",
              "ergebnisse": results}
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
