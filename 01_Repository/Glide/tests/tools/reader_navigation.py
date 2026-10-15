"""Aufgaben in flachen und durch Abschnittszeilen gegliederten Readerbäumen."""


def select_task(key, read_focus, title, *, limit=12):
    key('home')
    spoken = read_focus()
    if title in spoken:
        return spoken
    key('right')
    for _ in range(limit):
        key('down')
        spoken = read_focus()
        if title in spoken:
            return spoken
    raise AssertionError(('Aufgabe per Reader nicht ausgewählt', title, spoken))
