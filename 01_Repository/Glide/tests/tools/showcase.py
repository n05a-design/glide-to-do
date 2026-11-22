#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Erzeugt den Showcase „Stadtlicht“ mit echten App-APIs in einem temporären Bestand.

Eine Fotoreise durch Wuppertal, Berlin, München, Wien, Monaco, Bilbao und Seoul:
Reiseplan, Reiseführer mit Stadtseiten, Reisetagebuch, Galerie, Pixelstempel,
Routinen, Vorlagen und drei Pinnwände mit Bereichen und Verbindungen.
Bildquellen: PNG-Arbeitskopien eigener Fotos des Inhabers unter
tests/fixtures/showcase/bilder (Herkunft in quellen.json). `--sprache en`
erzeugt die englische Fassung unter tests/fixtures/showcase/en; Oberfläche,
Standardtitel und alle Beispieltexte folgen dann der englischen Sprache.
Alle Termine beziehen sich auf --tag; ohne Angabe auf den Erzeugungstag.
Kein Zugriff auf den persönlichen Glide-Datenordner, keine Laufzeitänderung.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from datetime import date, timedelta

from rundgang import load_module, ruhe

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "tests/fixtures/showcase"
BILDER = TARGET / "bilder"
SPRACHE = "de"


def tx(deutsch, englisch):
    """Beispieltext in der Sprache des gerade erzeugten Showcase."""
    return englisch if SPRACHE == "en" else deutsch


TITEL = {
    "de": {"BRIEFING_TITLE": "Reiseführer · Überblick", "MAIN_TITLE": "Reiseplan",
           "FOCUS_TASK": "Fotoauswahl für das Reisebuch treffen", "PHOTO_TITLE": "Stadtlicht · Auswahl",
           "PIXEL_TITLE": "Reisestempel · Lichtwechsel", "NOTIZ_TITLE": "Abendrunde · Offene Fragen",
           "PROJEKT": "Stadtlicht · Fotoreise", "PROFIL": "Unterwegs", "CANVAS": "Stadtlicht.canvas",
           "ROUTINEN": "Fotoroutinen", "BUCH": "Reiseführer", "JOURNAL": "Reisetagebuch",
           "VORLAGE": "{{Wochentag}} KW {{KW}} · {{Stadt}}", "FELD": "Stadt",
           "STADTSEITE": "Bilbao · Stahl und Licht", "LAYOUT_TASK": "Reisebuch-Layout bauen"},
    "en": {"BRIEFING_TITLE": "Travel guide · Overview", "MAIN_TITLE": "Travel plan",
           "FOCUS_TASK": "Choose photos for the travel book", "PHOTO_TITLE": "City Light · Selection",
           "PIXEL_TITLE": "Travel stamp · Light cycle", "NOTIZ_TITLE": "Evening round · Open questions",
           "PROJEKT": "City Light · Photo journey", "PROFIL": "On the road", "CANVAS": "City-Light.canvas",
           "ROUTINEN": "Photo routines", "BUCH": "Travel guide", "JOURNAL": "Travel diary",
           "VORLAGE": "{{Weekday}} week {{Week}} · {{City}}", "FELD": "City",
           "STADTSEITE": "Bilbao · Steel and light", "LAYOUT_TASK": "Build the travel book layout"},
}
# Deutsche Namen bleiben für bestehende Aufrufer als Modulkonstanten erhalten.
globals().update(TITEL["de"])


def ziel_fuer(sprache):
    return TARGET / "en" if sprache == "en" else TARGET


