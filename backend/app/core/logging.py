import logging
import logging.config
import sys
import structlog

def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure structured logging for the application.

    This setup integrates structlog with standard logging, so logs from other
    libraries are also processed by structlog.
    """
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging
    log_renderer = structlog.dev.ConsoleRenderer() # or JSONRenderer() for prod

    # Define logging configuration for dictConfig
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False, # Keep existing loggers (e.g. uvicorn)
        "formatters": {
            "default": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": log_renderer,
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout, # Explicitly set to stdout
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["default"],
                "level": log_level,
                "propagate": True, # Propagate to parent loggers
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False, # Do not propagate uvicorn.error to root
            },
            "uvicorn.access": {
                "handlers": ["default"], # Use the same handler for access logs
                "level": log_level, # Or another level like INFO
                "propagate": False, # Do not propagate uvicorn.access to root
            },
        },
    }

    logging.config.dictConfig(logging_config)

# Example of getting a logger instance
# logger = structlog.get_logger(__name__)