# SPDX-License-Identifier: MPL-2.0
"""Bento marketing: product cards and portfolio view for a software ecosystem (Bento 0.4.0).

Presents `glide_shell.software_catalog.Product` entries in the host's design:
colours come from the Bento context, the product's brand colour is only used
for its monogram tile (with a readable text colour), never for the host's
own controls. No tracking, no network, no pop-ups: links are shown as
buttons and open only through the host's `on_link(url)` callback after a
click. Missing or unknown facts are omitted, not invented.

Public interface:

- `ProductCard(master, context, product, language="en", logo=None, on_link=None,
  texts=None, current=False)` – a `BentoCard` with monogram or logo, name,
  status, category, summary, features and link buttons.
- `PortfolioView(master, context, catalog, current_id=None, language="en",
  logo_provider=None, on_link=None, texts=None, include_current=False)` – a
  `BentoGrid` with one `ProductCard` per product; `cards` maps id → card.
- `monogram(name)` – up to two initials; `TEXTS` – default English texts.
"""
from __future__ import annotations

import tkinter as tk

from glide_shell import color_roles, software_catalog

from .card import BentoCard
from .components import BentoActions
from .grid import BentoGrid
from .specs import BentoCardSpec

TEXTS = {"status": {"concept": "Concept", "development": "In development", "prerelease": "Pre-release",
                    "released": "Released", "maintenance": "Maintenance", "discontinued": "Discontinued"},
         "links": {"website": "Website", "repository": "Source code", "documentation": "Documentation",
                   "download": "Downloads"},
         "license": "Licence", "version": "Version", "this_app": "This app"}


def monogram(name):
    teile = [t for t in str(name).replace("&", " ").split() if t[:1].isalnum()]
    return ("".join(t[0] for t in teile[:2]) or str(name)[:2]).upper()


def _on_color(farbe):
    try:
        return "#FFFFFF" if color_roles.contrast_ratio(farbe, "#FFFFFF") >= color_roles.contrast_ratio(farbe, "#000000") else "#000000"
    except ValueError:
        return "#FFFFFF"


class ProductCard(BentoCard):
    def __init__(self, master, context, product, language="en", logo=None, on_link=None, texts=None, current=False):
        self.product, self.language = product, language
        self.texts = {**TEXTS, **(texts or {})}
        super().__init__(master, context=context, spec=BentoCardSpec(f"product-{product.id}", title=None))
        bg = context.resolve_color("card_bg")
        text = context.resolve_color("text_primary")
        muted = context.resolve_color("text_muted")
        kopf = tk.Frame(self.body, bg=bg)
        kopf.pack(fill="x")
        if logo is not None:
            marke = tk.Label(kopf, image=logo, bg=bg)
            marke.image = logo
        else:
            farbe = product.brand_color or context.resolve_color("accent")
            marke = tk.Label(kopf, text=monogram(product.name), width=3, height=1, bg=farbe, fg=_on_color(farbe),
                             font=context.resolve_font(16, "bold"))
        marke.pack(side="left", padx=(0, 10))
        titel = tk.Frame(kopf, bg=bg)
        titel.pack(side="left", fill="x", expand=True)
        tk.Label(titel, text=product.name, bg=bg, fg=text, anchor="w", font=context.resolve_font(15, "bold")).pack(fill="x")
        zeile = []
        if product.known("category"):
            zeile.append(software_catalog.text(product.category, language))
        if product.status in self.texts["status"]:
            zeile.append(self.texts["status"][product.status])
        if product.known("version"):
            zeile.append(f"{self.texts['version']} {product.version}")
        if current:
            zeile.append(self.texts["this_app"])
        tk.Label(titel, text=" · ".join(zeile), bg=bg, fg=muted, anchor="w", font=context.resolve_font(9)).pack(fill="x")
        zusammenfassung = software_catalog.text(product.summary, language)
        if zusammenfassung:
            self.summary_label = tk.Label(self.body, text=zusammenfassung, bg=bg, fg=text, anchor="w", justify="left",
                                          wraplength=320, font=context.resolve_font(10))
            self.summary_label.pack(fill="x", pady=(8, 4))
            self.body.bind("<Configure>", lambda e: self.summary_label.configure(wraplength=max(160, e.width - 8)), add="+")
        for merkmal in product.features[:5]:
            tk.Label(self.body, text="• " + software_catalog.text(merkmal, language), bg=bg, fg=muted, anchor="w",
                     font=context.resolve_font(9)).pack(fill="x")
        if product.known("license"):
            tk.Label(self.body, text=f"{self.texts['license']}: {product.license}", bg=bg, fg=muted, anchor="w",
                     font=context.resolve_font(9)).pack(fill="x", pady=(4, 0))
        links = [(self.texts["links"][k], product.link(k)) for k in software_catalog.LINK_KEYS if product.link(k)]
        self.link_targets = [url for _label, url in links]
        if links and on_link is not None:
            aktionen = BentoActions(self.body, context,
                                    actions=[(label, (lambda u=url: software_catalog.open_link(u, on_link)), "muted")
                                             for label, url in links])
            aktionen.pack(fill="x", pady=(8, 0))
            self.actions = aktionen


class PortfolioView(BentoGrid):
    def __init__(self, master, context, catalog, current_id=None, language="en", logo_provider=None, on_link=None,
                 texts=None, include_current=False):
        super().__init__(master, context=context)
        self.cards = {}
        produkte = catalog.products() if include_current else catalog.others(current_id)
        for product in produkte:
            logo = logo_provider(product) if logo_provider is not None else None
            karte = ProductCard(self, context, product, language=language, logo=logo, on_link=on_link, texts=texts,
                                current=product.id == current_id)
            self.cards[product.id] = karte
            self.add_card(karte)
