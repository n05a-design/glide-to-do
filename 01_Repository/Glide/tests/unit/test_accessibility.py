import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src' / 'glide'))

import unittest
from accessibility import Attributes, task_value, set_attributes, screenreader_active


class AccessibleValues(unittest.TestCase):
    def test_plan_and_due_remain_distinct_and_original_is_unchanged(self):
        item = dict(text="Angebot\n  prüfen", planned_date="2026-10-12", planned_time="09:30",
                    due="2026-10-14", due_time="16:00", importance=3, estimated_minutes=45,
                    repeat={"rule": "weekly"}, reminder={"time": "08:00"}, children=[{}])
        before = copy.deepcopy(item)
        value = task_value(item, label_names=("Haus am See",), blocked_titles=("Freigabe",))
        for text in ("Angebot prüfen", "Bearbeitungstag 12.10.2026 um 09:30", "Fällig 14.10.2026 um 16:00",
                     "Wichtigkeit hoch", "45 Minuten", "Wiederkehrend", "Erinnerung gesetzt",
                     "Wartet auf Freigabe", "Labels Haus am See", "1 Unterpunkt"):
            self.assertIn(text, value)
        self.assertEqual(item, before)

    def test_empty_dates_and_missing_estimate_are_explicit(self):
        value = task_value({"text": "Rückruf", "done": True, "due_time": "12:00"})
        for text in ("Erledigt", "Nicht eingeplant", "Ohne Fälligkeit", "Aufwand nicht geschätzt"):
            self.assertIn(text, value)
        self.assertNotIn("12:00", value)

    def test_structural_rows_are_not_announced_as_tasks(self):
        for kind, expected in (("group", "Gruppe"), ("heading", "Überschrift")):
            value = task_value(dict(text="Abschnitt", kind=kind, due="defekt", importance=99, done=True))
            self.assertIn(expected, value)
            self.assertNotIn("Erledigt", value)
            self.assertNotIn("Fällig", value)

    def test_invalid_values_do_not_produce_wrong_spoken_values(self):
        for fields in (dict(due="kein Datum"), dict(importance=True), dict(estimated_minutes=True),
                       dict(importance=4), dict(estimated_minutes=-2)):
            with self.assertRaises(ValueError):
                task_value(dict(text="Aufgabe", **fields))

    def test_unknown_internal_ids_are_not_substituted_for_names(self):
        value = task_value(dict(text="Aufgabe", labels=["label-uuid"], blocked_by=["task-uuid"]))
        self.assertNotIn("uuid", value)
        self.assertNotIn("Labels", value)
        self.assertNotIn("Wartet", value)

    def test_native_contract_requires_role_before_name_and_keeps_action_list(self):
        table = {}
        def native(command, window, value=None):
            if command == "tk":
                return "win32"
            key = command.removeprefix("::tk::accessible::set_acc_")
            if key != "role" and window not in table:
                raise RuntimeError("No table found. You must set the accessibility role first.")
            table.setdefault(window, {})[key] = value
        action = ("safe_command", "Text mit Leerzeichen; [kein Skript]")
        attrs = Attributes("Button", "Einplanen", value="Heute", action=action)
        set_attributes(native, ".plan", attrs)
        self.assertEqual(table[".plan"]["action"], action)
        self.assertEqual(table[".plan"]["name"], "Einplanen")
        with self.assertRaises(ValueError):
            Attributes("Frame", "Rahmen")
        with self.assertRaises(ValueError):
            Attributes("Button", "Einplanen", action="eval fremder_text")

    def test_aqua_button_label_uses_name_without_losing_description(self):
        for system in ("aqua", "win32", "x11"):
            values = {}
            def native(*args):
                if args == ("tk", "windowingsystem"):
                    return system
                values[args[0].removeprefix("::tk::accessible::set_acc_")] = args[2]
            attrs = Attributes("Button", "Aufgabe speichern", description="Änderungen übernehmen")
            set_attributes(native, ".save", attrs)
            expected = "Aufgabe speichern. Änderungen übernehmen" if system == "aqua" else "Änderungen übernehmen"
            self.assertEqual(values["description"], expected)
            self.assertEqual(values["name"], "Aufgabe speichern")

    def test_native_checkbox_state_requires_binary_values(self):
        for value in ("Offen", "Erledigt", "", "true"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "0 oder 1"):
                Attributes("Checkbutton", "Aufgabe erledigt", value=value)
        for value in ("0", "1"):
            self.assertEqual(Attributes("Checkbutton", "Aufgabe erledigt", value=value).value, value)

    def test_checkbox_role_matches_the_native_platform_tables(self):
        for system, role in (("aqua", "Checkbutton"), ("win32", "Checkbutton"), ("x11", "Checkbox")):
            values = {}
            def native(*args):
                if args == ("tk", "windowingsystem"):
                    return system
                values[args[0].removeprefix("::tk::accessible::set_acc_")] = args[2]
            set_attributes(native, ".done", Attributes("Checkbutton", "Aufgabe erledigt", value="1"))
            self.assertEqual((values["role"], values["value"]), (role, "1"))

    def test_unavailable_native_reader_warning_is_inactive(self):
        warning = 'Warning: Tk accessibility support not available in this build.'
        self.assertFalse(screenreader_active(lambda *args: warning))

    def test_inactive_native_reader_can_return_zero_or_empty(self):
        for value in (0, '0', '', None, False):
            with self.subTest(value=value):
                self.assertFalse(screenreader_active(lambda *args: value))
        for value in (1, '1', True):
            with self.subTest(value=value):
                self.assertTrue(screenreader_active(lambda *args: value))


if __name__ == "__main__":
    unittest.main()
