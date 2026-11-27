# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 18: component showcase registry for hosts built on the shell (Shell 0.7.0).

Tk-free at import. Every framework describes its own reusable components as
`ShowcaseEntry` objects; a host collects them in a `ShowcaseRegistry` and shows
them in its gallery. A host therefore needs no copy of a component to show it:
each entry's `build(master, env)` creates the real component from its package.

`ShowcaseEnv` carries the host's colour dictionary `palette` (roles such as `bg`, `card`,
`text`, `muted`, `input`, `input_border`, `selection`, `ui_accent`), a font
callable `font(size, weight)` and free `extra` values (for example a Bento
context). Builders read colours only from `env.palette`, so a theme change is a
rebuild with a new env.

`ShowcaseRegistry.coverage(expected)` names the expected component ids that
have no entry, `problems()` names entries without a builder or productive
usage note. A host test uses both to prove that no component is left out.

All texts in entries are English developer descriptions (D96); a host may show
them as they are or translate them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class ShowcaseEnv:
    palette: dict
    font: Callable[..., Any]
    extra: dict = field(default_factory=dict)

    def color(self, role, fallback="#808080"):
        return self.palette.get(role, fallback)


@dataclass(frozen=True)
class ShowcaseEntry:
    id: str
    name: str
    framework: str
    version: str
    module: str
    summary: str
    states: tuple = ()
    sizes: tuple = ()
    theming: str = ""
    limits: str = ""
    used_in: tuple = ()  # filled by the host: where the component works productively
    build: Callable[[Any, ShowcaseEnv], Any] | None = None

    def __post_init__(self):
        for name in ("id", "name", "framework", "version", "module", "summary"):
            if not str(getattr(self, name) or "").strip():
                raise ValueError(f"ShowcaseEntry.{name} must not be empty")


class ShowcaseRegistry:
    def __init__(self, entries: Iterable[ShowcaseEntry] = ()):
        self._entries: dict[str, ShowcaseEntry] = {}
        for entry in entries:
            self.register(entry)

    def register(self, entry):
        if not isinstance(entry, ShowcaseEntry):
            raise TypeError("only ShowcaseEntry objects can be registered")
        if entry.id in self._entries:
            raise ValueError(f"duplicate showcase id {entry.id!r}")
        self._entries[entry.id] = entry
        return entry

    def extend(self, entries):
        for entry in entries:
            self.register(entry)
        return self

    def entries(self, framework=None):
        return [e for e in self._entries.values() if framework is None or e.framework == framework]

    def frameworks(self):
        return list(dict.fromkeys(e.framework for e in self._entries.values()))

    def get(self, entry_id):
        return self._entries[entry_id]

    def coverage(self, expected):
        """Expected component ids without an entry, in the given order."""
        return [name for name in expected if name not in self._entries]

    def problems(self):
        """Entries that cannot be demonstrated or have no productive usage note."""
        result = []
        for entry in self._entries.values():
            if entry.build is None:
                result.append(f"{entry.id}: no builder")
            if not entry.used_in:
                result.append(f"{entry.id}: no productive usage noted (write 'gallery only' explicitly)")
        return result

    def __len__(self):
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries.values())


# Components of `custom_controls` and Tk-free helpers that a gallery can show.
SHELL_COMPONENTS = ("shell.canvas_label", "shell.checkbutton", "shell.radiobutton", "shell.listbox",
                    "shell.scale", "shell.auto_scrollbar", "shell.text_fit", "shell.spellcheck",
                    "shell.action_handle", "shell.drop_indicator")


def _build_label(master, env):
    from glide_shell.custom_controls import CanvasLabel
    return CanvasLabel(master, text="Canvas label · sample text", font=env.font(11),
                       fg=env.color("text"), bg=env.color("card"), anchor="w")


