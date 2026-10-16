"""Anzeige- und Bedienregeln für Palette, Hinweise, Termine und Tastenwege, ohne Tk oder Mutation."""


def palette_query(query):
    value = str(query or '').strip()
    return (value[1:].lstrip(), True) if value.startswith('>') else (value, False)


# B06 (15.10.2026): Ergänzende Bedienhinweise folgen einem gespeicherten
# Schalter in den Einstellungen statt einem „?“ je Ansicht. Vorgabe aus, wie
# bisher die eingeklappten Hinweise. Status- und Fehlermeldungen,
# Feldbeschriftungen und Hinweisblöcke in Seiten (D06) hängen nicht daran.
HINTS_SETTING = 'show_hints'
HINTS_DEFAULT = False
LEGACY_HINTS_SETTING = 'view_hints'

TRASH_EMPTY = 'Der Papierkorb ist leer.'
TRASH_EMPTY_HINT = 'Gelöschte Punkte, Listen und Ordner landen hier und bleiben wiederherstellbar.'


def hints_visible(settings, view=None):
    """Ob ergänzende Hinweise erscheinen; `view` bleibt nur für ältere Aufrufer."""
    return (settings or {}).get(HINTS_SETTING) is True


def migrate_hint_setting(settings):
    """Übernimmt die frühere Wahl je Ansicht in den gemeinsamen Schalter.

    War vorher in mindestens einer Ansicht „?“ aufgeklappt, bleiben Hinweise
    sichtbar – jetzt in allen Ansichten. Sonst gilt die Vorgabe aus. Ein
    bereits gespeicherter Schalter hat Vorrang. Liefert ein neues Wörterbuch.
    """
    result = dict(settings or {})
    legacy = normalize_hints(result.pop(LEGACY_HINTS_SETTING, None))
    value = result.get(HINTS_SETTING)
    result[HINTS_SETTING] = value if type(value) is bool else (any(legacy.values()) or HINTS_DEFAULT)
    return result


def trash_empty_text(hints):
    """Leertext des Papierkorbs (B15): kurz, Ergänzung nur mit Hinweisen."""
    return f'{TRASH_EMPTY} {TRASH_EMPTY_HINT}' if hints else TRASH_EMPTY


def date_text(due, planned, due_symbol, plan_symbol):
    """Beide Felder bleiben auch am gleichen Tag eindeutig sichtbar."""
    return ' · '.join(value for value in
                    (f'{due_symbol} {due}' if due else '',
                     f'{plan_symbol} {planned}' if planned else '') if value)


def normalize_hints(value):
    if not isinstance(value, dict):
        return {}
    return {key: flag for key, flag in value.items()
            if isinstance(key, str) and len(key) <= 64 and type(flag) is bool}


# Zuletzt benutzte Ziele (KO06 seit 3.33.20): nur lokal, keine Einstellung in
# der Oberfläche. Höchstens fünf stehen vorn, der Rest in gewohnter Reihenfolge.
RECENT_LIMIT = 5


def remember_recent(recent, key, limit=RECENT_LIMIT):
    """`key` an den Anfang; Dubletten und ungültige Einträge entfallen."""
    vorher = list(dict.fromkeys(value for value in (recent if isinstance(recent, list) else [])
                                if isinstance(value, str) and value and value != key))
    return ([key] + vorher)[:limit] if isinstance(key, str) and key else vorher[:limit]


def recent_first(keys, recent, limit=RECENT_LIMIT):
    """Ziele in Anzeigereihenfolge: zuletzt benutzte (noch vorhandene) zuerst.

    Liefert (vorn, rest); beide zusammen enthalten jede Kennung aus `keys`
    genau einmal, `rest` in der ursprünglichen Reihenfolge.
    """
    vorhanden = list(keys)
    menge = set(vorhanden)
    vorn = []
    for value in recent if isinstance(recent, list) else []:
        if value in menge and value not in vorn:
            vorn.append(value)
        if len(vorn) >= limit:
            break
    return vorn, [value for value in vorhanden if value not in vorn]


# X11-Emacs-Kürzel in Listen (3.43.1): Tk legt unter X11 Strg+A/B/E/F/N/P,
# mit Umschalt erweiternd, auf dieselben virtuellen Ereignisse wie Pfeiltasten,
# Pos1 und Ende (tk.tcl, ::tk::EventMotifBindings). Die Treeview reagiert erst
# seit Tk 9.1 darauf; Strg+Umschalt+P setzte so die Auswahl eine Zeile höher,
# bevor Glides „Einplanen“ lief. Text- und Eingabefelder behalten die Kürzel.
NAVIGATION_EVENTS = frozenset(f'<<{name}>>' for name in (
    'PrevChar', 'NextChar', 'SelectPrevChar', 'SelectNextChar',
    'PrevLine', 'NextLine', 'SelectPrevLine', 'SelectNextLine',
    'LineStart', 'LineEnd', 'SelectLineStart', 'SelectLineEnd'))
EMACS_GUARD_MARK = '# Glide: Strg+Buchstabe bleibt Glide-Kürzel (X11)'


def is_emacs_trigger(sequence):
    """Ob eine Tk-Sequenz Strg mit einem einzelnen Buchstaben ist, etwa <Control-P>.

    Umschalt und Feststelltaste dürfen dazukommen; Pfeil-, Pos1- und
    Endetasten (<Control-Left>, <Shift-Home>) zählen nicht.
    """
    text = str(sequence or '').strip()
    if not (text.startswith('<') and text.endswith('>')) or text.startswith('<<'):
        return False
    *modifiers, detail = text[1:-1].split('-')
    modifiers = {value for value in modifiers if value not in ('Key', 'KeyPress')}
    return ('Control' in modifiers and modifiers <= {'Control', 'Shift', 'Lock'}
            and len(detail) == 1 and detail.isalpha())


def emacs_guarded_events(class_events, event_sequences):
    """Navigationsereignisse einer Tk-Klasse, die auch ein Strg-Buchstabe auslöst.

    `class_events` sind die Ereignisse der Klassenbindung, `event_sequences`
    ordnet jedem virtuellen Ereignis seine Sequenzen zu (`event info`).
    """
    return sorted(event for event in set(class_events) if event in NAVIGATION_EVENTS
                  and any(is_emacs_trigger(sequence) for sequence in event_sequences.get(event, ())))


def guard_emacs_script(script):
    """Klassenbindung, die bei Strg+Buchstabe nichts tut und sonst unverändert wirkt.

    `%K` ist bei einem Tastendruck das Tastensymbol, beim unmittelbar erzeugten
    virtuellen Ereignis „??“. Kein `break`: Glides Kürzel an Fenster und
    Anwendung laufen danach wie unter Tk 9.0. Mehrfaches Anwenden ändert nichts.
    """
    text = str(script or '')
    if not text.strip() or text.startswith(EMACS_GUARD_MARK):
        return text
    return f'{EMACS_GUARD_MARK}\nif {{[string length %K] != 1}} {{\n{text}\n}}'
