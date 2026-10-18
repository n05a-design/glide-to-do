"""Isolierte Probe der App-Datensperre (glide.lock). Kuenstliche Daten, temporaerer GLIDE_DATA_DIR,
keine Tk-Instanz, keine Produktionsaenderung. Aufruf: python -B probe_lock.py --source <app.pyw> --output <json>"""
import argparse, hashlib, importlib.machinery, importlib.util, json, os, subprocess, sys, tempfile, time
from datetime import datetime, timedelta
from pathlib import Path


def main():
    p = argparse.ArgumentParser(); p.add_argument('--source', required=True); p.add_argument('--output', required=True)
    args = p.parse_args(); source = Path(args.source).resolve()
    with tempfile.TemporaryDirectory(prefix='glide-lockprobe-') as d:
        os.environ['GLIDE_DATA_DIR'] = str(Path(d) / 'data')
        loader = importlib.machinery.SourceFileLoader('glide_lock_probe', str(source))
        spec = importlib.util.spec_from_loader(loader.name, loader); m = importlib.util.module_from_spec(spec); loader.exec_module(m)
        lock = Path(m.LOCK_FILE); lock.parent.mkdir(parents=True, exist_ok=True)
        assert str(lock).startswith(d), 'Lockpfad liegt nicht im Temp-Ordner'
        host = os.environ.get('COMPUTERNAME') or os.environ.get('HOSTNAME') or 'unbekannt'
        now = datetime.now().astimezone()
        res = {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'python': sys.version, 'tests': []}

        def app():
            a = m.ListApp.__new__(m.ListApp); return a

        def clear():
            if lock.is_dir(): lock.rmdir()
            elif lock.exists(): lock.unlink()

        def rec(name, **kw):
            res['tests'].append({'name': name, **kw})

        child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])
        try:
            cases = [
                ('kein_lock', None),
                ('defektes_json', 'nicht json {'),
                ('json_liste', '[1,2]'),
                ('fremder_host_frisch', json.dumps({'host': 'ANDERER', 'pid': 4, 'token': 'x', 'started_at': now.isoformat(), 'refreshed_at': now.isoformat()})),
                ('fremder_host_9h', json.dumps({'host': 'ANDERER', 'pid': 4, 'token': 'x', 'started_at': (now - timedelta(hours=9)).isoformat(), 'refreshed_at': (now - timedelta(hours=9)).isoformat()})),
                ('gleicher_host_lebender_pid_frisch', json.dumps({'host': host, 'pid': child.pid, 'token': 'x', 'started_at': now.isoformat(), 'refreshed_at': now.isoformat()})),
                ('gleicher_host_lebender_pid_9h_ohne_schreiben', json.dumps({'host': host, 'pid': child.pid, 'token': 'x', 'started_at': (now - timedelta(hours=9)).isoformat(), 'refreshed_at': (now - timedelta(hours=9)).isoformat()})),
                ('gleicher_host_toter_pid', json.dumps({'host': host, 'pid': 999999, 'token': 'x', 'started_at': now.isoformat(), 'refreshed_at': now.isoformat()})),
            ]
            for name, content in cases:
                clear()
                if content is not None: lock.write_text(content, encoding='utf-8')
                r = app().read_foreign_lock()
                rec('read_foreign_lock:' + name, result_is_foreign=bool(r))
            # Lockpfad ist ein Verzeichnis -> open() wirft OSError
            clear(); lock.mkdir(); r = app().read_foreign_lock(); rec('read_foreign_lock:lockpfad_unlesbar_verzeichnis', result_is_foreign=bool(r)); lock.rmdir()

            # acquire bei defektem Lock: wird ueberschrieben, Instanz schreibfaehig
            clear(); lock.write_text('nicht json {', encoding='utf-8'); a = app(); info = a.acquire_data_lock()
            rec('acquire:defekter_lock', foreign=bool(info), read_only=a._data_read_only, lock_owned=json.loads(lock.read_text(encoding='utf-8')).get('token') == a._lock_token.get('token'))

            # refresh: Lockdatei verschwindet -> bleibt schreibfaehig, Lock wird nicht neu angelegt
            clear(); a = app(); a.acquire_data_lock(); lock.unlink(); a._lock_token = dict(a._lock_token, refreshed_at='alt'); a.refresh_data_lock()
            rec('refresh:lockdatei_entfernt', read_only=a._data_read_only, lock_recreated=lock.exists())

            # refresh: fremder Token -> nur-lesen
            clear(); a = app(); a.acquire_data_lock(); lock.write_text(json.dumps({'host': host, 'pid': child.pid, 'token': 'fremd', 'started_at': now.isoformat(), 'refreshed_at': now.isoformat()}), encoding='utf-8')
            a._lock_token = dict(a._lock_token, refreshed_at='alt'); a.refresh_data_lock(); rec('refresh:fremder_token', read_only=a._data_read_only)

            # Verdraengung: A besitzt Lock, B uebernimmt (z.B. nach defektem/abgelaufenem Lock), A schreibt Einstellungen ohne refresh
            clear(); a = app(); a.acquire_data_lock(); b_token = {'host': host, 'pid': child.pid, 'token': 'B', 'started_at': now.isoformat(), 'refreshed_at': now.isoformat()}
            lock.write_text(json.dumps(b_token), encoding='utf-8')
            rec('verdraengung:A_flag_vor_naechstem_save_items', read_only_cached=a._data_read_only,
                note='save_settings/save_window_geometry pruefen nur dieses Flag; erst save_items ruft refresh_data_lock')
            # Freigabe darf fremden Lock nicht loeschen
            a.release_data_lock(); rec('release:fremder_lock_bleibt', lock_still_present=lock.exists())
        finally:
            child.kill(); child.wait()
        Path(args.output).write_text(json.dumps(res, indent=2, ensure_ascii=False), encoding='utf-8')
        print(json.dumps(res, indent=1, ensure_ascii=True))


if __name__ == '__main__':
    main()
