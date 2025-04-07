import logging

from app.config import config


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger using the log level and formatter defined in config.

    Args:
        name (str): Name of the logger (usually __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    logger.setLevel(config.LOG_LEVEL.upper())

    handler = logging.StreamHandler()
    handler.setFormatter(config.LOG_FORMATTER)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
