# SPDX-License-Identifier: MPL-2.0
"""Einmalige Karte „Neu in …“ nach einem Update, ohne Tk (N07 seit 3.33.20).

Der Katalog nennt je Version höchstens fünf Neuerungen in einem Satz. Nach dem
ersten Start ohne Vorgängerversion erscheint nichts: Ein Einstieg für neue
Nutzer ist bewusst nicht gewählt (N06). „Gelesen“ merkt die Version lokal.

Seit B18 (15.10.2026) liest „Hilfe › Über Glide › Neuerungen“ denselben
Katalog: Was auf der Startseite weggeklickt wurde, bleibt dort nachlesbar.
Pflege je Version: siehe docs/10_VEROEFFENTLICHUNG.md („Neuerungen“). Der
Katalog ist keine Kopie des technischen CHANGELOG; Versionen ohne Eintrag
bleiben ohne Eintrag, nachträglich wird nichts erfunden.

Seit der menschlichen Abnahme vom 07.11.2026 (D66) zeigt die Karte höchstens
die drei neuesten Versionen mit Eintrag (`CARD_VERSIONS`); „Gelesen“ bleibt so
ohne langes Scrollen erreichbar. Ältere Einträge stehen weiter vollständig in
„Hilfe › Über Glide › Neuerungen“.
"""

