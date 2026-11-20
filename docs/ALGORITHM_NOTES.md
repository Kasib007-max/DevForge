# Algorithm Notes

## Binary search

Binary search works on a sequence sorted in ascending order. It compares the target with the middle element and discards the half that cannot contain the target.

- Best case: O(1), when the middle element is the target.
- Worst and average case: O(log n).
- Auxiliary space: O(1) for the iterative implementation.

The sorted-input precondition matters. Binary search does not reliably work on arbitrary unsorted data.

## Linear search

Linear search checks values from left to right and returns the first matching index.

- Best case: O(1).
- Worst and average case: O(n).
- Auxiliary space: O(1).

It works on unsorted sequences and is often the simplest choice for small inputs.

## Merge sort

Merge sort divides a sequence into halves, recursively sorts each half, and merges the sorted halves.

- Time complexity: O(n log n) in best, average, and worst cases.
- Auxiliary space: O(n).
- Stability: stable when equal elements are taken from the left half first.

Merge sort provides predictable runtime, at the cost of additional memory.
