# SPDX-License-Identifier: MPL-2.0
"""Tk-freie Datums- und Bestandsauswertung für bestehende Ansichten (P09b).

Nur das Lesen identischer Datumszeichenketten wird dauerhaft gemerkt.
Kennzahlen entstehen frisch; die Oberfläche hält sie höchstens einen Aufbau.
"""
from dataclasses import dataclass
from datetime import date, datetime
from functools import lru_cache


@lru_cache(maxsize=4096)
def parsed_date(value):
    """Bisherige strptime-Semantik, einschließlich nicht aufgefüllter Monate."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def due_status(item, today=None):
    value = item.get("due")
    if not value:
        return ""
    parsed = parsed_date(value)
    if parsed is None:
        return ""
    if item.get("done"):
        return "future"
    delta = (parsed - (today or date.today())).days
    return "overdue" if delta < 0 else "today" if delta == 0 else "soon" if delta <= 2 else "future"


@lru_cache(maxsize=4096)
def display_date(value):
    parsed = parsed_date(value)
    return parsed.strftime("%d.%m.%Y") if parsed is not None else ""


@dataclass(frozen=True)
class ItemMetrics:
    total: int = 0
    done: int = 0
    overdue: int = 0
    next_due: str | None = None
    labels: frozenset = frozenset()

    @property
    def stats(self):
        return self.total, self.done, self.overdue


def summarize(items, *, walk, schedulable, normalize_due, regular_labels=(), today=None,
              include_details=True):
    """Ein Durchlauf: Fortschritt, nächste offene Fälligkeit und eigene Labels."""
    today = today or date.today()
    iso_today = today.isoformat()
    regular_labels = frozenset(regular_labels)
    total = done = overdue = 0
    next_due = None
    labels = set()
    for item in walk(items):
        if not schedulable(item):
            continue
        total += 1
        if include_details:
            labels.update(value for value in item.get("labels", []) or [] if value in regular_labels)
        if item.get("done"):
            done += 1
            continue
        if due_status(item, today) == "overdue":
            overdue += 1
        due = normalize_due(item.get("due")) if include_details else None
        if due and due >= iso_today and (next_due is None or due < next_due):
            next_due = due
    return ItemMetrics(total, done, overdue, next_due, frozenset(labels))


def line_height(lines, linespace, pady, inset):
    """Zeilenraum plus aktueller Labelrand; Rand selbst wird nicht gecacht."""
    return lines * linespace + 2 * (int(float(pady or 0)) + inset)


# --- Unterzeile neben dem Logo (D66, menschliche Abnahme 07.11.2026) -------
# Steht das Logo, steht direkt unter dem Titel auch eine Unterzeile: Ohne sie
# wirkte der Kopf leer. Jede Ansicht hat einen sachlichen Ersatztext, falls ihre
# Kennzahlen einmal nichts liefern. Ein Datum steht weiterhin nicht im Kopf
# (B06); ergänzende Bedienhinweise bleiben getrennt und abschaltbar.

VIEW_SUBTITLES = {
    "home": "Dein Überblick für heute",
    "planday": "Tagesplan und heute Fälliges",
    "in_progress": "Aufgaben mit Fälligkeit",
    "overdue": "Verspätete Aufgaben",
    "saved_filter": "Eigene Filteransicht",
    "labels": "Punkte nach Labels",
    "table": "Aufgaben als Tabelle",
    "history": "Letzte Änderungen",
    "templates": "Vorlagen für Listen und Ordner",
    "library": "Listen und Ordner",
    "pages": "Alle Seiten",
    "notes": "Notizen und Notizbücher",
    "drawings": "Alle Zeichnungen",
    "globalboard": "Arbeitsfläche über den gesamten Bestand",
    "trash": "Papierkorb",
    "list": "Liste",
    "folder": "Ordner",
}
DEFAULT_SUBTITLE = "Lokal gespeichert"


def count_text(count, one, many):
    """„1 Aufgabe“, „3 Aufgaben“ – ganze Zahl vorn, Wortform nach Anzahl."""
    count = max(0, int(count or 0))
    return f"{count} {one if count == 1 else many}"


def join_facts(*parts):
    """Nicht leere Angaben mit „ · “ verbunden."""
    return " · ".join(str(part).strip() for part in parts if part and str(part).strip())


def latest_edit(entries):
    """Jüngster Bearbeitungstag (`updated_at`, sonst `created_at`) als JJJJ-MM-TT oder None."""
    tage = []
    for entry in entries or ():
        wert = str((entry or {}).get("updated_at") or (entry or {}).get("created_at") or "")[:10]
        if parsed_date(wert) is not None:
            tage.append(wert)
    return max(tage) if tage else None


def home_subtitle(today_count, late_count=0, upcoming_count=0):
    """Startseite: dieselben Zahlen wie „Heute“, „Verspätet“ und „Demnächst“ – ohne Datum (B06).

    „Heute“ enthält Verspätetes; deshalb „davon … verspätet“. „Demnächst“
    zählt alle Aufgaben mit Fälligkeit (Prüfbefund H7 vom 07.11.2026).
    """
    return join_facts(
        count_text(today_count, "Aufgabe heute", "Aufgaben heute") if today_count else "Heute nichts offen",
        f"davon {int(late_count)} verspätet" if late_count and today_count else
        (f"{int(late_count)} verspätet" if late_count else ""),
        f"{int(upcoming_count)} mit Fälligkeit" if upcoming_count else "")


def templates_subtitle(templates, shown=None):
    """Vorlagen: Gesamtzahl (bzw. Treffer) und Aufteilung nach Listen/Ordnern."""
    templates = list(templates or ())
    listen = sum(1 for vorlage in templates if (vorlage or {}).get("kind") != "folder")
    ordner = len(templates) - listen
    gesamt = (f"{shown} von {len(templates)} Vorlagen" if shown is not None
              else count_text(len(templates), "Vorlage", "Vorlagen"))
    return join_facts(gesamt, count_text(listen, "für Listen", "für Listen") if listen else "",
                      count_text(ordner, "für Ordner", "für Ordner") if ordner else "")


def ensure_subtitle(text, view):
    """Nie leer: vorhandener Text, sonst der Ersatztext der Ansicht."""
    shown = " ".join(str(text or "").split())
    return shown or VIEW_SUBTITLES.get(str(view or ""), DEFAULT_SUBTITLE)
