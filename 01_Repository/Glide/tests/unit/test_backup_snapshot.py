import io
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from backup_snapshot import read, regular_bytes


def inspect(archive):
    return archive.getinfo('data.json'), {i.filename:i for i in archive.infolist() if i.filename!='data.json'}


def validate(data, *, portable):
    if not isinstance(data, dict) or not isinstance(data.get('lists'),list):
        raise ValueError('Keine Listen')
    return data.get('assets', ())


def member(archive, info, limit):
    with archive.open(info) as source:
        result=source.read(limit+1)
    if len(result)>limit:
        raise ValueError('Daten zu groß')
    return result


class SourceSnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def read(self, path, **kw):
        return read(path,inspect_archive=inspect,validate_data=validate,read_member=member,
                    max_archive_bytes=10000,max_data_bytes=1000,**kw)

    def archive(self, assets=('attachments/a.png',), extra=()):
        path=self.root/'backup.glidebackup'
        with zipfile.ZipFile(path,'w') as archive:
            archive.writestr('data.json',json.dumps(dict(lists=[],assets=list(assets))))
            for name in (*assets,*extra):archive.writestr(name,b'image')
        return path

    def test_archive_changes_after_preview_do_not_change_selected_bytes(self):
        path=self.archive();snapshot=self.read(path);digest=snapshot.sha256
        path.write_bytes(b'danach ersetzt')
        assets=snapshot.capture_assets(snapshot.referenced,max_member_bytes=100,max_total_bytes=100)
        with assets.open('attachments/a.png') as source:self.assertEqual(source.read(),b'image')
        self.assertEqual(snapshot.sha256,digest)
        self.assertEqual(snapshot.available(),snapshot.referenced)

    def test_extra_or_missing_files_are_rejected_before_preview(self):
        with self.assertRaisesRegex(ValueError,'unvollständig|unerwartet'):
            self.read(self.archive(extra=('attachments/b.png',)))
        path=self.root/'missing.glidebackup'
        with zipfile.ZipFile(path,'w') as archive:
            archive.writestr('data.json',json.dumps(dict(lists=[],assets=['attachments/a.png'])))
        with self.assertRaisesRegex(ValueError,'unvollständig'):
            self.read(path)

    def test_size_limits_and_unknown_assets_are_enforced(self):
        snapshot=self.read(self.archive())
        for member_limit,total_limit in ((4,100),(100,4)):
            with self.assertRaises(ValueError):
                snapshot.capture_assets(snapshot.referenced,max_member_bytes=member_limit,max_total_bytes=total_limit)
        with self.assertRaisesRegex(ValueError,'gehört nicht'):
            snapshot.capture_assets(['attachments/fremd.png'],max_member_bytes=100,max_total_bytes=100)
        with self.assertRaises(ValueError):regular_bytes(self.root/'backup.glidebackup',4)

    def test_json_uses_explicit_local_sources_and_freezes_them(self):
        path=self.root/'auto.json';path.write_text(json.dumps(dict(lists=[],assets=['attachments/a.png'])))
        local=self.root/'a.png';local.write_bytes(b'local image')
        snapshot=self.read(path)
        self.assertFalse(snapshot.portable)
        self.assertEqual(snapshot.available(),frozenset())
        paths={'attachments/a.png':local}
        assets=snapshot.capture_assets(snapshot.referenced,max_member_bytes=100,max_total_bytes=100,local_paths=paths)
        local.write_bytes(b'changed')
        with assets.open('attachments/a.png') as source:self.assertEqual(source.read(),b'local image')
        with self.assertRaises(ValueError):
            snapshot.capture_assets(snapshot.referenced,max_member_bytes=100,max_total_bytes=100)

    def test_invalid_json_and_schema_do_not_create_files(self):
        path=self.root/'invalid.json';path.write_text('{')
        with self.assertRaises(ValueError):self.read(path)
        path.write_text(json.dumps(dict(elsewhere=[])))
        with self.assertRaisesRegex(ValueError,'Keine Listen'):self.read(path)
        self.assertEqual(list(self.root.iterdir()),[path])


if __name__=='__main__':unittest.main()
