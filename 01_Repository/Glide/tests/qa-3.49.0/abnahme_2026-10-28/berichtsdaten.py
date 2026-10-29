"""Redaktionell bewertete Abnahmeeinheiten, aus bestehenden Kennungen abgeleitet.

Das Register ist ein datierter Prüfbeleg, keine zweite aktuelle Roadmap.
"""
from pathlib import Path
import hashlib
import json
import re

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
ROOT = REPO.parents[1]


def row(identity, title, implementation, test, delivery, rest, modules=(), evidence='E01, E03'):
    return dict(id=identity, title=title, implementation=implementation, test=test,
                delivery=delivery, rest=rest, modules=list(modules), evidence=evidence)


def main():
    legacy = [
        row('G01 / U04 / KO03/05', 'Schnellerfassung und deutsche Chips', 'I', 'Historisch', 'bis 3.45', 'Aktuelle native Bedienabnahme', ['capture_parser.py']),
        row('G02 / AU01–07 / KO01/02/06', 'Heute, Demnächst, Planung und Kapazität', 'I', 'Historisch + E09', 'Kern bis 3.45', 'Neuere Tagesaktionen separat unten', ['planning.py','day_proposal.py','week_planning.py','routines.py']),
        row('G03/04 / N04 / AU04', 'Tagesabschluss und Stundenraster', 'I', 'Historisch', 'bis 3.45', 'Aktuelle native Bedienabnahme', ['week_planning.py']),
        row('G05 / H-02 / H-02r', 'Fokus und Tastaturwege', 'I', 'Historisch', 'bis 3.45', 'Reader/Tastatur; Zielhinweis erst nach Aktion', ['focus_timer.py','interaction_policy.py']),
        row('G29/31/32 / G08/30', 'Aufgaben in Seiten und Objektverweise', 'I', 'Historisch + E09', 'Kern bis 3.45', 'Neue Verweisaktionen separat unten', ['task_references.py','object_references.py']),
        row('G28/G09/U08 / U18', 'Seiten, Bilder, Live-Listen und Vorlagen', 'I', 'Historisch', 'bis 3.45', 'Enge/lange Inhalte, native Bedienung', ['page_features.py','page_markdown.py']),
        row('G11', 'Vorlagen mit Datum und Platzhaltern', 'I', 'Historisch', 'bis 3.45', 'Automatische Vorlagenwiederholung nicht gewählt', []),
        row('G14 / U01/03/07 / D-03', 'Inhaltssuche, Palette, Filtererklärung', 'I', 'Historisch', 'bis 3.45', 'Kein zusätzlicher Suchindex geschuldet', ['content_search.py','action_catalog.py','filter_explain.py']),
        row('N05 / U12 / KO04 / OB02–04', 'Gemeinsamer Aufgabeninspektor', 'I', 'Historisch', 'bis 3.45', 'DPI/Mehrmonitor und native Bedienung', ['ui_design.py']),
        row('UX1 / U02–24 / OB01/05/06', 'Alltagskomfort und ruhige Oberfläche', 'I', 'Historisch', 'bis 3.45', 'OB06/native Sicht; fortlaufende Designübertragung', ['appearance.py','home_tiles.py','release_notes.py']),
        row('G16/19/20', 'Pixelwerkstatt, Paletten und Symbolexport', 'I', 'Historisch', 'bis 3.45', 'Native Sicht/Nischeneignung', ['drawing.py']),
        row('G17 / D18 / S26-08', 'Animation mit Frames und PNG-Ausgabe', 'I', 'Historisch', 'ab 3.40', 'GIF/Zwiebelhaut waren nicht gewählt', ['animation.py','animation_export.py']),
        row('G24 / F-01/03', 'KI-Austausch und Sicherungsvergleich', 'I', 'Historisch', 'bis 3.45', 'Realer externer Dateirundlauf', ['exchange_patch.py','backup_diff.py']),
        row('G21 / V02 / N13', 'Notion-Import, Konflikte und Seitenrestore', 'I', 'Historisch', 'ab 3.41', 'Reale Importe/Restore, Plattformen', ['notion_import.py','notion_reimport.py','page_restore.py','restore_assets.py']),
        row('G26 / H-03 / N11 / S26-10', 'Eigenständige Pakete und Bauweg', 'I', 'Archive E05 gleich', 'native 3.45', 'Aktueller 3.49-Stand noch nicht paketiert', []),
        row('LG01–04 / D45 / S26-11/12/22', 'Logo, Symbolrollen und Tk-Rückfall', 'I', 'Historisch', 'ab 3.37', 'Logoentwurf freigegeben; keine appweite DPI-Freigabe', ['logo.py','glyph_metrics.py']),
    ]
    fp = [
        row('FP-00 / WA-17/18', 'Wiederholungseingabe und Kalenderparser', 'I', 'Historisch + E06 Units', 'ab 3.39.1', 'Keine offene Erstimplementierung', ['capture_parser.py','repeat_rules.py','repeat_ics.py']),
        row('FP-01 / WA-01', 'Wiederholen nach Rückgängig', 'I', 'ROT: 8/9', 'ab 3.44', 'Prüfadapter/Sitzungsabschluss korrigieren; Suite neu bestehen', ['undo_history.py'], 'E07, E08'),
        row('FP-02 / WA-02', 'Erweiterte Rhythmen, beide Stufen', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44', 'Native Bedienung/Kalenderaustausch', ['repeat_rules.py','repeat_ics.py']),
        row('FP-03 / WA-03', 'Gespeicherte Filter und Darstellungen', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44', 'Keine offenen Kernstufen; native Abnahme', ['view_definition.py']),
        row('FP-04 / WA-04', 'Seiten-/Notizkarten auf Pinnwänden', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44', 'Namespace erfüllt; allgemeines WA-09 bleibt separat', ['pinboard_pages.py']),
        row('FP-05 / WA-05', 'Unverknüpfte Titelerwähnungen', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44', 'Keine semantische KI-Verknüpfung geschuldet', ['object_references.py']),
        row('FP-06 / WA-06', 'Fünf KI-Dateiaufträge und volle Vorschau', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44, später ergänzt', 'Provider/Netzendpunkt nicht gewählt', ['exchange_recipes.py','exchange_patch.py']),
        row('FP-07 / WA-07 Stufe 1', 'Lesbarer Markdownbaum mit Medien', 'I', 'Historisch; frisch nicht gestartet', 'ab 3.44', 'Canvas Stufe 2 optional; kein Wiederimportversprechen', ['markdown_tree.py']),
    ]
    current = [
        row('A01 / E-U1 A / D55', 'Kompaktmodus 480 × 560', 'I', 'Historisch + E09', 'Kern ab 3.45', 'Windows Kürzel/Mehrmonitor und Mac/Reader offen', ['compact_mode.py']),
        row('A02 / E-U2 A / D55', 'Lesende Nebenansicht', 'I', 'Historisch + E09', 'Kern ab 3.45', 'Zwei schreibende Editoren sind kein Rest', ['side_view.py']),
        row('A03 / E-U3 A / D55', 'Seiten-/Blockaktionen und Kopfbedienung', 'I', 'Historisch', 'Kern ab 3.45', 'Windows Teilabnahme Punkte1–4, große Schrift/Mac offen', ['action_menu.py']),
        row('B01–B22 / D50', 'UI-/UX-Paket aus Nutzerbeobachtungen', 'I', 'Historisch; Einzelmatrix im Anhang', 'Kern ab 3.43', 'Menschliche Gesamtfreigabe nicht dokumentiert', ['ui_design.py','release_notes.py']),
        row('WA-11 / §21.17', 'Verweisvorschau ohne Hauptwechsel', 'I', 'Historisch + E09', 'ab 3.45', 'Native Fokus-/Readerabnahme', ['side_view.py','object_references.py']),
        row('WA-12 / §21.16', 'Vorschlag mit direkten Freigaben', 'I', 'Historisch', 'ab 3.45 laut §21.20', 'Menschenabnahme; ältere Lieferzeile widersprüchlich', ['day_proposal.py']),
        row('§21.19/22 / WA-39', 'Startseitenmodell und direktes Erledigen', 'I', 'Historisch + E09', 'Basis3.45; Aktionen später', 'Quelle/Lieferung auseinanderhalten', ['home_dashboard.py','home_task_tiles.py']),
        row('§21.23 / D57', 'Direkte Tagesplanung und Fokus', 'I', 'E09 gleicher Apphash', 'Python ab 3.46', 'Keine native aktuelle Paketabnahme', ['home_task_tiles.py']),
        row('§21.23 / D57', 'Suche und Abschnittssprünge nebenan', 'I', 'E09 gleicher Apphash', 'Python ab 3.46', 'Native/Reader-/DPI-Abnahme', ['side_view.py']),
        row('§21.24 / D57', 'Mehrfachplanung und Nebenansichtsverlauf', 'I', 'E09 gleicher Apphash', 'Python ab 3.47', 'Native/Reader-/DPI-Abnahme', ['home_task_tiles.py','side_view.py']),
        row('§21.26 / D57', 'Tagesnavigation, Wichtigkeit/Labels, interne Links', 'I', 'E09 gleicher Apphash', 'nur Quelle ab 3.48', 'Lieferung und breite Abnahme fehlen', ['task_editing.py','home_task_tiles.py','side_view.py']),
        row('§21.28 / D57', 'Wochenwahl, Fälligkeit/Aufwand, Verweisaktionen', 'I', 'E09 gleicher Apphash', 'nur Quelle3.49', 'Lieferung und breite Abnahme fehlen', ['task_editing.py','home_task_tiles.py','side_view.py']),
    ]
    safeguards = [
        row('WA-26', 'Gemeinsame Bildkonversion im Hintergrund', 'I', 'Historisch + E06 Units', 'ab 3.44', 'Native Konverter/Sicht', ['image_conversion.py','image_preview.py']),
        row('WA-27–31', 'Bestandswächter, Laden, Flush und Datensperre', 'I', 'Historisch + E06 Units', 'ab 3.44', 'Native/Cloud-Abgleich getrennt', ['structural_guard.py','load_phases.py','editor_flush.py','data_lock.py']),
        row('WA-40/47', 'Speicherstatus, Grenzen und Retry', 'I', 'E10; frisch nicht gestartet', 'Basis ab 3.45', 'Appweite Fehlerklassifikation separat offen', ['storage_health.py','persistence.py','save_result.py']),
        row('WA-48/51 / §21.15', 'Sicherungsübersicht und Anhangsschutz', 'I', 'Historisch + E06 Units', 'ab 3.45', 'Native Warnungen/Mac offen', ['backup_catalog.py','attachment_policy.py','image_conversion.py']),
        row('§21.27 / WA-42', 'Gesicherte Prüfabläufe', 'I', 'E06 Werkzeugtests', 'nur Quelle3.49', 'Kein allgemeiner Stabilitätsnachweis', []),
        row('§21.27 / WA-40/41B', 'Sitzungsnachweis, Freigabe und Restore', 'I', 'E10; aktueller Prüferkonflikt E08', 'nur Quelle3.49', 'Rückweg gezielt geprüft; kein WA-41B-Ursachenfix', ['session_guard.py']),
        row('§21.27 / WA-41A/40', 'Lokale Diagnose und Prozessbegleitung', 'I', 'E06 Units / E10', 'nur Quelle3.49', 'Native Builds/Startvarianten aktuell abnehmen', ['runtime_diagnostics.py','glide_start.py']),
    ]
    remaining = [
        row('P8 / N12 / U23 / S26-16', 'Zugänglicher Aufgaben-Kernablauf für4.0', 'P', 'Vorbereitung/Einzelbelege', 'keine4.0-Lieferung', 'Readerketten, Orca-Absturz, aktuelle UI, native Matrix; D50 pausiert', ['accessibility.py','core_accessibility.py']),
        row('WA-09 / A27', 'Allgemeine Zukunftsfeldtoleranz', 'T', 'Namespaces gezielt geprüft', 'teilweise', 'Unbekannte Unterfelder nicht allgemein erhalten', []),
        row('P05 / G27 / WA-32', 'Wartbarkeit und appweite Designübertragung', 'T', 'Piloten/Einzelansichten', 'teilweise', 'Appweite Kontext-/Komponentenabdeckung offen', ['ui_design.py']),
        row('WA-36', 'Mutations-, Snapshot- und Refreshkosten', 'T', 'Datierte Messungen', 'teilweise', 'Übrige Render-/Snapshotwege und native Leistung', ['item_index.py']),
        row('WA-37/38', 'Mutationsvertrag und Speicherergebnis', 'T', 'Kern-/Callerfälle', 'teilweise', 'Übrige direkte Struktur-/Importcaller', ['task_editing.py','persistence.py','save_result.py']),
        row('WA-39', 'Ansichts-/Dialog-/Themeauslagerung', 'T', 'Startseitenpilot', 'teilweise', 'Weitere Presenter/Settings/Detail/Theme nur schrittweise', ['home_dashboard.py','home_task_tiles.py']),
        row('WA-40', 'Fehlerbehandlung nach Wirkung appweit', 'T', 'Kritische Speicherpfade', 'teilweise', 'Übrige OS-/UI-/Teardownhandler systematisch prüfen', ['storage_health.py']),
        row('WA-41A/B', 'Prozessstabilität und Datenkonsistenz', 'T', 'Widersprüchliche Lastbefunde', 'Freigabe blockiert', 'A-Ursache ungeklärt; B-Felddifferenz nicht aufgelöst', []),
        row('WA-42 / PS-01/02', 'Prüfstabilität und Einzelbefunde', 'T', 'Neue Wächter/Kernfälle', 'teilweise', 'Originale Pflichtsuite jetzt rot; weitere Fokus-/Showcasebefunde offen', []),
    ]
    all_rows = legacy + fp + current + safeguards + remaining
    for entry in all_rows:
        entry['module_proofs'] = {name: hashlib.sha256((REPO/'src/glide'/name).read_bytes()).hexdigest()
                                  for name in entry['modules'] if (REPO/'src/glide'/name).is_file()}
        entry['missing_module_proofs'] = [name for name in entry['modules'] if name not in entry['module_proofs']]
    data = {'definition': 'Abnahmeeinheiten, keine addierbare Anzahl unabhängiger Features; Kennungen überlappen fachlich.',
            'legacy': legacy, 'fp': fp, 'current': current, 'safeguards': safeguards, 'remaining': remaining}
    (OUT/'paketmatrix.json').write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Abnahmeeinheiten', len(all_rows), 'fehlende Codebelege',
          [(entry['id'], entry['missing_module_proofs']) for entry in all_rows if entry['missing_module_proofs']])
    frozen = json.loads((OUT/'eingefroren.json').read_text())
    directory = Path(frozen['copy'].replace('%USERPROFILE%',str(Path.home())))
    counts = {}
    for name in ('Werkzeugtests', 'Fachlogik-Unit-Tests', 'Fachlogik ohne Systemzeitzonen'):
        text = (directory/'grundstufe'/(name+'.log')).read_text(encoding='utf-8')
        number = re.search(r'Ran (\d+) tests?', text)
        skipped = re.search(r'skipped=(\d+)',text)
        counts[name] = {'count':int(number.group(1)) if number else None,
                        'skipped':int(skipped.group(1)) if skipped else 0, 'ok':'\nOK' in text}
    (OUT/'testzaehlung.json').write_text(json.dumps(counts,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
