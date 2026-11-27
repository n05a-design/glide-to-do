# Post-Release-Entscheidungsvorlagen (M01–M14)

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26

Dieses Dokument bündelt die 14 strategischen Entscheidungsvorlagen für den Inhaber von Glide im Anschluss an die Veröffentlichung von Glide 1.0.2. Jede Vorlage ist vollständig nach dem verbindlichen 26-Punkte-Katalog ausgearbeitet und bietet entscheidungsreife Varianten.

---

## Übersicht der Entscheidungsvorlagen

| Referenz | Thema | Bisheriger Bezug | Kernfrage | Empfohlene Richtung | Freigabestatus |
|---|---|---|---|---|---|
| **M01** | Systemweite Schnellerfassung | G07 / Q2 | Globaler Hotkey vs. Einzelfenster | **Variante A:** Schlankes System-Tray/Hotkey-Helferprogramm (Phase 3) | Offen (Inhaber) |
| **M02** | Hintergrund-Erinnerungen | Grenze Stufe C / D24 | Dauerhafter Daemon vs. Nur-App-Laufzeit | **Variante A:** Diskrete OS-Benachrichtigungen nur bei laufender App (Status Quo beibehalten) | Offen (Inhaber) |
| **M03** | CalDAV-Synchronisation | WA-33 | Zwei-Wege-Sync vs. Lokaler ICS-Import | **Variante A:** Strikt lokaler ICS-Datei-Import/-Export beibehalten | Offen (Inhaber) |
| **M04** | Lokaler MCP-Server | Q3 / WA-61 | Direkter KI-Zugriff vs. Dateiaustausch | **Variante C+D:** Read-only-MCP & Änderungsvorschläge mit Freigabe (Phase 3) | Offen (Inhaber) |
| **M05** | Deep Links (`glide://`) | WA-34 | URL-Schema-Registrierung im OS | **Variante B:** Read-only Deep Links zur Navigation in Aufgaben/Seiten (Phase 3) | Offen (Inhaber) |
| **M06** | Lokale OCR-Texterkennung | WA-35 | Offline-Texterkennung für Bildanhänge | **Variante B:** Optionales lokales Tesseract-Plugin / Lazy-Loading (Phase 4) | Offen (Inhaber) |
| **M07** | Verschlüsselte Datenhaltung | G22 | SQLCipher/Verschlüsselung vs. Plaintext | **Variante A:** Unverschlüsselte lokale Dateien + OS-Verschlüsselung (FileVault/BitLocker) | Offen (Inhaber) |
| **M08** | Mobile Companion App | D03 | Native Smartphone-App vs. Desktop-Exzellenz| **Variante A:** Keine mobile App; kompromisslose Konzentration auf Desktop | Offen (Inhaber) |
| **M09** | Weitere Oberflächensprachen| D93 | Französisch/Spanisch vs. Nur DE/EN | **Variante B:** Community-Übersetzungskataloge über getrennte JSON/PO-Dateien (Phase 4)| Offen (Inhaber) |
| **M10** | Erledigungsverlauf & Habits | G06 | Habit-Tracker vs. Reine Aufgabenverwaltung| **Variante B:** Sanfte visuelle Wochenmuster ohne Zwangs-Streaks (Phase 3, L2) | Offen (Inhaber) |
| **M11** | Erweiterte Energieplanung | Marktvorschlag | Energielevel-Tags (Hoch/Mittel/Niedrig) | **Variante B:** Optionales Filter-Label für mentale Energie (Phase 2) | Offen (Inhaber) |
| **M12** | Work-in-Progress (WIP) Limits| Marktvorschlag | Begrenzung gleichzeitiger Aufgaben | **Variante B:** Sanfte Warnung bei mehr als 3 Aufgaben in Heute (Phase 2) | Offen (Inhaber) |
| **M13** | Erweiterte Pixel-Werkstatt | Marktvorschlag | SVG-Vektorisierung & Animations-Export | **Variante B:** PNG- und animierter GIF-Export ohne schwere Abhängigkeiten (Phase 3) | Offen (Inhaber) |
| **M15** | Rechtschreibprüfung (EDITOR-02) | Master-Serie Teil 03 | Welche Engine hinter `glide_shell.spellcheck`? | **Variante A:** systemeigene Prüfung je Plattform, keine mitgelieferten Wörterbücher | Offen (Inhaber) |
| **M14** | Lokales Plugin-System | Post-1.0-Architektur| Python-Erweiterbarkeit für Power-User | **Variante A:** Vorerst zurückgestellt; Stabilität des Bento-/Shell-Kerns geht vor | Offen (Inhaber) |

---


### [M01] Systemweite Schnellerfassung (Global Quick Capture)

