"""Glättung, exakte Kleinbilder und Symbolabdeckung über echte UI-Einstiege.

--app und --fall erlauben getrennte Gegenproben gegen die Vorversion.
Ausschließlich künstliche Daten; native Sicht-/DPI-Abnahme bleibt getrennt.
"""
import argparse
import base64
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import struct
import sys
import tempfile
from types import SimpleNamespace
import zlib

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--app",type=Path,default=Path(__file__).resolve().parents[2]/"src/glide/app.pyw")
parser.add_argument("--fall",choices=("logo","icons","symbole","alle"),default="alle")
args=parser.parse_args()
sys.path.insert(0,str(args.app.resolve().parent))


def rgba(photo):
    encoded=photo.tk.call(photo.name,"data","-format","png")
    png=encoded if isinstance(encoded,bytes) else base64.b64decode(encoded)
    width,height,depth,kind=struct.unpack(">IIBB",png[16:26])
    assert depth==8 and kind in (2,6),(depth,kind)
    channels=4 if kind==6 else 3
    pos,compressed=8,b""
    while pos<len(png):
        count=struct.unpack_from(">I",png,pos)[0]
        if png[pos+4:pos+8]==b"IDAT":compressed+=png[pos+8:pos+8+count]
        pos+=count+12
    raw=zlib.decompress(compressed)
    rows=[];previous=bytearray(width*channels)
    def paeth(a,b,c):
        p=a+b-c;distances=(abs(p-a),abs(p-b),abs(p-c))
        return (a,b,c)[distances.index(min(distances))]
    for y in range(height):
        offset=y*(width*channels+1);filter=raw[offset]
        row=bytearray(raw[offset+1:offset+1+width*channels])
        for i in range(len(row)):
            left=row[i-channels] if i>=channels else 0
            above=previous[i]
            upper_left=previous[i-channels] if i>=channels else 0
            predictors=(0,left,above,(left+above)//2,paeth(left,above,upper_left))
            row[i]=(row[i]+predictors[filter])&255
        rows.extend(tuple(row[i:i+channels]) if channels==4 else (*row[i:i+channels],255)
                    for i in range(0,len(row),channels))
        previous=row
    return width,height,rows


with tempfile.TemporaryDirectory(prefix="glide-logo3370-") as data:
    os.environ["GLIDE_DATA_DIR"]=data;os.environ["GLIDE_TEST_MODE"]="1"
    loader=importlib.machinery.SourceFileLoader("glide_logo3370_test",str(args.app))
    mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))
    sys.modules[loader.name]=mod;loader.exec_module(mod)
    root=mod.tk.Tk();root.geometry("1280x800+20+20")
    errors=[];root.report_callback_exception=lambda *e:errors.append(repr(e[1]))
    app=mod.ListApp(root);app.show_info=app.show_warning=app.show_error=lambda *a,**k:None
    logo=mod.glide_logo
    def settle():
        for _ in range(3):root.update_idletasks();root.update()
    try:
        settle()
        if args.fall in ("logo","alle"):
            native=logo.has_svg;logo.has_svg=lambda master:False
            try:
                for height in (16,32,54,108):
                    for color in ("#0185E1","#AB12CD"):
                        photo=logo.logo_photo(root,height,color)
                        assert photo is not None,"Tk-8.6-Logo fehlt als geglättetes Bild"
                        w,h,pixels=rgba(photo)
                        assert h==height and w==photo.width()
                        alphas={p[3] for p in pixels}
                        assert 0 in alphas and 255 in alphas and len(alphas)>=16,(height,alphas)
                        expected=tuple(int(color[i:i+2],16) for i in (1,3,5))
                        assert all(p[:3]==expected for p in pixels if p[3]==255)
                        # Geometrische Mitte des freigegebenen Innenraums:
                        # ceil(Bildbreite) enthält einen transparenten Restpixel
                        # und darf die Abtastposition nicht verschieben.
                        name = logo.LOGO_SMALL_FILE if height in (16, 32) else logo.LOGO_FILE
                        hole = logo.outline(name, schritte=32)[1]
                        cx = (min(x for x, y in hole) + max(x for x, y in hole)) / 2
                        cy = (min(y for x, y in hole) + max(y for x, y in hole)) / 2
                        bx, by, _, bh = logo.bounding_box(name)
                        px, py = int((cx - bx) * h / bh), int((cy - by) * h / bh)
                        inside = pixels[py * w + px][3]
                        assert inside == 0, (height, inside)
                canvas=mod.tk.Canvas(root)
                app.draw_logo(canvas,54,"#AB12CD")
                assert canvas.type(canvas.find_withtag("logo")[0])=="image"
                assert int(canvas.cget("width"))==canvas._logo_image.width()
                canvas.destroy()
            finally:logo.has_svg=native
            print("OK Logo: Alpha-Zwischentöne, Farbe, Innenraum, echte Zeichenfläche")
        if args.fall in ("icons","alle"):
            native=logo.has_svg;logo.has_svg=lambda master:False
            original_sys=logo.sys;original_photo=logo.tk.PhotoImage;loaded=[]
            def photo(*a,**kw):
                if kw.get("file"):loaded.append(Path(kw["file"]))
                return original_photo(*a,**kw)
            try:
                logo.tk.PhotoImage=photo
                for platform in ("darwin","win32","linux"):
                    logo.sys=SimpleNamespace(platform=platform)
                    images=logo.icon_photos(root,(16,32,64,256))
                    assert [(p.width(),p.height()) for p in images]==[(n,n) for n in (16,32,64,256)],"App-Symbole nicht exakt in Zielgröße"
                    assert [p.name for p in loaded[-4:]]==[f"glide-app-icon{'-macos' if platform=='darwin' else ''}-{n}.png" for n in (16,32,64,256)],"Großes PNG statt Zielgrößen geladen"
                    assert all(p.stat().st_size<128*1024 for p in loaded[-4:])
            finally:
                logo.has_svg=native;logo.sys=original_sys;logo.tk.PhotoImage=original_photo
            if logo.has_svg(root):
                images=logo.icon_photos(root,(16,32,64,256))
                assert [(p.width(),p.height()) for p in images]==[(n,n) for n in (16,32,64,256)]
            print("OK App-Symbole: exakte Zielgrößen, direkte Kleinbild-Dateien, natives SVG")
        if args.fall in ("symbole","alle"):
            assert set(app.ICONS)==set(type(app).ICONS)
            for weight in ("normal","bold"):
                font=mod.tkfont.Font(root=root,family=app.ui_font_family(),size=app.ui_font_size(1),weight=weight)
                family=str(font.actual("family")).casefold()
                for name,text in app.ICONS.items():
                    assert font.measure(text)>0,name
                    assert all(str(root.tk.call("font","actual",font.name,"-family",char)).casefold()==family for char in text),("Ersatzschrift",name,text)
            assert app.search_button.text==app.ICONS["search"]
            app.search_button.command();settle()
            assert app._quick_open is not None and app._quick_open["panel"].winfo_ismapped()
            app.close_quick_open();settle()
            assert app._quick_open is None
            app.settings["ui_font_size"]="gross";app.apply_ui_font();app.apply_theme();settle()
            assert app.search_button.text==app.ICONS["search"]
            for name in ("search_button", "settings_button", "print_button", "sidebar_toggle_button"):
                button = getattr(app, name)
                assert button.text_width() + button.TEXT_INSET <= int(button.cget("width")), name
            app.set_design("pixel")
            app.set_home_view();settle()
            pixel_icons = [w for w in app.iter_descendants(app.home_content) if getattr(w, "_glide_symbol", None)]
            assert pixel_icons, "Pixel-Kachelköpfe ohne separat gesetzte Symbole"
            for icon in pixel_icons:
                font = mod.tkfont.Font(root=root, font=icon.cget("font"))
                assert all(str(root.tk.call("font", "actual", font.name, "-family", char)).casefold()
                           == str(font.actual("family")).casefold() for char in icon._glide_symbol)
            print("OK Symbole: vollständige Tabelle, beide Schriftschnitte, echter Sucheinstieg, große Schrift, Pixel-Kopf")
        assert not errors,errors
    finally:
        app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
