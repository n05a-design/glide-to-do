"""Geometrie der mitgelieferten SVG-Logos, ohne Tk oder Dateizugriffe.

Unterstützt die freigegebenen Pfade (M/L/H/V/C/S/Z und matrix/translate/scale).
Die Canvas-Ausgabe verbindet Innenkonturen mit einer retracierten Brücke,
damit der ausgesparte Innenraum auch ohne SVG-Unterstützung transparent bleibt.
"""
import re
import xml.etree.ElementTree as ElementTree

_SVG_NS = "{http://www.w3.org/2000/svg}"

def _matrix(transform):
    """Eine Transformationsliste als Matrix (a, b, c, d, e, f); kennt matrix, translate, scale."""
    ergebnis = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    for art, werte in re.findall(r"(matrix|translate|scale)\s*\(([^)]*)\)", transform or ""):
        zahlen = [float(wert) for wert in re.split(r"[\s,]+", werte.strip()) if wert]
        if art == "matrix" and len(zahlen) == 6:
            schritt = tuple(zahlen)
        elif art == "translate":
            schritt = (1.0, 0.0, 0.0, 1.0, zahlen[0], zahlen[1] if len(zahlen) > 1 else 0.0)
        elif art == "scale":
            schritt = (zahlen[0], 0.0, 0.0, zahlen[1] if len(zahlen) > 1 else zahlen[0], 0.0, 0.0)
        else:
            raise ValueError(f"Unbekannte Transformation: {art}({werte})")
        ergebnis = _multiply(ergebnis, schritt)
    return ergebnis


def _multiply(m, n):
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + c * b2, b * a2 + d * b2, a * c2 + c * d2, b * c2 + d * d2,
            a * e2 + c * f2 + e, b * e2 + d * f2 + f)


def _apply(m, x, y):
    a, b, c, d, e, f = m
    return a * x + c * y + e, b * x + d * y + f


def _tokens(pfad):
    return re.findall(r"[A-Za-z]|-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", pfad)


def subpaths(pfad, schritte=10):
    """Zerlegt einen SVG-Pfad (M, L, H, V, C, S, Z – absolut und relativ) in Polygonzüge."""
    teile, aktuell = [], []
    zeichen = _tokens(pfad)
    i, befehl = 0, None
    x = y = start_x = start_y = 0.0
    control = None

    def zahl():
        nonlocal i
        wert = float(zeichen[i])
        i += 1
        return wert

    while i < len(zeichen):
        if re.fullmatch(r"[A-Za-z]", zeichen[i]):
            befehl = zeichen[i]
            i += 1
            if befehl in "Zz":
                if aktuell:
                    teile.append(aktuell)
                aktuell = []
                x, y = start_x, start_y
                control = None
                befehl = None
                continue
        if befehl is None:
            raise ValueError("Pfad beginnt ohne Befehl")
        relativ = befehl.islower()
        art = befehl.upper()
        if art == "M":
            if aktuell:
                teile.append(aktuell)
            nx, ny = zahl(), zahl()
            x, y = (x + nx, y + ny) if relativ else (nx, ny)
            start_x, start_y = x, y
            aktuell = [(x, y)]
            befehl = "l" if relativ else "L"
        elif art == "L":
            nx, ny = zahl(), zahl()
            x, y = (x + nx, y + ny) if relativ else (nx, ny)
            aktuell.append((x, y))
        elif art == "H":
            nx = zahl()
            x = x + nx if relativ else nx
            aktuell.append((x, y))
        elif art == "V":
            ny = zahl()
            y = y + ny if relativ else ny
            aktuell.append((x, y))
        elif art in ("C", "S"):
            werte = [zahl() for _ in range(6 if art == "C" else 4)]
            if relativ:
                werte = [wert + (x if index % 2 == 0 else y) for index, wert in enumerate(werte)]
            if art == "S":
                reflected = (2 * x - control[0], 2 * y - control[1]) if control else (x, y)
                werte = [*reflected, *werte]
            x1, y1, x2, y2, x3, y3 = werte
            for schritt in range(1, schritte + 1):
                t = schritt / schritte
                u = 1 - t
                aktuell.append((u ** 3 * x + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t ** 3 * x3,
                                u ** 3 * y + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t ** 3 * y3))
            x, y = x3, y3
            control = (x2, y2)
        else:
            raise ValueError(f"Pfadbefehl {befehl} wird nicht unterstützt")
        if art not in ("C", "S"):
            control = None
    if aktuell:
        teile.append(aktuell)
    return teile