1. **Fragestellung:** Soll Glide eine globale Tastenkombination (z. B. `Ctrl+Alt+Space` / `Cmd+Shift+Space`) unterstützen, um Aufgaben aus jeder beliebigen Anwendung heraus ohne sichtbares Hauptfenster blitzschnell zu erfassen?
2. **Konkrete Problemstellung:** Nutzer arbeiten in Browser, IDE oder Textverarbeitung und müssen den aktuellen Arbeitskontext verlassen, das Glide-Hauptfenster in den Vordergrund holen und die Schnellerfassung aufrufen. Das unterbricht den Denkfluss.
3. **Bestehende Inhaberentscheidung:** G07 / Q2: Glide läuft als Einzelfenster-Anwendung ohne ressourcenfressende Hintergrund-Daemons; Schnellerfassung ist innerhalb der App voll integriert.
4. **Tatsächlich vorhandene Funktionalität:** Schnellerfassung (`quick_capture.py`, `capture_parser.py`) mit zweisprachiger Datumserkennung (DE/EN) bei aktivem Glide-Fenster.
5. **Relevante Marktbeobachtung:** Things 3 bietet das Branchen-Vorbild für globale Schnellerfassung (Quick Entry mit Autofill). Obsidian nutzt globale Hotkeys über Dritt-Plugins oder externe Launcher (Alfred, Raycast).
6. **Erwarteter Nutzermehrwert:** Reduziert die Erfassungshürde für spontane Ideen auf unter 2 Sekunden; verhindert Kontextwechsel.
7. **Differenzierte Untersuchung der fünf Lösungsvarianten:**
   - **Variante A: Aktiver Hintergrundprozess mit globalem Hotkey**
     - *Mechanismus:* Ein schlankes, eigenständiges Helferprogramm (`glide_quick_entry.pyw`), das im System-Tray / in der macOS-Menüleiste sitzt, auf den globalen Hotkey lauscht, ein minimalistisches 400x120px Erfassungsfenster öffnet und neue Aufgaben atomar in die lokale Aufgabenablage schreibt.
     - *Ressourcen:* Ca. 25–35 MB RAM dauerhaft im Leerlauf; vernachlässigbare CPU-Last.
     - *Plattformen:* Win32 `RegisterHotKey` (stabil); macOS Carbon/Cocoa Event Taps (erfordert explizite Bedienungshilfen-Rechte in den Systemeinstellungen); Linux unter X11 gut machbar, unter Wayland jedoch restriktiv (erfordert Desktop-Portal oder globale Compositor-Keybindings).
     - *Datenintegrität:* Schreibt atomar über Dateisperren in den `item_change`-Weg; bei laufender Hauptanwendung muss diese Dateiänderungen neu einlesen.
     - *Inhaberphilosophie:* Steht im leichten Spannungsfeld mit der Grenze Stufe C (keine dauerhaften Hintergrund-Daemons); als optionales Werkzeug vertretbar.
   - **Variante B: Dateibasierte Schnellerfassung über ein Eingangsverzeichnis (Inbox Directory Watcher)**
     - *Mechanismus:* Glide überwacht beim Start oder periodisch einen lokalen Eingangsordner (z. B. `~/.glide/inbox/` oder `inbox.txt`). Externe Skripte, Notiztools oder Kurzbefehle legen Textdateien dort ab; Glide importiert sie beim nächsten Öffnen oder im Hintergrund.
     - *Ressourcen:* Null zusätzlicher RAM, wenn Glide geschlossen ist.
     - *Plattformen:* 100 % plattformübergreifend und OS-unabhängig.
     - *Datenintegrität:* Extrem robust; atomare Dateiverschiebung (`os.replace`).
     - *Inhaberphilosophie:* Entspricht perfekt Glides dateibasierter Unix-Philosophie (D01, D02).
   - **Variante C: CLI-Aufruf über Startparameter (z. B. `glide --quick-add "..."`)**
     - *Mechanismus:* Aufruf von Glide über die Befehlszeile mit Parametern. Ein minimalistischer Parser übernimmt den Text, parst Datumswörter via `capture_parser.py`, hängt die Aufgabe an den Aufgabenbestand an und terminiert sofort ohne Tkinter-GUI-Aufbau.
     - *Ressourcen:* Nur kurzlebiger Prozess für ca. 150–200 ms; kein Dauerläufer.
     - *Plattformen:* Funktioniert identisch unter Windows, macOS und Linux. Lässt sich systemweit mit beliebigem OS-Shortcut-Manager (z. B. Raycast, Alfred, Windows PowerToys Run, AutoHotkey, Sway/i3) verknüpfen.
     - *Datenintegrität:* Sehr hoch, wenn Datei-Locking beachtet wird.
     - *Inhaberphilosophie:* Sehr sympathisch für Power-User und Shell-Integratoren; keine Daemons nötig.
   - **Variante D: Direktes Schreiben in eine lokale JSON-Datei ohne GUI-Start**
     - *Mechanismus:* Ein autarkes Python-Skript oder CLI liest und manipuliert `tasks.json` direkt auf Plattenebene.
     - *Ressourcen:* Minimal.
     - *Plattformen:* Universell.
     - *Datenintegrität:* Risikoreich bei gleichzeitig geöffneter Haupt-App (Race Condition, Überschreiben nicht gespeicherter Änderungen).
     - *Inhaberphilosophie:* Widerspricht der Integrität von Glides Transaktionsschicht (`guarded_structural_change`).
   - **Variante E: Beibehaltung des Status Quo (Schnellerfassung nur bei geöffnetem Fenster)**
     - *Mechanismus:* Schnellerfassung (`quick_capture.py`) bleibt wie bisher an das aktive, fokussierte Glide-Hauptfenster gebunden.
     - *Ressourcen:* 0 MB Zusatzressourcen, 0 Hintergrundprozesse.
     - *Inhaberphilosophie:* Reinste Lehre (D24, Grenze Stufe C).
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Entspricht Variante E.
9. **Technische Abhängigkeiten:** Plattformübergreifende Hotkey-Registrierung erfordert OS-spezifische Schnittstellen (z. B. `pynput` oder native Windows/macOS API-Aufrufe).
10. **Betroffene Quellmodule:** `src/glide/quick_capture.py`, `src/glide/capture_parser.py`, `src/glide/app.pyw`, optional `src/glide/cli.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** In Variante A: Neues Kontextmenü im System-Tray / in der macOS-Menüleiste; kleiner, schwebender Schnellerfassungsdialog. In Variante C: Keine GUI-Änderung.
12. **Datenschutz:** Vollständig lokal; keine Datenübertragung.
13. **Sicherheit:** Unter macOS erfordert das Abfangen globaler Tastendrücke Bedienungshilfen-Rechte (Accessibility Permissions), was Nutzer misstrauisch machen kann.
14. **Plattformfolgen:** Unterschiedliche Registrierungsmechanismen unter Windows (Win32 `RegisterHotKey`), macOS (Carbon/Cocoa Event Taps) und Linux (X11 / Wayland). Unter Wayland sind globale Hotkeys restriktiv.
15. **Datenformatfolgen:** Keine; nutzt atomaren `item_change`-Dateischreibweg in Format 26.
16. **Auswirkungen auf Glide Shell:** Keine; läuft im Host oder separatem Helfer.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Gedanken können unmittelbar im Entstehen festgehalten werden.
    - *P2 (Form folgt Funktion):* Schwebendes Erfassungsfeld beschränkt sich auf eine klare Zeile.
    - *P3 (Keine Funktion doppelt):* `capture_parser.py` wird 1:1 wiederverwendet.
    - *P4 (Kein Platz verschwenden):* Kein permanenter Bildschirmplatz belegt.
    - *P5 (Nur das Wesentliche):* Keine ablenkenden Zusatzfelder bei der Erfassung.
    - *P6 (Geringe Komplexität):* Varianten B und C halten die interne Systemkomplexität minimal; Variante A erhöht sie durch Tray- und Hook-Logik.
19. **Aufwand mit Begründung:** **M** (ca. 3–4 Entwicklertage für Variante C oder A).
20. **Risiken:** Berechtigungshürden unter macOS; Hängenbleiben verwaister Tray-Prozesse.
21. **Wartungsaufwand:** Moderat bei Betriebssystem-Updates.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante C (CLI-Aufruf) in Phase 2 umsetzen**, da sie zero Hintergrund-Ressourcen verbraucht und mit externen Launchern (Raycast, Alfred, PowerToys) perfekt harmoniert; **Variante A als optionales Hilfsprogramm in Phase 3** evaluieren.
24. **Geeignete Entwicklungsphase:** Phase 2 (Variante C) / Phase 3 (Variante A).
25. **Konkrete Akzeptanzkriterien:** 1. Aufruf speichert die Aufgabe im Eingang in < 200 ms. 2. Datumswörter werden korrekt erkannt. 3. Keine GUI-Blockade.
26. **Erforderliche Inhaberfreigabe:** **Ja (Architektur- und Berechtigungsentscheidung).**

---

### [M02] Hintergrund-Erinnerungszustellung (Background Notifications)

1. **Fragestellung:** Soll Glide Benachrichtigungen für fällige Aufgaben zustellen können, wenn die Hauptanwendung nicht geöffnet ist?
2. **Konkrete Problemstellung:** Aufgaben mit exakter Uhrzeit-Erinnerung werden verpasst, wenn Glide während des Arbeitstages geschlossen wurde.
3. **Bestehende Inhaberentscheidung:** Grenze Stufe C / D24: Glide verzichtet bewusst auf permanente Hintergrunddienste oder Daemons, um Ressourcen zu schonen und keine versteckten Prozesse laufen zu lassen.
4. **Tatsächlich vorhandene Funktionalität:** Erinnerungsdialoge und akustische Hinweise erscheinen zuverlässig, solange Glide läuft oder minimiert ist (`reminders.py`).
5. **Relevante Marktbeobachtung:** Web-Apps fordern Browser-Push-Rechte an; Desktop-Apps wie Things nutzen den systemeigenen Kalender oder Notification Center Daemons.
6. **Erwarteter Nutzermehrwert:** Zuverlässige Erinnerung an zeitkritische Aufgaben, auch wenn Glide vergessen wurde zu starten.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo beibehalten / Empfohlen):* Glide bleibt ein reines Einzelfenster-Programm. Erinnerungen greifen bei laufender App. Zur externen Erinnerung nutzen Anwender den Kalenderexport (`.ics`) in ihren Systemkalender (Apple Kalender, Windows Outlook).
   - *Variante B:* Eintragung fälliger Aufgaben in den systemeigenen Task-Scheduler (Windows Aufgabenplanung / macOS `launchd`), der zu Fälligkeitszeitpunkten eine native OS-Benachrichtigung auslöst.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Variante B erfordert Verwaltung von `launchd` plist-Dateien bzw. Windows Scheduled Tasks.
10. **Betroffene Quellmodule:** `src/glide/reminders.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** Keine sichtbare Änderung, außer Einstellungsoption „Erinnerungen an Systemkalender übergeben“.
12. **Datenschutz:** Vollständig offline.
13. **Sicherheit:** Manipulation von Task-Schedulern kann Antiviren-Heuristiken triggern.
14. **Plattformfolgen:** Hoher Wartungsaufwand für drei Betriebssystem-Scheduler.
15. **Datenformatfolgen:** Keine.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Verlässliche Benachrichtigung nur bei aktiver Anwendung ist ehrlich und transparent.
    - *P2 (Form folgt Funktion):* Diskreter Erinnerungsdialog, keine aufdringlichen Overlays.
    - *P3 (Keine Funktion doppelt):* Betriebssystem-Kalender übernehmen die externe Alarmierung besser als ein zweiter Daemon.
    - *P4 (Kein Platz verschwenden):* Keine persistenten Tray-Icons.
    - *P5 (Nur das Wesentliche):* Konzentration auf den eigentlichen Arbeitskontext.
    - *P6 (Geringe Komplexität):* Variante A vermeidet die enorme Komplexität fehleranfälliger OS-Scheduler-Integrationen.
19. **Aufwand mit Begründung:** **L** für Variante B (ca. 5 Entwicklertage wegen robuster Fehlerbehandlung bei Zeitumstellungen und System-Standby).
20. **Risiken:** Verwaiste System-Tasks bei gelöschten Aufgaben; Beschwerden über Hintergrund-Aktivität.
21. **Wartungsaufwand:** Hoch bei Betriebssystem-Updates.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A (Status Quo beibehalten).** Die Trennung ist ehrlich und ressourcenschonend. Für Alarme ist der iCalendar-Export der verlässlichere Weg.
24. **Geeignete Entwicklungsphase:** Zurückgestellt / Phase 4.
25. **Konkrete Akzeptanzkriterien:** Bestehende Erinnerungen bei laufender App bleiben zu 100 % zuverlässig.
26. **Erforderliche Inhaberfreigabe:** **Ja (Bestätigung der Grenze Stufe C).**
19. **Aufwand mit Begründung:** **L** für Variante B (ca. 5 Entwicklertage wegen robuster Fehlerbehandlung bei Zeitumstellungen und System-Standby).
20. **Risiken:** Verwaiste System-Tasks bei gelöschten Aufgaben; Beschwerden über Hintergrund-Aktivität.
21. **Wartungsaufwand:** Hoch bei Betriebssystem-Updates.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A (Status Quo beibehalten).** Die Trennung ist ehrlich und ressourcenschonend. Für Alarme ist der iCalendar-Export der verlässlichere Weg.
24. **Geeignete Entwicklungsphase:** Zurückgestellt / Phase 4.
25. **Konkrete Akzeptanzkriterien:** Bestehende Erinnerungen bei laufender App bleiben zu 100 % zuverlässig.
26. **Erforderliche Inhaberfreigabe:** **Ja (Bestätigung der Grenze Stufe C).**

---

### [M03] CalDAV-Zwei-Wege-Synchronisation

