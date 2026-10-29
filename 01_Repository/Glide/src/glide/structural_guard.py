"""Transaktion des Bestandswächters ohne Tk (WA-27, Befund A32).

`ListApp.guarded_structural_change` sichert zu, dass eine Umbauaktion keinen
Punkt verliert. Bis 18.10.2026 merkte sich der Wächter nur die Tiefe des
Rückgängig-Stapels. Stand der Stapel schon auf seiner Grenze von 20 Schritten,
kürzte die Aktion ihn wieder auf 20 – der Rückweg fand dann keinen Schritt
mehr, der Verlust stand bereits in der Datei, und die Meldung behauptete
trotzdem, alles sei wiederhergestellt.

Dieses Modul hält den Zustand einer Wächterlaufzeit und entscheidet, was
gemeldet werden darf:

- Der Rückgängig-Stapel wird während des Wächters nicht gekürzt; der erste
  Schritt ab `depth_before` ist damit immer der Stand davor (Stapelmarke).
- Jeder Schreibversuch im Wächter prüft vorher den Bestand (`check_save`).
  Ein Verlust erreicht die Datei so gar nicht erst; sie bleibt bytegleich.
- „Vollständig wiederhergestellt“ steht nur da, wenn alle IDs wieder da sind
  und die Datei dem Stand davor entspricht: weil nichts geschrieben wurde oder
  weil das Zurückschreiben gelang.

Die App bleibt Adapter (D17): Sie misst IDs, wendet Schnappschüsse an und
zeigt die Meldung.
"""

import os
import tempfile

RESTORED = "restored"
UNSAVED = "unsaved"
INCOMPLETE = "incomplete"


def item_ids(items, into=None):
    """Punktbäume lesen; Listen-/Ordnerkennungen sind keine Punktkennungen."""
    found = set() if into is None else into
    for item in items or []:
        if not isinstance(item, dict):
            continue
        if item.get('id'):
            found.add(item['id'])
        item_ids(item.get('children', []), found)
    return found


def trash_item_ids(records):
    """Aktueller typisierter Papierkorb und bestehende ältere Payloadformen."""
    found = set()
    for record in records:
        if not isinstance(record, dict):
            continue
        point = record.get('item')
        if isinstance(point, dict):
            item_ids([point], found)
        container = record.get('list')
        if isinstance(container, dict):
            item_ids(container.get('items', []), found)
        for key in ('payload', 'items'):
            legacy = record.get(key)
            if isinstance(legacy, list):
                item_ids(legacy, found)
            elif isinstance(legacy, dict):
                item_ids(legacy['items'] if isinstance(legacy.get('items'), list) else [legacy], found)
    return found


def data_item_ids(lists, trash):
    """Vollständige Punktprojektion für den Wächter, ohne Modellmutation."""
    found = trash_item_ids(trash)
    for entry in lists:
        item_ids(entry.get('items', []), found)
    return found


class GuardTransaction:
    """Zustand eines laufenden Bestandswächters."""

    __slots__ = ("action_name", "before", "depth_before", "writes_before", "dirty_before",
                 "blocked_save", "blocked_missing", "aborted", "records", "file_before", "history_before")

    def __init__(self, action_name, before_ids, depth_before, writes_before=0, dirty_before=False):
        self.action_name = action_name
        self.before = frozenset(before_ids)
        self.depth_before = int(depth_before)
        self.writes_before = writes_before
        self.dirty_before = bool(dirty_before)
        # Der jüngste Schreibversuch im Wächter wurde abgewehrt – und keiner
        # danach gelang. Auch wenn der Aufrufer den Bestand selbst
        # zurückgesetzt hat, ist die Aktion dann nicht ausgeführt.
        self.blocked_save = False
        self.blocked_missing = 0
        self.aborted = False
        # Änderungsrahmen im Wächter; ein Abbruch setzt ihr `saved` auf False.
        self.records = []
        self.file_before = None
        self.history_before = None

    def missing(self, current_ids):
        """IDs, die vorher da waren und jetzt fehlen."""
        return self.before - set(current_ids)

    def check_save(self, current_ids):
        """Vor jedem Schreiben im Wächter: True, wenn der Bestand vollständig ist."""
        missing = self.missing(current_ids)
        self.blocked_save = bool(missing)
        if missing:
            self.blocked_missing = len(missing)
        return not missing

    def file_written(self, writes_now):
        """Ob seit Beginn des Wächters erfolgreich in die Datei geschrieben wurde."""
        return writes_now != self.writes_before

    def needs_abort(self, missing_now, crashed=False, reported=False):
        return bool(crashed or reported or missing_now or self.blocked_save)

    def abort(self):
        """Markiert die Aktion als nicht ausgeführt, auch für ihre Änderungsrahmen."""
        self.aborted = True
        for record in self.records:
            record.saved = False


def outcome(missing_after, file_written, rollback_saved, dirty_before=False):
    """Was nach dem Rückweg tatsächlich gilt.

    `missing_after`: Anzahl der IDs, die nach dem Rückweg noch fehlen.
    `file_written`: Im Wächter wurde die Datei geschrieben.
    `rollback_saved`: Ergebnis des Zurückschreibens (None, wenn keines nötig war).
    """
    if missing_after:
        return INCOMPLETE
    if dirty_before or (file_written and rollback_saved is not True):
        return UNSAVED
    return RESTORED


def restore_bytes(path, data, replace=os.replace):
    """Stellt die Originalbytes atomar wieder her; Fehler gehen an den Wächter.

    Der Adapter liefert seinen Windows-fähigen Ersetzungsweg. Dies ist ein
    interner Rückweg, kein Export in eine frei wählbare Nutzdatendatei.
    """
    fd, temporary = tempfile.mkstemp(prefix=".glide-rollback-", suffix=".tmp",
                                     dir=os.path.dirname(os.path.abspath(path)))
    try:
        with os.fdopen(fd, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.remove(temporary)


def stop_message(action_name, missing_count, result=RESTORED, crashed=False, missing_after=0):
    """Titel und Text der Abbruchmeldung; behauptet nur, was `result` belegt."""
    if crashed:
        detail = "Der Vorgang wurde abgebrochen."
    elif missing_count:
        detail = f"Dabei wären {missing_count} Punkt(e) verloren gegangen."
    else:
        detail = "Dabei wären Punkte verloren gegangen."
    head = f"„{action_name}“ wurde nicht ausgeführt.\n{detail}\n\n"
    if result == RESTORED:
        return ("Abgebrochen – keine Daten verloren",
                head + "Der vorherige Stand ist vollständig wiederhergestellt.")
    if result == UNSAVED:
        return ("Abgebrochen – noch nicht gespeichert",
                head + "Der vorherige Stand steht wieder in Glide, ließ sich aber nicht speichern. "
                "Glide versucht es beim nächsten Speichern erneut und fragt beim Beenden nach.")
    return ("Abgebrochen – Bestand prüfen",
            head + f"Glide konnte den vorherigen Stand nicht vollständig wiederherstellen; "
            f"{missing_after} Punkt(e) fehlen noch. Bitte zuerst mit Strg/Cmd+Z zurücknehmen "
            "und die Liste prüfen. Ältere Stände zeigt „Sicherungen vergleichen …“.")
