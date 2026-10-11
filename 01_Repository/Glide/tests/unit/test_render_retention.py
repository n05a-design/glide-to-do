"""Differenzabgleich erhält Fokusziele und ersetzt veraltete Aktionen."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src/glide"))
from render_retention import RetainedWidgets, snapshot


class Widget:
    def __init__(self, parent, **options):
        self.master = parent
        self.options = options
        self.children = []
        self.manager = ""
        self.geometry_calls = 0
        self.alive = True
        self.bindings = {}
        self.changed = []

    def winfo_exists(self):
        return self.alive

    def destroy(self):
        self.alive = False

    def configure(self, **options):
        self.changed.append(options)
        self.options.update(options)

    def bind(self, sequence, callback, add=None):
        self.bindings[sequence] = callback

    def pack_slaves(self):
        return list(self.children)

    def winfo_manager(self):
        return self.manager

    def pack(self, **options):
        self.geometry_calls += 1
        host = options.get("in_", self.master)
        if self in host.children:
            host.children.remove(self)
        if "after" in options:
            host.children.insert(host.children.index(options["after"]) + 1, self)
        elif "before" in options:
            host.children.insert(host.children.index(options["before"]), self)
        else:
            host.children.append(self)
        self.manager = "pack"


class RetentionTests(unittest.TestCase):
    def test_changed_content_preserves_target_and_unrelated_scope(self):
        pool = RetainedWidgets(configurable=(Widget,))
        host = object()
        for key in ("a", "b"):
            with pool.scope(key):
                pool.make(Widget, host, text=key)
        pool.end()
        first, second = [record[1] for record in pool.records.values()]
        pool.begin()
        with pool.scope("a"):
            self.assertIs(pool.make(Widget, host, text="neu"), first)
        pool.keep_scope("b")
        pool.end()
        self.assertEqual(first.options["text"], "neu")
        self.assertEqual(first.changed, [{"text": "neu"}])
        self.assertTrue(second.alive)
        pool.begin()
        pool.keep_scope("a")
        pool.end()
        self.assertFalse(second.alive)
        self.assertTrue(first.alive)

    def test_semantic_key_preserves_focus_target_when_optional_content_is_inserted(self):
        pool = RetainedWidgets(configurable=(Widget,))
        host = object()
        heading = pool.make(Widget, host, retention_key="heading", text="Titel")
        pool.end()
        pool.begin()
        cover = pool.make(Widget, host, retention_key="cover", text="Bild")
        self.assertIs(pool.make(Widget, host, retention_key="heading", text="Neu"), heading)
        pool.end()
        self.assertTrue(heading.alive)
        self.assertTrue(cover.alive)
        pool.begin()
        self.assertIs(pool.make(Widget, host, retention_key="heading", text="Neu"), heading)
        pool.end()
        self.assertFalse(cover.alive)

    def test_replaced_host_is_not_reused(self):
        pool = RetainedWidgets()
        host = object()
        first = pool.make(Widget, host, text="a")
        pool.end()
        pool.begin()
        second = pool.make(Widget, object(), text="a")
        pool.end()
        self.assertIsNot(first, second)
        self.assertFalse(first.alive)

    def test_binding_is_registered_once_but_action_is_current(self):
        pool = RetainedWidgets()
        widget = Widget(None)
        calls = []
        pool.bind(widget, "<Return>", lambda event: calls.append("alt"))
        binding = widget.bindings["<Return>"]
        pool.bind(widget, "<Return>", lambda event: calls.append("neu"))
        self.assertIs(widget.bindings["<Return>"], binding)
        binding(None)
        self.assertEqual(calls, ["neu"])

    def test_optional_child_keeps_visual_order_without_repacking_unchanged(self):
        pool = RetainedWidgets(configurable=(Widget,))
        host = Widget(None)
        first, last = Widget(host), Widget(host)
        pool.pack(first)
        pool.pack(last)
        pool.begin()
        pool.pack(first)
        pool.pack(last)
        self.assertEqual(first.geometry_calls, 1)
        self.assertEqual(last.geometry_calls, 1)
        middle = Widget(host)
        pool.begin()
        pool.pack(first)
        pool.pack(middle)
        pool.pack(last)
        self.assertEqual(host.children, [first, middle, last])
        pool.begin()
        pool.pack(last)
        pool.pack(first)
        pool.pack(middle)
        self.assertEqual(host.children, [last, first, middle])

    def test_snapshot_tracks_mutations_and_clone_equivalence(self):
        data = {"id": "a", "items": [{"done": False}]}
        before = snapshot(data)
        self.assertEqual(before, snapshot({"id": "a", "items": [{"done": False}]}))
        data["items"][0]["done"] = True
        self.assertNotEqual(before, snapshot(data))

    def test_keyword_defaults_in_actions_invalidate_cached_command(self):
        def action(text):
            return lambda *, value=text: value
        self.assertEqual(snapshot(action("alt")), snapshot(action("alt")))
        self.assertNotEqual(snapshot(action("alt")), snapshot(action("neu")))


if __name__ == "__main__":
    unittest.main()