1. **Fragestellung:** Soll Glide eine automatische Netzwerk-Synchronisation von Terminen über das CalDAV-Protokoll (z. B. für Nextcloud, Fastmail, Apple iCloud) implementieren?
2. **Konkrete Problemstellung:** Termine müssen derzeit manuell als `.ics`-Datei exportiert und importiert werden, um sie mit externen Kalendern abzugleichen.
3. **Bestehende Inhaberentscheidung:** WA-33: CalDAV wurde als nachrangige Option für Version 1.1+ eingestuft; Glide 1.0.2 arbeitet strikt offline ohne eigene Netzwerkprotokolle.
4. **Tatsächlich vorhandene Funktionalität:** Vollständiger manueller Import und Export von `.ics`-Dateien (`calendar_import.py`, `calendar_export.py`).
5. **Relevante Marktbeobachtung:** Sunsama und Morgen bauen auf tiefen Cloud-Kalender-Syncs auf (Google, Outlook); Super Productivity bietet optionalen CalDAV-Sync.
6. **Erwarteter Nutzermehrwert:** Nahtlose Terminsynchronisation im Hintergrund für Nutzer mit selbstgehosteter Nextcloud.
7. **Lösungsvarianten:**
   - *Variante A (Empfohlen):* Strikt lokaler Ansatz: Ausbau des manuellen Datei-Workflows (z. B. automatische Erkennung geänderter lokaler `.ics`-Dateien in einem überwachten Verzeichnis) ohne direkte Netzwerkanbindung.
   - *Variante B:* Separates, rein optionales CalDAV-Synchronisations-Plugin (`glide_sync_caldav.py`), das Zugangsdaten im OS-Keyring speichert und auf Nutzerbefehl abgleicht.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Manueller Menüaufruf für Import/Export.
9. **Technische Abhängigkeiten:** Variante B erfordert `caldav`-Bibliothek oder manuelle HTTP/XML/WebDAV-Implementierung und Zugangsdatenverwaltung (z. B. `keyring`).
10. **Betroffene Quellmodule:** `src/glide/calendar_view.py`, `src/glide/network/` (neu).
11. **Auswirkungen auf die Benutzeroberfläche:** Neuer Einstellungsreiter „Kalender-Konten“ mit Server-URL, Benutzername, Passwort-Aufforderung.
12. **Datenschutz:** Netzwerkübertragung von Kalenderdaten birgt Sicherheits- und Vertraulichkeitsrisiken.
13. **Sicherheit:** Speicherung von Passwörtern/App-Tokens auf dem lokalen Rechner erfordert sicheren Schlüsselbund.
14. **Plattformfolgen:** Schlüsselbund-APIs unterscheiden sich fundamental zwischen Windows (Credential Manager), macOS (Keychain) und Linux (Secret Service).
15. **Datenformatfolgen:** Zusätzliche externe Kalender-UIDs müssen persistent gespeichert werden.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Manueller Datei-Import (.ics) funktioniert ohne Netzwerk-Abbrüche oder Fehlermeldungen.
    - *P2 (Form folgt Funktion):* Keine unübersichtlichen Sync-Einstellungsdialoge im Kern.
    - *P3 (Keine Funktion doppelt):* Kalenderprogramme (Apple Kalender, Thunderbird, Outlook) synchronisieren bereits; Glide muss keinen CalDAV-Client nachbauen.
    - *P4 (Kein Platz verschwenden):* Keine Sync-Status-Icons oder Verbindungsbalken.
    - *P5 (Nur das Wesentliche):* Lokale Tagesplanung bleibt im Mittelpunkt.
    - *P6 (Geringe Komplexität):* Vermeidet hunderte Zeilen fehleranfälligen Netzwerk- und Synchronisations-Code (D01).
19. **Aufwand mit Begründung:** **XL** (mindestens 10 Entwicklertage für Konfliktlösung, Netzwerkausfall-Handling, Keyring-Integration und Tests).
20. **Risiken:** Hohe Fehleranfälligkeit bei schlechter Internetverbindung; Konflikte bei gleichzeitiger Änderung auf zwei Geräten; Bruch des Offline-First-Markenkerns.
21. **Wartungsaufwand:** Sehr hoch.
22. **Mögliche Kosten:** 0 € (Open-Source-Protokoll), aber erheblicher Supportaufwand.
23. **Begründete Empfehlung:** **Variante A (Ablehnung von CalDAV-Netzwerkcode im Kern).** Glide zeichnet sich durch absolute Verlässlichkeit ohne Sync-Konflikte aus. Datei-Austausch genügt.
24. **Geeignete Entwicklungsphase:** Bewusst zurückgestellt auf unbestimmte Zeit.
25. **Konkrete Akzeptanzkriterien:** Der Datei-Import von ICS bleibt fehlerfrei und wird um VALARM (WA-59) erweitert.
26. **Erforderliche Inhaberfreigabe:** **Ja (Schutz der Offline-Produktgrenze D01).**

---

### [M04] Lokaler MCP-Server (Model Context Protocol) – Detaillierte Architekturanalyse

1. **Fragestellung:** Soll Glide eine native Schnittstelle für das offene Model Context Protocol (MCP) anbieten, damit lokale KI-Agenten (wie Anthropic Claude Desktop, Google Antigravity, Gemini CLI, OpenAI Codex) strukturiert auf Aufgaben, Notizen und Projektkontexte zugreifen können?
2. **Konkrete Problemstellung:** Der bisherige KI-Austausch erfolgt über dateibasierte `.glideexchange`-Pakete. Nutzer müssen Dateien manuell exportieren, dem Agenten übergeben und das Ergebnis manuell importieren. Ein standardisierter MCP-Server würde diesen Dialog revolutionieren, birgt aber fundamentale Risiken für Datenintegrität und Sicherheit.
3. **Bestehende Inhaberentscheidung:** Q3 / D91 / D92: Glide kommuniziert mit KI-Agenten ausschließlich über überprüfbare Dokumente nach dem offenen Agent-Skills-Standard (`skills/glide-to-do/`). Direkte Schreibzugriffe fremder Agenten auf die aktive Datenbank sind strikt verboten.
4. **Tatsächlich vorhandene Funktionalität:** Zentrierter Agent-Skill `glide-to-do` (WA-61), Austauschformat 2, syntaktische und semantische Prüfung via `ki_ausgabe.py`.
5. **Relevante Marktbeobachtung:** MCP entwickelt sich zum De-facto-Industriestandard für die Anbindung lokaler Daten an Desktop-LLMs. Obsidian, Apple Notes und lokale SQLite-Tools bieten erste MCP-Server über `stdio` an.
6. **Erwarteter Nutzermehrwert:** Nahtlose Recherche und strukturierte Arbeitsvorbereitung: Ein Agent kann direkt fragen: „Welche Aufgaben sind heute fällig?“ oder „Erstelle mir einen Projektplan für das Vorhaben Stadtlicht“ – ohne manuelle Dateiverschiebungen.
7. **Differenzierte Untersuchung der Lösungsvarianten:**
   - **Variante A: Bestehender dateibasierter Austausch (Status Quo)**
     - *Mechanismus:* Agent erzeugt `.glideexchange`-Dateien, Nutzer importiert sie manuell über den Glide-Importdialog mit Vorschau, Transaktionssicherung und Undo.
     - *Vorteile:* Bewährte dateibasierte Technologie (Format 2); kein offener Socket-Server; Nutzer behält vor dem Einlesen die volle manuelle Sicht- und Freigabekontrolle.
     - *Nachteile:* Manueller Klickaufwand; Agent kann den aktuellen Stand nicht direkt automatisiert einsehen.
   - **Variante B: Lokales CLI-Export-Werkzeug (`glide-cli`)**
     - *Mechanismus:* Ein Konsolenbefehl (z. B. `python -m glide.cli export-context`), der Kontextpakete auf die Standardausgabe schreibt oder neue Pakete validiert.
     - *Vorteile:* Einfach zu scripten, kein permanenter Hintergrunddienst.
     - *Nachteile:* Kein echtes MCP-Protokoll; erfordert manuelle Terminal-Kenntnisse.
   - **Variante C: Read-only MCP-Server über `stdio` (Empfohlener Pilot)**
     - *Mechanismus:* Ein autarkes Python-Skript (`src/glide/mcp/server.py`), das als lokaler MCP-Server konfiguriert wird (Start via `stdio` durch Claude Desktop oder Antigravity). Bietet standardisierte Read-Tools an: `list_tasks(status, due)`, `get_project(name)`, `read_page(title)`.
     - *Sicherheit:* **Reiner Lesezugriff.** Der MCP-Server kann niemals Daten in Glide verändern oder löschen.
     - *Vorteile:* Höchster Komfort für Recherchen und Kontextübergabe bei garantierter Datenintegrität.
   - **Variante D: MCP-Server mit strukturierter Vorschlagserzeugung (Proposal Flow)**
     - *Mechanismus:* Ergänzt Variante C um ein Tool `propose_tasks(items)`. Der Agent schreibt diese Aufgaben jedoch nicht direkt in die Datenbank, sondern legt ein signiertes Änderungsvorschlagspaket in Glides Eingangsbereich ab. In Glide erscheint ein dezenter Badge: „1 neuer KI-Änderungsvorschlag“. Der Nutzer prüft die Elemente einzeln (WA-56) und bestätigt die Übernahme.
     - *Vorteile:* Perfekte Symbiose aus modernem MCP-Workflow und Glides unverrückbarem Prinzip der Nutzerkontrolle.
   - **Variante E: Direkte bidirektionale Schreibzugriffe über MCP**
     - *Mechanismus:* Der MCP-Server führt direkt `create_task`, `delete_task`, `update_task` auf den JSON-/SQLite-Datenbeständen aus.
     - *Sicherheitsbewertung:* **Strikte Ablehnung.** Umgeht Glides Transaktionssperren (`guarded_structural_change`), den atomaren Befehlsverlauf (`command_history`), führt zu Race Conditions bei gleichzeitig geöffneter GUI und öffnet Tür und Tor für versehentliche Datenlöschung durch Prompt Injection.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Reine Beibehaltung von Variante A (Agent-Skill `glide-to-do`).
