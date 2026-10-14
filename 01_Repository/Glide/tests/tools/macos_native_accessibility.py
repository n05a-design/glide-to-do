"""NSAccessibility-Anbieter ausschließlich des eigenen Tk-Testinterpreters.

Keine AX-Desktopinventur und kein Zugriff auf andere Prozesse/Fenster. Dies
prüft native Getter/Aktionen im Testprozess; VoiceOver-Abnahme bleibt getrennt.
Die externe AX-Beobachtung benötigt vom Inhaber verwaltete macOS-Rechte.
"""
import ctypes
from pathlib import Path
import sys


class NativeAccessibility:
    def __init__(self, root, library):
        if sys.platform != 'darwin' or str(root.tk.call('package', 'provide', 'Tk')) != '9.1.0':
            raise RuntimeError('Nur im eigenen macOS-/Tk-9.1-Testprozess.')
        library = Path(library).resolve()
        if not library.is_file() or library.name != 'libtcl9tk9.1.dylib':
            raise ValueError('Expliziter eigener Tk-9.1-Anbieter erforderlich.')
        images = ctypes.PyDLL(None)
        images._dyld_image_count.argtypes = []
        images._dyld_image_count.restype = ctypes.c_uint32
        images._dyld_get_image_name.argtypes = [ctypes.c_uint32]
        images._dyld_get_image_name.restype = ctypes.c_char_p
        loaded = {Path(name.decode('utf-8')).resolve() for index in range(images._dyld_image_count())
                  if (name := images._dyld_get_image_name(index))}
        if library not in loaded:
            raise ValueError('Der angegebene Anbieter ist nicht im eigenen Testprozess geladen.')
        self.root = root
        self.interpreter = root.tk.interpaddr()
        self.tk = ctypes.PyDLL(str(library))
        self.tk.Tk_MainWindow.argtypes = [ctypes.c_void_p]
        self.tk.Tk_MainWindow.restype = ctypes.c_void_p
        self.tk.Tk_NameToWindow.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
        self.tk.Tk_NameToWindow.restype = ctypes.c_void_p
        self.tk.TkAccessibility_GetElementForWindow.argtypes = [ctypes.c_void_p]
        self.tk.TkAccessibility_GetElementForWindow.restype = ctypes.c_void_p
        self.objc = ctypes.PyDLL('/usr/lib/libobjc.A.dylib')
        self.objc.sel_registerName.argtypes = [ctypes.c_char_p]
        self.objc.sel_registerName.restype = ctypes.c_void_p
        # Die einzelnen Signaturen sind auf arm64 verpflichtend; keine
        # variadischen Aufrufe und kein global wechselnder restype.
        self.pointer = ctypes.PYFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', self.objc))
        self.responds = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', self.objc))
        self.string = ctypes.PYFUNCTYPE(ctypes.c_char_p, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', self.objc))
        self.boolean = ctypes.PYFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)(('objc_msgSend', self.objc))

    def selector(self, name):
        return self.objc.sel_registerName(name.encode('ascii'))

    def element(self, widget):
        if widget.tk is not self.root.tk or not widget.winfo_exists():
            raise ValueError('Nur lebende Widgets dieses Testinterpreters.')
        window = self.tk.Tk_NameToWindow(self.interpreter, str(widget).encode('utf-8'),
                                        self.tk.Tk_MainWindow(self.interpreter))
        if not window:
            raise ValueError('Tk-Testfenster fehlt.')
        element = self.tk.TkAccessibility_GetElementForWindow(window)
        if not element:
            raise ValueError('Kein nativer NSAccessibility-Anbieter für das Testwidget.')
        return element

    def describe(self, widget):
        element = self.element(widget)
        def value(selector):
            if not self.responds(element, self.selector('respondsToSelector:'), self.selector(selector)):
                return None
            result = self.pointer(element, self.selector(selector))
            if not result:
                return None
            description = self.pointer(result, self.selector('description'))
            return self.string(description, self.selector('UTF8String')).decode('utf-8')
        return dict(role=value('accessibilityRole'), title=value('accessibilityTitle'),
                    label=value('accessibilityLabel'), value=value('accessibilityValue'),
                    help=value('accessibilityHelp'), identifier=value('accessibilityIdentifier'),
                    enabled=bool(self.boolean(element, self.selector('isAccessibilityEnabled')))
                            if self.responds(element, self.selector('respondsToSelector:'), self.selector('isAccessibilityEnabled')) else None,
                    focused=bool(self.boolean(element, self.selector('isAccessibilityFocused')))
                            if self.responds(element, self.selector('respondsToSelector:'), self.selector('isAccessibilityFocused')) else None,
                    ignored=bool(self.boolean(element, self.selector('accessibilityIsIgnored'))))

    def press(self, widget):
        return bool(self.boolean(self.element(widget), self.selector('accessibilityPerformPress')))
