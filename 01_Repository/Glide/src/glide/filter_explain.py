"""Bedingungen gespeicherter Filter prüfen und erklären, ohne Tk (D-03 seit 3.34.0).

Ein gespeicherter Filter besteht aus Bedingungen: Liste, Quelle, Status,
Wichtigkeit, Labels, Fälligkeit und Suchtext. Dieses Modul ist die einzige
Stelle, die sie auswertet – die Ansicht wählt damit aus, und „Warum?“ zeigt
dieselben Bedingungen mit erfüllt oder verfehlt. Es verändert keine Daten.

Ein Punkt wird als Wörterbuch beschrieben (`item_facts`): Liste, Herkunft aus
Seiten, erledigt, Wichtigkeit, Labels, Fälligkeitstag und ob der Suchtext im
Punkt vorkommt. Die App liefert diese Fakten; die Regeln stehen hier.
"""
from collections import Counter
from datetime import timedelta

STATUS_NAMES = {"all": "alle Aufgaben", "open": "nur offene", "done": "nur erledigte"}
IMPORTANCE_NAMES = {"0": "keine", "1": "niedrig", "2": "mittel", "3": "hoch"}
DUE_NAMES = {"any": "jede Fälligkeit", "none": "ohne Fälligkeit", "overdue": "überfällig", "today": "heute",
             "tomorrow": "morgen", "next7": "nächste 7 Tage", "next30": "nächste 30 Tage"}
ORDER = ("list", "source", "status", "importance", "labels", "due", "query")
TITLES = {"list": "Liste", "source": "Quelle", "status": "Status", "importance": "Wichtigkeit",
          "labels": "Labels", "due": "Fälligkeit", "query": "Suchtext"}


def due_window(due_mode, today):
    """(Start, Ende) des Fälligkeitsfensters oder None."""
    if due_mode not in ("today", "tomorrow", "next7", "next30"):
        return None
    start = today + timedelta(days=1 if due_mode == "tomorrow" else 0)
    return start, start + timedelta(days={"next7": 6, "next30": 29}.get(due_mode, 0))


def due_matches(due_mode, day, today, done):
    if due_mode == "none":
        return day is None
    if due_mode == "overdue":
        return day is not None and day < today and not done
    fenster = due_window(due_mode, today)
    if fenster is not None:
        return day is not None and fenster[0] <= day <= fenster[1]
    return True


def conditions(criteria, facts, today, names=None):
    """Alle gesetzten Bedingungen eines Filters für einen Punkt, in fester Reihenfolge.

    Jede Bedingung: {"key", "title", "ok", "detail"}. Nicht gesetzte
    Bedingungen (alle Listen, jede Wichtigkeit …) erscheinen nicht.
    `names` übersetzt Listen- und Labelkennungen in Namen (optional).
    """
    names = names or {}
    ergebnis = []

    def bedingung(key, ok, detail):
        ergebnis.append({"key": key, "title": TITLES[key], "ok": bool(ok), "detail": detail})

    listen = list(criteria.get("list_ids") or [])
    if listen:
        heimat = facts.get("list_id")
        bedingung("list", heimat in listen,
                  f"steht in „{names.get(heimat, heimat or '?')}“" + ("" if heimat in listen else
                                                                      " – nicht unter den gewählten Listen"))
    if criteria.get("source") == "pages":
        bedingung("source", bool(facts.get("from_pages")),
                  "aus einer Seite" if facts.get("from_pages") else "nicht aus einer Seite")
    status = criteria.get("status", "open")
    if status in ("open", "done"):
        erledigt = bool(facts.get("done"))
        bedingung("status", erledigt == (status == "done"),
                  f"verlangt: {STATUS_NAMES[status]} · Punkt ist {'erledigt' if erledigt else 'offen'}")
    wichtigkeit = criteria.get("importance", "all")
    if wichtigkeit not in (None, "all"):
        eigene = str(facts.get("importance", 0))
        bedingung("importance", eigene == wichtigkeit,
                  f"verlangt: {IMPORTANCE_NAMES.get(wichtigkeit, wichtigkeit)} · Punkt: "
                  f"{IMPORTANCE_NAMES.get(eigene, eigene)}")
    gesucht = list(criteria.get("label_ids") or [])
    if gesucht:
        eigene = set(facts.get("labels") or ())
        alle = criteria.get("label_mode") == "all"
        ok = set(gesucht).issubset(eigene) if alle else bool(set(gesucht) & eigene)
        fehlend = [names.get(kennung, kennung) for kennung in gesucht if kennung not in eigene]
        detail = ("alle gewählten Labels" if alle else "mindestens eines der gewählten Labels")
        if not ok:
            detail += " · fehlt: " + ", ".join(fehlend)
        bedingung("labels", ok, detail)
    faellig = criteria.get("due", "any")
    if faellig not in (None, "any"):
        tag = facts.get("due")
        ok = due_matches(faellig, tag, today, facts.get("done"))
        bedingung("due", ok, f"verlangt: {DUE_NAMES.get(faellig, faellig)} · Punkt: "
                              f"{tag.strftime('%d.%m.%Y') if tag else 'ohne Fälligkeit'}")
    suche = str(criteria.get("query") or "")
    if suche:
        bedingung("query", bool(facts.get("query_match")),
                  f"„{suche}“ " + ("kommt im Punkt vor" if facts.get("query_match") else "kommt im Punkt nicht vor"))
    return ergebnis


def matches(bedingungen):
    return all(eintrag["ok"] for eintrag in bedingungen)


def hidden_reasons(alle_bedingungen):
    """Zählt für ausgeblendete Punkte die erste verfehlte Bedingung (Reihenfolge `ORDER`)."""
    zaehler = Counter()
    for bedingungen in alle_bedingungen:
        verfehlt = [eintrag["key"] for eintrag in bedingungen if not eintrag["ok"]]
        if verfehlt:
            zaehler[min(verfehlt, key=ORDER.index)] += 1
    return [(TITLES[key], zaehler[key]) for key in ORDER if zaehler[key]]
