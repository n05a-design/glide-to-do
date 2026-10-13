"""Echte Bestandsnormalisierung ohne Tk-Fenster; nur künstliche Daten."""
import copy
import contextlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from types import SimpleNamespace

WORK = Path(__file__).resolve().parents[1]
DATA = tempfile.TemporaryDirectory(prefix='glide-animation-bruecke-')
os.environ.update(GLIDE_DATA_DIR=DATA.name, GLIDE_TEST_MODE='1')
SOURCE = WORK.parent / 'src/glide'
sys.path.insert(0, str(SOURCE))
loader = importlib.machinery.SourceFileLoader('glide_schema3400', str(SOURCE / 'app.pyw'))
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
sys.modules[loader.name] = mod
loader.exec_module(mod)


class SchemaBridgeTests(unittest.TestCase):
    def setUp(self):
        self.app = mod.ListApp.__new__(mod.ListApp)
        self.app.labels = []
        self.app.settings = {}
        self.app.lists = []
        self.app.folders = []
        self.app.trash = []
        self.app.flush_rich_note = lambda: True
        self.sequence = mod.glide_animation.Animation.from_legacy(
            mod.glide_drawing.DrawingModel.blank(16).to_document())
        self.second = self.sequence.duplicate('frame-1', new_identity='zweites-bild')
        self.sequence.frames[1].model.set_cell(0, 0, "#123456")
        self.sequence.set_duration(270)
        self.sequence.set_duration(90, self.second)
        self.fields = mod.glide_animation.entry_fields(self.sequence)

    def entry(self):
        return self.app.new_list_object('Bildfolge', list_id='folge', list_kind='drawing', **self.fields)

    def test_old_drawings_become_one_frame_and_new_sequences_keep_all_fields(self):
        for size in (16, 32, 64, 128):
            drawing = mod.glide_drawing.DrawingModel.blank(size).to_document()
            entry = self.app.new_list_object('Altzeichnung', list_kind='drawing', drawing=drawing)
            self.assertEqual(entry['drawing'], drawing)
            self.assertEqual(len(entry['animation']['frames']), 1)
            self.assertEqual(entry['animation']['frames'][0]['drawing'], drawing)
        entry = self.entry()
        self.assertEqual({key: entry[key] for key in self.fields}, self.fields)
        entry['animation']['frames'][1]['duration_ms'] = 200
        self.assertEqual(self.fields['animation']['frames'][1]['duration_ms'], 90)

    def test_normalized_dataset_and_trash_keep_full_sequence(self):
        entry = self.entry()
        data = dict(version=24, lists=[entry], trash=[dict(id='papierkorb', kind='list', list=entry)])
        before = copy.deepcopy(data)
        loaded, _active = self.app.normalize_lists_data(data)
        self.assertEqual(loaded[0]['animation'], self.fields['animation'])
        self.assertEqual(self.app.trash[0]['list']['animation'], self.fields['animation'])
        self.assertEqual(data, before)
        self.assertEqual(self.app.normalize_lists_data(dict(version=23, lists=[
            {k: v for k, v in entry.items() if k != 'animation'}]))[0][0]['animation']['frames'][0]['drawing'], entry['drawing'])
        with self.assertRaisesRegex(ValueError, 'Datenformat-Version'):
            self.app.normalize_lists_data(dict(version=self.app.DATA_SCHEMA_VERSION + 1, lists=[entry]))

    def test_corrupt_or_misplaced_sequence_is_rejected_without_source_mutation(self):
        for field in ('drawing', 'animation'):
            damaged = copy.deepcopy(self.fields)
            if field == 'drawing':
                damaged['drawing']['palette'][0] = '#000000'
            else:
                damaged['animation']['frames'][1]['id'] = 'frame-1'
            before = copy.deepcopy(damaged)
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.app.new_list_object('Defekt', list_kind='drawing', **damaged)
            self.assertEqual(damaged, before)
        with self.assertRaisesRegex(ValueError, 'Zeichnungsseite'):
            self.app.new_list_object('Seite', list_kind='page', **self.fields)

    def test_history_detects_a_later_frame_and_duration_change(self):
        entry = self.entry()
        original = self.app.drawing_history_hash(entry)
        changed = copy.deepcopy(entry)
        changed['animation']['frames'][1]['duration_ms'] = 200
        self.assertNotEqual(self.app.drawing_history_hash(changed), original)
        changed = copy.deepcopy(entry)
        drawing = changed['animation']['frames'][1]['drawing']
        drawing['rows'][0] = '00' + drawing['rows'][0][2:]
        self.assertNotEqual(self.app.drawing_history_hash(changed), original)
        self.assertEqual(self.app.drawing_history_hash(copy.deepcopy(entry)), original)

    def test_format24_backup_failure_stops_real_writer_before_history_or_file_write(self):
        calls, writes = [], []
        self.app.clear_render_cache = lambda: None
        self.app.refresh_data_lock = lambda: None
        self.app.sync_current_list_reference = lambda: None
        for version in (12, 13, 14, 15, 16, 17, 18, 19, 20, 21):
            setattr(self.app, 'ensure_schema'+str(version)+'_backup', lambda: None)
        def guard(version):
            calls.append(version)
            if version == 24:
                raise OSError('synthetischer Format-24-Vorsicherungsfehler')
        self.app.ensure_schema_backup = guard
        self.app.list_comparison = lambda **kw: writes.append('history')
        self.app.write_json_atomic = lambda *a: writes.append('file')
        self.assertFalse(self.app.save_items(show_error=False))
        self.assertEqual(calls, [22, 23, 24])
        self.assertEqual(writes, [])

    def test_snapshot_save_failure_rolls_back_metadata_undo_and_own_attachment(self):
        entry = self.entry()
        self.app.lists = [entry]
        self.app.undo_stack = ['vorher']
        self.app.dirty = False
        self.app.history = {'before': True}
        self.app._history_baseline = {'before': True}
        self.app.drawing_entry = lambda editor: entry
        self.app.themed_input_dialog = lambda *a, **k: 'Ganze Folge'
        self.app.update_sidebar_list = self.app.clear_render_cache = lambda: None
        messages, errors = [], []
        self.app.show_error = lambda *args: errors.append(args)
        editor = SimpleNamespace(animation=self.sequence, flush=lambda: True,
                                 update_status=messages.append)
        attachments = Path(mod.ATTACHMENTS_DIR)
        attachments.mkdir(parents=True, exist_ok=True)
        before_files = {p.name: p.read_bytes() for p in attachments.iterdir() if p.is_file()}
        before = copy.deepcopy(entry)
        @contextlib.contextmanager
        def failed_change(**kwargs):
            change = mod.ChangeRecord(())
            self.app.undo_stack.append('fehlgeschlagen')
            yield change
            change.saved = False
            self.app.history = {'failed': True}
            self.app.dirty = True
        self.app.sidebar_change = failed_change
        self.assertFalse(self.app.drawing_snapshot_save(editor))
        self.assertEqual(entry, before)
        self.assertEqual(self.app.undo_stack, ['vorher'])
        self.assertFalse(self.app.dirty)
        self.assertEqual(self.app.history, {'before': True})
        self.assertEqual(self.app._history_baseline, {'before': True})
        self.assertEqual({p.name: p.read_bytes() for p in attachments.iterdir() if p.is_file()}, before_files)
        self.assertFalse(messages, 'Kein Erfolg nach fehlgeschlagenem Speichern')
        self.assertTrue(errors)

    def test_read_only_snapshot_does_not_open_prompt_or_create_attachment(self):
        self.app._data_read_only = True
        self.app.drawing_entry = lambda editor: self.entry()
        self.app.themed_input_dialog = lambda *a, **k: self.fail('Schreibschutz öffnet Namensdialog')
        self.app.store_attachment = lambda *a: self.fail('Schreibschutz legt Anhang an')
        self.assertFalse(self.app.drawing_snapshot_save(SimpleNamespace()))

    def test_exchange_creation_v2_is_complete_and_v1_stays_readable(self):
        self.assertEqual(self.app.EXCHANGE_FORMAT_VERSION, 2)
        self.assertEqual(self.app.exchange_capabilities()['animations'], 1)
        self.assertEqual(self.app.exchange_capabilities()['max_animation_frames'], 120)
        self.assertEqual(self.app.exchange_capabilities()['animation_duration_ms'], [20, 60000])
        entry = self.entry()
        payload = self.app.build_exchange_payload(lists=[entry])
        self.assertEqual(payload['format_version'], 2)
        self.assertEqual(payload['lists'][0]['animation'], entry['animation'])
        value, report = self.app.parse_exchange_document(json.dumps(payload))
        self.assertIsNotNone(value, report.errors)
        self.assertFalse(report.errors or report.unknown_fields)
        self.assertEqual(value['lists'][0]['animation'], entry['animation'])
        old = copy.deepcopy(payload)
        old['format_version'] = 1
        old['lists'][0].pop('animation')
        value, report = self.app.parse_exchange_document(json.dumps(old))
        self.assertIsNotNone(value, report.errors)
        self.assertFalse(report.errors)
        old['lists'][0].update(list_kind='page', animation=entry['animation'])
        value, report = self.app.parse_exchange_document(json.dumps(old))
        self.assertIsNone(value)
        self.assertTrue(any('Zeichnungsseite' in message for message in report.errors))


if __name__ == '__main__':
    try:
        unittest.main()
    finally:
        DATA.cleanup()
