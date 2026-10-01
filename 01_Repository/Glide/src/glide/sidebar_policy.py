"""Zuordnung und Inhaltsgrenzen der vier Seitenleistenbereiche, ohne Tk."""
SECTIONS = ('pages', 'lists', 'notes', 'drawings')
TITLES = dict(zip(SECTIONS, ('Seiten', 'Listen', 'Notizen', 'Zeichnungen')))
DOCUMENTS = {'pages': frozenset(('page',)), 'notes': frozenset(('note',)),
             'drawings': frozenset(('drawing',))}
FOLDERS = {'pages': frozenset(('standard', 'library')), 'notes': frozenset(('standard', 'journal')),
           'drawings': frozenset(('standard',))}


def accepts(section, kind, value):
    if section == 'lists':
        return True
    return value in (DOCUMENTS if kind == 'list' else FOLDERS).get(section, ())


def normalize_visibility(value):
    value = value if isinstance(value, dict) else {}
    return {key: True if key == 'lists' else value.get(key) is not False for key in SECTIONS}


def normalize_locations(value):
    if not isinstance(value, dict):
        return {}
    return {key: section for key, section in value.items() if isinstance(key, str)
            and key.startswith(('list:', 'folder:')) and len(key) <= 100 and section in SECTIONS}


class SidebarPolicy:
    """Ein Index je Aufbau; gemischte Altbestände bleiben vollständig unter Listen."""
    def __init__(self, entries, folders, locations=None, visibility=None):
        self.entries = {e['id']: e for e in entries if isinstance(e, dict) and e.get('id')}
        self.folders = {f['id']: f for f in folders if isinstance(f, dict) and f.get('id')}
        self.locations = normalize_locations(locations)
        self.visibility = normalize_visibility(visibility)
        self.children = {}
        self.contents = {}
        self._sections = {}
        for folder in self.folders.values():
            self.children.setdefault(folder.get('parent_id'), []).append(folder)
        for entry in self.entries.values():
            self.contents.setdefault(entry.get('folder_id'), []).append(entry)

    def subtree_accepts(self, folder_id, section, seen=None):
        seen = set() if seen is None else seen
        if folder_id in seen or folder_id not in self.folders:
            return False
        seen.add(folder_id)
        folder = self.folders[folder_id]
        return (accepts(section, 'folder', folder.get('folder_kind', 'standard'))
                and all(accepts(section, 'list', e.get('list_kind', 'tasks'))
                        for e in self.contents.get(folder_id, ()))
                and all(self.subtree_accepts(f['id'], section, seen)
                        for f in self.children.get(folder_id, ())))

    def section(self, kind, identifier):
        key = (kind, identifier)
        if key in self._sections:
            return self._sections[key]
        obj = (self.entries if kind == 'list' else self.folders).get(identifier, {})
        parent = obj.get('folder_id' if kind == 'list' else 'parent_id')
        seen = set()
        while parent in self.folders and parent not in seen:
            seen.add(parent)
            obj = self.folders[parent];kind = 'folder';identifier = parent
            parent = obj.get('parent_id')
        if parent in seen:
            section = 'lists'
        else:
            natural = ({'page': 'pages', 'note': 'notes', 'drawing': 'drawings'}.get(obj.get('list_kind'), 'lists')
                       if kind == 'list' else {'library': 'pages', 'journal': 'notes'}.get(obj.get('folder_kind'), 'lists'))
            section = self.locations.get(f'{kind}:{identifier}', natural)
            valid = (accepts(section, kind, obj.get('list_kind', 'tasks')) if kind == 'list'
                     else self.subtree_accepts(identifier, section))
            if not valid or not self.visibility[section]:
                section = 'lists'
        self._sections[key] = section
        return section


def template_allowed(template, section):
    if section == 'lists':
        return True
    payload = template.get('payload')
    if isinstance(payload, dict):
        return (all(accepts(section, 'list', entry.get('list_kind', 'tasks')) for entry in payload.get('lists', ()))
                and all(accepts(section, 'folder', folder.get('folder_kind', 'standard')) for folder in payload.get('folders', ())))
    if template.get('kind') == 'list':
        return accepts(section, 'list', template.get('list_kind', 'tasks'))
    return (accepts(section, 'folder', template.get('folder_kind', 'standard'))
            and all(accepts(section, 'list', entry.get('list_kind', 'tasks'))
                    for entry in template.get('lists', ()) if isinstance(entry, dict))
            and all(template_allowed(dict(child, kind='folder'), section)
                    for child in template.get('folders', ()) if isinstance(child, dict)))


def sibling_ids(policy, kind, identifier):
    objects = policy.entries if kind == 'list' else policy.folders
    source = objects.get(identifier)
    if source is None:
        return []
    field = 'folder_id' if kind == 'list' else 'parent_id'
    parent = source.get(field)
    section = policy.section(kind, identifier)
    return [key for key, obj in objects.items() if obj.get(field) == parent
            and (parent is not None or policy.section(kind, key) == section)
            and obj.get('system_role') != 'inbox' and not obj.get('archived')]
