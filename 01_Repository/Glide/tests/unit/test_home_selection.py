"""Seitenübergreifende Tagesauswahl folgt frischen IDs, ohne Datenänderung."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
from home_task_tiles import planning_selection


def rows(count):
    return [(None, None, number, {'id':'source'}, {'id':str(number), 'done':False}) for number in range(count)]


class HomeSelectionTests(unittest.TestCase):
    def test_empty_is_one_page(self):
        self.assertEqual(planning_selection([]), dict(rows=(),available=(),selected=(),page=0,pages=1))

    def test_selection_survives_pages_in_source_order(self):
        values=rows(23)
        result=planning_selection(values, ('22','1','11','missing'), page=1)
        self.assertEqual(result['selected'], ('1','11','22'))
        self.assertEqual(result['rows'],tuple(values[10:20]))
        self.assertEqual(result['pages'],3)
        self.assertEqual(len(result['available']),23)

    def test_done_removed_and_duplicate_do_not_count(self):
        values=rows(3);values[0][-1]['done']=True;values.append(values[1])
        result=planning_selection(values, ('0','1','missing'))
        self.assertEqual(result['available'],('1','2'))
        self.assertEqual(result['selected'],('1',))

    def test_clamps_page_after_tasks_leave(self):
        self.assertEqual(planning_selection(rows(2),page=8)['page'],0)
        self.assertEqual(planning_selection(rows(23),page=-1)['page'],0)

    def test_new_objects_after_undo_and_no_mutation(self):
        original=rows(2); current=deepcopy(original); before=deepcopy(current)
        result=planning_selection(current, ('1',))
        self.assertIs(result['rows'][1][-1],current[1][-1])
        self.assertIsNot(result['rows'][1][-1],original[1][-1])
        self.assertEqual(current,before)

    def test_invalid_ids_and_zero_size(self):
        values=rows(3);values[0][-1]['id']='';values[1][-1]['id']=False
        result=planning_selection(values,page_size=0)
        self.assertEqual(result['available'],('2',))
        self.assertEqual(result['pages'],1)


if __name__=='__main__': unittest.main()
