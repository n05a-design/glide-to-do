"""Optische Höhe von Symbolen neben Text, ohne Tk (B09, 15.10.2026).

Tk setzt jedes Zeichen nach Schriftmetrik, nicht nach seiner sichtbaren Form:
Ein Dreieck steht dadurch tiefer, das Wiederverwertungszeichen höher als die
Mitte des Textes daneben. Dieses Modul liest die Begrenzungsrahmen der
Glyphen direkt aus einer TrueType-Datei (cmap, loca, glyf, OS/2) und rechnet,
wie weit die sichtbare Mitte eines Symbols von der Mitte der
Großbuchstabenhöhe abweicht. Die Oberfläche verschiebt das Symbol um diesen
Betrag – eine Regel für alle Symbole statt einzelner Pixelversätze.

Nur Standardbibliothek; keine Schriftbibliothek, kein Rendern.
"""

import struct

__all__ = ["FontMetrics", "load", "optical_shift"]


class FontMetrics:
    """Begrenzungsrahmen je Zeichen und die Großbuchstabenhöhe einer Schriftdatei."""

    def __init__(self, data):
        tabellen = self._tables(data)
        kopf = tabellen.get(b"head")
        if kopf is None or b"glyf" not in tabellen or b"loca" not in tabellen or b"cmap" not in tabellen:
            raise ValueError("Keine TrueType-Schrift mit glyf-Umrissen")
        self.units_per_em = struct.unpack(">H", data[kopf + 18:kopf + 20])[0]
        lang = struct.unpack(">h", data[kopf + 50:kopf + 52])[0] == 1
        anzahl = struct.unpack(">H", data[tabellen[b"maxp"] + 4:tabellen[b"maxp"] + 6])[0]
        self._data = data
        self._glyf = tabellen[b"glyf"]
        self._loca = self._read_loca(data, tabellen[b"loca"], anzahl, lang)
        self._cmap = self._read_cmap(data, tabellen[b"cmap"])
        self.cap_height = self._cap_height(data, tabellen.get(b"OS/2"))

    # --- Tabellen -------------------------------------------------------
    @staticmethod
    def _tables(data):
        anzahl = struct.unpack(">H", data[4:6])[0]
        result = {}
        for index in range(anzahl):
            tag, _summe, offset, _laenge = struct.unpack(">4sIII", data[12 + 16 * index:28 + 16 * index])
            result[tag] = offset
        return result

    @staticmethod
    def _read_loca(data, offset, anzahl, lang):
        if lang:
            return struct.unpack(f">{anzahl + 1}I", data[offset:offset + 4 * (anzahl + 1)])
        return tuple(2 * wert for wert in struct.unpack(f">{anzahl + 1}H", data[offset:offset + 2 * (anzahl + 1)]))

    @staticmethod
    def _read_cmap(data, offset):
        zuordnung = {}
        teile = struct.unpack(">H", data[offset + 2:offset + 4])[0]
        for index in range(teile):
            _plattform, _kodierung, start = struct.unpack(">HHI", data[offset + 4 + 8 * index:offset + 12 + 8 * index])
            tabelle = offset + start
            art = struct.unpack(">H", data[tabelle:tabelle + 2])[0]
            if art == 4:
                segmente = struct.unpack(">H", data[tabelle + 6:tabelle + 8])[0] // 2
                ende = tabelle + 14
                anfang = ende + 2 * segmente + 2
                delta = anfang + 2 * segmente
                bereich = delta + 2 * segmente
                for s in range(segmente):
                    bis = struct.unpack(">H", data[ende + 2 * s:ende + 2 * s + 2])[0]
                    von = struct.unpack(">H", data[anfang + 2 * s:anfang + 2 * s + 2])[0]
                    versatz = struct.unpack(">h", data[delta + 2 * s:delta + 2 * s + 2])[0]
                    sprung = struct.unpack(">H", data[bereich + 2 * s:bereich + 2 * s + 2])[0]
                    for zeichen in range(von, bis + 1):
                        if zeichen == 0xFFFF or zeichen in zuordnung:
                            continue
                        if sprung == 0:
                            glyphe = (zeichen + versatz) & 0xFFFF
                        else:
                            stelle = bereich + 2 * s + sprung + 2 * (zeichen - von)
                            glyphe = struct.unpack(">H", data[stelle:stelle + 2])[0]
                            if glyphe:
                                glyphe = (glyphe + versatz) & 0xFFFF
                        if glyphe:
                            zuordnung[zeichen] = glyphe
            elif art == 12:
                gruppen = struct.unpack(">I", data[tabelle + 12:tabelle + 16])[0]
                for g in range(gruppen):
                    von, bis, erste = struct.unpack(">III", data[tabelle + 16 + 12 * g:tabelle + 28 + 12 * g])
                    for zeichen in range(von, bis + 1):
                        zuordnung.setdefault(zeichen, erste + zeichen - von)
        return zuordnung

    def _cap_height(self, data, os2):
        if os2 is not None and struct.unpack(">H", data[os2:os2 + 2])[0] >= 2:
            wert = struct.unpack(">h", data[os2 + 88:os2 + 90])[0]
            if wert > 0:
                return wert
        rahmen = self.bbox("H")
        return rahmen[3] if rahmen else round(self.units_per_em * 0.7)

    # --- Abfragen -------------------------------------------------------
    def covers(self, char):
        return ord(char) in self._cmap

    def bbox(self, char):
        """(xMin, yMin, xMax, yMax) in Schrifteinheiten, oder None ohne Umriss."""
        glyphe = self._cmap.get(ord(char))
        if glyphe is None or glyphe + 1 >= len(self._loca):
            return None
        start, ende = self._loca[glyphe], self._loca[glyphe + 1]
        if ende <= start:
            return None
        stelle = self._glyf + start
        return struct.unpack(">hhhh", self._data[stelle + 2:stelle + 10])

    def ink_center(self, text):
        """Senkrechte Mitte der sichtbaren Form über der Grundlinie, in Em.

        Mehrzeichige Symbole wie ``⚑⚑`` (hohe Wichtigkeit) zählen mit der
        gemeinsamen Höhe aller Zeichen mit Umriss; Leerzeichen bleiben außen vor.
        """
        rahmen = [box for box in map(self.bbox, str(text)) if box is not None]
        if not rahmen:
            return None
        unten = min(box[1] for box in rahmen)
        oben = max(box[3] for box in rahmen)
        return (unten + oben) / 2 / self.units_per_em

    def cap_center(self):
        """Mitte der Großbuchstabenhöhe über der Grundlinie, in Em."""
        return self.cap_height / 2 / self.units_per_em


