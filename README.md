# DevForge

**A practical, evolving developer toolkit built from fundamentals to production-minded engineering.**

DevForge is a hands-on software engineering workspace focused on implementing useful tools, core computer science concepts, and reliable development practices. The goal is to build real, tested features—not collect disconnected snippets.

## Project tracks

| Track | Focus |
|---|---|
| Algorithms | Sorting, searching, complexity analysis, and reusable implementations |
| Data structures | Stacks, queues, linked lists, hash maps, trees, and heaps |
| Python utilities | Automation scripts, file processing, and validation |
| Developer tooling | Logging, configuration, testing, and clean project structure |
| Engineering practice | Documentation, test coverage, and maintainable code |

## Current progress

**Phase 2 — Data structures**

- [x] Stack and queue abstractions
- [x] Singly and doubly linked lists
- [x] Hash map with collision handling
- [ ] Binary search tree and traversal algorithms
- [ ] Heap and priority queue

## Quick start

```bash
python -m unittest discover -s tests -v
python -m devforge --help
```

No third-party dependencies are required for the current features.

## Repository layout

```text
DevForge/
├── devforge/          # Algorithms, data structures, validation, and CLI
├── tests/             # Automated unit tests
├── docs/              # Design notes, roadmap, and usage guides
└── README.md
```

## Development principles

1. Prefer readable implementations over clever tricks.
2. Validate inputs and handle edge cases.
3. Add tests alongside new behavior.
4. Explain algorithmic complexity where relevant.
5. Keep each change focused and documented.

## Status

Features are added incrementally. Each completed feature includes tests and documentation before its roadmap item is marked complete.

---
Built as a long-term software engineering practice project.