def staedte():
    """Reiseroute: Stadt, Tag relativ zum Bearbeitungstag, Region, Stimmung, zwei Fotos, Seite und Tagebuch."""
    return [
        {"key": "wuppertal", "name": "Wuppertal", "tag": -14, "region": "de", "mood": "happy",
         "fotos": [("Wuppertal-Schwebebahn.png", tx("Über der Wupper", "Above the Wupper"),
                    tx("Die Schwebebahn gleitet über den Fluss – der erste Morgen der Reise.",
                       "The suspension railway glides over the river – the first morning of the trip.")),
                   ("Wuppertal-Bahnsteig.png", tx("Stahl und Glas", "Steel and glass"),
                    tx("Bahnsteig unter dem Gerüst: Linien, die in die Tiefe ziehen.",
                       "A platform under the frame: lines that pull into the distance."))],
         "seite": tx("Wuppertal · Die Stadt am Gerüst", "Wuppertal · The city on a frame"),
         "text": tx("Die Schwebebahn hängt über der Wupper wie ein grüner Faden durch die Stadt. Am besten steht man "
                    "früh an einer Brücke und wartet auf den nächsten Wagen.",
                    "The suspension railway hangs over the Wupper like a green thread through the city. The best "
                    "spot is a bridge early in the morning, waiting for the next car."),
         "tabelle": [(tx("Brücke an der Kluse", "Bridge at Kluse"), tx("7–9 Uhr", "7–9 am"),
                      tx("Wagen kommen alle vier Minuten", "Cars every four minutes")),
                     (tx("Bahnsteig Vohwinkel", "Vohwinkel platform"), tx("Mittag", "Noon"),
                      tx("Schatten des Gerüsts nutzen", "Use the shadow of the frame"))],
         "zitat": tx("Man fährt nicht durch Wuppertal, man schwebt hindurch.",
                     "You don't travel through Wuppertal, you float through it."),
         "tagebuch": (tx("Start an der Wupper", "Starting at the Wupper"),
                      tx("Der erste Wagen kam pünktlich, das Licht noch weich. Drei Bilder, dann Kaffee am Bahnsteig. "
                         "Ein guter Anfang für zwei Wochen unterwegs.",
                         "The first car arrived on time, the light still soft. Three pictures, then coffee on the "
                         "platform. A good start for two weeks on the road."))},
        {"key": "berlin", "name": "Berlin", "tag": -12, "region": "de", "mood": "thoughtful",
         "fotos": [("Berlin-Nationalgalerie.png", tx("Ein Dach aus Stahl", "A roof of steel"),
                    tx("Die Neue Nationalgalerie in Schwarzweiß – fast nur Linie und Schatten.",
                       "The Neue Nationalgalerie in black and white – almost nothing but line and shadow.")),
                   ("Berlin-Spreeufer.png", tx("Glas an der Spree", "Glass on the Spree"),
                    tx("Der gläserne Würfel spiegelt Himmel und Wasser zugleich.",
                       "The glass cube mirrors sky and water at the same time."))],
         "seite": tx("Berlin · Beton, Glas und Himmel", "Berlin · Concrete, glass and sky"),
         "text": tx("Berlin belohnt Geduld: Unter dem großen Dach der Nationalgalerie verändert jede Wolke das Bild. "
                    "Am Hauptbahnhof spiegelt sich die Stadt in Glas und Wasser.",
                    "Berlin rewards patience: under the large roof of the Nationalgalerie every cloud changes the "
                    "picture. At the main station the city is mirrored in glass and water."),
         "tabelle": [(tx("Neue Nationalgalerie", "Neue Nationalgalerie"), tx("Vormittag", "Morning"),
                      tx("Schwarzweiß denken", "Think in black and white")),
                     (tx("Spreeufer am Hauptbahnhof", "Spree bank at the main station"), tx("Blaue Stunde", "Blue hour"),
                      tx("Spiegelung im Wasser abwarten", "Wait for the reflection in the water"))],
         "zitat": tx("Weniger Motiv, mehr Linie.", "Less subject, more line."),
         "tagebuch": (tx("Berlin in Grautönen", "Berlin in shades of grey"),
                      tx("Heute fast nur Schwarzweiß fotografiert. Das große Dach wirkt ohne Farbe noch ruhiger. "
                         "Abends an der Spree hat sich das Warten auf die blaue Stunde gelohnt.",
                         "Shot almost only black and white today. The large roof feels even calmer without colour. "
                         "In the evening by the Spree, waiting for the blue hour paid off."))},
        {"key": "muenchen", "name": tx("München", "Munich"), "tag": -10, "region": "de", "mood": "calm",
         "fotos": [("Muenchen-Arkade.png", tx("Licht im Bogengang", "Light in the arcade"),
                    tx("Streiflicht im Bogengang am Hofgarten – jeder Bogen ein eigener Rahmen.",
                       "Raking light in the arcade by the Hofgarten – every arch a frame of its own.")),
                   ("Muenchen-Zeltdach.png", tx("Das Zeltdach", "The tent roof"),
                    tx("Seile, Masten und Himmel: das Olympiadach von unten.",
                       "Cables, masts and sky: the Olympic roof from below."))],
         "seite": tx("München · Bögen und Seile", "Munich · Arches and cables"),
         "text": tx("Zwei Gesichter einer Stadt: die ruhigen Arkaden am Hofgarten und das leichte Dach im Olympiapark. "
                    "Beides lebt von Wiederholung.",
                    "Two faces of one city: the calm arcades by the Hofgarten and the light roof in the Olympic Park. "
                    "Both live from repetition."),
         "tabelle": [(tx("Hofgarten-Arkaden", "Hofgarten arcades"), tx("Später Nachmittag", "Late afternoon"),
                      tx("Tiefes Licht von Westen", "Low light from the west")),
                     (tx("Olympiapark", "Olympic Park"), tx("Klarer Himmel", "Clear sky"),
                      tx("Weitwinkel, von unten", "Wide angle, from below"))],
         "zitat": tx("Ein Bogen allein ist Architektur, zwanzig sind ein Rhythmus.",
                     "One arch is architecture, twenty are a rhythm."),
         "tagebuch": (tx("Rhythmus in München", "Rhythm in Munich"),
                      tx("Im Bogengang lag das Licht wie gezeichnet. Am Nachmittag unter dem Zeltdach gelegen und "
                         "nach oben fotografiert. Ruhiger Tag.",
                         "In the arcade the light looked drawn. In the afternoon I lay under the tent roof and shot "
                         "straight up. A calm day."))},
        {"key": "wien", "name": tx("Wien", "Vienna"), "tag": -8, "region": "at", "mood": "grateful",
         "fotos": [("Wien-Pavillon.png", tx("Grün und Gold", "Green and gold"),
                    tx("Ein Pavillon von Otto Wagner, Eisen und Ornament im Morgenlicht.",
                       "A pavilion by Otto Wagner, iron and ornament in the morning light.")),
                   ("Wien-Palmenhaus.png", tx("Glashaus", "Glass house"),
                    tx("Das Palmenhaus: ein langer Bogen aus Glas über dem Garten.",
                       "The Palmenhaus: a long arch of glass above the garden."))],
         "seite": tx("Wien · Eisen, Glas und Ornament", "Vienna · Iron, glass and ornament"),
         "text": tx("In Wien wird selbst eine Stadtbahnstation zum Schmuckstück. Wer früh kommt, hat den Pavillon fast "
                    "für sich; das Palmenhaus wirkt am besten bei bedecktem Himmel.",
                    "In Vienna even a city railway station becomes a jewel. Arrive early and you have the pavilion "
                    "almost to yourself; the Palmenhaus looks best under an overcast sky."),
         "tabelle": [(tx("Stadtbahn-Pavillon", "City railway pavilion"), tx("8 Uhr", "8 am"),
                      tx("Symmetrie von vorn", "Symmetry from the front")),
                     (tx("Palmenhaus", "Palmenhaus"), tx("Bedeckter Tag", "Overcast day"),
                      tx("Spiegelungen im Glas meiden", "Avoid reflections in the glass"))],
         "zitat": tx("Ornament ist hier keine Zugabe, sondern die Sprache.",
                     "Ornament here is not an extra, it is the language."),
         "tagebuch": (tx("Wien am Morgen", "Vienna in the morning"),
                      tx("Um acht stand ich allein vor dem Pavillon. Dankbar für diesen stillen Moment, bevor die "
                         "Stadt aufwacht.",
                         "At eight I stood alone in front of the pavilion. Grateful for that quiet moment before the "
                         "city woke up."))},
        {"key": "monaco", "name": "Monaco", "tag": -6, "region": "sued", "mood": "happy",
         "fotos": [("Monaco-Kueste.png", tx("Blick auf die Küste", "View of the coast"),
                    tx("Von oben: Hochhäuser, Hafen und Boote bis zum Horizont.",
                       "From above: towers, harbour and boats to the horizon.")),
                   ("Monaco-Treppe.png", tx("Warme Treppe", "Warm staircase"),
                    tx("Ein Bogen, eine Treppe, warmer Stein – Schatten wie gemalt.",
                       "An arch, a staircase, warm stone – shadows like a painting."))],
         "seite": tx("Monaco · Zwischen Fels und Meer", "Monaco · Between rock and sea"),
         "text": tx("Monaco ist steil. Wer die Treppen hinaufsteigt, bekommt den Blick über Hafen und Küste geschenkt. "
                    "In den Gassen darunter fangen Bögen das warme Licht.",
                    "Monaco is steep. Climb the stairs and you are rewarded with a view over harbour and coast. "
                    "In the lanes below, arches catch the warm light."),
         "tabelle": [(tx("Aussichtspunkt über der Stadt", "Viewpoint above the city"), tx("Vormittag", "Morning"),
                      tx("Teleobjektiv für die Boote", "Telephoto lens for the boats")),
                     (tx("Altstadttreppen", "Old town stairs"), tx("Mittag", "Noon"),
                      tx("Harte Schatten bewusst nutzen", "Use the hard shadows on purpose"))],
         "zitat": tx("Hier ist jede Treppe ein Aussichtspunkt.", "Here every staircase is a viewpoint."),
         "tagebuch": (tx("Hoch über Monaco", "High above Monaco"),
                      tx("Viele Stufen, ein großer Blick. Die Boote sahen von oben aus wie verstreute Reiskörner.",
                         "Many steps, one big view. From above, the boats looked like scattered grains of rice."))},
        {"key": "bilbao", "name": "Bilbao", "tag": -4, "region": "sued", "mood": "thoughtful",
         "fotos": [("Bilbao-Bruecke.png", tx("Rote Brücke", "Red bridge"),
                    tx("Die Schwebefähre: rotes Stahlgitter über der Flussmündung.",
                       "The transporter bridge: red steel lattice above the river mouth.")),
                   ("Bilbao-Bank.png", tx("Bank im Licht", "Bench in the light"),
                    tx("Eine Stahlbank mit einem roten Lichtakzent – schlicht und genau.",
                       "A steel bench with one red accent of light – simple and precise."))],
         "seite": tx("Bilbao · Stahl und Licht", "Bilbao · Steel and light"),
         "text": tx("Bilbao ist Stahl in allen Formen: als Brücke über der Mündung, als Fassade, als Bank im Licht. "
                    "Oben auf der Schwebefähre pfeift der Wind vom Atlantik.",
                    "Bilbao is steel in every form: a bridge above the estuary, a façade, a bench in the light. "
                    "On top of the transporter bridge the wind blows in from the Atlantic."),
         "tabelle": [(tx("Puente de Vizcaya", "Puente de Vizcaya"), tx("Nachmittag", "Afternoon"),
                      tx("Oben laufen, nach unten schauen", "Walk on top, look down")),
                     (tx("Stadion und Umgebung", "Stadium and surroundings"), tx("Abend", "Evening"),
                      tx("Licht und Stahl zusammen", "Light and steel together"))],
         "zitat": tx("Rot gegen Blau – mehr braucht das Bild nicht.", "Red against blue – the picture needs nothing more."),
         "tagebuch": (tx("Wind über Bilbao", "Wind over Bilbao"),
                      tx("Auf der Brücke war es stürmisch. Ich habe länger überlegt, ob das rote Gitter oder der "
                         "Himmel das eigentliche Motiv ist.",
                         "It was stormy on the bridge. I thought for a long time whether the red lattice or the sky "
                         "is the real subject."))},
        {"key": "seoul", "name": "Seoul", "tag": -2, "region": "kr", "mood": "calm",
         "fotos": [("Seoul-Turm.png", tx("Turm bei Nacht", "Tower at night"),
                    tx("Der N Seoul Tower leuchtet grün über dem Namsan.",
                       "N Seoul Tower glows green above Namsan.")),
                   ("Seoul-Gasse.png", tx("Altes Haus, neue Stadt", "Old house, new city"),
                    tx("Ein kleines Haus mit geschwungenem Dach zwischen den Hochhäusern.",
                       "A small house with a curved roof between the towers."))],
         "seite": tx("Seoul · Lichter am Abend", "Seoul · Lights in the evening"),
         "text": tx("Seoul wechselt im Minutentakt zwischen alt und neu. Abends leuchtet der Turm über allem, unten "
                    "in den Gassen stehen kleine Häuser mit geschwungenen Dächern.",
                    "Seoul switches between old and new every minute. In the evening the tower glows above it all, "
                    "while small houses with curved roofs stand in the lanes below."),
         "tabelle": [(tx("Namsan", "Namsan"), tx("Nach Sonnenuntergang", "After sunset"),
                      tx("Stativ mitnehmen", "Bring a tripod")),
                     (tx("Gassen in Jongno", "Lanes in Jongno"), tx("Früher Abend", "Early evening"),
                      tx("Leise sein, hier wohnen Menschen", "Be quiet, people live here"))],
         "zitat": tx("In Seoul ist die Nacht heller als mancher Tag.", "In Seoul the night is brighter than some days."),
         "tagebuch": (tx("Letzter Abend in Seoul", "Last evening in Seoul"),
                      tx("Mit Stativ auf dem Namsan. Der Turm wechselt die Farbe, die Stadt darunter wird zu einem "
                         "Lichtteppich. Ruhiges Ende einer langen Reise.",
                         "On Namsan with a tripod. The tower changes colour, the city below turns into a carpet of "
                         "light. A calm end to a long journey."))},
    ]


