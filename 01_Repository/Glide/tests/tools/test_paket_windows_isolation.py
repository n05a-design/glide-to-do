import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2] / 'packaging/paket'))
import unittest
from windows_isolation import plan


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
