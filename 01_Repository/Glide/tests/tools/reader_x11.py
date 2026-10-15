"""Prozess des echten X11-Eingabefokus, ausschließlich lesend für Reader-CI.

Tk-Fenster bieten nicht immer _NET_WM_PID. XRes fragt stattdessen den
X-Server nach dem Besitzer der fokussierten Ressource (wie GNOME libwnck).
Kein Fenstertitelvergleich und keine Übernahme fremder Fenster.
"""
import ctypes as C
import sys


def foreground_pid(environment):
    if sys.platform != 'linux':
        raise RuntimeError('X11-Fokusprüfung ausschließlich unter Linux.')
    x11 = C.CDLL('libX11.so.6')
    xres = C.CDLL('libXRes.so.1')

    class Spec(C.Structure):
        _fields_ = [('client', C.c_ulong), ('mask', C.c_uint)]

    class Value(C.Structure):
        _fields_ = [('spec', Spec), ('length', C.c_long), ('value', C.c_void_p)]

    x11.XOpenDisplay.argtypes = [C.c_char_p]
    x11.XOpenDisplay.restype = C.c_void_p
    x11.XCloseDisplay.argtypes = [C.c_void_p]
    x11.XCloseDisplay.restype = C.c_int
    x11.XGetInputFocus.argtypes = [C.c_void_p, C.POINTER(C.c_ulong), C.POINTER(C.c_int)]
    x11.XGetInputFocus.restype = C.c_int
    xres.XResQueryClientIds.argtypes = [C.c_void_p, C.c_long, C.POINTER(Spec),
                                       C.POINTER(C.c_long), C.POINTER(C.POINTER(Value))]
    xres.XResQueryClientIds.restype = C.c_int
    xres.XResGetClientPid.argtypes = [C.POINTER(Value)]
    xres.XResGetClientPid.restype = C.c_int
    xres.XResClientIdsDestroy.argtypes = [C.c_long, C.POINTER(Value)]
    xres.XResClientIdsDestroy.restype = None
    display_name = environment.get('DISPLAY')
    if not display_name:
        raise RuntimeError('Reader-Prüfstand hat keinen eigenen X11-Display.')
    display = x11.XOpenDisplay(display_name.encode())
    if not display:
        raise RuntimeError('Eigenes X11-Display nicht erreichbar.')
    try:
        focused, revert = C.c_ulong(), C.c_int()
        x11.XGetInputFocus(display, C.byref(focused), C.byref(revert))
        if focused.value <= 1:
            raise RuntimeError('Kein tatsächliches Appfenster hat den X11-Eingabefokus.')
        spec = Spec(focused.value, 2)  # XRES_CLIENT_ID_PID_MASK
        count, values = C.c_long(), C.POINTER(Value)()
        status = xres.XResQueryClientIds(display, 1, C.byref(spec), C.byref(count), C.byref(values))
        if status != 0:
            raise RuntimeError('X-Server konnte den Besitzer des fokussierten Fensters nicht belegen.')
        try:
            pids = {xres.XResGetClientPid(C.byref(values[index])) for index in range(count.value)}
            pids.discard(-1)
            if len(pids) != 1 or next(iter(pids)) <= 0:
                raise RuntimeError('Fokussiertes X11-Fenster hat keinen eindeutigen lokalen Prozess.')
            return pids.pop()
        finally:
            if values:
                xres.XResClientIdsDestroy(count, values)
    finally:
        x11.XCloseDisplay(display)
