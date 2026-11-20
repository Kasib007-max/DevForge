"""Command-line interface for DevForge."""

import argparse
from collections.abc import Sequence

from devforge.algorithms.searching import binary_search, linear_search
from devforge.algorithms.sorting import merge_sort


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="devforge",
        description="Explore practical algorithms and developer utilities.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    sort_parser = commands.add_parser("sort", help="Sort a list of integers.")
    sort_parser.add_argument("values", nargs="+", type=int)

    search_parser = commands.add_parser("search", help="Search a sorted integer list.")
    search_parser.add_argument("target", type=int)
    search_parser.add_argument("values", nargs="+", type=int)
    search_parser.add_argument(
        "--linear",
        action="store_true",
        help="Use linear search instead of binary search.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "sort":
        print(*merge_sort(args.values))
        return 0

    if args.command == "search":
        if args.linear:
            index = linear_search(args.values, args.target)
        else:
            if args.values != sorted(args.values):
                raise SystemExit("Binary search requires values in ascending order.")
            index = binary_search(args.values, args.target)

        print(index if index >= 0 else "not found")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