9. **Technische Abhängigkeiten:** Standard-Bibliotheken oder leichtgewichtiges `mcp`-Python-SDK über `stdio` (JSON-RPC 2.0). Kein Netzwerk-Port (kein HTTP/SSE-Server), ausschließlich lokale Standard-E/A.
10. **Betroffene Quellmodule:** Neues isoliertes Unterpaket `src/glide/mcp/` an der Anwendungs- und Schnittstellengrenze (Ebene A), `src/glide/core.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** In Variante D: Diskreter Eingangs-Indikator für KI-Vorschläge.
12. **Datenschutz:** Lokale Prozesskommunikation über Standard-E/A-Pipes (`stdio`). **Wichtige Präzisierung:** Werden cloudbasierte LLM-Clients (z. B. Claude Desktop über Anthropic API, Google Antigravity oder OpenAI) angebunden, verlassen die übermittelten Aufgaben und Notizauszüge den Rechner in Richtung der Cloud-Server des jeweiligen Modellanbieters. Ein vollständig isolierter Datenschutz besteht ausschließlich beim Einsatz lokaler Open-Source-Modelle (z. B. via Ollama oder LocalAI).
13. **Sicherheit:** Exzellent in Variante C und D; katastrophal in Variante E.
14. **Plattformfolgen:** Plattformübergreifend identisch (Standard-Python `sys.stdin`/`sys.stdout`).
15. **Datenformatfolgen:** Keine; nutzt die bestehenden Datenabfrageroutinen von Format 26.
16. **Auswirkungen auf Glide Shell:** Vollkommen entkoppelt von der Framework Shell.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Standardisiertes Protokoll erleichtert Anbindung an moderne KI-Assistenten ohne proprietäre Skripte.
    - *P2 (Form folgt Funktion):* Reine Daten- und Tool-Schnittstelle ohne visuelle Überfrachtung.
    - *P3 (Keine Funktion doppelt):* Nutzt die bestehenden Validierungsregeln aus `ki_ausgabe.py` und das Austauschformat 2.
    - *P4 (Kein Platz verschwenden):* Keine zusätzlichen permanenten UI-Elemente; diskreter Indikator nur bei vorliegenden Vorschlägen.
    - *P5 (Nur das Wesentliche):* Tools beschränken sich strikt auf die Kernentitäten (Aufgaben, Notizen, Projekte).
    - *P6 (Geringe Komplexität):* Variante C (Read-only stdio) hält die Komplexität minimal; Variante E würde extreme Nebenläufigkeits- und Locking-Komplexität erzwingen und wird daher strikt verworfen.
19. **Aufwand mit Begründung:** **L** (ca. 5 Entwicklertage für Variante C + D inklusive MCP-Tools, JSON-RPC-Parser und Validierung).
20. **Risiken:** Nutzer könnten erwarten, dass Schreibzugriffe direkt ohne Bestätigung erfolgen; klare Kommunikation der Proposal-Architektur zwingend.
21. **Wartungsaufwand:** Gering, da JSON-RPC über `stdio` sehr stabil ist.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante C in Phase 3 pilotieren, gefolgt von Variante D.** Variante E wird aus Integritätsgründen endgültig ausgeschlossen.
24. **Geeignete Entwicklungsphase:** Phase 3.
25. **Konkrete Akzeptanzkriterien:** 1. Claude Desktop oder Antigravity kann über MCP die heutigen Aufgaben abfragen. 2. Schreibversuche über das Protokoll werden abgewiesen oder als Freigabe-Paket abgelegt. 3. Keine Netzwerk-Sockets geöffnet.
26. **Erforderliche Inhaberfreigabe:** **Ja (Strategische Schnittstellen-Entscheidung).**

---

### [M05] Deep Links (`glide://item/...`)

1. **Fragestellung:** Soll Glide beim Betriebssystem das benutzerdefinierte URL-Schema `glide://` registrieren, um Aufgaben, Listen, Seiten und Pinnwände direkt aus externen Dokumenten (z. B. Obsidian, Mail, Browser-Lesezeichen) verlinken zu können?
2. **Konkrete Problemstellung:** Power User pflegen Projektnotizen in externen Markdown-Tools und möchten mit einem Klick genau die passende Aufgabe in Glide öffnen.
3. **Bestehende Inhaberentscheidung:** WA-34: Deep Links wurden als Mehrwertoption identifiziert, aber vor Version 1.0 zurückgestellt, um den Installer schlank zu halten.
4. **Tatsächlich vorhandene Funktionalität:** Interne Referenzen (`glide://`-Format wird in `references.py` textuell für interne Verweise genutzt, ist aber nicht systemweit registriert).
5. **Relevante Marktbeobachtung:** Things 3 besitzt ein weltklasse URL-Schema (`things:///show?id=...`), das intensiv in Produktivitäts-Workflows genutzt wird.
6. **Erwarteter Nutzermehrwert:** Nahtlose Integration in das persönliche Wissensmanagement; Glide wird zur verlässlichen Ausführungs-Engine externer Notizen.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo):* Interne Links funktionieren nur innerhalb der laufenden Glide-Instanz.
   - *Variante B (Empfohlen):* Registrierung des URL-Protokolls `glide://` über den Inno Setup Installer (Windows Registry) und das macOS `Info.plist` (`CFBundleURLTypes`). Befehle: `glide://open?id=<UUID>` (öffnet Aufgabe oder Seite), `glide://quick-entry` (öffnet Schnellerfassung).
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Keine OS-Registrierung.
9. **Technische Abhängigkeiten:** URL-Handler im App-Host (`app_host.py` / `app.pyw`). Single-Instance-Kommunikation (IPC via lokalem Named Pipe oder Socket), um Parameter an ein bereits laufendes Glide-Fenster zu übergeben.
10. **Betroffene Quellmodule:** `src/glide/glide_shell/app_host.py`, `src/glide/app.pyw`, `packaging/windows/glide.iss`, `packaging/macos/Info.plist`.
11. **Auswirkungen auf die Benutzeroberfläche:** Neuer Menüpunkt im Kontextmenü von Aufgaben und Seiten: „Link kopieren“ (`glide://item/<ID>`).
12. **Datenschutz:** Vollständig lokal.
13. **Sicherheit:** **Kritisch:** Der URL-Handler darf niemals unbestätigte destruktive Aktionen (wie Löschen oder Überschreiben) ausführen, um Angriffe über manipulierte Webseiten-Links zu verhindern. Nur Navigationsaktionen (`open`, `show`).
14. **Plattformfolgen:** IPC-Mechanismus muss unter Windows und macOS sauber implementiert sein.
15. **Datenformatfolgen:** Keine; nutzt bestehende UUIDs.
16. **Auswirkungen auf Glide Shell:** `app_host.py` muss URL-Startargumente verarbeiten.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Klick auf einen externen Verweis öffnet die Aufgabe direkt in Glide.
    - *P2 (Form folgt Funktion):* Das URL-Schema bildet die interne Datenstruktur transparent ab.
    - *P3 (Keine Funktion doppelt):* Nutzt die vorhandene UUID-Auflösung aus `references.py`.
    - *P4 (Kein Platz verschwenden):* Keine zusätzlichen Bedienelemente im Hauptfenster nötig.
    - *P5 (Nur das Wesentliche):* Beschränkung auf sichere Lese- und Navigationsaktionen (`open`, `show`).
    - *P6 (Geringe Komplexität):* Schlanker URL-Dispatcher im App-Host ohne externe Frameworks.
19. **Aufwand mit Begründung:** **M** (ca. 4 Entwicklertage für Installer-Registrierung, IPC-Single-Instance-Signalisierung und Sicherheitshärtung).
20. **Risiken:** Sicherheitslücken bei ungeprüfter URL-Parameterauswertung; muss strikt auf Lese-/Anzeigeaktionen begrenzt werden.
21. **Wartungsaufwand:** Gering.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante B in Phase 3** umsetzen. Hoher Nutzen für anspruchsvolle Wissensarbeiter.
24. **Geeignete Entwicklungsphase:** Phase 3.
25. **Konkrete Akzeptanzkriterien:** 1. Klick auf `glide://open?id=xyz` im Browser bringt Glide in den Vordergrund und selektiert die Aufgabe. 2. Keine Schadcode-Ausführung möglich.
26. **Erforderliche Inhaberfreigabe:** **Ja (Sicherheits- und Installer-Erweiterung).**

---

### [M06] Lokale OCR-Texterkennung für Dateianhänge

1. **Fragestellung:** Soll Glide eine eingebaute lokale Texterkennung (OCR) für gescannte Belege und Bildanhänge anbieten?
2. **Konkrete Problemstellung:** Nutzer hängen Fotos von Quittungen, Whiteboards oder Briefen an Aufgaben an; der Text darin kann über die globale Suche nicht gefunden werden.
3. **Bestehende Inhaberentscheidung:** WA-35: OCR wurde als interessante Option für die Zukunft notiert, aber wegen der Paketgröße von OCR-Bibliotheken abgelehnt.
4. **Tatsächlich vorhandene Funktionalität:** Anhänge werden mit Dateiname, Größe und Zeitstempel lokal abgelegt und verlinkt (`attachments.py`).
5. **Relevante Marktbeobachtung:** Apple Notizen und OneNote bieten serverseitige oder native OS-OCR.
6. **Erwarteter Nutzermehrwert:** Volltextsuche über abfotografierte Notizen und Dokumente.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo / Empfohlen):* Keine native OCR-Engine im Glide-Kern. Nutzer nutzen systemeigene OCR-Werkzeuge (z. B. macOS Live Text oder Windows PowerToys OCR) und fügen erkannten Text in die Notizzeilen ein.
   - *Variante B:* Anbindung an eine optional installierte lokale Tesseract-OCR-Binary über ein externes CLI-Tool.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Tesseract oder Apple Vision Framework (macOS PyObjC). Tesseract bläht Binärpakete um 50–150 MB auf.
