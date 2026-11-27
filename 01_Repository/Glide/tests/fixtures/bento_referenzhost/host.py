# SPDX-License-Identifier: MPL-2.0
"""Fremder Host ohne Glide: eigene Tokens/Farben, Multi-Span, Themen- und Sprachwechsel, Abbau."""
import sys, tkinter as tk
import glide_bento as b
assert not any(m in sys.modules for m in ("app", "ui_design", "i18n", "planning")), "Glide-Fachmodul geladen"
TEXTE = {"de": ("Kennzahlen", "Noch nichts da", "Anlegen"), "en": ("Metrics", "Nothing yet", "Create")}
themen = {"hell": {"card": "#FFFFFF", "bg": "#EEF0F4", "text": "#111111", "muted": "#555555", "accent": "#225588"},
          "dunkel": {"card": "#1E1E22", "bg": "#121214", "text": "#EEEEEE", "muted": "#AAAAAA", "accent": "#88AAFF"}}
zustand = {"thema": "hell", "sprache": "de"}
ctx = b.BentoContext.for_host(theme_provider=lambda: themen[zustand["thema"]],
                              token_provider=lambda: {"card_min_width": 260, "gap_relaxed": 12, "card_radius": 10})
root = tk.Tk(); root.geometry("1000x700")
grid = b.BentoGrid(root, context=ctx); grid.pack(fill="both", expand=True)
specs = [b.BentoCardSpec("a", span=2, weight=3), b.BentoCardSpec("b", weight=3), b.BentoCardSpec("c"), b.BentoCardSpec("d")]
karten = {}
def aufbauen():
    t = TEXTE[zustand["sprache"]]
    for s in specs:
        alt = karten.pop(s.key, None)
        if alt: grid.remove_card(s.key); alt.destroy()
        k = b.BentoCard(grid, context=ctx, title=f"{t[0]} {s.key}", spec=s)
        b.BentoEmptyState(k.body, context=ctx, title=t[1], description=t[1], action=(t[2], lambda: None, "accent"),
                          secondary_action=(t[2] + " 2", lambda: None, "muted")).pack(fill="x")
        karten[s.key] = k; grid.add_card(k)
def pump():
    for _ in range(3): root.update()
aufbauen(); pump(); grid.reflow(); pump()
assert grid.current_columns == 3, grid.current_columns
a, bb = karten["a"], karten["b"]
assert a.winfo_rootx() + a.winfo_width() <= bb.winfo_rootx() and a.winfo_width() > bb.winfo_width() * 1.5
for breite, spalten in ((700, 2), (400, 1), (1000, 3)):
    root.geometry(f"{breite}x700"); pump(); grid.reflow(); pump()
    assert grid.current_columns == spalten, (breite, grid.current_columns)
zustand["thema"] = "dunkel"; ctx.refresh_from_host(); grid.update_theme(ctx); pump()
assert grid.cget("bg") == themen["dunkel"]["bg"]
zustand["sprache"] = "en"; aufbauen(); pump(); grid.reflow(); pump()
assert karten["a"].winfo_exists() and len(grid._cards) == 4
grid.schedule_layout(); grid.destroy(); pump()
root.destroy()
print("Referenzhost OK: Multi-Span, Breakpoints, eigene Tokens/Themen, Sprachwechsel, Abbau")
