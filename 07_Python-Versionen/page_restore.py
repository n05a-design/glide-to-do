"""Selektive Seitenwiederherstellung planen, ohne Tk, Dateien oder Mutation.

Eingaben sind bereits vollständig validierte Glide-Datenstände. Eine UI
sichert vor Anwendung den Gesamtbestand und legt alle Anhänge neu ab.
"""
import copy
from dataclasses import dataclass, replace
import hashlib
import json
import uuid
import object_references as objects
import task_references as tasks
import attachment_paths as paths


def fingerprint(data):
    return hashlib.sha256(json.dumps(data,ensure_ascii=False,sort_keys=True,
                                    separators=(",",":"),allow_nan=False).encode()).hexdigest()


def forest_without(items, removed):
    """Nicht wiederhergestellte Kinder bleiben auch ohne ihren Elternpunkt."""
    result = []
    for original in items:
        item = copy.deepcopy(original)
        children = forest_without(item.get("children",[]),removed)
        if item["id"] in removed:
            result.extend(children)
        else:
            if "children" in item or children:
                item["children"] = children
            result.append(item)
    return result


@dataclass(frozen=True)
class Plan:
    page: dict
    trash: tuple
    added_labels: tuple
    attachments: tuple
    missing_files: tuple
    missing_targets: tuple
    remapped_items: tuple
    warnings: tuple
    current_hash: str
    occupied_attachment_ids: tuple
    occupied_storage: tuple
    staged: bool = False

    @property
    def ready(self):
        return not self.missing_files


