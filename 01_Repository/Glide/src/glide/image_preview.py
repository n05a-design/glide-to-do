"""Bildvorschauen für Galerie und Seiten mit den Mitteln von Tk 9 (27.09.2026).

Glide bleibt ohne Bildbibliothek. Was Tk 9 selbst kann, reicht weit:

- **macOS:** Der Bildtyp `nsimage` lädt über das System alles, was die
  Vorschau-App öffnet (PNG, JPEG, HEIC, WebP, TIFF, GIF, BMP), und skaliert
  glatt auf jede Breite. Kein Unterprozess, keine Zwischendatei.
- **SVG:** `photo` liest SVG seit Tk 9 selbst (nanosvg) und rechnet es auf die
  gewünschte Breite (`-scaletowidth`).
- **PNG, GIF, PPM:** liest `photo` überall. Verkleinert wird in rationalen
  Stufen (`copy -zoom p -subsample q`), also ohne Glättung.
- **Übrige Formate unter Windows:** Die Windows-Bildkomponenten (WIC) wandeln
  über PowerShell in ein PNG im Cache – so wie `sips` unter macOS. HEIC und
  WebP gehen dort nur mit den Erweiterungen aus dem Microsoft Store.
- **Linux:** PNG, GIF und SVG direkt; JPEG und weitere Formate, wenn ein
  Systemwerkzeug vorhanden ist (`gdk-pixbuf-thumbnailer`, sonst `djpeg` für
  JPEG; seit 3.34.0, N08, `preview_tools.py`). Sonst zeigt die Vorschau die
  Endung.

Alle geladenen Bilder bleiben in einem kleinen Zwischenspeicher je
Anzeigegröße, damit Galerie und Seiten beim Scrollen und Neuzeichnen nicht
erneut dekodieren. Nur Standardbibliothek und tkinter.
"""

import collections
import functools
import hashlib
import os
import sys
import tkinter as tk

import preview_tools as glide_preview_tools
import image_conversion as glide_image_conversion
from image_conversion import MAX_CONVERTED, windows_convert_command

NATIVE = (".png", ".gif", ".ppm", ".pgm")
VECTOR = (".svg",)
CONVERTIBLE = (".jpg", ".jpeg", ".heic", ".heif", ".webp", ".tif", ".tiff", ".bmp")
IMAGE_EXTENSIONS = NATIVE + VECTOR + CONVERTIBLE
FILE_PATTERN = " ".join("*" + endung for endung in IMAGE_EXTENSIONS)


def extension(path):
    return os.path.splitext(str(path or ""))[1].lower()


def is_image_name(name):
    return extension(name) in IMAGE_EXTENSIONS


def has_nsimage(master):
    try:
        return "nsimage" in master.tk.call("image", "types")
    except tk.TclError:
        return False


def has_svg(master):
    """Tk 9 liest SVG; Tk 8.6 nicht."""
    try:
        probe = tk.PhotoImage(master=master, format="svg",
                              data='<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>')
        probe.tk.call("image", "delete", probe.name)
        return True
    except tk.TclError:
        return False


def rational_factor(faktor, max_nenner=12):
    """(zoom, subsample) mit zoom/subsample möglichst nahe an `faktor`, nie darüber."""
    if faktor >= 1:
        zoom = max(1, int(faktor))
        return zoom, 1
    beste = (1, max_nenner)
    for nenner in range(1, max_nenner + 1):
        zaehler = int(faktor * nenner)
        if zaehler >= 1 and zaehler / nenner > beste[0] / beste[1]:
            beste = (zaehler, nenner)
    if beste[0] / beste[1] > faktor:
        # Sehr kleine Faktoren: nur verkleinern.
        return 1, max(1, round(1 / faktor + 0.5))
    return beste




