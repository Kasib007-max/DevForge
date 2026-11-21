"""Command-line interface for DevForge."""

import argparse
from collections.abc import Sequence

from devforge.algorithms.searching import binary_search, linear_search
from devforge.algorithms.sorting import merge_sort
from devforge.validation import (
    InputValidationError,
    ensure_sorted_ascending,
    parse_integer,
    parse_integer_list,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devforge",
        description="Explore practical algorithms and developer utilities.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    sort_parser = commands.add_parser("sort", help="Sort a list of integers.")
    sort_parser.add_argument("values", nargs="+")

    search_parser = commands.add_parser("search", help="Search an integer list.")
    search_parser.add_argument(
        "target", type=lambda raw: parse_integer(raw, field="target")
    )
    search_parser.add_argument("values", nargs="+")
    search_parser.add_argument(
        "--linear",
        action="store_true",
        help="Use linear search instead of binary search.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        values = parse_integer_list(args.values)
    except InputValidationError as exc:
        parser.error(str(exc))

    if args.command == "sort":
        print(*merge_sort(values))
        return 0

    if args.command == "search":
        if args.linear:
            index = linear_search(values, args.target)
        else:
            try:
                ensure_sorted_ascending(values)
            except InputValidationError as exc:
                parser.error(str(exc))
            index = binary_search(values, args.target)

        print(index if index >= 0 else "not found")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