10. **Betroffene Quellmodule:** `src/glide/attachments.py`, `src/glide/search.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** Fortschrittsbalken „Texterkennung läuft …“.
12. **Datenschutz:** Offline möglich, aber ressourcenintensiv.
13. **Sicherheit:** Parsing von Bilddateien birgt Verwundbarkeitsrisiken in Bildbibliotheken.
14. **Plattformfolgen:** Extrem hohe Komplexität bei der plattformübergreifenden Bündelung von OCR-Binaries.
15. **Datenformatfolgen:** Zusätzliches Datenfeld `extracted_text` in den Metadaten.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Verzicht auf fehleranfällige Hintergrund-OCR verhindert Hänger und Lärm.
    - *P2 (Form folgt Funktion):* Textnotizen gehören in Markdown-Felder, nicht in unsichtbare OCR-Schichten.
    - *P3 (Keine Funktion doppelt):* OS-Werkzeuge (Live Text, PowerToys) leisten OCR bereits auf Systemebene.
    - *P4 (Kein Platz verschwenden):* Keine Fortschrittsbalken oder unfertigen OCR-Texte in Karten.
    - *P5 (Nur das Wesentliche):* Schützt die Binärgröße (< 20 MB) vor 100+ MB schweren OCR-Modellen.
    - *P6 (Geringe Komplexität):* Variante A hält den Codebestand frei von nativen C-Bindings und Sprachdateien.
19. **Aufwand mit Begründung:** **XL** (mindestens 8 Entwicklertage für Paketierung, Sprachmodelle und Performance).
20. **Risiken:** Explosion der Downloadgröße von 20 MB auf über 100 MB; hohe CPU-/Lüfterlast bei Bildimporten.
21. **Wartungsaufwand:** Sehr hoch.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A (Status Quo beibehalten).** Das Missverhältnis zwischen Downloadgröße/Wartungsaufwand und Nutzermehrwert ist zu groß.
24. **Geeignete Entwicklungsphase:** Zurückgestellt / Phase 4.
25. **Konkrete Akzeptanzkriterien:** Bestehender Anhangs-Workflow bleibt schlank und schnell (< 20 MB Downloadgröße garantiert).
26. **Erforderliche Inhaberfreigabe:** **Ja (Verhinderung von Paket-Bloat).**

---

### [M07] Verschlüsselte Datenhaltung (Encryption at Rest)

1. **Fragestellung:** Soll Glide eine anwendungseigene Datenbankverschlüsselung (z. B. AES-256 via SQLCipher) mit Master-Passwort anbieten?
2. **Konkrete Problemstellung:** Liegen die SQLite-/JSON-Dateien im Klartext auf der Festplatte, können unbefugte Personen mit physischem Zugriff oder Schadsoftware auf dem Rechner die Notizen im Klartext lesen.
3. **Bestehende Inhaberentscheidung:** G22: Glide vertraut auf die bewährte Festplattenverschlüsselung des Betriebssystems (BitLocker unter Windows, FileVault unter macOS, LUKS unter Linux) und verzichtet auf eigene Krypto-Experimente.
4. **Tatsächlich vorhandene Funktionalität:** Lokale Klartextablage in geschütztem Benutzerordner (`%APPDATA%`, `Application Support`).
5. **Relevante Marktbeobachtung:** Standard-Desktop-Apps (Obsidian, Things, Logseq) speichern standardmäßig im Klartext im Benutzerprofil und verlassen sich auf OS-Verschlüsselung. Nur Spezialtools (Standard Notes) bieten Zero-Knowledge-Krypto.
6. **Erwarteter Nutzermehrwert:** Schutz hochsensibler Tagebücher vor anderen lokalen Benutzern.
7. **Lösungsvarianten:**
   - *Variante A (Empfohlen):* Beibehaltung der OS-Verschlüsselung (FileVault/BitLocker). Dokumentation der Sicherheitsarchitektur im Handbuch.
   - *Variante B:* Verschlüsselung einzelner privater Notizbücher über ein Passphrase-geschütztes Archiv.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** `cryptography` Python-Paket (externe C-Erweiterung, widerspricht dem Standardbibliothek-Gebot).
10. **Betroffene Quellmodule:** `src/glide/core.py`, `src/glide/data_migration.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** Passwortabfrage bei jedem Start; irreversibler Datenverlust bei vergessenem Passwort.
12. **Datenschutz:** Höchster Schutz, aber extremes Risiko von Nutzer-Supportfällen.
13. **Sicherheit:** Eigene Krypto-Implementierungen bergen hohes Fehlerrisiko (Key Derivation, Memory Dumps).
14. **Plattformfolgen:** C-Extensions erschweren native Bündelung.
15. **Datenformatfolgen:** Fundamentaler Bruch mit Format 26 (lesbares JSON).
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Dateien lassen sich ohne Passwortabfrage oder Krypto-Hänger öffnen.
    - *P2 (Form folgt Funktion):* Transparentes JSON-Format ermöglicht Reparatur und Inspektion.
    - *P3 (Keine Funktion doppelt):* Betriebssysteme (FileVault, BitLocker) bieten bereits hardwarenahe Vollverschlüsselung.
    - *P4 (Kein Platz verschwenden):* Keine modalen Entsperr-Dialoge beim Programmstart.
    - *P5 (Nur das Wesentliche):* Fokussiert auf Kernfunktionen statt proprietärer Krypto-Verwaltung.
    - *P6 (Geringe Komplexität):* Schließt C-Erweiterungen (`cryptography`) aus und bewahrt die reine Standardbibliothek.
19. **Aufwand mit Begründung:** **XL** (mindestens 10 Entwicklertage + Risiko).
20. **Risiken:** Hohes Risiko von Datenverlust bei Passwortverlust; keine Reparaturmöglichkeit für beschädigte Datenbanken.
21. **Wartungsaufwand:** Sehr hoch.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A (Status Quo beibehalten).** Das Versprechen von lesbarem JSON und einfacher Datensicherung hat Vorrang.
24. **Geeignete Entwicklungsphase:** Zurückgestellt.
25. **Konkrete Akzeptanzkriterien:** Klare Dokumentation in `SECURITY.md`, wie Nutzer ihren Datenordner mit BitLocker/FileVault schützen.
26. **Erforderliche Inhaberfreigabe:** **Ja (Sicherheits-Grundsatzentscheidung).**

---

### [M08] Mobile Begleit-App (Mobile Companion App)

1. **Fragestellung:** Soll für Glide eine Smartphone-App (iOS / Android) entwickelt werden?
2. **Konkrete Problemstellung:** Nutzer möchten unterwegs auf dem Smartphone Aufgaben abhaken oder neue Punkte erfassen.
3. **Bestehende Inhaberentscheidung:** D03 / Produktgrenzen: Glide ist eine reine Desktop-Anwendung. Eine mobile App ist ausdrücklich ausgeschlossen.
4. **Tatsächlich vorhandene Funktionalität:** Reine Desktop-Oberfläche unter Python/Tkinter für macOS, Windows und Linux.
5. **Relevante Marktbeobachtung:** Die Pflege mobiler Apps erfordert separate Codebasen (Swift, Kotlin oder Flutter), laufende App-Store-Gebühren ($99/Jahr Apple, Google Console), Review-Zyklen und zwingend einen sicheren Cloud-Synchronisationsdienst.
6. **Erwarteter Nutzermehrwert:** Mobile Erreichbarkeit der Aufgaben.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo / Empfohlen):* Keine mobile App. Bestätigung der klaren Fokussierung auf kompromisslose Desktop-Produktivität. Für mobile Schnellnotizen nutzen Anwender Standard-Apps und importieren diese am Schreibtisch via Markdown oder Agent-Skill.
   - *Variante B:* Vollständige Neuentwicklung einer mobilen Begleit-App mit Cloud-Sync.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Völlig neue Technologie (Flutter/React Native), Cloud-Server, Datenbank-Synchronisation.
10. **Betroffene Quellmodule:** Gesamtes Projekt.
11. **Auswirkungen auf die Benutzeroberfläche:** Keine auf dem Desktop.
12. **Datenschutz:** Cloud-Sync gefährdet Glides Offline-Datenschutzversprechen.
13. **Sicherheit:** Server-Sicherheit, Authentifizierung, DSGVO-Pflichten.
14. **Plattformfolgen:** Hoher administrativer Aufwand für App Stores.
15. **Datenformatfolgen:** Vollständiger Zwang zu Mehrgeräte-Konfliktauflösung (CRDTs).
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Kompromisslose Tastatur- und Mausoptimierung auf dem Desktop.
    - *P2 (Form folgt Funktion):* Desktop-Oberfläche muss sich nicht für kleine Touchscreens verbiegen.
    - *P3 (Keine Funktion doppelt):* Keine redundanten Apps auf mehreren Plattformen.
    - *P4 (Kein Platz verschwenden):* Volle Ausnutzung von Desktop-Breiten (Bento-Raster, Mehrspalten-Karten).
    - *P5 (Nur das Wesentliche):* Volle Konzentration auf das exzellente Desktop-Erlebnis.
    - *P6 (Geringe Komplexität):* Verhindert mehrjährige Pflege paralleler mobiler Codebasen und Cloud-Syncs.
