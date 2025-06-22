import logging.config as log_config
import os


def init_logger() -> None:
    filename: str | None = os.getenv("LOGGING_CONFIG")
    if filename:
        log_config.fileConfig(filename)
