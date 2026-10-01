# Paketierung Glide

Stand 24.09.2026 · Glide 3.29.0 · Aufgabenformat 19 · Einstellungen 2 · Vorlagen 2

Der aktuelle Stand ist eine geprüfte Python-Anwendung mit Ressourcen.
Ein Installer, eine Signatur oder eine Store-Abnahme wird hier nicht behauptet.

Ein Paket muss `src/glide/app.pyw`, seit 3.29.0 die Module `src/glide/drawing.py` und
`src/glide/drawing_image.py` sowie den vollständigen Ordner `src/glide/resources` (Schriften und Vorlagen) einschließlich
Lizenz enthalten. Die Bedienprobe `drawing_prototype.pyw` gehört nicht ins Paket. Private Registrierung verlangt keine systemweite Installation
der Schrift. Daten dürfen nicht in den Installationsordner geschrieben werden.

Vor der ersten Veröffentlichung: Anbieteridentitäten, Zielarchitektur,
Betriebssystemminimum, Signierung und Upgrade-/Deinstallationsverhalten anhand
eines echten Pakets festlegen und prüfen. Verbindliche Statusliste:
[Releasecheckliste](../docs/10_RELEASE_CHECKLIST.md).
