"""Synthetische eigene Tk-Fenster am eingefrorenen Analysebestand aufnehmen."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    base = args.app.parents[2]
    sys.path.insert(0, str(base / 'tests/integration'))
    sys.path.insert(0, str(base / 'tests/tools'))
    from test_uiux_paket import Lauf
    from releasedaten import save_windows_screenshot
    report = dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),
                  screens=[], errors=[], limits='Eigene Windows-Testfenster, synthetische Showcase; keine physische DPI-, Reader- oder Mehrplattformabnahme.')
    with tempfile.TemporaryDirectory(prefix='glide-sichtpruefung-') as temporary:
        run = Lauf(args.app, str(Path(temporary) / 'data'))
        try:
            run.showcase()
            app = run.app
            page = next(e for e in app.lists if app.is_page_list(e))
            listing = max((e for e in app.lists if not app.is_page_list(e) and e.get('items')), key=lambda e: len(e['items']))
            views = [('startseite', app.set_home_view), ('heute', app.set_today_view),
                     ('labels', app.set_labels_view), ('vorlagen', app.set_template_view),
                     ('papierkorb', app.set_trash_view), ('liste', lambda: app.set_active_list(listing['id'])),
                     ('seite', lambda: app.set_active_list(page['id'])),
                     ('pinnwand', app.open_global_board), ('kalender', app.open_calendar_view)]
            for label, geometry, font in [('normal', '1280x800+20+20', 'mittel'), ('eng_gross', '860x700+20+20', 'gross')]:
                app.settings['ui_font_size'] = font
                app.apply_ui_font()
                run.root.geometry(geometry)
                run.idle(4)
                for name, opener in views:
                    opener()
                    run.idle(5)
                    target = args.out / (str(len(report['screens']) + 1).zfill(2) + '_' + name + '_' + label + '.png')
                    save_windows_screenshot(run.root, target)
                    report['screens'].append(dict(view=name, configuration=label, file=target.name,
                                                  captured=True, visually_reviewed=False))
            def capture_dialog(dialog, *args, **kwargs):
                run.idle(4)
                save_windows_screenshot(dialog, target_dir / '19_einstellungen.png')
                dialog.destroy()
            target_dir = args.out
            app.run_modal = capture_dialog
            app.show_settings_dialog()
            report['screens'].append(dict(view='einstellungen', file='19_einstellungen.png', captured=True, visually_reviewed=False))
            report['errors'] += [str(x).replace(str(Path.home()), '~') for x in run.errors]
        except Exception as exc:
            report['errors'].append(type(exc).__name__ + ': ' + str(exc).replace(str(Path.home()), '~'))
        finally:
            run.ende()
    (args.out / 'sichtpruefung.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(screens=len(report['screens']), errors=report['errors'])))


if __name__ == '__main__':
    main()
