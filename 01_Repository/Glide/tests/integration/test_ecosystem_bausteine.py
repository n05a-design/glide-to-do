# SPDX-License-Identifier: MPL-2.0
"""Ecosystem E03–E05: Softwarekatalog, Marketing, Symbole, Diagramme, Caches, Hintergrund (T378).

Ohne Glide-Fachmodule; nur `glide_shell` und `glide_bento`. Prüft Verträge und
Randfälle: Katalog nur mit bekannten Angaben, Links nur über den Host-Öffner,
Symbolanbieter, Favoriten, Auswahl per Tastatur, unsichere SVG/PNG abgewiesen,
Diagramme mit leeren, einzelnen, fehlenden, negativen, gleichen und großen
Werten sowie langen Beschriftungen in Hell und Dunkel, Auswahl und Tastatur,
Zoom/Pan, gebündeltes Neuzeichnen, begrenzter Cache, Hintergrundaufträge mit
veralteten, abgebrochenen und fehlerhaften Ergebnissen und Abbau ohne offene Zeitgeber.
"""
import sys
import threading
import time
import tkinter as tk
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
from glide_shell import background, color_roles, resources, software_catalog, symbol_picker, symbols, window_lifetime
import glide_bento as b
from glide_bento import charts as c, data as bd, marketing as m

assert not any(n in sys.modules for n in ("app", "ui_design", "i18n", "planning")), "Glide-Fachmodul geladen"
schritte = []


def pump(root, n=4):
    for _ in range(n):
        root.update_idletasks()
        root.update()


# --- Katalog ---------------------------------------------------------------------------------------------
katalog = software_catalog.load_ecosystem()
assert not katalog.problems, katalog.problems
assert {p.id for p in katalog.products()} == {"glide", "steps", "chess-and-chains"}
steps = katalog.get("steps")
assert steps.known("platforms") is None, "unbekannte Plattformen dürfen nicht erfunden werden"
assert all(software_catalog.validate_url(u) for p in katalog.products() for u in p.links.values())
kaputt = software_catalog.parse({"format": "glide-software-catalog", "version": 1, "products": [
    {"id": "x1", "name": "X", "links": {"website": "http://unsicher.example", "repository": "javascript:alert(1)"},
     "brand_color": "rot", "status": "geheim"}, {"id": "Ungültig!", "name": "Y"}, {"id": "x1", "name": "Doppelt"}]})
assert len(kaputt) == 1 and not kaputt.get("x1").links and kaputt.get("x1").status == "unknown" and len(kaputt.problems) >= 5
assert software_catalog.parse({"format": "glide-software-catalog", "version": 99}).problems
geoeffnet = []
assert not software_catalog.open_link("file:///etc/passwd", geoeffnet.append) and geoeffnet == []
schritte.append("Katalog: 3 Produkte, unsichere Links/Farben/Status abgewiesen, Links nur per Öffner")

# --- Symbole (Tk-frei) ---------------------------------------------------------------------------------------
gute_svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><rect width="16" height="16" fill="#123456"/></svg>'
assert symbols.inspect_svg(gute_svg)[0]
for boese in (b'<!DOCTYPE svg [<!ENTITY x "y">]><svg/>', b'<svg><script>alert(1)</script></svg>',
              b'<svg onload="x()"/>', b'<svg xmlns:xlink="http://www.w3.org/1999/xlink"><image xlink:href="https://e.example/a.png"/></svg>',
              b'<svg><foreignObject/></svg>', b'<svg><rect style="fill:url(https://e.example/x)"/></svg>', b"<html/>", b"<svg"):
    assert not symbols.inspect_svg(boese)[0], boese
png = b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + (16).to_bytes(4, "big") * 2 + b"\x08\x06\x00\x00\x00"
assert symbols.inspect_png(png)[0] and not symbols.inspect_png(b"GIF89a")[0]
assert not symbols.inspect_png(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + (99999).to_bytes(4, "big") * 2)[0]
reg = symbols.SymbolRegistry({
    "sys": lambda: [symbols.Symbol(f"sys:{n}", n.title(), "Allgemein", "system", "glyph", license="MPL-2.0", resource=g)
                    for n, g in (("stern", "★"), ("herz", "♥"), ("pfeil", "→"))],
    "kaputt": lambda: 1 / 0,
    "ohne": lambda: [symbols.Symbol("ohne:x", "X", "Y", "system", "glyph")]})
