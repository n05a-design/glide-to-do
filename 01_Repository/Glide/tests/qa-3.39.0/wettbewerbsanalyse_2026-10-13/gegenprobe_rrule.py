"""Unabhängige Gegenrechnung zu `ics_recurrence.dates` (Nachweis 13.10.2026, kein Teil der App).

Referenz: Tag-für-Tag-Abtastung nach RFC 5545 §3.3.10, eigenständig geschrieben
(kein Code aus `ics_recurrence`). Vergleicht zufällige, von `parse_rule` akzeptierte
Regeln über rund drei Jahre; DTSTART wird auf den ersten zur Regel passenden Tag gelegt.
Ausgenommen und gezählt: UNTIL vor DTSTART (Auslegungsfrage, Glide liefert dann keinen Termin).

Aufruf aus `01_Repository/Glide`:
    python3 -B -I tests/qa-3.39.0/wettbewerbsanalyse_2026-10-13/gegenprobe_rrule.py src/glide 4000 1
Nur Standardbibliothek, keine Schreibzugriffe; Ausgabe JSON auf stdout.
"""
import calendar
import json
import random
import sys
from datetime import date, timedelta

sys.path.insert(0, sys.argv[1])
import ics_recurrence as ir  # noqa: E402

TAGE = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def wochenanfang(tag, wkst):
    return tag - timedelta(days=(tag.weekday() - wkst) % 7)


def periode_index(tag, start, regel):
    f = regel.frequency
    if f == "DAILY":
        return (tag - start).days
    if f == "WEEKLY":
        return (wochenanfang(tag, regel.week_start) - wochenanfang(start, regel.week_start)).days // 7
    if f == "MONTHLY":
        return (tag.year * 12 + tag.month) - (start.year * 12 + start.month)
    return tag.year - start.year


def periodentage(tag, regel):
    f = regel.frequency
    if f == "DAILY":
        return [tag]
    if f == "WEEKLY":
        a = wochenanfang(tag, regel.week_start)
        return [a + timedelta(days=i) for i in range(7)]
    if f == "MONTHLY":
        n = calendar.monthrange(tag.year, tag.month)[1]
        return [date(tag.year, tag.month, i) for i in range(1, n + 1)]
    erster = date(tag.year, 1, 1)
    return [erster + timedelta(days=i) for i in range(366 if calendar.isleap(tag.year) else 365)]


def ordinal_passt(tag, ordinal, bezug_jahr):
    if bezug_jahr:
        alle = [d for d in (date(tag.year, 1, 1) + timedelta(days=i)
                            for i in range(366 if calendar.isleap(tag.year) else 365)) if d.weekday() == tag.weekday()]
    else:
        n = calendar.monthrange(tag.year, tag.month)[1]
        alle = [date(tag.year, tag.month, i) for i in range(1, n + 1)
                if date(tag.year, tag.month, i).weekday() == tag.weekday()]
    pos = alle.index(tag)
    return (ordinal > 0 and pos == ordinal - 1) or (ordinal < 0 and pos == len(alle) + ordinal)


def im_satz(tag, start, regel):
    f = regel.frequency
    if regel.months and tag.month not in regel.months:
        return False
    if regel.monthdays:
        n = calendar.monthrange(tag.year, tag.month)[1]
        erlaubt = set()
        for wert in regel.monthdays:
            erlaubt.add(wert if wert > 0 else n + wert + 1)
        if tag.day not in erlaubt:
            return False
    if regel.weekdays:
        treffer = False
        for ordinal, wtag in regel.weekdays:
            if tag.weekday() != wtag:
                continue
            if ordinal is None or ordinal_passt(tag, ordinal, f == "YEARLY" and not regel.months):
                treffer = True
        if not treffer:
            return False
    # Ergänzung aus DTSTART, wenn kein passender BY-Teil die Periode füllt.
    if f == "WEEKLY" and not regel.weekdays and tag.weekday() != start.weekday():
        return False
    if f == "MONTHLY" and not regel.monthdays and not regel.weekdays and tag.day != start.day:
        return False
    if f == "YEARLY" and not regel.monthdays and not regel.weekdays:
        if tag.day != start.day:
            return False
        if not regel.months and tag.month != start.month:
            return False
    return True