def etappen_daten():
    """Weg zur nächsten Stadt: (Beschriftung, Verkehrsmittel, Flug)."""
    return [(tx("ICE · 3 Std.", "ICE · 3 h"), tx("Bahn", "Train"), False),
            (tx("ICE · 4 Std.", "ICE · 4 h"), tx("Bahn", "Train"), False),
            (tx("Railjet · 4 Std.", "Railjet · 4 h"), tx("Bahn", "Train"), False),
            (tx("Flug nach Nizza", "Flight to Nice"), tx("Flug", "Flight"), True),
            (tx("Flug über Paris", "Flight via Paris"), tx("Flug", "Flight"), True),
            (tx("Langstrecke · 14 Std.", "Long haul · 14 h"), tx("Flug", "Flight"), True)]


def alle_fotos():
    """(Pfad, Galerietitel, Bildunterschrift, Stadt) in Reihenfolge der Route."""
    return [(BILDER / datei, titel, text, stadt["key"]) for stadt in staedte() for datei, titel, text in stadt["fotos"]]


def ueberblick_text():
    reihen = "\n".join(f"| {s['name']} | {tx('Tag', 'Day')} {i + 1} | {s['seite'].split(' · ')[1]} |"
                       for i, s in enumerate(staedte()))
    return tx("""## Sieben Städte, zwei Wochen

Eine Fotoreise mit der Bahn und zwei Flügen. Jede Stadt hat eine eigene Seite mit Orten, Zeiten und Tipps; das Reisetagebuch hält fest, wie es wirklich war.

BILD:

| Stadt | Etappe | Thema |
|---|---|---|
""", """## Seven cities, two weeks

A photo journey by train and two flights. Every city has its own page with places, times and tips; the travel diary records how it really was.

BILD:

| City | Leg | Theme |
|---|---|---|
""") + reihen + tx("""

> Gute Reisebilder entstehen, wenn man einen Ort zweimal besucht: einmal zum Ankommen, einmal zum Sehen.

---

### Vor dem Abflug

- [x] Route und Zugverbindungen festgelegt
- [ ] Ersatzakku und zweite Speicherkarte einpacken
- [ ] Offline-Karten für alle Städte laden

Packtipps für Fotoreisen
""", """

> Good travel pictures happen when you visit a place twice: once to arrive, once to see.

---

### Before departure

- [x] Route and train connections fixed
- [ ] Pack a spare battery and a second memory card
- [ ] Download offline maps for every city

Packing tips for photo journeys
""")


def stadt_text(stadt):
    zeilen = "\n".join(f"| {ort} | {zeit} | {tipp} |" for ort, zeit, tipp in stadt["tabelle"])
    return (f"## {stadt['seite'].split(' · ')[1]}\n\n{stadt['text']}\n\nBILD:\n\n"
            + tx("| Ort | Zeit | Tipp |", "| Place | Time | Tip |") + "\n|---|---|---|\n" + zeilen
            + f"\n\n> {stadt['zitat']}\n\n"
            + tx("TIPP: Erst ohne Kamera ankommen, dann fotografieren.",
                 "TIP: Arrive without the camera first, then take pictures.")
            + "\n\n### " + tx("Kamera", "Camera") + "\n\n```\nf/8 · 1/250 s · ISO 200\n```\n\n"
            + tx("- [x] Orte auf der Karte markiert\n- [ ] Beste Bilder in die Auswahl übernehmen\n",
                 "- [x] Places marked on the map\n- [ ] Add the best pictures to the selection\n"))


def kasse_text():
    return tx("""## Was die Reise gekostet hat

| Posten | Betrag | Notiz |
|---|---|---|
| Bahn (drei Etappen) | 214 € | Sparpreise, früh gebucht |
| Flüge | 1.180 € | Langstrecke ist der größte Posten |
| Unterkünfte | 1.420 € | 13 Nächte |
| Eintritte und Fahrkarten vor Ort | 165 € | Museen, U-Bahn, Schwebefähre |

> Nächstes Mal die Langstrecke zuerst buchen.
""", """## What the journey cost

| Item | Amount | Note |
|---|---|---|
| Trains (three legs) | €214 | Saver fares, booked early |
| Flights | €1,180 | The long haul is the biggest item |
| Accommodation | €1,420 | 13 nights |
| Tickets and local transport | €165 | Museums, metro, transporter bridge |

> Next time, book the long haul first.
""")


