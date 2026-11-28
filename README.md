# DevForge

**A practical, evolving developer toolkit built from fundamentals to production-minded engineering.**

DevForge is a hands-on software engineering workspace focused on implementing useful tools, core computer science concepts, and reliable development practices. The goal is to build real, tested features—not collect disconnected snippets.

## Project tracks

| Track | Focus |
|---|---|
| Algorithms | Sorting, searching, complexity analysis, and reusable implementations |
| Data structures | Stacks, queues, linked lists, hash maps, trees, heaps, and priority queues |
| Python utilities | Automation scripts, file processing, and validation |
| Developer tooling | Structured JSON logging, configuration, testing, and clean project structure |
| Engineering practice | Documentation, test coverage, and maintainable code |

## Current progress

**Phase 1 — Foundations: complete**

**Phase 2 — Data structures: complete**

- [x] Stack and queue abstractions
- [x] Singly and doubly linked lists
- [x] Hash map with collision handling
- [x] Binary search tree and traversal algorithms
- [x] Heap and priority queue

**Phase 3 — Developer utilities: in progress**

- [x] Structured logging helpers
- [ ] Configuration loading and validation
- [ ] File inventory and duplicate detection
- [ ] Safe batch file operations with dry-run mode
- [ ] JSON and CSV inspection tools

See [the roadmap](docs/ROADMAP.md) for the complete development plan.

## Quick start

```bash
python -m unittest discover -s tests -v
python -m devforge --help
```

Structured logging is available through `from devforge import configure_logging`.
See [the logging guide](docs/LOGGING.md) for examples.

No third-party dependencies are required for the current features.

## Repository layout

```text
DevForge/
├── devforge/          # Algorithms, data structures, validation, and utilities
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
