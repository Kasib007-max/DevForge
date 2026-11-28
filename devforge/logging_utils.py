"""Small, dependency-free helpers for structured application logging."""

from __future__ import annotations

import datetime as _datetime
import json
import logging
import sys
from typing import Any, TextIO

_STANDARD_RECORD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__) | {
    "message", "asctime",
}
_HANDLER_MARKER = "_devforge_managed_handler"


class JsonLogFormatter(logging.Formatter):
    """Format each log record as one JSON object (JSON Lines).

    Values supplied through EXTRA fields are grouped under context.
    Non-JSON-native values are converted with str so logging cannot fail
    solely because an application attached an unusual value.
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = _datetime.datetime.fromtimestamp(
            record.created, tz=_datetime.timezone.utc
        )
        payload: dict[str, Any] = {
            "timestamp": timestamp.isoformat(timespec="milliseconds").replace(
                "+00:00", "Z"
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        context = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _STANDARD_RECORD_FIELDS and not key.startswith("_")
        }
        if context:
            payload["context"] = context
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            payload["stack"] = self.formatStack(record.stack_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


def _resolve_level(level: int | str) -> int:
    """Convert a numeric or named logging level into its integer value."""
    if isinstance(level, bool):
        raise ValueError("logging level must be an integer or level name")
    if isinstance(level, int):
        if level < 0:
            raise ValueError("logging level cannot be negative")
        return level
    if isinstance(level, str):
        resolved = logging.getLevelName(level.strip().upper())
        if isinstance(resolved, int):
            return resolved
    raise ValueError(f"unknown logging level: {level!r}")


def configure_logging(
    *,
    logger_name: str = "devforge",
    level: int | str = logging.INFO,
    stream: TextIO | None = None,
) -> logging.Logger:
    """Configure a named logger to emit structured JSON Lines to a stream.

    Repeated calls replace only the handler previously installed by DevForge;
    unrelated application handlers are preserved. Propagation is disabled to
    prevent duplicate output from root logger handlers. The default stream is
    sys.stderr. Importing DevForge does not configure logging automatically.
    """
    if not isinstance(logger_name, str) or not logger_name.strip():
        raise ValueError("logger_name must be a non-empty string")

    numeric_level = _resolve_level(level)
    logger = logging.getLogger(logger_name.strip())
    for handler in tuple(logger.handlers):
        if getattr(handler, _HANDLER_MARKER, False):
            logger.removeHandler(handler)
            handler.close()

    handler = logging.StreamHandler(stream if stream is not None else sys.stderr)
    setattr(handler, _HANDLER_MARKER, True)
    handler.setLevel(numeric_level)
    handler.setFormatter(JsonLogFormatter())
    logger.addHandler(handler)
    logger.setLevel(numeric_level)
    logger.propagate = False
    return logger
