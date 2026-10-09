"""KI-Austausch Stufe 2 ohne Tk: Kontextpaket und Änderungsvorschläge (G24 seit 3.35.0).

Stufe 1 (`mode: "create"`) legt nur Neues an. Stufe 2 schickt einer KI ein
Kontextpaket mit dem Ausgangsstand ausgewählter Aufgaben und nimmt einen
Änderungsvorschlag (`mode: "patch"`) zurück. Jede Änderung nennt die Aufgabe
über einen stabilen Verweis und den Ausgangsstand als Prüfsumme. Stimmt der
Ausgangsstand nicht mehr, ist das ein Konflikt – nie wird still überschrieben.

Keine internen Kennungen: Verweise sind Prüfsummen über die Kennung, aus denen
Glide die Aufgabe wiederfindet, die aber nichts über den Bestand verraten.
Dieses Modul liest und schreibt keine Dateien und ändert keine Daten.
"""
import hashlib
import json
import re

FORMAT = "glide.exchange"
CONTEXT_FORMAT = "glide.context"
VERSION = 2
FIELDS = ("title", "description", "importance", "due", "due_time", "planned_date", "estimated_minutes",
          "done", "labels")
FIELD_NAMES = {"title": "Titel", "description": "Beschreibung", "importance": "Wichtigkeit",
               "due": "Fälligkeit", "due_time": "Uhrzeit", "planned_date": "Bearbeitungstag",
               "estimated_minutes": "Aufwand", "done": "Erledigt", "labels": "Labels"}
MAX_CHANGES = 5000
_DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_UHRZEIT = re.compile(r"^([01]\d|2[0-3]):[0-5]\d$")


def ref(identity):
    """Stabiler Verweis auf eine Kennung, ohne die Kennung zu zeigen."""
    return "r-" + hashlib.sha256(b"glide-ref\0" + str(identity).encode("utf-8")).hexdigest()[:16]


def item_state(item, label_names):
    """Austauschfelder einer Aufgabe; `label_names` übersetzt Labelkennungen in Namen."""
    return {
        "title": str(item.get("text") or ""),
        "description": str(item.get("description") or ""),
        "importance": int(item.get("importance") or 0),
        "due": item.get("due") or None,
        "due_time": item.get("due_time") or None,
        "planned_date": item.get("planned_date") or None,
        "estimated_minutes": item.get("estimated_minutes") if item.get("estimated_minutes") else None,
        "done": bool(item.get("done")),
        "labels": sorted(label_names.get(kennung, "") for kennung in item.get("labels") or ()
                         if label_names.get(kennung)),
    }


