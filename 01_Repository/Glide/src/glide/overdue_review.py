# SPDX-License-Identifier: MPL-2.0
"""Ruhiger Umgang mit verstrichenen Fristen (WA-53, Glide 1.1.0) – Tk-frei nach D17.

Grundsätze (D01, D83, Entwicklungsplan WA-53):

* Frist (``due``) und Bearbeitungstag (``planned_date``) bleiben getrennt.
  „Heute einplanen“ setzt nur den Bearbeitungstag; die verstrichene Frist
  bleibt sichtbar, ein tatsächliches Terminproblem wird nicht versteckt.
* Fristen ändert nur eine bewusste, bestätigte Handlung auf ein gewähltes
  Datum ab heute. Serienaufgaben behalten ihre Regel und bleiben unverändert;
  ihr nächster Termin entsteht weiter beim Erledigen.
* Keine automatische Verschiebung, kein Zähler mit Druck, keine Bewertung:
  Die Zusammenfassung nennt Anzahl und Alter neutral.

Das Modul rechnet nur über übergebene Punkte; Mutation, Undo und Speichern
bleiben beim bestehenden Weg der Oberfläche (``apply_quick_plan`` bzw.
``item_change``).
"""
from dataclasses import dataclass
from datetime import date

import i18n as glide_i18n


def _day(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def is_open_task(item):
    return isinstance(item, dict) and not item.get("done") and item.get("kind", "task") in ("task", "long")


def is_overdue(item, today):
    due = _day(item.get("due")) if isinstance(item, dict) else None
    return is_open_task(item) and due is not None and due < today


def is_recurring(item):
    return bool(isinstance(item, dict) and item.get("repeat"))


@dataclass(frozen=True, slots=True)
class OverdueSummary:
    count: int
    oldest_days: int
    planned_today: int
    recurring: int

    @property
    def to_plan(self) -> int:
        """Wie viele noch keinen heutigen Bearbeitungstag haben."""
        return self.count - self.planned_today


def summarize(items, today):
    """Neutrale Zusammenfassung verstrichener Fristen offener Aufgaben."""
    overdue = [item for item in items if is_overdue(item, today)]
    oldest = max(((today - _day(item["due"])).days for item in overdue), default=0)
    heute = today.isoformat()
    return OverdueSummary(
        count=len(overdue), oldest_days=oldest,
        planned_today=sum(1 for item in overdue if item.get("planned_date") == heute),
        recurring=sum(1 for item in overdue if is_recurring(item)),
    )


def plan_today_ids(items, today):
    """Kennungen, die „Heute einplanen“ ändert: verstrichen, offen, nicht schon heute geplant."""
    heute = today.isoformat()
    return tuple(item["id"] for item in items
                 if is_overdue(item, today) and item.get("planned_date") != heute and item.get("id"))


@dataclass(frozen=True, slots=True)
class DueShift:
    new_due: str
    change_ids: tuple[str, ...]
    skipped_recurring: tuple[str, ...]


def due_shift(items, new_due, today):
    """Bewusst neue Frist für verstrichene Aufgaben; Serienaufgaben bleiben unverändert.

    ``new_due`` muss ein ISO-Datum ab heute sein – eine neue Frist in der
    Vergangenheit wäre sofort wieder verstrichen.
    """
    target = _day(new_due)
    if target is None or target.isoformat() != str(new_due)[:10]:
        raise ValueError(glide_i18n.t("mod.overdue_review.invalid_date", "Bitte ein gültiges Datum wählen."))
    if target < today:
        raise ValueError(glide_i18n.t("mod.overdue_review.date_in_past", "Die neue Frist darf nicht vor heute liegen."))
    change, skipped = [], []
    for item in items:
        if not is_overdue(item, today) or not item.get("id"):
            continue
        (skipped if is_recurring(item) else change).append(item["id"])
    return DueShift(target.isoformat(), tuple(change), tuple(skipped))


def banner_text(summary):
    """Ein ruhiger Satz ohne Druck: Anzahl, Alter und was schon für heute geplant ist."""
    if summary.count == 0:
        return ""
    if summary.count == 1:
        text = glide_i18n.t("mod.overdue_review.one", "1 Aufgabe mit verstrichener Frist")
    else:
        text = glide_i18n.t("mod.overdue_review.many", "{n} Aufgaben mit verstrichener Frist", n=summary.count)
    if summary.oldest_days > 1:
        text += glide_i18n.t("mod.overdue_review.oldest", " · älteste seit {days} Tagen", days=summary.oldest_days)
    if summary.planned_today:
        text += glide_i18n.t("mod.overdue_review.planned_today", " · {n} schon für heute eingeplant",
                             n=summary.planned_today)
    return text


def shift_confirmation(shift, day_text, undo_key="Strg+Z"):
    """Rückfragetext vor dem Ändern von Fristen (deutliche Bestätigung, Entwicklungsplan WA-53)."""
    text = glide_i18n.t("mod.overdue_review.confirm", "{n} Fristen auf {day} setzen?", n=len(shift.change_ids), day=day_text)
    if shift.skipped_recurring:
        text += "\n\n" + glide_i18n.t("mod.overdue_review.confirm_recurring",
                                      "{n} Serienaufgaben behalten ihre Regel und bleiben unverändert.",
                                      n=len(shift.skipped_recurring))
    text += "\n\n" + glide_i18n.t("mod.overdue_review.confirm_undo",
                                  "Die bisherigen Fristen lassen sich mit Rückgängig ({shortcut}) wiederherstellen.",
                                  shortcut=undo_key)
    return text
