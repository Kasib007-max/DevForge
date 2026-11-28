"""Tests for DevForge's structured logging helpers."""

from __future__ import annotations

import json
import logging
import sys
import unittest
from io import StringIO

from devforge.logging_utils import JsonLogFormatter, configure_logging


class JsonLogFormatterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.formatter = JsonLogFormatter()

    def test_formats_core_fields_and_interpolated_message(self) -> None:
        record = logging.LogRecord(
            "devforge.tests", logging.INFO, __file__, 12,
            "processed %d records", (4,), None
        )
        payload = json.loads(self.formatter.format(record))
        self.assertEqual(payload["level"], "INFO")
        self.assertEqual(payload["logger"], "devforge.tests")
        self.assertEqual(payload["message"], "processed 4 records")
        self.assertTrue(payload["timestamp"].endswith("Z"))

    def test_groups_extra_fields_under_context(self) -> None:
        record = logging.LogRecord(
            "devforge.tests", logging.WARNING, __file__, 20,
            "request rejected", (), None
        )
        record.request_id = "req-123"
        record.status_code = 422
        payload = json.loads(self.formatter.format(record))
        self.assertEqual(
            payload["context"],
            {"request_id": "req-123", "status_code": 422},
        )

    def test_non_json_context_values_are_stringified(self) -> None:
        record = logging.LogRecord(
            "devforge.tests", logging.INFO, __file__, 25, "value", (), None
        )
        record.custom_value = object()
        payload = json.loads(self.formatter.format(record))
        self.assertIsInstance(payload["context"]["custom_value"], str)

    def test_includes_exception_details(self) -> None:
        try:
            raise RuntimeError("sample failure")
        except RuntimeError:
            exception_info = sys.exc_info()
        record = logging.LogRecord(
            "devforge.tests", logging.ERROR, __file__, 30,
            "operation failed", (), exception_info
        )
        payload = json.loads(self.formatter.format(record))
        self.assertIn("RuntimeError: sample failure", payload["exception"])


class ConfigureLoggingTests(unittest.TestCase):
    def tearDown(self) -> None:
        for name in ("devforge.test", "devforge.invalid"):
            logger = logging.getLogger(name)
            for handler in tuple(logger.handlers):
                logger.removeHandler(handler)
                handler.close()

    def test_configures_json_output_to_supplied_stream(self) -> None:
        output = StringIO()
        logger = configure_logging(
            logger_name="devforge.test", level="DEBUG", stream=output
        )
        logger.debug("cache refreshed", extra={"cache_size": 8})
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["level"], "DEBUG")
        self.assertEqual(payload["message"], "cache refreshed")
        self.assertEqual(payload["context"]["cache_size"], 8)
        self.assertFalse(logger.propagate)

    def test_reconfiguration_does_not_duplicate_devforge_handlers(self) -> None:
        output = StringIO()
        logger = configure_logging(logger_name="devforge.test", stream=output)
        first_handler = logger.handlers[0]
        configure_logging(logger_name="devforge.test", stream=output)
        logger.info("one line")
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsNot(logger.handlers[0], first_handler)
        self.assertEqual(len(output.getvalue().splitlines()), 1)

    def test_preserves_handlers_not_owned_by_devforge(self) -> None:
        logger = logging.getLogger("devforge.test")
        external_handler = logging.NullHandler()
        logger.addHandler(external_handler)
        configure_logging(logger_name="devforge.test", stream=StringIO())
        self.assertIn(external_handler, logger.handlers)

    def test_rejects_unknown_level(self) -> None:
        with self.assertRaises(ValueError):
            configure_logging(
                logger_name="devforge.invalid", level="LOUD", stream=StringIO()
            )

    def test_rejects_blank_logger_name(self) -> None:
        with self.assertRaises(ValueError):
            configure_logging(logger_name="  ", stream=StringIO())


if __name__ == "__main__":
    unittest.main()