def referenz(start, regel, bis):
    ergebnis = [start]
    if regel.count == 1:
        return ergebnis
    ende = bis
    if regel.until:
        u = date(int(regel.until[:4]), int(regel.until[4:6]), int(regel.until[6:8]))
        ende = min(ende, u)
    perioden = {}
    tag = start + timedelta(days=1)
    while tag <= ende:
        idx = periode_index(tag, start, regel)
        if idx % regel.interval == 0:
            schluessel = (idx,)
            if schluessel not in perioden:
                kandidaten = [d for d in periodentage(tag, regel) if im_satz(d, start, regel)]
                if regel.positions:
                    gewaehlt = set()
                    for p in regel.positions:
                        if abs(p) <= len(kandidaten):
                            gewaehlt.add(kandidaten[p - 1] if p > 0 else kandidaten[p])
                    kandidaten = sorted(gewaehlt)
                perioden[schluessel] = set(kandidaten)
            if tag in perioden[schluessel]:
                ergebnis.append(tag)
                if regel.count is not None and len(ergebnis) >= regel.count:
                    break
        tag += timedelta(days=1)
    return ergebnis


def zufallsregel(rnd):
    f = rnd.choice(["DAILY", "WEEKLY", "MONTHLY", "YEARLY"])
    teile = [f"FREQ={f}"]
    if rnd.random() < 0.6:
        teile.append(f"INTERVAL={rnd.choice([1, 2, 3, 4, 6])}")
    if f in ("MONTHLY", "YEARLY") and rnd.random() < 0.5:
        anz = rnd.choice([1, 1, 2])
        ws = []
        for _ in range(anz):
            o = rnd.choice(["", "", "1", "2", "3", "4", "-1", "-2"])
            ws.append(o + rnd.choice(TAGE))
        teile.append("BYDAY=" + ",".join(dict.fromkeys(ws)))
    elif f in ("WEEKLY", "DAILY") and rnd.random() < 0.5:
        teile.append("BYDAY=" + ",".join(rnd.sample(TAGE, rnd.choice([1, 2, 3, 5]))))
    if f in ("MONTHLY", "YEARLY") and rnd.random() < 0.3:
        teile.append("BYMONTHDAY=" + ",".join(str(x) for x in rnd.sample([1, 15, 28, 29, 30, 31, -1, -2], rnd.choice([1, 2]))))
    if f == "YEARLY" and rnd.random() < 0.4:
        teile.append("BYMONTH=" + ",".join(str(x) for x in rnd.sample(range(1, 13), rnd.choice([1, 2, 3]))))
    if rnd.random() < 0.2 and any(t.startswith(("BYDAY", "BYMONTHDAY", "BYMONTH")) for t in teile):
        teile.append("BYSETPOS=" + rnd.choice(["1", "-1", "2", "1,-1"]))
    r = rnd.random()
    if r < 0.25:
        teile.append(f"COUNT={rnd.randint(1, 30)}")
    elif r < 0.45:
        teile.append("UNTIL=2028%02d%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)))
    if rnd.random() < 0.15:
        teile.append("WKST=" + rnd.choice(["MO", "SU", "WE"]))
    return ";".join(teile)


def main():
    anzahl = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    rnd = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 20261013)
    feste_starts = [date(2026, 1, 31), date(2028, 2, 29), date(2026, 12, 31), date(2026, 3, 29), date(2026, 10, 25)]
    geprueft = abweichend = abgelehnt = start_unpassend = until_vor_start = 0
    beispiele = []
    for _ in range(anzahl):
        text = zufallsregel(rnd)
        try:
            regel = ir.parse_rule(text)
        except ir.RuleError:
            abgelehnt += 1
            continue
        start = rnd.choice(feste_starts) if rnd.random() < 0.3 else date(2026, 1, 1) + timedelta(days=rnd.randint(0, 900))
        # Erster passender Tag ab dem Zufallsstart, damit DTSTART zur Regel passt.
        versuch = 0
        while not ir.matches_start(start, regel) and versuch < 800:
            start += timedelta(days=1)
            versuch += 1
        if not ir.matches_start(start, regel):
            start_unpassend += 1
            continue
        if regel.until and regel.until[:8] < start.strftime("%Y%m%d"):
            until_vor_start += 1
            continue
        bis = start + timedelta(days=1100)
        glide = list(ir.dates(start, regel, bis))
        ref = referenz(start, regel, bis)
        geprueft += 1
        if glide != ref:
            abweichend += 1
            if len(beispiele) < 15:
                nur_glide = sorted(set(glide) - set(ref))[:5]
                nur_ref = sorted(set(ref) - set(glide))[:5]
                beispiele.append({"regel": text, "start": start.isoformat(),
                                  "nur_glide": [d.isoformat() for d in nur_glide],
                                  "nur_referenz": [d.isoformat() for d in nur_ref],
                                  "anzahl_glide": len(glide), "anzahl_referenz": len(ref)})
    print(json.dumps({"erzeugt": anzahl, "von_parse_rule_abgelehnt": abgelehnt,
                      "start_passt_nicht_zur_regel": start_unpassend, "until_vor_start_ausgenommen": until_vor_start, "verglichen": geprueft,
                      "abweichend": abweichend, "beispiele": beispiele}, ensure_ascii=False, indent=1))


main()
