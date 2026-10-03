# Heute und Demnächst 3.33.6 – Nachweis

02.10.2026 · App 3.33.6 · macOS, Python 3.14.5, Tk 9.0 · temporäres `GLIDE_DATA_DIR`, keine echten Nutzerdaten · [Funktionen, Heute](../../../docs/20_FUNKTIONEN.md#4-heute-demnächst-und-planung)

## Vollprüfung und Auslieferung

[Eingefrorener Quellstand](quellstand.json) mit 342 Dateien. [Vollprüfung](vollpruefung/ergebnis.json) im dritten Lauf 17:27–18:25, entsperrt, ohne Eingaben: **Exitcode 0**, 81 Schritte, zwei plattformbedingt übersprungen; Quellstand unverändert. [Lieferabgleich](auslieferung.json): 146 Dateien in `07_Python-Versionen` und 60 im Bundle per SHA-256 gleich `src/glide`, Bundle 3.33.6, Signatur gültig; Showcase ausgeliefert.

## Ungültige Vorläufe

**Erster Lauf (gesperrter Bildschirm):**

Erster Vollprüfungsstart 14:59: `test_ui39` (15:05) und `test_workspace310` rot, beide an einem per `event_generate` gesendeten Return, das ein Aufklappfeld nicht schloss. Zwischen 15:05:55 und 15:57:06 stand der Lauf still; danach liefen die Suiten wieder im Sekundentakt. Die letzte Eingabe am Mac lag um 16:08 rund elf Minuten zurück, der Bildschirm war wieder entsperrt – also Sperre von etwa 15:02 bis 15:57 mit Fokusverlust (bekanntes Muster aus 3.33.1). Lauf um 16:11 abgebrochen, Protokolle lokal aufbewahrt (nicht versioniert, sie enthalten Benutzerpfade); Quellstand unverändert; Wiederholung ab 16:12.

**Zweiter Lauf (16:12–17:09, Zeitrennen unter Last):** 80 von 81 Schritten grün; rot nur `test_speicherlast330` an der Stelle „Hinweis vorgemerkt“. Die App zeigt den Hinweis „Bestand umgestellt“ 700 ms nach dem Laden und löscht dabei die Vormerkung; die Suite prüfte die Vormerkung erst nach ihrem Leerlauf. Während des Laufs belegten OneDrive und `fileproviderd` zusammen über 200 % CPU (Synchronisierung der Fixture- und Archivdateien des Versionswechsels); `test_mindestgroesse330` brauchte 12½ statt rund 5 Minuten. Messung mit `reference_v17`, Laden plus Leerlauf, je sieben Durchgänge, abwechselnd: 3.33.5 Median 420/433 ms, 3.33.6 Median 430/431 ms; Seitenleiste 4,6–4,9 gegen 5,1–5,2 ms – D14 verlangsamt das Laden nicht. Korrektur nur in der Suite: vorgemerkt oder bereits gezeigt, beides zählt; danach muss die Meldung „Bestand umgestellt“ vorliegen. Einzellauf grün; Quellstand neu eingefroren, dritter Lauf ab 17:27.

## Gezielte Prüfungen

- Unit-Tests grün (61), davon sechs neue für `today_view.py`.
- `test_heute3336.py` grün; Gegenprobe mit dem ausgelieferten Stand 3.33.5: Exitcode 1 (Seitenleiste zeigt „Mein Tag“).
- Nacheinander statt parallel (Tastaturfokus), im Hintergrundmodus: `test_glide`, `test_features316`, `test_features320`, `test_features322`, `test_features323`, `test_features330`, `test_kartenfuss330`, `test_festlayout330`, `test_kontrast330`, `test_mindestgroesse330` (Schalter „Tag …“ bei Mindestgröße ohne Befund), `test_klappmechanismen3321`, `test_ui_polish36`, `test_seiten330`, `test_eingabe3333`, `test_startseite3332`, `audit_app`, `test_logo330`, `test_vollpruefung325` grün.
- Auf den Vertrag D14 gebracht und danach grün: `test_features312` (Titel „Heute · …“), `test_features315` (Titel „Tagesplan · …“ an anderen Tagen, Zahl der Seitenleiste gilt heute), `test_features317` (Tageszettel „Tagesplan“), `test_features324`/`test_features325`/`test_glide` („Demnächst“ ohne nächste Aufgabe; sie steht in „Heute“ und gleicht der Startseite), `test_rueckmeldung330` (Verweis auf „Demnächst“ statt Abschnitt „In Bearbeitung“). Im ersten Lauf von `test_rueckmeldung330` wählte die Anpassung die falsche Listenart (`list` statt `tasks`); korrigiert.
- Statische Analysen, Symbol-, Dubletten- und Attributprüfung ohne Abbruch.