assert len(reg) == 3 and any("provider failed" in p for p in reg.problems) and any("without licence" in p for p in reg.problems)
assert [s.id for s in reg.search("herz")] == ["sys:herz"]
zustand = symbols.SymbolState()
zustand.toggle_favorite("sys:stern")
schritte.append("Symbole: sichere SVG/PNG-Prüfung (8 Angriffsmuster abgewiesen), Anbieter, Lizenzpflicht, Suche")

# --- Cache ---------------------------------------------------------------------------------------------------
cache = resources.BoundedCache("probe", max_entries=3, max_cost=10, cost=len)
for k in "abcd":
    cache.put(k, "xx")
assert "a" not in cache and len(cache) == 3 and cache.stats()["evictions"] == 1
cache.get("b"); cache.get("zz")
assert cache.stats()["hits"] == 1 and cache.stats()["misses"] == 1
cache.put("gross", "x" * 50)
assert "gross" not in cache, "Eintrag über dem Budget darf nicht gehalten werden"
assert cache.invalidate(lambda k: k in ("b", "c")) == 2
schritte.append("Cache: Anzahl- und Kostenbudget, LRU, Statistik, Invalidierung")

root = tk.Tk()
root.geometry("900x700+20+20")
fehler = []
root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
themen = {}
for modus in ("light", "dark"):
    themen[modus] = color_roles.with_accent(color_roles.neutral_theme(modus), "#0F766E")

# --- Marketing -------------------------------------------------------------------------------------------------
for modus, roles in themen.items():
    ctx = b.BentoContext.for_host(theme_provider=lambda r=roles: r)
    portfolio = m.PortfolioView(root, ctx, katalog, current_id="glide", language="de", on_link=geoeffnet.append)
    portfolio.pack(fill="both", expand=True)
    pump(root)
    assert set(portfolio.cards) == {"steps", "chess-and-chains"}, "„Weitere Programme“ ohne die eigene App"
    karte = portfolio.cards["steps"]
    assert karte.link_targets and geoeffnet == []
    karte.actions.buttons[0].invoke()
    assert geoeffnet == [karte.link_targets[0]], geoeffnet
    geoeffnet.clear()
    portfolio.destroy()
assert m.monogram("Chess & Chains") == "CC"
schritte.append("Marketing: Portfolio ohne eigene App, Links erst nach Klick, hell/dunkel")

# --- Symbolauswahl ----------------------------------------------------------------------------------------------
bilder = []


def zeichnen(symbol, groesse, roles):
    bild = tk.PhotoImage(master=root, width=groesse, height=groesse)
    bild.put(roles["text"], to=(2, 2, groesse - 2, groesse - 2))
    bilder.append(bild)
    return bild


auswahl = symbol_picker.SymbolPicker(root, reg, themen["light"], zeichnen, state=zustand, title="Symbole")
pump(root)
auswahl.set_category(symbol_picker.FAVORITES)
assert auswahl.order == ["sys:stern"]
auswahl.set_category(symbol_picker.ALL)
auswahl.move(1)  # entspricht der Bindung <Right>
auswahl.move(1)
assert auswahl.selected == "sys:pfeil", auswahl.selected
erzeugt = len(bilder)
auswahl.fill()
assert len(bilder) - erzeugt <= 1, "Raster muss Bilder aus dem Cache wiederverwenden"
assert auswahl.choose(auswahl.selected) == "sys:pfeil" and zustand.recent[0] == "sys:pfeil"
assert not auswahl.dialog.winfo_exists()
leer = symbol_picker.SymbolPicker(root, reg, themen["dark"], lambda *_a: None, title="Leer")
leer.search.set("gibt es nicht")
leer.search.flush()
assert leer.order == []
leer.close()
schritte.append("Symbolauswahl: Favoriten, Tastatur, Cache-Wiederverwendung, Zuletzt verwendet, Leerzustand, Rückfalltext")

