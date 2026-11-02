"""Aktuelle eigene Fenster aufnehmen; Fenster-ID statt fremder OS-Überlagerungen.

macOS: python3 -B sichtprobe.py REPO AUSGABE
Nur synthetische Daten; nutzt die vorhandene Aufnahme aus test_fenster330.
"""
import ast
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile


def main():
    if sys.platform != "darwin":
        raise SystemExit("Diese native Fensterprobe benötigt macOS.")
    repo, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = repo / "src/glide/app.pyw"
    sys.path[:0] = [str(source.parent), str(repo / "tests/integration")]
    # Nur die erprobte Aufnahmefunktion laden; der umgebende Test würde seine
    # eigene vollständige Fenstersuite starten.
    capture_source = repo / "tests/integration/test_fenster330.py"
    capture_ast = ast.parse(capture_source.read_text())
    capture_node = next(n for n in ast.walk(capture_ast)
                        if isinstance(n, ast.FunctionDef) and n.name == "fenster_foto")
    namespace = dict(os=os, sys=sys, subprocess=subprocess, Path=Path, REPO=repo,
                     FOTOS=str(output), fenster=[], befunde=[])
    exec(compile(ast.Module(body=[capture_node], type_ignores=[]), str(capture_source), "exec"), namespace)
    result = dict(app_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  capture_helper_sha256=hashlib.sha256(capture_source.read_bytes()).hexdigest(),
                  method="CGWindowList: eigener PID/Layer 0; screencapture -l", images=[])
    with tempfile.TemporaryDirectory(prefix="glide-sichtabschluss-") as data:
        os.environ["GLIDE_DATA_DIR"], os.environ["GLIDE_TEST_MODE"] = data, "1"
        loader = importlib.machinery.SourceFileLoader("glide_capture_fonts", str(source))
        module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = module
        loader.exec_module(module)
        module.register_private_fonts()
        from test_uiux_paket import Lauf
        run = Lauf(source, data)
        try:
            app = run.app
            app.set_design("dark")
            label = app.new_label_object("Text", color="export")
            app.labels.append(label)
            tasks = [app.new_item("Unterlagen prüfen"), app.new_item("Termin abstimmen")]
            listing = app.new_list_object("Projektplanung", tasks)
            app.lists.append(listing)
            assert app.save_items()
            page = app.new_page_from_markdown(
                "# Projektübersicht\n\nInformationen und nächste Schritte an einem Ort.\n\n"
                "## Freigaben\n\n- Unterlagen abstimmen\n- Angebot prüfen\n")
            for entry in (listing, page):
                app.toggle_page_label("list", entry["id"], label["id"])

            def capture(name):
                filename = f"{len(namespace['fenster']):03d}_{name}.png"
                target = output / filename
                if target.exists():
                    raise FileExistsError("Eine frische Ausgabeablage verwenden.")
                run.root.after(300, run.root.quit)
                run.root.mainloop()
                run.idle()
                namespace["fenster_foto"](run.root, name)
                assert not namespace["befunde"], namespace["befunde"]
                png = target.read_bytes()
                assert png.startswith(b"\x89PNG\r\n\x1a\n")
                width, height = struct.unpack(">II", png[16:24])
                result["images"].append(dict(file=filename, width=width, height=height,
                                             sha256=hashlib.sha256(png).hexdigest()))
                namespace["fenster"].append(name)

            app.set_active_list(page["id"])
            run.idle()
            capture("Seite_Ecklabels")
            app.set_active_list(listing["id"])
            app.open_list_view()
            run.idle()
            app.tree.selection_set(tasks[0]["id"])
            app.tree.focus(tasks[0]["id"])
            run.idle()
            app.show_quick_plan_row()
            run.idle()
            capture("Liste_Symbolaktionen")
            from test_arbeitsmodi import phase348_bestand
            _today, tomorrow, *_rest = phase348_bestand(run)
            app._data_read_only = True
            app.change_home_day(tomorrow)
            run.idle()
            capture("Startseite_Schreibschutz")
            run.root.geometry("860x800+20+20")
            run.idle()
            capture("Startseite_Schmal")
            app._data_read_only = False
            assert not run.errors, run.errors
            result["callback_errors"] = run.errors
        finally:
            run.ende()
    (output / "sichtpruefung.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
