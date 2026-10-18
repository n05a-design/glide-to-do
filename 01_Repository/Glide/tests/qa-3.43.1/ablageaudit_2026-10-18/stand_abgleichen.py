"""Einmaliger Standabgleich; historische Messergebnisse bleiben erhalten."""
from pathlib import Path
import json
import re
from dokumente_aktualisieren import ROOT, AUDIT, CHANGES, write, section

CHANGES.extend(json.loads((AUDIT/'dokumentaenderungen.json').read_text(encoding='utf-8')))
Q='01_Repository/Glide/'
child=ROOT/'.claude/worktrees/jolly-noether-593099'
proof='../tests/qa-3.43.1/schutzrunde_2026-10-18/README.md'

for name in ['06_DATA_BACKUP_MIGRATION.md','20_FUNKTIONEN.md']:
    rel=Q+'docs/'+name; old=(ROOT/rel).read_text(encoding='utf-8')
    notice=('**Prüfkandidat vom 18.10.2026:** FP-01 und WA-27–WA-30 sind im Quellbaum integriert (Version 3.43.1, Format 25). '
            'Die zuvor nachgestellten Grenzen A32/A33/A34/A35/A36 haben gezielte Schutzprüfungen und Gegenproben; '
            'die historische Analyse beschreibt den Zustand vor dieser Integration. '
            f'[Schutznachweis]({proof}), [aktueller Prüf- und Lieferstand](07_QA_BERICHT.md). '
            '07 und die eigenständigen Pakete sind noch nicht auf diesen Kandidaten aktualisiert. Native Abnahmen und Phasenabschluss bleiben offen.')
    s,n=re.subn(r'(?m)^\*\*Abgleich der Fehlergrenzen am 18\.10\.2026:\*\*.*$',lambda m:notice,old);assert n==1
    if name.startswith('06'):
        newlock=next(x for x in (child/rel).read_text(encoding='utf-8').splitlines() if x.startswith('- `glide.lock` verhindert'))
        s,n=re.subn(r'(?m)^- `glide.lock` verhindert.*$',lambda m:newlock+' Die lokale OS-Sperre auf `glide.lock.acquire` schützt auch die Übernahme verwaister Sperren; sie ist kein verteilter Konsens zwischen Rechnern.',s);assert n==1
    else:
        s=s.replace('- **Papierkorb:**','- **Schutz vor nicht übernommenen Änderungen (WA-27–WA-30):** Umbauten bewahren ihren Vorzustand auch bei vollem Undo-Stapel; Darstellungsfehler machen gültige Dateien nicht zu beschädigten Dateien. Kontextwechsel und Ausgaben prüfen die tatsächliche Editorübernahme. Unveränderte, bereits übernommene Inhalte lassen sich auch schreibgeschützt exportieren; neue nicht übernommene Änderungen halten die Aktion an. Datensperren gelten für Aufgaben, Einstellungen, Vorlagen und Fensterzustand.\n- **Papierkorb:**',1)
    write(rel,old,s,'Aktuellen Schutzvertrag vom historischen Fehlerbefund und von der noch älteren Lieferung getrennt.')

rel=Q+'docs/02_ARCHITECTURE.md';old=(ROOT/rel).read_text(encoding='utf-8');s=old
cs=(child/rel).read_text(encoding='utf-8')
rows=[x.replace('in Arbeit (Schutzrunde)','Prüfkandidat 18.10.2026') for x in cs.splitlines() if any(x.startswith('| `'+mod+'`') for mod in ['structural_guard.py','load_phases.py','editor_flush.py','data_lock.py'])]
assert len(rows)==4
line=next(x for x in s.splitlines() if x.startswith('| `undo_history.py`'))
s=s.replace(line,line+'\n'+'\n'.join(rows),1)
bullets=[x for x in cs.splitlines() if x.startswith(('- **Editorübernahme (WA-29):**','- **Datensperre (WA-30):**'))]
assert len(bullets)==2
s=s.replace('## 3.', '## 3.',1) # Überschriften bleiben unverändert.
position=s.index('- **Editoren:**')
s=s[:position]+'\n'.join(bullets)+'\n'+s[position:]
s=re.sub(r'Die Analyse vom 18\.10\.2026 weist Grenzen[^\n]*',
         'Die Analyse vom 18.10.2026 bleibt als Vorzustand erhalten. WA-27–WA-30 und FP-01 sind im Prüfkandidaten gezielt geprüft; dies ist keine pauschale Verlustfreiheitsgarantie. `GuardTransaction` sichert Stapel und Originalbytes, prüft IDs vor dem Schreiben und wertet den Rückweg aus. `load_phases.py` trennt Lese- von Darstellungsfehlern. [Prüfgrenzen](07_QA_BERICHT.md).',s)