# --- Diagramme -------------------------------------------------------------------------------------------------
lang = "Eine sehr lange Beschriftung, die nicht in eine Achse passt"
faelle = {
    "leer": [bd.series("e", "Leer", [])],
    "einzeln": [bd.series("s", "Eins", [("A", 5)])],
    "fehlend": [bd.series("f", "Lücken", [("A", 3), ("B", None), ("C", 4), (lang, None), ("E", 2)])],
    "negativ": [bd.series("n", "Saldo", [("A", -4), ("B", 6), ("C", -1)])],
    "gleich": [bd.series("g", "Gleich", [("A", 7), ("B", 7)])],
    "gross": [bd.series("x", "Groß", [(f"P{i}", (i * 37) % 1000 * 1e6) for i in range(200)])],
    "viele": [bd.series(f"r{k}", f"Reihe {k}", [(f"T{i}", (i + k) % 9) for i in range(12)]) for k in range(9)],
    "ungueltig": [bd.series("u", "Ungültig", [("A", float("nan")), ("B", "x"), ("C", 1)])],
}
assert faelle["ungueltig"][0].missing == 2 and len(faelle["ungueltig"][0].problems) == 2
assert faelle["fehlend"][0].values()[1] is None, "fehlende Werte dürfen nicht null werden"
assert bd.extent(faelle["leer"]) is None and bd.nice_ticks(0, 1e9)[-1] >= 1e9
gebaut = 0
for modus, roles in themen.items():
    ctx = b.BentoContext.for_host(theme_provider=lambda r=roles: r)
    flaeche = tk.Frame(root)
    flaeche.pack(fill="both", expand=True)
    for name, reihen in faelle.items():
        for chart in (c.BarChart(flaeche, reihen, context=ctx), c.BarChart(flaeche, reihen, context=ctx, orientation="horizontal", mode="stacked"),
                      c.LineChart(flaeche, reihen, context=ctx, area=True), c.PieChart(flaeche, reihen[0], context=ctx, donut=True),
                      c.Sparkline(flaeche, reihen[0], context=ctx), c.RadarChart(flaeche, reihen, context=ctx)):
            chart.pack(fill="x")
            gebaut += 1
    pump(root)
    for widget in flaeche.winfo_children():
        widget.draw()
    flaeche.destroy()
    pump(root)
schritte.append(f"Diagramme: {gebaut} Darstellungen mit leeren, einzelnen, fehlenden, negativen, gleichen, großen, vielen und ungültigen Daten (hell/dunkel)")

ctx = b.BentoContext.for_host(theme_provider=lambda: themen["light"])
gewaehlt = []
balken = c.BarChart(root, faelle["fehlend"], context=ctx, on_select=gewaehlt.append, width=500)
balken.pack()
pump(root)
assert balken.elements() == ["f:0", "f:2", "f:4"], balken.elements()
balken.focus_force()
balken.move_selection(1)
balken.select(balken.selected)
assert gewaehlt == ["f:0"], gewaehlt
pump(root)  # Fokus- und Auswahlereignisse abarbeiten, bevor gezählt wird
vorher = balken.redraws
for _ in range(20):
    balken.schedule_draw()
pump(root)
assert balken.redraws - vorher == 1, f"20 Anforderungen müssen zu genau einem Neuzeichnen führen ({balken.redraws - vorher})"
linie = c.LineChart(root, faelle["gross"], context=ctx, width=500)
linie.pack()
pump(root)
linie._zoom(1, 250)
assert linie.view is not None and linie.view[1] - linie.view[0] < 199
fenster = linie.view
linie._pan(type("E", (), {"x": 300})())
linie._pan(type("E", (), {"x": 200})())
assert linie.view != fenster or fenster[1] == 199
linie.reset_view()
assert linie.view is None
linie.destroy()
heat = c.CalendarHeatmap(root, {"2026-11-02": 3, "2026-11-03": None, "2026-11-10": 1}, context=ctx)
heat.pack(fill="x")
zeit = c.Timeline(root, [bd.Span("a", "Planung", 0, 5, "Team A"), bd.Span("m", "Abnahme", 7, None, "Team B")], context=ctx)
zeit.pack(fill="x")
graph = c.GraphChart(root, [bd.Node("r", "Wurzel"), bd.Node("k1", "Kind 1", "r"), bd.Node("k2", "Kind 2", "r")],
                     [bd.Edge("k1", "k2"), bd.Edge("k2", "k1")], context=ctx)