19. **Aufwand mit Begründung:** **Astronomisch (mehrere Personenjahre).**
20. **Risiken:** Scheitern des Gesamtprojekts an den Wartungskosten mobiler Plattformen.
21. **Wartungsaufwand:** Enorm.
22. **Mögliche Kosten:** Mindestens 99 $/Jahr Developer Fee + Serverbetrieb.
23. **Begründete Empfehlung:** **Variante A (Strikte Bestätigung der Ablehnung D03).** Glides Stärke liegt in der tiefen, ungestörten Desktop-Arbeit.
24. **Geeignete Entwicklungsphase:** Ausgeschlossen.
25. **Konkrete Akzeptanzkriterien:** Festhalten der Grenze in `01_PRODUCT_CONSTRAINTS.md` und `README.md`.
26. **Erforderliche Inhaberfreigabe:** **Ja (Festhalten an Kernprinzip D03).**

---

### [M09] Weitere Oberflächensprachen (Französisch, Spanisch, Italienisch)

1. **Fragestellung:** Soll Glide über Deutsch und Englisch hinaus in weitere europäische Sprachen übersetzt werden?
2. **Konkrete Problemstellung:** Anwender im nicht-deutsch- und nicht-englischsprachigen Raum bevorzugen eine Oberfläche in ihrer Muttersprache.
3. **Bestehende Inhaberentscheidung:** D93: Glide 1.0.2 ist vollständig zweisprachig (Deutsch und Englisch) geliefert und getestet (Test T335).
4. **Tatsächlich vorhandene Funktionalität:** Standardisiertes Lokalisierungsmodul `i18n.py` mit JSON-Katalogen in `src/glide/resources/locales/de.json` und `en.json`.
5. **Relevante Marktbeobachtung:** Internationale Open-Source-Projekte skalieren Sprachversionen über Community-Plattformen (Crowdin, Weblate).
6. **Erwarteter Nutzermehrwert:** Größere internationale Reichweite und Zugänglichkeit in Frankreich, Spanien und Lateinamerika.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo):* Beibehaltung der exzellenten Zweisprachigkeit DE/EN.
   - *Variante B (Empfohlen für Phase 4):* Vorbereitung der Architektur für Community-Übersetzungen: Trennung des Handbuchs von den UI-Strings, sodass freiwillige Übersetzer `fr.json` oder `es.json` beisteuern können.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** `i18n.py` unterstützt bereits beliebige Sprachcodes.
10. **Betroffene Quellmodule:** `src/glide/i18n.py`, `resources/locales/`.
11. **Auswirkungen auf die Benutzeroberfläche:** Dropdown „Sprache“ im Einstellungsdialog um zusätzliche Einträge erweitern.
12. **Datenschutz:** Keine.
13. **Sicherheit:** Überprüfung fremder Übersetzungsdateien auf Textlängen (Vermeidung von Layoutbrüchen).
14. **Plattformfolgen:** Keine.
15. **Datenformatfolgen:** Keine.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Keine (Bento liest Tokens aus dem Host).
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Benutzeroberfläche spricht die Sprache des Nutzers ohne Nachjustieren.
    - *P2 (Form folgt Funktion):* Sprachumschaltung erfolgt nahtlos zur Laufzeit (`refresh_sidebar_locale()`).
    - *P3 (Keine Funktion doppelt):* Zentrale Übersetzungsschlüssel in `i18n.py` ohne Doppelungen.
    - *P4 (Kein Platz verschwenden):* Sorgfältige Längenprüfung verhindert Überläufe in Menüs und Leisten.
    - *P5 (Nur das Wesentliche):* Priorität auf vollständige DE/EN-Qualität vor unfertigen Übersetzungen.
    - *P6 (Geringe Komplexität):* Flache JSON-Kataloge ohne schwere Gettext-Kompilierungsschritte.
19. **Aufwand mit Begründung:** **M** je Sprache (ca. 2 Entwicklertage für Prüfung, Qualitätssicherung und Schnittstellenanpassung).
20. **Risiken:** Unvollständige Übersetzungen bei Feature-Updates; erfordert englische Fallbacks für fehlende Schlüssel.
21. **Wartungsaufwand:** Moderat.
22. **Mögliche Kosten:** 0 € bei Community-Beiträgen.
23. **Begründete Empfehlung:** **Variante B in Phase 4 vorbereiten.** Zunächst die DE/EN-Qualität weiter festigen.
24. **Geeignete Entwicklungsphase:** Phase 4.
25. **Konkrete Akzeptanzkriterien:** Fallback-Mechanismus garantiert, dass bei fehlendem Sprachschlüssel der englische Text erscheint, ohne Absturz.
26. **Erforderliche Inhaberfreigabe:** **Ja.**

---

### [M10] Erledigungsverlauf & Gewohnheiten (Habit Tracker)

1. **Fragestellung:** Soll Glide eine dezidierte Gewohnheits- und Routineerfassung (Habit Tracking mit Streaks und Monatsrastern) integrieren?
2. **Konkrete Problemstellung:** Wiederkehrende tägliche Gewohnheiten (z. B. „Sport machen“, „Lesen“, „Meditation“) verstopfen die normale Aufgabenliste.
3. **Bestehende Inhaberentscheidung:** G06: Routinen gehören zu den Tagesblöcken; kein eigenständiger Habit-Tracker in Version 1.0.
4. **Tatsächlich vorhandene Funktionalität:** Wiederholende Aufgaben (`recurrence.py`) und Routinenblöcke in `time_blocks.py`.
5. **Relevante Marktbeobachtung:** Apps wie Habitica oder Streaks nutzen Gamification; Things und Todoist wickeln Gewohnheiten über wiederholende Aufgaben ab.
6. **Erwarteter Nutzermehrwert:** Unterstützung positiver Alltagsgewohnheiten ohne Wechsel in eine separate Habit-App.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo):* Gewohnheiten werden als reguläre tägliche Wiederholungsaufgaben geführt.
   - *Variante B (Empfohlen):* Ein dedizierter Habit-Bento-Karten-Typ `BentoHabitCard` auf der Startseite: Zeigt 3–5 tägliche Gewohnheiten mit einer diskreten 7-Tage-Punktematrix (ohne Bestrafungs-Streaks).
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Bento Box System 0.2.0+.
10. **Betroffene Quellmodule:** `src/glide/glide_bento/cards/habit_card.py` (neu), `src/glide/habits.py` (neu).
11. **Auswirkungen auf die Benutzeroberfläche:** Neue optionale Bento-Karte für das Home-Dashboard.
12. **Datenschutz:** Vollständig lokal.
13. **Sicherheit:** Keine.
14. **Plattformfolgen:** Keine.
15. **Datenformatfolgen:** Aufgabenformat 26: Speicherung als Liste mit `list_kind: "habits"`.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Bereicherung des Komponenten-Katalogs.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Gewohnheiten lassen sich mit einem Klick auf den Tagespunkt abhaken.
    - *P2 (Form folgt Funktion):* Diskrete 7-Tage-Punktematrix ohne visuelle Bestrafung oder Druck.
    - *P3 (Keine Funktion doppelt):* Nutzt das Aufgaben- und Wiederholungsmodell statt paralleler Datenstrukturen.
    - *P4 (Kein Platz verschwenden):* Integriert als kompakte Bento-Karte auf der Startseite.
    - *P5 (Nur das Wesentliche):* Keine künstlichen Levels, Erfahrungspunkte oder Flammen-Icons.
    - *P6 (Geringe Komplexität):* Leichtgewichtige Komponente im Bento-System.
19. **Aufwand mit Begründung:** **M** (ca. 3 Entwicklertage).
20. **Risiken:** Entstehung von psychologischem Druck; muss strikt wohlwollend gestaltet sein.
21. **Wartungsaufwand:** Gering.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante B in Phase 3** als optionale Bento-Karte umsetzen.
24. **Geeignete Entwicklungsphase:** Phase 3.
25. **Konkrete Akzeptanzkriterien:** Ein Klick auf den Tagespunkt hakt die Gewohnheit ab; Historie der letzten 7 Tage bleibt sichtbar.
26. **Erforderliche Inhaberfreigabe:** **Ja.**

---

### [M11] Erweiterte Energie- und Belastungsplanung

1. **Fragestellung:** Soll Glide Aufgaben mit einem Energielevel (z. B. `Hoch`, `Mittel`, `Niedrig` oder `Fokus` vs. `Routine`) versehen können, um Aufgaben passend zur tageszeitlichen Leistungsfähigkeit auszuwählen?
2. **Konkrete Problemstellung:** Am Nachmittag im „Tief“ fehlen oft leichte Aufgaben; Nutzer überfordern sich, indem sie schwere analytische Aufgaben in unpassende Zeitfenster legen.
3. **Bestehende Inhaberentscheidung:** Bisherige Filterung läuft über Prioritäten (P1–P4) und Labels; keine feste Energie-Eigenschaft.
4. **Tatsächlich vorhandene Funktionalität:** Flexible Labels mit Farbakzenten (`labels.py`).
5. **Relevante Marktbeobachtung:** Sunsama und Things 3 nutzen Tags wie `#low-energy`; spezialisierte ADHS-Planer heben Energielevels hervor.
6. **Erwarteter Nutzermehrwert:** Ergonomischere Arbeitsverteilung: Bei Erschöpfung mit einem Klick alle Aufgaben filtern, die wenig mentale Energie kosten.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo / Empfohlen):* Nutzung des vorhandenen Label-Systems. Bereitstellung von Standard-Labels (`⚡ Hoch`, `☕ Niedrig`) in den mitgelieferten Vorlagen ohne neues Datenbankfeld.
   - *Variante B:* Einführung eines festen Attributs `energy_level` im Datenmodell mit speziellem Filter im Aufgabeninspektor.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Keine bei Variante A; Schemaerweiterung bei Variante B.
