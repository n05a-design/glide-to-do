import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import errno
import unittest
import tempfile
from pathlib import Path
from windows_isolation import access_denied, acl_rules, acl_snapshot, normalize_environment, plan, restoration_entries, restoration_security_information, isolation_probe


class NativeDenialEvidence(unittest.TestCase):
    def test_native8_protected_python_sources_keep_protection_and_explicit_aces(self):
        original = 'D:P(A;;FA;;;BA)(A;;FA;;;SY)(A;;0x1200a9;;;BU)'
        rewritten = 'D:(A;ID;FA;;;BA)(A;ID;FA;;;SY)(A;ID;0x1200a9;;;BU)'
        self.assertNotEqual(acl_rules({'token.py': original}), acl_rules({'token.py': rewritten}))
        self.assertEqual(restoration_security_information(original), 0x80000004)
        for header in ('D:', 'D:AI', 'D:ARAI'):
            self.assertEqual(restoration_security_information(header+'(A;ID;FA;;;SY)'), 0x20000004)
        self.assertEqual(restoration_security_information('D:PAI(A;;FA;;;SY)'), 0x80000004)

    def test_native_acl_flags_reject_non_dacl_or_unknown_header(self):
        for dacl in ('S:(A;;FA;;;SY)', '', 'D:unknown(A;;FA;;;SY)'):
            with self.subTest(dacl=dacl), self.assertRaises(ValueError):
                restoration_security_information(dacl)

    def test_acl_rules_only_ignore_auto_inherited_descriptor_model_marker(self):
        original={'x64':'D:AI(A;OICIID;FA;;;SY)', 'x64\\python.exe':'D:AI(A;ID;0x1301bf;;;AU)'}
        after={name:dacl.replace('D:AI','D:') for name,dacl in original.items()}
        self.assertNotEqual(original,after)
        self.assertEqual(acl_rules(original),acl_rules(after))
        self.assertEqual(original['x64'],'D:AI(A;OICIID;FA;;;SY)')

    def test_acl_rule_comparison_keeps_protection_request_and_every_ace_bit(self):
        original={'x64':'D:AI(A;OICIID;FA;;;SY)(A;ID;RX;;;BU)'}
        for dacl in ('D:PAI(A;OICIID;FA;;;SY)(A;ID;RX;;;BU)',
                     'D:ARAI(A;OICIID;FA;;;SY)(A;ID;RX;;;BU)',
                     'D:AI(A;OICIID;RX;;;SY)(A;ID;RX;;;BU)',
                     'D:AI(A;ID;FA;;;SY)(A;ID;RX;;;BU)',
                     'D:AI(A;OICIID;FA;;;BA)(A;ID;RX;;;BU)',
                     'D:AI(A;ID;RX;;;BU)(A;OICIID;FA;;;SY)'):
            with self.subTest(dacl=dacl):
                self.assertNotEqual(acl_rules(original),acl_rules({'x64':dacl}))

    def test_previous_icacls_python_file_reinheritance_remains_a_failure(self):
        original={'python.exe':'D:AI(A;ID;0x1301bf;;;AU)(A;ID;FA;;;SY)'}
        rewritten={'python.exe':'D:AI(A;ID;0x1301bf;;;AU)(A;OICIIOID;SDGXGWGR;;;AU)(A;OICIID;FA;;;SY)'}
        self.assertNotEqual(acl_rules(original),acl_rules(rewritten))

    def test_acl_rule_comparison_requires_the_complete_same_file_set(self):
        original={'x64':'D:AI(A;ID;FA;;;SY)', 'x64\\python.exe':'D:AI(A;ID;FA;;;SY)'}
        self.assertNotEqual(acl_rules(original),acl_rules({'x64':original['x64']}))
        self.assertNotEqual(acl_rules(original),acl_rules(dict(original,foreign=original['x64'])))

    def test_original_acl_restore_targets_only_the_saved_tree_and_parent_first(self):
        source = r'C:\Python\x64'
        entries = restoration_entries(source, {r'x64\python.exe':'D:AI(A;ID;FA;;;SY)',
                                               r'x64':'D:(A;OICI;FA;;;SY)'})
        self.assertEqual([path for path, _ in entries], [source, source+r'\python.exe'])
        self.assertEqual(entries[0][1], 'D:(A;OICI;FA;;;SY)')

    def test_acl_restore_rejects_parent_escape_absolute_paths_and_foreign_sibling(self):
        for name in (r'x64\..\foreign', r'C:\Other', r'other\python.exe', r'\system'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                restoration_entries(r'C:\Python\x64', {'x64':'D:AI', name:'D:AI'})

    def test_acl_restore_requires_root_descriptor_and_valid_dacl(self):
        for snapshot in ({}, {r'x64\python.exe':'D:AI'}, {'x64':'S:'}):
            with self.subTest(snapshot=snapshot), self.assertRaises(ValueError):
                restoration_entries(r'C:\Python\x64', snapshot)

    def test_crt_fileio_eacces_and_native_winerror_are_both_access_denied(self):
        self.assertTrue(access_denied(PermissionError(errno.EACCES, 'Permission denied')))
        native = OSError('Access denied')
        native.winerror = 5
        self.assertTrue(access_denied(native))

    def test_unrelated_missing_file_and_other_os_failures_do_not_prove_denial(self):
        for error in (FileNotFoundError(errno.ENOENT, 'Missing'),
                      OSError(errno.EIO, 'I/O error'), PermissionError(errno.EPERM, 'Not permitted')):
            with self.subTest(error=error):
                self.assertFalse(access_denied(error))

    def test_acl_comparison_preserves_every_dacl_but_ignores_enumeration_order(self):
        before = 'Python\\\r\nD:AI(A;OICI;FA;;;SY)\r\nPython\\python.exe\r\nD:AI(A;ID;FA;;;SY)\r\n'
        after = 'Python\\python.exe\r\nD:AI(A;ID;FA;;;SY)\r\nPython\\\r\nD:AI(A;OICI;FA;;;SY)\r\n'
        snapshot = acl_snapshot(before.encode('utf-16'))
        self.assertEqual(snapshot, acl_snapshot(after.encode('utf-16')))
        self.assertNotEqual(snapshot, acl_snapshot(after.replace(';FA;', ';RX;', 1).encode('utf-16')))
        self.assertNotEqual(snapshot, acl_snapshot('Python\\\r\nD:AI(A;OICI;FA;;;SY)\r\n'.encode('utf-16')))

    def test_incomplete_duplicate_and_malformed_acl_backups_are_rejected(self):
        for text in ('', 'Python\r\n', 'Python\r\ninvalid\r\n',
                     'Python\r\nD:AI\r\nPython\r\nD:AI\r\n'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                acl_snapshot(text.encode('utf-16'))


class RuntimeReadProbe(unittest.TestCase):
    def test_own_runtime_requires_real_binary_and_preserves_existing_source_probes(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder).resolve()
            (base/'runtime-bau.json').write_text('{}')
            self.assertIsNone(isolation_probe(base))
            native = base/'python-extension/_tkinter.cp314-win_amd64.pyd'
            native.parent.mkdir();native.write_bytes(b'own-native-extension')
            self.assertEqual(isolation_probe(base), native)
            (base/'python.exe').write_bytes(b'python')
            self.assertEqual(isolation_probe(base), base/'python.exe')

    def test_link_outside_the_blocked_source_cannot_prove_denial(self):
        with tempfile.TemporaryDirectory() as folder:
            base=Path(folder);source=base/'source';source.mkdir()
            external=base/'external';external.write_bytes(b'outside')
            try:
                (source/'python.exe').symlink_to(external)
            except OSError:
                self.skipTest('Prüfstand erlaubt keine temporären Dateisymlinks')
            self.assertIsNone(isolation_probe(source))


class HostedIsolationBoundary(unittest.TestCase):
    def setUp(self):
        self.environment={'GITHUB_ACTIONS':'true','CI':'true','RUNNER_ENVIRONMENT':'github-hosted','RUNNER_OS':'Windows',
            'RUNNER_TEMP':r'D:\a\_temp','RUNNER_TOOL_CACHE':r'C:\hostedtoolcache\windows',
            'GITHUB_WORKSPACE':r'D:\a\glide\glide','SystemRoot':r'C:\Windows'}
        self.package=r'D:\a\_temp\paket\Glide';self.report=r'D:\a\_temp\nachweis\start.json'
        self.python=r'C:\hostedtoolcache\windows\Python\3.14.7\x64'

    def test_only_owned_ci_sources_are_accepted_and_nested_paths_are_combined(self):
        result=plan(self.environment,self.package,self.report,[self.python,self.python+r'\DLLs',r'D:\a\glide\glide'])
        self.assertEqual(len(result['forbidden']),2)
        self.assertIn(self.python,result['forbidden'])

    def test_real_windows_uppercase_environment_has_the_same_boundary(self):
        native = {key.upper(): value for key,value in self.environment.items()}
        before = dict(native)
        self.assertEqual(plan(native,self.package,self.report,[self.python]),
                         plan(self.environment,self.package,self.report,[self.python]))
        self.assertEqual(native,before)
        self.assertEqual(normalize_environment(self.environment)['SYSTEMROOT'], r'C:\Windows')

    def test_conflicting_case_variants_are_refused_before_any_acl_change(self):
        with self.assertRaisesRegex(ValueError,'Widersprüchliche'):
            plan(dict(self.environment,SYSTEMROOT=r'D:\Anderes'),self.package,self.report,[self.python])

    def test_human_windows_and_self_hosted_machines_are_always_rejected(self):
        for key,value in [('GITHUB_ACTIONS','false'),('CI','false'),('RUNNER_ENVIRONMENT','self-hosted'),('RUNNER_OS','macOS')]:
            with self.subTest(key=key),self.assertRaisesRegex(ValueError,'Hosted-Windows'):
                plan(dict(self.environment,**{key:value}),self.package,self.report,[self.python])

    def test_package_report_and_system_library_paths_cannot_be_blocked(self):
        for path in [self.package,r'D:\a\_temp\paket',r'D:\a\_temp\nachweis',r'C:\Windows',r'C:\Windows\System32']:
            with self.subTest(path=path),self.assertRaises(ValueError):
                plan(self.environment,self.package,self.report,[path])

    def test_user_installations_and_unrelated_ci_tools_remain_out_of_scope(self):
        for path in [r'C:\Inhaber\Python',r'C:\Program Files\Python',r'C:\hostedtoolcache\windows',
                     r'C:\hostedtoolcache\windows\Node','C:\\',r'D:\a\_temp']:
            with self.subTest(path=path),self.assertRaises(ValueError):
                plan(self.environment,self.package,self.report,[path])

    def test_unc_relative_parent_traversal_and_drive_relative_paths_are_rejected(self):
        for path in [r'\\server\share\Python',r'C:Python',r'Python',r'D:\a\_temp\..\Python']:
            with self.subTest(path=path),self.assertRaises(ValueError):
                plan(self.environment,self.package,self.report,[path])

    def test_case_variants_cannot_evade_overlap_checks(self):
        with self.assertRaises(ValueError):
            plan(self.environment,self.package,self.report,[r'd:\A\_TEMP\PAKET'])

    def test_output_in_user_folder_or_inside_package_is_rejected(self):
        for package,report in [(r'C:\Inhaber\Glide',self.report),
                               (self.package,self.package+r'\start.json'),
                               (self.package,r'C:\Inhaber\start.json')]:
            with self.subTest(package=package,report=report),self.assertRaises(ValueError):
                plan(self.environment,package,report,[self.python])


if __name__=='__main__':unittest.main()
