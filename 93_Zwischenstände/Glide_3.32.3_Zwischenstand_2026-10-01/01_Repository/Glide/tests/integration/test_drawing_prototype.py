"""Regressionstests für die isolierte Tk-Zeichenflächenprobe."""

from __future__ import annotations

import importlib.machinery
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import sys
import tempfile
import tkinter as tk


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/glide/drawing_prototype.pyw"
loader = importlib.machinery.SourceFileLoader("drawing_prototype_test", str(SOURCE))
spec = importlib.util.spec_from_loader(loader.name, loader)
prototype = importlib.util.module_from_spec(spec)
sys.modules[loader.name] = prototype
loader.exec_module(prototype)

root = tk.Tk()
root.geometry("980x820")
root.update_idletasks()

# Direkte Eingaben werden robust normalisiert; der gespeicherte Vertrag bleibt #RRGGBB.
assert prototype.normalize_ui_color("#abc", root) == "#AABBCC"
assert prototype.normalize_ui_color("abc", root) == "#AABBCC"
assert prototype.normalize_ui_color("00ff7f", root) == "#00FF7F"
assert prototype.normalize_ui_color("red", root) == "#FF0000"
try:
    prototype.normalize_ui_color("kein-farbwert", root)
except prototype.DrawingFormatError:
    pass
else:
    raise AssertionError("Ungültiger Farbwert wurde angenommen")

# Beliebige Seitenverhältnisse werden deterministisch auf die feste Referenzebene gerahmt.
wide = tk.PhotoImage(master=root, width=4, height=2)
wide.put("{#FF0000 #FF0000 #0000FF #0000FF} {#FF0000 #FF0000 #0000FF #0000FF}")
fit = prototype.render_framed_reference(wide, "fit")
fill = prototype.render_framed_reference(wide, "fill")
assert (fit.width(), fit.height()) == (128, 128)
assert fit.get(0, 0) == (255, 255, 255)  # Querformat erhält beim Einpassen Rand.
assert fill.get(0, 64) == (255, 0, 0)
assert fill.get(127, 64) == (0, 0, 255)
shifted = prototype.render_framed_reference(wide, "fill", 100, 128, 0)
assert shifted.get(0, 64) == (255, 255, 255)

# Eine Kontur, die mindestens ein Drittel einer Zielzelle trifft, bleibt auch
# dann erhalten, wenn die reine Mittelpunkt-Abtastung sie verfehlen würde.
large = tk.PhotoImage(master=root, width=256, height=256)
large.put("#FFFFFF", to=(0, 0, 256, 256))
large.put("#000000", to=(21, 0, 22, 256))
center_sample = prototype.render_framed_reference(large, "fit")
contour_sample = prototype.render_trace_reference(large, "fit")
assert center_sample.get(10, 50) == (255, 255, 255)
assert contour_sample.get(10, 50) == (0, 0, 0)

# Der Nachzeichner hält Weiß als Hintergrund, bewahrt ausreichend breite
# Konturen und begrenzt das bearbeitbare Ergebnis auf insgesamt 64 Farben.
source = tk.PhotoImage(master=root, width=128, height=128)
gradient_rows = []
for y in range(128):
    colors = []
    for x in range(128):
        if 20 <= x < 22:
            colors.append("#000000")
        elif x < 4:
            colors.append("#FFFFFF")
        else:
            colors.append(f"#{x * 2:02X}{y * 2:02X}{(x + y) % 256:02X}")
    gradient_rows.append("{" + " ".join(colors) + "}")
source.put(" ".join(gradient_rows))
traced = prototype.quantize_reference(source)
assert traced.palette[0] == "#FFFFFF"
assert len(traced.palette) <= 64
assert traced.color_index_at(0, 50) == 0
assert traced.color_at(20, 50) == "#000000"
assert prototype.DrawingModel.from_json(traced.to_json()).to_json() == traced.to_json()

app = prototype.DrawingPrototype(root)
root.update_idletasks()

# Die Zeichenfläche wird in beiden Achsen zentriert, solange sie in die Ansicht passt.
app._center_surface(SimpleNamespace(width=900, height=800))
region = tuple(float(value) for value in app.canvas.cget("scrollregion").split())
assert region == (-130.0, -80.0, 770.0, 720.0), region

# Fokuswechsel innerhalb der App dürfen den ersten Strich nicht mehr abbrechen.
assert app.root.bind("<FocusOut>") in (None, "")
assert app.canvas.bind("<FocusOut>")
app.canvas.configure(scrollregion=(0, 0, 640, 640))
app.canvas.xview_moveto(0)
app.canvas.yview_moveto(0)
press = SimpleNamespace(x=12, y=12)
drag = SimpleNamespace(x=112, y=12)
app._press(press)
assert app.dragging, "Erstes Ansetzen wurde abgebrochen"
app._drag(drag)
app._release()
assert sum(value != 0 for value in app.model.cells) > 1, "Erster Strich blieb ein Einzelpunkt"

# Die beiden Abschlusswege des PNG-Dialogs bleiben getrennt: Referenz allein
# verändert das Modell nicht, Nachzeichnen ersetzt es erst nach der Vorschau.
original_picker = prototype.filedialog.askopenfilename
original_dialog = prototype.ReferenceFrameDialog
with tempfile.TemporaryDirectory() as temp_dir:
    png_path = Path(temp_dir) / "referenz.png"
    local_image = tk.PhotoImage(master=root, width=128, height=128)
    local_image.put("#D42A3A", to=(0, 0, 128, 128))
    local_image.write(png_path, format="png")
    prototype.filedialog.askopenfilename = lambda **_kwargs: str(png_path)

    before = app.model.to_json()

    class ReferenceOnly:
        def __init__(self, _parent, image, _filename, **_kwargs):
            self.result = prototype.render_framed_reference(image)
            self.trace_model = None

    prototype.ReferenceFrameDialog = ReferenceOnly
    app.load_reference()
    assert app.model.to_json() == before
    assert app.reference_visible.get() is True

    class TraceChoice:
        def __init__(self, _parent, image, _filename, **_kwargs):
            self.result = prototype.render_framed_reference(image)
            self.trace_model = prototype.quantize_reference(self.result)

    prototype.ReferenceFrameDialog = TraceChoice
    app.load_reference()
    assert app.reference_visible.get() is False
    assert app.model.palette == ["#FFFFFF", "#D42A3A"]
    assert set(app.model.cells) == {1}

prototype.filedialog.askopenfilename = original_picker
prototype.ReferenceFrameDialog = original_dialog

root.destroy()
print("test_drawing_prototype: OK")
