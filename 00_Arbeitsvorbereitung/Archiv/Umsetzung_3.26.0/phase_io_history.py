from pathlib import Path
p = Path(__file__).resolve().parents[2] / '01_Repository/Glide/src/glide/app.pyw'
s = p.read_text(encoding='utf-8')
def scoped(name, old, new):
    global s
    a = s.index('    def '+name+'(')
    b = s.find('\n    def ', a+5)
    if b < 0: b = len(s)
    part = s[a:b]
    assert old in part, name
    s = s[:a] + part.replace(old,new,1) + s[b:]
scoped('show_exchange_export_dialog', '            dialog.destroy()\n            self.show_info(', '            self.record_data_operation("exported", pfad)\n            dialog.destroy()\n            self.show_info(')
scoped('show_exchange_import_dialog', '            dialog.destroy()\n            self.set_active_list', '            self.record_data_operation("imported", pfad)\n            dialog.destroy()\n            self.set_active_list')
scoped('show_csv_import_dialog', '                self.show_info("Import erfolgreich",', '                self.record_data_operation("imported", path)\n                self.show_info("Import erfolgreich",')
scoped('show_ics_import_dialog', '                self.show_info("Import erfolgreich",', '                self.record_data_operation("imported", path)\n                self.show_info("Import erfolgreich",')
scoped('show_calendar_export_dialog', '            dialog.destroy()\n            if oeffnen:', '            self.record_data_operation("exported", pfad)\n            dialog.destroy()\n            if oeffnen:')
scoped('import_txt_as_new_lists', '        self.show_info("Import erfolgreich",', '        self.record_data_operation("imported", paths[0] if len(paths) == 1 else f"{len(paths)} Textdateien")\n        self.show_info("Import erfolgreich",')
scoped('import_from_txt', '                self.show_info(\n                    "Import erfolgreich",', '                self.record_data_operation("imported", path)\n                self.show_info(\n                    "Import erfolgreich",')
scoped('import_full_backup', '            self.save_settings()\n            if show_success:', '            self.save_settings()\n            self.record_data_operation("imported", path)\n            if show_success:')
scoped('export_templates_file', '            self.show_info("Vorlagen exportiert",', '            self.record_data_operation("exported", path)\n            self.show_info("Vorlagen exportiert",')
p.write_text(s, encoding='utf-8')
