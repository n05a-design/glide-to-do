# SPDX-License-Identifier: MPL-2.0
"""Projektübersicht aus echten Glide-Daten, ohne Tk (Ecosystem E04).

Ein Projekt ist ein oberster Ordner mit allen Unterordnern; Aufgaben sind die
Punkte der Aufgabenlisten darin (Seiten, Notizen, Zeichnungen zählen nicht).
Berechnet werden nur Werte mit belastbarer Grundlage im Datenmodell:
offen/erledigt (`done`), überfällig und anstehend (`due` gegen das heutige
Datum), Erledigungen je Tag (`done_at`) und Verteilung nach Wichtigkeit
(`importance`). Auslastung und Abhängigkeiten werden bewusst nicht berechnet:
Das Datenmodell hat dafür keine verlässliche Grundlage.

`summary(lists, folders, today, days=56, horizon=30)` liefert ein Wörterbuch
mit `projects` (je Projekt: id, title, open, done, overdue, next_due), `totals`,
`completions` (ISO-Datum → Anzahl, nur Tage mit Erledigungen im Zeitraum),
`due_soon` (Liste von (project id, item id, title, Tage bis Fälligkeit)),
`importance` (Stufe → offene Anzahl) und `week` (erledigt in den letzten 7
Tagen und in den 7 Tagen davor).
"""
from __future__ import annotations

import datetime as dt

TASK_KINDS = (None, "", "tasks")
NO_PROJECT = "__none__"


def _date(value):
    try:
        return dt.date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _root(folder_id, parents):
    gesehen = set()
    while folder_id in parents and parents[folder_id] and folder_id not in gesehen:
        gesehen.add(folder_id)
        folder_id = parents[folder_id]
    return folder_id


def summary(lists, folders, today, days=56, horizon=30, no_project_title="Ohne Projekt"):
    parents = {f.get("id"): f.get("parent_id") for f in folders if isinstance(f, dict)}
    titel = {f.get("id"): f.get("title") or "" for f in folders if isinstance(f, dict)}
    projekte = {}
    erledigungen = {}
    bald = []
    wichtigkeit = {}
    woche = {"last_7": 0, "previous_7": 0}
    start = today - dt.timedelta(days=days - 1)
    for liste in lists:
        if not isinstance(liste, dict) or liste.get("list_kind") not in TASK_KINDS or liste.get("archived"):
            continue
        ordner = liste.get("folder_id")
        pid = _root(ordner, parents) if ordner in parents else NO_PROJECT
        projekt = projekte.setdefault(pid, {"id": pid, "title": titel.get(pid) or no_project_title, "open": 0, "done": 0,
                                           "overdue": 0, "next_due": None})
        for punkt in liste.get("items") or []:
            if not isinstance(punkt, dict):
                continue
            if punkt.get("done"):
                projekt["done"] += 1
                tag = _date(punkt.get("done_at"))
                if tag is not None:
                    if start <= tag <= today:
                        erledigungen[tag.isoformat()] = erledigungen.get(tag.isoformat(), 0) + 1
                    abstand = (today - tag).days
                    if 0 <= abstand < 7:
                        woche["last_7"] += 1
                    elif 7 <= abstand < 14:
                        woche["previous_7"] += 1
                continue
            projekt["open"] += 1
            stufe = punkt.get("importance") or "none"
            wichtigkeit[stufe] = wichtigkeit.get(stufe, 0) + 1
            faellig = _date(punkt.get("due"))
            if faellig is None:
                continue
            if faellig < today:
                projekt["overdue"] += 1
            elif (faellig - today).days <= horizon:
                bald.append((pid, punkt.get("id"), punkt.get("text") or "", (faellig - today).days))
            if faellig >= today and (projekt["next_due"] is None or faellig.isoformat() < projekt["next_due"]):
                projekt["next_due"] = faellig.isoformat()
    liste_projekte = sorted(projekte.values(), key=lambda p: (p["id"] == NO_PROJECT, p["title"].casefold()))
    gesamt = {k: sum(p[k] for p in liste_projekte) for k in ("open", "done", "overdue")}
    return {"projects": liste_projekte, "totals": gesamt, "completions": erledigungen,
            "due_soon": sorted(bald, key=lambda x: x[3])[:60], "importance": wichtigkeit, "week": woche,
            "period": (start.isoformat(), today.isoformat())}
