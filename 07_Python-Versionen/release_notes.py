"""Einmalige Karte „Neu in …“ nach einem Update, ohne Tk (N07 seit 3.33.20).

Der Katalog nennt je Version höchstens fünf Neuerungen in einem Satz. Nach dem
ersten Start ohne Vorgängerversion erscheint nichts: Ein Einstieg für neue
Nutzer ist bewusst nicht gewählt (N06). „Gelesen“ merkt die Version lokal.
"""

# Je Version höchstens fünf Sätze; neueste Version oben. Eine Version ohne
# Eintrag zeigt keine Karte.
CATALOG = {
    "3.33.19": (
        "Schneller: Seiten mit vielen Bildern, die Startseite und das Einstellungsfenster reagieren zügiger.",
        "Weniger Schreibvorgänge je Aktion – gespeichert wird weiterhin sofort.",
    ),
    "3.33.20": (
        "Wiederholungen: „Diesen Termin überspringen“ und „Verpasste Termine überspringen“ im Kontextmenü.",
        "Erinnerung gleich beim Erfassen: „erinnere 9 Uhr“ oder „Erinnerung 30 min vorher“.",
        "Mehrere Zeilen in die Eingabezeile einfügen legt auf Wunsch je Zeile eine Aufgabe an.",
        "„+“ legt an, Umschalt+Enter öffnet die erweiterte Eingabe; zuletzt benutzte Listen und Labels stehen vorn.",
        "Routinen: wiederkehrende Checklisten auf Wunsch als eigener Abschnitt in „Heute“.",
    ),
    "3.33.21": (
        "Hell oder dunkel wie das System: Einstellungen › Darstellung und Bedienung.",
        "Schmale Seitenleiste mit Symbolen: Ansicht › Seitenleiste schmal.",
        "Die Pinnwand braucht nur noch eine Werkzeugzeile; Seltenes steht unter „…“.",
        "Seiten zeigen ihren Titel groß und in leerem Zustand einen Schreibhinweis.",
        "Ruhigere Farben: Lila nur noch für Hinzufügen, eingeschaltete Schalter neutral.",
    ),
    "3.34.0": (
        "Bilder in Seiten überlappen nicht mehr; Drucken und PDF zeigen sie mit.",
        "Markdown mit Bildern: kopieren, speichern und wieder als Seite öffnen.",
        "Die Suche markiert Fundstellen in der geöffneten Seite.",
        "Gespeicherte Filter erklären, warum ein Punkt erscheint oder fehlt.",
        "Alt+Pfeile ordnen auch Seiten, Notizen und Zeichnungen in der Seitenleiste.",
    ),
    "3.35.0": (
        "Eine KI kann vorhandene Aufgaben überarbeiten: Kontextpaket hin, Vorschlag geprüft zurück.",
        "Sicherungen vergleichen zeigt, was sich zwischen zwei Ständen geändert hat.",
        "Pixel-Werkstatt: Farbe ändern mit Vorschau – Doppelklick auf die Farbleiste.",
        "Vor dem Symbolexport zeigt Glide 16, 32 und 48 Pixel auf hellem und dunklem Grund.",
    ),
}
# Bestand ohne gemerkte Version stammt aus der Zeit vor dieser Karte.
BEFORE_CATALOG = "3.33.18"


def version_tuple(text):
    """„3.33.20“ → (3, 33, 20); Unlesbares → None."""
    teile = str(text or "").strip().split(".")
    if not teile or not all(teil.isdigit() for teil in teile):
        return None
    return tuple(int(teil) for teil in teile)


def notes_since(last_seen, current, catalog=None):
    """Neuerungen der Versionen nach `last_seen` bis einschließlich `current`.

    Ohne gemerkte Version (erster Start) oder bei gleicher bzw. neuerer
    gemerkter Version: leer. Neueste Version zuerst, höchstens fünf Punkte je
    Version.
    """
    katalog = CATALOG if catalog is None else catalog
    alt, neu = version_tuple(last_seen), version_tuple(current)
    if alt is None or neu is None or alt >= neu:
        return []
    treffer = []
    for version, punkte in katalog.items():
        stand = version_tuple(version)
        if stand is not None and alt < stand <= neu and punkte:
            treffer.append((stand, version, list(punkte)[:5]))
    return [(version, punkte) for _stand, version, punkte in sorted(treffer, reverse=True)]


def normalize_seen(value):
    """Gemerkte Version als Text oder None, wenn sie nicht lesbar ist."""
    return value.strip() if isinstance(value, str) and version_tuple(value) is not None else None


def last_seen(settings, existing_install):
    """Gemerkte Version; ohne sie bei vorhandenem Bestand die Version vor dem Katalog."""
    gemerkt = (settings or {}).get("release_notes_seen")
    if isinstance(gemerkt, str) and version_tuple(gemerkt) is not None:
        return gemerkt
    return BEFORE_CATALOG if existing_install else None


def should_show(settings, current, catalog=None, existing_install=False):
    """True, wenn die Karte für `current` noch nicht gelesen ist und etwas zeigt."""
    return bool(notes_since(last_seen(settings, existing_install), current, catalog))


def remember_seen(settings, current):
    """Neue Einstellungen mit gemerkter Version; Original bleibt unverändert."""
    neu = dict(settings or {})
    neu["release_notes_seen"] = str(current)
    return neu
