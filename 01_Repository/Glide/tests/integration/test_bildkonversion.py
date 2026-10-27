"""WA-26: echte Renderwege mit blockiertem Konverter, Hostabbau und Retry.

--app erlaubt die Gegenprobe mit der App vor der Umstellung. Alle Daten und
der PNG-Cache entstehen temporär; auch der langsame Konverter berührt kein Tk.
"""
import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO/'src/glide'))
sys.path.insert(0, str(REPO/'tests/integration'))
from test_schutzrunde import Lauf


def pump(run, predicate, timeout=5):
    deadline=time.monotonic()+timeout
    while time.monotonic()<deadline:
        run.idle(1)
        if predicate():
            return
        time.sleep(.005)
    raise AssertionError('Erwarteter Vorschauzustand blieb aus')


@contextmanager
def converter(run, directory, fail=False):
    cache=run.app.previews
    cache.PLATFORM='nt'  # Gleicher Konversionsvertrag auch auf Mac/Linux.
    png=run.mod.tk.PhotoImage(master=run.root,width=20,height=12)
    png.put('#1185e1',to=(0,0,20,12))
    target=Path(directory)/'synthetisch.png';png.write(str(target),format='png');data=target.read_bytes()
    release=threading.Event();entered=threading.Event();calls=[];cancelled=[]
    main=threading.get_ident();mode={'fail':fail}
    def work(path, cache_dir, platform, expected=None, cancel=None, **kwargs):
        calls.append(threading.get_ident());entered.set()
        event=cancel or threading.Event()
        if threading.get_ident() == main:
            time.sleep(.15)  # Rote Gegenprobe bleibt endlich statt im alten Tk-Callback zu hängen.
            return None
        while not release.wait(.01):
            if event.is_set():
                cancelled.append(path);return None
        if event.is_set():
            cancelled.append(path);return None
        if mode.get('unexpected'):
            raise ValueError('C:/Privat/Bild.jpg: geheimer Inhalt')
        if mode['fail']:
            return None
        result=cache.converted_path(path, expected)
        Path(result).parent.mkdir(parents=True,exist_ok=True);Path(result).write_bytes(data)
        return result
    # Die alte App darf für die rote Gegenprobe nicht im Test selbst hängen.
    with patch('image_conversion.convert_file',work):
        try:
            yield cache,release,entered,calls,cancelled,mode
        finally:
            release.set();cache.close()


def assert_responsive(run, entered, calls):
    pump(run,entered.is_set)
    tick=[];run.root.after(1,lambda:tick.append(threading.get_ident()))
    pump(run,lambda:bool(tick))
    assert calls and all(t!=threading.get_ident() for t in calls),'Konverter im Tk-Hauptthread'
    assert tick==[threading.get_ident()],'Tk-Rückruf fehlt während Konversion'


def gallery(run,path):
    app=run.app
    entry=app.new_list_object('Vorschauprobe',[],list_kind='gallery')
    app.lists.append(entry);app.set_active_list(entry['id'])
    app.add_gallery_images(entry['id'],[str(path)])
    return app.gallery_view


def fall_galerie(run,path,control):
    cache,release,entered,calls,*_=control
    run.root.geometry('860x700+20+20')
    run.app.settings['ui_font_size']='gross'
    view=gallery(run,path)
    view.set_tile_size('small')
    assert_responsive(run,entered,calls)
    for _ in range(5):view.redraw()
    assert len(calls)==1,'Doppelte Konversion desselben Dateistands'
    labels=[i for i in view.canvas.find_all() if view.canvas.type(i)=='text'
            and 'Wird geladen' in view.canvas.itemcget(i,'text')]
    assert labels,'Ladezustand fehlt'
    bounds=view.canvas.bbox(labels[0]);tile=view.hits[0][0]
    assert tile[0]<=bounds[0] and bounds[2]<=tile[2],('Status ragt aus Kachel',bounds,tile)
    release.set()
    pump(run,lambda:view.thumbnail(view.images()[0],80) is not None)
    assert cache._conversions is not None,'Kein gemeinsamer Dienst'


def fall_seite(run,path,control):
    cache,release,entered,calls,*_=control
    run.app.new_page_from_markdown('# Bild\n\nText')
    run.idle();editor=run.app.rich_note_editor
    keys=editor.insert_images([str(path)],'3.0')
    assert keys
    assert_responsive(run,entered,calls);release.set()
    pump(run,lambda:any(getattr(view,'_photo',None) is not None for view in editor._image_views.values()))


