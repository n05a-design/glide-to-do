"""Startet das eigenständige Paket oder dessen isolierte native Startprobe."""
from pathlib import Path
import json
import hashlib
import os
import sys
import tempfile
import traceback


def loaded_libraries():
    """Native Anbieter feststellen; ausschließlich bei der isolierten Paketprobe."""
    import ctypes
    if sys.platform == 'darwin':
        process = ctypes.CDLL(None)
        count = process._dyld_image_count
        count.argtypes = [];count.restype = ctypes.c_uint32
        name = process._dyld_get_image_name
        name.argtypes = [ctypes.c_uint32];name.restype = ctypes.c_char_p
        return list(dict.fromkeys(name(i).decode('utf-8') for i in range(count())))
    if sys.platform == 'win32':
        from ctypes import wintypes
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        current = kernel.GetCurrentProcess
        current.argtypes = [];current.restype = wintypes.HANDLE
        enumerate_modules = kernel.K32EnumProcessModules
        enumerate_modules.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.HMODULE),
                                      wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
        enumerate_modules.restype = wintypes.BOOL
        filename = kernel.GetModuleFileNameW
        filename.argtypes = [wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]
        filename.restype = wintypes.DWORD
        capacity, required = 1024, wintypes.DWORD()
        while True:
            if capacity > 65536:
                raise RuntimeError('Unerwartet viele native Laufzeitbibliotheken.')
            modules = (wintypes.HMODULE*capacity)()
            if not enumerate_modules(current(), modules, ctypes.sizeof(modules), ctypes.byref(required)):
                raise ctypes.WinError(ctypes.get_last_error())
            if required.value <= ctypes.sizeof(modules):
                break
            capacity = required.value//ctypes.sizeof(wintypes.HMODULE)+64
        names = []
        for module in modules[:required.value//ctypes.sizeof(wintypes.HMODULE)]:
            buffer = ctypes.create_unicode_buffer(32768)
            length = filename(module, buffer, len(buffer))
            if length == 0 or length >= len(buffer):
                raise ctypes.WinError(ctypes.get_last_error())
            names.append(buffer.value)
        return list(dict.fromkeys(names))
    raise RuntimeError('Paketprobe braucht eine beauftragte native Zielplattform.')


def accessible_core_probe(app, mod, settle):
    """Echter Paket-Kernablauf bei gebündelter 9.1-Runtime; kein Readerersatz."""
    import time
    root = app.root
    assert str(root.tk.call('package', 'present', 'Tk')) == '9.1.0'
    assert app.tree._glide_accessibility.supported, 'Paket enthält kein natives Zugangsbackend.'
    def wait(condition):
        deadline = time.monotonic()+4
        while time.monotonic() < deadline:
            settle()
            if condition():
                return
            time.sleep(.02)
        raise AssertionError('Kernablauf im isolierten Paket erreicht seinen gespeicherten Zustand nicht.')
    def named(name):
        for widget in app.iter_descendants(app.detail_pane):
            binding = getattr(widget, '_glide_accessibility', None)
            if binding is not None and widget.winfo_ismapped():
                value = binding.attributes()
                if value is not None and value.name == name:
                    return widget
        raise AssertionError('Benanntes Paketfeld fehlt: '+name)
    inbox = app.ensure_inbox_list()
    app.set_active_list(inbox['id'])
    settle()
    listing = lambda: next(entry for entry in app.lists if entry.get('id') == inbox['id'])
    previous = {item['id'] for item in listing()['items']}
    app.entry.focus_force()
    app.entry.delete(0, 'end')
    app.entry.insert(0, 'Zugängliche Paketprobe')
    app.entry_placeholder_active = False
    app.entry.event_generate('<Return>')
    wait(lambda: len(listing()['items']) == len(previous)+1)
    item = next(item for item in listing()['items'] if item['id'] not in previous)
    identity = item['id']
    fresh = lambda: app.find_item_in_lists(identity)[0]
    assert app.entry._glide_accessibility.attributes().name == 'Neue Aufgabe'
    app.search_entry.focus_force()
    app.search_entry.delete(0, 'end')
    app.search_entry.insert(0, 'Zugängliche')
    app.search_placeholder_active = False
    app.search_entry.event_generate('<KeyRelease>')
    wait(lambda: app.tree.exists(identity) and all(not app.tree.exists(key) for key in previous))
    app.search_entry.event_generate('<Escape>')
    wait(lambda: app.tree.exists(identity) and all(app.tree.exists(key) for key in previous))
    app.tree.selection_set(identity)
    app.tree.focus(identity)
    app.tree.focus_force()
    settle()
    assert 'Zugängliche Paketprobe' in app.tree._glide_accessibility.attributes().value
    menu = app.build_quick_plan_menu(item_ids=(identity,))
    try:
        choice = next(index for index in range(menu.index('end')+1)
                      if menu.type(index) == 'command' and menu.entrycget(index, 'label').startswith('Heute'))
        menu.invoke(choice)
        wait(lambda: fresh().get('planned_date') == mod.date.today().isoformat())
    finally:
        menu.destroy()
    assert not fresh().get('due')
    app.set_today_view()
    settle()
    assert app.open_task_inspector(identity)
    settle()
    title = named('Aufgabentitel')
    if isinstance(title, mod.tk.Text):
        title.delete('1.0', 'end')
        title.insert('1.0', 'Paketprobe bearbeitet 🏠')
    else:
        title.delete(0, 'end')
        title.insert(0, 'Paketprobe bearbeitet 🏠')
    title.focus_force()
    settle()
    title.event_generate('<Control-s>')
    wait(lambda: fresh()['text'] == 'Paketprobe bearbeitet 🏠')
    field = named('Neuer Checklistenpunkt')
    field.focus_force()
    settle()
    field.insert(0, 'Paket-Unterlagen prüfen')
    field.event_generate('<Return>')
    wait(lambda: len(fresh().get('checklist', [])) == 1)
    checkbox = named('Paket-Unterlagen prüfen')
    assert isinstance(checkbox, mod.tk.Checkbutton)
    checkbox.focus_force()
    settle()
    checkbox.event_generate('<space>')
    wait(lambda: fresh()['checklist'][0]['done'])
    current = named('Paket-Unterlagen prüfen')
    assert current._glide_accessibility.attributes().value == '1'
    assert root.focus_get() is current, 'Checkbox verliert beim Umschalten ihren Paketfokus.'
    app.undo_last_change()
    wait(lambda: not fresh()['checklist'][0]['done'])
    assert not named('Paket-Unterlagen prüfen')._accessible_variable.get()
    return dict(native_backend=True, erfassen_suchen_heute_inspektor=True,
                unicode_titel_gespeichert=True, checkbox_leertaste_undo=True,
                reader_abnahme='separat offen; tatsächlicher Paketablauf ohne Reader')


def smoke(report_path):
    result = {"eigenstaendiger_pruefstart": True, "exitcode": 1}
    root = app = None
    with tempfile.TemporaryDirectory(prefix="glide-paketprobe-") as folder:
        os.environ["GLIDE_DATA_DIR"] = folder
        os.environ["GLIDE_TEST_MODE"] = "1"
        try:
            import glide_app as mod
            import platform
            assert getattr(sys, "frozen", False), "Probe muss das gebaute Paket starten."
            root = mod.tk.Tk()
            root.geometry("1280x800+20+20")
            errors = []
            root.report_callback_exception = lambda *exc: errors.append(repr(exc[1]))
            app = mod.ListApp(root)
            app.show_info = app.show_warning = app.show_error = lambda *a, **k: None
            def settle():
                for _ in range(3):
                    root.update_idletasks(); root.update()
            settle()
            inbox = app.ensure_inbox_list()
            app.set_active_list(inbox["id"])
            task = app.new_item("Isolierte Paketprüfung")
            task["planned_date"] = mod.date.today().isoformat()
            with app.item_change((), restore=False) as change:
                inbox["items"].append(task)
                change.mark()
            settle()
            app.toggle_item_done_anywhere(task["id"])
            settle()
            assert app.find_item_in_lists(task["id"])[0]["done"]
            app.undo_last_change(); settle()
            assert not app.find_item_in_lists(task["id"])[0]["done"]
            views = ("set_home_view", "set_today_view", "set_table_view", "set_library_view", "set_pages_view")
            for name in views:
                getattr(app, name)(); settle()
            app.set_active_list(inbox["id"]); settle()
            assert Path(mod.BASE_DIR).resolve() == Path(folder).resolve()
            assert Path(mod.SAVE_FILE).is_file()
            app.load_items(); settle()
            assert not app.find_item_in_lists(task['id'])[0]['done']
            payload = app.app_backup_payload()
            backup = Path(folder) / 'paketprobe.glideapp'
            app.write_complete_backup(str(backup), payload)
            restored, section = app.read_app_backup_file(str(backup))
            assert restored['lists'] == payload['lists']
            assert section['format_version'] == app.APP_BACKUP_FORMAT_VERSION
            protocol = Path(folder) / "fehlerprotokoll.txt"
            assert not errors, errors
            assert not protocol.exists() or not protocol.read_text(encoding="utf-8").strip()
            bundle = Path(sys.executable).parent.parent if sys.platform == "darwin" else Path(sys.executable).parent
            bundle = bundle.resolve()
            extraction = Path(sys._MEIPASS).resolve()
            assert extraction.is_relative_to(bundle), "Die Paketdateien liegen außerhalb des Pakets."
            inputs = json.loads((extraction / "glide-input.json").read_text(encoding="utf-8"))
            resources = {name: digest for name, digest in inputs["sha256"].items()
                         if name.startswith("resources/")}
            assert any(name.startswith("resources/fonts/") for name in resources)
            assert any(name.startswith("resources/logo/") for name in resources)
            for name, digest in resources.items():
                resource = (extraction / name).resolve()
                assert resource.is_relative_to(bundle) and resource.is_file(), name
                assert hashlib.sha256(resource.read_bytes()).hexdigest() == digest, name
            for name, digest in inputs["licenses_sha256"].items():
                license_file = (extraction / name).resolve()
                assert license_file.is_relative_to(bundle) and license_file.is_file(), name
                assert hashlib.sha256(license_file.read_bytes()).hexdigest() == digest, name
            assert inputs["version"] == mod.APP_VERSION
            families = {str(value).casefold() for value in mod.tkfont.families(root=root)}
            required_families = ("DejaVu Sans", "Pixelify Sans")
            for family in required_families:
                assert family.casefold() in families, "Gebündelte Schrift fehlt: " + family
                font = mod.tkfont.Font(root=root, family=family, size=12)
                assert str(font.actual("family")).casefold() == family.casefold(), family
                assert font.measure("Glide 123") > 0
            assert app.file_drop_support(), app._file_drop_error
            dnd_version = str(root.tk.call("package", "present", "tkdnd"))
            loaded = root.tk.splitlist(root.tk.call("info", "loaded"))
            dnd_libraries = []
            for pair in loaded:
                filename, package = root.tk.splitlist(pair)
                if "tkdnd" in str(package).casefold():
                    library = Path(filename).resolve()
                    assert library.is_relative_to(bundle), str(library)
                    dnd_libraries.append(str(library.relative_to(bundle)))
            assert dnd_libraries, "Die native DND-Bibliothek wurde nicht geladen."
            logo = mod.glide_logo.logo_photo(root, 32)
            assert logo.width() > 0 and logo.height() == 32
            external_paths = [value for value in sys.path
                              if value and not Path(value).resolve().is_relative_to(bundle)]
            assert not external_paths, external_paths
            from runtime_paths import authenticode, script_library, tk_providers, validate_loaded
            native_libraries = loaded_libraries()
            providers = tk_providers(native_libraries)
            assert {'tcl', 'tk'} <= providers.keys(), 'Geladene native Tcl-/Tk-Anbieter fehlen.'
            for provider in providers.values():
                assert Path(provider).resolve().is_relative_to(bundle), 'Geladene Tcl-/Tk-Bibliothek außerhalb des Pakets.'
            loaded_proof = None
            if sys.platform == 'win32':
                loaded_proof = validate_loaded(str(bundle), os.environ['SystemRoot'], native_libraries,
                    programdata=os.environ.get('ProgramData'),
                    authenticate=lambda path: authenticode(path, os.environ['SystemRoot']))
                assert loaded_proof['exitcode'] == 0, loaded_proof['fehler']
            libraries = {}
            for key, command in (("tcl", ("info", "library")), ("tk", ("set", "tk_library"))):
                libraries[key] = script_library(root.tk.call(*command), key, bundle, provider=providers[key])
            core_proof = accessible_core_probe(app, mod, settle) if inputs.get('own_runtime') else None
            assert not errors, errors
            result.update(exitcode=0, app_version=mod.APP_VERSION, python=sys.version.split()[0],
                          tcl=str(root.tk.call("info", "patchlevel")),
                          tk=str(root.tk.call("package", "present", "Tk")), plattform=sys.platform,
                          architektur=platform.machine(), ansichten=len(views)+1,
                          anlegen_abhaken_undo=True, dateilesen=True, app_backup_rundlauf=True,
                          daten_isoliert=True, bibliotheken=libraries,
                          native_anbieter={key:Path(value).resolve().relative_to(bundle).as_posix()
                                           for key,value in providers.items()},
                          windows_geladene_bibliotheken=loaded_proof,
                          ressourcen_sha256_geprueft=len(resources),
                          lizenzdateien_sha256_geprueft=len(inputs["licenses_sha256"]), logo_geladen=True,
                          gebuendelte_schriften_verfuegbar=list(required_families),
                          dnd_version=dnd_version, native_dnd_bibliotheken=dnd_libraries,
                          externe_python_suchpfade=external_paths, callbackfehler=errors, zugangs_kernablauf=core_proof)
        except BaseException as exc:
            result.update(fehler=str(exc), traceback=traceback.format_exc())
        finally:
            if app is not None:
                try:
                    app.cancel_pending_callbacks()
                    app.release_data_lock()
                except Exception as exc:
                    result.update(exitcode=1, abschlussfehler=str(exc))
            if root is not None:
                try:
                    root.destroy()
                except Exception:
                    pass
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return result["exitcode"]


def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--paket-pruefen":
        raise SystemExit(smoke(sys.argv[2]))
    import runtime_diagnostics as diagnostic
    if diagnostic.consume_child_flag():
        diagnostic.start_session()
        import glide_app
        diagnostic.record_phase('imported')
        return glide_app.main()
    command = [sys.executable]
    if not getattr(sys, 'frozen', False):
        command.append(str(Path(__file__).resolve()))
    try:
        input_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / 'glide-input.json'
        metadata = json.loads(input_path.read_text(encoding='utf-8'))
        version = metadata.get('version', '')
        build = metadata.get('sha256', {}).get('app.pyw', '')
    except (OSError, ValueError, TypeError, AttributeError):
        version = build = ''
    return diagnostic.supervise([*command, diagnostic.CHILD_FLAG, *sys.argv[1:]],
                                version=version, build=build)


if __name__ == "__main__":
    raise SystemExit(main())
