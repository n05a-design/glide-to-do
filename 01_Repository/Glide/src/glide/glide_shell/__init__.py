# SPDX-License-Identifier: MPL-2.0
"""Glide Shell – wiederverwendbares Tk-Fundament ohne Glide-Bezug (D86, D95).

Die Shell bündelt anwendungsneutrale Desktop-Bausteine für Tk-Anwendungen.
Jedes Modul importiert ausschließlich die Standardbibliothek, `tkinter` und
andere Module dieses Pakets; Werte, Texte und Farben liefert der Host als
Argumente oder Rückrufe (Abhängigkeitsrichtung Host → Shell → Tk).

Bausteine:
- `modal_session`: Dialogfabrik `create_dialog`, modaler Warteweg mit Griff,
  Freigabe und Fokusrückgabe (`run_modal`, `wait_modal`, `modal_over`).
- `window_lifetime`: Zeitgeberbesitz je Widget (`AfterScope`, `scope_for`).
- `custom_controls`: thementaugliche Canvas-Bedienelemente.
- `desktop_adapter`: Menüleiste, Tastaturkürzel und Betriebssystemaktionen.

Das Paket lädt beim Import nichts nach; Hosts importieren die Bausteine
einzeln, etwa `from glide_shell import modal_session`. Ein lauffähiges
Beispiel ohne Glide ist `python -m glide_shell.demo`.
"""

SHELL_VERSION = "0.1.0"

__all__ = ["SHELL_VERSION", "modal_session", "window_lifetime", "custom_controls", "desktop_adapter", "demo"]