def fall_startseite(run,path,control):
    cache,release,entered,calls,*_=control
    attachment=run.app.store_attachment(str(path))
    widget=run.mod.tk.Label(run.root);widget.pack()
    run.app.show_home_gallery_thumbnail(widget,attachment,64)
    assert_responsive(run,entered,calls);release.set()
    pump(run,lambda:bool(widget.cget('image')))
    widget.destroy()


def fall_titelbild(run,path,control):
    cache,release,entered,calls,*_=control
    attachment=run.app.store_attachment(str(path))
    entry={'attachments':[attachment],'cover':{'kind':'image','attachment':attachment['id']}}
    host=run.mod.tk.Frame(run.root);host.pack()
    canvas=run.app.make_page_cover(host,entry,image_path=str(path));canvas.pack()
    assert_responsive(run,entered,calls)
    assert cache._conversions is not None,'Titelbild startet weiterhin eigenen Thread'
    release.set();pump(run,lambda:getattr(canvas,'_photo',None) is not None)
    host.destroy()


def fall_pinnwand(run,path,control):
    cache,release,entered,calls,cancelled,_=control
    app=run.app
    item=app.new_item('Karte mit Bild')
    item['attachments']=[app.store_attachment(str(path))]
    entry=app.new_list_object('Pinnwandprobe',[item])
    app.lists.append(entry);app.set_active_list(entry['id'])
    view=app.workspace
    view.pin([item['id']]);run.idle()
    assert_responsive(run,entered,calls)
    assert item['id'] in view.card_ids and not view._card_images
    first_host=view.canvas
    for _ in range(5):view.draw_board()
    assert len(calls)==1,'Pinnwand startet doppelte Konversion'
    view.set_mode('list');run.idle()
    pump(run,lambda:bool(cancelled))
    assert not cache._requests,'Verdeckte Pinnwand behält Beobachter'
    view.set_mode('board');run.idle()
    assert view.canvas is not first_host,'Alter Pinnwand-Host wiederverwendet'
    release.set();pump(run,lambda:bool(view._card_images))
    assert len(calls)==2,'Neuer Host fordert Konversion nicht erneut an'
    assert view.card_preview(item,160) is not None


def fall_retry(run,path,control):
    cache,release,entered,calls,_,mode=control;mode['fail']=True
    view=gallery(run,path)
    assert_responsive(run,entered,calls);release.set()
    attachment=view.images()[0];stored=run.app.resolve_attachment_path(attachment)
    pump(run,lambda:cache.conversion_status(stored)=='failed' and not cache._requests)
    for _ in range(10):view.redraw();run.idle()
    assert len(calls)==1,'Fehlversuch wird endlos wiederholt'
    mode['fail']=False;view.retry_thumbnail(0)
    pump(run,lambda:view.thumbnail(attachment,80) is not None)
    assert len(calls)==2,'Expliziter Retry startet nicht genau einen neuen Versuch'


def fall_hostwechsel(run,path,control):
    cache,release,entered,calls,cancelled,_=control
    host=run.mod.tk.Frame(run.root);host.pack();callbacks=[]
    cache.request_conversion(host,str(path),lambda result:callbacks.append(result))
    assert_responsive(run,entered,calls)
    host.destroy()
    pump(run,lambda:bool(cancelled))
    assert not callbacks and not cache._requests,'Rückruf oder Bindung lebt nach Hostabbau weiter'
    # Derselbe Dateistand kann in einem neuen Host erneut angefordert werden.
    host2=run.mod.tk.Frame(run.root);host2.pack()
    cache.request_conversion(host2,str(path),lambda result:callbacks.append(result))
    release.set();pump(run,lambda:bool(callbacks));host2.destroy()
    assert len(calls)==2


def fall_generation(run,path,control):
    cache,release,entered,calls,_,_=control
    host=run.mod.tk.Frame(run.root);host.pack();callbacks=[]
    cache.request_conversion(host,str(path),lambda result:callbacks.append(result))
    assert_responsive(run,entered,calls)
    old_key=cache.conversion_key(str(path))
    path.write_bytes(b'Neuer Dateistand mit anderem Umfang')
    pump(run,lambda:cache._conversions.state(old_key)[0]=='cancelled')
    release.set();pump(run,lambda:bool(callbacks))
    assert callbacks==[cache.existing_conversion(str(path))],'Veraltetes Ergebnis im neuen Dateistand'
    assert callbacks[0] and len(calls)==2
    host.destroy()