write(rel,old,s,'Vier Fachmodule, Editor- und Sperrverträge ergänzt; bestehende Ausnahmen an Mutationseinstiegen erhalten.')

rel=Q+'docs/07_QA_BERICHT.md';old=(ROOT/rel).read_text(encoding='utf-8');s=old
s=s.replace('lokale Python-Fassung, getrennter Upstream-FP-01-Kandidat und eigenständige Pakete 3.42.0','integrierter Prüfkandidat, getrennte Python-Lieferung und eigenständige Pakete 3.42.0',1)
s=s.replace('## Standanalyse und Dokumentationsnachlauf 18.10.2026','## Standanalyse und Dokumentationsnachlauf 18.10.2026\n\n**Historischer Vorzustand vor Integration:** Die folgenden Befunde und Ergebnisse beziehen sich auf `c0252ba` / App-Hash `ed2b7eb…`. Der spätere Kandidat und Ablagenachlauf stehen unter „Aktuelle Prüfstände“. Die alten Ergebnisdateien bleiben unverändert.',1)
s=section(s,'## Aktuelle Prüfstände',lambda c:'''## Aktuelle Prüfstände

Standabgleich vom 18.10.2026: gleiche Versionsnummer bedeutet nicht gleiche Dateien.

| Bereich | Tatsächlicher Stand und Grenze |
|---|---|
| Quellbaum | 3.43.1 / Format 25 auf `9ec474b` mit FP-01 und WA-27–WA-30; App-SHA-256 `f74af723e3fe1fc18aae5beafcef3d026a3a9c39d8eb16c90b68fb3ae7ddec26`; 72 eigene Laufzeitdateien, 94 Integrationssuiten. |
| Schutzrunde | Zehn Schutzfälle grün und zehn entsprechende Gegenproben auf der unveränderten FP-01-Basis rot; 754 Fachlogik- und 152 Werkzeugtests grün. Sechs betroffene bestehende Suiten erneut grün. [Kandidatenmanifest und Einzelbelege](../tests/qa-3.43.1/schutzrunde_2026-10-18/README.md). |
| Globale Ablage und Dokumentation | Vollinventar einschließlich Git und Arbeitskopien, Dateihashes, Dokumentregister, gesicherte Integration, Bereinigung und erneute Validierung: [Ablagenachweis](../tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Das Ergebnis dort führt die nach Integration tatsächlich wiederholten Prüfungen auf. |
| Python-Lieferung 07 | Weiterhin vorherige 3.43.1 / App-SHA-256 `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`; unverändert. Enthält weder den neuen FP-01- noch den Schutzkandidaten. |
| Windows-Paket | Weiterhin unsigniertes Entwicklungsartefakt 3.42.0; ursprünglicher Manifestabgleich 102/102. Keine neue Paketlieferung. |
| Mac-Bundle | Weiterhin 3.42.0; ursprünglicher Abgleich 327/330, drei Frameworkdateien fehlen. Kein aktueller Start-/Signaturnachweis. |
| Offene Tore | Eingefrorene Gesamtprüfung der bestätigten nächsten Produktionsphase, 07-/Paketlieferung, native Mac-/Reader- und menschliche Abnahmen. Weder dieser Ablagenachlauf noch ein Pull Request geben einen Release frei. |

Historische Messwerte und Lieferergebnisse bleiben in der folgenden Versionstabelle und ihren Originalnachweisen erhalten. Die wiederholten Erzählungen derselben Läufe wurden zusammengeführt; Aufgaben und offene Entscheidungen stehen ausschließlich im Entwicklungsplan.

''')
write(rel,old,s,'Doppelte Laufgeschichten durch aktuelle Standmatrix ersetzt; historische Versionstabelle und Rohbelege erhalten.')