def checksum(state):
    """Prüfsumme des Ausgangsstands (kanonisches JSON)."""
    text = json.dumps(state, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def build_context(eintraege, label_names, created_at="", application_version=""):
    """Kontextpaket aus [(Liste, Punkt, Elternpunkt oder None)].

    Je Liste ein Objekt mit Titel und Beschreibung, je Aufgabe ihr Verweis,
    ihr Ausgangsstand und dessen Prüfsumme.
    """
    listen, aufgaben = {}, []
    for liste, item, eltern in eintraege:
        listen.setdefault(liste.get("id"), {"ref": ref(liste.get("id")), "kind": "list",
                                             "title": str(liste.get("title") or ""),
                                             "description": str(liste.get("note") or "")})
        zustand = item_state(item, label_names)
        aufgaben.append({"ref": ref(item.get("id")), "kind": "item", "list": ref(liste.get("id")),
                         "parent": ref(eltern.get("id")) if eltern else None,
                         "base": checksum(zustand), "fields": zustand})
    return {"format": CONTEXT_FORMAT, "format_version": VERSION, "created_at": created_at,
            "application_version": application_version,
            "instructions": ("Antworte mit einer Datei im Format glide.exchange, format_version 2, "
                             "mode \"patch\": changes = [{ref, base, set: {Feld: neuer Wert}}]. "
                             "Übernimm ref und base unverändert aus diesem Paket."),
            "fields": list(FIELDS), "lists": list(listen.values()), "items": aufgaben}


class PatchError(ValueError):
    """Die Datei ist kein gültiger Änderungsvorschlag."""


def parse_patch(data):
    """Prüft Rahmen und Form eines Änderungsvorschlags; liefert die Liste der Änderungen."""
    if not isinstance(data, dict):
        raise PatchError("Die Datei enthält kein JSON-Objekt.")
    if data.get("format") != FORMAT:
        raise PatchError("Das Format heißt nicht „glide.exchange“.")
    if data.get("format_version") != VERSION or data.get("mode") != "patch":
        raise PatchError("Erwartet wird format_version 2 mit mode „patch“.")
    changes = data.get("changes")
    if not isinstance(changes, list) or not changes:
        raise PatchError("Der Vorschlag enthält keine Änderungen.")
    if len(changes) > MAX_CHANGES:
        raise PatchError(f"Höchstens {MAX_CHANGES} Änderungen je Datei.")
    ergebnis = []
    for nummer, change in enumerate(changes, 1):
        if (not isinstance(change, dict) or not isinstance(change.get("ref"), str)
                or not isinstance(change.get("base"), str) or not isinstance(change.get("set"), dict)):
            raise PatchError(f"Änderung {nummer}: ref, base und set fehlen oder haben die falsche Form.")
        ergebnis.append(change)
    return ergebnis


def validate_value(feld, wert):
    """Normalisierter Wert oder ValueError mit einer verständlichen Meldung."""
    if feld == "title":
        if not isinstance(wert, str) or not wert.strip() or len(wert) > 500:
            raise ValueError("Titel muss Text mit 1 bis 500 Zeichen sein")
        return " ".join(wert.split())
    if feld == "description":
        if not isinstance(wert, str) or len(wert) > 20000:
            raise ValueError("Beschreibung muss Text bis 20.000 Zeichen sein")
        return wert
    if feld == "importance":
        if isinstance(wert, bool) or not isinstance(wert, int) or not 0 <= wert <= 3:
            raise ValueError("Wichtigkeit muss 0 bis 3 sein")
        return wert
    if feld in ("due", "planned_date"):
        if wert is None:
            return None
        if not isinstance(wert, str) or not _DATUM.fullmatch(wert):
            raise ValueError("Datum im Format JJJJ-MM-TT oder null")
        return wert
    if feld == "due_time":
        if wert is None:
            return None
        if not isinstance(wert, str) or not _UHRZEIT.fullmatch(wert):
            raise ValueError("Uhrzeit im Format HH:MM oder null")
        return wert
    if feld == "estimated_minutes":
        if wert is None:
            return None
        if isinstance(wert, bool) or not isinstance(wert, int) or not 1 <= wert <= 10080:
            raise ValueError("Aufwand in Minuten (1 bis 10.080) oder null")
        return wert
    if feld == "done":
        if not isinstance(wert, bool):
            raise ValueError("Erledigt muss true oder false sein")
        return wert
    if feld == "labels":
        if not isinstance(wert, list) or not all(isinstance(name, str) and name.strip() for name in wert):
            raise ValueError("Labels als Liste von Namen")
        return sorted(dict.fromkeys(" ".join(name.split()) for name in wert))
    raise ValueError("unbekanntes Feld")


def check_patch(changes, resolve, known_labels=()):
    """Vorschau je Änderung, ohne etwas zu ändern.

    `resolve(ref)` liefert (Punkt, label_names) oder None. Ergebnis je Änderung:
    {"ref", "title", "status", "diffs", "messages", "values"} mit Status
    `ok` (anwendbar), `unchanged`, `conflict` (Ausgangsstand stimmt nicht mehr),
    `unknown` (Aufgabe nicht gefunden) oder `invalid` (ungültige Werte).
    """
    bekannt = set(known_labels)
    vorschau = []
    gesehen = set()
    for change in changes:
        eintrag = {"ref": change["ref"], "title": "", "status": "ok", "diffs": [], "messages": [], "values": {}}
        vorschau.append(eintrag)
        if change["ref"] in gesehen:
            eintrag["status"] = "invalid"
            eintrag["messages"].append("Dieselbe Aufgabe kommt mehrfach vor")
            continue
        gesehen.add(change["ref"])
        gefunden = resolve(change["ref"])
        if gefunden is None:
            eintrag["status"] = "unknown"
            eintrag["messages"].append("Aufgabe nicht gefunden (gelöscht oder nicht im Kontextpaket)")
            continue
        item, label_names = gefunden
        zustand = item_state(item, label_names)
        eintrag["title"] = zustand["title"]
        if checksum(zustand) != change["base"]:
            eintrag["status"] = "conflict"
            eintrag["messages"].append("Die Aufgabe wurde seit dem Kontextpaket geändert")
        for feld, wert in change["set"].items():
            if feld not in FIELDS:
                eintrag["messages"].append(f"Unbekanntes Feld „{feld}“")
                eintrag["status"] = "invalid" if eintrag["status"] == "ok" else eintrag["status"]
                continue
            try:
                neu = validate_value(feld, wert)
            except ValueError as fehler:
                eintrag["messages"].append(f"{FIELD_NAMES[feld]}: {fehler}")
                eintrag["status"] = "invalid" if eintrag["status"] == "ok" else eintrag["status"]
                continue
            if feld == "labels" and bekannt:
                fremd = [name for name in neu if name not in bekannt]
                if fremd:
                    eintrag["messages"].append("Unbekannte Labels: " + ", ".join(fremd))
                    eintrag["status"] = "invalid" if eintrag["status"] == "ok" else eintrag["status"]
                    continue
            if neu != zustand[feld]:
                eintrag["diffs"].append((FIELD_NAMES[feld], zustand[feld], neu))
                eintrag["values"][feld] = neu
        if eintrag["status"] == "ok" and not eintrag["diffs"]:
            eintrag["status"] = "unchanged"
    return vorschau


def summary(vorschau):
    zaehler = {}
    for eintrag in vorschau:
        zaehler[eintrag["status"]] = zaehler.get(eintrag["status"], 0) + 1
    namen = (("ok", "anwendbar"), ("unchanged", "ohne Änderung"), ("conflict", "Konflikte"),
             ("unknown", "nicht gefunden"), ("invalid", "ungültig"))
    return " · ".join(f"{zaehler[key]} {name}" for key, name in namen if zaehler.get(key))
