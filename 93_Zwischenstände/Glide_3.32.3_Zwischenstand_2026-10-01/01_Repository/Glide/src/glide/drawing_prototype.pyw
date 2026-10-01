"""Isolierte Bedienprobe für Glides geplante Pixel-Zeichenfläche.

Start: ``python3 src/glide/drawing_prototype.pyw``

Die Probe öffnet und speichert ausschließlich ausdrücklich gewählte JSON- und
Glide-SVG-Dateien. Sie kennt den produktiven Glide-Datenordner nicht und ändert
weder dessen Datenformat noch Nutzdaten.
"""

from __future__ import annotations

import colorsys
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

SOURCE_DIR = Path(__file__).resolve().parent
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from drawing import (
    BACKGROUND,
    BRUSH_SIZES,
    HEIGHT,
    WIDTH,
    DrawingFormatError,
    DrawingModel,
    import_glide_svg,
)
from drawing_image import (
    model_to_photo,
    normalize_ui_color,
    quantize_reference,
    render_framed_reference,
    render_trace_reference,
)


class TracePreviewDialog:
    PREVIEW_ZOOM = 4

    def __init__(self, parent: tk.Misc, reference: tk.PhotoImage, replaces_existing: bool):
        self.result = None
        self.reference = reference
        self.model = DrawingModel.blank()
        self.base_image = None
        self.preview_image = None
        self._preview_job = None
        self.white_threshold = tk.IntVar(value=245)
        self.grid_mode = tk.StringVar(value="cells")
        self.status = tk.StringVar()
        self.window = tk.Toplevel(parent)
        self.window.title("Nachzeichnung prüfen")
        self.window.transient(parent)
        self.window.resizable(False, False)

        tk.Label(
            self.window,
            text="Nachzeichnung: 128 × 128 Zellen · höchstens 64 Farben · Hintergrund Weiß",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 6))
        self.preview = tk.Canvas(
            self.window, width=WIDTH * self.PREVIEW_ZOOM,
            height=HEIGHT * self.PREVIEW_ZOOM,
            bg="white", highlightthickness=1, highlightbackground="#666666",
        )
        self.preview.pack(padx=12)

        tolerance = tk.Frame(self.window)
        tolerance.pack(fill="x", padx=12, pady=(8, 0))
        tk.Label(tolerance, text="Weiß ab", width=12, anchor="w").pack(side="left")
        tk.Scale(
            tolerance, from_=220, to=255, orient="horizontal", length=300,
            variable=self.white_threshold, command=lambda _value: self._schedule_preview(),
        ).pack(side="left")
        tk.Label(tolerance, text="je RGB-Kanal").pack(side="left", padx=(6, 0))

        grid = tk.Frame(self.window)
        grid.pack(fill="x", padx=12, pady=(5, 0))
        tk.Label(grid, text="Vorschau-Raster", width=12, anchor="w").pack(side="left")
        for value, label in (("none", "Aus"), ("cells", "Jede Zelle"), ("groups", "8er-Gruppen")):
            tk.Radiobutton(
                grid, text=label, value=value, variable=self.grid_mode,
                command=self._draw_preview,
            ).pack(side="left")

        tk.Label(self.window, textvariable=self.status, anchor="w").pack(
            fill="x", padx=12, pady=(6, 0)
        )
        if replaces_existing:
            tk.Label(
                self.window,
                text="Die Übernahme ersetzt den aktuellen Inhalt der Zeichenfläche.",
                fg="#A33A2B", anchor="w",
            ).pack(fill="x", padx=12, pady=(3, 0))

        actions = tk.Frame(self.window)
        actions.pack(fill="x", padx=12, pady=(8, 12))
        tk.Button(actions, text="Zurück zum Rahmen", command=self.window.destroy).pack(side="left")
        tk.Button(actions, text="Nachzeichnung übernehmen", command=self._apply).pack(side="right")

        self._refresh_model()
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.grab_set()
        self.window.wait_window()

    def _schedule_preview(self):
        if self._preview_job is not None:
            self.window.after_cancel(self._preview_job)
        self._preview_job = self.window.after(50, self._refresh_model)

    def _refresh_model(self):
        self._preview_job = None
        self.model = quantize_reference(
            self.reference, max_colors=64,
            white_threshold=self.white_threshold.get(),
        )
        self.base_image = model_to_photo(self.model)
        self.preview_image = self.base_image.zoom(self.PREVIEW_ZOOM, self.PREVIEW_ZOOM)
        used = len(set(self.model.cells))
        self.status.set(f"{used} Farben verwendet · breite Konturen bleiben als Zellen erhalten")
        self._draw_preview()

    def _draw_preview(self):
        self.preview.delete("all")
        self.preview.create_image(0, 0, image=self.preview_image, anchor="nw")
        mode = self.grid_mode.get()
        if mode == "none":
            return
        step = 1 if mode == "cells" else 8
        for value in range(0, WIDTH + 1, step):
            position = value * self.PREVIEW_ZOOM
            color = "#777777" if value % 8 == 0 else "#C8C8C8"
            width = 1 if value % 8 else 2
            self.preview.create_line(position, 0, position, HEIGHT * self.PREVIEW_ZOOM,
                                     fill=color, width=width)
            self.preview.create_line(0, position, WIDTH * self.PREVIEW_ZOOM, position,
                                     fill=color, width=width)

    def _apply(self):
        self.result = self.model
        self.window.destroy()


