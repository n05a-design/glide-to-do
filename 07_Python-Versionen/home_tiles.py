"""Startseitenkacheln ohne Tk: Bestand, Standard, Sichtbarkeit und die zusammengeführte Kachel „Heute“."""

# (Schlüssel, Titel, Gewicht im Raster, volle Breite, Teil des Standards)
#
# Der Standard „Ruhig“ (Entscheidung D12, 01.10.2026) zeigt sieben Kacheln:
# Heute, Gismo, Woche, Zuletzt bearbeitet, Angeheftet, Zeichnungen und die
# Pinnwand-Vorschau. Bis 3.33.1 waren es zwölf; „Heute“ erschien dabei
# viermal (Begrüßung mit Tagesziel, Heute, Nächste Aufgabe, Uhr mit nächstem
# Termin). Alle übrigen Kacheln bleiben wählbar.
DEFINITIONS = (
    ("clock", "Uhr, Datum und nächster Termin", 1, True, False),
    ("welcome", "Begrüßung, Tagesziel und Schnellzugriff", 3, True, False),
    # „Mein Tag“ und „Heute fällig“ standen bis 3.22
    # als zwei gleich aussehende Kacheln nebeneinander. Fachlich sind es
    # zwei Fragen – woran arbeite ich heute, und was muss heute fertig
    # sein –, aber zwei Kacheln beantworten sie schlechter als eine mit
    # zwei Abschnitten: Erst nebeneinander wird sichtbar, ob das eine zum
    # anderen passt. Seit D12 trägt sie auch Tagesziel und nächste Aufgabe.
    ("mascot", "Gismo – Begleiter", 1, False, True),
    ("today", "Heute – Tagesziel, nächste Aufgabe, eingeplant und fällig", 2, False, True),
    ("focus", "Nächste Aufgabe – der konkrete nächste Schritt", 2, False, False),
    ("week", "Die nächsten sieben Tage", 2, False, True),
    ("labels", "Labels im Bestand", 2, False, False),
    ("recent", "Zuletzt bearbeitet", 2, False, True),
    ("templates", "Mit einer Vorlage starten", 2, False, False),
    ("impulse", "Impuls für den Tag", 1, False, False),
    # Vier weitere Bausteine. Bis 3.23 gab es zehn
    # Kacheln, von denen sich sieben um dieselbe Frage drehten – was ist
    # offen. Die neuen beantworten andere: wann (Kalender), was ist liegen
    # geblieben (Verspätet), wie weit bin ich (Fortschritt) und woran
    # denke ich gerade (Pinnwände).
    ("calendar", "Kalendervorschau", 3, False, False),
    ("overdue", "Verspätet – was liegen geblieben ist", 2, False, False),
    ("progress", "Fortschritt heute und diese Woche", 2, False, False),
    ("boards", "Pinnwände", 2, False, False),
    # Die Pinnwand als Bild statt als
    # Zeile. Standardmäßig sichtbar, weil sie genau das leistet, was der
    # Startseite fehlte: eine Fläche, die man ansieht statt liest.
    ("boardpreview", "Pinnwand-Vorschau", 2, False, True),
    # 3.30: Zeichnungen als Bilder, angeheftete Seiten und Filter.
    ("drawings", "Zeichnungen", 2, False, True),
    ("pinned", "Angeheftet", 2, False, True),
    ("filters", "Angeheftete Filter", 2, False, False),
    ("stats", "Dein aktueller Bestand", 6, False, False),
)
KEYS = tuple(key for key, _titel, _gewicht, _breit, _standard in DEFINITIONS)
STANDARD = tuple(key for key, _titel, _gewicht, _breit, standard in DEFINITIONS if standard)


def _known(values):
    result = []
    for key in values if isinstance(values, list) else ():
        if key in KEYS and key not in result:
            result.append(key)
    return result


def normalize(order, hidden, show_stats=True):
    """Bereinigt Reihenfolge und ausgeblendete Kacheln; liefert ``(order, hidden)``.

    Eine leere Reihenfolge heißt: Niemand hat die Startseite eingerichtet.
    Dann gilt der Standard – jede Kachel außerhalb davon ist aus. Eine
    gespeicherte Reihenfolge ist eine eigene Auswahl und bleibt unverändert.
    Ausdrücklich ausgeblendete Kacheln bleiben in jedem Fall aus.
    """
    order = _known(order)
    hidden = _known(hidden)
    if not order:
        hidden += [key for key in KEYS if key not in STANDARD and key not in hidden]
    if not show_stats and "stats" not in hidden:
        hidden.append("stats")
    return order, hidden


def ordered(order):
    """Alle Kacheln in gespeicherter Reihenfolge; unbekannte Namen fallen still heraus."""
    result = _known(order)
    return result + [key for key in KEYS if key not in result]


def own_selection(order, hidden, key=None, hide=None):
    """Hält eine Änderung als eigene Auswahl fest; liefert ``(order, hidden)``.

    Bis 3.33.1 speicherte das Ein- und Ausblenden direkt auf der Startseite
    nur die ausgeblendeten Kacheln. Ohne gespeicherte Reihenfolge setzte der
    nächste Start den Standard wieder ein – eine eingeblendete Uhr war weg.
    """
    hidden = [value for value in _known(hidden) if value != key]
    if key in KEYS and hide:
        hidden.append(key)
    return ordered(order), hidden


def standard_selection():
    """Die Startseite nach D12, wie nach einem Zurücksetzen: ``(order, hidden)``."""
    return [], [key for key in KEYS if key not in STANDARD]


def today_sections(visible):
    """Was die Kachel „Heute“ zusätzlich zeigt, ohne andere sichtbare Kacheln zu doppeln."""
    visible = set(visible)
    return {"goal": "welcome" not in visible, "next": "focus" not in visible}
