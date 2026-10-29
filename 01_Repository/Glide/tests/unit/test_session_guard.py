"""Wiederanlauf prüft ausschließlich künstliche Daten und lokale Marker."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SRC = Path(__file__).resolve().parents[2] / "src/glide"
sys.path.insert(0, str(SRC))
import session_guard as sg


def data():
    return dict(version=26, lists=[dict(id="list-a", items=[dict(
        id="item-a", text="Künstlicher vertraulicher Aufgabeninhalt", children=[])])],
                folders=[], labels=[], trash=[], history=[])


class SessionGuardTests(unittest.TestCase):
    def test_newer_original_blocks_recovery_and_replacement(self):
        next_guard = self.dirty()
        incoming = data()
        original = dict(incoming, version=999)
        self.path.write_text(json.dumps(original), encoding='utf-8')
        raw = self.path.read_bytes()
        self.assertEqual(next_guard.assess().kind, 'newer_format')
        result = next_guard.begin_replacement(lock_owned=True, replacement_data=incoming,
                                              validate_data=lambda value: None)
        self.assertFalse(result.writable)
        self.assertEqual(result.kind, 'newer_format')
        self.assertEqual(raw, self.path.read_bytes())

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="glide-session-unit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.path = self.root / "data/liste_speicher.json"
        self.path.parent.mkdir()
        self.path.write_text(json.dumps(data(), ensure_ascii=False), encoding="utf-8")
        self.original = self.path.read_bytes()
        self.guard = self.new_guard()

    def new_guard(self, **overrides):
        options = dict(state_dir=self.root / "local", host="PRUEFGERAET", pid=1001, alive=lambda pid: False)
        options.update(overrides)
        return sg.SessionGuard(self.path.parent, self.path, **options)

    def dirty(self):
        self.assertTrue(self.guard.begin(lock_owned=True).writable)
        return self.new_guard(pid=1002)

    def test_first_start_requires_data_lock_and_records_no_contents(self):
        self.assertEqual(self.guard.begin(lock_owned=False).kind, "lock_required")
        self.assertFalse(self.guard.marker_path.exists())
        started = self.guard.begin(lock_owned=True)
        self.assertEqual((started.kind, started.writable), ("started", True))
        raw = self.guard.marker_path.read_text(encoding="utf-8")
        self.assertNotIn("vertraulicher", raw)
        self.assertNotIn(str(self.path), raw)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_clean_close_and_next_start_skip_complete_data_analysis(self):
        with mock.patch.object(sg, "_basic_data_check", side_effect=AssertionError("unnötiger Vollscan")):
            self.guard.begin(lock_owned=True)
            self.assertTrue(self.guard.finish(saved=True))
            next_guard = self.new_guard(pid=1002)
            self.assertEqual(next_guard.assess().kind, "clean")
            self.assertTrue(next_guard.begin(lock_owned=True).writable)

    def test_failed_save_never_claims_clean_close(self):
        self.guard.begin(lock_owned=True)
        self.assertFalse(self.guard.finish(saved=False))
        self.assertEqual(json.loads(self.guard.marker_path.read_text())["state"], "running")
        self.assertTrue(self.new_guard(pid=1002).assess().needs_recovery)

    def test_second_begin_is_idempotent_for_owned_session(self):
        first = self.guard.begin(lock_owned=True)
        raw = self.guard.marker_path.read_bytes()
        self.assertEqual(self.guard.begin(lock_owned=True), first)
        self.assertEqual(self.guard.marker_path.read_bytes(), raw)

    def test_unclean_end_needs_explicit_confirmation_and_exact_backup(self):
        next_guard = self.dirty()
        old_marker = next_guard.marker_path.read_bytes()
        checked = next_guard.begin(lock_owned=True)
        self.assertTrue(checked.needs_recovery)
        self.assertFalse(checked.writable)
        self.assertEqual(next_guard.marker_path.read_bytes(), old_marker)
        self.assertFalse((self.path.parent / "backups").exists())
        resumed = next_guard.resume(lock_owned=True, expected_sha256=checked.sha256)
        self.assertEqual((resumed.kind, resumed.writable), ("recovery_started", True))
        self.assertEqual(Path(resumed.preserved_path).read_bytes(), self.original)
        self.assertEqual(self.path.read_bytes(), self.original)
        self.assertTrue(next_guard.finish(saved=True))

    def test_failed_original_copy_keeps_protection_and_marker(self):
        next_guard = self.dirty()
        checked = next_guard.assess()
        marker = next_guard.marker_path.read_bytes()
        with mock.patch.object(next_guard, "preserve_original", side_effect=PermissionError):
            result = next_guard.resume(lock_owned=True, expected_sha256=checked.sha256)
        self.assertEqual(result.kind, "preservation_failed")
        self.assertFalse(result.writable)
        self.assertEqual(next_guard.marker_path.read_bytes(), marker)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_changed_data_invalidates_previous_confirmation(self):
        next_guard = self.dirty()
        checked = next_guard.assess()
        modified = data()
        modified["lists"][0]["items"][0]["text"] = "Nach der Vorschau geändert"
        self.path.write_text(json.dumps(modified), encoding="utf-8")
        current = self.path.read_bytes()
        result = next_guard.resume(lock_owned=True, expected_sha256=checked.sha256)
        self.assertEqual(result.kind, "recovery_changed")
        self.assertFalse((self.path.parent / "backups").exists())
        self.assertEqual(self.path.read_bytes(), current)

    def test_empty_confirmation_or_missing_lock_never_resume(self):
        next_guard = self.dirty()
        self.assertEqual(next_guard.resume(lock_owned=False, expected_sha256="x").kind, "lock_required")
        self.assertEqual(next_guard.resume(lock_owned=True, expected_sha256="").kind, "recovery_changed")

    def test_invalid_data_never_create_empty_replacement_or_new_marker(self):
        next_guard = self.dirty()
        marker = next_guard.marker_path.read_bytes()
        for payload in (b"{", b"[]garbage", b"null", b'{"version":26,"lists":null}',
                        b'{"version":26,"lists":[],"lists":[]}'):
            with self.subTest(payload=payload):
                self.path.write_bytes(payload)
                result = next_guard.begin(lock_owned=True)
                self.assertEqual(result.kind, "invalid_data")
                self.assertFalse(result.writable)
                self.assertEqual(self.path.read_bytes(), payload)
                self.assertEqual(next_guard.marker_path.read_bytes(), marker)

    def test_lost_data_after_dirty_or_clean_session_never_create_empty_file(self):
        for clean in (False, True):
            with self.subTest(clean=clean):
                self.path.write_bytes(self.original)
                self.guard = self.new_guard(pid=2000)
                if self.guard.marker_path.exists():
                    self.guard.marker_path.unlink()
                self.guard.begin(lock_owned=True)
                if clean:
                    self.assertTrue(self.guard.finish(saved=True))
                self.path.unlink()
                result = self.new_guard(pid=2001).assess()
                self.assertEqual(result.kind, "missing_data")
                self.assertFalse(self.path.exists())

    def test_truncated_data_after_simulated_power_loss_remains_unchanged(self):
        next_guard = self.dirty()
        self.path.write_bytes(self.original[:23])
        truncated = self.path.read_bytes()
        self.assertEqual(next_guard.assess().kind, "invalid_data")
        self.assertEqual(self.path.read_bytes(), truncated)

    def test_marker_corruption_and_old_version_require_the_same_explicit_backup(self):
        self.guard.marker_path.parent.mkdir()
        for raw, expected in ((b"{", "defective"), (b'{"marker_version":0}', "obsolete")):
            with self.subTest(expected=expected):
                self.guard.marker_path.write_bytes(raw)
                next_guard = self.new_guard(pid=1002)
                result = next_guard.assess()
                self.assertEqual((result.kind, result.marker_kind), ("recovery_required", expected))
                resumed = next_guard.resume(lock_owned=True, expected_sha256=result.sha256)
                self.assertTrue(resumed.writable)
                self.assertEqual(Path(resumed.preserved_path).read_bytes(), self.original)

    def test_living_second_process_never_replaced_even_with_old_marker(self):
        self.guard.begin(lock_owned=True)
        record = json.loads(self.guard.marker_path.read_text())
        for version in (sg.MARKER_VERSION, 0):
            record["marker_version"] = version
            self.guard.marker_path.write_text(json.dumps(record))
            original = self.guard.marker_path.read_bytes()
            next_guard = self.new_guard(pid=1002, alive=lambda pid: True)
            self.assertEqual(next_guard.begin(lock_owned=True).kind, "active")
            self.assertEqual(next_guard.resume(lock_owned=True, expected_sha256="anything").kind, "active")
            self.assertEqual(next_guard.marker_path.read_bytes(), original)

    def test_foreign_marker_never_replaced(self):
        self.guard.begin(lock_owned=True)
        record = json.loads(self.guard.marker_path.read_text())
        record["host"] = "ANDERER-RECHNER"
        self.guard.marker_path.write_text(json.dumps(record))
        original = self.guard.marker_path.read_bytes()
        self.assertEqual(self.guard.assess().kind, "foreign")
        self.assertFalse(self.guard.finish(saved=True))
        self.assertEqual(self.guard.marker_path.read_bytes(), original)

    def test_implausible_process_id_is_defective_without_calling_native_probe(self):
        self.guard.begin(lock_owned=True)
        record = json.loads(self.guard.marker_path.read_text())
        record["pid"] = 2 ** 100
        self.guard.marker_path.write_text(json.dumps(record))
        next_guard = self.new_guard(pid=1002, alive=mock.Mock(side_effect=AssertionError("Native PID-Probe")))
        result = next_guard.assess()
        self.assertEqual((result.kind, result.marker_kind), ("recovery_required", "defective"))

    def test_unreadable_marker_and_unwritable_state_are_explicit(self):
        with mock.patch.object(sg, "regular_bytes", side_effect=PermissionError):
            self.assertEqual(self.guard.assess().kind, "unreadable")
        with mock.patch.object(self.guard, "_atomic_marker", side_effect=PermissionError):
            result = self.guard.begin(lock_owned=True)
            self.assertEqual((result.kind, result.writable), ("marker_write_failed", False))
            self.assertFalse(self.guard.finish(saved=True))

    def test_missing_marker_and_missing_data_is_a_normal_first_start(self):
        self.path.unlink()
        self.assertTrue(self.guard.begin(lock_owned=True).writable)
        self.assertFalse(self.path.exists())

    def test_foreign_replacement_between_check_and_marker_write_is_not_overwritten(self):
        original_write = self.guard._atomic_marker
        def replacing(record, expected_digest):
            self.guard.marker_path.parent.mkdir(parents=True, exist_ok=True)
            self.guard.marker_path.write_text('{"host":"FREMDER-RECHNER"}')
            original_write(record, expected_digest)
        with mock.patch.object(self.guard, "_atomic_marker", side_effect=replacing):
            self.assertEqual(self.guard.begin(lock_owned=True).kind, "marker_write_failed")
        self.assertEqual(json.loads(self.guard.marker_path.read_text())["host"], "FREMDER-RECHNER")

    def test_failed_clean_marker_write_keeps_running_state(self):
        self.guard.begin(lock_owned=True)
        with mock.patch.object(self.guard, "_atomic_marker", side_effect=PermissionError):
            self.assertFalse(self.guard.finish(saved=True))
        self.assertEqual(json.loads(self.guard.marker_path.read_text())["state"], "running")
        self.assertTrue(self.guard.last_error)

    def test_inspection_calls_existing_validator_without_changing_original(self):
        next_guard = self.dirty()
        validator = mock.Mock(side_effect=ValueError("ungültige Serie"))
        self.assertEqual(next_guard.assess(validate_data=validator).kind, "invalid_data")
        validator.assert_called_once()
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_current_duplicate_ids_and_broken_folder_links_are_rejected(self):
        next_guard = self.dirty()
        variants = []
        duplicate = data(); duplicate["lists"][0]["items"] *= 2; variants.append(duplicate)
        missing = data(); missing["lists"][0]["folder_id"] = "missing"; variants.append(missing)
        cycle = data(); cycle["folders"] = [dict(id="folder", parent_id="folder")]; variants.append(cycle)
        newer = data(); newer["version"] = 27; variants.append(newer)
        invalid_version = data(); invalid_version["version"] = True; variants.append(invalid_version)
        for payload in variants:
            with self.subTest(payload=payload):
                self.path.write_text(json.dumps(payload), encoding="utf-8")
                expected = 'newer_format' if payload is newer else 'invalid_data'
                self.assertEqual(next_guard.assess().kind, expected)

    def test_old_formats_remain_available_for_explicit_migration(self):
        next_guard = self.dirty()
        for payload in (["Alte Aufgabe"], dict(version=4, lists=[dict(items=["Alt"])], folders=[])):
            self.path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertTrue(next_guard.assess().needs_recovery)

    def test_preserving_invalid_bytes_never_rewrites_the_original(self):
        self.path.write_bytes(b"{beschaedigt")
        before = self.path.read_bytes()
        digest = hashlib.sha256(before).hexdigest()
        preserved = self.guard.preserve_original(expected_sha256=digest)
        self.assertEqual(Path(preserved).read_bytes(), before)
        self.assertEqual(self.path.read_bytes(), before)
        with self.assertRaises(ValueError):
            self.guard.preserve_original(expected_sha256="falsch")

    def test_data_change_during_original_copy_blocks_restart(self):
        next_guard = self.dirty()
        checked = next_guard.assess()
        original_preserve = next_guard.preserve_original
        def change(**kwargs):
            path = original_preserve(**kwargs)
            self.path.write_bytes(b"{dazwischen geaendert")
            return path
        with mock.patch.object(next_guard, "preserve_original", side_effect=change):
            result = next_guard.resume(lock_owned=True, expected_sha256=checked.sha256)
        self.assertEqual(result.kind, "preservation_failed")
        self.assertEqual(self.path.read_bytes(), b"{dazwischen geaendert")

    def test_unreadable_data_and_size_limit_remain_protected(self):
        next_guard = self.dirty()
        original_read = sg.regular_bytes
        def read(path, limit):
            if Path(path) == self.path:
                raise PermissionError
            return original_read(path, limit)
        with mock.patch.object(sg, "regular_bytes", side_effect=read):
            self.assertEqual(next_guard.assess().kind, "unreadable_data")
        with mock.patch.object(sg, "MAX_JSON_BYTES", 4):
            self.assertEqual(next_guard.assess().kind, "invalid_data")
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_incomplete_original_copy_is_not_left_as_a_valid_backup(self):
        before = self.path.read_bytes()
        with mock.patch.object(sg.os, "fsync", side_effect=OSError("Datentraegerfehler")):
            with self.assertRaises(OSError):
                self.guard.preserve_original()
        directory = self.path.parent / "backups/wiederanlauf"
        self.assertFalse(list(directory.glob("*.json")))
        self.assertEqual(self.path.read_bytes(), before)

    def test_preserved_payload_keeps_series_references_ids_and_external_attachment(self):
        payload = data()
        task = payload["lists"][0]["items"][0]
        task.update(series_id="series-a", depends_on=["other-item"],
                    attachments=[dict(storage="attachments/beleg.txt")])
        payload["lists"][0]["items"].append(dict(id="other-item", text="Referenzziel", children=[]))
        attachment = self.path.parent / "attachments/beleg.txt"
        attachment.parent.mkdir()
        attachment.write_bytes(b"Kuenstlicher Anhang")
        self.path.write_text(json.dumps(payload), encoding="utf-8")
        original = self.path.read_bytes()
        next_guard = self.dirty()
        checked = next_guard.assess()
        resumed = next_guard.resume(lock_owned=True, expected_sha256=checked.sha256)
        restored = json.loads(Path(resumed.preserved_path).read_bytes())
        self.assertEqual(restored, payload)
        self.assertEqual(Path(resumed.preserved_path).read_bytes(), original)
        self.assertEqual(attachment.read_bytes(), b"Kuenstlicher Anhang")

    def test_resume_requires_recovery_state_and_finish_requires_owned_token(self):
        self.assertEqual(self.guard.resume(lock_owned=True, expected_sha256="anything").kind, "recovery_changed")
        self.assertFalse(self.guard.finish(saved=True))
        self.guard.begin(lock_owned=True)
        other = self.new_guard(pid=1002)
        self.assertFalse(other.finish(saved=True))

    def test_real_abrupt_process_exit_leaves_detectable_unclean_session(self):
        code = """