# Je Version höchstens fünf Sätze; neueste Version oben. Eine Version ohne
# Eintrag zeigt keine Karte.
CATALOG = {
    "3.55.1": (
        "Beim Entlasten eines Tages wählst du die Aufgaben und den neuen Bearbeitungstag und bestätigst mit „Umplanen“.",
        "Der JSON-Canvas-Export funktioniert wieder und schlägt wie die App-Sicherung einen Dateinamen mit einfacher Endung vor.",
    ),
    "3.55.0": (
        "Die Tagesbilanz zeigt Aufgabenaufwand, belegte Kalenderzeit, verbleibende Kapazität und Überlastungsgründe.",
        "Aufgaben ohne Schätzung bleiben sichtbar. Im Entlastungsdialog siehst du, welche Fälligkeiten beim Umplanen erhalten bleiben.",
    ),
    "3.54.0": (
        "Fundorte anzeigen nennt alle Verwendungen einer Aufgabe, Seite, Notiz, Liste oder Zeichnung mit direktem Sprung.",
        "Pinnwände lassen sich als offene JSON-Canvas-1.0-Datei (.canvas) mit Karten, Bereichen, Verbindungen und Verlustbericht exportieren.",
        "Auswahlkästchen, Radioschalter, Listenfelder und Schieberegler sind vollständig in das Glide-Design integriert.",
    ),
    "3.52.0": (
        "Schriftstile: Modern Rubik, Technisch DM Mono, Kreativ DM Serif Display, Klassisch Charis SIL; gespeicherte Stile bleiben erhalten.",
        "Schriftgewicht und Schriftgröße lassen sich getrennt einstellen. Kreativ und Klassisch sind automatisch kräftiger.",
        "Hinzufügen und weitere Hervorhebungen folgen der gewählten Themenfarbe. Löschen bleibt rot und Bestätigen grün.",
        "Das Kopflogo ist etwas größer und sitzt zwei Pixel weiter rechts.",
        "DejaVu Sans bleibt intern für UI-Symbole, die die auswählbaren Schriften nicht enthalten.",
    ),
    "3.51.0": (
        "Die Plus-Knöpfe der Seitenleiste zeigen ihre Fläche beim Überfahren und den Fokus bei Tastaturbedienung.",
        "Seitenleistenzähler haben mehr Platz zur rechten Kante. Die Windows-Menüs sind flacher und die Kopfsymbole auf den Titel abgestimmt.",
    ),
    "3.50.7": (
        "Glide verbindet Projekte, Aufgaben, Tagesplanung, Pinnwände und Pixel-Zeichnungen als Desktop-Planer.",
        "Über Glide zeigt die Produktbeschreibung, die MPL-2.0-Lizenz und den Bezug zum Quellcode.",
        "Die separate Python-Fassung enthält den vollständigen Lizenztext und Hinweise zur Weitergabe.",
        "Die Seitenleiste passt ihre Zeilenhöhe an die gewählte Schrift an und behält ihre Gestaltung auch nach einem Neustart.",
    ),
    "3.50.6": (
        "Seiten zeigen ihren Titel nur noch im Kopf in der Themenfarbe; darunter steht jede Ansicht mit einer Unterzeile.",
        "Titelfelder zählen die freien Zeichen herunter, zu lange Anhangsnamen werden vor dem Speichern gekürzt.",
        "Die Pinnwand hat eine einzige Leistenzeile, Auswahlfelder zeigen ihren Text vollständig.",
        "Rücktaste im Textfeld löscht keinen markierten Punkt mehr, und Bereiche hinterlassen beim Schließen keine Lücke.",
        "Erledigte und offene Punkte beginnen an derselben Kante; die Neuerungen zeigen höchstens drei Versionen.",
    ),
    "3.50.5": (
        "Buttons kürzen lange Beschriftungen mit drei Punkten; der vollständige Text bleibt im Tooltip.",
        "Neue und geänderte Aufgabentitel sind wie Seiten-, Listen- und Ordnertitel auf 40 Zeichen begrenzt.",
        "Notizen und Zeichnungen bündeln Journalaktionen im Mehr-Menü und geben mehr Platz an den Inhalt zurück.",
        "Die Startseite bietet ein Feld für die globale Suche, Vorlagen einen eigenen Suchfilter.",
        "Die schmale Heute-Leiste und die Abstände innerhalb der Seitenleistenabschnitte sind kompakter.",
    ),
    "3.50.4": (
        "Bücher nutzen ihre ganze Breite auch mit schmaler oder ausgeblendeter Seitenleiste.",
        "Glide verwendet die überarbeitete G-Form und neue lila/gelbe App-Symbole.",
        "Gelbe Hinweise im Darkmode erscheinen einheitlich im neuen Markengelb.",
    ),
    "3.50.3": (
        "Seiten- und Zeichenwerkzeuge bleiben einzeilig; weitere Aktionen sind im jeweiligen Menü erreichbar.",
        "Aufgabenaktionen sind dauerhaft sichtbar; Labels und Bücher nutzen die verfügbare Breite ohne leere Aktionsreserve.",
        "Fristen in Tabellen bleiben vollständig lesbar; Eingabe, Suche und Seitenfuß erhalten passende Abstände.",
        "Die Zellmarkierung der Zeichnung erscheint bei Tastaturbedienung und verschwindet bei Mausbedienung.",
    ),
    "3.50.2": (
        "Seitenleiste und Inhalt behalten ihre helle oder dunkle Themenfarbe; die gewählte Hintergrundfarbe liegt dahinter.",
        "Schriftstile: Modern: Rubik, Technisch: Roboto Mono, Kreativ: Playfair Display und Klassisch: Fraunces.",
        "Playfair Display und Fraunces mit kräftigerer Grundschrift; fette und kursive Hervorhebungen bleiben verfügbar.",
        "Die Kopfzeile bleibt beim Wechsel zu Heute stabil; die Inhaltsfläche erhält ihren vorgesehenen Platz.",
    ),
    "3.50.0": (
        "Erster öffentlicher Stand: Aufgaben, Seiten, Notizen, Pinnwände und Pixel-Werkstatt lokal nutzen; vier Schriftstile mit Rubik als Vorgabe.",
        "Hintergrundfarbe unabhängig vom Design wählen; „Wie die Fensterfläche“ verbindet die Flächen ohne Materialschatten.",
        "Volle Seitenleiste, Kopf auf Inhaltsflucht; Seitenblöcke am Sechspunktgriff ziehen und per Rechtsklick formatieren.",
        "Nebenansicht: Treffer und Abschnitte ansteuern, letzte Suchen aufrufen und markierten Text nachschlagen.",
        "Fokusintervalle wählen, um fünf Minuten verlängern und zur nächsten Aufgabe wechseln; große Bestände schneller speichern.",
    ),
    "3.49.0": (
        "Startseite: über Woche direkt einen Tag der betrachteten, vorherigen oder nächsten Woche wählen.",
        "Ausgewählte Tagesaufgaben gemeinsam in Fälligkeit und Aufwand ändern, mit einem Rückgängig-Schritt.",
        "Nebenansicht: Verweise kopieren, Ziele im Hauptbereich öffnen und Inhalte gezielt verknüpfen.",
        "Nach ungeklärtem Programmende bleibt der Bestand bis zur bewussten Freigabe mit Originalvorsicherung geschützt.",
        "Lokale Start- und Abschlussprotokolle dokumentieren Betriebsphasen ohne Aufgabeninhalte.",
    ),
    "3.48.0": (
        "Startseite: zwischen Tagen wechseln oder ein Datum wählen und den passenden Tagesplan öffnen.",
        "Planung, freie Zeit und Fälligkeiten bleiben für den angezeigten Tag getrennt nachvollziehbar.",
        "Ausgewählte Tagesaufgaben gemeinsam priorisieren und eigene Labels hinzufügen oder entfernen.",
        "Interne Textlinks in der Nebenansicht öffnen weitere Inhalte, ohne die Hauptarbeit zu wechseln.",
        "Verweise und Rückverweise in der Nebenansicht durchsuchen und mit dem Verlauf zurückkehren.",
    ),
    "3.47.0": (
        "Startseite: mehrere Tagesaufgaben auswählen und gemeinsam planen oder den Bearbeitungstag entfernen.",
        "Die Auswahl bleibt über Vorschauseiten erhalten; Alle auswählen umfasst alle offenen Tagesaufgaben.",
        "Gemeinsame Planung mit Kapazitätsvorschau, unveränderter Fälligkeit und einem Rückgängig-Schritt.",
        "Nebenansicht: Zurück und Vorwärts, auch mit Alt+Pfeil, stellen Suche und Leseposition wieder her.",
        "Verlauf zeigt besuchte Inhalte mit aktuellen Titeln und bietet den direkten Inhaltswechsel.",
    ),
    "3.46.0": (
        "Startseite: Tagesaufgaben direkt abhaken; die Vorschau zeigt fünf wirklich offene Aufgaben.",
        "Mehr an jeder Tagesaufgabe: mit Kapazitätsvorschau einplanen, umplanen oder den Bearbeitungstag entfernen.",
        "Nächste Aufgabe: Fokus und Planung direkt starten; der Tagesvorschlag ist auf der Startseite erreichbar.",
        "Nebenansicht: Inhalt durchsuchen, Treffer markieren und mit Enter oder Umschalt+Enter wechseln.",
        "Über Abschnitte zu Überschriften oder Aufgabengruppen springen, während die Hauptarbeit offen bleibt.",
    ),
    "3.45.0": (
        "Kompaktmodus direkt oben im Menü Ansicht; Nebenansicht und durchsuchbare Seiten- und Blockaktionen.",
        "Speicherstatus mit getrennten Fehlermeldungen, Erneut speichern und Sicherungsreserve.",
        "Sicherungsübersicht: Dateien suchen, Größen sehen, Inhalte lesen, vergleichen und gezielt wiederherstellen.",
        "Ausführbare Anhänge öffnen erst nach Rückfrage; Windows-Bildvorschauen vertragen ungewöhnliche Dateinamen.",
    ),
    "3.44.0": (
        "Wiederholen: Strg/Cmd+Umschalt+Z, unter Windows auch Strg+Y, nimmt ein Rückgängig zurück.",
        "Eigene Rhythmen: mehrere Wochentage, n-ter Wochentag, Monatsende, Pause und begrenzte Anzahl.",
        "Gespeicherte Ansichten mit mehr Bedingungen, als Liste, Tabelle oder Spaltenboard, gruppiert und sortiert.",
        "Seiten und Notizen als Pinnwandkarten; unverknüpfte Erwähnungen zeigen vergessene Bezüge.",
        "Alles als Markdown-Ordner exportieren; fünf fertige KI-Aufträge mit vollständiger Vorschau.",
    ),
    "3.43.0": (
        "Startseite: neue Kachel Galeriebilder, „Startseite anpassen“ links, nach „Gelesen“ sofort oben.",
        "Gismo heißt fest Gismo und spielt immer mit; wer ihn nicht möchte, blendet seine Kachel aus.",
        "Ruhigere Kopfzeile mit Lupe zum Suchen, ohne Datum und „?“; Bedienhinweise über die Einstellungen.",
        "Titel haben mehr Platz, Knöpfe werden nicht mehr überdeckt, Seiten mit Bildern scrollen gleichmäßig.",
        "Diese Neuerungen bleiben unter Hilfe › Über Glide nachlesbar.",
    ),
    "3.36.0": (
        "Startseite und geänderte Bibliothekskarten werden schneller aktualisiert.",
        "Die Einstellungen öffnen schneller und verwerfen ungespeicherte Eingaben weiterhin beim Abbrechen.",
    ),
    "3.33.19": (
        "Schneller: Seiten mit vielen Bildern, die Startseite und das Einstellungsfenster reagieren zügiger.",
        "Weniger Schreibvorgänge je Aktion – gespeichert wird weiterhin sofort.",
    ),
    "3.33.20": (
        "Wiederholungen: „Diesen Termin überspringen“ und „Verpasste Termine überspringen“ im Kontextmenü.",
        "Erinnerung gleich beim Erfassen: „erinnere 9 Uhr“ oder „Erinnerung 30 min vorher“.",
        "Mehrere Zeilen in die Eingabezeile einfügen legt auf Wunsch je Zeile eine Aufgabe an.",
        "„+“ legt an, Umschalt+Enter öffnet die erweiterte Eingabe; zuletzt benutzte Listen und Labels stehen vorn.",
        "Routinen: wiederkehrende Checklisten auf Wunsch als eigener Abschnitt in „Heute“.",
    ),
    "3.33.21": (
        "Hell oder dunkel wie das System: Einstellungen › Darstellung und Bedienung.",
        "Schmale Seitenleiste mit Symbolen: Ansicht › Seitenleiste schmal.",
        "Die Pinnwand braucht nur noch eine Werkzeugzeile; Seltenes steht unter „…“.",
        "Seiten zeigen ihren Titel groß und in leerem Zustand einen Schreibhinweis.",
        "Ruhigere Farben: Lila nur noch für Hinzufügen, eingeschaltete Schalter neutral.",
    ),
    "3.34.0": (
        "Bilder in Seiten überlappen nicht mehr; Drucken und PDF zeigen sie mit.",
        "Markdown mit Bildern: kopieren, speichern und wieder als Seite öffnen.",
        "Die Suche markiert Fundstellen in der geöffneten Seite.",
        "Gespeicherte Filter erklären, warum ein Punkt erscheint oder fehlt.",
        "Alt+Pfeile ordnen auch Seiten, Notizen und Zeichnungen in der Seitenleiste.",
    ),
    "3.35.0": (
        "Eine KI kann vorhandene Aufgaben überarbeiten: Kontextpaket hin, Vorschlag geprüft zurück.",
        "Sicherungen vergleichen zeigt, was sich zwischen zwei Ständen geändert hat.",
        "Pixel-Werkstatt: Farbe ändern mit Vorschau – Doppelklick auf die Farbleiste.",
        "Vor dem Symbolexport zeigt Glide 16, 32 und 48 Pixel auf hellem und dunklem Grund.",
    ),
}
# Bestand ohne gemerkte Version stammt aus der Zeit vor dieser Karte.
BEFORE_CATALOG = "3.33.18"
# Die Karte „Neu in …“ zeigt höchstens so viele Versionen (D66, 07.11.2026).
CARD_VERSIONS = 3