10. **Betroffene Quellmodule:** `src/glide/labels.py`, Vorlagenkatalog.
11. **Auswirkungen auf die Benutzeroberfläche:** Schnellfilterleiste um Energie-Schaltflächen erweitern.
12. **Datenschutz:** Vollständig lokal.
13. **Sicherheit:** Keine.
14. **Plattformfolgen:** Keine.
15. **Datenformatfolgen:** Keine bei Variante A (Aufgabenformat 26 bleibt absolut stabil).
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Optionale Metrik auf der Startseite.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Filterung nach Leistungsfähigkeit über bekannte Farblabels.
    - *P2 (Form folgt Funktion):* Aufgaben bleiben Aufgaben; Energietags sind freiwillige Kennzeichnungen.
    - *P3 (Keine Funktion doppelt):* Nutzt das bestehende, mächtige Label-System (`labels.py`) ohne neues Datenfeld.
    - *P4 (Kein Platz verschwenden):* Keine separaten Eingabefelder im Aufgabeninspektor.
    - *P5 (Nur das Wesentliche):* Schützt vor Schema-Aufblähung in Format 26.
    - *P6 (Geringe Komplexität):* Null zusätzliche Persistenzlogik oder Migrationen nötig.
19. **Aufwand mit Begründung:** **S** für Variante A (ca. 1 Entwicklertag für Vorlagenpflege und Filterhilfe).
20. **Risiken:** Überfrachtung von Aufgabenmasken durch zu viele Pflichtfelder; Variante A hält die Eingabe freiwillig.
21. **Wartungsaufwand:** Minimal.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A in Phase 2.** Das bestehende, mächtige Label-System reicht völlig aus und vermeidet Schemabrüche.
24. **Geeignete Entwicklungsphase:** Phase 2.
25. **Konkrete Akzeptanzkriterien:** Vorlagen enthalten Standardlabels; Filter nach Energielevel funktioniert verzögerungsfrei.
26. **Erforderliche Inhaberfreigabe:** **Nein (Vorlagenpraxis).**

---

### [M12] Work-in-Progress (WIP) Grenzen für Spalten und Heute-Ansicht

1. **Fragestellung:** Soll Glide eine Begrenzung der maximal gleichzeitig in Arbeit befindlichen Aufgaben (WIP-Limits, z. B. maximal 3 Aufgaben in der Heute-Ansicht oder Kanban-Spalte „In Arbeit“) unterstützen?
2. **Konkrete Problemstellung:** Nutzer überladen ihre Tagesliste mit 15 Aufgaben und verzetteln sich durch ständiges Multitasking.
3. **Bestehende Inhaberentscheidung:** Überlastungswarnung existiert im Entlastungsdialog (D81) basierend auf Gesamtminuten, nicht auf reiner Aufgabenanzahl.
4. **Tatsächlich vorhandene Funktionalität:** Tageskapazitätsbalken und Zeitaufwandssummen (`day_planner.py`).
5. **Relevante Marktbeobachtung:** Kanban-Methodik schreibt WIP-Limits zwingend vor; Trello und Super Productivity bieten zählbare Begrenzungen.
6. **Erwarteter Nutzermehrwert:** Fördert echtes Single-Tasking und erfolgreichen Abschluss („Stop starting, start finishing“).
7. **Lösungsvarianten:**
   - *Variante A (Status Quo):* Reine Information über Stundenkapazität ohne Deckelung der Stückzahl.
   - *Variante B (Empfohlen):* Sanfte, wohlwollende Warnung (Soft Limit): Überschreitet die Anzahl der offenen Aufgaben in „Heute“ einen Schwellenwert (Standard: 5 Aufgaben), färbt sich der Zähler dezent bernsteinfarben mit dem Hinweis: „Fokus-Tipp: Mehr als 5 Aufgaben führen selten zum Abschluss.“ Kein harter Block.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** `day_planner.py`.
