"""Einmaliger, nachvollziehbarer Dokumentationsnachlauf vom 18.10.2026."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[5]
AUDIT = Path(__file__).resolve().parent
CHANGES = []


def write(rel, old, new, reason):
    p = ROOT / rel
    assert p.read_text(encoding="utf-8") == old, rel
    if old == new:
        return
    CHANGES.append(dict(pfad=rel, grund=reason, vorher_bytes=len(old.encode()),
                        nachher_bytes=len(new.encode()),
                        vorher_sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    p.write_bytes(new.encode())
    CHANGES[-1]["nachher_sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()


def section(s, prefix, transform):
    heads = list(re.finditer(r"(?m)^#{1,3} .+$", s))
    hit = [(i, m) for i, m in enumerate(heads) if m.group().startswith(prefix)]
    assert len(hit) == 1, (prefix, len(hit))
    i, m = hit[0]
    end = heads[i+1].start() if i+1 < len(heads) else len(s)
    return s[:m.start()] + transform(s[m.start():end]) + s[end:]


def plan():
    rel = '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md'
    old = (ROOT/rel).read_text(encoding='utf-8'); s = old
    def history(chunk):
        table = re.search(r'(?m)^\|.*(?:\n\|.*)+', chunk).group()
        return chunk.splitlines()[0] + '\n\n' + (
            '**Historischer Umfang nach D44 vom 10.10.2026.** Die folgende Tabelle bewahrt die bestätigten Aufgaben und ihre Reihenfolge. Der aktuelle Fortgang steht in §18–§20.\n\n'
        ) + table + '\n\n' + (
            'Pakete 1–7 wurden als 3.36.0–3.42.0 geliefert; FP-00 lag als 3.39.1 vor Paket 5. Das nach D50 vorgezogene UI-/UX-Paket folgte als Python-Lieferung 3.43.0/3.43.1. Paket 8 ist weiterhin nicht geliefert. Seine Vorbereitung einschließlich GUI10 und SIG11 bleibt im [historischen Nachweis](../01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md) nachvollziehbar.\n\n'
            'Die wiederholten Liefergeschichten sind hier zusammengeführt; Einzelwerte und damalige Grenzen bleiben in den QA-Nachweisen und der Git-Historie erhalten. FP-01 und WA-27–WA-30 sind inzwischen im lokalen Prüfkandidaten integriert (§18.3). Das ist keine neue Lieferung nach 07 und kein Abschluss der offenen Phasenentscheidungen.\n\n'
        )
    s = section(s, '### 15.7 ', history)
    s = section(s, '### 15.8 ', lambda c: c.splitlines()[0]+'\n\n'+
        'D44, D50 und D51 bestimmen den Fortgang: gezielte Prüfungen während einer Phase, eingefrorene Vollprüfung und Lieferung am bestätigten Phasenende. Die vorgeschlagenen Gesamtphasen bleiben entscheidungspflichtig. D17/P05, D35/D42 und die Datenformat-Tore gelten weiter; Format 24/25 erfordern Altleser- und Sicherungsprüfungen. D45 ist erfüllt.\n\n'+
        'I6 und N12 bleiben menschliche Abnahmen. D43 sowie I1–I5/I9–I11 werden mit ihren eigenen Nachweisen geprüft. Automatisierte Prüfungen ersetzen weder native Sicht-/Screenreaderabnahme noch Freigabe einer neuen Lieferung.\n\n'+
        'Vor jedem Commit läuft die CI-Grundstufe. Der Auftrag vom 18.10. umfasst Bestandsprüfung, Zusammenführung, Bereinigung, Validierung sowie Commit und Pull Request; der Pull Request wird nicht automatisch zusammengeführt. Temporäre Arbeitskopien dürfen nach Sicherung und Abgleich entfallen, ihre Branches und Sicherungen bleiben erhalten.\n\n')
    proof='[Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md)'
    rows={
      'WA-27 / A32':f'| **WA-27 / A32** Bestandswächter auch bei 20 Undo-Schritten | Prüfkandidat umgesetzt | I integriert; P gezielte Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `structural_guard.py` sichert den Vorzustand unabhängig von der Stapeltiefe; fehlende IDs werden vor dem Schreiben erkannt. Später Abbruch stellt Originalbytes wieder her; Speicherfehler führen zu einer zutreffenden Fehlermeldung. | Voller Stapel, Savefehler, bytegleiche Datei nach Abbruch und Undo/Redo geprüft; {proof}. |',
      'WA-28 / A34':f'| **WA-28 / A34** gültige Datei bei Darstellungsfehler behalten | Prüfkandidat umgesetzt | I integriert; P gezielte Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `load_phases.py` trennt Lesen/Normalisierung vom UI-Aufbau. Ein Darstellungsfehler klassifiziert gültiges JSON nicht als beschädigte Datei; Schreibschutz und Bestand bleiben geschützt. | Gültige Datei mit UI-Fehler, ungültiges JSON und zukünftiges Format geprüft; {proof}. |',
      'WA-29 / A35':f'| **WA-29 / A35** vor Kontextwechsel zuverlässig speichern | Prüfkandidat umgesetzt | I integriert; P echte Aufrufer und Fehlerfälle grün; L noch nicht nach 07 geliefert; M native Abnahme offen | `editor_flush.py` vereinheitlicht den True/False-Vertrag. Kontextwechsel und Ausgaben warten auf tatsächliche Übernahme; ein Dirty-Kennzeichen allein reicht nicht. Unveränderte übernommene Inhalte bleiben schreibgeschützt exportierbar. | Navigation, Anlegen, Ausgabe, Notion/Restore und beide Editoren geprüft; {proof}. |',
      'WA-30 / A36':f'| **WA-30 / A36** Datensperre ohne Fail-open | Prüfkandidat umgesetzt | I integriert; P L1/L2/L3/L4/L5 und Prozessproben grün; L noch nicht nach 07 geliefert; M Cloud-Abgleich offen | `data_lock.py` nutzt exklusive Anlage und einen lokalen OS-Mutex für Übernahmen alter Sperren. Beschädigte Sperren bleiben schreibgeschützt bis zur bewussten Übernahme; alle Schreibwege einschließlich Einstellungen und Beenden verwenden die gemeinsame Schranke. Kein verteiltes Cloud-Lock. | Fehlende/verdrängte Sperre, Einstellungen, Beenden und sechs synchronisierte Prozesspaare geprüft; {proof}. |'
    }
    for key,row in rows.items():
        s,n=re.subn(r'(?m)^\| \*\*'+re.escape(key)+r'\*\*.*$',lambda m:row,s); assert n==1,(key,n)
    s=re.sub(r'(?m)^\| Umsetzungsstand \| \*\*Upstream-Kandidat.*$',
        '| Umsetzungsstand | **Lokaler Prüfkandidat auf FP-01-Stand:** PR #36 / `9ec474b` ist integriert; Version 3.43.1, Format 25. Wiederholen mit neun Fällen einschließlich 10.001 Aufgaben sowie A33 erneut grün. Die früheren Messwerte und 57 Bereichssuiten bleiben im [FP-01-Nachweis](../01_Repository/Glide/tests/qa-3.43.1/fp01_wiederholen_2026-10-17/README.md) historisch erhalten. 07 und Pakete enthalten den Kandidaten noch nicht; eingefrorener Phasenabschluss und native Abnahmen bleiben offen. |',s)
    s=re.sub(r'(?m)^\*\*Schutzrunde WA-27/28/29.*$',
        '**Schutzrunde WA-27/28/29 und WA-30:** im lokalen Prüfkandidaten auf FP-01 integriert. Zehn Schutzfälle sind grün; dieselben zehn Gegenproben sind auf der ursprünglichen FP-01-Basis rot. Kein neues Datenformat, keine Lieferung nach 07. D51-Phasenabschluss und native/menschliche Abnahmen bleiben eigene offene Tore.',s)
    s=s.replace('**notwendige Schutzrunde vor Breitphase**','**Schutzrunde vor Breitphase: Kandidat umgesetzt**')
    ids=lambda x:set(re.findall(r'\b(?:[A-Z]{1,3}\d{1,3}|[A-Z]{1,4}-\d{1,3})\b',x))
    assert not ids(old)-ids(s),sorted(ids(old)-ids(s))
    assert re.findall(r'(?m)^#{1,4} .+$',old)==re.findall(r'(?m)^#{1,4} .+$',s)
    write(rel,old,s,'Historien zusammengeführt; alle Aufgaben-IDs und Überschriften erhalten; aktueller Prüfkandidat und Liefergrenzen abgeglichen.')


if __name__=='__main__':
    plan()
    (AUDIT/'dokumentaenderungen.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(CHANGES,ensure_ascii=False,indent=2))
