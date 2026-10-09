"""Gemeinsamer Vergleichsstand für Verlauf und erfolgreich gespeicherte Aktivität.

Ein Durchlauf je Aufgabenbaum. Teilbaum-Prüfsummen entstehen von unten nach
oben; ein Elternpunkt kodiert seine Kinder nicht noch einmal. Die Prüfsummen
leben nur im Arbeitsspeicher und gehören zu keinem Dateiformat.
"""
from dataclasses import dataclass, field
from collections import Counter
import hashlib
import json


@dataclass
class ListComparison:
    items: dict
    lists: dict
    list_signatures: dict
    item_signatures: dict
    parts: dict = field(default_factory=dict, compare=False)


def prepare_comparison(entries, *, previous_parts=None, changed_ids=None, **options):
    """P08b: deklarierte Listen neu lesen, sonst vollständig vergleichen.

    Der Aufrufer übernimmt parts erst nach erfolgreichem Schreiben. None als
    Änderungsmenge bedeutet Vollvergleich; neue Listen werden immer gelesen.
    Die Reihenfolge bleibt die aktuelle Modellreihenfolge, auch bei Löschen
    oder Verschieben. Die Daten und Vergleichswerte werden nicht verändert.
    """
    result = ListComparison({}, {}, {}, {})
    previous_parts = previous_parts or {}
    entries = list(entries or ())
    ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    duplicate_ids = {value for value, count in Counter(ids).items() if count > 1}
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        list_id = entry.get("id")
        part = (previous_parts.get(list_id)
                if changed_ids is not None and list_id not in changed_ids
                and list_id not in duplicate_ids else None)
        if part is None:
            part = compare_lists([entry], **options)
        for name in ("items", "lists", "list_signatures", "item_signatures"):
            getattr(result, name).update(getattr(part, name))
        result.parts[list_id] = part
    return result


def history_value(item, field):
    """Der bestehende Verlaufsvertrag, ohne Tk oder Zugriff auf Nutzerdaten."""
    value = item.get(field)
    if field == "labels":
        return tuple(sorted(entry for entry in value or () if isinstance(entry, str)))
    if field == "attachments":
        return len(value) if isinstance(value, list) else 0
    if field == "description":
        text = str(value or "")
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16] if text else ""
    if isinstance(value, (dict, list)):
        if not value:
            return "{}" if isinstance(value, dict) else "[]"
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


def tree_signature(value, child_key, children):
    """JSON-Inhalt vergleichen, mit bereits berechneten Kind-Prüfsummen.

    Schlüsselreihenfolge ist wie bisher bedeutungslos, Feld-/Arrayreihenfolge
    und JSON-Typen bleiben unterscheidbar. Fehlendes children/items und eine
    leere Liste unterscheiden sich ebenfalls. Andere Felder werden vollständig
    kodiert, auch solche, die der Verlauf nicht beobachtet.
    """
    raw_children = value.get(child_key)
    if isinstance(raw_children, (list, tuple)):
        own = {key: item for key, item in value.items() if key != child_key}
        digest = hashlib.sha256(json.dumps(own, sort_keys=True, ensure_ascii=False,
                                         separators=(",", ":")).encode("utf-8"))
        # Eigene JSON-Daten enden vor einem separaten, längenkodierten Teil.
        # Jeder Kind-Digest ist genau 32 Bytes lang.
        digest.update(b"\x00children\x00" + len(children).to_bytes(8, "big"))
        for child in children:
            digest.update(child)
        return digest.digest()
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":")).encode("utf-8")).digest()


def stamp_done_time(item, before, completed_at, schedulable):
    """Beim ersten Erledigen datieren; alte Abschlüsse nicht nachdatieren."""
    if item.get("done"):
        if not item.get("done_at") and schedulable(item):
            previous = before.get(item.get("id"))
            if not (previous and previous.get("werte", {}).get("done")):
                item["done_at"] = completed_at
    elif item.get("done_at"):
        item["done_at"] = None


def compare_lists(entries, *, item_fields, schedulable, drawing_hash,
                  baseline=None, completed_at=None, include_edits=True):
    """Neue Vergleichswerte ohne Cache nach Objektidentität aufbauen.

    Nur completed_at erlaubt das bisherige Setzen/Leeren von done_at. Reine
    Verlaufsabfragen bleiben lesend. include_edits=False spart dort sämtliche
    Aktivitäts-Prüfsummen. Der Aufrufer übernimmt sie erst nach erfolgreichem
    Dateischreiben; nach Undo/Import wird jeder ersetzte Baum neu gelesen.
    """
    result = ListComparison({}, {}, {}, {})
    before = baseline.get("items", {}) if isinstance(baseline, dict) else {}

    def walk(points, list_id, title, parent_id, visible=True):
        signatures = []
        for item in points or ():
            if not isinstance(item, dict):
                if include_edits:
                    signatures.append(hashlib.sha256(json.dumps(
                        item, sort_keys=True, ensure_ascii=False,
                        separators=(",", ":")).encode("utf-8")).digest())
                continue
            item_id = item.get("id")
            valid = visible and isinstance(item_id, str) and bool(item_id)
            if completed_at is not None:
                stamp_done_time(item, before, completed_at, schedulable)
            if valid:
                result.items[item_id] = {
                    "list": list_id, "list_title": title, "parent": parent_id,
                    "text": str(item.get("text") or ""),
                    "werte": {field: history_value(item, field) for field in item_fields},
                }
            children = walk(item.get("children"), list_id, title, item_id, valid)
            if include_edits:
                signature = tree_signature(item, "children", children)
                signatures.append(signature)
                if schedulable(item):
                    result.item_signatures[item["id"]] = signature
        return signatures

    for entry in entries or ():
        if not isinstance(entry, dict):
            continue
        list_id = entry.get("id")
        valid = isinstance(list_id, str) and bool(list_id)
        title = str(entry.get("title") or "")
        if valid:
            result.lists[list_id] = {
                "title": title, "folder": entry.get("folder_id"),
                "note": history_value(entry, "rich_note"), "kind": entry.get("list_kind"),
                "drawing": drawing_hash(entry), "references": history_value(entry, "references"),
                "page_features": (history_value(entry, "live_lists"), history_value(entry, "cover")),
            }
        children = walk(entry.get("items"), list_id, title, None, valid)
        if include_edits:
            result.list_signatures[entry["id"]] = tree_signature(entry, "items", children)
    return result
