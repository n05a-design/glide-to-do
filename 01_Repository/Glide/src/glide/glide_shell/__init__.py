# SPDX-License-Identifier: MPL-2.0
"""Glide Shell – wiederverwendbares Tk-Fundament ohne Glide-Bezug (D86, D95, D98).

Die Shell bündelt anwendungsneutrale Desktop-Bausteine für Tk-Anwendungen.
Jedes Modul importiert ausschließlich die Standardbibliothek, `tkinter` und
andere Module dieses Pakets; Werte, Texte und Farben liefert der Host als
Argumente oder Rückrufe (Abhängigkeitsrichtung Host → Shell → Tk).
Meldungen für Entwickler (Ausnahmen, Protokolltexte) sind Englisch (D96).

Bausteine:
- `modal_session`: Dialogfabrik `create_dialog`, modaler Warteweg mit Griff,
  Freigabe und Fokusrückgabe (`run_modal`, `wait_modal`, `modal_over`).
- `window_lifetime`: Zeitgeberbesitz je Widget (`AfterScope`, `scope_for`).
- `custom_controls`: thementaugliche Canvas-Bedienelemente.
- `desktop_adapter`: Menüleiste, Tastaturkürzel und Betriebssystemaktionen.
- `motion`: kurze, unterbrechbare Übergänge mit injizierter Zeitplanung.
- `window_geometry`: Geometrietexte lesen/schreiben, Fenster auf der Arbeitsfläche halten.
- `system_appearance`: Hell/Dunkel des Systems auf macOS, Windows und Linux deuten.
- `redo_history`: Wiederholen-Stapel neben dem Rückgängig-Stapel des Hosts.
- `text_fit`: Text auf Zeichen- oder Pixelbreite kürzen, Zeichen auf gleiche Breite bringen.
- `action_picker`: durchsuchbare Aktionsauswahl aus einem fertigen Menü (Ordnen, Suchen, Gruppieren).
- `runtime_paths`: Daten- und Cacheordner nach Plattformkonvention auflösen, ohne Dateisystemmutation.
- `command_history`: Rückgängig/Wiederholen für Zustandsabbilder und Befehlsobjekte (Phase 4).
- `app_host`: Hauptfenster, Startprüfungen, Menüleiste, Kürzel und Beenden für einen Controller (Phase 5).
- `selftest`: Prüfung einer übernommenen Kopie auf dem Zielrechner (`python -m glide_shell.selftest`).

Das Paket lädt beim Import nichts nach; Hosts importieren die Bausteine
einzeln, etwa `from glide_shell import modal_session`. Ein lauffähiges
Beispiel ohne Glide ist `python -m glide_shell.demo`; die Anleitung für
Folgeprojekte steht in `README.md` (Englisch) und `README.de.md` (Deutsch).
"""

SHELL_VERSION = "0.6.2"

__all__ = ["SHELL_VERSION", "modal_session", "window_lifetime", "custom_controls", "desktop_adapter", "motion",
           "window_geometry", "system_appearance", "redo_history", "text_fit", "action_picker",
           "runtime_paths", "command_history", "app_host", "selftest", "demo"]
