# Paketierung Glide 3.9.0

Der aktuelle Stand ist eine geprüfte Python-Anwendung mit Ressourcen.
Ein Installer, eine Signatur oder eine Store-Abnahme wird hier nicht behauptet.

Ein Paket muss `src/glide/app.pyw` und den vollständigen Ordner `src/glide/resources` (Schriften und Vorlagen) einschließlich
Lizenz enthalten. Private Registrierung verlangt keine systemweite Installation
der Schrift. Daten dürfen nicht in den Installationsordner geschrieben werden.

Vor der ersten Veröffentlichung: Anbieteridentitäten, Zielarchitektur,
Betriebssystemminimum, Signierung und Upgrade-/Deinstallationsverhalten anhand
eines echten Pakets festlegen und prüfen. Verbindliche Statusliste:
[Releasecheckliste](../docs/10_RELEASE_CHECKLIST.md).
