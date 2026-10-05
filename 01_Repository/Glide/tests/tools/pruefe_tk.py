"""Tk-Start und auf macOS die tatsächliche Mausisolierung eigener QA-Fenster prüfen."""
import os
import sys
import tkinter as tk

root = tk.Tk()
root.geometry('240x120+20+20')
events, errors = [], []
root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
root.bind('<Button-1>', lambda e: events.append(('button', e.x, e.y)))
root.bind('<FocusIn>', lambda e: events.append(('focus',)))


def visible_windows():
    import ctypes
    import ctypes.util
    lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))
    lib.objc_getClass.argtypes = [ctypes.c_char_p]
    lib.objc_getClass.restype = ctypes.c_void_p
    lib.sel_registerName.argtypes = [ctypes.c_char_p]
    lib.sel_registerName.restype = ctypes.c_void_p
    ptr = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', lib))
    number = ctypes.CFUNCTYPE(ctypes.c_ulong, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', lib))
    at = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong)(('objc_msgSend', lib))
    boolean = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', lib))
    sel = lib.sel_registerName
    app = ptr(lib.objc_getClass(b'NSApplication'), sel(b'sharedApplication'))
    windows = ptr(app, sel(b'windows'))
    visible = []
    for i in range(number(windows, sel(b'count'))):
        window = at(windows, sel(b'objectAtIndex:'), i)
        if boolean(window, sel(b'isVisible')):
            visible.append(boolean(window, sel(b'ignoresMouseEvents')))
    return visible


try:
    previous = 0
    for name in ('root', 'dialog', 'tooltip'):
        if name != 'root':
            window = tk.Toplevel(root)
            window.geometry('200x90+30+30')
            if name == 'tooltip':
                window.overrideredirect(True)
        root.update()
        if sys.platform == 'darwin' and os.environ.get('GLIDE_QA_HINTERGRUND'):
            flags = visible_windows()
            assert len(flags) > previous and all(flags), (name, flags)
            previous = len(flags)
            print(name, flags)
    root.event_generate('<Button-1>', x=5, y=7)
    root.event_generate('<FocusIn>')
    root.update()
    assert ('button', 5, 7) in events and ('focus',) in events, events
    assert not errors, errors
    print('Tk', root.tk.call('package', 'provide', 'Tk'),
          '· Tcl', root.tk.call('info', 'patchlevel'),
          '· eigene native Fenster und synthetische Bedienbindungen: ok')
finally:
    root.destroy()