class PreviewCache:
    """Lädt Bilder in Anzeigegröße und merkt sich die letzten `limit` Stück."""

    # Plattform für Umwandlung; Prüfungen erzwingen so den Linux-Weg (N08).
    PLATFORM = None

    def __init__(self, cache_dir=None, limit=160, diagnostic=None):
        self._cache_dir = cache_dir
        self._limit = limit
        self._images = collections.OrderedDict()
        self._sizes = {}
        self._nsimage = None
        self._svg = None
        self._conversions = None
        self._requests = {}
        self._observers = collections.Counter()
        self._poll_root = None
        self._poll_job = None
        self._diagnostic = diagnostic
        self._reported_conversion_errors = ()

    # --- Werkzeuge -------------------------------------------------------
    def cache_dir(self):
        ordner = self._cache_dir() if callable(self._cache_dir) else self._cache_dir
        return ordner or os.path.join(os.path.expanduser("~"), ".glide-cache")

    @staticmethod
    def stamp(path):
        try:
            info = os.stat(path)
        except OSError:
            return None
        return (os.path.normcase(os.path.abspath(path)), info.st_mtime_ns, info.st_size)

    def uses_nsimage(self, master):
        if self._nsimage is None:
            self._nsimage = has_nsimage(master)
        return self._nsimage

    def reads_svg(self, master):
        if self._svg is None:
            self._svg = has_svg(master)
        return self._svg

    def platform(self):
        return self.PLATFORM or ("nt" if os.name == "nt" else sys.platform)

    def converted_base(self, path, stamp=None):
        stamp = stamp or self.stamp(path)
        if stamp is None:
            return None
        schluessel = hashlib.sha1(repr(stamp).encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir(), schluessel)

    def converted_path(self, path, stamp=None):
        basis = self.converted_base(path, stamp)
        return basis + ".png" if basis else None

    def existing_conversion(self, path, stamp=None):
        """Vorhandene Vorschaudatei (PNG, unter Linux auch PPM aus `djpeg`) oder None."""
        basis = self.converted_base(path, stamp)
        if not basis:
            return None
        for endung in (".png", ".ppm"):
            if os.path.isfile(basis + endung) and os.path.getsize(basis + endung) > 0:
                return basis + endung
        return None

    def native_loader(self, master):
        """Lädt macOS über `nsimage`? Nur auf dem Mac – Prüfungen können das abschalten."""
        return self.platform() == "darwin" and self.uses_nsimage(master)

    def needs_conversion(self, master, path):
        """True, wenn erst ein Unterprozess eine Vorschau anlegen muss."""
        endung = extension(path)
        if endung not in CONVERTIBLE or self.native_loader(master):
            return False
        return bool(self.converted_base(path)) and not self.existing_conversion(path) and self.can_convert(path) and self.conversion_status(path) != 'failed'

    def can_convert(self, path=None):
        """Gibt es einen Umwandlungsweg? Unter Linux nur mit passendem Systemwerkzeug."""
        if self.platform() in ("darwin", "nt"):
            return True
        if path is None:
            return any(glide_preview_tools.shutil.which(name) for name in ("gdk-pixbuf-thumbnailer", "djpeg"))
        return glide_preview_tools.linux_plan(path, "x") is not None

    def convert(self, path):
        """Blockierender Werkzeugweg; UI-Einstiege verwenden request_conversion."""
        return glide_image_conversion.convert_file(path, self.cache_dir(), self.platform())

    def conversion_key(self, path):
        return (self.stamp(path), self.cache_dir(), self.platform())

    def conversion_status(self, path):
        return self._conversions.state(self.conversion_key(path))[0] if self._conversions else 'missing'

    def request_conversion(self, master, path, callback, retry=False):
        """Im Tk-Thread anmelden/abholen; Worker erhält ausschließlich Dateiparameter.

        Ein Beobachter pro Host und Quellpfad. Hostabbau gibt Rückrufe frei und
        bricht Aufträge ohne weitere Beobachter ab. Ein neuer Dateistand ersetzt
        die alte Anmeldung, ohne deren Ergebnis in die neue Ansicht einzuspielen.
        """
        key = self.conversion_key(path)
        if key[0] is None:
            return 'failed'
        if self._conversions is None:
            self._conversions = glide_image_conversion.ConversionService()
        if self._conversions.state(key)[0] == 'ready' and not self.existing_conversion(path):
            self._conversions.forget(key)
        observer = (id(master), os.path.normcase(os.path.abspath(path)))
        previous = self._requests.get(observer)
        if previous and previous['key'] == key and not retry:
            return self._conversions.state(key)[0]
        if previous:
            previous['stop']()
        work = functools.partial(glide_image_conversion.convert_file, path, key[1], key[2], key[0])
        status = self._conversions.submit(key, work, retry=retry)
        if status == 'closed':
            return status
        record = {'key': key, 'binding': None, 'master': master, 'path': path, 'callback': callback, 'work': work}

        def stop(cancel=True):
            if self._requests.get(observer) is not record:
                return
            self._requests.pop(observer, None)
            self._observers[key] -= 1
            if self._observers[key] <= 0:
                del self._observers[key]
                if cancel:
                    self._conversions.cancel(key)
            try:
                if record['binding'] is not None:
                    master.unbind('<Destroy>', record['binding'])
            except tk.TclError:
                pass
            record['binding'] = None
            record.pop('stop', None)
            if not self._requests and self._poll_job is not None:
                try:
                    self._poll_root.after_cancel(self._poll_job)
                except tk.TclError:
                    pass
                self._poll_job = None

        def destroyed(event):
            if event.widget is master:
                stop()

        record['stop'] = stop
        self._requests[observer] = record
        self._observers[key] += 1
        try:
            record['binding'] = master.bind('<Destroy>', destroyed, add='+')
            self._poll_root = master._root()
            self._schedule_poll()
        except tk.TclError:
            stop()
        return status

    def _schedule_poll(self):
        if self._requests and self._poll_job is None:
            self._poll_job = self._poll_root.after(40, self._poll_conversions)

    def _poll_conversions(self):
        """Ein Tk-Timer, höchstens 64 Beobachter pro Schritt, unabhängig von der Bildzahl."""
        self._poll_job = None
        try:
            if self._conversions is not None and self._diagnostic is not None:
                kinds = tuple(kind for kind, count in self._conversions.diagnostics())
                new = [kind for kind in kinds if kind not in self._reported_conversion_errors]
                self._reported_conversion_errors = kinds
                for kind in new:
                    self._diagnostic(f'Bildvorschau: unerwarteter Workerfehler ({kind}). '
                                     'Dateipfad und Fehlerinhalt werden nicht protokolliert.')
            for observer, record in list(self._requests.items())[:64]:
                if self._requests.get(observer) is not record:
                    continue
                master, path, key = record['master'], record['path'], record['key']
                callback = record['callback']
                if not master.winfo_exists():
                    record['stop']()
                    continue
                if self.conversion_key(path) != key:
                    record['stop']()
                    if self.stamp(path) is not None:
                        self.request_conversion(master, path, callback)
                    else:
                        callback(None)
                    continue
                state, result = self._conversions.state(key)
                if state in ('missing', 'cancelled'):
                    state = self._conversions.submit(key, record['work'])
                if state in ('queued', 'running', 'busy'):
                    continue
                record['stop'](cancel=False)
                if state != 'closed':
                    callback(result)
        finally:
            self._schedule_poll()

    def cancel_requests(self, master):
        for observer, record in list(self._requests.items()):
            if observer[0] == id(master):
                record['stop']()

    def close(self):
        for record in list(self._requests.values()):
            record['stop']()
        if self._conversions:
            self._conversions.close()

    # --- Laden -----------------------------------------------------------
    def natural_size(self, master, path):
        """(Breite, Höhe) in Pixeln oder None, ohne Unterprozess."""
        stamp = self.stamp(path)
        if stamp is None:
            return None
        if stamp in self._sizes:
            return self._sizes[stamp]
        bild = self._load_raw(master, path, stamp)
        if bild is None:
            return None
        groesse = (int(bild.width()), int(bild.height()))
        self._delete(bild)
        if groesse[0] > 0 and groesse[1] > 0:
            self._sizes[stamp] = groesse
            return groesse
        return None

    def _load_raw(self, master, path, stamp):
        endung = extension(path)
        try:
            if endung in VECTOR:
                if not self.reads_svg(master):
                    return None
                return tk.PhotoImage(master=master, file=path, format="svg")
            if self.native_loader(master) and endung in NATIVE + CONVERTIBLE:
                return tk.Image("nsimage", master=master, cnf={"source": path, "as": "file"})
            if endung in NATIVE:
                return tk.PhotoImage(master=master, file=path)
            if endung in CONVERTIBLE:
                ziel = self.existing_conversion(path, stamp)
                if ziel:
                    return tk.PhotoImage(master=master, file=ziel)
        except (tk.TclError, OSError, MemoryError):
            return None
        return None

    @staticmethod
    def _delete(bild):
        try:
            bild.tk.call("image", "delete", bild.name)
        except (tk.TclError, AttributeError):
            pass

    def image(self, master, path, width=None, box=None, fit=None):
        """Tk-Bild in Anzeigegröße, oder None.

        `width` setzt die Breite (Seitenbilder), `box` begrenzt Breite und
        Höhe gleich (Galeriekacheln), `fit=(b, h)` getrennt (Pinnwandkarten).
        Das Seitenverhältnis bleibt immer erhalten; vergrößert wird nur mit
        `width`.
        """
        stamp = self.stamp(path)
        if stamp is None:
            return None
        natur = self.natural_size(master, path)
        if natur is None:
            return None
        nat_w, nat_h = natur
        if fit is not None:
            faktor = min(fit[0] / nat_w, fit[1] / nat_h, 1.0)
        elif box is not None:
            faktor = min(box / nat_w, box / nat_h, 1.0)
        elif width:
            faktor = max(1, int(width)) / nat_w
        else:
            faktor = 1.0
        ziel_w = max(1, round(nat_w * faktor))
        schluessel = (stamp, ziel_w, str(master))
        if schluessel in self._images:
            self._images.move_to_end(schluessel)
            return self._images[schluessel]
        bild = self._render(master, path, stamp, faktor, ziel_w, round(nat_h * faktor))
        if bild is None:
            return None
        self._images[schluessel] = bild
        while len(self._images) > self._limit:
            _alt, weg = self._images.popitem(last=False)
            # Tk löscht ein Bild, sobald seine Python-Hülle frei wird. Wer ein
            # Bild zeigt, hält deshalb selbst eine Referenz darauf.
            del weg
        return bild

    def _render(self, master, path, stamp, faktor, ziel_w, ziel_h):
        endung = extension(path)
        try:
            if endung in VECTOR:
                if not self.reads_svg(master):
                    return None
                return tk.PhotoImage(master=master, file=path, format=f"svg -scaletowidth {max(1, ziel_w)}")
            if self.native_loader(master) and endung in NATIVE + CONVERTIBLE:
                return tk.Image("nsimage", master=master,
                                cnf={"source": path, "as": "file", "width": max(1, ziel_w),
                                     "height": max(1, ziel_h)})
            quelle = path if endung in NATIVE else self.existing_conversion(path, stamp)
            if not quelle or not os.path.isfile(quelle):
                return None
            roh = tk.PhotoImage(master=master, file=quelle)
            # Eine gewandelte Vorschau ist schon verkleinert: Faktor neu bestimmen.
            faktor = ziel_w / max(1, roh.width())
            if abs(faktor - 1.0) < 0.02:
                return roh
            zoom, teiler = rational_factor(faktor)
            neu = tk.PhotoImage(master=master)
            neu.tk.call(neu.name, "copy", roh.name, "-zoom", zoom, zoom, "-subsample", teiler, teiler)
            self._delete(roh)
            return neu
        except (tk.TclError, OSError, MemoryError, ValueError):
            return None

    def forget(self, path=None):
        """Vergisst alle Bilder (oder die eines Pfads), etwa nach einem Designwechsel."""
        if path is None:
            self._images.clear()
            if self._conversions:
                self._conversions.forget()
            return
        stamp = self.stamp(path)
        for schluessel in [k for k in self._images if k[0] == stamp]:
            self._images.pop(schluessel, None)
        if self._conversions:
            self._conversions.forget(self.conversion_key(path))
