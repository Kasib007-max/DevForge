"""Reusable input parsing and validation helpers."""

from collections.abc import Iterable, Sequence
from typing import TypeVar

T = TypeVar("T")


class InputValidationError(ValueError):
    """Raised when user-provided input does not meet an expected format."""


def parse_integer(value: str, *, field: str = "value") -> int:
    """Parse a base-10 integer from text with a useful validation message."""
    if not isinstance(value, str):
        raise InputValidationError(f"{field} must be provided as text")

    token = value.strip()
    if not token:
        raise InputValidationError(f"{field} cannot be empty")

    try:
        return int(token, 10)
    except ValueError as exc:
        raise InputValidationError(
            f"{field} must be a whole number; received {value!r}"
        ) from exc


def parse_integer_list(
    values: Iterable[str], *, field: str = "values"
) -> list[int]:
    """Parse a non-empty iterable of integer strings into a list of integers.

    Error positions are one-based so they are easy to match to user input.
    """
    parsed: list[int] = []
    for position, value in enumerate(values, start=1):
        parsed.append(parse_integer(value, field=f"{field} item {position}"))

    if not parsed:
        raise InputValidationError(f"{field} must contain at least one integer")

    return parsed


def ensure_sorted_ascending(
    values: Sequence[T], *, field: str = "values"
) -> None:
    """Raise InputValidationError if values are not in ascending order.

    Equal neighboring values are allowed. The input is not modified.
    """
    for index in range(1, len(values)):
        try:
            out_of_order = values[index] < values[index - 1]
        except TypeError as exc:
            raise InputValidationError(
                f"{field} must contain mutually comparable values"
            ) from exc

        if out_of_order:
            raise InputValidationError(
                f"{field} must be sorted in ascending order; "
                f"positions {index} and {index + 1} are out of order"
            )
