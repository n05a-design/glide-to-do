import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import errno
import unittest
from windows_isolation import access_denied, acl_snapshot, normalize_environment, plan


class NativeDenialEvidence(unittest.TestCase):
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
