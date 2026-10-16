# Nachlauf 16.10.2026 – ACL-Restaurierung an Symlinks in der Windows-Paketprobe

Stand 16.10.2026 · Glide 3.43.0 unverändert (Apphash `379e97e3`, Datenformat 25) · Prüfwerkzeugnachlauf ohne neue App-Version · Windows 11 Pro, Python 3.14.7, künstliche Daten

## Anlass

Windows-Paketlauf nach [PR #29](https://github.com/n05a-design/glide-to-do/pull/29) ([Lauf 38927787712](https://github.com/n05a-design/glide-to-do/actions/runs/38927787712), Artefakt `paket-windows-belege`): Das Paket startet isoliert und besteht alle Funktionsproben; rot ist der Schritt „Isolierte Startprobe ohne externes Python“, weil die native ACL-Restaurierung an Reparse-Punkten mit WinError 5 scheitert – vier Symlinks unter `paket-runtime/quellen/python/Misc/mypy` und `python3.exe` im Tool-Cache, `acl_native_restaurierung_exitcodes` `[0, 0, 1, 0, 1]`. Der Weg kam mit PR #26 (Vorbereitung Paket 8) hinzu.

## Ursache

Lokal nachgestellt mit künstlichem CPython-Quellbaum (relative Datei-Symlinks) und Tool-Cache-Ordner (absoluter `python3.exe`-Symlink) im eigenen Scratch-Ordner:

1. `windows_acl.py` öffnete den Link nur mit `WRITE_DAC` und setzte die DACL mit `SetSecurityInfo`. Das liest beim Setzen die vorhandene Sicherheitsbeschreibung über dasselbe Handle und scheitert ohne `READ_CONTROL` mit WinError 5 – geschützt, ungeschützt und nur DACL gleichermaßen, auch ganz ohne vorherige Sperre. Genau die drei Reparse-Punkte des Nachbaus scheiterten, alle übrigen Einträge nicht.
2. `icacls /save` und `/restore` ohne `/L` behandeln einen Symlink über sein Ziel: Gesichert wird die DACL des Ziels, `/restore` schreibt durch den Link hindurch. Sperre (`/deny (OI)(CI)`) und Entsperrung erreichen dagegen den Link selbst und berechnen seine geerbten ACEs neu (gemessen: aus `(I)(OI)(CI)` wird `(I)`). Gesichertes und verändertes Objekt waren also verschieden; die Nachprüfung sah den Link selbst nie. Der Codekommentar nahm das Gegenteil an.

## Korrektur

- `packaging/paket/windows_acl.py`: Reparse-Punkte werden weiter mit `WRITE_DAC` ohne Zielverfolgung geöffnet; die gesicherte DACL wird per `SetKernelObjectSecurity` wörtlich gesetzt (braucht kein Leserecht) – geerbte ACEs und P-Schutz bleiben exakt, das Ziel unberührt. Normale Dateien (`SetFileSecurityW`) und geschützte Originale (`SetNamedSecurityInfoW`) behalten ihren Weg.
- `packaging/paket/pruefe_start_windows.py`: Sichern, Restaurieren und Nachprüfen mit `icacls … /L`. Gilt für den Paketjob und den Zugangs-Paketprototyp, die denselben Prüfer aufrufen.
- `.github/workflows/python-app.yml`: Der Windows-Paketjob führt vor der Startprobe `test_paket_windows_isolation.py` auf dem Hosted-Runner aus.

## Prüfung

| Prüfung | Ergebnis |
|---|---|
| `tests/tools/test_paket_windows_isolation.py` | 26/26 grün (vorher 24). Neu: nativer Link-Rundlauf (Link und Ziel mit verschiedenen Regeln, Link gestört, Restaurierung, Vergleich mit `/L`, Ziel unverändert) und Vertrag „`/L` in allen drei icacls-Aufrufen“ |
| Rote Gegenprobe gegen `main` (`8b59a8b`) | beide neuen Fälle rot: WinError 5 am Link, drei Aufrufe ohne `/L` |
| Nachbau des CI-Ablaufs (Sichern, Sperre, Entsperren, `/restore`, native Restaurierung, Nachprüfung) | vorher drei Einträge WinError 5, nachher keiner; Zugriffsregeln beider Quellen gleich, nur der AI-Modellmarker weicht wie vorgesehen ab |
| CI-Grundstufe Windows | bestanden, Exit 0: Syntax (307 Quelldateien), Versionen 3.43.0/Format 25, 189 Dokumentlinks, 152 Werkzeugtests, 711 Units auch ohne Systemzeitzonen, fünf Analysen, Startprobe, Lieferstand bytegleich, Datenschutz, Ablagegröße, Synchronisation ([Protokoll](grundstufe.json)); gelaufen mit zusätzlichem `READ_CONTROL` am Linkhandle, nach dessen Wegfall Werkzeugtests (152), Nachbau, Stand-, Link-, Synchronisations- und Datenschutzprüfung erneut grün |
| App und Lieferstand | `src/glide`, `07_Python-Versionen` und `05_Probelisten_Testdaten` unverändert; 67 Code-/146 Ressourcendateien bytegleich |

## Grenzen

- Lokal als Benutzer ohne Adminrechte: `icacls /restore` braucht SeRestorePrivilege und meldet hier 1300; auf dem erhöhten Hosted-Runner nicht. Die native Restaurierung danach ist davon unabhängig und wurde vollständig geprüft.
- Erst der Windows-Paketlauf auf GitHub (`windows-2025`) belegt den grünen Schritt; er steht nach dem Push aus.
- Gesperrt wurde nur der eigene Scratch-Ordner; keine Inhaberinstallation berührt.
- Unverändert offen: unter Linux `test_tempo330`, `test_planen33313`, `test_oberflaeche33321` und „Kalibrierte Erwartungen“ (Paket 8), Mac-Vollprüfung und Mac-Bundle, Menschenabnahme.
