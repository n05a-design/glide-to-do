"""Routinen in „Heute“ ohne Tk (AU06 seit 3.33.20).

Eine Routine ist eine vorhandene Aufgabenliste mit wiederkehrender Checkliste,
die der Nutzer für „Heute“ ausgewählt hat. Es gibt kein neues Datenfeld: Die
Auswahl und der Tag des letzten vollständigen Durchgangs sind lokale
Anzeigeeinstellungen (wie die Bereichszuordnung der Seitenleiste). Glide führt
keine Gewohnheitsstatistik (G06 vorerst nicht); gezeigt wird nur, was heute
offen ist und ob die Routine heute schon einmal vollständig war.
"""

from datetime import date

# Obergrenze der gemerkten Auswahl; mehr Routinen trägt „Heute“ nicht sinnvoll.
MAX_ROUTINES = 20


def normalize_selection(ids):
    """Gespeicherte Auswahl: eindeutige Kennungen in Reihenfolge, höchstens MAX_ROUTINES."""
    if not isinstance(ids, list):
        return []
    return list(dict.fromkeys(kennung for kennung in ids if isinstance(kennung, str) and kennung))[:MAX_ROUTINES]


def normalize_done_days(value):
    """Gemerkte Tage vollständiger Durchgänge: Kennung → ISO-Datum; Unlesbares entfällt."""
    if not isinstance(value, dict):
        return {}
    ergebnis = {}
    for kennung, tag in value.items():
        if not (isinstance(kennung, str) and kennung and isinstance(tag, str)):
            continue
        try:
            date.fromisoformat(tag)
        except ValueError:
            continue
        ergebnis[kennung] = tag
    return ergebnis


def is_candidate(entry):
    """Aufgabenliste mit wiederkehrender Checkliste, weder archiviert noch Eingang."""
    return (isinstance(entry, dict) and entry.get("list_kind", "tasks") == "tasks"
            and entry.get("recurring_checklist") is True and not entry.get("archived")
            and entry.get("system_role") != "inbox")


def selected(lists, ids, archived_folder=lambda _folder_id: False):
    """Ausgewählte Routinen in der Reihenfolge der Auswahl; fehlende entfallen."""
    nach_id = {entry.get("id"): entry for entry in lists if isinstance(entry, dict)}
    ergebnis = []
    for kennung in ids or ():
        entry = nach_id.get(kennung)
        if is_candidate(entry) and not archived_folder(entry.get("folder_id")):
            ergebnis.append(entry)
    return ergebnis


def walk(items):
    for item in items or ():
        if isinstance(item, dict):
            yield item
            yield from walk(item.get("children"))


def tasks(entry):
    """Abhakbare Punkte einer Routine einschließlich Unteraufgaben."""
    return [item for item in walk(entry.get("items")) if item.get("kind", "task") == "task"]


def section(entries, done_days, today):
    """Zeilen des Abschnitts „Routinen“.

    Je Routine: Kennung, Titel, erledigte/gesamte Punkte, offene Punkte in
    Listenreihenfolge und ob sie heute schon vollständig war. Eine Routine
    ohne abhakbare Punkte erscheint nicht.
    """
    zeilen = []
    for entry in entries:
        punkte = tasks(entry)
        if not punkte:
            continue
        erledigt = sum(1 for item in punkte if item.get("done"))
        zeilen.append({
            "list_id": entry.get("id"),
            "title": str(entry.get("title") or "Routine"),
            "done": erledigt,
            "total": len(punkte),
            "open": [item.get("id") for item in punkte if not item.get("done")],
            "completed_today": (done_days or {}).get(entry.get("id")) == today,
        })
    return zeilen


def remember_completion(done_days, list_id, today, valid_ids=None):
    """Tag des vollständigen Durchgangs merken; Einträge fehlender Listen entfallen."""
    ergebnis = {key: value for key, value in (done_days or {}).items()
                if isinstance(key, str) and isinstance(value, str)
                and (valid_ids is None or key in valid_ids)}
    ergebnis[list_id] = today
    return ergebnis


def toggled(ids, list_id):
    """Auswahl umschalten: hinzufügen am Ende oder entfernen."""
    ids = [kennung for kennung in ids or () if isinstance(kennung, str)]
    return [kennung for kennung in ids if kennung != list_id] if list_id in ids else ids + [list_id]


def summary(zeile):
    """Kurzer Fortschrittstext für die Abschnittszeile."""
    if zeile["completed_today"] and not zeile["open"]:
        return f"{zeile['title']} · heute erledigt"
    if zeile["completed_today"]:
        return f"{zeile['title']} · heute schon einmal erledigt · {zeile['done']}/{zeile['total']}"
    return f"{zeile['title']} · {zeile['done']}/{zeile['total']}"
