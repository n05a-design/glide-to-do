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
- **Linux:** nur PNG, GIF und SVG; andere Formate zeigen die Endung.

Alle geladenen Bilder bleiben in einem kleinen Zwischenspeicher je
Anzeigegröße, damit Galerie und Seiten beim Scrollen und Neuzeichnen nicht
erneut dekodieren. Nur Standardbibliothek und tkinter.
"""

import collections
import hashlib
import os
import subprocess
import sys
import tkinter as tk

NATIVE = (".png", ".gif", ".ppm", ".pgm")
VECTOR = (".svg",)
CONVERTIBLE = (".jpg", ".jpeg", ".heic", ".heif", ".webp", ".tif", ".tiff", ".bmp")
IMAGE_EXTENSIONS = NATIVE + VECTOR + CONVERTIBLE
FILE_PATTERN = " ".join("*" + endung for endung in IMAGE_EXTENSIONS)
MAX_CONVERTED = 1600


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


def windows_convert_command(quelle, ziel, max_kante=MAX_CONVERTED):
    """PowerShell-Aufruf, der über WIC in ein PNG mit höchstens `max_kante` Pixeln wandelt."""
    def pfad(wert):
        return "'" + str(wert).replace("'", "''") + "'"
    skript = (
        "$ErrorActionPreference='Stop';"
        "Add-Type -AssemblyName PresentationCore;"
        f"$s=[System.IO.File]::OpenRead({pfad(quelle)});"
        "try{"
        "$d=[System.Windows.Media.Imaging.BitmapDecoder]::Create($s,"
        "[System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat,"
        "[System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad);"
        "$f=$d.Frames[0];"
        f"$k=[Math]::Min(1.0,{int(max_kante)}/[Math]::Max($f.PixelWidth,$f.PixelHeight));"
        "$b=New-Object System.Windows.Media.Imaging.TransformedBitmap($f,"
        "(New-Object System.Windows.Media.ScaleTransform($k,$k)));"
        "$e=New-Object System.Windows.Media.Imaging.PngBitmapEncoder;"
        "$e.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($b));"
        f"$o=[System.IO.File]::Create({pfad(ziel)});"
        "try{$e.Save($o)}finally{$o.Close()}"
        "}finally{$s.Close()}"
    )
    return ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", skript]


class PreviewCache:
    """Lädt Bilder in Anzeigegröße und merkt sich die letzten `limit` Stück."""

    def __init__(self, cache_dir=None, limit=160):
        self._cache_dir = cache_dir
        self._limit = limit
        self._images = collections.OrderedDict()
        self._sizes = {}
        self._nsimage = None
        self._svg = None

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

    def converted_path(self, path, stamp=None):
        stamp = stamp or self.stamp(path)
        if stamp is None:
            return None
        schluessel = hashlib.sha1(repr(stamp).encode("utf-8")).hexdigest()
        return os.path.join(self.cache_dir(), f"{schluessel}.png")

    def needs_conversion(self, master, path):
        """True, wenn erst ein Unterprozess eine Vorschau anlegen muss."""
        endung = extension(path)
        if endung not in CONVERTIBLE or self.uses_nsimage(master):
            return False
        ziel = self.converted_path(path)
        return bool(ziel) and not os.path.isfile(ziel) and self.can_convert()

    @staticmethod
    def can_convert():
        return sys.platform == "darwin" or os.name == "nt"

    def convert(self, path):
        """Legt die PNG-Vorschau an (blockierend, mit Zeitlimit). Liefert den Pfad oder None."""
        ziel = self.converted_path(path)
        if not ziel:
            return None
        if os.path.isfile(ziel):
            return ziel
        try:
            os.makedirs(os.path.dirname(ziel), exist_ok=True)
            if sys.platform == "darwin":
                befehl = ["sips", "-s", "format", "png", "-Z", str(MAX_CONVERTED), path, "--out", ziel]
                optionen = {}
            elif os.name == "nt":
                befehl = windows_convert_command(path, ziel)
                optionen = {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}
            else:
                return None
            subprocess.run(befehl, capture_output=True, timeout=45, check=False, **optionen)
        except (OSError, subprocess.SubprocessError, ValueError):
            return None
        return ziel if os.path.isfile(ziel) and os.path.getsize(ziel) > 0 else None

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
            if self.uses_nsimage(master) and endung in NATIVE + CONVERTIBLE:
                return tk.Image("nsimage", master=master, cnf={"source": path, "as": "file"})
            if endung in NATIVE:
                return tk.PhotoImage(master=master, file=path)
            if endung in CONVERTIBLE:
                ziel = self.converted_path(path, stamp)
                if ziel and os.path.isfile(ziel):
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
            if self.uses_nsimage(master) and endung in NATIVE + CONVERTIBLE:
                return tk.Image("nsimage", master=master,
                                cnf={"source": path, "as": "file", "width": max(1, ziel_w),
                                     "height": max(1, ziel_h)})
            quelle = path if endung in NATIVE else self.converted_path(path, stamp)
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
            return
        stamp = self.stamp(path)
        for schluessel in [k for k in self._images if k[0] == stamp]:
            self._images.pop(schluessel, None)
