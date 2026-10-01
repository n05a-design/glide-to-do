import pathlib

p = pathlib.Path('src/glide/app.pyw')
text = p.read_text(encoding='utf-8')

replacements = {
    '"Punkte anheften …"': '"Anheften"',
    '"Verbinden …"': '"Verbinden"',
    '"Kartengröße …"': '"Kartengröße"',
    '"Drucken und PDF …"': '"Drucken und PDF"',
    '"   Punkte anheften …"': '"   Anheften"',
    '"   Alle Aktionen …"': '"   Aktionen"',
    '"Reiter …"': '"Reiter"',
    '"Weitere Aktionen …"': '"Aktionen"'
}

for k, v in replacements.items():
    text = text.replace(k, v)

p.write_text(text, encoding='utf-8')
print("Ersetzungen abgeschlossen")
