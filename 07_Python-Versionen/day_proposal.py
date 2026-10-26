"""Erklärbare Tagesauswahl: reine Berechnung, stabile Quellen, keine Mutation."""
from datetime import date, timedelta
import hashlib
import json

REASONS = {"overdue": "überfällig", "due_today": "heute fällig",
           "carried": "liegen geblieben", "due_soon": "in den nächsten zwei Tagen fällig",
           "unblocks": "gibt andere frei", "important": "wichtig"}


def release_counts(records, dependency_done=None):
    """Direkte Freigaben: genau eine offene Voraussetzung pro aktiver Folgeaufgabe.

    Die Statusprojektion umfasst auch archivierte Voraussetzungen. Fehlende
    Ziele blockieren wie im bestehenden App-Vertrag nicht; Selbstbezüge und
    doppelte Folgeaufgaben erzeugen keinen zusätzlichen Nutzen.
    """
    done = dependency_done if dependency_done is not None else {
        record["item"]["id"]: bool(record["item"].get("done")) for record in records}
    counts, seen = {}, set()
    for record in records:
        item = record["item"]
        identity = (record["list_id"], item["id"])
        if identity in seen or item.get("done"):
            continue
        seen.add(identity)
        blockers = {key for key in item.get("blocked_by") or () if key in done and not done[key]}
        if len(blockers) == 1:
            blocker = next(iter(blockers))
            if blocker != item["id"]:
                counts[blocker] = counts.get(blocker, 0) + 1
    return counts


def reason_text(row):
    """Grund und echte direkte Freigabezahl, auch neben höherer Dringlichkeit."""
    reason = REASONS[row["reason"]]
    count = row.get("unblocks", 0)
    if not count:
        return reason
    release = f"gibt {count} weitere {'Aufgabe' if count == 1 else 'Aufgaben'} frei"
    return release if row["reason"] == "unblocks" else f"{reason} · {release}"


def propose(records, day, summary, fallback=30, *, dependency_done=None):
    """Greedy-Auswahl nach Dringlichkeit; spätere Pläne bleiben unangetastet.

    records enthalten list_id, item und blocked. Bereits geplante unbekannte
    Aufwände reservieren denselben ausdrücklich benannten Ersatzwert wie neue
    Kandidaten. Das ändert weder die AU02-Bilanz noch geschätzte Aufwände.
    """
    reference = date.fromisoformat(day)
    soon = (reference + timedelta(days=2)).isoformat()
    releases = release_counts(records, dependency_done)
    rows, seen = [], set()
    for record in records:
        item = record["item"]
        identity = (record["list_id"], item["id"])
        if identity in seen or item.get("done") or record.get("blocked"):
            continue
        seen.add(identity)
        planned, due = item.get("planned_date"), item.get("due")
        if planned == day or (planned and planned > day):
            continue
        reason = ("overdue" if due and due < day else "due_today" if due == day else
                  "carried" if planned and planned < day else
                  "due_soon" if due and due <= soon else
                  "unblocks" if releases.get(item["id"]) else
                  "important" if item.get("importance", 0) else None)
        if reason is None:
            continue
        minutes = item.get("estimated_minutes")
        assumed = type(minutes) is not int or minutes <= 0
        rows.append(dict(list_id=identity[0], item_id=identity[1], reason=reason,
                         unblocks=releases.get(item["id"], 0),
                         minutes=fallback if assumed else minutes, assumed=assumed,
                         title=str(item.get("text") or ""), due=due or "9999",
                         importance=item.get("importance", 0)))
    order = {name: position for position, name in enumerate(REASONS)}
    rows.sort(key=lambda row: (order[row["reason"]],
                               -row["unblocks"] if row["reason"] == "unblocks" else 0,
                               row["due"], -row["importance"],
                               row["list_id"], row["item_id"]))
    remaining = summary["remaining"]
    budget = None if remaining is None else max(0, remaining - summary["without_estimate"] * fallback)
    rest = budget
    for row in rows:
        row["selected"] = rest is not None and row["minutes"] <= rest
        if row["selected"]:
            rest -= row["minutes"]
    # Der komplette relevante Bestand ist Teil des Vorschauvertrags, auch
    # belegte Zeit und Aufgaben, die zwischenzeitlich aus der Auswahl fallen.
    state = {"day": day, "summary": summary, "unblocks": releases, "records": sorted(records,
             key=lambda record: (record["list_id"], record["item"]["id"]))}
    signature = hashlib.sha256(json.dumps(state, sort_keys=True, ensure_ascii=False,
                                         separators=(",", ":")).encode("utf-8")).hexdigest()
    return dict(day=day, rows=rows, budget=budget, remaining=rest, signature=signature,
                planned_unknown=summary["without_estimate"])


def selected_rows(proposal, identities):
    wanted = set(identities)
    selected = [row for row in proposal["rows"] if (row["list_id"], row["item_id"]) in wanted]
    if len(selected) != len(wanted):
        raise ValueError("Die Auswahl enthält keine aktuellen Vorschlagsaufgaben.")
    if proposal["budget"] is None:
        raise ValueError("Bitte zuerst eine Tageskapazität festlegen.")
    if sum(row["minutes"] for row in selected) > proposal["budget"]:
        raise ValueError("Die Auswahl überschreitet das verfügbare Auswahlbudget.")
    return selected
