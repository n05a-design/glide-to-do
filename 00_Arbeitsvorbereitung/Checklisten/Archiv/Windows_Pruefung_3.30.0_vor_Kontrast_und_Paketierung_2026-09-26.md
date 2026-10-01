# Windows-Prüfung – Glide 3.30.0

Stand 26.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · noch nicht ausgeführt

Seit 3.29 fehlt ein Gesamtlauf unter Windows. Mit diesem Paket startest du die
automatische Vollprüfung selbst. Es ist dieselbe Prüfung, die auf dem
Entwicklungs-Mac läuft. Die echten Daten unter `%APPDATA%\Glide` bleiben dabei
unberührt, weil jede Suite in einem eigenen temporären Datenordner arbeitet.

## Vorbereitung (einmalig)

1. **Python 3.12 oder neuer** von [python.org](https://www.python.org/downloads/windows/)
   installieren, mit der Option „tcl/tk and IDLE“ (Standard) und dem
   Python-Starter `py`.
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

Der Lauf dauert etwa 15 bis 25 Minuten. Dabei öffnen und schließen sich
Glide-Fenster. Während des Laufs bitte nicht mit der Maus eingreifen und keine
weiteren rechenintensiven Programme starten: Einige Oberflächentests messen
Layouts und reagieren auf Last.

## Ergebnis

- Am Ende stehen **Exitcode** und Protokollordner, zum Beispiel
  `tests\qa-3.30.0\windows_2026-09-27_1030`.
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

## Danach von Hand (Auszug aus der Prüfliste 3.30)

- [ ] Glide 3.30 starten (`07_Python-Versionen`), Design „Pixel“ wählen:
      Seitentitel und Kachelköpfe in Pixelify Sans, Umlaute und ß korrekt.
- [ ] 100, 150 und 200 % Anzeigeskalierung sowie zwei Monitore.
- [ ] „Präsentation als PDF …“ und „Drucken und PDF …“ im Browser als PDF
      sichern.
- [ ] Bildschirmleser (NVDA): Seitenleiste, Suche, Detailbereich.

Die vollständige Liste steht in der [Prüfliste 3.30](Manuelle_Pruefung_3.30.0.md).
