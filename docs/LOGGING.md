# Structured Logging

DevForge provides a JSON Lines logging setup built on Python's standard
`logging` package. It has no third-party dependencies.

## Quick start

```python
from devforge import configure_logging

logger = configure_logging(level="INFO")
logger.info(
    "payment accepted",
    extra={"payment_id": "pay-1042", "amount_minor": 2599},
)
```

Each record is written as one JSON object:

```json
{
  "timestamp": "2026-11-28T13:30:00.123Z",
  "level": "INFO",
  "logger": "devforge",
  "message": "payment accepted",
  "context": {
    "payment_id": "pay-1042",
    "amount_minor": 2599
  }
}
```

The timestamp is UTC. Custom fields passed through Python logging's `extra`
argument are grouped under `context`. Values that are not directly JSON
serializable are converted to strings. Exception information is included in
an `exception` field when a record is logged with exception details, such as
through `logger.exception()`.

## Configuration

`configure_logging` accepts:

| Argument | Default | Purpose |
|---|---|---|
| `logger_name` | `"devforge"` | Logger to configure |
| `level` | `logging.INFO` | Numeric level or name such as `"DEBUG"` |
| `stream` | `sys.stderr` | Text stream receiving JSON lines |

```python
import logging
from devforge import configure_logging

logger = configure_logging(logger_name="my_app", level=logging.DEBUG)
logger.debug("starting import", extra={"source": "customers.csv"})
```

Calling the function again replaces the handler previously installed by
DevForge instead of adding another one. Other handlers already attached by
the application are preserved. Propagation is disabled for the configured
logger so records are not duplicated by root logger handlers.

The helper configures only the selected logger. It does not change the global
root logger or automatically configure logging when DevForge is imported.

## Exception logging

```python
try:
    int("not-a-number")
except ValueError:
    logger.exception(
        "could not parse customer age",
        extra={"customer_id": 42},
    )
```

The formatted traceback is included in the JSON record's `exception` field.

## Design notes

- Uses only the Python standard library.
- Emits one JSON object per line, suitable for log collectors.
- Keeps application-specific metadata separate from standard log fields.
- Does not configure the root logger or produce output merely by importing
  DevForge.
