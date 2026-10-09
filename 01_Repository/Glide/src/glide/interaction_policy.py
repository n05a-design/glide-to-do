"""Anzeigeregeln für Palette, Hinweise und Termine, ohne Tk oder Mutation."""


def palette_query(query):
    value = str(query or '').strip()
    return (value[1:].lstrip(), True) if value.startswith('>') else (value, False)


def hints_visible(settings, view):
    return (settings.get('view_hints') or {}).get(str(view)) is True


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
