from reconx.config.startup_checks import run_startup_checks
from reconx.core.logging.logger import logger


def main():
    try:
        run_startup_checks()
        logger.info("Configuration loaded successfully")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