class ColorSpectrumDialog:
    WIDTH = 256
    HEIGHT = 144

    def __init__(self, parent: tk.Misc, initial: str):
        self.result = None
        self.window = tk.Toplevel(parent)
        self.window.title("Zeichenfarbe aus Farbspektrum")
        self.window.transient(parent)
        self.window.resizable(False, False)
        red = int(initial[1:3], 16) / 255
        green = int(initial[3:5], 16) / 255
        blue = int(initial[5:7], 16) / 255
        hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
        self.hue = hue
        self.saturation = saturation
        self.brightness = tk.IntVar(value=max(20, round(value * 100)))
        self.selected = initial
        self.image = None
        self.marker = None

        tk.Label(
            self.window,
            text="Farbton horizontal, Sättigung vertikal",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 4))
        self.canvas = tk.Canvas(
            self.window, width=self.WIDTH, height=self.HEIGHT,
            highlightthickness=1, highlightbackground="#666666",
        )
        self.canvas.pack(padx=12)
        self.canvas.bind("<Button-1>", self._select)
        self.canvas.bind("<B1-Motion>", self._select)

        brightness_row = tk.Frame(self.window)
        brightness_row.pack(fill="x", padx=12, pady=(8, 0))
        tk.Label(brightness_row, text="Helligkeit").pack(side="left")
        tk.Scale(
            brightness_row, from_=5, to=100, orient="horizontal",
            variable=self.brightness, command=self._brightness_changed,
            showvalue=True, length=190,
        ).pack(side="left", padx=(8, 0))

        result_row = tk.Frame(self.window)
        result_row.pack(fill="x", padx=12, pady=8)
        self.swatch = tk.Label(result_row, width=4, relief="sunken", bg=initial)
        self.swatch.pack(side="left")
        self.value_label = tk.Label(result_row, text=initial, width=10, anchor="w")
        self.value_label.pack(side="left", padx=8)
        tk.Button(result_row, text="Abbrechen", command=self.window.destroy).pack(side="right")
        tk.Button(result_row, text="Übernehmen", command=self._apply).pack(side="right", padx=4)

        self._draw_spectrum()
        self._update_selection()
        self.selected = initial
        self.swatch.configure(bg=initial)
        self.value_label.configure(text=initial)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.grab_set()
        self.window.wait_window()

    def _draw_spectrum(self):
        value = self.brightness.get() / 100
        rows = []
        for y in range(self.HEIGHT):
            saturation = 1 - y / (self.HEIGHT - 1)
            colors = []
            for x in range(self.WIDTH):
                red, green, blue = colorsys.hsv_to_rgb(x / (self.WIDTH - 1), saturation, value)
                colors.append(f"#{round(red * 255):02X}{round(green * 255):02X}{round(blue * 255):02X}")
            rows.append("{" + " ".join(colors) + "}")
        self.image = tk.PhotoImage(master=self.window, width=self.WIDTH, height=self.HEIGHT)
        self.image.put(" ".join(rows))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def _select(self, event):
        self.hue = min(1.0, max(0.0, event.x / (self.WIDTH - 1)))
        self.saturation = min(1.0, max(0.0, 1 - event.y / (self.HEIGHT - 1)))
        self._update_selection()

    def _brightness_changed(self, _value=None):
        self._draw_spectrum()
        self._update_selection()

    def _update_selection(self):
        value = self.brightness.get() / 100
        red, green, blue = colorsys.hsv_to_rgb(self.hue, self.saturation, value)
        self.selected = f"#{round(red * 255):02X}{round(green * 255):02X}{round(blue * 255):02X}"
        self.swatch.configure(bg=self.selected)
        self.value_label.configure(text=self.selected)
        x = self.hue * (self.WIDTH - 1)
        y = (1 - self.saturation) * (self.HEIGHT - 1)
        outline = "white" if value < 0.5 else "black"
        if self.marker is not None:
            self.canvas.delete(self.marker)
        self.marker = self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline=outline, width=2)

    def _apply(self):
        self.result = self.selected
        self.window.destroy()


