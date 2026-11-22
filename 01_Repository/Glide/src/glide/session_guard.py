# SPDX-License-Identifier: MPL-2.0
"""Lokaler Sitzungsnachweis und lesende Wiederanlaufprüfung ohne Tk.

Dieser Nachweis ersetzt weder die Datensperre noch eine Sicherung. Ein
ungeklärtes Ende erlaubt erst nach Prüfung, bewusster Freigabe und bytegleicher
Vorsicherung wieder einen schreibenden Start. Der Adapter erwirbt davor die
bestehende Datensperre und markiert erst nach erfolgreichem Speichern sauber.
"""
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import uuid

from backup_snapshot import regular_bytes
from data_lock import host_name, process_alive
from storage_health import MAX_JSON_BYTES
import i18n as glide_i18n


MARKER_VERSION = 1
MAX_MARKER_BYTES = 64 * 1024


@dataclass(frozen=True)
class Assessment:
    kind: str
    writable: bool
    detail: str = ""
    marker_kind: str = ""
    sha256: str = ""
    preserved_path: str = ""
    original_missing: bool = False

    @property
    def needs_recovery(self):
        return self.kind == "recovery_required"


def _stamp():
    return datetime.now(timezone.utc).isoformat()


def _sync_directory(directory):
    # POSIX benötigt zusätzlich die Verzeichnis-Metadaten. Windows bietet
    # hierfür keine entsprechende Python-Schnittstelle; Datei-fsync und
    # atomarer Austausch bleiben dort die verfügbare Betriebssystemgrenze.
    if os.name != "nt":
        fd = os.open(directory, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def _default_state_dir():
    isolated = os.environ.get("GLIDE_DATA_DIR")
    if isolated:
        return Path(isolated) / ".glide-session"
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Glide/sessions"
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA") or Path.home()) / "Glide/sessions"
    return Path(os.environ.get("XDG_STATE_HOME") or Path.home() / ".local/state") / "glide/sessions"


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(glide_i18n.t("mod.session_guard.unique_object.the_json_file_contains", "Die JSON-Datei enthält doppelte Feldnamen."))
        result[key] = value
    return result


def _basic_data_check(data, schema_version):
    """Konservative Strukturprüfung; der Adapter ergänzt seinen Schema-Prüfer.

    Fehlende IDs alter Formate bleiben migrierbar. Nicht auflösbare interne
    Textverweise sind zulässige Inhalte; Ordnerbezüge und doppelte vorhandene
    IDs gehören dagegen zum Speichervertrag.
    """
    if isinstance(data, list):
        lists, folders = [{"items": data}], []
    elif isinstance(data, dict):
        version = data.get("version")
        if version is not None and (type(version) is not int or not 1 <= version <= schema_version):
            raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.the_data_format_version", "Die Datenformat-Version wird nicht unterstützt."))
        lists, folders = data.get("lists"), data.get("folders", [])
        if not isinstance(lists, list) or not isinstance(folders, list):
            raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.list_or_folder_fields", "Listen- oder Ordnerfelder sind ungültig."))
        for name in ("labels", "trash", "history"):
            if not isinstance(data.get(name, []), list):
                raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.a_shared_data_field", "Ein gemeinsames Bestandsfeld ist ungültig."))
    else:
        raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.the_file_contains_no", "Die Datei enthält keinen Glide-Bestand."))

    def ids(entries, label):
        found = set()
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError(glide_i18n.t("mod.session_guard.ids.a_is_invalid", 'Ein {label} ist ungültig.', label=label))
            ident = entry.get("id")
            if ident is not None:
                if not isinstance(ident, str) or not ident or ident in found:
                    raise ValueError(glide_i18n.t("mod.session_guard.ids.a_id_is_invalid", 'Eine {label}-ID ist ungültig oder doppelt.', label=label))
                found.add(ident)
        return found

    folder_ids = ids(folders, glide_i18n.t("ui.kachel_boards.folder", "Ordner"))
    ids(lists, glide_i18n.t("editor.toolbar.list", "Liste"))
    parents = {entry.get("id"): entry.get("parent_id") for entry in folders}
    for entry in folders:
        ident, parent = entry.get("id"), entry.get("parent_id")
        seen = {ident}
        while parent is not None:
            if not isinstance(parent, str) or parent not in folder_ids or parent in seen:
                raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.a_folder_reference_is", "Ein Ordnerbezug fehlt oder bildet einen Kreis."))
            seen.add(parent)
            parent = parents.get(parent)
    item_ids = set()
    for entry in lists:
        folder = entry.get("folder_id")
        if folder is not None and (not isinstance(folder, str) or folder not in folder_ids):
            raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.a_list_refers_to", "Eine Liste verweist auf einen fehlenden Ordner."))
        items = entry.get("items", [])
        if not isinstance(items, list):
            raise ValueError(glide_i18n.t("ui.validate_backup_schema.the_task_field_of_2", "Das Aufgabenfeld einer Liste ist ungültig."))
        stack = [(item, 0) for item in items]
        while stack:
            item, depth = stack.pop()
            if depth > 100:
                raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.the_task_data_is", "Der Aufgabenbestand ist zu tief verschachtelt."))
            if isinstance(item, str):
                continue
            if not isinstance(item, dict):
                raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.a_task_item_is", "Ein Aufgabenpunkt ist ungültig."))
            ident = item.get("id")
            if ident is not None:
                if not isinstance(ident, str) or not ident or ident in item_ids:
                    raise ValueError(glide_i18n.t("mod.session_guard.basic_data_check.a_task_id_is", "Eine Aufgaben-ID ist ungültig oder doppelt."))
                item_ids.add(ident)
            children = item.get("children", [])
            if not isinstance(children, list):
                raise ValueError(glide_i18n.t("ui.validate_backup_schema.the_subtasks_of_a", "Die Unterpunkte einer Aufgabe sind ungültig."))
            stack.extend((child, depth + 1) for child in children)


class SessionGuard:
    """Ein Nachweis pro Gerät und Datendatei; alle Schreibwege brauchen Besitz.

    ``state_dir`` ist für isolierte Prüfungen und portable Adapter explizit
    setzbar. Standardmäßig liegt der Marker im lokalen Zustandsordner und
    enthält nur technische Metadaten, keine Dateipfade oder Aufgabeninhalte.
    """

    def __init__(self, data_dir, data_file, *, state_dir=None, schema_version=26,
                 host=None, pid=None, alive=process_alive):
        self.data_dir = Path(data_dir).absolute()
        path = Path(data_file)
        self.data_file = path.absolute() if path.is_absolute() else self.data_dir / path
        self.state_dir = Path(state_dir) if state_dir is not None else _default_state_dir()
        self.host = host or host_name()
        self.pid = os.getpid() if pid is None else pid
        self.alive = alive
        self.schema_version = schema_version
        key = os.path.normcase(os.path.realpath(self.data_file))
        self.data_key = hashlib.sha256(key.encode("utf-8")).hexdigest()
        device_key = hashlib.sha256(self.host.encode("utf-8")).hexdigest()[:16]
        self.marker_path = self.state_dir / f"{device_key}-{self.data_key}.json"
        self._owned_token = None
        self._begun = None
        self.last_error = ""

    def _marker(self):
        try:
            raw = regular_bytes(self.marker_path, MAX_MARKER_BYTES)
        except FileNotFoundError:
            return "missing", None, None
        except OSError:
            return "unreadable", None, None
        except ValueError:
            return "defective", None, None
        digest = hashlib.sha256(raw).hexdigest()
        try:
            record = json.loads(raw.decode("utf-8"), object_pairs_hook=_unique_object)
            if not isinstance(record, dict):
                raise ValueError
            if isinstance(record.get("host"), str) and record["host"] and record["host"] != self.host:
                return "foreign", record, digest
            if ("pid" in record and
                    (type(record["pid"]) is not int or not 0 < record["pid"] <= 2147483647)):
                raise ValueError
            if (record.get("state") == "running" and record.get("host") == self.host
                    and type(record.get("pid")) is int and record["pid"] > 0
                    and record.get("token") != self._owned_token and self.alive(record["pid"])):
                return "active", record, digest
            if type(record.get("marker_version")) is not int or record["marker_version"] != MARKER_VERSION:
                return "obsolete", record, digest
            if (record.get("data_key") != self.data_key
                    or not isinstance(record.get("host"), str)
                    or not record["host"]
                    or type(record.get("pid")) is not int or record["pid"] <= 0
                    or not isinstance(record.get("token"), str) or not record["token"]
                    or record.get("state") not in ("running", "clean")):
                raise ValueError
            instant = datetime.fromisoformat(record["started_at"])
            if instant.tzinfo is None:
                raise ValueError
        except (ValueError, TypeError, KeyError, UnicodeError, RecursionError, OverflowError):
            return "defective", None, digest
        if record["host"] != self.host:
            return "foreign", record, digest
        if record["state"] == "clean":
            return "clean", record, digest
        if self._owned_token and record["token"] == self._owned_token and record["pid"] == self.pid:
            return "owned", record, digest
        # Keine Zeitfrist erklärt einen lebenden Besitzer für beendet. Bei
        # wiederverwendeter PID bleibt ein konservativer, sichtbarer Schutz.
        if self.alive(record["pid"]):
            return "active", record, digest
        return "unclean", record, digest

    def _inspect(self, marker_kind, validate_data):
        try:
            content = regular_bytes(self.data_file, MAX_JSON_BYTES)
            data = json.loads(content.decode("utf-8-sig"), object_pairs_hook=_unique_object)
            if (isinstance(data, dict) and type(data.get('version')) is int
                    and data['version'] > self.schema_version):
                return Assessment('newer_format', False,
                                  glide_i18n.t("ui.read_only_notice.the_data_comes_from", 'Der Bestand stammt aus einer neueren Glide-Version und bleibt unverändert.'), marker_kind)
            _basic_data_check(data, self.schema_version)
            if validate_data is not None:
                validate_data(data)
        except FileNotFoundError:
            return Assessment("missing_data", False,
                              glide_i18n.t("mod.session_guard.inspect.after_the_unclear_end", "Nach dem ungeklärten Ende fehlt die Datendatei. Es wird kein leerer Bestand gespeichert."),
                              marker_kind)
        except OSError as exc:
            return Assessment("unreadable_data", False,
                              glide_i18n.t("mod.session_guard.inspect.the_data_file_could", 'Die Datendatei konnte nicht lesend geprüft werden ({name}).', name=type(exc).__name__), marker_kind)
        except (ValueError, TypeError, KeyError, UnicodeError, RecursionError) as exc:
            if type(exc).__name__ == 'NewerDataError':
                return Assessment('newer_format', False,
                                  glide_i18n.t("mod.session_guard.inspect.the_data_contains_data", 'Der Bestand enthält Daten einer neueren Glide-Version und bleibt unverändert.'), marker_kind)
            return Assessment("invalid_data", False,
                              glide_i18n.t("mod.session_guard.inspect.the_read_only_data", 'Die lesende Bestandsprüfung ist fehlgeschlagen ({name}). Originaldatei erhalten; eine Sicherung kann bewusst ausgewählt werden.', name=type(exc).__name__), marker_kind)
        return Assessment("recovery_required", False,
                          glide_i18n.t("mod.session_guard.inspect.the_previous_end_is", "Der vorherige Abschluss ist ungeklärt. Der Bestand ist lesbar geprüft. "
                          "Schreibend fortsetzen erfordert eine bewusste Freigabe mit Originalvorsicherung."),
                          marker_kind, hashlib.sha256(content).hexdigest())

    def assess(self, *, validate_data=None):
        """Nur lesen; eine gültige Altsitzung wird niemals still freigegeben."""
        kind, record, _ = self._marker()
        if kind in ("active", "foreign"):
            return Assessment(kind, False, glide_i18n.t("mod.session_guard.assess.the_session_record_belongs", "Der Sitzungsnachweis gehört einem anderen oder noch lebenden Prozess."), kind)
        if kind == "unreadable":
            return Assessment(kind, False, glide_i18n.t("mod.session_guard.assess.the_local_session_record", "Der lokale Sitzungsnachweis ist nicht lesbar."), kind)
        if kind == "owned":
            return self._begun or Assessment("started", True, marker_kind=kind)
        if kind == "missing":
            return Assessment("new", True, marker_kind=kind)
        if kind == "clean" and not (record.get("data_present") and not self.data_file.exists()):
            return Assessment("clean", True, marker_kind=kind)
        return self._inspect(kind, validate_data)

    def _atomic_marker(self, record, expected_digest):
        self.state_dir.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".glide-session-", suffix=".tmp", dir=self.state_dir)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write((json.dumps(record, sort_keys=True) + "\n").encode("utf-8"))
                stream.flush()
                os.fsync(stream.fileno())
            _, _, actual_digest = self._marker()
            if actual_digest != expected_digest:
                raise OSError(glide_i18n.t("mod.session_guard.atomic_marker.the_session_record_was", "Der Sitzungsnachweis wurde zwischenzeitlich verändert."))
            os.replace(temporary, self.marker_path)
            _sync_directory(self.state_dir)
        finally:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass

    def _start(self, assessment, *, expected_digest, preserved_path="", kind=None, original_missing=False):
        token = uuid.uuid4().hex
        record = dict(marker_version=MARKER_VERSION, data_key=self.data_key, host=self.host,
                      pid=self.pid, token=token, state="running", started_at=_stamp())
        if kind == "replacement_started":
            record["original_missing"] = original_missing
        try:
            self._atomic_marker(record, expected_digest)
        except (OSError, ValueError) as exc:
            self.last_error = glide_i18n.t("mod.session_guard.start.session_record_cannot_be", 'Sitzungsnachweis nicht schreibbar ({name}).', name=type(exc).__name__)
            return Assessment("marker_write_failed", False, self.last_error, assessment.marker_kind,
                              assessment.sha256, preserved_path)
        self._owned_token = token
        result = Assessment(kind or ("recovery_started" if preserved_path else "started"), True,
                            glide_i18n.t("mod.session_guard.start.original_backed_up_unchanged", "Original unverändert gesichert; Wiederanlauf freigegeben.") if preserved_path else "",
                            assessment.marker_kind, assessment.sha256, preserved_path, original_missing)
        self._begun = result
        return result

    def begin(self, *, lock_owned, validate_data=None):
        if lock_owned is not True:
            return Assessment("lock_required", False, glide_i18n.t("mod.session_guard.begin.the_data_lock_is", "Vor dem Sitzungsstart ist die Datensperre erforderlich."))
        _, _, digest = self._marker()
        assessment = self.assess(validate_data=validate_data)
        if not assessment.writable or self._owned_token:
            return assessment
        return self._start(assessment, expected_digest=digest)

    def preserve_original(self, *, expected_sha256=None, destination_dir=None):
        """Originalbytes exklusiv sichern; Fehler brechen die Freigabe ab.

        Auch beschädigtes JSON darf hier gesichert werden. Eine fehlende Datei
        oder ein geänderter Vorschauhash wird nie als leere Sicherung ersetzt.
        """
        content = regular_bytes(self.data_file, MAX_JSON_BYTES)
        digest = hashlib.sha256(content).hexdigest()
        if expected_sha256 is not None and digest != expected_sha256:
            raise ValueError(glide_i18n.t("mod.session_guard.preserve_original.the_data_file_was", "Die Datendatei wurde seit der Prüfung verändert."))
        directory = Path(destination_dir) if destination_dir is not None else self.data_dir / "backups/wiederanlauf"
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        target = directory / f"liste_vor_wiederanlauf_{stamp}_{uuid.uuid4().hex[:8]}.json"
        # Exklusive Anlage statt Ersetzen: keine frühere Vorsicherung opfern.
        created = False
        try:
            with target.open("xb") as stream:
                created = True
                stream.write(content)
                stream.flush()
                os.fsync(stream.fileno())
            if hashlib.sha256(regular_bytes(target, MAX_JSON_BYTES)).hexdigest() != digest:
                raise OSError(glide_i18n.t("mod.session_guard.preserve_original.the_original_pre_backup", "Die Originalvorsicherung stimmt nicht mit den gelesenen Bytes überein."))
            _sync_directory(directory)
        except (OSError, ValueError):
            if created:
                try:
                    target.unlink()
                except OSError:
                    pass
            raise
        return str(target)

    def resume(self, *, lock_owned, expected_sha256, validate_data=None):
        """Bewusste Freigabe nur desselben lesbar geprüften Bestands."""
        if lock_owned is not True:
            return Assessment("lock_required", False, glide_i18n.t("mod.session_guard.resume.the_data_lock_is", "Vor dem Wiederanlauf ist die Datensperre erforderlich."))
        _, _, digest = self._marker()
        assessment = self.assess(validate_data=validate_data)
        if not assessment.needs_recovery:
            return assessment if not assessment.writable else Assessment(
                "recovery_changed", False, glide_i18n.t("mod.session_guard.resume.the_restart_state_was", "Der Wiederanlaufzustand wurde zwischenzeitlich verändert."), assessment.marker_kind)
        if not expected_sha256 or assessment.sha256 != expected_sha256:
            return Assessment("recovery_changed", False, glide_i18n.t("mod.session_guard.resume.the_data_was_changed", "Der Bestand wurde seit der Vorschau verändert."),
                              assessment.marker_kind, assessment.sha256)
        try:
            preserved = self.preserve_original(expected_sha256=expected_sha256)
            if hashlib.sha256(regular_bytes(self.data_file, MAX_JSON_BYTES)).hexdigest() != expected_sha256:
                raise ValueError(glide_i18n.t("mod.session_guard.resume.the_data_file_was", "Die Datendatei wurde während der Vorsicherung verändert."))
        except (OSError, ValueError) as exc:
            return Assessment("preservation_failed", False,
                              glide_i18n.t("mod.session_guard.resume.the_original_pre_backup", 'Die Originalvorsicherung ist fehlgeschlagen ({name}). Der Bestand bleibt schreibgeschützt.', name=type(exc).__name__), assessment.marker_kind, assessment.sha256)
        return self._start(assessment, expected_digest=digest, preserved_path=preserved)

    def _original_digest(self):
        try:
            content = regular_bytes(self.data_file, MAX_JSON_BYTES)
        except FileNotFoundError:
            if os.path.lexists(self.data_file):
                raise OSError(glide_i18n.t("mod.session_guard.original_digest.the_existing_data_path", "Der vorhandene Datenpfad ist nicht als reguläre Datei lesbar.")) from None
            return None
        return hashlib.sha256(content).hexdigest()

    def _preserve_absence(self):
        """Fehlende Quelle dokumentieren, ohne einen leeren Datenbestand zu erfinden."""
        directory = self.data_dir / "backups/wiederanlauf"
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        target = directory / f"liste_vor_wiederanlauf_{stamp}_{uuid.uuid4().hex[:8]}.abwesenheit.json"
        proof = dict(evidence_version=1, original_missing=True, data_key=self.data_key,
                     host=self.host, recorded_at=_stamp())
        created = False
        try:
            with target.open("x", encoding="utf-8") as stream:
                created = True
                json.dump(proof, stream, sort_keys=True)
                stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            _sync_directory(directory)
        except OSError:
            if created:
                try:
                    target.unlink()
                except OSError:
                    pass
            raise
        return str(target)

    def begin_replacement(self, *, lock_owned, replacement_data, validate_data,
                          expected_sha256=None, expected_marker=None):
        """Bewusst gewähltes Restore vorbereiten; der Adapter commitet erst danach.

        Der Eingangsbestand und seine Anhangbytes sind vor dem Aufruf zu
        prüfen. Der zwingende Validator prüft hier erneut die Datenstruktur.
        Beschädigte Originalbytes werden roh gesichert; eine fehlende Datei
        erhält ausschließlich einen Abwesenheitsbeleg. Nach einem gescheiterten
        Commit darf dieselbe eigene laufende Sitzung erneut versuchen.
        """
        if lock_owned is not True:
            return Assessment("lock_required", False, glide_i18n.t("mod.session_guard.begin_replacement.the_data_lock_is", "Vor der Wiederherstellung ist die Datensperre erforderlich."))
        marker_kind, _, marker_digest = self._marker()
        if marker_kind in ("active", "foreign", "unreadable"):
            return Assessment(marker_kind, False,
                              glide_i18n.t("mod.session_guard.begin_replacement.the_session_record_belongs", "Der Sitzungsnachweis gehört einem anderen Prozess oder ist nicht lesbar."), marker_kind)
        original_check = self._inspect(marker_kind, validate_data)
        if original_check.kind == 'newer_format':
            return original_check
        if expected_marker is not None and expected_marker != marker_digest:
            return Assessment("recovery_changed", False, glide_i18n.t("mod.session_guard.begin_replacement.the_session_record_was", "Der Sitzungsnachweis wurde seit der Vorschau verändert."), marker_kind)
        try:
            if not callable(validate_data):
                raise ValueError(glide_i18n.t("mod.session_guard.begin_replacement.a_strict_schema_checker", "Ein strenger Schema-Prüfer ist erforderlich."))
            _basic_data_check(replacement_data, self.schema_version)
            validate_data(replacement_data)
        except (ValueError, TypeError, KeyError, UnicodeError, RecursionError) as exc:
            return Assessment("invalid_replacement", False,
                              glide_i18n.t("mod.session_guard.begin_replacement.the_chosen_restore_is", 'Die gewählte Wiederherstellung ist nicht gültig ({name}).', name=type(exc).__name__), marker_kind)
        try:
            original_digest = self._original_digest()
            if expected_sha256 is not None and original_digest != expected_sha256:
                return Assessment("recovery_changed", False,
                                  glide_i18n.t("mod.session_guard.begin_replacement.the_original_file_was", "Die Originaldatei wurde seit der Vorschau verändert."), marker_kind,
                                  original_digest or "")
            preserved = (self._preserve_absence() if original_digest is None else
                         self.preserve_original(expected_sha256=original_digest))
            if self._original_digest() != original_digest:
                raise ValueError(glide_i18n.t("mod.session_guard.begin_replacement.the_original_state_was", "Der Originalzustand wurde während der Vorsicherung verändert."))
        except (OSError, ValueError) as exc:
            return Assessment("preservation_failed", False,
                              glide_i18n.t("mod.session_guard.begin_replacement.the_original_pre_backup", 'Die Originalvorsicherung ist fehlgeschlagen ({name}). Der Bestand bleibt schreibgeschützt.', name=type(exc).__name__), marker_kind)
        assessment = Assessment("replacement_ready", False, marker_kind=marker_kind,
                                sha256=original_digest or "", original_missing=original_digest is None)
        return self._start(assessment, expected_digest=marker_digest, preserved_path=preserved,
                           kind="replacement_started", original_missing=original_digest is None)

    def finish(self, *, saved):
        """Nur nach erfolgreichem Save und nur den eigenen Nachweis abschließen."""
        if saved is not True or not self._owned_token:
            return False
        kind, record, digest = self._marker()
        if (kind != "owned" or record["token"] != self._owned_token or record["pid"] != self.pid):
            self.last_error = glide_i18n.t("mod.session_guard.finish.your_own_session_record", "Der eigene Sitzungsnachweis ist nicht mehr vorhanden.")
            return False
        record = dict(record, state="clean", finished_at=_stamp(), data_present=self.data_file.is_file())
        try:
            self._atomic_marker(record, digest)
        except (OSError, ValueError) as exc:
            self.last_error = glide_i18n.t("mod.session_guard.finish.the_clean_end_of", 'Der saubere Sitzungsabschluss konnte nicht vermerkt werden ({name}).', name=type(exc).__name__)
            return False
        self._owned_token = None
        self._begun = None
        return True