10. **Betroffene Quellmodule:** `src/glide/today_view.py`, `src/glide/board_view.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** Dezenter Zählerhinweis `(4/5)`.
12. **Datenschutz:** Vollständig lokal.
13. **Sicherheit:** Keine.
14. **Plattformfolgen:** Keine.
15. **Datenformatfolgen:** Einstellungsformat 2: Optionales Limit in Benutzereinstellungen.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Bento-Metrik `BentoMetric` kann Auslastungsfarbe anpassen.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Sanfte visuelle Tönung warnt vor Zersplitterung ohne harte Blockaden.
    - *P2 (Form folgt Funktion):* Zahl der aktiven Aufgaben spiegelt mentale Kapazität wider.
    - *P3 (Keine Funktion doppelt):* Ergänzt den zeitbasierten Entlastungsdialog um stückzahlbasierte Heuristik.
    - *P4 (Kein Platz verschwenden):* Dezente Zählererweiterung im bestehenden Spaltenkopf `(4/5)`.
    - *P5 (Nur das Wesentliche):* Keine zeitraubenden Konfigurationsdialoge; einfache Obergrenze.
    - *P6 (Geringe Komplexität):* Reine Zählerprüfung im View-Rendering.
19. **Aufwand mit Begründung:** **S** (ca. 1 Entwicklertag).
20. **Risiken:** Bevormundung des Nutzers; darf niemals das Anlegen weiterer Aufgaben blockieren.
21. **Wartungsaufwand:** Minimal.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante B in Phase 2** als sanfte visuelle Unterstützung einführen.
24. **Geeignete Entwicklungsphase:** Phase 2.
25. **Konkrete Akzeptanzkriterien:** Überschreitung färbt Zähler sanft ein, blockiert jedoch keine Aktionen.
26. **Erforderliche Inhaberfreigabe:** **Nein.**

---

### [M13] Erweiterte Pixel-Werkstatt & SVG-Export

1. **Fragestellung:** Soll die integrierte Pixel-Werkstatt um Vektorisierung, SVG-Export und den Export animierter GIF-Stempel erweitert werden?
2. **Konkrete Problemstellung:** In der Pixel-Werkstatt erstellte Kunstwerke und Reisestempel können bisher nur als internes Format oder Cover-Miniatur genutzt werden; ein Export für Webseiten, Markdown-Dateien oder Präsentationen fehlt.
3. **Bestehende Inhaberentscheidung:** Pixel-Werkstatt ist ein integraler, kreativer Bestandteil von Glide (D100, V1.80 Showcase).
4. **Tatsächlich vorhandene Funktionalität:** Raster-Editor, Farbpaletten, Stempelanimationen und Miniatur-Eckcover (`pixel_workshop.py`, `pixel_cover.py`).
5. **Relevante Marktbeobachtung:** Pixel-Art-Tools (Aseprite) bieten GIF- und Spritesheet-Export; Vektor-Tools exportieren SVG.
6. **Erwarteter Nutzermehrwert:** Nutzer können ihre kreativen Stempel und Projekt-Icons in anderen Anwendungen und im Web weiterverwenden.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo):* Stempel verbleiben ausschließlich innerhalb der Glide-Oberfläche.
   - *Variante B (Empfohlen):* Exportfunktion `Datei › Zeichnung exportieren …` mit zwei Formaten: 1. Hochauflösendes PNG (skaliert ohne Kantenglättung / Nearest Neighbor) und 2. Echtes animiertes GIF (unter Nutzung der Standardbibliothek bzw. reiner Python-Byte-Generierung ohne externe Binaries).
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Standard-Python `struct` zur GIF/PNG-Bilderzeugung (bereits in `logo.py` bewährt); keine C-Bibliotheken erforderlich.
10. **Betroffene Quellmodule:** `src/glide/pixel_workshop.py`, `src/glide/drawing_export.py` (neu/Tk-frei).
11. **Auswirkungen auf die Benutzeroberfläche:** Neuer Menüpunkt „Exportieren als Bild …“ im Werkstattmenü.
12. **Datenschutz:** Vollständig lokal.
13. **Sicherheit:** Keine.
14. **Plattformfolgen:** Plattformübergreifend identisch.
15. **Datenformatfolgen:** Keine.
16. **Auswirkungen auf Glide Shell:** Keine.
17. **Auswirkungen auf Glide Bento:** Bento-Karten können exportierte PNGs als Header-Illustrationen laden.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Gezeichnete Stempel und Icons lassen sich sofort als PNG/GIF exportieren.
    - *P2 (Form folgt Funktion):* Pixel-Art wird pixelgenau ohne Unschärfe skaliert.
    - *P3 (Keine Funktion doppelt):* Nutzt den internen Canvas-Puffer direkt für den Byte-Export.
    - *P4 (Kein Platz verschwenden):* Export-Dialog öffnet sich nur auf Nutzerbefehl.
    - *P5 (Nur das Wesentliche):* Standardformate PNG und animiertes GIF statt überkomplexer Vektorisierer.
    - *P6 (Geringe Komplexität):* Reiner Python-Byte-Encoder ohne externe Grafikbibliotheken.
19. **Aufwand mit Begründung:** **M** (ca. 2–3 Entwicklertage für reinen Python-GIF/PNG-Encoder und Speicherdialog).
20. **Risiken:** Keine; bewährte Tk-freie Auslagerung.
21. **Wartungsaufwand:** Gering.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante B in Phase 3** umsetzen. Starkes Differenzierungsmerkmal gegenüber sterilen Standard-To-Do-Apps.
24. **Geeignete Entwicklungsphase:** Phase 3.
25. **Konkrete Akzeptanzkriterien:** Exportiertes GIF lässt sich in jedem Webbrowser abspielen; Pixel bleiben gestochen scharf.
26. **Erforderliche Inhaberfreigabe:** **Ja.**

---

### [M14] Lokales Plugin-System (Post-1.0-Architektur)

1. **Fragestellung:** Soll Glide eine Plugin-Schnittstelle erhalten, über die externe Python-Entwickler eigene Bento-Karten, Ansichten oder Importfilter nachrüsten können?
2. **Konkrete Problemstellung:** Power User und Entwickler haben spezifische Anforderungen (z. B. Spezialformate, Nischen-Hardware, individuelle Themes), die den Glide-Kern überfrachten würden.
3. **Bestehende Inhaberentscheidung:** Glide Shell (0.6.2) und Bento Box System (0.1.0) sind als modulare Pakete entworfen, aber für die Kernanwendung fest integriert; kein dynamisches Laden von Drittcode zur Laufzeit.
4. **Tatsächlich vorhandene Funktionalität:** Feste Modulstruktur mit sauberer Schichtenarchitektur (Ebene A -> B -> C -> D).
5. **Relevante Marktbeobachtung:** Obsidians Erfolg basiert maßgeblich auf seinem Community-Plugin-Ökosystem; birgt jedoch enorme Stabilitäts- und Sicherheitsrisiken.
6. **Erwarteter Nutzermehrwert:** Nahezu unbegrenzte Erweiterbarkeit bei schlankem Kern.
7. **Lösungsvarianten:**
   - *Variante A (Status Quo / Empfohlen):* Vorerst kein Plugin-System. Stattdessen Konzentration auf die Härtung von Bento Box System und Framework Shell für Schwesterprojekte (STEPS, Chess & Chains). Erweiterungen erfolgen über Pull Requests im Haupt-Repository.
   - *Variante B:* Formales lokales Plugin-Verzeichnis (`~/.glide/plugins/`), aus dem beim Start deklarierte Bento-Karten geladen werden.
8. **Option, den bisherigen Stand beizubehalten (Status Quo):** Siehe Variante A.
9. **Technische Abhängigkeiten:** Dynamischer Python-Import (`importlib`), Sicherheits-Sandbox, API-Stabilitätsgarantien.
10. **Betroffene Quellmodule:** `src/glide/app.pyw`, `src/glide/glide_bento/context.py`.
11. **Auswirkungen auf die Benutzeroberfläche:** Plugin-Verwaltungsdialog mit Aktivieren/Deaktivieren-Schaltern.
12. **Datenschutz:** Drittcode könnte heimlich Daten ins Internet senden (enormes Sicherheitsrisiko!).
13. **Sicherheit:** **Höchstes Sicherheitsrisiko:** Ausführung beliebigen Python-Codes von Drittanbietern bricht Glides Offline- und Datenschutzversprechen.
14. **Plattformfolgen:** Komplexe Fehlerdiagnose bei Plugin-Abstürzen.
15. **Datenformatfolgen:** Gefahr von Datenkorruption bei fehlerhaften Plugin-Schreiboperationen.
16. **Auswirkungen auf Glide Shell:** Hohe Architekturkomplexität.
17. **Auswirkungen auf Glide Bento:** Ermöglicht externe BentoCard-Registrierungen.
18. **Auswirkungen auf Gestaltungsprinzipien P1–P6:**
    - *P1 (Funktioniert selbstverständlich):* Die Anwendung läuft absolut stabil ohne abstürzende Dritt-Plugins.
    - *P2 (Form folgt Funktion):* Klare Architektur mit 4 definierten Ebenen (A, B, C, D) statt offener Laufzeit-Mutation.
    - *P3 (Keine Funktion doppelt):* Framework-Shell und Bento-System werden im Repository gepflegt, nicht fragmentiert.
    - *P4 (Kein Platz verschwenden):* Keine Plugin-Stores, Download-Manager oder Update-Benachrichtigungen im UI.
    - *P5 (Nur das Wesentliche):* Bewahrt Glides Kern als verlässliches Monolith-Werkzeug.
    - *P6 (Geringe Komplexität):* Verhindert API-Fragmentierung, Sandbox-Komplexität und Sicherheitslücken.
19. **Aufwand mit Begründung:** **XL** (mindestens 15 Entwicklertage für sichere API, Fehlerisolierung und Berechtigungsarchitektur).
20. **Risiken:** Fragmentierung des Projekts, Supportaufwand durch abstürzende Plugins Dritter, Verlust des Vertrauens in die Datensicherheit.
21. **Wartungsaufwand:** Extrem hoch.
22. **Mögliche Kosten:** 0 €.
23. **Begründete Empfehlung:** **Variante A (Vorerst strikte Zurückstellung).** Glide 1.0 muss erst als monolithisch verlässlicher, stabiler Arbeitsplatz reifen. Ein Plugin-System ist frühestens für Version 2.0 denkbar.
24. **Geeignete Entwicklungsphase:** Zurückgestellt auf Version 2.0+.
25. **Konkrete Akzeptanzkriterien:** Kern bleibt frei von dynamischem Drittcode-Import.
26. **Erforderliche Inhaberfreigabe:** **Ja (Architektur-Grundsatzentscheidung).**

---

### M15 – Rechtschreibprüfung (EDITOR-02, Master-Serie Teil 03, 27.11.2026)

1. **Ausgangslage:** Tk-Textfelder haben keine Rechtschreibprüfung; das Betriebssystem prüft sie nicht mit. Seit Shell 0.8.0 gibt es den Vertrag `glide_shell.spellcheck` (Wortgrenzen ohne URLs, E-Mail, Pfade und Code, unbekannte Wörter, Vorschläge, Ignorieren, persönliches Wörterbuch) ohne eigene Engine. Er ist in der Komponenten-Galerie vorgeführt, in Glide aber nicht aktiv.
2. **Varianten:**

| Variante | Engine | Lizenz (Stand 27.11.2026, vor Einbau nochmals am Paket prüfen) | DE/EN | Offline | Paketfolgen | Risiken |
|---|---|---|---|---|---|---|
| **A – systemeigen** | macOS `NSSpellChecker` über PyObjC (`pyobjc-framework-Cocoa`, MIT); Windows `ISpellChecker` (ab Windows 8) über `ctypes`/COM ohne Zusatzpaket oder `comtypes` (MIT); Linux: Hunspell-Wörterbücher des Systems mit `spylls` (MPL-2.0) | Engines frei; Wörterbücher gehören dem System, Glide liefert keine | je installierte Systemsprache | ja | macOS + PyObjC-Teilpaket, Windows ohne/mit kleinem Zusatz, Linux + `spylls` | drei Adapter; Vorschlagsqualität je System verschieden; COM-Aufrufe im Hauptthread kurz halten |
| B – `spylls` überall + mitgelieferte Wörterbücher | reines Python (MPL-2.0) | deutsches `igerman98`: GPL-2.0/GPL-3.0 bzw. OASIS-Lizenz (nur für ODF-Programme), Angaben je Paket widersprüchlich | DE/EN | ja | +5–10 MB Wörterbücher | Lizenzlage des deutschen Wörterbuchs, langsamer als C-Hunspell |
| C – `pyenchant` | Enchant (LGPL-2.1+ mit Ausnahme) | Windows-Wheels bündeln Enchant; macOS braucht Homebrew-Enchant | DE/EN je Provider | ja | Fremdbibliothek, auf dem Mac nicht selbstständig | Paketbau macOS, LGPL-Pflichten |
| D – Cloud/KI-Dienst | – | – | – | **nein** | – | widerspricht Produktgrenze „ohne Internet“; ausgeschlossen |

3. **Kosten:** 0 € Lizenzkosten; Aufwand Variante A etwa 3–5 Tage (drei Adapter, Hintergrundprüfung nach Eingabepause, Kontextmenü, Einstellungen, Tests je Plattform).
4. **Empfehlung:** **Variante A.** Keine Wörterbuchlizenz im Glide-Paket, Sprache und Qualität wie im übrigen System, offline. Die Prüfung läuft verzögert nach einer Eingabepause und nur für geänderte Bereiche (`misspelled(..., ranges=...)`). URLs, Code und Bezeichner sind ausgenommen. Das persönliche Wörterbuch liegt im Datenordner.
5. **Akzeptanz:** Markierung ohne spürbare Eingabeverzögerung (Median < 16 ms je Prüfschritt bei 10.000 Zeichen); Vorschläge im Kontextmenü; Ignorieren und Hinzufügen; DE/EN wählbar, Standard Oberflächensprache; abschaltbar; Formatierung und Blockart bleiben bei Korrekturen erhalten; Rückgängig.
6. **Erforderliche Inhaberfreigabe:** **Ja** (neue Laufzeitabhängigkeit PyObjC auf macOS bzw. `spylls` unter Linux nach AGENTS-Regel 4).

Quellen: [spylls (PyPI)](https://pypi.org/project/spylls), [spylls (GitHub)](https://github.com/zverok/spylls), [igerman98 – Debian-Copyright](https://metadata.ftp-master.debian.org/changelogs/main/i/igerman98/stable_hunspell-de-de.copyright), [pyenchant – Installation](https://pyenchant.github.io/pyenchant/install.html), [pyenchant (PyPI)](https://pypi.org/project/PyEnchant).
