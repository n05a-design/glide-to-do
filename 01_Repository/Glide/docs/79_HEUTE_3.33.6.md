# Glide 3.33.6 – Heute und Demnächst (D14)

Stand 02.10.2026 · Glide 3.33.6 · Aufgabenformat 20

Auftrag vom 02.10.2026 („einfach weiterarbeiten“ nach der Feature-Folge des Entwicklungsplans). Grundlage ist D14 in der [Arbeitsrichtung](ARBEITSRICHTUNG.md) und U06 in der [UX-Prüfung](../../../00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md): zwei Hauptansichten statt sich überlappender Wege. Interne Kennungen (`planday`, `in_progress`, Einstellungsschlüssel) bleiben; keine Datenformatänderung, keine neue Abhängigkeit.

## Bedienvertrag

**Heute** (bisher „Mein Tag“) zeigt am heutigen Tag von oben nach unten:

| Abschnitt | Inhalt |
|---|---|
| Nächste Aufgabe | genau eine Aufgabe nach `task_urgency_rank` – heute eingeplant, sonst überfällig oder heute fällig, sonst liegen geblieben; dieselbe Aufgabe wie die Startseitenkachel |
| Verspätet | offene Aufgaben mit vergangener Fälligkeit, die nicht für heute eingeplant sind |
| Liegen geblieben | an einem früheren Tag eingeplant, noch offen, nicht überfällig |
| Tagesplan (bzw. Zeitplan/Ohne Uhrzeit) | was über den Bearbeitungstag für heute eingeplant ist |
| Heute fällig | offene Aufgaben mit Fälligkeit heute, die nicht eingeplant sind – auch aus dem Eingang |
| Verweis „Demnächst · N weitere Fälligkeiten“ | Doppelklick oder Return öffnet „Demnächst“ |
| Eingang | Punkte des Eingangs ohne Bearbeitungstag |

- **Jede Aufgabe steht genau einmal.** Eingeplantes bleibt im Tagesplan, auch wenn es überfällig ist; die nächste Aufgabe wird aus ihrem Abschnitt herausgenommen; ein heute fälliger Eingangspunkt steht unter „Heute fällig“, nicht im Eingang.
- **Künftige Fälligkeiten** stehen nicht mehr in der Tagesansicht (bis 3.33.5 als Abschnitt „In Bearbeitung“), sondern in „Demnächst“; der Verweis am Ende ersetzt den Weg dorthin.
- Der Tagesplan bekommt eine Überschrift, sobald über ihm ein Abschnitt steht; ohne solche Abschnitte bleibt er flach wie bisher. Mit Uhrzeiten gelten Zeitplan und Stundenraster unverändert.
- **Andere Tage** (◀/▶): Titel „Tagesplan · Wochentag, Datum“, Abschnitte Tagesplan und „An diesem Tag fällig“ sowie der Eingang; keine nächste Aufgabe, kein Verspätet.
- **Tagesbeginn und Tagesabschluss** sind Modi von „Heute“: Schalter „Tag …“ in der Filterzeile und Einträge im Kontextmenü der Seitenleistenzeile; die Wege über „Ansicht › Ansichten“ und die Schnellsuche bleiben.
- Die Zahl hinter „Heute“ in der Seitenleiste zählt alle Aufgaben, die „Heute“ ohne Filter zeigt (ohne Eingang) – auch wenn gerade ein anderer Tag offen ist.
- Abschnitte lassen sich wie bisher zuklappen; der Zustand übersteht den Neustart. Die entfallene Kennung `planinprogress:heading` wird beim Laden verworfen.

**Demnächst** (bisher „In Bearbeitung“) zeigt alle Aufgaben mit Fälligkeit chronologisch; Überfälliges steht oben unter „Verspätet“, der Rest unter „Noch offen“. Die nächste Aufgabe steht nicht mehr hier, sondern in „Heute“; „Nächste Aufgabe“ in Menü und Startseite führt dorthin. „Demnächst“ hat bewusst keine Seitenleistenzeile (U06); erreichbar über den Verweis in „Heute“, „Ansicht › Ansichten“, die Schnellsuche und die Startseite.

