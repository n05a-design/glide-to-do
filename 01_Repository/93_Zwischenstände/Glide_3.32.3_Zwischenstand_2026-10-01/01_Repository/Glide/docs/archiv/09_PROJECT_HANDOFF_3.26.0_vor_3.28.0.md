# Projektübergabe – Glide 3.26.0

Stand 21.09.2026 · App 3.26.0 · Aufgabenformat 17 · Einstellungen 2 · Vorlagen 2

Kanonisch ist `src/glide/app.pyw`. Die startbare Kopie wird unter `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.26.0.pyw` im äußeren Projektordner mit denselben Ressourcen bereitgestellt. Der Ordner ist kein Git-Checkout. Originalstände sind archiviert.

## Umgesetzter Stand

Mein-Tag-Aufklappen, lesbare Pinnwandvorschau, Verbindungsbearbeitung, Ordnergrenzen, responsive Buttons und Formulare sind nachgebessert. Pinnwand-Lasso, optionale Ausrichtung mit Guides/Abständen, sechs Zoomstufen und Navigator sind vorhanden. Gismo hat Kontexttexte, Füttern, Hover-Reaktion und einen Schalter für Spielereien. Notizlisten verbinden sechs Aufgabenzeilen mit Rich Text samt Formatierung, Unicode, lokalem Undo/Redo und strukturiertem Austausch. Schema 17 sichert vor der ersten Migration die bisherige Datei. Verlauf ist über die Seitenleiste erreichbar und begrenzt auf 15 Einträge beziehungsweise 15 Tage. Import-/Export-/Backup-Aktionen werden erfasst. Das Handbuch lässt sich als HTML speichern und zum Drucken öffnen.

## Weiterarbeit und Prüfung

Den [QA-Bericht](07_QA_BERICHT.md) und die [Umsetzungsmatrix](decisions/Entscheidungen_3.26.0.md) zuerst lesen. Bereits erledigte Punkte nicht erneut als offen behandeln. Der [Windows-Gesamtlauf vom 21.09.2026](../tests/qa-3.26.0/abschluss_final_2026-09-21/ergebnis.json) hat Exitcode 0; seine 47 automatisierten Prüfschritte bestanden. Bei Quelländerungen GLIDE_DATA_DIR vor dem Import isolieren und die betroffenen Regressionen ausführen. Wiederholbarer Vollaufruf aus dem Repository: `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.26.0/<neuer-Ordner> --timeout 900`.

Benannte Pinnwandbereiche, echte Aufgabenabhängigkeiten und Pinnwand-Reisen sind fachlich offen. Der Konkurrenz-Backlog ist kein vollständig beauftragtes 3.26-Paket. Es liegen Lizenzentwurf, Vertriebs-/Markenrecherche-Vorbereitung und Signierungsanleitung vor; keine abgeschlossene Markenfreigabe, keine Signierung und keine Veröffentlichung.

