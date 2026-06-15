import logging
import sys
import structlog
from core.reconx.config.settings import settings

def setup_logger():
    """Configure structlog for ReconX."""
    # Shared processors
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Context variables
    structlog.contextvars.clear_contextvars()

    if settings.DEBUG:
        # Colored, human-readable logging for development
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True)
        ]
        log_level = logging.DEBUG
    else:
        # JSON logging for production
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]
        log_level = logging.INFO

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    return structlog.get_logger("reconx")

logger = setup_logger()
