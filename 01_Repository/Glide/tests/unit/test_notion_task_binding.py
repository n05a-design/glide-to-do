import copy
import itertools
import unittest
import notion_archive as notion
from test_notion_archive import archive, ROOT


class TaskBindingTests(unittest.TestCase):
    def setUp(self):
        export = notion.inspect_export(archive({ROOT: '# Seite\n\n- [ ] Prüfen 😀\n- [x] Fertig\n'}))
        self.document = notion.page_document(export, export.pages[0], {}, {})
        self.ids = itertools.count()

    def factory(self, text, done=False):
        return dict(id='task-'+str(next(self.ids)), text=text, done=done, kind='task')

    def test_checkboxes_are_real_tasks_with_unique_refs_and_source_unchanged(self):
        original = copy.deepcopy(self.document)
        document, items = notion.bind_page_tasks(self.document, self.factory)
        self.assertEqual([item['done'] for item in items], [False, True])
        self.assertEqual([item['text'] for item in items], ['Prüfen 😀', 'Fertig'])
        self.assertEqual({s['tag'] for s in document['spans'] if s['tag'].startswith('item:')}, {'item:task-0', 'item:task-1'})
        self.assertNotIn('tasks', document)
        self.assertEqual(self.document, original)
        self.assertEqual(document['text'], original['text'])
        self.assertEqual(document['links'], original['links'])

    def test_missing_or_unrepresented_tasks_are_rejected(self):
        for which in ('missing-task', 'missing-span'):
            broken = copy.deepcopy(self.document)
            if which == 'missing-task':
                broken['tasks'].pop()
            else:
                broken['spans'] = [span for span in broken['spans'] if span['tag'] != 'taskref:1']
            original = copy.deepcopy(broken)
            with self.subTest(which=which), self.assertRaises(notion.NotionFormatError):
                notion.bind_page_tasks(broken, self.factory)
            self.assertEqual(broken, original)

    def test_duplicate_source_or_generated_ids_are_rejected(self):
        broken = copy.deepcopy(self.document)
        broken['tasks'][1]['ref'] = 0
        with self.assertRaises(notion.NotionFormatError):
            notion.bind_page_tasks(broken, self.factory)
        with self.assertRaises(notion.NotionFormatError):
            notion.bind_page_tasks(self.document, lambda text, done:dict(id='same', text=text, done=done))

    def test_plain_page_and_invalid_task_data(self):
        plain = dict(text='Text', spans=[], links={}, images={})
        document, items = notion.bind_page_tasks(plain, self.factory)
        self.assertEqual((document, items), (plain, ()))
        for field, value in (('ref', True), ('text', False), ('done', 'false')):
            broken = copy.deepcopy(self.document)
            broken['tasks'][0][field] = value
            with self.subTest(field=field), self.assertRaises(notion.NotionFormatError):
                notion.bind_page_tasks(broken, self.factory)


if __name__ == '__main__':
    unittest.main()
