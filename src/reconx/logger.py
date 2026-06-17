import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("reconx")
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Info Log
    info_handler = RotatingFileHandler(
        "logs/reconx.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    # Error Log
    error_handler = RotatingFileHandler(
        "logs/errors.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Stream (Console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Avoid duplicate logs if instantiated multiple times
    if not logger.handlers:
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)
        logger.addHandler(console_handler)

    return logger
