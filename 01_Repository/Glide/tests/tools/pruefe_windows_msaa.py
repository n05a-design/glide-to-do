"""Eigene native MSAA-Identitäten über echte COM-Getter im Hosted-CI prüfen."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import traceback


def fixture(exchange):
    if not os.environ.get('GLIDE_DATA_DIR'):
        raise ValueError('Eigene temporäre Testdaten fehlen.')
    import tkinter as tk
    sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
    from core_accessibility import bind_entry
    root=tk.Tk();root.geometry('500x300+20+20')
    before=tk.Frame(root);before.pack()
    field=tk.Entry(root,name='field');field.pack()
    bind_entry(field,'Originalfeld')
    phase=0
    def update():
        nonlocal phase,field
        request=exchange/'phase.txt'
        requested=int(request.read_text()) if request.exists() else 0
        if requested != phase:
            if requested==1:
                for _ in range(10):tk.Label(before,text='Künstlicher Nachbar').pack()
            elif requested==2:
                field.destroy()
                field=tk.Entry(root,name='field');field.pack()
                bind_entry(field,'Ersatzfeld')
                field.focus_force()
            elif requested==3:
                root.destroy();return
            phase=requested
            root.update_idletasks()
            root.tk.call('::tk::accessible::add_acc_object',str(root))
        path=exchange/'zustand.tmp'
        path.write_text(json.dumps(dict(pid=os.getpid(),hwnd=root.winfo_id(),phase=phase,focus=str(root.focus_get()))))
        path.replace(exchange/'zustand.json')
        root.after(80,update)
    def ready():
        field.focus_force();root.tk.call('::tk::accessible::add_acc_object',str(root));update()
    root.after(400,ready);root.after(60_000,root.destroy)
    root.mainloop()


def wait_state(exchange, child, phase):
    deadline=time.monotonic()+15
    while time.monotonic()<deadline:
        path=exchange/'zustand.json'
        if path.exists():
            state=json.loads(path.read_text())
            if state['pid']==child.pid and state['phase']==phase:return state
        if child.poll() is not None:raise RuntimeError('Eigene MSAA-Fixture vorzeitig beendet.')
        time.sleep(.05)
    raise TimeoutError('Eigene MSAA-Fixture erreicht Phase nicht: '+str(phase))


def run(destination):
    if (sys.platform!='win32' or os.environ.get('GITHUB_ACTIONS')!='true' or
            os.environ.get('RUNNER_ENVIRONMENT')!='github-hosted'):
        raise RuntimeError('MSAA-Probe nur im vergänglichen Windows-Hosted-CI.')
    destination=destination.resolve();temporary=Path(os.environ['RUNNER_TEMP']).resolve()
    if destination==temporary or not destination.is_relative_to(temporary) or destination.exists():
        raise ValueError('Neuer eigener MSAA-Prüfbereich unter RUNNER_TEMP erforderlich.')
    destination.mkdir(parents=True)
    import ctypes as C
    from ctypes import wintypes as W
    class Guid(C.Structure):
        _fields_=[('a',W.DWORD),('b',W.WORD),('c',W.WORD),('d',C.c_ubyte*8)]
    class Payload(C.Union):
        _fields_=[('integer',C.c_int32),('pointer',C.c_void_p),('record',C.c_void_p*2)]
    class Variant(C.Structure):
        _fields_=[('type',W.WORD),('r1',W.WORD),('r2',W.WORD),('r3',W.WORD),('data',Payload)]
    assert C.sizeof(Variant)==24 and C.sizeof(C.c_void_p)==8
    system=Path(os.environ['SystemRoot'])/'System32'
    ole=C.WinDLL(str(system/'ole32.dll'));acc=C.WinDLL(str(system/'oleacc.dll'))
    automation=C.WinDLL(str(system/'oleaut32.dll'));user=C.WinDLL(str(system/'user32.dll'))
    ole.CoInitializeEx.argtypes=[C.c_void_p,W.DWORD];ole.CoInitializeEx.restype=C.c_int32
    ole.CoUninitialize.argtypes=[];ole.CoUninitialize.restype=None
    initialize=ole.CoInitializeEx(None,2);assert initialize in (0,1),initialize
    acc.AccessibleObjectFromWindow.argtypes=[W.HWND,W.DWORD,C.POINTER(Guid),C.POINTER(C.c_void_p)]
    acc.AccessibleObjectFromWindow.restype=C.c_int32
    automation.SysFreeString.argtypes=[C.c_void_p];automation.SysFreeString.restype=None
    user.GetWindowThreadProcessId.argtypes=[W.HWND,C.POINTER(W.DWORD)];user.GetWindowThreadProcessId.restype=W.DWORD
    result=dict(exitcode=1,nur_eigene_fixture=True,reader_abnahme='getrennt offen')
    child=None;pointer=C.c_void_p()
    try:
        with tempfile.TemporaryDirectory(prefix='glide-msaa-data-',dir=temporary) as data, (destination/'fixture.log').open('w') as log:
            exchange=destination/'austausch';exchange.mkdir()
            child=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'--kind',str(exchange)],
                env=dict(os.environ,GLIDE_DATA_DIR=data,PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=subprocess.STDOUT)
            ready=wait_state(exchange,child,0)
            # winfo_id ist der Tk-Client-HWND mit dessen WM_GETOBJECT-Anbieter.
            # GA_ROOT würde die Windows-Rahmenhülle mit Standard-Oleacc liefern.
            hwnd=ready['hwnd'];owner=W.DWORD()
            user.GetWindowThreadProcessId(hwnd,C.byref(owner));assert owner.value==child.pid
            iid=Guid(0x618736e0,0x3c3d,0x11cf,(C.c_ubyte*8)(0x81,0x0c,0,0xaa,0,0x38,0x9b,0x71))
            assert acc.AccessibleObjectFromWindow(hwnd,0xfffffffc,C.byref(iid),C.byref(pointer))==0 and pointer.value
            table=C.cast(pointer,C.POINTER(C.POINTER(C.c_void_p))).contents
            get_focus=C.WINFUNCTYPE(C.c_int32,C.c_void_p,C.POINTER(Variant))(table[18])
            get_name=C.WINFUNCTYPE(C.c_int32,C.c_void_p,Variant,C.POINTER(C.c_void_p))(table[10])
            def focused():
                value=Variant();code=get_focus(pointer,C.byref(value))
                assert code==0 and value.type==3 and value.data.integer>0,(code,value.type,value.data.integer)
                return value.data.integer
            def name(identity):
                value=Variant();value.type=3;value.data.integer=identity;text=C.c_void_p()
                code=get_name(pointer,value,C.byref(text))
                try:return code,C.wstring_at(text) if text.value else ''
                finally:
                    if text.value:automation.SysFreeString(text)
            original=focused();assert name(original)==(0,'Originalfeld'),name(original)
            (exchange/'phase.txt').write_text('1');wait_state(exchange,child,1)
            after_layout=focused();assert after_layout==original,(original,after_layout)
            assert name(original)==(0,'Originalfeld'),name(original)
            (exchange/'phase.txt').write_text('2');wait_state(exchange,child,2)
            replacement=focused();assert replacement!=original,(original,replacement)
            assert name(original)[0]!=0,'Entfernte Widgetkennung darf kein neues Widget adressieren.'
            assert name(replacement)==(0,'Ersatzfeld'),name(replacement)
            (exchange/'phase.txt').write_text('3');child.wait(timeout=15)
            assert name(replacement)[0]!=0,'Gehaltenes Root-Interface muss nach Destroy geschlossen sein.'
            result.update(exitcode=0,original_id=original,layout_id=after_layout,ersatz_id=replacement,checks=[
                'Echte COM-Fokus-/Namensgetter der eigenen Tk-Fixture',
                'Gehaltene Kindkennung bleibt nach zusätzlichen Nachbarn gleich',
                'Entfernte Kennung ungültig; Ersatz am gleichen Widgetpfad erhält neue Kennung',
                'Gehaltenes Root-Interface nach Destroy verweigert Zugriff'])
    except Exception as error:
        result.update(fehler=str(error),traceback=traceback.format_exc())
    finally:
        if pointer.value:
            table=C.cast(pointer,C.POINTER(C.POINTER(C.c_void_p))).contents
            C.WINFUNCTYPE(W.ULONG,C.c_void_p)(table[2])(pointer)
        if child is not None and child.poll() is None:child.terminate();child.wait(timeout=10)
        ole.CoUninitialize()
    (destination/'ergebnis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Native MSAA-Identitätsprobe Exit',result['exitcode'])
    return result['exitcode']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--ziel',type=Path);parser.add_argument('--kind',type=Path,help=argparse.SUPPRESS)
    args=parser.parse_args()
    if args.kind:fixture(args.kind)
    elif args.ziel:raise SystemExit(run(args.ziel))
    else:parser.error('--ziel erforderlich')
