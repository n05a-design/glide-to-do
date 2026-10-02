"""Abschnitte der Ansicht „Heute“ ohne Tk (Entscheidung D14).

„Heute“ ersetzt „Mein Tag“ und beantwortet eine Frage: was ist heute dran?
Oben steht die eine nächste Aufgabe, darunter Verspätetes, Liegengebliebenes,
der Tagesplan und was heute fällig ist; am Ende der Eingang. Künftige
Fälligkeiten gehören nach „Demnächst“ (bisher „In Bearbeitung“).

Jede Aufgabe steht genau einmal. Ein Eintrag ist ein Tupel, dessen letztes
Element der Punkt ist – die Tupelform der Übersichten
``(Fälligkeit, Listenindex, Punktindex, Quellliste, Punkt)`` ebenso wie die
des Eingangs ``(Quellliste, Punkt)``.
"""
from collections import namedtuple

# Reihenfolge der Abschnitte von oben nach unten.
ABSCHNITTE = ("naechste", "verspaetet", "liegen", "plan", "faellig", "eingang")
# „demnaechst“ ist kein Abschnitt, sondern zählt für den Verweis am Ende, was
# später fällig ist und deshalb in „Demnächst“ steht.
Abschnitte = namedtuple("Abschnitte", ABSCHNITTE + ("demnaechst",))


def _tag(value):
    """ISO-Datum als Text oder None – ohne Uhrzeit, ohne Prüfung des Kalenders."""
    text = str(value or "")[:10]
    return text if len(text) == 10 and text[4] == "-" and text[7] == "-" else None


def _punkt(eintrag):
    return eintrag[-1]


def einordnung(item, tag, heute):
    """In welchen Abschnitt eine Aufgabe gehört, die nicht am Tag eingeplant ist.

    Am heutigen Tag: „verspaetet“ (Fälligkeit vorbei), „faellig“ (heute
    fällig), „liegen“ (an einem früheren Tag eingeplant und offen geblieben).
    An einem anderen Tag zählt nur „faellig“ an genau diesem Tag. Erledigtes
    und alles Übrige liefert None.
    """
    if item.get("done"):
        return None
    faellig = _tag(item.get("due"))
    if tag != heute:
        return "faellig" if faellig == tag else None
    geplant = _tag(item.get("planned_date"))
    if faellig and faellig < heute:
        return "verspaetet"
    if faellig == heute:
        return "faellig"
    if geplant and geplant < heute:
        return "liegen"
    return None


def abschnitte(geplant, bestand, eingang, tag, heute, rang=None, hoechste_stufe=None):
    """Teilt die Einträge eines Tags auf die Abschnitte auf.

    ``geplant`` sind die Einträge mit Bearbeitungstag ``tag`` in ihrer
    Reihenfolge; ``bestand`` alle übrigen Kandidaten, ``eingang`` die Punkte
    des Eingangs ohne Bearbeitungstag. ``rang`` bestimmt die nächste Aufgabe
    (kleiner ist dringender); ``hoechste_stufe`` begrenzt sie auf Stufen bis
    einschließlich dieses Werts – dieselbe Grenze wie auf der Startseite.
    Die nächste Aufgabe gibt es nur am heutigen Tag; sie wird aus ihrem
    Abschnitt herausgenommen.
    """
    belegt = {id(_punkt(eintrag)) for eintrag in geplant}
    gruppen = {"verspaetet": [], "liegen": [], "faellig": []}
    spaeter = []
    for eintrag in bestand:
        item = _punkt(eintrag)
        if id(item) in belegt:
            continue
        ziel = einordnung(item, tag, heute)
        if ziel is None:
            faellig = _tag(item.get("due"))
            if tag == heute and not item.get("done") and faellig and faellig > heute:
                spaeter.append(eintrag)
            continue
        belegt.add(id(item))
        gruppen[ziel].append(eintrag)
    gruppen["verspaetet"].sort(key=lambda eintrag: _tag(_punkt(eintrag).get("due")) or "")
    gruppen["liegen"].sort(key=lambda eintrag: _tag(_punkt(eintrag).get("planned_date")) or "")
    plan = list(geplant)
    naechste = None
    if tag == heute and rang is not None:
        kandidaten = []
        for eintrag in plan + gruppen["verspaetet"] + gruppen["liegen"] + gruppen["faellig"]:
            item = _punkt(eintrag)
            if item.get("done"):
                continue
            wert = rang(item)
            if hoechste_stufe is not None and wert[0] > hoechste_stufe:
                continue
            kandidaten.append((wert, eintrag))
        if kandidaten:
            naechste = min(kandidaten, key=lambda paar: paar[0])[1]
    if naechste is not None:
        plan = [eintrag for eintrag in plan if eintrag is not naechste]
        for name in gruppen:
            gruppen[name] = [eintrag for eintrag in gruppen[name] if eintrag is not naechste]
    rest = [eintrag for eintrag in eingang if id(_punkt(eintrag)) not in belegt]
    return Abschnitte(naechste, gruppen["verspaetet"], gruppen["liegen"], plan, gruppen["faellig"], rest,
                      [eintrag for eintrag in spaeter if id(_punkt(eintrag)) not in belegt])


def leer(teile):
    """True, wenn kein Abschnitt etwas zeigt; der Verweis auf „Demnächst“ zählt nicht."""
    return teile.naechste is None and not any(getattr(teile, name) for name in ABSCHNITTE[1:])
