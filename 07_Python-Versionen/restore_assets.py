"""Anhänge für einen selektiven Restore neu ablegen; keine Bestandsmutation, kein Tk."""
import copy
from dataclasses import dataclass
import os
from pathlib import Path
import re
import uuid
import unicodedata
import attachment_paths as paths


def valid_id(value):
    return isinstance(value,str) and 1<=len(value)<=64 and all(c.isascii() and (c.isalnum() or c in '_-') for c in value)


@dataclass
class Staged:
    metadata: dict
    created: tuple
    retained: bool = False

    def keep(self):
        self.retained = True

    def cleanup(self):
        if self.retained:
            return
        for path,identity in reversed(self.created):
            try:
                st=path.stat(follow_symlinks=False)
                if (st.st_dev,st.st_ino)==identity:
                    path.unlink()
            except FileNotFoundError:
                pass

    def __enter__(self):
        return self

    def __exit__(self,*_exc):
        self.cleanup()


def stage(attachments, directory, open_source, *, occupied_ids=(), occupied_storage=(),
          max_bytes, new_id=None, now=''):
    """Dateien nur exklusiv anlegen, vollständig lesen/prüfen und fsync ausführen.

    `open_source(storage)` liefert einen frischen lesbaren Context-Manager,
    etwa ZipExtFile aus einem zuvor vollständig validierten Archiv. Der
    Aufrufer behält die Dateien erst nach erfolgreicher Bestandsübernahme.
    """
    if type(max_bytes)is not int or max_bytes<0:
        raise ValueError('Ungültige Anhangsgrenze.')
    attachments=tuple(attachments)
    original_ids=[a.get('id')for a in attachments if isinstance(a,dict)]
    if (len(original_ids)!=len(attachments) or any(not valid_id(x)for x in original_ids)
            or len(set(original_ids))!=len(original_ids)):
        raise ValueError('Sicherungsanhänge nicht eindeutig.')
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    occupied=set(occupied_ids)|set(original_ids)
    used={paths.storage_key(p)for p in occupied_storage}
    used.update(unicodedata.normalize('NFC','attachments/'+p.name).casefold() for p in directory.iterdir())
    factory=new_id or (lambda:uuid.uuid4().hex)
    result=Staged({},())
    created=[]
    try:
        for original in attachments:
            size=original.get('size')
            if type(size)is not int or not 0<=size<=max_bytes:
                raise ValueError('Unzulässige Sicherungsanhangsgröße.')
            old_storage=paths.validate_storage(original.get('storage'))
            if old_storage!=original['storage']:
                raise ValueError('Nicht kanonischer Sicherungsanhangspfad.')
            for _attempt in range(100):
                identity=factory()
                if not valid_id(identity)or identity in occupied:
                    continue
                suffix=Path(str(original.get('name')or'')).suffix
                suffix=re.sub(r'[^A-Za-z0-9.]','',suffix)[:16].strip('. ')
                storage='attachments/'+identity+('.'+suffix if suffix else '.dat')
                key=paths.storage_key(storage)
                if key in used:
                    continue
                target=directory/storage.split('/')[1]
                try:
                    output=target.open('xb')
                except FileExistsError:
                    used.add(key)
                    continue
                break
            else:
                raise OSError('Kein freier Anhangsname für die Wiederherstellung.')
            # Diese Datei gehört allein dieser Transaktion; nie vorhandene Bytes entfernen.
            st=os.fstat(output.fileno());created.append((target,(st.st_dev,st.st_ino)))
            result.created=tuple(created)
            with output,open_source(old_storage)as source:
                total=0
                while True:
                    chunk=source.read(min(1024*1024,size-total+1))
                    if not chunk:
                        break
                    total+=len(chunk)
                    if total>size or total>max_bytes:
                        raise ValueError('Sicherungsanhang ist größer als angegeben.')
                    output.write(chunk)
                if total!=size:
                    raise ValueError('Sicherungsanhang ist unvollständig.')
                output.flush();os.fsync(output.fileno())
            metadata=copy.deepcopy(original)
            metadata.update(id=identity,storage=storage)
            metadata.setdefault('added_at',now)
            result.metadata[original['id']]=metadata
            occupied.add(identity);used.add(key)
        return result
    except BaseException:
        result.cleanup()
        raise
