"""Kontrast: jeder dargestellte Text in jedem Design erreicht WCAG 2.2 AA.

Grenzen: 4,5:1 für normale Schrift, 3:1 für große (ab 18 pt oder 14 pt fett).
Gemessen wird an den tatsächlich dargestellten Elementen, nicht an der
Palette:

- Labels, Kontrollkästchen, Eingabefelder;
- farbige Zeilen der Listen und Tabellen (Tags);
- jede Schaltfläche in allen drei Zuständen (ruhend, beim Überfahren,
  aktiv) – so, wie `RoundedButton` sie zeichnet.

Die erste Messung am 26.09.2026 fand im hellen Design 38 und im Glasdesign
40 Farbpaare unter der Grenze (Grün, Orange und Türkis bei 2,0 bis 2,6:1),
in allen dunklen und bunten Designs weiße Schrift auf hellen Hover-Flächen
(bis 1,3:1) und zu blasse Platzhalter. Seitdem ziehen `legible_text_roles`
die Schriftrollen und `RoundedButton.legible_text` die Knopfschrift nach.
Farbe auf Zeichenflächen (Pinnwandkarten, Kalenderzellen) misst die Suite
nicht; das bleibt Teil der Sichtprüfung.
"""
import collections
import importlib.machinery
import importlib.util
import os
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BEISPIELE = REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"


def nachfahren(widget):
    for kind in widget.winfo_children():
        yield kind
        yield from nachfahren(kind)


with tempfile.TemporaryDirectory(prefix="glide-kontrast-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(BEISPIELE) as z:
        Path(ordner, "liste_speicher.json").write_bytes(z.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_k", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec); loader.exec_module(mod)
    root = mod.tk.Tk(); root.geometry("1280x860+0+30")
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *a, **k: None

    def farbe(w, wert):
        try:
            r, g, b = w.winfo_rgb(wert)
            return f"#{r // 257:02x}{g // 257:02x}{b // 257:02x}"
        except Exception:
            return None

    def gross(fontspec, w):
        try:
            f = mod.tkfont.Font(root=root, font=fontspec)
            groesse = abs(int(f.actual("size")))
            fett = f.actual("weight") == "bold"
            return groesse >= 18 or (groesse >= 14 and fett)
        except Exception:
            return False

    normal = next(e for e in app.lists if e.get("list_kind") in (None, "", "list", "tasks") and len(e.get("items", [])) > 5)
    ansichten = [("Startseite", app.set_home_view), ("Mein Tag", app.set_plan_day_view),
                 ("Labels", app.set_labels_view), ("Bibliothek", app.set_library_view),
                 ("Vorlagen", app.set_template_view), ("Liste", lambda: app.set_active_list(normal["id"])),
                 ("Tabelle", app.set_table_view),
                 ("Pinnwand", lambda: (app.set_active_list(normal["id"]), app.workspace.set_mode("board"))),
                 ("zurück", lambda: app.workspace.set_mode("list"))]
    nur = list(app.DESIGN_ORDER)
    gesamt, gepruefte_paare = [], 0
    for design in nur:
        app.set_design(design); app.apply_theme(); root.update()
        befunde = collections.OrderedDict()
        for name, oeffnen in ansichten:
            oeffnen()
            for _ in range(3): root.update()
            for w in nachfahren(root):
                try:
                    if not w.winfo_ismapped():
                        continue
                    art = w.winfo_class()
                    paare = []
                    if isinstance(w, mod.RoundedButton):
                        if not w.text.strip():
                            continue
                        for zustand in ("ruhend", "hover", "aktiv"):
                            flaeche, schrift = w.state_colors(zustand)
                            paare.append((f"Knopf/{zustand}", w.text, schrift, flaeche, w.font))
                    elif isinstance(w, mod.CanvasLabel):
                        text = str(w.cget("text")).strip()
                        if not text:
                            continue
                        paare.append(("Beschriftung", text, w.cget("fg"), w.cget("bg"), w.cget("font")))
                    elif art in ("Label", "Checkbutton", "Radiobutton", "Button"):
                        text = str(w.cget("text")).strip()
                        if not text:
                            continue
                        paare.append((art, text, w.cget("fg"), w.cget("bg"), w.cget("font")))
                    elif art == "Entry":
                        paare.append(("Eingabe", str(w.get())[:20] or "(leer)", w.cget("fg"), w.cget("bg"), w.cget("font")))
                    elif art == "Treeview":
                        stil = w.cget("style") or "Treeview"
                        grund = mod.ttk.Style().lookup(stil, "background") or mod.ttk.Style().lookup("Treeview", "background")
                        schrift = mod.ttk.Style().lookup(stil, "font") or "TkDefaultFont"
                        for tag in (set(t for iid in w.get_children("") for t in w.item(iid, "tags")) - {"spacer", "empty"}) | {""}:
                            if tag:
                                vg = w.tag_configure(tag, "foreground") or mod.ttk.Style().lookup(stil, "foreground")
                                hg = w.tag_configure(tag, "background") or grund
                            else:
                                vg, hg = mod.ttk.Style().lookup(stil, "foreground"), grund
                            if vg and hg:
                                paare.append((f"Zeile:{tag or 'normal'}", tag, vg, hg, w.tag_configure(tag, "font") if tag else schrift))
                    gepruefte_paare += len(paare)
                    for rolle, text, vg, hg, fontspec in paare:
                        a, b = farbe(w, vg), farbe(w, hg)
                        if not a or not b:
                            continue
                        wert = mod.contrast_ratio(a, b)
                        grenze = 3.0 if gross(fontspec, w) else 4.5
                        if wert < grenze:
                            schluessel = (rolle, a, b)
                            befunde.setdefault(schluessel, (wert, grenze, name, str(text)[:28]))
                except (mod.tk.TclError, ValueError):
                    continue
        gesamt.extend(f"{design}: {wert:.2f} < {grenze} {rolle} {a} auf {b} „{text}“ ({ansicht})"
                      for (rolle, a, b), (wert, grenze, ansicht, text) in befunde.items())
    root.destroy()
    assert not gesamt, gesamt[:8]
    assert gepruefte_paare > 5000, gepruefte_paare

print(f"test_kontrast330: OK; {len(nur)} Designs, {gepruefte_paare} Schrift-Flächen-Paare in "
      f"{len(ansichten)} Ansichten, keines unter WCAG AA.")
