@echo off
rem Glide – Windows-Vollpruefung in der Windows-Sandbox per Doppelklick: eigene Sitzung, Fenster auf dem zweiten Bildschirm.
rem Details und Optionen: windows_sandbox.py (zum Beispiel --bildschirm 1, --speicher 8192, --schliessen).
cd /d "%~dp0..\.."
py -3.14 -B tests\tools\windows_sandbox.py --warten %*
echo.
pause
