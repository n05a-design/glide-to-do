"""Wird die Prüf-App beim Einblenden eines Dialogs aktiv (und nimmt damit Tastatur)?"""
import ctypes, ctypes.util, sys, tkinter as tk
objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library("objc"))
objc.objc_getClass.restype = ctypes.c_void_p; objc.objc_getClass.argtypes = [ctypes.c_char_p]
objc.sel_registerName.restype = ctypes.c_void_p; objc.sel_registerName.argtypes = [ctypes.c_char_p]
msg = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(("objc_msgSend", objc))
msg_bool = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(("objc_msgSend", objc))
def aktiv():
    app = msg(objc.objc_getClass(b"NSApplication"), objc.sel_registerName(b"sharedApplication"))
    return msg_bool(app, objc.sel_registerName(b"isActive"))
root = tk.Tk(); root.geometry("300x200+40+40"); root.update()
for _ in range(5): root.update(); root.after(50); 
print("nach Start", aktiv(), flush=True)
variante = sys.argv[1]
d = tk.Toplevel(root); d.transient(root); tk.Entry(d).pack(); 
if variante == "verborgen":
    d.withdraw(); d.update_idletasks(); d.geometry("400x300+80+80"); d.deiconify()
else:
    d.update_idletasks(); d.geometry("400x300+80+80")
for _ in range(10): root.update(); root.after(30)
print(variante, "nach Dialog", aktiv(), flush=True)
d.destroy(); root.destroy()
