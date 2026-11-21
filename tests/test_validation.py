"""Unit tests for reusable input validation helpers."""

import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from devforge.cli import main
from devforge.validation import (
    InputValidationError,
    ensure_sorted_ascending,
    parse_integer,
    parse_integer_list,
)


class IntegerParsingTests(unittest.TestCase):
    def test_parse_integer_trims_whitespace_and_accepts_signs(self) -> None:
        self.assertEqual(parse_integer("  -42 "), -42)
        self.assertEqual(parse_integer("+7"), 7)

    def test_parse_integer_rejects_blank_and_non_integer_text(self) -> None:
        for raw in ("", "   ", "3.14", "hello"):
            with self.subTest(raw=raw):
                with self.assertRaises(InputValidationError):
                    parse_integer(raw)

    def test_parse_integer_list_reports_one_based_item_position(self) -> None:
        self.assertEqual(parse_integer_list(["3", "-1", " 8 "]), [3, -1, 8])
        with self.assertRaisesRegex(InputValidationError, "item 2"):
            parse_integer_list(["3", "two"])

    def test_parse_integer_list_rejects_empty_input(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "at least one"):
            parse_integer_list([])


class SortedInputTests(unittest.TestCase):
    def test_accepts_sorted_values_and_duplicates(self) -> None:
        self.assertIsNone(ensure_sorted_ascending([1, 2, 2, 5]))

    def test_rejects_first_out_of_order_pair(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "positions 2 and 3"):
            ensure_sorted_ascending([1, 5, 3, 7])

    def test_rejects_values_that_cannot_be_compared(self) -> None:
        with self.assertRaisesRegex(InputValidationError, "comparable"):
            ensure_sorted_ascending([1, "two"])


class CommandLineValidationTests(unittest.TestCase):
    def test_sort_parses_integer_arguments(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["sort", "8", "-2", "4"]), 0)
        self.assertEqual(output.getvalue(), "-2 4 8\n")

    def test_binary_search_rejects_unsorted_values(self) -> None:
        error = StringIO()
        with redirect_stderr(error):
            with self.assertRaises(SystemExit) as raised:
                main(["search", "4", "8", "2", "4"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("sorted in ascending order", error.getvalue())

    def test_linear_search_allows_unsorted_values(self) -> None:
        output = StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(["search", "4", "8", "2", "4", "--linear"]), 0)
        self.assertEqual(output.getvalue(), "2\n")


if __name__ == "__main__":
    unittest.main()
