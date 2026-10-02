# Windows-Prüfung – Glide (fortgeschriebene Prüfliste)

Stand 02.10.2026 · Glide 3.33.6 · Aufgabenformat 20 · noch nicht ausgeführt

Dateiname und Linkziel bleiben stabil. Maßgeblich ist `VERSION`, aus der das Startskript den QA-Ordner bildet. Neu enthalten sind Klapp-, Drag-/Performance- und Bibliothekskartenkontrolle. [Arbeitsrichtung](../../01_Repository/Glide/docs/ARBEITSRICHTUNG.md).


Für den aktuellen Entwicklungsstand ist noch kein Windows-Gesamtlauf nachgewiesen. Mit diesem Paket startest du die
automatische Vollprüfung selbst. Es ist dieselbe Prüfung, die auf dem
Entwicklungs-Mac läuft. Die echten Daten unter `%APPDATA%\Glide` bleiben dabei
unberührt, weil jede Suite in einem eigenen temporären Datenordner arbeitet.

## Vorbereitung (einmalig)

1. **Python 3.14** von [python.org](https://www.python.org/downloads/windows/)
   installieren, mit der Option „tcl/tk and IDLE“ (Standard) und dem
   Python-Starter `py`. Die verwendete Python-/Tk-Kombination ist vor Ort zu prüfen; Grundlage ist Python 3.14/Tk 9 (E-03). Am 28.09.2026 war auf dem PC nur Python 3.13 mit
   Tk 8.6 installiert; damit prüft der Lauf nur den Rückfallweg (Logo als
   Fläche, keine Systemmitteilung, keine SVG-Vorschau). Beide Fassungen
   dürfen nebeneinander installiert sein; `py -3.14` wählt die neue.
2. **OneDrive:** den Ordner `Glide ToDo` im Explorer per Rechtsklick auf
   „Immer auf diesem Gerät behalten“ stellen und warten, bis alle Dateien
   heruntergeladen sind. Nur online verfügbare Platzhalter ließen den Lauf 3.28
   scheitern; das Skript bricht in diesem Fall mit einem Hinweis ab.
3. Glide vorher schließen.

## Prüfung starten

- **Doppelklick:**
  `01_Repository\Glide\tests\tools\windows_vollpruefung.cmd`;
- **oder in PowerShell** aus `01_Repository\Glide`:
  `powershell -NoProfile -ExecutionPolicy Bypass -File tests\tools\windows_vollpruefung.ps1`.

Der Umfang ist derzeit 58 Suiten und fünf Analysen; die Dauer hängt vom PC ab. Dabei öffnen und schließen sich
Glide-Fenster. Während des Laufs bitte nicht mit der Maus eingreifen und keine
weiteren rechenintensiven Programme starten: Einige Oberflächentests messen
Layouts und reagieren auf Last.

## Ergebnis

- Am Ende stehen **Exitcode** und Protokollordner, zum Beispiel
  `tests\qa-3.32.3\windows_2026-10-01_1030`.
  - `0` heißt: alle automatischen Schritte bestanden;
  - `1` heißt: mindestens ein Schritt gescheitert – die Logdatei im Ordner
    nennt ihn;
  - `3` oder `4` heißt: fehlendes Python/Tk bzw. OneDrive-Platzhalter.
- Unter Windows legt die Prüfung zusätzlich eine Aufnahme des Hauptfensters
  ab (`release_hell.png`, Releaseplanung im hellen Design). Bitte auf Schärfe
  und abgeschnittene Texte ansehen. Das Design „Pixel“ prüfst du von Hand (unten).
- Den Protokollordner einfach liegen lassen – er liegt im geteilten Ordner.
  Der nächste Agent überträgt das Ergebnis in den
  [QA-Bericht](../../01_Repository/Glide/docs/07_QA_BERICHT.md) und den
  [QA-Verlauf](../../01_Repository/Glide/tests/qa-verlauf.md).

## Danach von Hand

Die Schritte nach dem Lauf stehen in Teil B der
[Fortgeschriebenen Prüfliste](Manuelle_Pruefung_3.30.0.md#b-windows-pc-nach-der-vollprüfung):
echter Windows-Bestand (B2), Design „Pixel“, Skalierung, Logo und Lupe,
Startmenü-Verknüpfung, Vorschauen, Ziehen aus dem Explorer,
Systemmitteilung, Druck und Beenden. Bis zum 29.09.2026 stand hier ein
Auszug davon – zwei Listen für dieselben Schritte.

## Laufzeit vor Ort abgleichen

`windows_vollpruefung.ps1` wählt `py -3`, sonst `python`; es kann deshalb bei mehreren Installationen eine andere Python-Version auswählen. Die Ausgabe unter „Tk“ liest derzeit die Tcl-Version, nicht `package present Tk`. Die tatsächliche Tk-Version separat prüfen, zum Beispiel mit `py -3.14 -c "import tkinter as t; r=t.Tk(); print(r.tk.call('package', 'present', 'Tk')); r.destroy()"`. Die Probe öffnet kurz ein natives Tk-Fenster und greift nicht auf Glide-Daten zu.

Falls der Starter eine andere Laufzeit wählt, die Vollprüfung aus dem Repository ausdrücklich mit `py -3.14 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-<Version>/windows_manuell --timeout 900` starten (`<Version>` durch VERSION ersetzen). Ergebnis und tatsächlich verwendete Python-/Tk-Version dokumentieren; kein Windows-Nachweis wird aus dem Mac-Lauf abgeleitet.
