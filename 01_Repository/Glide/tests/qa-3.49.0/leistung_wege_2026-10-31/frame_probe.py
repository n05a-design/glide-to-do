import sys, time, tkinter as tk
groesse = sys.argv[1] if len(sys.argv) > 1 else '1280x800'
r = tk.Tk(); r.geometry(groesse + '+20+20'); f = tk.Frame(r, bg='#f4f1ea'); f.pack(fill='both', expand=True)
for i in range(30): tk.Label(f, text=f'Zeile {i} mit etwas Text', bg='#f4f1ea').pack(anchor='w')
for _ in range(5): r.update()
b = tk.Label(f, text='Erledigt', bg='white', fg='green', padx=16, pady=8)
zeiten = []
for s in range(14):
    t = time.perf_counter(); b.place(relx=0.5, rely=1.0, y=-(14 + s*3), anchor='s'); b.lift(); r.update(); zeiten.append((time.perf_counter()-t)*1000)
b.destroy(); t = time.perf_counter(); r.update(); ende = (time.perf_counter()-t)*1000
import statistics
print(f"Tk {r.tk.call('info','patchlevel')} Fenster {groesse}: je Bild Median {statistics.median(zeiten):.1f} ms, max {max(zeiten):.1f} ms, Summe {sum(zeiten):.0f} ms")
r.destroy()