def prepare(current, backup, page_id, available_assets, *, new_id=None, max_trash=200, max_labels=80):
    """Kein stilles Überschreiben fremder IDs oder Dateien, kein Mit-Restore anderer Seiten."""
    candidates = [page for page in backup.get("lists",[]) if page.get("id") == page_id]
    if len(candidates) != 1 or candidates[0].get("list_kind") != "page":
        raise ValueError("Die Sicherung enthält diese Seite nicht eindeutig.")
    page = copy.deepcopy(candidates[0])
    live_pages = [entry for entry in current.get("lists",[]) if entry.get("id") == page_id]
    if len(live_pages)>1 or (live_pages and live_pages[0].get("list_kind") != "page"):
        raise ValueError("Die Zielkennung gehört nicht eindeutig derselben Seitenart.")
    original_page = live_pages[0] if live_pages else None
    incoming = list(tasks.walk(page.get("items",[])))
    source_ids = [item["id"] for item in incoming]
    if len(set(source_ids)) != len(source_ids):
        raise ValueError("Mehrdeutige Aufgabenkennungen auf der Sicherungsseite.")
    index = objects.nodes(current.get("lists",[]),current.get("trash",[]))
    occupied = {identity for _kind,identity in index} | set(source_ids)
    occupied.update(entry["id"] for entry in current.get("trash",[]))
    factory = new_id or (lambda:uuid.uuid4().hex)
    def fresh():
        for _ in range(100):
            identity = factory()
            if (isinstance(identity,str) and 1<=len(identity)<=64
                    and all(c.isascii() and (c.isalnum() or c in "_-") for c in identity)
                    and identity not in occupied):
                occupied.add(identity)
                return identity
        raise ValueError("Keine freie gültige Kennung für die Wiederherstellung.")
    owned_trash = set()
    for deleted in current.get("trash",[]):
        if deleted.get("kind")=="item" and (deleted.get("origin") or {}).get("list_id")==page_id:
            owned_trash.update(item["id"] for item in tasks.walk([deleted["item"]]))
        containers = [deleted.get("list") or {},*(deleted.get("folder") or {}).get("lists",[])]
        for entry in containers:
            if entry.get("id")==page_id:
                owned_trash.update(item["id"] for item in tasks.walk(entry.get("items",[])))
    mapping = {}
    for identity in source_ids:
        existing = index.get(("item",identity))
        if existing:
            state,_item,owner = existing
            is_own = (owner is not None and owner.get("id")==page_id) or (state=="trash" and identity in owned_trash)
            if not is_own:
                mapping[identity] = fresh()
    for item in incoming:
        item["id"] = mapping.get(item["id"],item["id"])
        for field in ("links","blocked_by"):
            if field in item:
                item[field] = [mapping.get(identity,identity) for identity in item[field]]
        objects.remap_holder(item,{},mapping)
    tasks.remap(page.get("rich_note"),mapping)
    objects.remap_holder(page,{},mapping)
    restored = {item["id"] for item in incoming}
    warnings = []
    folders = {entry["id"] for entry in current.get("folders",[])}
    wanted_folder = original_page.get("folder_id") if original_page else page.get("folder_id")
    page["folder_id"] = wanted_folder if wanted_folder in folders else None
    if wanted_folder and wanted_folder not in folders:
        warnings.append("Der frühere Ordner fehlt; die Seite wird ohne Ordner eingeordnet.")
    if original_page and page.get("folder_id") != candidates[0].get("folder_id"):
        warnings.append("Die heutige Ordnereinordnung bleibt erhalten.")
    trash = []
    def trash_item(item, source=None):
        record = copy.deepcopy(source) if source else dict(id=fresh(),kind="item",deleted_at="",
                list=None,folder=None,item=None,origin_folder_id=None,origin_folder_title="",origin={})
        record.update(kind="item",list=None,folder=None,item=item,
                      origin=dict(list_id=page_id,list_title=page.get("title") or "Seite",
                                  parent_item_id=None,index=None))
        return record
    for deleted in current.get("trash",[]):
        if deleted.get("kind")=="item" and (deleted.get("origin") or {}).get("list_id")==page_id:
            remaining = forest_without([deleted["item"]],restored)
            if remaining == [deleted["item"]]:
                trash.append(copy.deepcopy(deleted))
            else:
                for number,item in enumerate(remaining):
                    trash.append(trash_item(item,deleted if number==0 else None))
            continue
        entry = deleted.get("list") or {}
        if deleted.get("kind")=="list" and entry.get("id")==page_id:
            trash.extend(trash_item(item) for item in forest_without(entry.get("items",[]),restored))
            continue
        changed = copy.deepcopy(deleted)
        folder = changed.get("folder") or {}
        if "lists" in folder:
            keep = []
            for entry in folder["lists"]:
                if entry.get("id")==page_id:
                    trash.extend(trash_item(item) for item in forest_without(entry.get("items",[]),restored))
                else:
                    keep.append(entry)
            folder["lists"] = keep
        trash.append(changed)
    if original_page:
        removed = forest_without(original_page.get("items",[]),restored)
        trash = [*(trash_item(item) for item in removed),*trash]
        if removed:
            warnings.append("Heute vorhandene, nicht wiederhergestellte Aufgaben bleiben im Papierkorb.")
    if len(trash)>max_trash:
        raise ValueError("Die Wiederherstellung würde den Papierkorb kürzen; bitte zuerst Platz schaffen.")
    holders = [page,*incoming]
    known_labels = {value["id"]:value for value in current.get("labels",[])}
    saved_labels = {value["id"]:value for value in backup.get("labels",[])}
    needed = {identity for holder in holders for identity in holder.get("labels",[])}
    if needed-known_labels.keys()-saved_labels.keys():
        raise ValueError("Labeldefinition fehlt in der Sicherung.")
    added = tuple(copy.deepcopy(saved_labels[key]) for key in sorted(needed-known_labels.keys()))
    if len(known_labels)+len(added)>max_labels:
        raise ValueError("Die Wiederherstellung würde die Labelgrenze überschreiten.")
    if any(key in known_labels and key in saved_labels and known_labels[key]!=saved_labels[key] for key in needed):
        warnings.append("Zwischenzeitlich geänderte Labeldefinitionen bleiben wie heute; andere Seiten ändern sich nicht.")
    attachments = {}
    for holder in holders:
        for attachment in holder.get("attachments",[]):
            identity = attachment["id"]
            if identity in attachments and attachments[identity] != attachment:
                raise ValueError("Anhangskennung ist in der Sicherungsseite mehrdeutig.")
            attachments[identity] = copy.deepcopy(attachment)
    referenced = {value.get("attachment") for value in (page.get("rich_note") or {}).get("images",{}).values()}
    cover = page.get("cover") or {}
    if cover.get("kind")=="image":referenced.add(cover.get("attachment"))
    referenced.discard(None)
    missing = set(referenced-attachments.keys())
    missing.update(key for key,value in attachments.items() if value["storage"] not in available_assets)
    lists = [entry for entry in current.get("lists",[]) if entry.get("id") != page_id]+[page]
    target_index,outgoing,_incoming = objects.graph(lists,trash)
    targets = set(outgoing.get(("list",page_id),()))
    for item in incoming:
        targets.update(outgoing.get(("item",item["id"]),()))
        targets.update(("item",key) for key in item.get("blocked_by",[]))
    missing_targets = tuple((kind,identity,target_index.get((kind,identity),("missing",None,None))[0])
                            for kind,identity in sorted(targets)
                            if target_index.get((kind,identity),("missing",None,None))[0] != "active")
    current_holders = [holder for _state,holder,_owner in index.values()]
    current_holders.extend(current.get("folders",[]))
    current_holders.extend((entry.get("folder") or {}) for entry in current.get("trash",[]))
    all_assets = [asset for holder in current_holders for asset in holder.get("attachments",[])]
    all_assets.extend(attachments.values())
    return Plan(page,tuple(trash),added,tuple(attachments[key] for key in sorted(attachments)),
                tuple(sorted(missing)),missing_targets,tuple(sorted(mapping.items())),tuple(warnings),fingerprint(current),
                tuple(sorted({asset["id"] for asset in all_assets})),
                tuple(sorted({asset["storage"] for asset in all_assets})))


