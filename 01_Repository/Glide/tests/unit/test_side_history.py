"""Flüchtiger Nebenansichtsverlauf mit Positionszustand und aktuellen Zielen."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'src/glide'))
from side_view import History, Location, remember_location, visit_location, history_step


class SideHistoryTests(unittest.TestCase):
    def chain(self):
        history=History()
        for value in 'abc': history=visit_location(history,Location(value))
        return history

    def test_first_and_no_duplicate_target(self):
        first=visit_location(History(),Location('a'))
        updated=visit_location(first,Location('a',query='Plan',search_open=True))
        self.assertEqual(len(updated.entries),1)
        self.assertEqual(updated.entries[0].query,'Plan')
        self.assertEqual(first.entries[0].query,'')

    def test_backward_forward_and_edges(self):
        history=self.chain()
        back=history_step(history,-1,'abc')
        self.assertEqual(back.index,1)
        self.assertEqual(history_step(back,1,'abc'),history)
        self.assertEqual(history_step(history,1,'abc'),history)
        self.assertEqual(history_step(History(),-1,'abc'),History())

    def test_deleted_targets_are_skipped(self):
        history=self.chain()
        self.assertEqual(history_step(history,-1,'ac').index,0)
        self.assertEqual(history_step(history,-1,'c'),history)

    def test_branch_replaces_forward_history(self):
        history=history_step(self.chain(),-1,'abc')
        branch=visit_location(history,Location('d'))
        self.assertEqual(tuple(v.list_id for v in branch.entries),('a','b','d'))

    def test_state_snapshot_without_new_station(self):
        history=self.chain()
        updated=remember_location(history,Location('c','task','Straße',True,2,0.75))
        self.assertEqual(updated.index,history.index)
        self.assertEqual(len(updated.entries),3)
        self.assertEqual(updated.entries[2].scroll,0.75)
        self.assertEqual(updated.entries[2].item_id,'task')
        self.assertEqual(remember_location(updated,Location('wrong')),updated)

    def test_limit_and_task_stations(self):
        history=History()
        for n in range(50): history=visit_location(history,Location(str(n)))
        self.assertEqual(len(history.entries),30)
        self.assertEqual(history.entries[0].list_id,'20')
        self.assertEqual(history.index,29)
        history=visit_location(History(),Location('a','one'))
        history=visit_location(history,Location('a','two'))
        self.assertEqual(len(history.entries),2)

    def test_zero_step_and_empty_availability(self):
        history=self.chain()
        self.assertEqual(history_step(history,0,'abc'),history)
        self.assertEqual(history_step(history,-1,()),history)


if __name__=='__main__': unittest.main()