class ReferenceFrameDialog:
    PREVIEW_ZOOM = 4

    def __init__(
        self,
        parent: tk.Misc,
        source: tk.PhotoImage,
        filename: str,
        *,
        replaces_existing: bool = False,
    ):
        self.result = None
        self.trace_model = None
        self.source = source
        self.replaces_existing = replaces_existing
        self._preview_job = None
        self.preview_image = None
        self.mode = tk.StringVar(value="fill")
        self.zoom_percent = tk.DoubleVar(value=100)
        self.offset_x = tk.DoubleVar(value=0)
        self.offset_y = tk.DoubleVar(value=0)
        self.window = tk.Toplevel(parent)
        self.window.title("PNG auf 128 × 128 einpassen")
        self.window.transient(parent)
        self.window.resizable(False, False)

        tk.Label(
            self.window,
            text=f"{filename} · {source.width()} × {source.height()} Pixel",
            anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 6))
        self.preview = tk.Canvas(
            self.window, width=WIDTH * self.PREVIEW_ZOOM,
            height=HEIGHT * self.PREVIEW_ZOOM,
            bg="white", highlightthickness=1, highlightbackground="#666666",
        )
        self.preview.pack(padx=12)

        modes = tk.Frame(self.window)
        modes.pack(fill="x", padx=12, pady=(8, 0))
        tk.Radiobutton(
            modes, text="Fläche füllen (Zuschneiden)", value="fill", variable=self.mode,
            command=self._schedule_preview,
        ).pack(side="left")
        tk.Radiobutton(
            modes, text="Ganzes Bild zeigen", value="fit", variable=self.mode,
            command=self._schedule_preview,
        ).pack(side="left", padx=(8, 0))

        self._add_scale("Größe", self.zoom_percent, 25, 400, "%")
        self._add_scale("Horizontal", self.offset_x, -128, 128, " Zellen")
        self._add_scale("Vertikal", self.offset_y, -128, 128, " Zellen")

        actions = tk.Frame(self.window)
        actions.pack(fill="x", padx=12, pady=(8, 12))
        tk.Button(actions, text="Zurücksetzen", command=self._reset).pack(side="left")
        tk.Button(actions, text="Abbrechen", command=self.window.destroy).pack(side="right")
        tk.Button(actions, text="Nur als Referenz", command=self._apply_reference).pack(side="right", padx=4)
        tk.Button(actions, text="Nachzeichnen…", command=self._trace).pack(side="right")

        self._refresh_preview()
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
        self.window.grab_set()
        self.window.wait_window()

    def _add_scale(self, label, variable, start, end, suffix):
        row = tk.Frame(self.window)
        row.pack(fill="x", padx=12, pady=(5, 0))
        tk.Label(row, text=label, width=11, anchor="w").pack(side="left")
        tk.Scale(
            row, from_=start, to=end, resolution=1, orient="horizontal",
            showvalue=False, length=330, variable=variable,
            command=lambda _value: self._schedule_preview(),
        ).pack(side="left")
        value_label = tk.Label(row, width=10, anchor="e")
        value_label.pack(side="left")
        variable.trace_add(
            "write", lambda *_args, target=value_label, source=variable, unit=suffix:
            target.configure(text=f"{source.get():.0f}{unit}")
        )
        value_label.configure(text=f"{variable.get():.0f}{suffix}")

    def _schedule_preview(self):
        if self._preview_job is not None:
            self.window.after_cancel(self._preview_job)
        self._preview_job = self.window.after(35, self._refresh_preview)

    def _render(self):
        return render_framed_reference(
            self.source, self.mode.get(), self.zoom_percent.get(),
            self.offset_x.get(), self.offset_y.get(),
        )

    def _refresh_preview(self):
        self._preview_job = None
        framed = self._render()
        self.preview_image = framed.zoom(self.PREVIEW_ZOOM, self.PREVIEW_ZOOM)
        self.preview.delete("all")
        self.preview.create_image(0, 0, image=self.preview_image, anchor="nw")

    def _reset(self):
        self.mode.set("fill")
        self.zoom_percent.set(100)
        self.offset_x.set(0)
        self.offset_y.set(0)
        self._schedule_preview()

    def _apply_reference(self):
        self.result = self._render()
        self.window.destroy()

    def _trace(self):
        framed = self._render()
        trace_reference = render_trace_reference(
            self.source, self.mode.get(), self.zoom_percent.get(),
            self.offset_x.get(), self.offset_y.get(),
        )
        dialog = TracePreviewDialog(self.window, trace_reference, self.replaces_existing)
        if dialog.result is None:
            self.window.grab_set()
            return
        self.result = framed
        self.trace_model = dialog.result
        self.window.destroy()


