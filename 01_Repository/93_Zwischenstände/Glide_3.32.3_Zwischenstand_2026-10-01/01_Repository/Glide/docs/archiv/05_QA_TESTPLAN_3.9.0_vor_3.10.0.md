# QA-Testplan – Glide 3.9.0

Stand 12.09.2026

`python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.9.0/oberflaeche/abschluss`

Der Lauf prüft Syntax, Versionen, Dokumentindex/-links, historische Datenformate, dreizehn Integrationssuiten, zwei Analysen sowie Reproduktion von Beispieldaten und Release-Fixture. Jede Suite verwendet vor dem App-Import einen temporären `GLIDE_DATA_DIR`. Echte Nutzerdaten werden nie verwendet.

Die neue Suite `test_ui39.py` ergänzt:

- Hell/Dunkel, Kopfzeile, ausblendbare Seitenleiste einschließlich voller Inhaltsbreite und Speicherung.
- Gleichmäßige Vorlagenabstände und erreichbare Schaltflächen.
- Auswahl ohne zusätzliche Toplevels/Grabs; wiederholter Außerklick, Escape, Tab, Pfeile/Enter, Fokusverlust und Zerstörung bei offenem Popup; Abbau temporärer Bindtags.
- Grafische Einfach-/Mehrfachauswahl, Verhalten im modalen Dialog und Rückkehr zur Hauptapp.
- „Neue Liste“ bei simulierten 720/1400 Pixeln Bildschirmhöhe, Zweispaltenmodus und thematische Felder.
- Light/Dark Mode speichern, Aktionen-Parität einschließlich Untermenüs, Suche und Textkopieren.

Bestehende Suiten prüfen weiter Datensicherheit, Migration/Originalkopien, Struktur, Undo, Papierkorb, Exporte, Anhänge, Vorlagen, Kalender und Benachrichtigungszustellung. Alte Prüferwartungen an Mac-only-OptionMenus und den verschobenen Themenschalter sind an den neuen UI-Vertrag angepasst.

Native manuelle Prüfung: macOS/Windows, echte App-Wechsel und Trackpad, verschiedene DPI/Monitore, Screenreader und Tastatur, Dock-/Taskleistenaufmerksamkeit, physisches Schlafen/Aufwachen. GUI-Ereignistests und simulierte Bildschirmhöhen ersetzen keine Prüfung auf dem Zielgerät. Der separate Dauerlauf `tests/tools/dauerlauf.py` bleibt eine Freigabeprüfung vor Veröffentlichung.

Maßgeblicher Ergebnisstand: [QA-Bericht](07_QA_BERICHT.md). Keine Signatur-/Installationsfreigabe durch grüne Quelltests.