def abendrunde_text():
    return tx("""## Abend nach der Rückkehr

Die Reise ist vorbei, die Auswahl beginnt. Aus rund 230 Bildern sollen 14 ins Reisebuch.

- Pro Stadt zwei Bilder, die zusammen eine kleine Geschichte erzählen.
- Schwarzweiß nur dort, wo die Linie wichtiger ist als die Farbe.
- Die Reihenfolge folgt der Route, nicht der Lieblingsstadt.

> Lieber eine starke Seite pro Stadt als drei mittelmäßige.
""", """## Evening after coming home

The journey is over, the selection begins. Out of roughly 230 pictures, 14 should go into the travel book.

- Two pictures per city that tell a small story together.
- Black and white only where line matters more than colour.
- The order follows the route, not the favourite city.

> Better one strong page per city than three mediocre ones.
""")


def letzter_werktag(anchor):
    """Letzter Montag–Freitag des Monats von `anchor`, sonst des Folgemonats."""
    jahr, monat = anchor.year, anchor.month
    while True:
        tag = date(jahr + monat // 12, monat % 12 + 1, 1) - timedelta(days=1)
        while tag.weekday() > 4:
            tag -= timedelta(days=1)
        if tag >= anchor:
            return tag
        jahr, monat = jahr + monat // 12, monat % 12 + 1


def zweiter_dienstag(anchor):
    """Zweiter Dienstag des Monats von `anchor`, sonst des Folgemonats."""
    jahr, monat = anchor.year, anchor.month
    while True:
        erster = date(jahr, monat, 1)
        tag = erster + timedelta(days=(1 - erster.weekday()) % 7 + 7)
        if tag >= anchor:
            return tag
        jahr, monat = (jahr + 1, 1) if monat == 12 else (jahr, monat + 1)


def reisestempel(mod, light):
    """Briefmarke mit Zahnrand, Stadtsilhouette und wechselndem Himmelslicht (32 × 32)."""
    bild = mod.glide_drawing.DrawingModel.blank(32)

    def rechteck(x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                bild.set_cell(xx, yy, color)

    rechteck(0, 0, 32, 32, "#F4EFE4")
    for i in range(0, 32, 2):  # Zahnrand
        for x, y in ((i, 0), (i, 31), (0, i), (31, i)):
            bild.set_cell(x, y, "#1B2B34")
    rechteck(3, 3, 26, 26, "#1B2B34")
    rechteck(4, 4, 24, 16, light)
    rechteck(20, 6, 4, 4, "#FFF3C4")  # Sonne oder Mond
    for x, h in ((5, 6), (8, 9), (11, 5), (14, 11), (17, 7), (20, 10), (23, 6), (26, 8)):
        rechteck(x, 20 - h, 2, h, "#2E4A57")  # Silhouette
    rechteck(15, 6, 1, 3, "#2E4A57")  # Turmspitze
    rechteck(4, 20, 24, 8, "#2F6F7A")
    for x in range(5, 27, 4):
        rechteck(x, 23, 2, 1, "#9FD3D6")  # Wellen
    return bild


def bildfolge(mod):
    colors = ("#F2B37A", "#8FC3E8", "#5A6FB0", "#1F2A55")
    frames = [{"id": f"frame-{index}", "drawing": reisestempel(mod, color).to_document(), "duration_ms": None}
              for index, color in enumerate(colors, 1)]
    return {"format": mod.glide_animation.FORMAT, "format_version": mod.glide_animation.FORMAT_VERSION,
            "width": 32, "height": 32, "duration_ms": 400, "frames": frames}


def kamera_symbol(mod):
    icon = mod.glide_drawing.DrawingModel.blank(16)
    for y in range(5, 13):
        for x in range(2, 14):
            icon.set_cell(x, y, "#2E4A57")
    for x in range(5, 9):
        icon.set_cell(x, 4, "#2E4A57")
    for y in range(7, 11):
        for x in range(6, 10):
            icon.set_cell(x, y, "#F2B37A")
    icon.set_cell(11, 6, "#F4EFE4")
    return icon


def build(app, mod, root, anchor):
    """Zusammenhängende Dokumente; zurückgegeben wird die portable Projektwahl."""
    T = TITEL[SPRACHE]
    STAEDTE = staedte()
    FOTOS = alle_fotos()
    tag = lambda offset: (anchor + timedelta(days=offset)).isoformat()
    app.flush_rich_note()
    app.settings["daily_hints"] = {}
    app.lists = [entry for entry in app.lists if entry.get("system_role") == "inbox"]
    app.folders = []
    labels = {}
    for key, name, color in (("Foto", tx("Foto", "Photo"), "accent"), ("Buchung", tx("Buchung", "Booking"), "clear"),
                             ("Unterwegs", tx("Unterwegs", "On the way"), "export"),
                             ("Freigabe", tx("Freigabe", "Approval"), "flag"),
                             ("Warten", tx("Warten", "Waiting"), "due_action")):
        label = app.new_label_object(name, color=color)
        app.labels.append(label)
        labels[key] = label["id"]
    icon_doc = kamera_symbol(mod).to_document()
    attachments_dir = Path(mod.BASE_DIR) / "showcase-quellen"
    attachments_dir.mkdir(parents=True, exist_ok=True)
    route_csv = tx("Etappe;Von;Nach;Verkehrsmittel;Weg\n", "Leg;From;To;Transport;Route\n") + "".join(
        f"{i};{a['name']};{b['name']};{mittel};{weg}\n"
        for i, (a, b, (weg, mittel, _flug)) in enumerate(zip(STAEDTE, STAEDTE[1:], etappen_daten()), 1))
    generated = {
        tx("Reisestempel.png", "Travel-stamp.png"): reisestempel(mod, "#8FC3E8").to_png(scale=8),
        tx("Kamera-Symbol.ico", "Camera-icon.ico"): kamera_symbol(mod).to_ico(),
        tx("Stadtlicht-Palette.gpl", "City-Light-palette.gpl"):
            mod.glide_drawing.palette_to_gpl(tx("Stadtlicht", "City Light"), ["#2E4A57", "#F2B37A", "#8FC3E8"]).encode(),
        tx("Stadtlicht-Palette.hex", "City-Light-palette.hex"):
            mod.glide_drawing.palette_to_hex(["#2E4A57", "#F2B37A", "#8FC3E8"]).encode(),
        tx("Route.csv", "Route.csv"): route_csv.encode(),
        tx("Reisebuch-Notizen.txt", "Travel-book-notes.txt"): tx(
            "Stadtlicht · Reisebuch\nFormat 21 × 21 cm, eine Doppelseite pro Stadt.\nUmschlag: Schwebebahn am Morgen.\n",
            "City Light · Travel book\nFormat 21 × 21 cm, one spread per city.\nCover: the suspension railway in the morning.\n").encode(),
    }
    erzeugt = {}
    for name, content in generated.items():
        path = attachments_dir / name
        path.write_bytes(content)
        erzeugt[name.split(".")[-1] if name.endswith((".png", ".ico", ".gpl", ".hex", ".csv", ".txt")) else name] = \
            app.store_attachment(str(path))
    project = app.new_folder_object(T["PROJEKT"], color="accent", icon=icon_doc,
                                    note=tx("Eine Fotoreise durch sieben Städte: Planung, Auswahl und Reisebuch.",
                                            "A photo journey through seven cities: planning, selection and travel book."))
    library = app.new_folder_object(T["BUCH"], parent_id=None, folder_kind="library", color="clear",
                                    note=tx("Eine Seite pro Stadt mit Orten, Zeiten und Tipps.",
                                            "One page per city with places, times and tips."))
    journal = app.new_folder_object(T["JOURNAL"], parent_id=None, folder_kind="journal", color="confirm")
    archive = app.new_folder_object(tx("Archiv · Erste Route", "Archive · First route"), parent_id=project["id"],
                                    archived=True, archived_at=tag(-30)+"T16:00:00+02:00")
    app.folders.extend([project, library, journal, archive])
    stored = {str(pfad): app.store_attachment(str(pfad)) for pfad, _t, _n, _s in FOTOS}
    assert all(stored.values()), "Ein Beispielbild konnte nicht eingelesen werden."
    foto = lambda datei: copy.deepcopy(stored[str(BILDER / datei)])
    # Ein Anhang am Ordner bleibt beim Projektimport erhalten.
    project["attachments"] = [copy.deepcopy(erzeugt["txt"])]

    def task(text, **kwargs):
        return app.new_item(text, **kwargs)

    focus = task(T["FOCUS_TASK"], due=tag(0), due_time="11:00", importance=3,
        planned_date=tag(0), planned_time="09:00", estimated_minutes=90, time_spent_minutes=35,
        labels=[labels["Foto"], labels["Freigabe"]],
        description=tx("Pro Stadt zwei Bilder auswählen, die zusammen eine kleine Geschichte erzählen.",
                       "Choose two pictures per city that tell a small story together."),
        attachments=[foto("Wuppertal-Schwebebahn.png")],
        checklist=[{"text": tx("Rohdaten gesichert", "Raw files backed up"), "done": True},
                   {"text": tx("Erste Auswahl mit Sternen markiert", "First selection marked with stars"), "done": True},
                   {"text": tx("Zweite Runde: Schwarzweiß prüfen", "Second round: check black and white")}])
    layout = task(tx("Reisebuch-Layout bauen", "Build the travel book layout"), kind=app.ITEM_KIND_LONG, due=tag(2),
        planned_date=tag(0), planned_time="13:30", estimated_minutes=120, importance=2, labels=[labels["Foto"]],
        description=tx("21 × 21 cm, eine Doppelseite pro Stadt. Links das ruhige Bild, rechts das Detail.",
                       "21 × 21 cm, one spread per city. The calm picture on the left, the detail on the right."),
        blocked_by=[focus["id"]], color="clear", attachments=[copy.deepcopy(erzeugt["txt"])],
        checklist=[{"text": tx("Format festgelegt", "Format settled"), "done": True},
                   {"text": tx("Schrift für Bildunterschriften", "Typeface for captions")},
                   {"text": tx("Probedruck bestellen", "Order a test print")}])
    captions = task(tx("Bildunterschriften schreiben", "Write the captions"), due=tag(1), planned_date=tag(0),
        planned_time="11:00", estimated_minutes=45, importance=2, labels=[labels["Foto"]],
        attachments=[foto("Berlin-Nationalgalerie.png"), foto("Seoul-Turm.png")],
        description=tx("Kurz, mit Ort und Moment. Keine Kameradaten in die Unterschrift.",
                       "Short, with place and moment. No camera data in the caption."))
    share = task(tx("Reisebericht an Freunde schicken", "Send the travel report to friends"), due=tag(4), importance=3,
        labels=[labels["Freigabe"]], blocked_by=[layout["id"]], links=[focus["id"]],
        attachments=[copy.deepcopy(erzeugt["csv"])],
        reminder={"mode": "fixed", "at": app.local_reminder_time(tag(4), "10:00")},
        description=tx("Link zur Galerie und die Route als Tabelle mitschicken.",
                       "Send the gallery link and the route as a table."))
    booked = task(tx("Zug Wuppertal → Berlin gebucht", "Booked the train Wuppertal → Berlin"), done=True,
                  done_at=tag(-20)+"T14:30:00+02:00", labels=[labels["Buchung"]],
                  planned_date=tag(-20), estimated_minutes=20, time_spent_minutes=15)
    waiting = task(tx("Rechnung vom Hotel in Bilbao anfordern", "Request the invoice from the hotel in Bilbao"),
                   due=tag(-1), importance=1, labels=[labels["Warten"], labels["Buchung"]],
                   description=tx("Mail ist raus, Antwort steht noch aus.", "Email sent, reply still pending."))
    tasche = task(tx("Kameratasche ausräumen", "Unpack the camera bag"), kind=app.ITEM_KIND_GROUP, children=[
        task(tx("Akkus laden", "Charge the batteries"), due=tag(1), estimated_minutes=10),
        task(tx("Sensor reinigen lassen", "Have the sensor cleaned"), due=tag(5), estimated_minutes=30),
        task(tx("Speicherkarten gesichert", "Memory cards backed up"), done=True, done_at=tag(0)+"T08:30:00+02:00")])
    main = app.new_list_object(T["MAIN_TITLE"], [
        task(tx("Vorbereitung", "Preparation"), kind=app.ITEM_KIND_HEADING), booked, waiting,
        task(tx("Nach der Reise", "After the journey"), kind=app.ITEM_KIND_HEADING), focus, captions, layout, share,
        tasche], folder_id=project["id"], labels=[labels["Foto"]], icon=icon_doc, color="accent",
        attachments=[copy.deepcopy(erzeugt["csv"])],
        note=tx("Von der Bahnbuchung bis zum fertigen Reisebuch.", "From the train booking to the finished travel book."))
    note = app.new_list_object(T["NOTIZ_TITLE"], [
        task(tx("Zweite Meinung zur Auswahl einholen", "Get a second opinion on the selection"), due=tag(0)),
        task(tx("Lieblingsbild je Stadt markieren", "Mark the favourite picture per city"), planned_date=tag(1),
             estimated_minutes=30)],
        folder_id=project["id"], list_kind="note",
        rich_note=mod.glide_page_markdown.markdown_to_page(abendrunde_text()),
        labels=[labels["Foto"]], attachments=[copy.deepcopy(erzeugt["csv"])])
    gallery = app.new_list_object(T["PHOTO_TITLE"], [], folder_id=project["id"], list_kind="gallery",
        attachments=[copy.deepcopy(stored[str(pfad)]) for pfad, _t, _n, _s in FOTOS],
        note=tx("Vierzehn Bilder, zwei pro Stadt, in der Reihenfolge der Route.",
                "Fourteen pictures, two per city, in the order of the route."))
    animation = bildfolge(mod)
    drawing = app.new_list_object(T["PIXEL_TITLE"], [], folder_id=None, list_kind="drawing",
        drawing=copy.deepcopy(animation["frames"][0]["drawing"]), animation=animation, icon=icon_doc,
        attachments=[copy.deepcopy(erzeugt["png"]), copy.deepcopy(erzeugt["ico"])],
        drawing_reference={"attachment_id": erzeugt["png"]["id"], "mode": "fit", "zoom_percent": 100},
        note=tx("Ein Reisestempel mit vier Himmelsfarben von Morgen bis Nacht, PNG-Referenz und 16-Pixel-Symbol.",
                "A travel stamp with four sky colours from morning to night, a PNG reference and a 16-pixel icon."))
    app.lists.extend([main, note, gallery, drawing])
    for pfad, titel, text, _stadt in FOTOS:
        app.set_gallery_caption(gallery["id"], stored[str(pfad)]["id"], titel, text)
    wechsel = app.new_list_object(tx("Vor jedem Stadtwechsel", "Before every change of city"),
        [task(tx("Akkus und Powerbank laden", "Charge batteries and power bank")),
         task(tx("Bilder des Tages sichern", "Back up the day's pictures"), done=True),
         task(tx("Fahrkarte und Unterkunft prüfen", "Check ticket and accommodation")),
         task(tx("Objektive reinigen", "Clean the lenses"))],
        folder_id=project["id"], recurring_checklist=True, color="due_action",
        attachments=[copy.deepcopy(erzeugt["csv"])])
    repeats = []
    for index, (title, rule, offset) in enumerate([
        (tx("Bilder des Tages sichern", "Back up the day's pictures"), {"art": "taeglich"}, 0),
        (tx("Wochenauswahl in die Galerie", "Weekly selection into the gallery"), {"art": "woechentlich"}, 1),
        (tx("Objektive reinigen", "Clean the lenses"), {"art": "tage", "abstand": 14}, 2),
        (tx("Fotowalk in der eigenen Stadt", "Photo walk in your own city"), {"art": "wochentage", "tage": [2, 5]}, 3),
        (tx("Archiv auf zweite Platte spiegeln", "Mirror the archive to a second drive"), {"art": "monatlich"}, 5),
        (tx("Jahresbuch zusammenstellen", "Put together the yearbook"), {"art": "jaehrlich"}, 7),
        # Serie aus FP-02 (3.44.0): erster Termin ist der nächste letzte Werktag.
        (tx("Monatsrückblick ins Tagebuch", "Monthly review in the diary"),
         {"art": "serie", "rrule": "FREQ=MONTHLY;INTERVAL=1;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1"},
         (letzter_werktag(anchor) - anchor).days),
        # Erweiterte Rhythmen FP-02 Stufe 2 (3.44.0): n-ter Wochentag, Bezug auf
        # Erledigung, begrenzte Anzahl und Pause.
        (tx("Fotoclub am zweiten Dienstag", "Photo club on the second Tuesday"),
         {"art": "serie", "rrule": "FREQ=MONTHLY;INTERVAL=1;BYDAY=2TU"}, (zweiter_dienstag(anchor) - anchor).days),
        (tx("Pflanzen gießen", "Water the plants"), {"art": "tage", "abstand": 3, "bezug": "erledigt"}, 1),
        (tx("Abzüge beim Labor nachfragen", "Follow up on prints at the lab"), {"art": "woechentlich", "rest": 3}, 4),
        (tx("Reisekasse abrechnen", "Settle the travel kitty"), {"art": "monatlich", "pausiert": True}, 10)]):
        repeats.append(task(title, due=tag(offset), repeat=rule, reminder={"mode": "relative", "minutes": 30},
                            due_time="09:00", estimated_minutes=15,
                            labels=[labels[("Foto", "Unterwegs", "Buchung", "Warten")[index % 4]]]))
    rhythm = app.new_list_object(T["ROUTINEN"], repeats, folder_id=project["id"],
        note=tx("Alle sieben Wiederholungsarten, Serien am letzten Werktag und am zweiten Dienstag, Abstand nach "
                "Erledigung, begrenzte Anzahl und eine pausierte Reihe; Systembenachrichtigungen sind im Showcase "
                "ausgeschaltet.",
                "All seven repeat types, series on the last weekday and the second Tuesday, interval after "
                "completion, a limited count and a paused series; system notifications are off in the showcase."))
    rhythm["items"].insert(2, task(tx("Bildunterschriften gegenlesen", "Proofread the captions"), due=tag(3),
        planned_date=tag(2), labels=[labels["Foto"], labels["Freigabe"]], estimated_minutes=30))
    app.lists.extend([wechsel, rhythm])
    inbox = next(entry for entry in app.lists if entry.get("system_role") == "inbox")
    inbox["items"] = [task(tx("Postkarte aus Wien einscannen", "Scan the postcard from Vienna"), labels=[labels["Foto"]]),
                      task(tx("Freundin wegen Seoul-Tipps zurückrufen", "Call a friend back about Seoul tips"),
                           description=tx("Sie fliegt im Frühjahr und möchte die Orte vom Namsan.",
                                          "She flies in spring and wants the spots on Namsan."))]
    # Reisetagebuch: ein Eintrag pro Stadt plus der Abend nach der Rückkehr.
    for stadt in STAEDTE:
        titel, text = stadt["tagebuch"]
        app.lists.append(app.new_list_object(titel, [], folder_id=journal["id"], list_kind="note",
            rich_note=mod.glide_page_markdown.markdown_to_page("# " + titel + "\n\n" + text),
            journal={"moment_date": tag(stadt["tag"]), "mood": stadt["mood"],
                     "favorite": stadt["key"] in ("wien", "seoul"), "location": stadt["name"],
                     "prompt": tx("Was möchte ich von heute bewahren?", "What do I want to keep from today?")}))
    heimkehr = tx("Wieder zu Hause", "Back home")
    app.lists.append(app.new_list_object(heimkehr, [], folder_id=journal["id"], list_kind="note",
        rich_note=mod.glide_page_markdown.markdown_to_page("# " + heimkehr + "\n\n" + tx(
            "Koffer ausgepackt, Bilder gesichert. Morgen beginnt die Auswahl.",
            "Suitcase unpacked, pictures backed up. Tomorrow the selection begins.")),
        journal={"moment_date": tag(0), "mood": "grateful", "favorite": False, "location": T["PROFIL"],
                 "prompt": tx("Was nehme ich von dieser Reise mit?", "What do I take away from this journey?")}))
    app.lists.append(app.new_list_object(tx("Erste Route über Paris", "First route via Paris"), [
        task(tx("Zugverbindung über Paris prüfen", "Check the train connection via Paris"), done=True,
             done_at=tag(-32)+"T12:00:00+02:00"),
        task(tx("Route wegen Flugzeiten geändert", "Route changed because of flight times"), done=True,
             done_at=tag(-31)+"T15:00:00+02:00")], folder_id=archive["id"], archived=True,
        archived_at=tag(-30)+"T16:00:00+02:00"))
    app.save_items()
    # Reiseführer: Überblick und eine Seite pro Stadt; Bilder über den echten Editorweg.
    briefing = app.new_page_from_markdown(ueberblick_text(), title=T["BRIEFING_TITLE"], folder_id=library["id"])
    seiten = {}
    for stadt in STAEDTE:
        seiten[stadt["key"]] = app.new_page_from_markdown(stadt_text(stadt), title=stadt["seite"],
                                                          folder_id=library["id"])
    # Eine schlichte Seite ohne Titelbild und ohne Bilder: Kostentabelle der Reise.
    app.new_page_from_markdown(kasse_text(), title=tx("Reisekasse", "Travel kitty"), folder_id=library["id"])
    ruhe(root)
    modes = ("right", "left", "center")

    def bild_einsetzen(page, datei, mode, width):
        app.set_active_list(page["id"])
        ruhe(root)
        editor = app.rich_note_editor
        lines = editor.text.get("1.0", "end-1c").splitlines()
        number = next(i for i, line in enumerate(lines, 1) if line.startswith("BILD:"))
        editor.text.delete(f"{number}.0", f"{number}.end")  # Ankerwort dient nur der Platzierung
        key = editor.insert_images([str(BILDER / datei)], f"{number}.0")[0]
        editor.images[key].update(mode=mode, width=width)
        return editor, editor.images[key]["attachment"]

    for index, stadt in enumerate(STAEDTE):
        page = seiten[stadt["key"]]
        mode = modes[index % 3]
        editor, attachment_id = bild_einsetzen(page, stadt["fotos"][0][0], mode, 420 if mode == "center" else 250)
        # Hinweiszeile als Hervorhebung (Callout).
        lines = editor.text.get("1.0", "end-1c").splitlines()
        line = next(i for i, text in enumerate(lines, 1) if text.startswith(("TIPP:", "TIP:")))
        editor.text.mark_set("insert", f"{line}.0")
        editor.convert_block("callout")
        editor.flush()
        ruhe(root)
        page = next(entry for entry in app.lists if entry["id"] == page["id"])
        page["cover"] = {"kind": "image", "attachment": attachment_id}
        page["icon"] = icon_doc if index == 0 else None
    editor, _attachment = bild_einsetzen(briefing, "Wuppertal-Schwebebahn.png", "center", 420)
    # Klappblock mit echten semantischen Tags.
    lines = editor.text.get("1.0", "end-1c").splitlines()
    kopf = tx("Packtipps für Fotoreisen", "Packing tips for photo journeys")
    line = next(i for i, text in enumerate(lines, 1) if text.startswith(kopf))
    editor.text.delete(f"{line}.0", f"{line}.end")
    editor.text.insert(f"{line}.0", kopf + "\n" + tx(
        "Ein Zoom und eine kleine Festbrennweite reichen.\nStativ nur für die Abende einplanen.\n"
        "Jeden Abend sichern, bevor neue Bilder dazukommen.",
        "One zoom and one small prime lens are enough.\nPlan the tripod only for the evenings.\n"
        "Back up every evening before new pictures arrive."))
    editor.text.mark_set("insert", f"{line}.0")
    editor.convert_block("toggle")
    for number in range(line + 1, line + 4):
        editor.text.tag_add("indent1", f"{number}.0", f"{number}.end")
    editor.set_toggle_open(f"{line}.0", False)
    editor.flush()
    ruhe(root)
    # Live-Liste, Titelbild aus der Pixelzeichnung und lokale Verweise (G29/G08).
    briefing = next(entry for entry in app.lists if entry["id"] == briefing["id"])
    briefing["live_lists"] = mod.glide_pages.live_lists([mod.glide_objects.uri("list", main["id"])])
    briefing["cover"] = {"kind": "drawing", "document": copy.deepcopy(animation["frames"][1]["drawing"])}
    briefing["icon"] = icon_doc
    note["references"] = mod.glide_objects.normalize([mod.glide_objects.uri("item", focus["id"]),
                                                      mod.glide_objects.uri("list", briefing["id"]),
                                                      mod.glide_objects.uri("list", gallery["id"])])
    focus["references"] = mod.glide_objects.normalize([mod.glide_objects.uri("list", gallery["id"])])
    app.save_items()
    ruhe(root)
    # Zwei kleine, portable Vorlagen ergänzen den mitgelieferten Katalog.
    meeting_template = app.capture_template(list_id=note["id"])
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    meeting_template["title"] = T["VORLAGE"]
    meeting_template["note"] = tx("Abendnotiz für jeden Reisetag: Datumsfelder füllen sich selbst, die Stadt wird "
                                  "abgefragt. Aufgaben und Anhang bleiben enthalten.",
                                  "Evening note for every travel day: date fields fill themselves, the city is asked "
                                  "for. Tasks and attachment are kept.")
    routine_template = app.capture_template(list_id=wechsel["id"])
    routine_template = next(t for t in app.templates if t["id"] == routine_template["id"])
    routine_template["title"] = tx("Reise · Stadtwechsel", "Journey · Change of city")
    meeting_template = next(t for t in app.templates if t["id"] == meeting_template["id"])
    settings = copy.deepcopy(app.settings)
    # Projektpinnwand: Regionen als Bereiche, Etappen als beschriftete Verbindungen.
    positionen = {"wuppertal": (28, 64), "berlin": (248, 64), "muenchen": (468, 64), "wien": (28, 404),
                  "monaco": (348, 404), "bilbao": (568, 404), "seoul": (808, 64)}
    page_card = lambda page, x, y, scale="small": {"list_id": page["id"], "item_id": "page:" + page["id"],
                                                    "x": x, "y": y, "scale": scale}
    board_cards = [page_card(seiten[key], x, y) for key, (x, y) in positionen.items()]
    board_cards += [{"list_id": main["id"], "item_id": focus["id"], "x": 808, "y": 404, "scale": "large"},
                    {"list_id": main["id"], "item_id": layout["id"], "x": 808, "y": 720, "scale": "normal"},
                    page_card(drawing, 568, 720)]
    etappen = []
    for a, b, (weg, _mittel, flug) in zip(STAEDTE, STAEDTE[1:], etappen_daten()):
        etappen.append({"from": "page:" + seiten[a["key"]]["id"], "to": "page:" + seiten[b["key"]]["id"],
                        "label": weg, "dash": flug})
    etappen.append({"from": "page:" + seiten["seoul"]["id"], "to": focus["id"],
                    "label": tx("zurück: Auswahl", "back: selection")})
    etappen.append({"from": focus["id"], "to": layout["id"], "label": tx("dann Layout", "then layout")})
    bereiche = [
        {"id": "region-de", "name": tx("Deutschland · Bahn", "Germany · Train"), "color": "accent",
         "x": 8, "y": 16, "w": 700, "h": 320},
        {"id": "region-at", "name": tx("Österreich", "Austria"), "color": "confirm", "x": 8, "y": 356, "w": 300, "h": 320},
        {"id": "region-sued", "name": tx("Mittelmeer und Atlantik", "Mediterranean and Atlantic"), "color": "export",
         "x": 328, "y": 356, "w": 460, "h": 320},
        {"id": "region-kr", "name": tx("Korea", "Korea"), "color": "flag", "x": 788, "y": 16, "w": 260, "h": 320},
        {"id": "nach-der-reise", "name": tx("Nach der Reise", "After the journey"), "color": "clear",
         "x": 548, "y": 696, "w": 500, "h": 320}]
    folder_scope = "folder:" + project["id"]
    list_scope = "list:" + main["id"]
    settings.update(profile_name=T["PROFIL"], start_on_home=True, show_home_stats=True, language=SPRACHE,
        sidebar_sections_visible={"pages": True, "lists": True, "notes": True, "drawings": True},
        sidebar_locations={},
        mascot_name="Gismo", mascot_playful=False, system_notifications=False,
        pinned_pages=[{"kind": "list", "id": briefing["id"]}, {"kind": "folder", "id": library["id"]}],
        recent_lists=[{"id": entry["id"], "edited_at": tag(0)+"T10:00:00+02:00"}
                      for entry in [briefing, note, gallery, drawing]],
        page_favorites=[briefing["id"], seiten["seoul"]["id"], seiten["wien"]["id"]],
        page_recent=[briefing["id"], seiten["bilbao"]["id"]],
        gallery_tile_size={gallery["id"]: "large"},
        list_group_by={main["id"]: "importance"},
        saved_filters=[{"id": "showcase-freigabe", "name": tx("Reise · Freigaben", "Journey · Approvals"), "query": "",
                        "label_ids": [labels["Freigabe"]], "list_ids": [main["id"]], "status": "open"},
                       {"id": "showcase-woche", "name": tx("Diese Woche · Eisenhower", "This week · Eisenhower"),
                        "query": "", "label_ids": [], "list_ids": [], "status": "open"}],
        # FP-03 (3.44.0): gespeicherte Bedingungen und Darstellung je Ansicht.
        saved_view_conditions_v1={"showcase-woche": {"mode": "any", "planned": "this_week", "effort": "at_least",
                                                     "minutes": 30}},
        saved_view_layouts_v1={"showcase-woche": {"display": "table", "group": "eisenhower", "sort": "due",
                                                  "columns": ["title", "source", "due", "planned_date",
                                                              "estimated_minutes", "importance"]}},
        # Realistischer Tag (D57/WA-12): Kapazität je Wochentag und Tagesziel.
        daily_capacity_by_weekday=[300, 360, 300, 240, 150, 120, None], daily_goal=4,
        completion_history={tag(-2): 2, tag(-1): 1, tag(0): 2},
        # Reiter (bis zwölf) und ein eigener KI-Auftrag für den Dateiaustausch (FP-06).
        open_tabs=[{"list_id": main["id"], "item_id": focus["id"], "used": 1},
                   {"list_id": main["id"], "item_id": layout["id"], "used": 2}],
        exchange_recipes=[{"id": "showcase-reisebericht",
                           "title": tx("Reisebericht aus Tagebuch entwerfen", "Draft a travel report from the diary"),
                           "mode": "patch", "instruction": tx(
                               "Fasse die ausgewählten Aufgaben zu einer kurzen Liste für den Reisebericht zusammen "
                               "und schlage höchstens eine Checkliste je Aufgabe vor. Ändere keine Termine.",
                               "Summarize the selected tasks into a short list for the travel report and suggest at "
                               "most one checklist per task. Do not change any dates.")}],
        active_tab={folder_scope: "board", list_scope: "list"},
        pinboards={folder_scope: {"cards": board_cards, "layout": "free", "background": "dots", "width": 200,
            "areas": bereiche, "connections": etappen,
            "show_description": True, "show_checklist": True, "color_mode": "header"},
            list_scope: {"cards": [{"list_id": main["id"], "item_id": item["id"], "x": 0, "y": 0, "scale": "normal"}
                                   for item in (focus, captions, layout, share)],
                         "layout": "columns", "group_by": "planned", "background": "grid",
                         "show_checklist": True, "color_mode": "stripe"},
            mod.ItemWorkspace.GLOBAL_SCOPE: {
                "cards": [
                    {"list_id": briefing["id"], "item_id": "page:"+briefing["id"], "x": 34, "y": 63, "scale": "normal"},
                    {"list_id": note["id"], "item_id": "page:"+note["id"], "x": 34, "y": 355, "scale": "normal"},
                    {"list_id": main["id"], "item_id": focus["id"], "x": 390, "y": 64, "scale": "large"},
                    {"list_id": main["id"], "item_id": captions["id"], "x": 735, "y": 58, "scale": "normal"},
                    {"list_id": drawing["id"], "item_id": "page:"+drawing["id"], "x": 735, "y": 470, "scale": "small"},
                ],
                "layout": "free", "width": 238, "background": "lines", "show_checklist": True,
                "areas": [{"id": "global-auswahl", "name": tx("Auswahl und Reisebuch", "Selection and travel book"),
                           "color": "accent", "x": 370, "y": 30, "w": 640, "h": 620}],
                "connections": [
                    {"from": "page:"+briefing["id"], "to": focus["id"], "label": tx("Route ansehen", "Review the route")},
                    {"from": "page:"+note["id"], "to": focus["id"], "label": tx("Fragen klären", "Settle questions")},
                    {"from": focus["id"], "to": captions["id"], "label": tx("dann beschriften", "then caption")},
                    {"from": captions["id"], "to": "page:"+drawing["id"], "label": tx("Stempel aufs Cover", "Stamp on the cover"),
                     "dash": True},
                ]}})
    app.settings = app.normalize_personal_settings(settings)
    app.save_settings()
    app.save_templates()
    app.set_active_list(briefing["id"])
    app.sync_all_item_kind_labels()
    app.save_items()
    payload = app.partial_backup_payload([drawing["id"]], [project["id"], library["id"], journal["id"]])
    payload["pinboards"] = {scope: board for scope, board in app.exportable_pinboards().items()
                           if scope != mod.ItemWorkspace.GLOBAL_SCOPE}
    return payload, [meeting_template, routine_template]


def export(target, anchor, sprache="de"):
    global SPRACHE
    SPRACHE = sprache
    T = TITEL[sprache]
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="glide-showcase-erzeugen-") as directory:
        mod = load_module(Path(directory)/"Glide")
        root = mod.tk.Tk()
        root.geometry("1440x960+20+30")
        errors = []
        root.report_callback_exception = lambda *args: errors.append(str(args[1]))
        app = mod.ListApp(root)
        app.show_info = lambda *a, **k: None
        app.show_warning = app.show_error = lambda *a, **k: errors.append(str(a))
        try:
            # Sprache vor dem Aufbau: Standardtitel, Eingang und mitgelieferte Vorlagen folgen ihr (D93).
            app.settings["language"] = sprache
            mod.glide_i18n.set_language(sprache)
            app.templates = app.localize_builtin_templates(app.templates)
            app.ensure_inbox_list()
            ruhe(root)
            payload, templates = build(app, mod, root, anchor)
            paths = [target/"Glide-Showcase.glidebackup", target/"Glide-Showcase_App.glideapp",
                     target/"Glide-Showcase.glidetemplates"]
            app.write_complete_backup(str(paths[0]), payload)
            app.write_complete_backup(str(paths[1]), app.app_backup_payload())
            app.write_json_atomic(str(paths[2]), {"format_version": app.TEMPLATE_FORMAT_VERSION, "templates": templates})
            # Zeilenenden wie im Repository (LF): Unter Windows schreibt die App
            # CRLF, und die Prüfsumme im Manifest passte nach dem Einchecken nicht.
            paths[2].write_bytes(paths[2].read_bytes().replace(b"\r\n", b"\n"))
            app.open_global_board()
            ruhe(root)
            canvas = target / T["CANVAS"]
            assert app.export_board_json_canvas(str(canvas)) == str(canvas)
            canvas.write_bytes(canvas.read_bytes().replace(b"\r\n", b"\n"))
            paths.append(canvas)
            ruhe(root)
            assert not errors, errors
            manifest = {"app_version": mod.APP_VERSION, "format_version": app.DATA_SCHEMA_VERSION, "sprache": sprache,
                "thema": T["PROJEKT"], "bearbeitungstag": anchor.isoformat(),
                "listen": len(app.lists),
                "dokumente": [{"titel": e["title"], "art": e["list_kind"]} for e in payload["lists"]],
                "bilder": len(alle_fotos()),
                "seitenbilder": sum(len((e.get("rich_note") or {}).get("images") or {}) for e in payload["lists"]),
                "projektpinnwaende": len(payload["pinboards"]), "vorlagen": len(templates),
                "dateien": {p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
                            for p in paths}}
            (target/"manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n",
                                                encoding="utf-8", newline="\n")
            print(json.dumps(manifest, ensure_ascii=False, indent=2))
        finally:
            root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ziel", type=Path)
    parser.add_argument("--tag", type=date.fromisoformat, default=date.today())
    parser.add_argument("--sprache", choices=("de", "en"), default="de")
    args = parser.parse_args()
    export((args.ziel or ziel_fuer(args.sprache)).expanduser().resolve(), args.tag, args.sprache)


if __name__ == "__main__":
    main()
