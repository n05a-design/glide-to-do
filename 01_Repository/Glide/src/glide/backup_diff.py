"""Zwei Sicherungsstände vergleichen, ohne Tk und ohne Schreibzugriff (F-03 seit 3.35.0).

Verglichen werden zwei bereits gelesene Datenstände (dasselbe JSON wie
`liste_speicher.json`, eine automatische Sicherung oder der Datenteil einer
Backupdatei): Listen und Aufgaben neu, entfernt, verschoben oder mit
geänderten Feldern. Dieses Modul liest und schreibt keine Dateien.
"""
import json

LIST_FIELDS = (("title", "Titel"), ("folder_id", "Ordner"), ("list_kind", "Art"), ("note", "Notiz"),
               ("archived", "Archiviert"), ("rich_note", "Seitentext"), ("labels", "Labels"),
               ("color", "Farbe"))
ITEM_FIELDS = (("text", "Titel"), ("done", "Erledigt"), ("kind", "Art"), ("due", "Fälligkeit"),
               ("due_time", "Uhrzeit"), ("planned_date", "Bearbeitungstag"), ("planned_time", "Zeitfenster"),
               ("importance", "Wichtigkeit"), ("labels", "Labels"), ("description", "Beschreibung"),
               ("repeat", "Wiederholung"), ("reminder", "Erinnerung"), ("estimated_minutes", "Aufwand"),
               ("checklist", "Checkliste"), ("attachments", "Anhänge"), ("color", "Farbe"))
LEER = (None, "", [], {}, False, 0)


def walk(items, parent_id=None):
    """Alle Punkte einer Liste mit der Kennung ihres Elternpunkts."""
    for item in items or ():
        if isinstance(item, dict):
            yield item, parent_id
            yield from walk(item.get("children"), item.get("id"))


def index(data):
    """(Listen nach Kennung, Punkte nach Kennung → (Punkt, Listenkennung, Elternkennung))."""
    listen, punkte = {}, {}
    for entry in (data or {}).get("lists") or ():
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        listen[entry["id"]] = entry
        for item, parent in walk(entry.get("items")):
            if item.get("id"):
                punkte[item["id"]] = (item, entry["id"], parent)
    return listen, punkte


def _gleich(a, b):
    if a in LEER and b in LEER:
        return True
    return json.dumps(a, sort_keys=True, ensure_ascii=False, default=str) == \
        json.dumps(b, sort_keys=True, ensure_ascii=False, default=str)


def describe(value, limit=60):
    """Kurze, lesbare Form eines Feldwerts."""
    if value in LEER and value is not False and value != 0:
        return "–"
    if isinstance(value, bool):
        return "ja" if value else "nein"
    if isinstance(value, dict) and "text" in value and isinstance(value.get("text"), str):
        value = value["text"]
    if isinstance(value, (list, tuple)):
        teile = [describe(teil, limit) for teil in value]
        text = ", ".join(teile) if all(isinstance(t, str) for t in teile) else str(len(value))
    elif isinstance(value, dict):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    else:
        text = " ".join(str(value).split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def field_changes(alt, neu, felder):
    return [(titel, describe(alt.get(key)), describe(neu.get(key)))
            for key, titel in felder if not _gleich(alt.get(key), neu.get(key))]


def compare(alt, neu):
    """Unterschied zweier Datenstände; ändert keinen von beiden."""
    listen_alt, punkte_alt = index(alt)
    listen_neu, punkte_neu = index(neu)

    def titel(listen, kennung):
        return str((listen.get(kennung) or {}).get("title") or "Liste")

    ergebnis = {"lists_added": [], "lists_removed": [], "lists_changed": [],
                "items_added": [], "items_removed": [], "items_moved": [], "items_changed": []}
    for kennung, entry in listen_neu.items():
        if kennung not in listen_alt:
            ergebnis["lists_added"].append((kennung, titel(listen_neu, kennung)))
        else:
            aenderungen = field_changes(listen_alt[kennung], entry, LIST_FIELDS)
            if aenderungen:
                ergebnis["lists_changed"].append((kennung, titel(listen_neu, kennung), aenderungen))
    for kennung in listen_alt:
        if kennung not in listen_neu:
            ergebnis["lists_removed"].append((kennung, titel(listen_alt, kennung)))
    for kennung, (item, liste, _eltern) in punkte_neu.items():
        name = describe(item.get("text"), 80)
        if kennung not in punkte_alt:
            ergebnis["items_added"].append((kennung, name, titel(listen_neu, liste)))
            continue
        vorher, liste_vorher, eltern_vorher = punkte_alt[kennung]
        if liste_vorher != liste:
            ergebnis["items_moved"].append((kennung, name, titel(listen_alt, liste_vorher), titel(listen_neu, liste)))
        aenderungen = field_changes(vorher, item, ITEM_FIELDS)
        if aenderungen:
            ergebnis["items_changed"].append((kennung, name, titel(listen_neu, liste), aenderungen))
    for kennung, (item, liste, _eltern) in punkte_alt.items():
        if kennung not in punkte_neu:
            ergebnis["items_removed"].append((kennung, describe(item.get("text"), 80), titel(listen_alt, liste)))
    return ergebnis


def summary(ergebnis):
    """Ein Satz mit den Zahlen je Art, z. B. für den Kopf des Vergleichs."""
    teile = [("lists_added", "Listen neu"), ("lists_removed", "Listen entfernt"),
             ("lists_changed", "Listen geändert"), ("items_added", "Aufgaben neu"),
             ("items_removed", "Aufgaben entfernt"), ("items_moved", "Aufgaben verschoben"),
             ("items_changed", "Aufgaben geändert")]
    text = [f"{len(ergebnis[key])} {name}" for key, name in teile if ergebnis[key]]
    return " · ".join(text) if text else "Keine Unterschiede bei Listen und Aufgaben"