def version_tuple(text):
    """„3.33.20“ → (3, 33, 20); Unlesbares → None."""
    teile = str(text or "").strip().split(".")
    if not teile or not all(teil.isdigit() for teil in teile):
        return None
    return tuple(int(teil) for teil in teile)


def notes_since(last_seen, current, catalog=None):
    """Neuerungen der Versionen nach `last_seen` bis einschließlich `current`.

    Ohne gemerkte Version (erster Start) oder bei gleicher bzw. neuerer
    gemerkter Version: leer. Neueste Version zuerst, höchstens fünf Punkte je
    Version und höchstens `CARD_VERSIONS` Versionen; ältere Einträge bleiben
    über `history` nachlesbar.
    """
    katalog = CATALOG if catalog is None else catalog
    alt, neu = version_tuple(last_seen), version_tuple(current)
    if alt is None or neu is None or alt >= neu:
        return []
    treffer = []
    for version, punkte in katalog.items():
        stand = version_tuple(version)
        if stand is not None and alt < stand <= neu and punkte:
            treffer.append((stand, version, list(punkte)[:5]))
    neueste = sorted(treffer, reverse=True)[:CARD_VERSIONS]
    return [(version, punkte) for _stand, version, punkte in neueste]


def normalize_seen(value):
    """Gemerkte Version als Text oder None, wenn sie nicht lesbar ist."""
    return value.strip() if isinstance(value, str) and version_tuple(value) is not None else None