rel='00_Arbeitsvorbereitung/Glide_Uebergabe.md';old=(ROOT/rel).read_text(encoding='utf-8')
table=re.search(r'(?m)^\| Thema.*(?:\n\|.*)+',old).group()
s='''# Glide – Übergabe an eine neue Sitzung

Stand 18.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · integrierter Prüfkandidat, noch keine neue Lieferung

## 1. Tatsächlicher Stand

Die Hauptarbeitskopie enthält FP-01 aus `origin/main` / `9ec474b` und die geprüfte Schutzrunde WA-27–WA-30. Integrationszweig: `codex/ablageaudit-schutzrunde-2026-10-18`. App-SHA-256: `f74af723e3fe1fc18aae5beafcef3d026a3a9c39d8eb16c90b68fb3ae7ddec26`; 72 eigene Laufzeitdateien, 94 Integrationssuiten. Alle 14 ausführbaren Änderungen stimmen mit dem geprüften Schutzkandidaten überein. [Schutznachweis](../01_Repository/Glide/tests/qa-3.43.1/schutzrunde_2026-10-18/README.md).

Die Python-Lieferung in 07 bleibt unverändert auf dem vorherigen App-Hash `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`. Eigenständige Pakete bleiben 3.42.0: Windows 102/102 Manifestdateien bestätigt, Mac 327/330 mit drei fehlenden Frameworkdateien. Keine neue Paketlieferung, Signatur oder Releasefreigabe. [Verbindliche Prüf- und Liefermatrix](../01_Repository/Glide/docs/07_QA_BERICHT.md).

## 2. Zuständige Dokumente

'''+table+'''

## 3. Auftrag und Bereinigung

Der Inhaber hat am 18.10.2026 die Wiederaufnahme und Prüfung der Schutzrunde sowie anschließend die vollständige Ablageprüfung, Aktualisierung, Zusammenführung, Bereinigung, erneute Validierung und einen Commit samt GitHub-Pull-Request beauftragt. Der Pull Request wird nicht automatisch zusammengeführt. Das ist keine Freigabe für weitere Features, neue Versionen oder eine Lieferung nach 07.

Die Inventur schließt jede Datei und jeden Ordner der Projektwurzel einschließlich versteckter Git-Daten und Arbeitskopien ein. Inhaltsprüfung und Wichtigkeit, sichere Aufbewahrung, tatsächliche Einsparung und verbleibende Grenzen stehen im [Ablagenachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Uncommittete Ausgangsstände wurden außerhalb der Projektwurzel gesichert; ihre Hashmanifeste bleiben im Nachweis. Zweige und Stashes tragen wiederherstellbare Entwicklungsstände; entfernte Arbeitskopien sind keine gelöschten Branches. Der alte Affinity-Bestand bleibt erhalten: Der historische Löschblock ist keine heutige Freigabe.

## 4. Nächste Arbeit und offene Entscheidungen

WA-27/A32, WA-28/A34, WA-29/A35 und WA-30/A36 sind im Kandidaten gezielt geschlossen; A33 ist durch FP-01 integriert. WA-26/A31 (kalte Bildkonversion) bleibt offen und benötigt einen gemeinsamen asynchronen Dienst. Natürliche Fehlerhäufigkeit und Schutz-Gegenproben sind getrennte Aussagen.

D01–D51 gelten weiter; neue Entscheidungen beginnen bei D52, D49 bleibt eine Auslegung mit Korrekturvorbehalt. D51 erlaubt mehrere Pakete pro Phase mit gezielten Prüfungen während der Arbeit und Gesamtprüfung/Lieferung am Phasenende. E-P1–E-P5 sind damit nicht pauschal bestätigt. WA-19–WA-25/TK9-RAD/PS-01/PS-02 bleiben vergebene Kennungen. Für Nutzpakete bleiben E-U1 Kompaktmodus, E-U2 Nebenansicht, E-U3 Notion-Muster und die Phasen-/Zusatzentscheidungen im Plan §20 offen; keine Analyseempfehlung entscheidet sie. Paket 8 ist nicht geliefert.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokal und ohne neue Laufzeitabhängigkeit; [AGENTS.md](../01_Repository/Glide/AGENTS.md), D17 und die bestehenden Mutationseinstiege beachten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Echte Nutzerdaten und private Fehlerprotokolle gehören nicht zu diesem Auftrag.
- Die 28 Originalreferenzen sind Eingangsbelege, keine austauschbare QA-Bildserie; lokal behalten und bei Rechnerwechsel als vollständiges Paket mitgeben. Alle sieben aktuellen QA-Versionen, die Bilder der drei neuesten Versionen, Migrationsfixtures, 07, Showcase und vorhandene Pakete bleiben geschützt. Git-Ignore ist keine Löschfreigabe.
- Ein Thema, eine Quelle; historische Prüfergebnisse nicht nachträglich grün schreiben. Arbeitskopien erst nach Sicherung, Inhaltsabgleich und Integration entfernen.
- Vor einem Commit CI-Grundstufe; ein absichtlich älterer Lieferstand wird dokumentiert. `--lieferstand-streng` ist erst beim gemeinsamen Lieferabschluss passend. Der aktuelle Commit-/Pushauftrag umfasst den überprüften Kandidaten und den Ablagenachlauf.
- Produktionsphasen nach D51: Quell-/Prüf-/Ressourcenstand einfrieren, vollständige Matrix und native Plattformtore prüfen, dann 07/Showcase/Pakete und Hashes abgleichen. Neue ausführbare Änderungen erfordern neue betroffene Prüfungen. Suitezahl aus `SUITEN` ableiten.

## 6. Bewusste Grenzen

Der Schutzkandidat und die Ablage sind gezielt geprüft; die gesamte zukünftige Produktionsphase ist damit nicht abgeschlossen. Native Mac-Start-/Signaturprüfung, fehlende Mac-Frameworkdateien, VoiceOver/NVDA/Orca, physische Bedienung, DPI/Mehrmonitor sowie Rechte-, Lizenz- und Releasefragen bleiben offen. Die frühere Standanalyse beschreibt ihren damaligen Quellstand; aktuelle Aussagen stehen in der QA-Matrix. Keine gemessenen Zeiten aus alten Protokollen als heutige Messung ausgeben.
'''
write(rel,old,s,'Übergabe auf integrierten Kandidaten, aktuellen Auftrag und tatsächliche Liefergrenzen konzentriert.')