def load(path):
    """Liest eine Schriftdatei; eine beschädigte Datei meldet ValueError."""
    with open(path, "rb") as datei:
        data = datei.read()
    try:
        return FontMetrics(data)
    except (struct.error, IndexError, KeyError) as fehler:
        raise ValueError(f"Schriftdatei nicht lesbar: {fehler}") from fehler


def relative_shift(metrics, symbol, reference, px):
    """Pixel nach unten (positiv), damit `symbol` mittig steht wie `reference`.

    Für Symbole, die Tk in derselben Schrift und Zeile setzt (Baumzeilen):
    Ausgerichtet wird an der Bezugsform der übrigen Symbole.
    """
    eigen = metrics.ink_center(symbol) if metrics is not None else None
    bezug = metrics.ink_center(reference) if metrics is not None else None
    if eigen is None or bezug is None:
        return 0
    return round((eigen - bezug) * px)


def label_center_for_cap(text_baseline, text_metrics, text_px, symbol_metrics, symbol, symbol_px,
                         symbol_ascent, symbol_linespace):
    """Zeilenmitte eines Symbol-Labels, bei der die Symbolmitte auf der Großbuchstabenmitte liegt.

    Alle Werte in Pixeln; `text_baseline` ist die Grundlinie des Textes im
    gemeinsamen Elternrahmen. Tk zentriert den Text eines Labels senkrecht:
    Grundlinie = Zeilenmitte − Zeilenhöhe/2 + Oberlänge.
    """
    ziel = text_baseline - text_metrics.cap_center() * text_px
    mitte = symbol_metrics.ink_center(symbol) if symbol_metrics is not None else None
    if mitte is None:
        return None
    return ziel + mitte * symbol_px + symbol_linespace / 2 - symbol_ascent


def optical_shift(symbol_metrics, symbol, symbol_px, text_metrics, text_px, baseline_gap=0.0):
    """Pixel, um die das Symbol nach unten (positiv) bzw. oben rücken muss.

    Ziel: Die sichtbare Mitte des Symbols liegt auf der Mitte der
    Großbuchstabenhöhe des Textes. `baseline_gap` ist, wie weit die Grundlinie
    des Symbols bei unverschobenem Satz tiefer liegt als die des Textes (px).
    Unbekannte Zeichen verschieben nichts.
    """
    mitte = symbol_metrics.ink_center(symbol) if symbol_metrics is not None else None
    if mitte is None or text_metrics is None:
        return 0
    symbol_mitte = baseline_gap - mitte * symbol_px
    text_mitte = -text_metrics.cap_center() * text_px
    return round(text_mitte - symbol_mitte)