def last_seen(settings, existing_install):
    """Gemerkte Version; ohne sie bei vorhandenem Bestand die Version vor dem Katalog."""
    gemerkt = (settings or {}).get("release_notes_seen")
    if isinstance(gemerkt, str) and version_tuple(gemerkt) is not None:
        return gemerkt
    return BEFORE_CATALOG if existing_install else None


def should_show(settings, current, catalog=None, existing_install=False):
    """True, wenn die Karte für `current` noch nicht gelesen ist und etwas zeigt."""
    return bool(notes_since(last_seen(settings, existing_install), current, catalog))


def remember_seen(settings, current):
    """Neue Einstellungen mit gemerkter Version; Original bleibt unverändert."""
    neu = dict(settings or {})
    neu["release_notes_seen"] = str(current)
    return neu


def history(current, catalog=None):
    """Alle Neuerungen bis einschließlich `current`, neueste Version zuerst."""
    katalog = CATALOG if catalog is None else catalog
    neu = version_tuple(current)
    treffer = []
    for version, punkte in katalog.items():
        stand = version_tuple(version)
        if stand is not None and punkte and (neu is None or stand <= neu):
            treffer.append((stand, version, list(punkte)[:5]))
    return [(version, punkte) for _stand, version, punkte in sorted(treffer, reverse=True)]


def history_text(current, catalog=None):
    """Lesbarer Text für „Über Glide › Neuerungen“."""
    eintraege = history(current, catalog)
    if not eintraege:
        return "Für diese Version sind keine Neuerungen hinterlegt."
    abschnitte = []
    for version, punkte in eintraege:
        abschnitte.append(f"Version {version}\n" + "\n".join(f"• {punkt}" for punkt in punkte))
    return "\n\n".join(abschnitte)