def _build_checks(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import GlideCheckbutton
    rahmen = tk.Frame(master, bg=env.color("card"))
    for text, wert, zustand in (("Enabled, on", True, "normal"), ("Enabled, off", False, "normal"),
                                ("Disabled", True, "disabled")):
        variable = tk.BooleanVar(master=master, value=wert)
        knopf = GlideCheckbutton(rahmen, text=text, variable=variable, bg=env.color("card"), fg=env.color("text"),
                                 selectcolor=env.color("input"), font=env.font(10), anchor="w")
        knopf._showcase_variable = variable
        if zustand == "disabled":
            knopf.configure(state="disabled")
        knopf.pack(fill="x", pady=1)
    return rahmen


def _build_radios(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import GlideRadiobutton
    rahmen = tk.Frame(master, bg=env.color("card"))
    variable = tk.StringVar(master=master, value="a")
    rahmen._showcase_variable = variable
    for text, wert in (("Option A", "a"), ("Option B", "b"), ("Option C", "c")):
        GlideRadiobutton(rahmen, text=text, variable=variable, value=wert, bg=env.color("card"),
                         fg=env.color("text"), selectcolor=env.color("input"), font=env.font(10),
                         anchor="w").pack(fill="x", pady=1)
    return rahmen


def _build_listbox(master, env):
    from glide_shell.custom_controls import GlideListbox
    liste = GlideListbox(master, height=4, width=28, bg=env.color("input"), fg=env.color("text"),
                         selectbackground=env.color("selection"), selectforeground=env.color("text"),
                         font=env.font(10))
    liste.insert("end", "Sample row 1", "Sample row 2", "Sample row 3", "Sample row 4", "Sample row 5")
    liste.selection_set(1)
    return liste


def _build_scale(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import GlideScale
    variable = tk.IntVar(master=master, value=40)
    regler = GlideScale(master, from_=0, to=100, resolution=1, orient="horizontal", showvalue=False,
                        length=240, variable=variable, bg=env.color("selection"), fg=env.color("text"),
                        troughcolor=env.color("input_border"), width=12, sliderlength=22,
                        highlightthickness=0, bd=0, sliderrelief="flat", activebackground=env.color("selection"))
    regler._showcase_variable = variable
    return regler


def _build_scrollbar(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import ThemedAutoScrollbar
    rahmen = tk.Frame(master, bg=env.color("card"))
    text = tk.Text(rahmen, height=4, width=32, bg=env.color("input"), fg=env.color("text"), relief="flat",
                   bd=0, highlightthickness=0, font=env.font(10))
    leiste = ThemedAutoScrollbar(rahmen, bg_color=env.color("card"), track_color=env.color("card"),
                                 thumb_color=env.color("input_border"), active_thumb_color=env.color("muted"),
                                 width=10, radius=5)
    text.configure(yscrollcommand=leiste.set)
    leiste.set_command(text.yview)
    text.insert("1.0", "\n".join(f"Sample line {n}" for n in range(1, 13)))
    text.pack(side="left", fill="both", expand=True)
    leiste.pack(side="right", fill="y")
    return rahmen


def _build_text_fit(master, env):
    import tkinter as tk
    import tkinter.font as tkfont
    from glide_shell.text_fit import fit
    rahmen = tk.Frame(master, bg=env.color("card"))
    schrift = env.font(10)
    messung = tkfont.Font(root=master, font=schrift) if not isinstance(schrift, tkfont.Font) else schrift
    satz = "A long sample title that does not fit into a narrow column"
    for breite in (320, 200, 120):
        tk.Label(rahmen, text=f"{breite:>3} px  {fit(satz, messung.measure, breite)}", bg=env.color("card"),
                 fg=env.color("text"), font=schrift, anchor="w").pack(fill="x")
    return rahmen


def _build_spellcheck(master, env):
    import tkinter as tk
    from glide_shell.spellcheck import LayeredChecker, WordListChecker, misspelled
    probe = LayeredChecker(WordListChecker({"en": ["this", "sample", "sentence", "has", "one", "error", "and", "a", "link"]}))
    satz = "This sample sentense has one error and a link https://example.invalid/sentense"
    feld = tk.Text(master, height=2, width=60, bg=env.color("input"), fg=env.color("text"), relief="flat", bd=0,
                   highlightthickness=0, font=env.font(10), wrap="word")
    feld.insert("1.0", satz)
    feld.tag_configure("misspelled", underline=True, foreground=env.color("delete", "#C0392B"))
    for a, b, _wort in misspelled(probe, satz, "en"):
        feld.tag_add("misspelled", f"1.0 + {a} chars", f"1.0 + {b} chars")
    feld._showcase_findings = misspelled(probe, satz, "en")
    feld.configure(state="disabled")
    return feld


def _build_action_handle(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import ActionHandle

    frame = tk.Frame(master, bg=env.color("card"))
    status = tk.Label(frame, text="Open actions", bg=env.color("card"), fg=env.color("text"))
    ActionHandle(frame, glyph="\u283f", background=env.color("card"), foreground=env.color("muted"),
                 hover_background=env.color("hover"), hover_foreground=env.color("text"), font=env.font(12),
                 command=lambda: status.configure(text="Action invoked")).pack(side="left")
    status.pack(side="left", padx=6)
    return frame


def _build_drop_indicator(master, env):
    import tkinter as tk
    from glide_shell.custom_controls import DropIndicator

    frame = tk.Frame(master, bg=env.color("card"), height=108)
    marker = DropIndicator(frame)
    for y, zone in ((4, "before"), (38, "into"), (72, "after")):
        row = tk.Label(frame, bg=env.color("card"), fg=env.color("text"), text=zone, anchor="w", padx=10)
        row.place(x=0, y=y, relwidth=1, height=32)
        row.bind("<Enter>", lambda _event, top=y, z=zone:
                 marker.show((0, top, frame.winfo_width(), 32), z, color=env.color("ui_accent")))
        row.bind("<Leave>", lambda _event, top=y: marker.clear() if not top <= frame.winfo_pointery() - frame.winfo_rooty() < top + 32 else None)
    return frame


def shell_entries(version=None):
    """Showcase entries for the shell's own reusable components."""
    if version is None:
        from glide_shell import SHELL_VERSION as version
    gemeinsam = dict(framework="Glide Shell", version=version)
    return [
        ShowcaseEntry("shell.canvas_label", "CanvasLabel", module="glide_shell.custom_controls",
                      summary="Label drawn on a canvas: exact ink box, theme colours, optional fit to ink.",
                      states=("normal",), sizes=("any font size",), theming="fg/bg from host roles",
                      limits="no text selection", build=_build_label, **gemeinsam),
        ShowcaseEntry("shell.checkbutton", "GlideCheckbutton", module="glide_shell.custom_controls",
                      summary="Themed check box with hover, focus ring and keyboard toggle (space).",
                      states=("on", "off", "hover", "focus", "disabled"), sizes=("10–14 pt",),
                      theming="bg, text, input", limits="", build=_build_checks, **gemeinsam),
        ShowcaseEntry("shell.radiobutton", "GlideRadiobutton", module="glide_shell.custom_controls",
                      summary="Themed radio button sharing one variable; arrow keys move the choice.",
                      states=("selected", "unselected", "hover", "focus", "disabled"), sizes=("10–14 pt",),
                      theming="bg, text, input", limits="", build=_build_radios, **gemeinsam),
        ShowcaseEntry("shell.listbox", "GlideListbox", module="glide_shell.custom_controls",
                      summary="Listbox replacement with Tk-compatible API (insert, selection, see, yview).",
                      states=("selection", "focus", "scroll"), sizes=("rows × chars",),
                      theming="input, text, selection", limits="single selection mode only in gallery",
                      build=_build_listbox, **gemeinsam),
        ShowcaseEntry("shell.scale", "GlideScale", module="glide_shell.custom_controls",
                      summary="Horizontal or vertical slider bound to a Tk variable.",
                      states=("drag", "hover", "focus", "disabled"), sizes=("length, width",),
                      theming="selection, input_border", limits="", build=_build_scale, **gemeinsam),
        ShowcaseEntry("shell.auto_scrollbar", "ThemedAutoScrollbar", module="glide_shell.custom_controls",
                      summary="Rounded scrollbar that hides itself when everything is visible.",
                      states=("hidden", "visible", "hover", "drag"), sizes=("width, radius",),
                      theming="card, input_border, muted", limits="", build=_build_scrollbar, **gemeinsam),
        ShowcaseEntry("shell.text_fit", "text_fit.fit", module="glide_shell.text_fit",
                      summary="Shortens text to a pixel width with an ellipsis, using the host's measure.",
                      states=("fits", "shortened"), sizes=("any width",), theming="none (pure function)",
                      limits="", build=_build_text_fit, **gemeinsam),
        ShowcaseEntry("shell.action_handle", "ActionHandle", module="glide_shell.custom_controls",
                      summary="An action target with host-controlled menu and drag callbacks.",
                      states=("resting", "hover", "focus"), sizes=("font and padding",),
                      theming="card, muted, hover, text", build=_build_action_handle, **gemeinsam),
        ShowcaseEntry("shell.drop_indicator", "DropIndicator", module="glide_shell.custom_controls",
                      summary="Insertion and container feedback drawn over a target row.",
                      states=("before", "after", "inside", "invalid"), sizes=("host row bounds",),
                      theming="host accent or warning colour", build=_build_drop_indicator, **gemeinsam),
        ShowcaseEntry("shell.spellcheck", "spellcheck", module="glide_shell.spellcheck",
                      summary="Engine-neutral spell-checking contract: word tokens without URLs and code, "
                              "unknown words, suggestions, ignore list and personal dictionary.",
                      states=("unknown word marked", "URL skipped"), sizes=("any text",),
                      theming="host marks findings with its own tag colours",
                      limits="ships no engine or dictionary; gallery uses a tiny sample word list",
                      build=_build_spellcheck, **gemeinsam),
    ]
