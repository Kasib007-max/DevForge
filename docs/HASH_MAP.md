# Hash Map

DevForge's `HashMap` stores key-value pairs and resolves hash collisions with
**separate chaining**. Each bucket contains a small list of entries that map to
the same bucket index.

## Quick start

```python
from devforge.data_structures import HashMap

scores = HashMap()
scores["Ada"] = 98
scores["Grace"] = 95
scores["Linus"] = 92

print(scores["Ada"])          # 98
print("Grace" in scores)      # True

scores["Grace"] = 97          # update an existing key
del scores["Linus"]

for name, score in scores.items():
    print(name, score)
```

The class implements Python's `MutableMapping` interface, so familiar mapping
operations such as `get`, `update`, `pop`, `keys`, `values`, and `items`
are available. Keys must be hashable. Values may be any Python object,
including `None`.

## Collision handling

Different keys can produce the same hash or bucket index. DevForge stores
those entries together in a bucket rather than overwriting an earlier value.

For example, two custom keys may both return `7` from `__hash__`. The map
still distinguishes them using key equality. Deleting one colliding key leaves
the other entries in that bucket intact.

## Capacity and resizing

- The default bucket capacity is 8.
- `initial_capacity` is rounded up to the next power of two.
- `max_load_factor` defaults to 0.75.
- When the load factor (entry count divided by bucket count) exceeds the
  configured maximum, the bucket array doubles and entries are redistributed.
- `capacity` and `load_factor` are read-only properties for inspection.
- `clear()` removes all entries but retains the current capacity.

```python
cache = HashMap(initial_capacity=4, max_load_factor=0.75)
cache["user:42"] = {"name": "Ada"}

print(cache.capacity)
print(cache.load_factor)
```

Iteration visits every key once, but its order is unspecified. Do not rely on
iteration order remaining the same after an insertion or resize.

## Complexity

Let `n` be the number of entries and `b` the number of buckets.

| Operation | Expected | Worst case |
|---|---:|---:|
| Lookup | O(1) | O(n) |
| Insert / update | O(1) amortized | O(n) |
| Delete | O(1) | O(n) |
| Iterate all keys | O(n + b) | O(n + b) |
| Resize | O(n + b) | O(n + b) |

Expected constant-time operations assume keys are distributed reasonably
across buckets. If many keys collide, a bucket becomes a linear chain and
operations on that bucket take O(n). Resizing reduces the load factor but
cannot eliminate collisions caused by identical hash values.

As with Python dictionaries, a key's hash and equality behavior should remain
stable while the key is stored in the map.
