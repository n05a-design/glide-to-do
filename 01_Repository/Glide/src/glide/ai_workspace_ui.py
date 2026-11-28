# SPDX-License-Identifier: MPL-2.0
"""Oberflächen des KI-Arbeitsbereichs (Teil 06): Prompt-Bibliothek, Prompt-Editor,
Projekt- und Agentenprofile, Kontextbibliothek, Export/Übergabe, Berichte und
Dokumentenbibliothek.

Nutzt ausschließlich vorhandene Glide-Bausteine (Dialogfabrik, Dialogknöpfe,
Bento-Karten, Seiteneditor für den Freitext, Auswahl- und Eingabedialoge).
Fachlogik liegt Tk-frei in `ai_workspace`. Keine Netzwerkzugriffe: „Anbieter
öffnen“ öffnet nur auf Klick eine Website im Browser und überträgt nichts.
"""
from __future__ import annotations

import json
import os
import tkinter as tk
from tkinter import filedialog, ttk
import webbrowser

import ai_workspace as aw
import glide_bento


def SearchField(*args, **kwargs):  # noqa: N802 – erst beim Öffnen der Bibliothek laden (E05)
    from glide_shell.controls import SearchField as _SearchField
    return _SearchField(*args, **kwargs)
import i18n as glide_i18n

_H = {}


def install(**host):
    """Vom Host gesetzte Bausteine: app_font, ButtonFlow, modal."""
    _H.update(host)


def T(key, de, **kw):
    return glide_i18n.t("ai." + key, de, **kw)


def lang():
    return "en" if glide_i18n.get_language() == "en" else "de"


STATUS_DE = {"draft": "Entwurf", "prepared": "Vorbereitet", "handed_over": "Als übergeben markiert",
             "in_progress": "In Bearbeitung (manuell gesetzt)", "result_received": "Ergebnis erhalten",
             "in_review": "In Prüfung", "done": "Abgeschlossen", "blocked": "Blockiert", "archived": "Archiviert"}


def status_label(key):
    return T(f"status.{key}", STATUS_DE[key])


PROVIDERS = (("ChatGPT", "https://chatgpt.com/"), ("Claude", "https://claude.ai/"), ("Gemini", "https://gemini.google.com/"),
             ("GitHub Copilot", "https://github.com/copilot"), ("Codex", "https://chatgpt.com/codex"))


# --- gemeinsame Hilfen -------------------------------------------------------------
def font(size=10, weight="normal"):
    return _H["app_font"](size, weight)


def dialog(app, title, size="980x720"):
    d = _H["modal"].create_dialog(app.root, title, transient=False)
    d.geometry(size)
    d.minsize(640, 460)
    d.configure(bg=app.theme["bg"])
    return d


def button(app, master, text, command, role="muted"):
    return app._make_dialog_button(master, text, command, role,
                                   width=max(110, font(10, "bold").measure(text) + 40) if hasattr(font(10, "bold"), "measure") else 140,
                                   height=34)


def flow(app, master):
    return _H["ButtonFlow"](master, bg=app.theme["bg"])


def label(app, master, text, muted=False, size=10, bold=False, wrap=0, bg=None):
    return tk.Label(master, text=text, bg=bg or app.theme["bg"], fg=app.theme["muted" if muted else "text"],
                    font=font(size, "bold" if bold else "normal"), anchor="w", justify="left", wraplength=wrap)


def text_field(app, master, height=2, value=""):
    t = tk.Text(master, height=height, wrap="word", font=font(10), bg=app.theme["card"], fg=app.theme["text"],
                insertbackground=app.theme["text"], relief="flat", padx=8, pady=6, highlightthickness=1,
                highlightbackground=app.theme["line"], highlightcolor=app.theme["ui_accent"], undo=True)
    t.insert("1.0", value)
    return t


def scroll_area(app, master):
    rahmen = tk.Frame(master, bg=app.theme["bg"])
    leinwand = tk.Canvas(rahmen, bg=app.theme["bg"], highlightthickness=0, bd=0)
    innen = tk.Frame(leinwand, bg=app.theme["bg"])
    fenster = leinwand.create_window(0, 0, anchor="nw", window=innen)
    leiste = app._dialog_scrollbar(rahmen, compact=True)
    leiste.set_command(leinwand.yview)
    leinwand.configure(yscrollcommand=leiste.set)
    leiste.pack(side="right", fill="y")
    leinwand.pack(side="left", fill="both", expand=True)
    innen.bind("<Configure>", lambda _e: leinwand.configure(scrollregion=leinwand.bbox("all")))
    leinwand.bind("<Configure>", lambda e: leinwand.itemconfigure(fenster, width=e.width))
    app.bind_mousewheel(leinwand) if hasattr(app, "bind_mousewheel") else None
    return rahmen, innen


def page_title(app, list_id):
    e = next((x for x in app.lists if x.get("id") == list_id), None)
    return str((e or {}).get("title") or "").strip() or T("untitled", "Ohne Titel")


def page_body(app, list_id):
    e = next((x for x in app.lists if x.get("id") == list_id), None)
    return ((e or {}).get("rich_note") or {}).get("text", "")


def resolver(app):
    """Kontextquellen auflösen: Glide-Seiten/Notizen und Dokumentversionen (nur lokal)."""
    ws = app.ai_workspace()

    def aufloesen(item):
        if item["kind"] == "ref":
            ziel = app.ai_parse_reference(item["id"])
            list_id = ziel[1] if ziel and ziel[0] == "list" else None
            e = next((x for x in app.lists if x.get("id") == list_id), None) if list_id else None
            if e is None:
                return None, None
            return str(e.get("title") or ""), (e.get("rich_note") or {}).get("text", "") or e.get("note", "")
        if item["kind"] == "doc":
            did, _, vid = str(item["id"]).partition("@")
            d = ws.documents.get(did)
            if not d or not d["versions"]:
                return None, None
            v = next((x for x in d["versions"] if x["id"] == vid), d["versions"][-1])
            text = aw.extract_text(app.ai_data_path(v["storage"])) or T("doc_not_text", "[Dokument ohne erschließbaren Text: {name}]", name=v["name"])
            return f"{d['title']} ({v['name']})", text
        return None, None
    return aufloesen


def render(app, list_id, frozen=None, exclude=()):
    ws = app.ai_workspace()
    return ws.render(list_id, page_title(app, list_id), page_body(app, list_id), resolver(app), lang(), frozen=frozen, exclude=exclude)


class Auswahl:
    """Glides Auswahlfeld (`_make_option_menu`) mit Index-Schnittstelle."""

    def __init__(self, app, master, werte, index=0, on_change=None):
        self.werte = list(werte)
        self.var = tk.StringVar(master=master, value=self.werte[index] if self.werte else "")
        self.rahmen, self.feld = app._make_option_menu(master, self.var, self.werte)
        if on_change:
            self.var.trace_add("write", lambda *_a: on_change())

    def current(self, index=None):
        if index is not None:
            self.var.set(self.werte[index])
            return index
        return self.werte.index(self.var.get()) if self.var.get() in self.werte else 0

    def get(self):
        return self.var.get()

    def pack(self, **kw):
        self.rahmen.pack(**kw)
        return self


def kaestchen(app, master, text, variable, command=None):
    """Glides Kontrollkästchen aus der Shell statt eines Systemkästchens."""
    return _H["GlideCheckbutton"](master, text=text, variable=variable, command=command, bg=app.theme["bg"],
                                  fg=app.theme["text"], activeforeground=app.theme["text"], selectcolor=app.theme["card"],
                                  font=font(10))


def copy_text(app, text):
    """Kopiert nur in die lokale Zwischenablage; keine Übertragung."""
    app.root.clipboard_clear()
    app.root.clipboard_append(text)