**Umbenennungen:** Seitenleiste, Fenstertitel, Menüs und Befehlspalette („Heute: Tag zurück/vor/Stundenraster ein/aus“), Startseitenknöpfe, Schnellaktionen, Startansicht-Auswahl, Kalenderausgabe-Umfang, Tageszettel („Tagesplan“), Handbuch, Kontextmenü („Für heute einplanen“, „Auswahl für heute ergänzen“, „Aus dem heutigen Tagesplan nehmen“) und Hinweistexte. `/meintag` bleibt als Eingabebefehl erhalten.

Die Fachlogik ist Tk-frei in `today_view.py` (D17): Einordnung je Aufgabe, Aufteilung ohne Dubletten, nächste Aufgabe mit Stufengrenze, Zählung für den Verweis. Sechs Unit-Tests mit festem Stichtag. In `app.pyw` liefern `today_view_pool` und `plan_day_sections` die Daten; `refresh_task_overview`, `open_next_task`, `count_today_view` und `plan_day_title` nutzen sie. Entfallen sind `plan_in_progress_entries`, `next_task_entry` und `PLAN_IN_PROGRESS_ROW_ID`.

## Prüfung

Neue Pflichtsuite `test_heute3336.py` über echte Wege: Auswahl der Seitenleistenzeile; sechs Abschnitte plus Verweis in fester Reihenfolge; nächste Aufgabe gleich Startseite; keine Dubletten, nichts Künftiges oder Erledigtes; Verweis öffnet „Demnächst“; Doppelklick auf neue Überschriften; Zuklappen über Neuladen, alte Kennung verworfen; „Tag …“ sichtbar, Klick auf „Tagesbeginn …“ startet den Modus; Kontextmenü der Seitenleistenzeile; anderer Tag; „Demnächst“ chronologisch ohne nächste Aufgabe; „Nächste Aufgabe“ aus der Startseite; Palette, Schnellsuche, Startansicht, Handbuch, Kontextmenü einer Liste.

Angepasste Altsuiten (frühere Verträge, jetzt durch D14 ersetzt): `test_glide`, `test_features312`, `test_features315`, `test_features317`, `test_features324`, `test_features325`, `test_rueckmeldung330`.

Angepasst wurde außerdem `test_speicherlast330`: Es prüft den Hinweis zur Formatumstellung jetzt zeitunabhängig (vorgemerkt oder bereits gezeigt). Anlass war ein Zeitrennen unter hoher Systemlast im zweiten Prüflauf, kein Fehler der App.

## Abschluss 02.10.2026

[Nachweis](../tests/qa-3.33.6/heute_2026-10-02/README.md), [Vollprotokoll](../tests/qa-3.33.6/heute_2026-10-02/vollpruefung/ergebnis.json), [Quellstand](../tests/qa-3.33.6/heute_2026-10-02/quellstand.json), [Lieferabgleich](../tests/qa-3.33.6/heute_2026-10-02/auslieferung.json).

- **Vollprüfung Exitcode 0** (dritter Lauf, 17:27–18:25, ohne Eingaben): 81 Schritte, alle 64 Integrationssuiten, Unit-Tests, Showcase und fünf Analysen; Quellstand (342 Dateien) unverändert. Zwei ungültige Vorläufe sind im Nachweis belegt: gesperrter Bildschirm und das oben genannte Zeitrennen.
- **Auslieferung:** `abgleich_07.py` ohne Abweichung (3.33.5-Hauptdatei als `_Z` archiviert), Bundle neu gebaut; 146 Dateien in `07_Python-Versionen` und 60 im Bundle per SHA-256 gleich `src/glide`; Bundle 3.33.6, `de.shaye.glide`, Signatur gültig. Showcase ausgeliefert.
- **Manuell offen:** „Heute“ und „Tag …“ mit echter Tastatur und Maus, Windows/Linux, DPI und Screenreader.
