# SPDX-License-Identifier: MPL-2.0
"""Komponenten-Galerie: Glide als Schaufenster seiner Frameworks (D105, Master-Serie Teil 02).

Tk-frei nach D17. Die Galerie zeigt die echten Bausteine aus `glide_shell`
und `glide_bento`; jedes Framework beschreibt seine Komponenten selbst
(`glide_shell.showcase.shell_entries`, `glide_bento.showcase.bento_entries`).
Glide ergänzt nur, wo eine Komponente in Glide produktiv arbeitet
(`GLIDE_USAGE`, Übersetzungsschlüssel mit deutschem Rückfalltext). Eine
Komponente ohne natürlichen Einsatzort trägt ausdrücklich `GALLERY_ONLY`.

Regeln:
1. Keine nachgebauten Kopien: Gezeigt wird, was die Builder der Frameworks
   erzeugen.
2. Vollständigkeit: `missing_components` nennt jede erwartete Komponente ohne
   Eintrag, `registry_problems` jeden Eintrag ohne Builder oder Einsatzangabe.
   Spätere Teile (Navigation, Kanban, Symbole, Katalog) ergänzen ihre Einträge
   in denselben Registern; eine zweite Galerie entsteht nicht.
3. Nur künstliche Daten; die Galerie liest und schreibt keine Nutzerdaten.
"""
from __future__ import annotations

import dataclasses

GALLERY_ONLY = "gallery_only"

# Komponente → Einsatzorte in Glide (Schlüssel, deutscher Rückfalltext).
GLIDE_USAGE = {
    "shell.canvas_label": (("ui.component_gallery.usage.home_editor", "Startseite anpassen, Seitenkopf"),),
    "shell.checkbutton": (("ui.component_gallery.usage.settings_checks", "Sicherungsauswahl, Planungs- und Ansichtsdialoge"),),
    "shell.radiobutton": (("ui.component_gallery.usage.day_relief", "Entlastungsdialog, Animationsdialog"),),
    "shell.listbox": (("ui.component_gallery.usage.listbox", "Anhänge, Checklisten, Fundorte, Auswahldialoge"),),
    "shell.scale": (("ui.component_gallery.usage.drawing_scale", "Pixel-Werkstatt: Regler im Zeichendialog"),),
    "shell.auto_scrollbar": (("ui.component_gallery.usage.scrolling", "Alle scrollenden Ansichten und Dialoge"),),
    "shell.text_fit": (("ui.component_gallery.usage.text_fit", "Kürzen von Namen und Titeln (über ui_design)"),),
    # Rechtschreibprüfung: produktiv erst nach Freigabe einer Engine (EDITOR-02, Entscheidungsvorlage M15).
    "shell.spellcheck": (GALLERY_ONLY,),
    "shell.action_handle": (("ui.component_gallery.usage.handles", "Blockeditor und Inline-Aufgabenerfassung"),),
    "shell.drop_indicator": (("ui.component_gallery.usage.sidebar_drop", "Platzanzeige beim Ziehen in der Seitenleiste"),),
    "shell.search_field": (("ui.component_gallery.usage.ai_search", "KI-Arbeitsbereich: Suche in Prompt- und Dokumentenbibliothek"),),
    # Neue Shell-Bausteine 0.10.0 ohne natürlichen Glide-Einsatzort; Glides eigene Knöpfe,
    # Tooltips und Leisten bleiben bis zu einer gezielten Ablösung bestehen (E04/E05).
    "shell.button": (GALLERY_ONLY,),
    "shell.tooltip": (GALLERY_ONLY,),
    "shell.toolbar": (GALLERY_ONLY,),
    "shell.workspaces": (GALLERY_ONLY,),
    "shell.theme_provider": (GALLERY_ONLY,),
    "bento.card": (("ui.component_gallery.usage.home_cards", "Startseite: Kacheln"),),
    "bento.metric": (GALLERY_ONLY,),
    "bento.actions": (GALLERY_ONLY,),
    "bento.empty_state": (("ui.component_gallery.usage.empty_states", "Leerzustände der Startseite und der Seitenübersicht"),),
    "bento.divider": (GALLERY_ONLY,),
    # Die Startseite nutzt den Planer mit eigenen Behältern, nicht das Grid-Widget (Lücke, Teil 07).
    "bento.grid": (GALLERY_ONLY,),
    "bento.layout_planner": (("ui.component_gallery.usage.home_planner", "Startseite: Spalten- und Bandplanung"),),
}

# Breite der Vorführfläche in Pixeln; der Nutzer wählt sie in der Galerie.
WIDTHS = (("narrow", 360), ("medium", 640), ("wide", 960))
DEFAULT_WIDTH = "medium"
# „current“ = aktives Design, „light“/„dark“ = Grunddesigns zum Vergleich.
THEME_CHOICES = ("current", "light", "dark")


def expected_components():
    from glide_bento.showcase import BENTO_COMPONENTS
    from glide_shell.showcase import SHELL_COMPONENTS
    return tuple(SHELL_COMPONENTS) + tuple(BENTO_COMPONENTS)


def build_registry(usage=None):
    """Register aller Galerie-Einträge mit Glide-Einsatzorten."""
    from glide_bento.showcase import bento_entries
    from glide_shell.showcase import ShowcaseRegistry, shell_entries
    usage = GLIDE_USAGE if usage is None else usage
    registry = ShowcaseRegistry()
    for entry in list(shell_entries()) + list(bento_entries()):
        registry.register(dataclasses.replace(entry, used_in=tuple(usage.get(entry.id, ()))))
    return registry


def missing_components(registry):
    return registry.coverage(expected_components())


def registry_problems(registry):
    return registry.problems()


def width_for(key):
    return dict(WIDTHS).get(key, dict(WIDTHS)[DEFAULT_WIDTH])


def usage_texts(entry, translate):
    """Einsatzorte als Anzeigetexte; `translate(key, fallback)` liefert die Sprache des Hosts."""
    texte = []
    for item in entry.used_in:
        if item == GALLERY_ONLY:
            texte.append(translate("ui.component_gallery.usage.gallery_only", "Nur in der Galerie"))
        else:
            key, fallback = item
            texte.append(translate(key, fallback))
    return texte
