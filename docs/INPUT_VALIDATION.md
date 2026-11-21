# Input Parsing and Validation

DevForge provides reusable helpers in `devforge.validation`. They keep command-line input handling consistent and make validation easy to reuse from other Python modules.

## Available helpers

- `parse_integer(text, field="value")` converts a string to a base-10 integer. Surrounding whitespace is ignored, while blank text and decimal values such as `"2.5"` are rejected.
- `parse_integer_list(items, field="values")` converts an iterable of integer strings into a non-empty list. Error messages identify the invalid item using a one-based position.
- `ensure_sorted_ascending(values, field="values")` checks that a sequence is in ascending order. Duplicate values are allowed and the original sequence is not modified.

All validation failures raise `InputValidationError`, which is a subclass of `ValueError`.

## Use the command-line interface

Sort integer arguments:

```bash
python -m devforge sort 8 -2 4
# -2 4 8
```

Search a sorted list with binary search:

```bash
python -m devforge search 4 1 4 7
# 1
```

Use linear search when the input is not sorted:

```bash
python -m devforge search 4 7 2 4 --linear
# 2
```

Binary search rejects unsorted input rather than silently returning a potentially incorrect result. Linear search does not require sorted input.

## Use the helpers in Python code

```python
from devforge.validation import (
    ensure_sorted_ascending,
    parse_integer_list,
)

numbers = parse_integer_list(["10", "20", "30"])
ensure_sorted_ascending(numbers)
print(numbers)
```

Catch `InputValidationError` when an application needs to recover from invalid input and display its own message.
