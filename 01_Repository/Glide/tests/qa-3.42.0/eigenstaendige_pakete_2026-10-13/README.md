# Eigenständige Pakete 3.42.0

Prüfstand 13.10.2026, künstliche Daten; Aufgabenformat 25 unverändert.

- [Mac-Bau](mac_bau.json): Python 3.14.5/Tcl-Tk 9.0.3, PyInstaller 6.22.3, 64 kompilierte Codeobjekte, native arm64-Bibliotheken und Lizenzzuordnung geprüft; Ad-hoc-Signatur grün.
- [Isolierter Mac-Start](mac_start.json): externe Python-Laufzeit, Bauumgebung und Projektquellen ausschließlich im Kindprozess gesperrt. Anlegen, Abhaken, Undo, sechs Ansichten, Dateilesen, App-Sicherungs-Rundlauf, Logo, Schriften, Drag-and-drop, Ressourcen/Lizenzen und interne Anbieter grün. Systeminstallationen unverändert.
- [Pflichtsuite](bauquellen_mac_start.json) prüft reale Module, Ressourcen und Pins beider Zielplattformen und den Mac-Startbericht.
- [Gegenproben](gegenproben.json): 3.41.0 an fehlenden Bauwegen und im tatsächlichen isolierten Altbundle-Start passend rot. Vor jedem Import temporärer Datenordner, auch beim Altbundle.

[Eingefrorene Mac-Vollprüfung](mac_voll.json) Exit 0: 107 ausgeführt/zwei übersprungen, 90 Integrationssuiten/638 Units. [1.054 Dateien unverändert](mac_frozen_unveraendert.json). [Lieferabgleich im Kandidaten](lieferabgleich_vorlauf.json): 63 Code-/146 Ressourcen-/sechs Showcase-Dateien bytegleich; 330 Paketdateien und 29 Symlinks gleich dem nativen Bau, Rückkopiesignatur grün. Native Linux-/Windows-Matrix, Windows-Paketbau und Inhaberlieferabschluss stehen noch aus. Keine öffentliche Releasefreigabe; Menschen-/DPI-/Readerabnahme getrennt offen. Rohprotokolle und Pakete bleiben außerhalb des öffentlichen Repositorys.


Die erste strenge CI-Grundstufe fand nach der Bundlerückkopie zwei Pflegefehler: der erzeugte Bundle-Lizenztext wurde als aktives Dokument geprüft; zwei Werkzeugtests enthielten künstliche Benutzerpfade. [Roter Vorlauf](ci_vorlauf.json). Die Dokumentinventur grenzt nun ausschließlich die erzeugten `build/`-Pakete ab (Quell-Paketdokumente bleiben pflichtig), die Testpfade liegen in neutralen QA-/Inhaberordnern. 14 Stand-/44 Paket-Werkzeugtests grün. App, Bootstrap, Bauwerkzeuge und fertiges Mac-Paket bleiben bytegleich; [Frischer eingefrorener Volllauf](mac_final_voll.json) Exit 0, 107/2; [alle 1.060 Dateien unverändert](mac_final_quellstand.json). [Erneute strenge CI](ci_kandidat.json) Exit 0 mit dem tatsächlichen eigenständigen Bundle; Datenschutz, Stand, Lieferstand und Werkzeugtests grün. Der lokale SSL-Hinweis beim Vendor-Originalabruf wird in der nativen Grundstufe erneut geprüft. Native Linux-/Windows-Abnahme und Inhaberlieferabschluss bleiben offen.