rel='00_Arbeitsvorbereitung/Glide_Analyse.md';old=(ROOT/rel).read_text(encoding='utf-8');lines=old.splitlines(keepends=True)
notice='\n**Einordnung nach Integration am 18.10.2026:** Die folgende Gesamtanalyse bewahrt den untersuchten Vorzustand `c0252ba` / App-Hash `ed2b7eb…` sowie die damalige Upstream-Probe. FP-01 und WA-27–WA-30 sind inzwischen im lokalen Prüfkandidaten integriert. Aktuelle Quell-, Prüf- und Lieferstände stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Aufgaben nur im [Plan](Glide_Entwicklungsplan.md). Die vollständige Ablagenachprüfung steht im [Nachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Historische Befunde und Messergebnisse werden hier nicht umgedeutet.\n'
write(rel,old,lines[0]+notice+''.join(lines[1:]),'Historischen Untersuchungsstand klar von aktueller Integration abgegrenzt.')

for rel in ['README.md',Q+'docs/00_INDEX.md',Q+'tests/README.md',Q+'README.md',Q+'packaging/README.md']:
    old=(ROOT/rel).read_text(encoding='utf-8');s=old
    if rel==Q+'tests/README.md':s=s.replace('92 Suiten aus','94 Suiten aus',1).replace('92 lokale Integrationssuiten','94 lokale Integrationssuiten',1)
    elif rel=='README.md':
        s=s.replace('lokale Python-Lieferung; getrennte Kandidaten und Pakete im QA-Bericht','integrierter Prüfkandidat; getrennte Lieferung und Pakete im QA-Bericht',1)
        s=re.sub(r'(?m)^- \*\*Lokale Python-Lieferung 3\.43\.1.*$', '- **Prüfkandidat 3.43.1 / Format 25 vom 18.10.2026:** FP-01 und WA-27–WA-30 sind im Quellbaum integriert und gezielt geprüft. Die Python-Lieferung 07 bleibt auf dem vorherigen 3.43.1-Stand, Pakete bleiben 3.42.0. [Aktuelle Prüf- und Liefermatrix](01_Repository/Glide/docs/07_QA_BERICHT.md). Dies ist eine Entwicklungsfassung.',s)
    elif rel.endswith('00_INDEX.md'):s=s.replace('Lokale 3.43.1-Grundprüfung/Fehlerproben, getrennte Upstream-Kandidaten und Paketstände','Integrierter 3.43.1-Prüfkandidat, Schutzrunde/Ablagenachlauf und getrennte Liefer-/Paketstände')
    elif rel==Q+'README.md':s=s.replace('Neubau für 3.43.0','Neubau für den aktuellen Kandidaten')
    else:s=s.replace('Windows102/102','Windows 102/102')
    write(rel,old,s,'Einstieg auf aktuellen Kandidaten beziehungsweise tatsächliche Suitezahl abgeglichen.')