import os, sys
sys.path.insert(0, sys.argv[1])
from session_guard import SessionGuard
guard = SessionGuard(sys.argv[2], sys.argv[3], state_dir=sys.argv[4], host='PRUEFGERAET')
assert guard.begin(lock_owned=True).writable
os._exit(17)
"""
        child = subprocess.run([sys.executable, "-B", "-c", code, str(SRC), str(self.path.parent),
                                str(self.path), str(self.root / "local")], timeout=20,
                               capture_output=True, text=True)
        self.assertEqual(child.returncode, 17, child.stderr)
        result = self.guard.assess()
        self.assertTrue(result.needs_recovery)
        self.assertFalse(result.writable)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_explicit_test_isolation_never_uses_real_local_state(self):
        with mock.patch.dict(os.environ, GLIDE_DATA_DIR=str(self.path.parent)):
            guard = sg.SessionGuard(self.path.parent, self.path)
        self.assertEqual(guard.state_dir, self.path.parent / ".glide-session")
        self.assertFalse(guard.marker_path.exists())


class ReplacementGuardTests(unittest.TestCase):
    setUp = SessionGuardTests.setUp
    new_guard = SessionGuardTests.new_guard
    dirty = SessionGuardTests.dirty

    def replace(self, guard, **overrides):
        args = dict(lock_owned=True, replacement_data=data(), validate_data=lambda payload: None)
        args.update(overrides)
        return guard.begin_replacement(**args)

    def test_invalid_original_is_preserved_raw_before_explicit_replacement(self):
        guard = self.dirty()
        invalid = b'{"version":26,"abgebrochen":'
        self.path.write_bytes(invalid)
        result = self.replace(guard)
        self.assertEqual((result.kind, result.writable, result.original_missing),
                         ("replacement_started", True, False))
        self.assertEqual(Path(result.preserved_path).read_bytes(), invalid)
        self.assertEqual(self.path.read_bytes(), invalid)
        self.assertEqual(json.loads(guard.marker_path.read_text())["state"], "running")
        self.assertFalse(guard.finish(saved=False))

    def test_missing_original_has_absence_proof_without_fabricated_empty_file(self):
        guard = self.dirty()
        self.path.unlink()
        result = self.replace(guard)
        self.assertTrue(result.writable and result.original_missing)
        evidence = json.loads(Path(result.preserved_path).read_text(encoding="utf-8"))
        self.assertTrue(evidence["original_missing"])
        self.assertEqual(evidence["data_key"], guard.data_key)
        self.assertNotIn("lists", evidence)
        self.assertFalse(self.path.exists())
        self.assertTrue(json.loads(guard.marker_path.read_text())["original_missing"])

    def test_invalid_replacement_is_checked_before_any_backup_or_marker_change(self):
        guard = self.dirty()
        self.path.write_bytes(b"{beschaedigt")
        marker = guard.marker_path.read_bytes()
        validator = mock.Mock(side_effect=ValueError("Serienregel"))
        result = self.replace(guard, validate_data=validator)
        self.assertEqual((result.kind, result.writable), ("invalid_replacement", False))
        validator.assert_called_once()
        self.assertFalse((self.path.parent / "backups").exists())
        self.assertEqual(guard.marker_path.read_bytes(), marker)
        self.assertEqual(self.path.read_bytes(), b"{beschaedigt")

    def test_replacement_requires_strict_validator_and_valid_schema(self):
        guard = self.dirty()
        self.assertEqual(self.replace(guard, validate_data=None).kind, "invalid_replacement")
        self.assertEqual(self.replace(guard, replacement_data=dict(version=999, lists=[])).kind,
                         "invalid_replacement")
        self.assertFalse((self.path.parent / "backups").exists())

    def test_replacement_requires_data_lock_and_never_overrides_living_owner(self):
        guard = self.dirty()
        self.assertEqual(self.replace(guard, lock_owned=False).kind, "lock_required")
        live = self.new_guard(pid=1002, alive=lambda pid: True)
        marker = live.marker_path.read_bytes()
        self.assertEqual(self.replace(live).kind, "active")
        self.assertEqual(live.marker_path.read_bytes(), marker)

    def test_original_hash_preview_change_prevents_backup_and_replacement(self):
        guard = self.dirty()
        original_hash = hashlib.sha256(self.original).hexdigest()
        self.path.write_bytes(b"{anderer_originalzustand")
        self.assertEqual(self.replace(guard, expected_sha256=original_hash).kind, "recovery_changed")
        self.assertFalse((self.path.parent / "backups").exists())

    def test_marker_preview_change_prevents_backup_and_replacement(self):
        guard = self.dirty()
        self.assertEqual(self.replace(guard, expected_marker="nicht-der-markerhash").kind, "recovery_changed")
        self.assertFalse((self.path.parent / "backups").exists())

    def test_copy_failure_preserves_original_marker_and_read_only_result(self):
        guard = self.dirty()
        marker = guard.marker_path.read_bytes()
        with mock.patch.object(guard, "preserve_original", side_effect=PermissionError):
            result = self.replace(guard)
        self.assertEqual((result.kind, result.writable), ("preservation_failed", False))
        self.assertEqual(guard.marker_path.read_bytes(), marker)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_original_changes_during_copy_block_marker_start(self):
        guard = self.dirty()
        marker = guard.marker_path.read_bytes()
        preserve = guard.preserve_original
        def changing(**kwargs):
            path = preserve(**kwargs)
            self.path.write_bytes(b"{neuer_originalzustand")
            return path
        with mock.patch.object(guard, "preserve_original", side_effect=changing):
            result = self.replace(guard)
        self.assertEqual((result.kind, result.writable), ("preservation_failed", False))
        self.assertEqual(guard.marker_path.read_bytes(), marker)
        self.assertEqual(self.path.read_bytes(), b"{neuer_originalzustand")

    def test_missing_original_appearing_during_proof_blocks_marker_start(self):
        guard = self.dirty()
        self.path.unlink()
        marker = guard.marker_path.read_bytes()
        preserve = guard._preserve_absence
        def appearing():
            proof = preserve()
            self.path.write_bytes(self.original)
            return proof
        with mock.patch.object(guard, "_preserve_absence", side_effect=appearing):
            result = self.replace(guard)
        self.assertEqual(result.kind, "preservation_failed")
        self.assertEqual(guard.marker_path.read_bytes(), marker)
        self.assertEqual(self.path.read_bytes(), self.original)

    def test_marker_replaced_during_copy_is_never_overwritten(self):
        guard = self.dirty()
        preserve = guard.preserve_original
        def replacing(**kwargs):
            path = preserve(**kwargs)
            guard.marker_path.write_text('{"host":"FREMDER-RECHNER"}')
            return path
        with mock.patch.object(guard, "preserve_original", side_effect=replacing):
            result = self.replace(guard)
        self.assertEqual((result.kind, result.writable), ("marker_write_failed", False))
        self.assertEqual(json.loads(guard.marker_path.read_text())["host"], "FREMDER-RECHNER")

    def test_precommit_failure_allows_deliberate_retry_only_for_owned_marker(self):
        guard = self.dirty()
        self.path.write_bytes(b"{alter-defekter-bestand")
        first = self.replace(guard)
        self.assertTrue(first.writable)
        self.assertFalse(guard.finish(saved=False))
        second = self.replace(guard)
        self.assertTrue(second.writable)
        self.assertEqual(Path(second.preserved_path).read_bytes(), b"{alter-defekter-bestand")
        self.assertEqual(self.path.read_bytes(), b"{alter-defekter-bestand")
        self.path.write_bytes(self.original)
        self.assertTrue(guard.finish(saved=True))
        self.assertEqual(self.new_guard(pid=1003).assess().kind, "clean")


if __name__ == "__main__":
    unittest.main()
