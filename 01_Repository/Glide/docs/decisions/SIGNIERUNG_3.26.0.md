# Signierung und Notarisierung von Glide 3.26.0

Stand 21.09.2026 · App-Version 3.26.0 · Vorbereitungsanleitung, keine Signierungsbestätigung

Herausgeber ist Tim von Trostorff. Zertifikate, Zugangsdaten und dauerhafte Plattformkennungen werden nicht erfunden und nicht im Repository gespeichert. Die Python-Quelldatei und lokale QA-Läufe belegen keinen signierten Installer.

## Windows

1. Den geprüften Build und den Installer reproduzierbar erzeugen; endgültige Versionsinformationen kontrollieren.
2. SignTool aus dem Windows SDK verwenden. Das zugelassene Code-Signing-Zertifikat über den Zertifikatsspeicher oder den vorgesehenen Hardware-/Dienstanbieter auswählen.
3. Binärdateien und anschließend den fertigen Installer mit SHA-256 signieren; einen RFC-3161-Zeitstempel des Zertifikatanbieters mit SHA-256 hinzufügen. Konkrete Zertifikatauswahl und Zeitstempeladresse gehören in die lokale Build-Konfiguration.
4. `signtool verify /pa /v <Datei>` gegen jedes ausgelieferte Artefakt ausführen. Signatur, Herausgeber, Zeitstempel und SHA-256-Prüfsumme im Release-Protokoll festhalten.
5. Installation und Start auf einem sauberen Windows-Testsystem prüfen. Ein erfolgreich signiertes Paket garantiert keine bestimmte SmartScreen-Einstufung.

Quellen: [Microsoft SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool), [Authenticode-Zeitstempel](https://learn.microsoft.com/en-us/windows/win32/seccrypto/time-stamping-authenticode-signatures).

## macOS

1. Auf einem unterstützten Mac mit passender Python/Tk-Laufzeit ein natives App-Bundle erzeugen und testen. Ein Windows-Test ist kein macOS-Nachweis.
2. Bundle-Identifier, Zielarchitektur und Mindestversion verbindlich festlegen. Mit Developer ID Application und den für das konkrete Bundle erforderlichen Optionen signieren; enthaltene ausführbare Komponenten einbeziehen.
3. Das Distributionsarchiv mit `xcrun notarytool submit <Archiv> --keychain-profile <Profil> --wait` einreichen. Zugangsdaten verbleiben im lokalen Schlüsselbundprofil.
4. Nur bei Status `Accepted` fortfahren, das Ticket mit `xcrun stapler staple <App-oder-Paket>` anheften und mit `xcrun stapler validate <App-oder-Paket>` prüfen.
5. Gatekeeper-Prüfung, Installation, Start, Datenablage und Update auf einem separaten Zielsystem dokumentieren.

Quellen: [Apple Notarisierung](https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution), [Notarisierungsablauf](https://developer.apple.com/documentation/security/customizing-the-notarization-workflow).

## Freigabestatus

Keine echten Signaturen oder Notarisierungen wurden im Rahmen der Quellcode-Nachbesserung vorgenommen. Zertifikate, bestätigte Paketkennungen und macOS-Buildnachweis sind externe Voraussetzungen der Auslieferung.