graph.pack(fill="x")
pump(root)
assert set(graph.elements()) == {"r", "k1", "k2"} and graph.problems, "Zyklus muss gemeldet werden"
tabelle = c.BentoTable(root, ctx, [("name", "Name", "text"), ("wert", "Wert", "number")],
                       [{"id": "a", "name": "B", "wert": 2}, {"id": "b", "name": "A", "wert": None}, {"id": "c", "name": "C", "wert": 1}])
tabelle.pack()
tabelle.sort_by("wert")
assert [z["id"] for z in tabelle.sorted_rows()] == ["c", "a", "b"], "fehlende Werte stehen am Ende"
tabelle.sort_by("wert")
assert [z["id"] for z in tabelle.sorted_rows()] == ["a", "c", "b"]
for widget in (c.ProgressBar(root, 0.4, segments=5, target=0.8, context=ctx), c.ProgressBar(root, None, context=ctx),
               c.RadialProgress(root, 3, 4, semicircle=True, context=ctx), c.MultiProgress(root, [("x", "X", 2, 4), ("y", "Y", None, 4)], context=ctx),
               c.Badge(root, ctx, "Neu"), c.StatusDot(root, ctx, "warning", "Prüfen"),
               c.MetricTrend(root, ctx, "Offen", 12, previous=15, higher_is_better=False, trend=faelle["fehlend"][0])):
    widget.pack(fill="x")
pump(root)
schritte.append("Interaktion: Auswahl, Tastatur, 20 Anforderungen → 1 Neuzeichnen, Zoom/Pan, Kalender, Zeitachse, Graph mit Zyklus, sortierbare Tabelle, Fortschritt, Trend")

# --- Hintergrund ---------------------------------------------------------------------------------------------------
besitzer = tk.Frame(root)
besitzer.pack()
q = background.TaskQueue(besitzer, workers=2, max_pending=4, poll_ms=5)
ergebnisse, fehlerliste = [], []
tor = threading.Event()
haupt = threading.get_ident()
q.submit(lambda: (tor.wait(2), threading.get_ident())[1], on_done=lambda r: ergebnisse.append(("thread", r != haupt, threading.get_ident() == haupt)))
alt = q.submit(lambda: "alt", on_done=ergebnisse.append, key="suche")
neu = q.submit(lambda: "neu", on_done=ergebnisse.append, key="suche")
q.submit(lambda: 1 / 0, on_error=lambda e: fehlerliste.append(type(e).__name__))
tor.set()
ende = time.time() + 5
while time.time() < ende and len(ergebnisse) + len(fehlerliste) < 3:
    root.update()
    time.sleep(0.01)
assert ("thread", True, True) in ergebnisse, ergebnisse
assert "neu" in ergebnisse and "alt" not in ergebnisse and alt.state == "stale", (ergebnisse, alt.state)
assert fehlerliste == ["ZeroDivisionError"]
for _ in range(8):
    q.submit(time.sleep, 0.05)
assert q.stats()["refused"] >= 1, "volle Warteschlange muss ablehnen"
spaet = []
q.submit(lambda: "spät", on_done=spaet.append)
besitzer.destroy()
for _ in range(30):
    root.update()
    time.sleep(0.01)
assert spaet == [] and q.stats()["closed"], "nach dem Abbau keine Zustellung"
schritte.append("Hintergrund: Ergebnis im Tk-Thread, veraltete Ergebnisse verworfen, Fehlerweg, Begrenzung, keine Zustellung nach Abbau")

for w in list(root.winfo_children()):
    w.destroy()
pump(root)
assert not fehler, fehler
root.destroy()
print("test_ecosystem_bausteine: OK – " + "; ".join(schritte) + " (Windows-Tk, künstliche Daten)")
