"""
Structured logging configuration for theCooperator backend.

This module will set up structured logging (e.g., via structlog) and integrate
with Uvicorn/Gunicorn access logs.
"""

# TODO: implement structured logging setup using structlog or similar.

def configure_logging() -> None:
    """Configure structured logging for the application."""
    import logging
    import structlog

    timestamper = structlog.processors.TimeStamper(fmt="iso")
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )
    # Configure root logger
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    # Redirect Uvicorn loggers to structlog
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        # Clear existing handlers and attach StreamHandler
        uv_logger.handlers.clear()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        uv_logger.addHandler(handler)
        uv_logger.setLevel(logging.INFO)