"""Structured logging configuration for asprom."""

from __future__ import annotations

import logging
import os
import sys

import structlog


def configure_logging(json_output: bool | None = None) -> None:
    """Configure structlog for console or JSON output."""
    if json_output is None:
        json_output = os.environ.get("ASPROM_LOG_FORMAT", "").lower() == "json"

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
    ]
    if json_output:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,  # type: ignore[arg-type]
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str, **initial: object) -> structlog.BoundLogger:
    """Return a bound structlog logger."""
    return structlog.get_logger(name).bind(**initial)
