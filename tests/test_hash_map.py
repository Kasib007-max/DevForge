"""Tests for the separate-chaining hash map."""

import unittest

from devforge.data_structures import HashMap


class CollisionKey:
    """Hashable test key that deliberately collides with every peer."""

    def __init__(self, label: str) -> None:
        self.label = label

    def __hash__(self) -> int:
        return 7

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CollisionKey) and self.label == other.label


class HashMapTests(unittest.TestCase):
    def test_basic_insert_lookup_and_length(self) -> None:
        values = HashMap()
        values["name"] = "DevForge"
        values["version"] = 1
        self.assertEqual(values["name"], "DevForge")
        self.assertEqual(values["version"], 1)
        self.assertEqual(len(values), 2)

    def test_overwriting_a_key_does_not_increase_length(self) -> None:
        values = HashMap([("language", "Python")])
        values["language"] = "Python 3"
        self.assertEqual(values["language"], "Python 3")
        self.assertEqual(len(values), 1)

    def test_separate_chaining_keeps_colliding_keys_distinct(self) -> None:
        first, second, third = (
            CollisionKey("first"),
            CollisionKey("second"),
            CollisionKey("third"),
        )
        values = HashMap()
        values[first] = 10
        values[second] = 20
        values[third] = 30
        self.assertEqual((values[first], values[second], values[third]), (10, 20, 30))
        self.assertEqual(len(values), 3)

    def test_deleting_one_collision_preserves_the_others(self) -> None:
        first, second = CollisionKey("first"), CollisionKey("second")
        values = HashMap([(first, "a"), (second, "b")])
        del values[first]
        self.assertNotIn(first, values)
        self.assertEqual(values[second], "b")
        self.assertEqual(len(values), 1)

    def test_resize_preserves_entries_and_increases_capacity(self) -> None:
        values = HashMap(initial_capacity=2, max_load_factor=0.75)
        original_capacity = values.capacity
        for number in range(20):
            values[number] = number * number
        self.assertGreater(values.capacity, original_capacity)
        self.assertEqual(len(values), 20)
        for number in range(20):
            self.assertEqual(values[number], number * number)

    def test_missing_key_raises_key_error(self) -> None:
        values = HashMap()
        with self.assertRaises(KeyError):
            _ = values["missing"]
        with self.assertRaises(KeyError):
            del values["missing"]

    def test_none_values_are_not_confused_with_missing_keys(self) -> None:
        values = HashMap()
        values["present"] = None
        self.assertIn("present", values)
        self.assertIsNone(values["present"])
        self.assertNotIn("absent", values)

    def test_mapping_helpers_update_get_and_pop(self) -> None:
        values = HashMap()
        values.update({"a": 1, "b": 2})
        self.assertEqual(values.get("a"), 1)
        self.assertEqual(values.pop("b"), 2)
        self.assertEqual(values.get("b", "default"), "default")
        self.assertEqual(dict(values.items()), {"a": 1})

    def test_iteration_visits_every_key_once(self) -> None:
        values = HashMap((number, str(number)) for number in range(12))
        self.assertEqual(set(values), set(range(12)))
        self.assertEqual(len(list(values)), 12)

    def test_clear_retains_capacity_and_resets_size(self) -> None:
        values = HashMap([(1, "one"), (2, "two")], initial_capacity=4)
        capacity = values.capacity
        values.clear()
        self.assertEqual(len(values), 0)
        self.assertEqual(values.capacity, capacity)
        self.assertEqual(list(values), [])

    def test_unhashable_keys_raise_type_error(self) -> None:
        values = HashMap()
        with self.assertRaises(TypeError):
            values[["mutable"]] = "value"

    def test_capacity_rounds_up_to_power_of_two(self) -> None:
        self.assertEqual(HashMap(initial_capacity=5).capacity, 8)

    def test_invalid_configuration_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            HashMap(initial_capacity=0)
        with self.assertRaises(ValueError):
            HashMap(max_load_factor=0)
        with self.assertRaises(ValueError):
            HashMap(max_load_factor=float("nan"))
        with self.assertRaises(TypeError):
            HashMap(initial_capacity=2.5)


if __name__ == "__main__":
    unittest.main()