# --- Prompt-Editor ---------------------------------------------------------------------
class PromptEditor:
    def __init__(self, app, list_id):
        self.app, self.list_id = app, list_id
        self.ws = app.ai_workspace()
        self.p = self.ws.prompt(list_id)
        self.felder = {}
        self._job = None
        self.d = dialog(app, T("editor.title", "Prompt bearbeiten – {title}", title=page_title(app, list_id)), "1180x780")
        self.d._prompt_editor = self
        self.bauen()
        self.vorschau_aktualisieren()

    def bauen(self):
        app, th = self.app, self.app.theme
        kopf = tk.Frame(self.d, bg=th["bg"])
        kopf.pack(fill="x", padx=16, pady=(12, 6))
        label(app, kopf, page_title(app, self.list_id), bold=True, size=15).pack(side="left")
        self.modus = button(app, kopf, "", self.modus_wechseln)
        self.modus.pack(side="right")
        self.status = Auswahl(app, kopf, [status_label(s) for s in aw.STATUSES], aw.STATUSES.index(self.p["status"]),
                              on_change=self.status_setzen)
        self.status.pack(side="right", padx=8)
        agenten = [("", T("agent.none", "Kein Agent"))] + sorted(((k, a["name"]) for k, a in self.ws.agents.items()), key=lambda x: x[1])
        self._agenten = agenten
        self.agent = Auswahl(app, kopf, [n for _k, n in agenten],
                             next((i for i, (k, _n) in enumerate(agenten) if k == (self.p["agent"] or "")), 0),
                             on_change=self.agent_setzen)
        self.agent.pack(side="right", padx=8)
        label(app, self.d, T("editor.body_hint", "Freitext: im Seiteneditor dieser Seite. Strukturierte Felder hier; die Vorschau setzt beides zusammen."),
              muted=True, size=9).pack(fill="x", padx=16)
        fuss = flow(app, self.d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        for text, befehl, rolle in (
                (T("editor.copy", "Prompt kopieren"), lambda: copy_text(app, render(app, self.list_id)[0]), "accent"),
                (T("editor.context", "Kontext …"), self.kontext_waehlen, "muted"),
                (T("editor.custom", "Eigenes Feld …"), self.eigenes_feld, "muted"),
                (T("editor.version", "Version speichern"), self.version_speichern, "muted"),
                (T("editor.versions", "Versionen …"), lambda: VersionsDialog(app, self.list_id, self), "muted"),
                (T("editor.export", "Übergabe und Export …"), lambda: ExportDialog(app, self.list_id), "muted"),
                (T("editor.report", "Bericht übernehmen …"), lambda: report_import(app, self.list_id), "muted"),
                (T("editor.follow_up", "Folgeauftrag"), lambda: app.ai_create_follow_up(self.list_id), "muted"),
                (T("editor.open_page", "Freitext öffnen"), lambda: app.set_active_list(self.list_id), "muted")):
            fuss.add(button(app, fuss, text, befehl, rolle))
        haupt = tk.PanedWindow(self.d, orient="horizontal", bg=th["bg"], sashwidth=6, bd=0)
        haupt.pack(fill="both", expand=True, padx=16)
        links, self.innen = scroll_area(app, haupt)
        rechts = tk.Frame(haupt, bg=th["bg"])
        haupt.add(links, minsize=420, width=620)
        haupt.add(rechts, minsize=300)
        label(app, rechts, T("editor.preview", "Vorschau (so wird der Prompt ausgegeben)"), bold=True).pack(fill="x")
        self.info = label(app, rechts, "", muted=True, size=9, wrap=480)
        self.info.pack(fill="x", pady=(2, 4))
        self.vorschau = text_field(app, rechts, height=30)
        self.vorschau.configure(state="disabled", font=("Consolas", 10) if os.name == "nt" else font(10))
        self.vorschau.pack(fill="both", expand=True)
        self.gruppen_bauen()

    def gruppen_bauen(self):
        app, th = self.app, self.app.theme
        for kind in self.innen.winfo_children():
            kind.destroy()
        self.felder.clear()
        erweitert = self.p["mode"] == "advanced"
        self.modus.set_text(T("editor.simple", "Einfacher Modus") if erweitert else T("editor.advanced", "Erweiterter Modus"))
        for gruppe in self.p["group_order"]:
            if not erweitert and gruppe not in aw.SIMPLE_GROUPS:
                continue
            definition = next((g for g in aw.FIELD_GROUPS if g[0] == gruppe), None)
            eigene = [c for c in self.p["custom"] if c["group"] == gruppe]
            if definition is None and not eigene:
                continue
            versteckt = gruppe in self.p["hidden"]
            kopf = tk.Frame(self.innen, bg=th["bg"])
            kopf.pack(fill="x", pady=(10, 2))
            titel = aw.group_title(gruppe, lang()) if definition else gruppe
            pfeil = tk.Label(kopf, text="▸" if versteckt else "▾", bg=th["bg"], fg=th["muted"], font=font(11), cursor="hand2")
            pfeil.pack(side="left")
            pfeil.bind("<Button-1>", lambda _e, g=gruppe: self.gruppe_umschalten(g))
            kopf_label = label(app, kopf, titel, bold=True, size=11)
            kopf_label.pack(side="left", padx=4)
            kopf_label.bind("<Button-1>", lambda _e, g=gruppe: self.gruppe_umschalten(g))
            if erweitert:
                for zeichen, richtung in (("↑", -1), ("↓", 1)):
                    k = tk.Label(kopf, text=zeichen, bg=th["bg"], fg=th["muted"], font=font(10), cursor="hand2")
                    k.pack(side="right", padx=2)
                    k.bind("<Button-1>", lambda _e, g=gruppe, r=richtung: self.gruppe_verschieben(g, r))
            if versteckt:
                continue
            werte = self.p["fields"].get(gruppe, {})
            for key, de, en in (definition[3] if definition else ()):
                label(app, self.innen, de if lang() == "de" else en, muted=True, size=9).pack(fill="x")
                t = text_field(app, self.innen, height=2 if gruppe != "basics" else 3, value=werte.get(key, ""))
                t.pack(fill="x", pady=(0, 4))
                t.bind("<KeyRelease>", lambda _e, g=gruppe, k=key, w=t: self.feld_geaendert(g, k, w))
                self.felder[(gruppe, key)] = t
            for c in eigene:
                label(app, self.innen, c["label"] + "  ·  " + T("editor.custom_mark", "eigenes Feld"), muted=True, size=9).pack(fill="x")
                t = text_field(app, self.innen, height=2, value=c["value"])
                t.pack(fill="x", pady=(0, 4))
                t.bind("<KeyRelease>", lambda _e, cid=c["id"], w=t: self.eigenes_geaendert(cid, w))
                self.felder[("custom", c["id"])] = t
        if not erweitert:
            label(app, self.innen, T("editor.more_hint", "Weitere Feldgruppen (Rolle, Technik, Anforderungen, Qualität …) im erweiterten Modus. Ausgeblendetes bleibt erhalten."),
                  muted=True, size=9, wrap=560).pack(fill="x", pady=(12, 0))

    # Änderungen
    def feld_geaendert(self, gruppe, key, widget):
        self.ws.set_field(self.list_id, gruppe, key, widget.get("1.0", "end-1c"))
        self.geaendert()

    def eigenes_geaendert(self, cid, widget):
        for c in self.p["custom"]:
            if c["id"] == cid:
                c["value"] = widget.get("1.0", "end-1c")
        self.geaendert()

    def geaendert(self):
        if self._job is not None:
            self.app.after_scope().cancel(self._job)
        self._job = self.app.after_scope().after(400, self._speichern_und_zeigen)

    def _speichern_und_zeigen(self):
        self._job = None
        self.app.save_ai_workspace()
        self.vorschau_aktualisieren()

    def modus_wechseln(self):
        self.p["mode"] = "simple" if self.p["mode"] == "advanced" else "advanced"
        self.gruppen_bauen()
        self.geaendert()

    def gruppe_umschalten(self, gruppe):
        if gruppe in self.p["hidden"]:
            self.p["hidden"].remove(gruppe)
        else:
            self.p["hidden"].append(gruppe)
        self.gruppen_bauen()
        self.geaendert()

    def gruppe_verschieben(self, gruppe, richtung):
        o = self.p["group_order"]
        i = o.index(gruppe)
        j = max(0, min(len(o) - 1, i + richtung))
        o[i], o[j] = o[j], o[i]
        self.gruppen_bauen()
        self.geaendert()

    def status_setzen(self):
        self.ws.set_status(self.list_id, aw.STATUSES[self.status.current()])
        self.geaendert()

    def agent_setzen(self):
        self.p["agent"] = self._agenten[self.agent.current()][0] or None
        self.geaendert()

    def eigenes_feld(self):
        name = self.app.themed_input_dialog(T("editor.custom", "Eigenes Feld …"), T("editor.custom_name", "Feldname:"))
        if not name:
            return
        gruppe = self.app.themed_input_dialog(T("editor.custom", "Eigenes Feld …"),
                                              T("editor.custom_group", "Gruppe (vorhandene oder neue):"), initial="Eigene Angaben")
        if not gruppe:
            return
        bekannt = {aw.group_title(g, lang()): g for g in aw.GROUP_KEYS}
        self.ws.add_custom_field(self.list_id, name, group=bekannt.get(gruppe, gruppe))
        self.p["mode"] = "advanced" if bekannt.get(gruppe, gruppe) not in aw.SIMPLE_GROUPS else self.p["mode"]
        self.gruppen_bauen()
        self.geaendert()

    def kontext_waehlen(self):
        ContextChooser(self.app, self.list_id, on_done=self.geaendert)

    def version_speichern(self):
        md, info = render(self.app, self.list_id)
        notiz = self.app.themed_input_dialog(T("editor.version", "Version speichern"), T("editor.version_note", "Notiz zur Version (optional):")) or ""
        nr = self.ws.create_version(self.list_id, md, page_body(self.app, self.list_id), info, notiz)
        self.app.save_ai_workspace()
        self.app.show_undo_toast(T("editor.version_saved", "Version {n} gespeichert", n=nr))

    def vorschau_aktualisieren(self):
        if not self.d.winfo_exists():
            return
        md, info = render(self.app, self.list_id)
        b = aw.budget(md)
        teile = [T("editor.budget", "{chars} Zeichen · {words} Wörter · ca. {tokens} Token (Schätzung, kein Tokenizer)",
                   chars=b["chars"], words=b["words"], tokens=b["tokens_estimate"]),
                 T("editor.sources", "Kontextquellen: {n}", n=len(info["sources"]))]
        if info["missing"]:
            teile.append(T("editor.missing", "Fehlende Quellen: {n}", n=len(info["missing"])))
        if info["placeholders"]:
            teile.append(T("editor.placeholders", "Offene Platzhalter: {names}", names=", ".join(info["placeholders"])))
        self.info.configure(text=" · ".join(teile))
        self.vorschau.configure(state="normal")
        self.vorschau.delete("1.0", "end")
        self.vorschau.insert("1.0", md)
        self.vorschau.configure(state="disabled")


# --- Kontextauswahl -----------------------------------------------------------------------
class ContextChooser:
    def __init__(self, app, list_id, on_done=None, pack_id=None):
        self.app, self.list_id, self.on_done, self.pack_id = app, list_id, on_done, pack_id
        ws = app.ai_workspace()
        ziel = ws.packs[pack_id]["items"] if pack_id else ws.prompt(list_id)["context"]
        gewaehlt = {(c["kind"], c["id"]) for c in ziel}
        d = dialog(app, T("context.title", "Kontext auswählen"), "760x640")
        rahmen, innen = scroll_area(app, d)
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        rahmen.pack(fill="both", expand=True, padx=16, pady=12)
        self.vars = []

        def abschnitt(titel, eintraege):
            label(app, innen, titel, bold=True, size=11).pack(fill="x", pady=(10, 2))
            if not eintraege:
                label(app, innen, T("context.empty", "Keine Einträge."), muted=True, size=9).pack(fill="x")
            for art, kennung, text in eintraege:
                v = tk.BooleanVar(value=(art, kennung) in gewaehlt)
                kaestchen(app, innen, text, v).pack(fill="x", anchor="w")
                self.vars.append((art, kennung, v))
        projekt = (next((x for x in app.lists if x.get("id") == list_id), {}) or {}).get("folder_id") if list_id else None
        anweisungen = []
        for fid, pr in ws.projects.items():
            for a in pr["instructions"]:
                ordner = (app.get_folder(fid) or {}).get("title", "?")
                anweisungen.append(("instruction", a["id"], f"{ordner} › {a['title']} (" + T("context.dynamic", "aktueller Stand") + ")"))
        abschnitt(T("context.instructions", "Projektanweisungen"), anweisungen)
        if not pack_id:
            abschnitt(T("context.packs", "Kontextpakete"), [("pack", k, p["title"]) for k, p in ws.packs.items()])
        abschnitt(T("context.blocks", "Kontextbausteine"), [("block", k, b["title"]) for k, b in ws.blocks.items()])
        abschnitt(T("context.documents", "Dokumente (neueste Version)"), [("doc", k, d_["title"]) for k, d_ in ws.documents.items() if not d_["archived"]])
        seiten = [("ref", f"glide://list/{e['id']}", str(e.get("title") or "")) for e in app.lists
                  if e.get("list_kind") in ("page", "note") and e.get("id") != list_id and not e.get("archived")]
        abschnitt(T("context.pages", "Seiten und Notizen (Verweis, keine Kopie)"), seiten[:300])
        if projekt:
            label(app, innen, T("context.project_hint", "Projekt dieses Prompts: {name}", name=(app.get_folder(projekt) or {}).get("title", "")),
                  muted=True, size=9).pack(fill="x", pady=(8, 0))

        def uebernehmen():
            neu = [{"kind": a, "id": k} for a, k, v in self.vars if v.get()]
            alt = [c for c in ziel if (c["kind"], c["id"]) not in {(a, k) for a, k, _v in self.vars}]
            ziel[:] = alt + neu
            if pack_id:
                ws.packs[pack_id]["revision"] += 1
            app.save_ai_workspace()
            d.destroy()
            if on_done:
                on_done()
        fuss.add(button(app, fuss, T("button.apply", "Übernehmen"), uebernehmen, "accent"))
        fuss.add(button(app, fuss, T("button.cancel", "Abbrechen"), d.destroy, "muted"))
        self.d = d


# --- Versionen ---------------------------------------------------------------------------
class VersionsDialog:
    def __init__(self, app, list_id, editor=None):
        ws = app.ai_workspace()
        p = ws.prompt(list_id)
        d = dialog(app, T("versions.title", "Versionen – {title}", title=page_title(app, list_id)), "980x640")
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        oben = tk.Frame(d, bg=app.theme["bg"])
        oben.pack(fill="both", expand=True, padx=16, pady=12)
        baum = ttk.Treeview(oben, columns=("datum", "status", "notiz"), show="headings", height=8, style="App.Treeview")
        for spalte, titel, breite in (("datum", T("versions.date", "Datum"), 180), ("status", T("versions.status", "Status"), 160),
                                      ("notiz", T("versions.note", "Notiz"), 420)):
            baum.heading(spalte, text=titel)
            baum.column(spalte, width=breite)
        for v in reversed(p["versions"]):
            baum.insert("", "end", iid=str(v["number"]), values=(f"#{v['number']} · {v['created'][:16].replace('T', ' ')}",
                                                                 status_label(v.get("status", "draft")), v["note"]))
        baum.pack(fill="x")
        anzeige = text_field(app, oben, height=18)
        anzeige.pack(fill="both", expand=True, pady=(8, 0))

        def gewaehlt():
            s = baum.selection()
            return ws.version(list_id, int(s[0])) if s else None

        def zeigen(_e=None):
            v = gewaehlt()
            anzeige.delete("1.0", "end")
            if v:
                anzeige.insert("1.0", v["markdown"])

        def vergleichen():
            v = gewaehlt()
            if v:
                anzeige.delete("1.0", "end")
                anzeige.insert("1.0", aw.Workspace.diff(v["markdown"], render(app, list_id)[0]) or T("versions.same", "Keine Unterschiede."))

        def wiederherstellen():
            v = gewaehlt()
            if not v or not app.ask_yes_no(T("versions.restore", "Version wiederherstellen"),
                                           T("versions.restore_q", "Felder und Freitext von Version {n} übernehmen? Der aktuelle Stand wird vorher als Version gesichert.", n=v["number"])):
                return
            md, info = render(app, list_id)
            ws.create_version(list_id, md, page_body(app, list_id), info, T("versions.before_restore", "vor Wiederherstellung"))
            body = ws.restore_version(list_id, v["number"])
            app.ai_set_page_body(list_id, body)
            app.save_ai_workspace()
            d.destroy()
            if editor and editor.d.winfo_exists():
                editor.gruppen_bauen()
                editor.vorschau_aktualisieren()

        def exportieren():
            v = gewaehlt()
            if not v:
                return
            pfad = filedialog.asksaveasfilename(defaultextension=".md", initialfile=f"prompt_v{v['number']}.md",
                                                filetypes=[("Markdown", "*.md"), ("Text", "*.txt")])
            if pfad:
                with open(pfad, "w", encoding="utf-8", newline="\n") as f:
                    f.write(v["markdown"])

        def duplizieren():
            v = gewaehlt()
            if v:
                app.ai_create_prompt(title=page_title(app, list_id) + " (v" + str(v["number"]) + ")", body=v["body"],
                                     fields=v["fields"], custom=v["custom"], open_editor=True)
        baum.bind("<<TreeviewSelect>>", zeigen)
        for text, befehl in ((T("versions.compare", "Mit aktuellem Stand vergleichen"), vergleichen),
                             (T("versions.restore", "Version wiederherstellen"), wiederherstellen),
                             (T("versions.duplicate", "Als neuen Prompt"), duplizieren),
                             (T("versions.export", "Exportieren …"), exportieren),
                             (T("button.close", "Schließen"), d.destroy)):
            fuss.add(button(app, fuss, text, befehl))
        self.d, self.baum = d, baum


# --- Export und Übergabe -------------------------------------------------------------------
class ExportDialog:
    def __init__(self, app, list_id):
        self.app, self.list_id = app, list_id
        ws = self.ws = app.ai_workspace()
        d = self.d = dialog(app, T("export.title", "Übergabe und Export – {title}", title=page_title(app, list_id)), "1080x760")
        label(app, d, T("export.intro", "1. Anbieter wählen · 2. Inhalt prüfen · 3. Quellen und Anhänge wählen · 4. Kopieren oder exportieren · "
                        "5. Anbieter bewusst öffnen und manuell einfügen. Glide überträgt nichts selbst."), muted=True, size=9, wrap=1000).pack(fill="x", padx=16, pady=(12, 4))
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        haupt = tk.PanedWindow(d, orient="horizontal", bg=app.theme["bg"], sashwidth=6)
        haupt.pack(fill="both", expand=True, padx=16)
        links, innen = scroll_area(app, haupt)
        rechts = tk.Frame(haupt, bg=app.theme["bg"])
        haupt.add(links, minsize=320, width=380)
        haupt.add(rechts, minsize=360)
        label(app, innen, T("export.provider", "Anbieter"), bold=True).pack(fill="x")
        self.anbieter = Auswahl(app, innen, [n for n, _u in PROVIDERS] + [T("export.other", "Anderer Agent / lokal")], len(PROVIDERS))
        self.anbieter.pack(fill="x", pady=(0, 8))
        _md, info = render(app, list_id)
        label(app, innen, T("export.sources", "Kontextquellen"), bold=True).pack(fill="x")
        self.quellen = []
        for schluessel, kopf, _text in info["sources"]:
            v = tk.BooleanVar(value=True)
            kaestchen(app, innen, kopf, v, self.aktualisieren).pack(fill="x", anchor="w")
            self.quellen.append((schluessel, v))
        label(app, innen, T("export.attachments", "Anhänge und Dokumente (nur im Paket)"), bold=True).pack(fill="x", pady=(8, 0))
        self.anhaenge = []
        for name, pfad in app.ai_prompt_files(list_id):
            v = tk.BooleanVar(value=False)
            kaestchen(app, innen, name, v, self.aktualisieren).pack(fill="x", anchor="w")
            self.anhaenge.append((name, pfad, v))
        if not self.anhaenge:
            label(app, innen, T("context.empty", "Keine Einträge."), muted=True, size=9).pack(fill="x")
        self.info = label(app, rechts, "", muted=True, size=9, wrap=640)
        self.info.pack(fill="x")
        self.warnung = label(app, rechts, "", size=9, wrap=640)
        self.warnung.pack(fill="x")
        self.vorschau = text_field(app, rechts, height=28)
        self.vorschau.pack(fill="both", expand=True)
        for text, befehl, rolle in ((T("export.copy", "Kopieren"), self.kopieren, "accent"),
                                    (T("export.copy_plain", "Ohne Kontext kopieren"), self.ohne_kontext, "muted"),
                                    (T("export.save_md", "Als Markdown …"), lambda: self.speichern(".md"), "muted"),
                                    (T("export.save_txt", "Als Text …"), lambda: self.speichern(".txt"), "muted"),
                                    (T("export.save_json", "Als JSON …"), self.json_speichern, "muted"),
                                    (T("export.package", "Kontextpaket (ZIP) …"), self.paket, "muted"),
                                    (T("export.open_provider", "Anbieter öffnen"), self.anbieter_oeffnen, "muted"),
                                    (T("export.mark", "Als übergeben markieren"), self.markieren, "muted"),
                                    (T("button.close", "Schließen"), d.destroy, "muted")):
            fuss.add(button(app, fuss, text, befehl, rolle))
        self.aktualisieren()

    def text(self, ohne_kontext=False):
        """Ausgehender Text: nur ausgewählte Quellen; ohne Kontext gar keine."""
        aus = {k for k, v in self.quellen if not v.get()}
        if ohne_kontext:
            aus |= {k for k, _v in self.quellen}
        return render(self.app, self.list_id, exclude=aus)[0]

    def aktualisieren(self):
        md = self.text()
        b = aw.budget(md)
        dateien = [n for n, _p, v in self.anhaenge if v.get()]
        self.info.configure(text=T("export.summary", "{chars} Zeichen · {words} Wörter · ca. {tokens} Token (Schätzung) · Quellen {src} · Dateien im Paket {files}",
                                   chars=b["chars"], words=b["words"], tokens=b["tokens_estimate"],
                                   src=sum(1 for _k, v in self.quellen if v.get()), files=len(dateien)))
        funde = aw.sensitive_findings(md)
        self.warnung.configure(fg=self.app.theme["flag"],
                               text=(T("export.sensitive", "Möglicherweise sensible Inhalte ({n}): {list} – bitte prüfen. Keine vollständige Erkennung.",
                                       n=len(funde), list=", ".join(sorted({a for a, _ in funde}))) if funde else ""))
        self.vorschau.delete("1.0", "end")
        self.vorschau.insert("1.0", md)

    def ausgabe(self):
        return self.vorschau.get("1.0", "end-1c")

    def kopieren(self):
        copy_text(self.app, self.ausgabe())
        self.app.show_undo_toast(T("export.copied", "In die Zwischenablage kopiert – nichts wurde übertragen"))

    def ohne_kontext(self):
        copy_text(self.app, self.text(ohne_kontext=True))
        self.app.show_undo_toast(T("export.copied", "In die Zwischenablage kopiert – nichts wurde übertragen"))

    def speichern(self, endung):
        pfad = filedialog.asksaveasfilename(defaultextension=endung, initialfile="PROMPT" + endung)
        if pfad:
            with open(pfad, "w", encoding="utf-8", newline="\n") as f:
                f.write(self.ausgabe())

    def json_daten(self):
        p = self.ws.prompt(self.list_id)
        return {"format": "glide-prompt", "version": 1, "title": page_title(self.app, self.list_id), "status": p["status"],
                "mode": p["mode"], "fields": p["fields"], "custom": p["custom"], "markdown": self.ausgabe()}

    def json_speichern(self):
        pfad = filedialog.asksaveasfilename(defaultextension=".json", initialfile="prompt.json")
        if pfad:
            with open(pfad, "w", encoding="utf-8", newline="\n") as f:
                json.dump(self.json_daten(), f, ensure_ascii=False, indent=2)

    def paket(self, ziel=None):
        dateien = [(f"dateien/{n}", pfad) for n, pfad, v in self.anhaenge if v.get()]
        nicht = [k for k, v in self.quellen if not v.get()] + [n for n, _p, v in self.anhaenge if not v.get()]
        ziel = ziel or filedialog.asksaveasfilename(defaultextension=".zip", initialfile="kontextpaket.zip")
        if not ziel:
            return None
        try:
            manifest = aw.build_package(ziel, self.ausgabe(), dateien + [("prompt.json", json.dumps(self.json_daten(), ensure_ascii=False, indent=2).encode("utf-8"))],
                                        {"title": page_title(self.app, self.list_id), "generator": "Glide"}, not_included=nicht)
        except (OSError, ValueError) as exc:
            self.app.show_error(T("export.package", "Kontextpaket (ZIP) …"), str(exc))
            return None
        self.app.show_undo_toast(T("export.package_done", "Paket mit {n} Dateien geschrieben", n=len(manifest["files"])))
        return manifest

    def anbieter_oeffnen(self):
        i = self.anbieter.current()
        if i < len(PROVIDERS):
            # Öffnet nur die Website. Glide sendet weder Prompt noch Dateien.
            webbrowser.open(PROVIDERS[i][1])

    def markieren(self):
        md = self.ausgabe()
        _m, info = render(self.app, self.list_id)
        self.ws.set_status(self.list_id, "handed_over")
        nr = self.ws.create_version(self.list_id, md, page_body(self.app, self.list_id), info,
                                    T("export.version_note", "übergeben an {who}", who=self.anbieter.get()))
        self.app.save_ai_workspace()
        self.app.show_undo_toast(T("export.marked", "Als übergeben markiert (Version {n} eingefroren)", n=nr))


def report_import(app, list_id, text=None, title=None, kind="report"):
    """Bericht als Daten übernehmen; enthaltene Anweisungen werden nie ausgeführt."""
    if text is None:
        pfad = filedialog.askopenfilename(filetypes=[("Text/Markdown", "*.md *.txt"), ("*", "*.*")])
        if pfad:
            with open(pfad, "r", encoding="utf-8", errors="replace") as f:
                text = f.read(aw.MAX_TEXT)
            title = title or os.path.basename(pfad)
        else:
            text = app.themed_input_dialog(T("report.title", "Bericht übernehmen"), T("report.paste", "Bericht einfügen (wird als Daten gespeichert, nicht ausgeführt):"))
            title = title or T("report.default", "Bericht")
    if not text:
        return None
    rid = app.ai_workspace().add_report(list_id, title or T("report.default", "Bericht"), text, kind=kind)
    ws = app.ai_workspace()
    if ws.prompt(list_id)["status"] in ("handed_over", "in_progress"):
        ws.set_status(list_id, "result_received")
    app.save_ai_workspace()
    return rid


# --- Bibliotheken ------------------------------------------------------------------------
class PromptLibrary:
    def __init__(self, app):
        self.app = app
        ws = app.ai_workspace()
        d = self.d = dialog(app, T("library.title", "Prompt-Bibliothek"), "1120x740")
        kopf = tk.Frame(d, bg=app.theme["bg"])
        kopf.pack(fill="x", padx=16, pady=(12, 4))
        label(app, kopf, T("library.title", "Prompt-Bibliothek"), bold=True, size=16).pack(side="left")
        self.karten = tk.Frame(d, bg=app.theme["bg"])
        self.karten.pack(fill="x", padx=10)
        befunde = app.ai_consistency()
        teile = []
        if befunde["dormant_prompts"]:
            teile.append(T("library.dormant", "{n} Prompts liegen mit ihrer Seite im Papierkorb", n=len(befunde["dormant_prompts"])))
        if befunde["orphan_prompts"]:
            teile.append(T("library.orphans", "{n} Prompt-Datensätze ohne Seite (bleiben erhalten, nicht angezeigt)", n=len(befunde["orphan_prompts"])))
        if befunde["missing_documents"]:
            teile.append(T("library.missing_docs", "{n} Verweise auf fehlende Dokumente", n=len(befunde["missing_documents"])))
        if befunde["missing_relations"]:
            teile.append(T("library.missing_rel", "{n} Beziehungen zu fehlenden Prompts", n=len(befunde["missing_relations"])))
        self.hinweis = label(app, d, " · ".join(teile), muted=True, size=9, wrap=1080)
        if teile:
            self.hinweis.configure(fg=app.theme["flag"])
            self.hinweis.pack(fill="x", padx=16)
        leiste = tk.Frame(d, bg=app.theme["bg"])
        leiste.pack(fill="x", padx=16, pady=6)
        # Shell-Suchfeld (E02): Platzhalter, Leeren-Knopf, Escape; gefiltert wird sofort.
        feld = SearchField(leiste, app.theme, placeholder=T("library.search", "Prompts durchsuchen"), font=font(10))
        feld.pack(side="left", fill="x", expand=True)
        self.suche = feld.variable
        self.suche.trace_add("write", lambda *_a: self.fuellen())
        self.gruppe = Auswahl(app, leiste, [T("library.by_status", "nach Status"), T("library.by_project", "nach Projekt"),
                                            T("library.by_agent", "nach Agent"), T("library.recent", "zuletzt bearbeitet")], 0,
                              on_change=lambda: self.fuellen())
        self.gruppe.pack(side="left", padx=8)
        self.archiv = tk.BooleanVar(value=False)
        kaestchen(app, leiste, T("library.archive", "Archiv zeigen"), self.archiv, self.fuellen).pack(side="left")
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        self.baum = ttk.Treeview(d, columns=("status", "projekt", "agent", "geaendert"), show="tree headings", style="App.Treeview")
        for spalte, titel, breite in (("#0", T("library.col_title", "Prompt"), 380), ("status", T("versions.status", "Status"), 190),
                                      ("projekt", T("library.col_project", "Projekt"), 170), ("agent", T("library.col_agent", "Agent"), 130),
                                      ("geaendert", T("library.col_updated", "Geändert"), 140)):
            self.baum.heading(spalte, text=titel)
            self.baum.column(spalte, width=breite)
        self.baum.pack(fill="both", expand=True, padx=16)
        self.baum.bind("<Double-1>", lambda _e: self.oeffnen())
        for text, befehl, rolle in ((T("library.new", "Neuer Prompt"), lambda: app.ai_create_prompt(open_editor=True), "accent"),
                                    (T("library.from_template", "Aus Vorlage …"), app.ai_create_from_template, "muted"),
                                    (T("library.open", "Bearbeiten"), self.oeffnen, "muted"),
                                    (T("library.duplicate", "Duplizieren"), self.duplizieren, "muted"),
                                    (T("library.favorite", "Favorit"), self.favorit, "muted"),
                                    (T("library.archive_btn", "Archivieren"), self.archivieren, "muted"),
                                    (T("library.save_template", "Als Vorlage speichern"), self.als_vorlage, "muted"),
                                    (T("library.chain", "Auftragskette"), self.kette, "muted"),
                                    (T("library.restore", "Aus Sicherung …"), lambda: app.ai_restore_from_backup(), "muted"),
                                    (T("button.close", "Schließen"), d.destroy, "muted")):
            fuss.add(button(app, fuss, text, befehl, rolle))
        self.fuellen()

    def eintraege(self):
        ws = self.app.ai_workspace()
        q = self.suche.get().strip().casefold()
        for list_id, p in ws.prompts.items():
            e = next((x for x in self.app.lists if x.get("id") == list_id), None)
            if e is None or (bool(e.get("archived")) != self.archiv.get()):
                continue
            agent = ws.agents.get(p["agent"] or "", {}).get("name", "")
            projekt = (self.app.get_folder(e.get("folder_id")) or {}).get("title", "")
            felder = " ".join(v for werte in p["fields"].values() for v in werte.values())
            if q and q not in " ".join([str(e.get("title")), felder, agent, projekt, (e.get("rich_note") or {}).get("text", ""),
                                        self.app.ai_label_names(e)]).casefold():
                continue
            yield list_id, p, e, agent, projekt

    def fuellen(self):
        ws = self.app.ai_workspace()
        for kind in self.karten.winfo_children():
            kind.destroy()
        alle = list(self.eintraege())
        ctx = self.app.glide_bento_context()
        for i, (wert, text) in enumerate(((len(alle), T("library.count", "Prompts")),
                                          (sum(1 for _i, p, *_r in alle if p["status"] in ("draft", "prepared")), T("library.open_count", "in Vorbereitung")),
                                          (sum(1 for _i, p, *_r in alle if p["status"] == "result_received"), T("library.results", "Ergebnis erhalten")),
                                          (len(ws.documents), T("library.documents", "Dokumente")))):
            karte = self.app.make_bento_card(self.karten)
            karte.grid(row=0, column=i, sticky="nsew", padx=6, pady=4)
            self.karten.grid_columnconfigure(i, weight=1, uniform="pl")
            glide_bento.BentoMetric(karte.inner, ctx, value=str(wert), label=text).pack(fill="x")
        self.baum.delete(*self.baum.get_children())
        modus = self.gruppe.current()
        gruppen = {}
        for list_id, p, e, agent, projekt in sorted(alle, key=lambda r: r[1]["updated"], reverse=True):
            schluessel = (status_label(p["status"]), projekt or T("library.no_project", "ohne Projekt"),
                          agent or T("agent.none", "Kein Agent"), "")[modus]
            if modus < 3 and schluessel not in gruppen:
                gruppen[schluessel] = self.baum.insert("", "end", text=schluessel, open=True)
            favorit = "★ " if list_id in (self.app.settings.get("page_favorites") or []) else ""
            self.baum.insert(gruppen.get(schluessel, ""), "end", iid=list_id, text=favorit + str(e.get("title") or ""),
                             values=(status_label(p["status"]), projekt, agent, p["updated"][:16].replace("T", " ")))

    def gewaehlt(self):
        s = [i for i in self.baum.selection() if i in self.app.ai_workspace().prompts]
        return s[0] if s else None

    def oeffnen(self):
        if self.gewaehlt():
            PromptEditor(self.app, self.gewaehlt())

    def duplizieren(self):
        if self.gewaehlt():
            self.app.ai_duplicate_prompt(self.gewaehlt())
            self.fuellen()

    def favorit(self):
        if self.gewaehlt():
            self.app.toggle_page_favorite(self.gewaehlt())
            self.fuellen()

    def archivieren(self):
        if self.gewaehlt():
            e = next(x for x in self.app.lists if x.get("id") == self.gewaehlt())
            self.app.set_archived("list", e["id"], not e.get("archived"))
            self.fuellen()

    def als_vorlage(self):
        if self.gewaehlt():
            self.app.ai_save_as_template(self.gewaehlt())

    def kette(self):
        if self.gewaehlt():
            ws = self.app.ai_workspace()
            zeilen = [f"{i + 1}. {page_title(self.app, x)} – {status_label(ws.prompt(x)['status'])}" for i, x in enumerate(ws.chain(self.gewaehlt()))]
            self.app.show_info(T("library.chain", "Auftragskette"), "\n".join(zeilen))


class ProfileDialog:
    """Projekt- oder Agentenprofil mit festen Feldern; Projektanweisungen versioniert."""
    PROJECT_FIELDS = (("description", "Beschreibung"), ("goal", "Projektziel"), ("repository", "Repository-URL"),
                      ("local_path", "Lokaler Pfad (privat, wird nicht exportiert)"), ("language", "Programmiersprache"),
                      ("stack", "Technologiestack"), ("architecture", "Architektur"), ("state", "Entwicklungsstand"),
                      ("versions", "Versionsstände"), ("formats", "Datenformate"), ("design_system", "Designsystem"),
                      ("docs_structure", "Dokumentationsstruktur"), ("work_rules", "Arbeitsregeln"), ("security_rules", "Sicherheitsregeln"),
                      ("git_rules", "Git-Regeln"), ("test_procedure", "Testverfahren"), ("open_decisions", "Offene Entscheidungen"),
                      ("risks", "Bekannte Risiken"))
    AGENT_FIELDS = (("name", "Name"), ("provider", "Anbieter"), ("model", "Modell (optional)"), ("areas", "Bevorzugte Aufgaben"),
                    ("output_format", "Gewünschtes Ausgabeformat"), ("rules", "Agentenregeln"), ("context_structure", "Bevorzugte Kontextstruktur"),
                    ("handover", "Übergabemethoden"), ("url", "Anbieterlink (optional)"))

    def __init__(self, app, kind, key):
        ws = app.ai_workspace()
        self.app = app
        datensatz = ws.project(key) if kind == "project" else ws.agents[key]
        titel = (app.get_folder(key) or {}).get("title", "") if kind == "project" else datensatz["name"]
        d = dialog(app, (T("profile.project", "KI-Projektprofil – {name}", name=titel) if kind == "project"
                         else T("profile.agent", "Agentenprofil – {name}", name=titel)), "900x760")
        label(app, d, T("profile.local", "Lokale Organisationsdaten. Keine Zugangsdaten oder Schlüssel speichern; Glide verbindet sich mit keinem Anbieter."),
              muted=True, size=9, wrap=860).pack(fill="x", padx=16, pady=(10, 0))
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        rahmen, innen = scroll_area(app, d)
        rahmen.pack(fill="both", expand=True, padx=16, pady=8)
        felder = {}
        for key_, de in (self.PROJECT_FIELDS if kind == "project" else self.AGENT_FIELDS):
            label(app, innen, T(f"profile.f.{key_}", de), muted=True, size=9).pack(fill="x")
            t = text_field(app, innen, height=2, value=datensatz.get(key_, ""))
            t.pack(fill="x", pady=(0, 4))
            felder[key_] = t
        if kind == "project":
            label(app, innen, T("profile.instructions", "Projektanweisungen (jede Änderung wird eine neue Fassung; frühere Prompts behalten ihren Stand)"),
                  bold=True).pack(fill="x", pady=(12, 2))
            for a in datensatz["instructions"]:
                zeile = tk.Frame(innen, bg=app.theme["bg"])
                zeile.pack(fill="x")
                label(app, zeile, f"{a['title']} · " + T("profile.revision", "Fassung {n}", n=a["version"])).pack(side="left")
                button(app, zeile, T("profile.edit", "Bearbeiten"), lambda a=a: self.anweisung(key, a["id"])).pack(side="right")
            button(app, innen, T("profile.add_instruction", "Neue Anweisung …"), lambda: self.anweisung(key, None)).pack(anchor="w", pady=4)

        def speichern():
            for key_, t in felder.items():
                datensatz[key_] = t.get("1.0", "end-1c")[:20000]
            datensatz["updated"] = aw.now()
            app.save_ai_workspace()
            d.destroy()
        fuss.add(button(app, fuss, T("button.save", "Speichern"), speichern, "accent"))
        fuss.add(button(app, fuss, T("button.cancel", "Abbrechen"), d.destroy))
        self.d = d

    def anweisung(self, folder_id, instruction_id):
        ws = self.app.ai_workspace()
        a = ws.instruction(instruction_id) if instruction_id else None
        titel = self.app.themed_input_dialog(T("profile.instruction", "Projektanweisung"), T("profile.instruction_title", "Titel:"),
                                             initial=(a or {}).get("title", ""))
        if not titel:
            return
        text = self.app.themed_input_dialog(T("profile.instruction", "Projektanweisung"), T("profile.instruction_text", "Text:"),
                                            initial=(a or {}).get("text", ""))
        if text is None:
            return
        ws.set_instruction(folder_id, titel, text, instruction_id)
        self.app.save_ai_workspace()
        self.d.destroy()
        ProfileDialog(self.app, "project", folder_id)


class ContextLibrary:
    def __init__(self, app):
        ws = app.ai_workspace()
        d = self.d = dialog(app, T("ctxlib.title", "Kontextbibliothek, Projekte und Agenten"), "1000x700")
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        baum = self.baum = ttk.Treeview(d, columns=("art",), show="tree headings", style="App.Treeview")
        baum.heading("#0", text=T("ctxlib.name", "Name"))
        baum.heading("art", text=T("ctxlib.kind", "Art"))
        baum.pack(fill="both", expand=True, padx=16, pady=12)

        def fuellen():
            baum.delete(*baum.get_children())
            for titel, eintraege in ((T("ctxlib.projects", "KI-Projektprofile"), [(f"project:{k}", (app.get_folder(k) or {}).get("title", k), T("ctxlib.project", "Projekt")) for k in ws.projects]),
                                     (T("ctxlib.agents", "Agentenprofile"), [(f"agent:{k}", a["name"], a["provider"]) for k, a in ws.agents.items()]),
                                     (T("ctxlib.blocks", "Kontextbausteine"), [(f"block:{k}", b["title"], b["kind"]) for k, b in ws.blocks.items()]),
                                     (T("ctxlib.packs", "Kontextpakete"), [(f"pack:{k}", p["title"], T("ctxlib.items", "{n} Quellen · Stand {r}", n=len(p["items"]), r=p["revision"])) for k, p in ws.packs.items()])):
                oben = baum.insert("", "end", text=titel, open=True)
                for iid, name, art in eintraege:
                    baum.insert(oben, "end", iid=iid, text=name, values=(art,))
        self.fuellen = fuellen

        def gewaehlt():
            s = baum.selection()
            return s[0].split(":", 1) if s and ":" in s[0] else (None, None)

        def bearbeiten():
            art, k = gewaehlt()
            if art in ("project", "agent"):
                ProfileDialog(app, art, k)
            elif art == "block":
                b = ws.blocks[k]
                text = app.themed_input_dialog(T("ctxlib.block", "Kontextbaustein"), b["title"], initial=b["text"])
                if text is not None:
                    b["text"], b["updated"] = text, aw.now()
                    app.save_ai_workspace()
            elif art == "pack":
                ContextChooser(app, None, on_done=fuellen, pack_id=k)

        def neues_projekt():
            ordner = app.themed_choice_dialog(T("ctxlib.new_project", "KI-Projektprofil"), T("ctxlib.pick_folder", "Ordner, der das Projekt darstellt:"),
                                              [(f["id"], f.get("title") or "") for f in app.folders if not f.get("archived")])
            if ordner:
                ws.project(ordner)
                app.save_ai_workspace()
                ProfileDialog(app, "project", ordner)
                fuellen()

        def neuer_agent():
            name = app.themed_input_dialog(T("ctxlib.new_agent", "Neues Agentenprofil"), T("ctxlib.agent_name", "Name (z. B. Claude, Codex):"))
            if name:
                k = ws.add_agent(name)
                app.save_ai_workspace()
                ProfileDialog(app, "agent", k)
                fuellen()

        def neuer_baustein():
            titel = app.themed_input_dialog(T("ctxlib.block", "Kontextbaustein"), T("ctxlib.block_title", "Titel:"))
            if titel:
                text = app.themed_input_dialog(T("ctxlib.block", "Kontextbaustein"), T("ctxlib.block_text", "Inhalt:")) or ""
                ws.add_block(titel, text)
                app.save_ai_workspace()
                fuellen()

        def neues_paket():
            titel = app.themed_input_dialog(T("ctxlib.pack", "Kontextpaket"), T("ctxlib.pack_title", "Titel:"))
            if titel:
                k = ws.add_pack(titel, [])
                app.save_ai_workspace()
                ContextChooser(app, None, on_done=fuellen, pack_id=k)
                fuellen()
        for text, befehl, rolle in ((T("ctxlib.edit", "Öffnen"), bearbeiten, "accent"), (T("ctxlib.new_project", "KI-Projektprofil"), neues_projekt, "muted"),
                                    (T("ctxlib.new_agent", "Neues Agentenprofil"), neuer_agent, "muted"), (T("ctxlib.new_block", "Neuer Baustein"), neuer_baustein, "muted"),
                                    (T("ctxlib.new_pack", "Neues Paket"), neues_paket, "muted"), (T("button.close", "Schließen"), d.destroy, "muted")):
            fuss.add(button(app, fuss, text, befehl, rolle))
        baum.bind("<Double-1>", lambda _e: bearbeiten())
        fuellen()


class DocumentLibrary:
    def __init__(self, app):
        self.app = app
        ws = app.ai_workspace()
        d = self.d = dialog(app, T("docs.title", "Dokumentenbibliothek"), "1180x760")
        kopf = tk.Frame(d, bg=app.theme["bg"])
        kopf.pack(fill="x", padx=16, pady=(12, 2))
        label(app, kopf, T("docs.title", "Dokumentenbibliothek"), bold=True, size=16).pack(side="left")
        label(app, d, T("docs.managed", "Alle Dokumente hier sind verwaltete Kopien im Glide-Datenordner und Teil der vollständigen Sicherung. "
                        "Externe Verknüpfungen gibt es nicht; Vorschauen und Suchindex sind abgeleitet."), muted=True, size=9, wrap=1120).pack(fill="x", padx=16)
        leiste = tk.Frame(d, bg=app.theme["bg"])
        leiste.pack(fill="x", padx=16, pady=6)
        feld = SearchField(leiste, app.theme, placeholder=T("docs.search", "Dokumente durchsuchen"), font=font(10))
        feld.pack(side="left", fill="x", expand=True)
        self.suche = feld.variable
        self.suche.trace_add("write", lambda *_a: self.fuellen())
        fuss = flow(app, d)
        fuss.pack(side="bottom", fill="x", padx=16, pady=10)
        haupt = tk.PanedWindow(d, orient="horizontal", bg=app.theme["bg"], sashwidth=6)
        haupt.pack(fill="both", expand=True, padx=16)
        self.baum = ttk.Treeview(haupt, columns=("typ", "versionen", "groesse", "status"), show="tree headings", style="App.Treeview")
        for spalte, titel, breite in (("#0", T("docs.col_title", "Dokument"), 300), ("typ", T("docs.col_type", "Typ"), 70),
                                      ("versionen", T("docs.col_versions", "Versionen"), 80), ("groesse", T("docs.col_size", "Größe"), 90),
                                      ("status", T("docs.col_state", "Zustand"), 120)):
            self.baum.heading(spalte, text=titel)
            self.baum.column(spalte, width=breite)
        rechts = tk.Frame(haupt, bg=app.theme["bg"])
        haupt.add(self.baum, minsize=420, width=640)
        haupt.add(rechts, minsize=360)
        self.detail = label(app, rechts, "", size=9, wrap=480)
        self.detail.pack(fill="x")
        self.bild = tk.Label(rechts, bg=app.theme["bg"])
        self.bild.pack(anchor="w")
        self.vorschau = text_field(app, rechts, height=20)
        self.vorschau.pack(fill="both", expand=True)
        self.baum.bind("<<TreeviewSelect>>", lambda _e: self.zeigen())
        for text, befehl, rolle in ((T("docs.import", "Importieren …"), lambda: app.ai_import_documents(), "accent"),
                                    (T("docs.new_version", "Neue Version …"), self.neue_version, "muted"),
                                    (T("docs.open", "Öffnen"), self.oeffnen, "muted"),
                                    (T("docs.export", "Version exportieren …"), self.exportieren, "muted"),
                                    (T("docs.restore_version", "Ältere Version zurückholen"), self.version_zurueck, "muted"),
                                    (T("docs.link", "Mit Prompt verbinden …"), self.verbinden, "muted"),
                                    (T("docs.check", "Integrität prüfen"), self.pruefen, "muted"),
                                    (T("docs.archive", "Archivieren"), self.archivieren, "muted"),
                                    (T("button.close", "Schließen"), d.destroy, "muted")):
            fuss.add(button(app, fuss, text, befehl, rolle))
        self.index = aw.TextIndex().rebuild(ws, app.ai_data_dir())
        self.fuellen()

    def fuellen(self):
        ws = self.app.ai_workspace()
        self.baum.delete(*self.baum.get_children())
        q = self.suche.get().strip()
        treffer = {did: art for did, art in self.index.search(ws, q)} if q else None
        for did, doc in sorted(ws.documents.items(), key=lambda x: x[1]["title"].casefold()):
            if treffer is not None and did not in treffer:
                continue
            v = doc["versions"][-1] if doc["versions"] else None
            pfad = self.app.ai_data_path(v["storage"]) if v else None
            zustand = T("docs.ok", "vorhanden") if pfad and os.path.isfile(pfad) else T("docs.missing", "Datei fehlt")
            if doc["archived"]:
                zustand += " · " + T("docs.archived", "archiviert")
            if treffer is not None:
                zustand += " · " + (T("docs.hit_text", "Treffer im Text") if treffer[did] == "text" else T("docs.hit_meta", "Treffer in Metadaten"))
            self.baum.insert("", "end", iid=did, text=doc["title"],
                             values=(os.path.splitext(v["name"])[1].lstrip(".").upper() if v else "", len(doc["versions"]),
                                     f"{(v['size'] if v else 0) / 1024:.1f} KB", zustand))

    def gewaehlt(self):
        s = self.baum.selection()
        return s[0] if s else None

    def zeigen(self):
        ws = self.app.ai_workspace()
        did = self.gewaehlt()
        if not did:
            return
        doc = ws.documents[did]
        v = doc["versions"][-1]
        orte = ws.document_usages(did)
        orte_text = ", ".join(page_title(self.app, k) if art == "prompt" else ws.packs[k]["title"] for art, k in orte) or T("docs.unused", "nirgends verwendet")
        self.detail.configure(text=T("docs.detail", "{title}\nVersion {n} von {total} · {name} · SHA-256 {sha}…\nVerwendet in: {where}",
                                     title=doc["title"], n=len(doc["versions"]), total=len(doc["versions"]), name=v["name"],
                                     sha=v["sha256"][:12], where=orte_text))
        pfad = self.app.ai_data_path(v["storage"])
        self.bild.configure(image="")
        self.vorschau.delete("1.0", "end")
        if pfad.lower().endswith((".png", ".gif")) and os.path.isfile(pfad):
            try:
                foto = tk.PhotoImage(file=pfad)
                faktor = max(1, foto.width() // 420 + 1)
                foto = foto.subsample(faktor, faktor)
                self.bild.configure(image=foto)
                self.bild.image = foto
            except tk.TclError:
                pass
        text = aw.extract_text(pfad)
        self.vorschau.insert("1.0", (text or T("docs.no_preview", "Keine interne Vorschau für dieses Format; „Öffnen“ nutzt das Standardprogramm."))[:20000])

    def neue_version(self):
        if self.gewaehlt():
            self.app.ai_import_documents(add_version_to=self.gewaehlt())
            self.index.rebuild(self.app.ai_workspace(), self.app.ai_data_dir())
            self.fuellen()

    def oeffnen(self):
        if self.gewaehlt():
            v = self.app.ai_workspace().documents[self.gewaehlt()]["versions"][-1]
            self.app.open_external_path(self.app.ai_data_path(v["storage"]))

    def exportieren(self):
        if not self.gewaehlt():
            return
        doc = self.app.ai_workspace().documents[self.gewaehlt()]
        wahl = self.app.themed_choice_dialog(T("docs.export", "Version exportieren …"), T("docs.pick_version", "Welche Version?"),
                                             [(v["id"], f"{i + 1}: {v['name']} · {v['created'][:16]}") for i, v in enumerate(doc["versions"])])
        v = next((x for x in doc["versions"] if x["id"] == wahl), None)
        if v:
            ziel = filedialog.asksaveasfilename(initialfile=v["name"])
            if ziel:
                with open(self.app.ai_data_path(v["storage"]), "rb") as q, open(ziel, "wb") as z:
                    z.write(q.read())

    def version_zurueck(self):
        """Ältere Fassung wird neueste Version – ohne Kopie der Datei, nichts wird überschrieben."""
        if not self.gewaehlt():
            return
        ws = self.app.ai_workspace()
        doc = ws.documents[self.gewaehlt()]
        wahl = self.app.themed_choice_dialog(T("docs.restore_version", "Ältere Version zurückholen"), T("docs.pick_version", "Welche Version?"),
                                             [(v["id"], f"{i + 1}: {v['name']} · {v['created'][:16]}") for i, v in enumerate(doc["versions"][:-1])])
        v = next((x for x in doc["versions"] if x["id"] == wahl), None)
        if v:
            ws.add_document_version(self.gewaehlt(), dict(v, id=aw.new_id(), created=aw.now(),
                                                          note=T("docs.restored_from", "wiederhergestellt aus {name}", name=v["created"][:16])))
            self.app.save_ai_workspace()
            self.fuellen()

    def verbinden(self):
        did = self.gewaehlt()
        if not did:
            return
        ws = self.app.ai_workspace()
        ziel = self.app.themed_choice_dialog(T("docs.link", "Mit Prompt verbinden …"), T("docs.pick_prompt", "Prompt:"),
                                             [(k, page_title(self.app, k)) for k in ws.prompts])
        if ziel:
            ws.relate(ziel, "document", did)
            ws.prompt(ziel)["context"].append({"kind": "doc", "id": did})
            self.app.save_ai_workspace()
            self.zeigen()

    def pruefen(self):
        ws = self.app.ai_workspace()
        fehlend, abweichend = [], []
        for doc in ws.documents.values():
            for v in doc["versions"]:
                pfad = self.app.ai_data_path(v["storage"])
                if not os.path.isfile(pfad):
                    fehlend.append(v["name"])
                elif aw.sha256_file(pfad) != v["sha256"]:
                    abweichend.append(v["name"])
        self.app.show_info(T("docs.check", "Integrität prüfen"), T("docs.check_result", "Versionen geprüft: {n} · fehlend: {missing} · Prüfsumme abweichend: {bad}",
                                                                      n=sum(len(x["versions"]) for x in ws.documents.values()),
                                                                      missing=", ".join(fehlend) or "0", bad=", ".join(abweichend) or "0"))
        return fehlend, abweichend

    def archivieren(self):
        did = self.gewaehlt()
        if did:
            doc = self.app.ai_workspace().documents[did]
            doc["archived"] = not doc["archived"]
            self.app.save_ai_workspace()
            self.fuellen()