rel=Q+'docs/ARBEITSRICHTUNG.md';old=(ROOT/rel).read_text(encoding='utf-8')
addition='**Fortsetzung 18.10.2026:** Schutzrunde WA-27–WA-30 auf FP-01 prüfen und integrieren; anschließend jede Datei und Ablage im Projekt inventarisieren, Dokumentation aktualisieren und zusammenführen, belegbar entbehrliche Kopien entfernen, erneut validieren, Commit und GitHub-Pull-Request erstellen. Keine automatische Zusammenführung, neue Version oder Lieferung nach 07. Die frühere Analyse ist ein abgeschlossener Vorzustand; aktueller Status steht im QA-Bericht und im Entwicklungsplan.\n\n'
s=old.replace('## Beauftragt\n\n','## Beauftragt\n\n'+addition,1)
write(rel,old,s,'Aktuellen Inhaberauftrag ergänzt; bestätigte Entscheidungen unverändert.')

rel=Q+'docs/DOKUMENTENPFLEGE.md';old=(ROOT/rel).read_text(encoding='utf-8')
s=old+'\n## Ablageprüfung vom 18.10.2026\n\nDer [globale Nachweis](../tests/qa-3.43.1/ablageaudit_2026-10-18/README.md) erfasst Dateien, Ordner, vollständige Hashes und Dokumentzuständigkeiten einschließlich Git und lokaler Arbeitskopien. Ignorierte Dateien sind nicht automatisch entbehrlich. Originalreferenzen, aktuelle QA-Bilder, Migrationsfixtures und bestehende Lieferstände werden unabhängig vom Git-Status geschützt. Historische Rohbelege bleiben historisch; doppelte Erzählungen werden in der aktuellen Quelle zusammengeführt.\n\nGit-Objektverdichtung erfolgt ohne History-, Ref- oder Reflogverlust und mit Objektmengenvergleich. Arbeitskopien entfallen erst nach Prüfung ihrer eigenen Änderungen und lokalen Belege, Sicherung außerhalb der Projektwurzel und Integration; Branches und Stashes bleiben erhalten. Ein abgelehnter Löschschritt bleibt mit seinem tatsächlichen Ergebnis im Journal.\n'
write(rel,old,s,'Nachweis und Aufbewahrungsgrenzen für globale Bereinigung ergänzt.')

rel=Q+'tests/qa-3.42.0/bestandspruefung_2026-10-15/README.md';old=(ROOT/rel).read_text(encoding='utf-8')
s=re.sub(r'\[([^\]]*)\]\(grundstufe/ergebnis\.json\)',r'\1 (`grundstufe/ergebnis.json`, lokal nicht vorhanden)',old)
if s!=old:s+='\nNavigationskorrektur 18.10.2026: Der frühere Link auf `grundstufe/ergebnis.json` ist in dieser Ablage nicht auflösbar. Es wurde kein Ergebnis rekonstruiert; die historischen Prüfaussagen bleiben unverändert.\n'
write(rel,old,s,'Nicht vorhandenen historischen Zielbeleg als fehlend ausgewiesen statt gebrochen zu verlinken.')

(AUDIT/'dokumentaenderungen.json').write_text(json.dumps(CHANGES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Dokumentänderungen:',len(CHANGES))