def outline(svg):
    """Polygonzüge aller Flächen im Koordinatensystem des Masters (viewBox).

    Gelesen werden nur die mitgelieferten Master aus `resources/logo`, nie
    Dateien des Nutzers. Entitäten lehnt die Funktion trotzdem ab: Ein Master
    braucht keine, und so kann auch ein versehentlich getauschter keine
    Entitätenexpansion auslösen. Externe Verweise (die DTD im Kopf) lädt
    ElementTree ohnehin nicht.
    """
    text = svg
    if "<!ENTITY" in text:
        raise ValueError("SVG enthält Entitätsdefinitionen")
    wurzel = ElementTree.fromstring(text)
    ergebnis = []
    empty_classes = {name for name, styles in re.findall(r"\.([\w-]+)\s*\{([^}]+)\}", text)
                     if re.search(r"fill\s*:\s*none(?:\s*[;}])?", styles)}

    def laufen(knoten, matrix):
        matrix = _multiply(matrix, _matrix(knoten.get("transform")))
        if knoten.tag == _SVG_NS + "clipPath":
            return
        if knoten.tag == _SVG_NS + "path":
            stil = (knoten.get("style") or "") + " " + (knoten.get("fill") or "")
            if knoten.get("fill") != "none" and "fill:none" not in stil.replace(" ", "") and not (set((knoten.get("class") or "").split()) & empty_classes):
                for teil in subpaths(knoten.get("d") or ""):
                    ergebnis.append([_apply(matrix, px, py) for px, py in teil])
        for kind in knoten:
            laufen(kind, matrix)

    laufen(wurzel, (1.0, 0.0, 0.0, 1.0, 0.0, 0.0))
    if not ergebnis:
        raise ValueError("SVG enthält keine Fläche")
    return tuple(tuple(teil) for teil in ergebnis)


def signed_area(points):
    return sum(x * points[(i + 1) % len(points)][1] - points[(i + 1) % len(points)][0] * y
               for i, (x, y) in enumerate(points)) / 2


def contains(points, point):
    x, y = point
    inside = False
    for i, (x1, y1) in enumerate(points):
        x2, y2 = points[(i + 1) % len(points)]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def canvas_polygons(rings):
    """Outer contours with nested holes, for the approved compound logo paths."""
    parents = [next((j for j, other in sorted(enumerate(rings), key=lambda pair: abs(signed_area(pair[1])))
                     if j != i and abs(signed_area(other)) > abs(signed_area(ring)) and contains(other, ring[0])), None)
               for i, ring in enumerate(rings)]
    depth = []
    for parent in parents:
        level = 0
        while parent is not None:
            level += 1
            parent = parents[parent]
        depth.append(level)
    output = []
    for i, ring in enumerate(rings):
        if depth[i] % 2:
            continue
        polygon = list(ring)
        for j, hole in enumerate(rings):
            if parents[j] != i:
                continue
            hole = list(hole)
            if signed_area(polygon) * signed_area(hole) > 0:
                hole.reverse()
            # Retracing the bridge leaves zero area; opposite winding cuts the hole.
            hi = min(range(len(hole)), key=lambda k: hole[k][0])
            oi = min(range(len(polygon)), key=lambda k: (polygon[k][0] - hole[hi][0]) ** 2
                     + (polygon[k][1] - hole[hi][1]) ** 2)
            loop = hole[hi:] + hole[:hi] + [hole[hi]]
            polygon = polygon[:oi + 1] + loop + [polygon[oi]] + polygon[oi + 1:]
        output.append(tuple(polygon))
    return tuple(output)


def inline_styles(svg):
    """Inline simple class styles because Tk's SVG reader ignores style sheets."""
    if "<!ENTITY" in svg:
        raise ValueError("SVG enthält Entitätsdefinitionen")
    root = ElementTree.fromstring(svg)
    classes = {}
    for name, styles in re.findall(r"\.([\w-]+)\s*\{([^}]+)\}", svg):
        classes[name] = styles.strip()
    for node in root.iter():
        styles = [classes[name] for name in (node.get("class") or "").split() if name in classes]
        if styles:
            node.set("style", ";".join(styles + [node.get("style", "")]))
    ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    return ElementTree.tostring(root, encoding="unicode")


def tinted(svg, color):
    pattern = r"#0185e1\b|rgb\(\s*1\s*,\s*133\s*,\s*225\s*\)"
    if not re.search(pattern, svg, re.IGNORECASE):
        raise ValueError("Der Logo-Master trägt nicht die freigegebene Füllfarbe")
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", str(color or "")):
        raise ValueError(f"Keine Farbe im Format #RRGGBB: {color!r}")
    return inline_styles(re.sub(pattern, color, svg, flags=re.IGNORECASE))
