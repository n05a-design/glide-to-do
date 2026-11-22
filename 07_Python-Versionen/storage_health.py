# SPDX-License-Identifier: MPL-2.0
"""Größenbudget und Speicherzustand ohne Tk (WA-40/WA-47)."""
import json
import os
import i18n as glide_i18n

MAX_JSON_BYTES = 32 * 1024 * 1024
WARNING_RATIO = 0.8
LABELS = {"data": "Aufgaben", "settings": "Einstellungen", "templates": "Vorlagen",
          "backup": "Automatische Sicherung", "recovery": "Wiederanlauf",
          "diagnostics": "Lokale Diagnose"}


def label(kind):
    """Anzeigename eines Speicherbereichs in der aktiven Sprache; `LABELS` bleibt die deutsche Vorlage."""
    return glide_i18n.t(f"mod.storage_health.label.{kind}", LABELS.get(kind, kind))


class SizeLimitError(ValueError):
    """Eine Datei überschreitet das gemeinsame JSON-Budget."""


def size_text(size):
    return f"{size / (1024 * 1024):.1f} MiB".replace(".", ",")


def check_size(size, limit=MAX_JSON_BYTES):
    if size > limit:
        raise SizeLimitError(glide_i18n.t("mod.storage_health.check_size.the_json_file_is", 'Die JSON-Datei ist mit {size_text} größer als die unterstützten {size_text2}. Sie bleibt unverändert.', size_text=size_text(size), size_text2=size_text(limit)))


def json_size(text, newline=None):
    """Tatsächliche UTF-8-Größe einschließlich Textmodus-Zeilenenden."""
    newline = os.linesep if newline is None else newline
    return len(text.encode("utf-8")) + text.count("\n") * (len(newline) - 1)


def read_stream(stream, limit=MAX_JSON_BYTES):
    """Vorab prüfen, dann begrenzt lesen; auch Wachstum nach fstat abfangen."""
    check_size(os.fstat(stream.fileno()).st_size, limit)
    raw = stream.read(limit + 1)
    if isinstance(raw, str):
        raw = raw.encode("utf-8")
    check_size(len(raw), limit)
    return json.loads(raw.decode("utf-8-sig"))


def read_json(path, limit=MAX_JSON_BYTES):
    with open(path, "rb") as stream:
        return read_stream(stream, limit)


class Health:
    """Fehler bleiben bis zum Erfolg desselben Speicherwegs sichtbar."""
    def __init__(self):
        self.failures = {}
        self.sizes = {}

    def fail(self, kind, detail):
        detail = str(detail)
        previous = self.failures.get(kind)
        count = previous[1] + 1 if previous and previous[0] == detail else 1
        self.failures[kind] = (detail, count)
        return previous is None or previous[0] != detail

    def success(self, kind, size=None):
        self.failures.pop(kind, None)
        if size is not None:
            self.sizes[kind] = max(0, int(size))

    def capacity_warning(self, limit=MAX_JSON_BYTES):
        # Konservative Frühwarnung: lokale, eingerückte JSON-Dateien zusammen.
        # Die tatsächliche Größe eines App-Backups wird beim Export geprüft.
        return sum(self.sizes.values()) >= limit * WARNING_RATIO

    def notice(self, limit=MAX_JSON_BYTES):
        if self.failures:
            return glide_i18n.t("mod.storage_health.notice.storage_problem_details", "Speicherproblem · Details")
        if self.capacity_warning(limit):
            return glide_i18n.t("mod.storage_health.notice.backup_reserve_details", "Sicherungsreserve · Details")
        return ""

    def report(self, limit=MAX_JSON_BYTES):
        lines = []
        for kind, (detail, count) in self.failures.items():
            attempts = glide_i18n.t("mod.storage_health.report.failed_attempt", "fehlgeschlagener Versuch") if count == 1 else glide_i18n.t("mod.storage_health.report.failed_attempts", "fehlgeschlagene Versuche")
            lines.append(f"{label(kind)}: {count} {attempts}\n{detail}")
        if not lines:
            lines.append(glide_i18n.t("mod.storage_health.report.no_open_storage_errors", "Keine offenen Speicherfehler."))
        lines.append(glide_i18n.t("mod.storage_health.report.size_of_the_local", "\nGröße der lokalen JSON-Dateien:"))
        for kind in ("data", "settings", "templates"):
            value = self.sizes.get(kind)
            lines.append(f"{label(kind)}: {size_text(value) if value is not None else glide_i18n.t("mod.storage_health.report.no_file_yet", 'noch keine Datei')}")
        total = sum(self.sizes.values())
        lines.append(glide_i18n.t("mod.storage_health.report.total_json_limit_per", 'Zusammen: {size_text} · JSON-Grenze je Datei: {size_text2}', size_text=size_text(total), size_text2=size_text(limit)))
        if self.capacity_warning(limit):
            lines.append(glide_i18n.t("mod.storage_health.report.the_local_json_files", "\nDie lokalen JSON-Dateien erreichen mindestens 80 % des Sicherungsbudgets. "
                         "Bitte ein vollständiges App-Backup prüfen. Dessen tatsächliche Größe "
                         "wird beim Export kontrolliert; die Summe hier ist eine Frühwarnung."))
        return "\n\n".join(lines)
