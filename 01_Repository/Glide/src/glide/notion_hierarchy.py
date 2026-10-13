"""Bestehende Glide-Ordner für die gewählten Notion-Unterseiten planen, ohne Tk."""
from dataclasses import dataclass
from notion_reimport import is_source_key
import uuid



def source_key(value):
    if not is_source_key(value):
        raise ValueError("Ungültige Notion-Ordnerzuordnung.")
    return value


def restored_source_key(folder, live_folders):
    """Eine zurückgeholte Ordnerkopie übernimmt keine schon lebende Zuordnung."""
    value = folder.get('notion_source_key')
    if value is None:
        return None
    key = source_key(value)
    existing = [source_key(item['notion_source_key']) for item in live_folders
                if item.get('notion_source_key') is not None]
    if len(existing) != len(set(existing)):
        raise ValueError('Die vorhandene Notion-Ordnerzuordnung ist nicht eindeutig.')
    return None if key in existing else key


@dataclass(frozen=True)
class Folder:
    identity: str
    title: str
    parent_id: str | None
    source_key: str


@dataclass(frozen=True)
class Plan:
    folders: tuple[Folder,...]
    page_folders: tuple[tuple[str,str | None],...]


def prepare(pages, existing_folders, current_pages=(), *, target_folder_id=None,
            max_depth=8, new_id=None, occupied_ids=()):
    if type(max_depth)is not int or max_depth<1:
        raise ValueError("Ungültige Ordnertiefe.")
    folders={};bindings={};occupied=set(occupied_ids)
    for folder in existing_folders:
        identity=folder['id']
        if identity in folders:raise ValueError("Mehrdeutige vorhandene Ordnerkennung.")
        folders[identity]=folder;occupied.add(identity)
        key=folder.get('notion_source_key')
        if key is not None:
            key=source_key(key)
            if key in bindings:raise ValueError("Mehrdeutige Notion-Ordnerzuordnung.")
            bindings[key]=identity
    if target_folder_id is not None and target_folder_id not in folders:
        raise ValueError("Der gewählte Zielordner fehlt.")
    current={page['id']:page for page in current_pages}
    occupied.update(current)
    source_targets={}
    for page in current.values():
        value=page.get('notion_source')
        if value is not None:
            key=source_key(value['key'])
            if key in source_targets:raise ValueError("Mehrdeutige vorhandene Quellseite.")
            source_targets[key]=page
    factory=new_id or (lambda:uuid.uuid4().hex)
    def fresh():
        for _ in range(100):
            identity=factory()
            if (isinstance(identity,str) and 1<=len(identity)<=64
                    and all(c.isascii()and(c.isalnum()or c in '_-')for c in identity)
                    and identity not in occupied):
                occupied.add(identity);return identity
        raise ValueError("Keine freie Ordnerkennung verfügbar.")
    def check_chain(identity):
        seen=set();depth=0
        while identity is not None:
            if identity in seen or identity not in folders:
                raise ValueError("Die Zielordnerstruktur enthält einen Kreis oder ein fehlendes Ziel.")
            seen.add(identity);depth+=1
            folder=folders[identity]
            if folder.get('archived') is True:
                raise ValueError("Der Importzielordner ist archiviert.")
            identity=folder.get('parent_id')
        if depth>max_depth:raise ValueError("Die Unterseiten überschreiten die erlaubte Ordnertiefe.")
    descriptors={};created=[];assignments=[];seen_pages=set()
    check_chain(target_folder_id)
    for page in pages:
        if page.key in seen_pages:raise ValueError("Eine Quellseite wurde mehrfach gewählt.")
        seen_pages.add(page.key)
        existing=source_targets.get(page.key)
        if existing is not None:
            folder_id=existing.get('folder_id')
            check_chain(folder_id)
            assignments.append((page.key,folder_id));continue
        parent=target_folder_id;prior_key=None
        for key,title in page.folders:
            key=source_key(key)
            descriptor=(prior_key,title)
            if key in descriptors and descriptors[key]!=descriptor:
                raise ValueError("Die Exportordnerstruktur ist nicht eindeutig.")
            descriptors[key]=descriptor
            if key not in bindings:
                identity=fresh();bindings[key]=identity
                folder=Folder(identity,str(title).strip()[:200]or 'Ohne Titel',parent,key)
                created.append(folder)
                folders[identity]={'id':identity,'parent_id':parent}
            parent=bindings[key]
            check_chain(parent)
            prior_key=key
        assignments.append((page.key,parent))
    return Plan(tuple(created),tuple(assignments))