class DrawingPrototype:
    MIN_ZOOM = 2
    MAX_ZOOM = 8
    MAX_REFERENCE_BYTES = 32 * 1024 * 1024
    MAX_REFERENCE_DIMENSION = 4096

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Glide – isolierte Zeichenflächenprobe")
        self.root.geometry("980x820")
        self.model = DrawingModel.blank()
        self.rendered_cells = bytearray(self.model.cells)
        self.tool = tk.StringVar(value="brush")
        self.brush_size = tk.IntVar(value=1)
        self.color = tk.StringVar(value="#000000")
        self.zoom = tk.IntVar(value=5)
        self.grid_visible = tk.BooleanVar(value=True)
        self.reference_visible = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value="Bereit · nicht im Glide-Bestand gespeichert")
        self.dragging = False
        self.last_point = None
        self.reference_source = None
        self.reference_original = None
        self.reference_scaled = None
        self.reference_path = None
        self.preview_items = []
        self.cell_items = []
        self.grid_items = []
        self._build()
        self._rebuild_canvas()
        self._bind_shortcuts()

    def _build(self):
        filebar = tk.Frame(self.root, padx=8)
        filebar.pack(fill="x", pady=(8, 4))
        tk.Button(filebar, text="Neu", command=self.new).pack(side="left")
        tk.Button(filebar, text="Öffnen", command=self.open_file).pack(side="left", padx=(4, 0))
        tk.Button(filebar, text="JSON speichern", command=self.save_json).pack(side="left", padx=(4, 0))
        tk.Button(filebar, text="SVG exportieren", command=self.save_svg).pack(side="left", padx=(4, 10))

        tools = tk.Frame(self.root, padx=8)
        tools.pack(fill="x", pady=(0, 4))

        for value, label in (("brush", "Pinsel"), ("fill", "Füllen"), ("eyedropper", "Pipette")):
            tk.Radiobutton(tools, text=label, value=value, variable=self.tool).pack(side="left")
        for size in BRUSH_SIZES:
            tk.Radiobutton(
                tools, text=f"{size}×{size}", value=size, variable=self.brush_size,
                indicatoron=False, width=4,
            ).pack(side="left", padx=(3, 0))

        self.color_button = tk.Button(tools, text="Farbspektrum…", command=self.choose_color)
        self.color_button.pack(side="left", padx=(10, 3))
        self.color_entry = tk.Entry(tools, width=9, textvariable=self.color)
        self.color_entry.pack(side="left")
        self.color_entry.bind("<Return>", self._apply_color_from_entry)
        self.color_entry.bind("<KeyRelease>", self._preview_typed_color)
        self.color_swatch = tk.Label(tools, width=2, relief="sunken", bg=self.color.get())
        self.color_swatch.pack(side="left", padx=(3, 10))

        options = tk.Frame(self.root, padx=8)
        options.pack(fill="x", pady=(0, 6))
        tk.Button(options, text="↶ Undo", command=self.undo).pack(side="left")
        tk.Button(options, text="↷ Redo", command=self.redo).pack(side="left", padx=(4, 10))
        tk.Button(options, text="−", command=lambda: self.change_zoom(-1), width=3).pack(side="left")
        tk.Label(options, text="Zoom", padx=4).pack(side="left")
        tk.Label(options, textvariable=self.zoom, width=2).pack(side="left")
        tk.Button(options, text="+", command=lambda: self.change_zoom(1), width=3).pack(side="left", padx=(0, 10))
        tk.Checkbutton(
            options, text="Raster", variable=self.grid_visible, command=self._draw_grid,
        ).pack(side="left")
        tk.Button(options, text="PNG-Referenz laden", command=self.load_reference).pack(side="left", padx=(10, 4))
        tk.Checkbutton(
            options, text="Referenz anzeigen", variable=self.reference_visible,
            command=self._toggle_reference,
        ).pack(side="left")
        tk.Label(
            options,
            text="PNG wird auf 128 × 128 gerahmt",
            fg="#555555",
        ).pack(side="left", padx=(10, 0))

        surface = tk.Frame(self.root)
        surface.pack(fill="both", expand=True, padx=8, pady=(0, 5))
        self.canvas = tk.Canvas(surface, bg="white", highlightthickness=1, highlightbackground="#777777")
        xbar = tk.Scrollbar(surface, orient="horizontal", command=self.canvas.xview)
        ybar = tk.Scrollbar(surface, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        surface.grid_rowconfigure(0, weight=1)
        surface.grid_columnconfigure(0, weight=1)
        tk.Label(self.root, textvariable=self.status, anchor="w", padx=8, pady=6).pack(fill="x")

        self.canvas.bind("<ButtonPress-1>", self._press)
        self.canvas.bind("<B1-Motion>", self._drag)
        self.canvas.bind("<Motion>", self._motion)
        self.canvas.bind("<Leave>", lambda _event: self._clear_preview())
        self.canvas.bind("<Configure>", self._center_surface)
        self.canvas.bind("<FocusOut>", self._cancel_drag, add="+")
        self.root.bind_all("<ButtonRelease-1>", self._release, add="+")

    def _bind_shortcuts(self):
        self.root.bind("<Control-z>", lambda _event: self.undo())
        self.root.bind("<Control-y>", lambda _event: self.redo())
        self.root.bind("<Control-Shift-Z>", lambda _event: self.redo())
        self.root.bind("<Escape>", self._cancel_drag)
        self.root.bind("b", lambda _event: self.tool.set("brush"))
        self.root.bind("f", lambda _event: self.tool.set("fill"))
        self.root.bind("i", lambda _event: self.tool.set("eyedropper"))
        for size in BRUSH_SIZES:
            self.root.bind(str(size), lambda _event, value=size: self.brush_size.set(value))

    def _logical_point(self, event):
        zoom = self.zoom.get()
        return self.canvas.canvasx(event.x) / zoom, self.canvas.canvasy(event.y) / zoom

    def _cell_from_event(self, event):
        u, v = self._logical_point(event)
        x, y = int(u), int(v)
        return (x, y) if 0 <= x < WIDTH and 0 <= y < HEIGHT else None

    def _rebuild_canvas(self):
        self.canvas.delete("all")
        zoom = self.zoom.get()
        extent = WIDTH * zoom
        self.canvas.configure(scrollregion=(0, 0, extent, extent))
        self.reference_item = self.canvas.create_image(0, 0, anchor="nw", state="hidden")
        self.cell_items = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                color = self.model.color_at(x, y)
                fill = "" if self.reference_visible.get() and color == BACKGROUND else color
                self.cell_items.append(self.canvas.create_rectangle(
                    x * zoom, y * zoom, (x + 1) * zoom, (y + 1) * zoom,
                    fill=fill, outline="",
                ))
        self.rendered_cells = bytearray(self.model.cells)
        self._refresh_reference_image()
        self._draw_grid()
        self.root.after_idle(self._center_surface)

    def _center_surface(self, event=None):
        """Center the finite drawing whenever it fits in the viewport."""
        extent = WIDTH * self.zoom.get()
        viewport_width = event.width if event is not None else self.canvas.winfo_width()
        viewport_height = event.height if event is not None else self.canvas.winfo_height()
        pad_x = max(0, round((viewport_width - extent) / 2))
        pad_y = max(0, round((viewport_height - extent) / 2))
        self.canvas.configure(scrollregion=(-pad_x, -pad_y, extent + pad_x, extent + pad_y))
        if pad_x:
            self.canvas.xview_moveto(0)
        if pad_y:
            self.canvas.yview_moveto(0)

    def _draw_grid(self):
        for item in self.grid_items:
            self.canvas.delete(item)
        self.grid_items.clear()
        if not self.grid_visible.get():
            return
        zoom = self.zoom.get()
        extent = WIDTH * zoom
        color = "#B8B8B8" if zoom >= 4 else "#D8D8D8"
        for value in range(WIDTH + 1):
            position = value * zoom
            self.grid_items.append(self.canvas.create_line(position, 0, position, extent, fill=color))
            self.grid_items.append(self.canvas.create_line(0, position, extent, position, fill=color))
        for item in self.preview_items:
            self.canvas.tag_raise(item)

    def _render_changes(self):
        show_reference = self.reference_visible.get() and self.reference_source is not None
        for index, current in enumerate(self.model.cells):
            if current == self.rendered_cells[index]:
                continue
            color = self.model.palette[current]
            self.canvas.itemconfigure(
                self.cell_items[index],
                fill="" if show_reference and color == BACKGROUND else color,
            )
            self.rendered_cells[index] = current

    def _full_recolor(self):
        show_reference = self.reference_visible.get() and self.reference_source is not None
        for index, current in enumerate(self.model.cells):
            color = self.model.palette[current]
            self.canvas.itemconfigure(
                self.cell_items[index],
                fill="" if show_reference and color == BACKGROUND else color,
            )
        self.rendered_cells = bytearray(self.model.cells)

    def _motion(self, event):
        self._clear_preview()
        if self.tool.get() != "brush":
            return
        u, v = self._logical_point(event)
        zoom = self.zoom.get()
        for x, y in self.model.brush_cells(u, v, self.brush_size.get()):
            self.preview_items.append(self.canvas.create_rectangle(
                x * zoom + 1, y * zoom + 1,
                (x + 1) * zoom - 1, (y + 1) * zoom - 1,
                outline="#E34A33", width=2,
            ))

    def _clear_preview(self):
        for item in self.preview_items:
            self.canvas.delete(item)
        self.preview_items.clear()

    def _press(self, event):
        self.canvas.focus_set()
        point = self._logical_point(event)
        cell = self._cell_from_event(event)
        if cell is None:
            return
        try:
            if self.tool.get() == "brush":
                color_index = self.model.ensure_color(self.apply_color())
                self.dragging = True
                self.last_point = point
                changed = self.model.paint_brush(*point, self.brush_size.get(), color_index)
                self._render_changes()
                self._changed(changed)
            elif self.tool.get() == "fill":
                color_index = self.model.ensure_color(self.apply_color())
                changed = self.model.fill(*cell, color_index)
                self._render_changes()
                self._changed(changed)
            else:
                self.pick_color(*cell)
        except (DrawingFormatError, tk.TclError) as exc:
            self.status.set(str(exc))
            self.root.bell()

    def _drag(self, event):
        if not self.dragging or self.tool.get() != "brush":
            return
        point = self._logical_point(event)
        try:
            color_index = self.model.ensure_color(self.apply_color())
            changed = self.model.paint_path(
                [self.last_point, point], self.brush_size.get(), color_index,
            )
            self.last_point = point
            self._render_changes()
            self._changed(changed)
            self._motion(event)
        except DrawingFormatError as exc:
            self.status.set(str(exc))
            self.dragging = False

    def _release(self, _event=None):
        self.dragging = False
        self.last_point = None

    def _cancel_drag(self, _event=None):
        self._release()
        self._clear_preview()

    def _changed(self, count):
        if count:
            self.status.set(
                f"{count} Zelle(n) geändert · Undo {self.model.undo_count}/20 · noch nicht exportiert"
            )

    def apply_color(self):
        color = normalize_ui_color(self.color.get(), self.root)
        self.model.ensure_color(color)
        self.color.set(color)
        self.color_swatch.configure(bg=color)
        return color

    def choose_color(self):
        try:
            initial = normalize_ui_color(self.color.get(), self.root)
        except DrawingFormatError:
            initial = "#000000"
        dialog = ColorSpectrumDialog(self.root, initial)
        if dialog.result:
            self.color.set(dialog.result)
            self.apply_color()

    def _preview_typed_color(self, _event=None):
        try:
            color = normalize_ui_color(self.color.get(), self.root)
        except DrawingFormatError:
            return
        self.color_swatch.configure(bg=color)

    def _apply_color_from_entry(self, _event=None):
        try:
            color = self.apply_color()
        except DrawingFormatError as exc:
            self.status.set(str(exc))
            self.root.bell()
            return "break"
        self.status.set(f"Zeichenfarbe: {color}")
        return "break"

    def pick_color(self, x, y):
        color = self.model.color_at(x, y)
        if color == BACKGROUND and self.reference_visible.get() and self.reference_source is not None:
            value = self.reference_source.get(x, y)
            if isinstance(value, tuple):
                color = "#{:02X}{:02X}{:02X}".format(*value[:3])
            elif isinstance(value, str) and value.startswith("#"):
                color = value.upper()
        self.color.set(color)
        self.apply_color()
        self.status.set(f"Pipette: {color} aus Zelle {x}, {y}")

    def undo(self):
        change = self.model.undo()
        self._render_changes()
        self.status.set("Letzte Zelländerung zurückgenommen" if change else "Kein weiterer Undo-Schritt")

    def redo(self):
        change = self.model.redo()
        self._render_changes()
        self.status.set("Zelländerung wiederhergestellt" if change else "Kein weiterer Redo-Schritt")

    def change_zoom(self, delta):
        target = min(self.MAX_ZOOM, max(self.MIN_ZOOM, self.zoom.get() + delta))
        if target != self.zoom.get():
            self.zoom.set(target)
            self._rebuild_canvas()
            self.status.set(f"Zoom: {target} Bildschirmpixel je logischer Zelle")

    def load_reference(self):
        path = filedialog.askopenfilename(
            parent=self.root, title="Lokale PNG-Referenz wählen",
            filetypes=(("PNG-Bild", "*.png"),),
        )
        if not path:
            return
        try:
            file_size = Path(path).stat().st_size
            if file_size > self.MAX_REFERENCE_BYTES:
                raise DrawingFormatError("Das PNG ist größer als 32 MB")
            image = tk.PhotoImage(file=path)
            if max(image.width(), image.height()) > self.MAX_REFERENCE_DIMENSION:
                raise DrawingFormatError("PNG-Referenzen dürfen höchstens 4096 × 4096 Pixel groß sein")
        except (OSError, tk.TclError, DrawingFormatError) as exc:
            messagebox.showerror("PNG-Referenz", str(exc), parent=self.root)
            return
        dialog = ReferenceFrameDialog(
            self.root, image, Path(path).name,
            replaces_existing=any(self.model.cells),
        )
        if dialog.result is None:
            return
        self.reference_original = image
        self.reference_source = dialog.result
        self.reference_path = Path(path)
        if dialog.trace_model is not None:
            self.model = dialog.trace_model
            self.reference_visible.set(False)
            self._rebuild_canvas()
            self.status.set(
                f"Referenz mit {len(self.model.palette)} Farben nachgezeichnet: "
                f"{self.reference_path.name}"
            )
        else:
            self.reference_visible.set(True)
            self._refresh_reference_image()
            self._full_recolor()
            self.status.set(
                f"Referenz geladen und auf 128 × 128 gerahmt: {self.reference_path.name}"
            )

    def _refresh_reference_image(self):
        if self.reference_source is None:
            self.canvas.itemconfigure(self.reference_item, state="hidden", image="")
            return
        zoom = self.zoom.get()
        self.reference_scaled = self.reference_source.zoom(zoom, zoom)
        self.canvas.itemconfigure(
            self.reference_item,
            image=self.reference_scaled,
            state="normal" if self.reference_visible.get() else "hidden",
        )
        self.canvas.tag_lower(self.reference_item)

    def _toggle_reference(self):
        if self.reference_source is None:
            self.reference_visible.set(False)
        self._refresh_reference_image()
        self._full_recolor()

    def new(self):
        if not messagebox.askyesno("Neue Zeichnung", "Aktuelle Probe verwerfen?", parent=self.root):
            return
        self.model = DrawingModel.blank()
        self._rebuild_canvas()
        self.status.set("Neue leere Zeichnung")

    def open_file(self):
        path = filedialog.askopenfilename(
            parent=self.root, title="Zeichnung öffnen",
            filetypes=(("Glide-Zeichnung", "*.json *.svg"), ("JSON", "*.json"), ("SVG", "*.svg")),
        )
        if not path:
            return
        try:
            content = Path(path).read_bytes()
            if Path(path).suffix.lower() == ".svg":
                imported = import_glide_svg(content)
                model = imported.model
                warning = " · " + "; ".join(imported.warnings) if imported.warnings else ""
            else:
                model = DrawingModel.from_json(content)
                warning = ""
        except (OSError, DrawingFormatError) as exc:
            messagebox.showerror("Zeichnung öffnen", str(exc), parent=self.root)
            return
        self.model = model
        self._rebuild_canvas()
        self.status.set(f"Geöffnet: {Path(path).name}{warning}")

    def save_json(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, title="Zeilenmodell speichern", defaultextension=".json",
            filetypes=(("JSON", "*.json"),),
        )
        if path:
            self._write(path, self.model.to_json() + "\n")

    def save_svg(self):
        path = filedialog.asksaveasfilename(
            parent=self.root, title="Glide-SVG exportieren", defaultextension=".svg",
            filetypes=(("SVG", "*.svg"),),
        )
        if path:
            self._write(path, self.model.to_svg(Path(path).stem))

    def _write(self, path, content):
        try:
            Path(path).write_text(content, encoding="utf-8", newline="\n")
        except OSError as exc:
            messagebox.showerror("Datei speichern", str(exc), parent=self.root)
            return
        self.status.set(f"Exportiert: {Path(path).name}")


def main():
    root = tk.Tk()
    DrawingPrototype(root)
    root.mainloop()


if __name__ == "__main__":
    main()
