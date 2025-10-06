"""Logging helpers for the KI Dev Tycoon simulation."""

from __future__ import annotations

import logging
from typing import Iterable

_LOGGER_NAME = "ki_dev_tycoon"


class KeyValueFormatter(logging.Formatter):
    """Format log records as key-value pairs appended to the base message."""

    _STRUCTURED_KEYS: Iterable[str] = ("seed", "ticks", "tick", "duration_ms")

    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        extras = []
        for key in self._STRUCTURED_KEYS:
            value = record.__dict__.get(key)
            if value is not None:
                extras.append(f"{key}={value}")
        if extras:
            return f"{base} | {' '.join(extras)}"
        return base


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure a shared logger with structured key-value output."""

    logger = logging.getLogger(_LOGGER_NAME)
    level_name = level.upper()
    log_level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(log_level)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            KeyValueFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        logger.addHandler(handler)
        logger.propagate = False
    else:
        for handler in logger.handlers:
            handler.setLevel(log_level)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger below the global KI Dev Tycoon logger."""

    return logging.getLogger(f"{_LOGGER_NAME}.{name}")
