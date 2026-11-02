"""Frischer echter Appstart: gebündelte Symbole und sichtbare Navigationszähler."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile


with tempfile.TemporaryDirectory(prefix="glide-kaltstart-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    source = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(source.parent))
    loader = importlib.machinery.SourceFileLoader("glide_cold_start", str(source))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    original = mod.ListApp
    expected = {name: original.ICONS[name] for name in ("home", "today", "templates", "settings")}
    result = {"errors": [], "counts": []}

    class CheckedApp(original):
        def __init__(self, root):
            super().__init__(root)
            root.report_callback_exception = lambda *_args: result["errors"].append("Tk-Callbackfehler")
            # Der erste Aufbau kann nach 100 ms noch ausstehen, etwa wenn macOS
            # das Fenster im Hintergrund erst später einblendet; dann misst die
            # Probe eine Fläche von 1 Pixel. Sie wartet deshalb bis zu 10 s auf
            # die echte Breite der Navigation, bevor sie urteilt.
            versuche = {"rest": 100}

            def check():
                tree = self.system_listbox
                try:
                    if tree.winfo_width() <= 1 and versuche["rest"] > 0:
                        versuche["rest"] -= 1
                        root.after(100, check)
                        return
                except Exception:
                    pass
                try:
                    result["tk"] = str(root.tk.call("package", "provide", "Tk"))
                    result["font"] = self.ui_font_family()
                    result["icons"] = {name: self.ICONS[name] for name in expected}
                    if result["icons"] != expected:
                        result["errors"].append("Gebündelte Standardsymbole beim frischen Start ersetzt")
                    for row in tree.get_children():
                        value = tree.set(row, "count")
                        if not value:
                            continue
                        box = tree.bbox(row, "count")
                        result["counts"].append({"value": value, "box": box, "viewport": tree.winfo_width()})
                        if not box or box[0] < 0 or box[0] + box[2] > tree.winfo_width():
                            result["errors"].append("Navigationszähler außerhalb der sichtbaren Fläche")
                except Exception as error:
                    result["errors"].append(f"Probe: {error!r}")
                self.on_close()
            root.after(100, check)

    mod.ListApp = CheckedApp
    mod.main()
    print(json.dumps(result, ensure_ascii=False))
    raise SystemExit(bool(result["errors"]))