def with_attachments(plan, stored):
    expected = {value["id"] for value in plan.attachments}
    if set(stored) != expected or not plan.ready:
        raise ValueError("Alle Sicherungsanhänge müssen vor Übernahme verfügbar sein.")
    if plan.staged:
        raise ValueError("Die Sicherungsanhänge wurden bereits zugeordnet.")
    if any(not isinstance(value, dict) for value in stored.values()):
        raise ValueError("Ungültige Metadaten eines kopierten Anhangs.")
    new_ids = [value.get("id") for value in stored.values()]
    if any(not isinstance(identity, str) or not 1 <= len(identity) <= 64
           or any(not c.isascii() or not (c.isalnum() or c in "_-") for c in identity)
           for identity in new_ids) or len(set(new_ids)) != len(new_ids):
        raise ValueError("Neue Anhangskennungen sind nicht eindeutig oder ungültig.")
    if set(new_ids).intersection(plan.occupied_attachment_ids):
        raise ValueError("Eine neue Anhangskennung ist bereits belegt.")
    storage = [value.get("storage") for value in stored.values()]
    keys = [paths.storage_key(value) for value in storage]
    occupied = {paths.storage_key(value) for value in plan.occupied_storage}
    if (any(paths.validate_storage(value) != value for value in storage)
            or len(set(keys)) != len(keys) or set(keys).intersection(occupied)):
        raise ValueError("Jeder kopierte Anhang braucht einen freien gültigen Speicherpfad.")
    for original in plan.attachments:
        copied = stored[original["id"]]
        if type(copied.get("size")) is not int or copied["size"] != original.get("size"):
            raise ValueError("Eine kopierte Anhangsgröße stimmt nicht mit der Sicherung überein.")
        for field in ("name", "mime", "title", "note"):
            if copied.get(field) != original.get(field):
                raise ValueError("Beschreibende Anhangsfelder müssen aus der Sicherung erhalten bleiben.")
    page = copy.deepcopy(plan.page)
    for holder in [page,*tasks.walk(page.get("items",[]))]:
        if "attachments" in holder:
            holder["attachments"] = [copy.deepcopy(stored[value["id"]]) for value in holder["attachments"]]
    for value in (page.get("rich_note") or {}).get("images",{}).values():
        if value.get("attachment") in stored:value["attachment"] = stored[value["attachment"]]["id"]
    cover=page.get("cover") or {}
    if cover.get("kind")=="image":cover["attachment"]=stored[cover["attachment"]]["id"]
    return replace(plan,page=page,staged=True)


def validate(plan, current):
    if not plan.ready:
        raise ValueError("Dateien für die Wiederherstellung fehlen.")
    if plan.attachments and not plan.staged:
        raise ValueError("Anhänge müssen vor Übernahme neu abgelegt werden.")
    if fingerprint(current) != plan.current_hash:
        raise ValueError("Der Bestand hat sich geändert; bitte die Vorschau neu aufbauen.")
    return True