def fall_referenz(run,path,control):
    cache,release,entered,calls,*_=control
    app=run.app;entry=app.new_list_object('Referenzprobe',[],list_kind='drawing')
    app.lists.append(entry);app.set_active_list(entry['id']);run.idle()
    editor=app.drawing_editor;assert editor is not None
    dialogs=[]
    with patch.object(run.mod.filedialog,'askopenfilename',return_value=str(path)):
        app.drawing_reference_frame_dialog=lambda *a,**k:dialogs.append(threading.get_ident())
        app.drawing_load_reference(editor)
        assert_responsive(run,entered,calls)
        assert not dialogs,'Dialog vor abgeschlossener Konversion'
        release.set();pump(run,lambda:bool(dialogs))
    assert dialogs==[threading.get_ident()]


def fall_warteschlange(run,path,control):
    cache,release,entered,calls,*_=control
    host=run.mod.tk.Frame(run.root);host.pack();callbacks=[]
    for i in range(120):
        source=path.with_name(f'probe-{i}.jpg');source.write_bytes(b'Bildquelle')
        cache.request_conversion(host,str(source),lambda result:callbacks.append((result,threading.get_ident())))
    assert_responsive(run,entered,calls)
    assert len(cache._conversions._queue)<=32
    assert cache._poll_job and all('timer' not in r for r in cache._requests.values()),'Eigener Timer pro Bild'
    release.set();pump(run,lambda:len(callbacks)==120,timeout=10)
    assert all(result and thread==threading.get_ident() for result,thread in callbacks)
    assert not cache._requests and cache._poll_job is None
    host.destroy()


def fall_diagnose(run, path, control):
    cache, release, entered, calls, cancelled, mode = control
    mode['unexpected'] = True
    host = run.mod.tk.Frame(run.root)
    host.pack()
    messages, results = [], []
    with patch.object(run.app, 'log_error', side_effect=lambda text: messages.append((text, threading.get_ident()))):
        cache.request_conversion(host, str(path), lambda value: results.append(value))
        assert_responsive(run, entered, calls)
        release.set()
        pump(run, lambda: len(results) == 1)
        assert len(messages) == 1 and 'ValueError' in messages[0][0], messages
        assert messages[0][1] == threading.get_ident(), 'Diagnose aus dem Worker'
        assert 'Privat' not in messages[0][0] and 'geheimer Inhalt' not in messages[0][0]
        cache._conversions.submit(('retry-diagnose',), lambda cancel: (_ for _ in ()).throw(ValueError('Privat')))
        pump(run, lambda: cache._conversions.state(('retry-diagnose',))[0] == 'failed')
        cache._poll_conversions()
        assert len(messages) == 1, 'Gleiche Fehlerklasse flutet das Protokoll'
    assert results == [None]
    host.destroy()


FAELLE=('galerie','seite','startseite','titelbild','pinnwand','retry','hostwechsel','generation','referenz','warteschlange','diagnose')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report',type=Path);parser.add_argument('--fall',choices=FAELLE)
    args=parser.parse_args();report={'faelle':{},'fehler':[]}
    for name in ([args.fall] if args.fall else FAELLE):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-wa26-') as directory:
            try:
                run=Lauf(args.app,str(Path(directory)/'daten'))
                path=Path(directory)/'probe.jpg';path.write_bytes(b'Synthetische Konvertereingabe')
                with converter(run,directory) as control:
                    globals()['fall_'+name](run,path,control)
                assert not run.errors,run.errors
                report['faelle'][name]={'ok':True};print('OK',name,flush=True)
            except Exception as error:
                report['faelle'][name]={'ok':False,'fehler':str(error).replace(str(Path.home()),'~')[:700]}
                report['fehler'].append(name);print('ROT',name,report['faelle'][name]['fehler'],flush=True)
            finally:
                if run is not None:
                    run.app.previews.close();run.ende()
    if args.report:
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'gruen':len(report['faelle'])-len(report['fehler']),'rot':report['fehler']},ensure_ascii=False))
    return int(bool(report['fehler']))


if __name__=='__main__':
    raise SystemExit(main())
