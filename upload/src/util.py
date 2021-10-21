import logging
import logging.config
from os import environ


def configure_logging() -> None:
    logging_levels = {value: key for key, value in logging._levelToName.items()}
    logging_level_name = environ.get("LOG_LEVEL", "INFO")
    if logging_level_name not in logging_levels:
        raise ValueError(f"{logging_level_name} is not a valid log level")
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "class": "logging.Formatter",
                    "datefmt": "%H:%M:%S%z",
                    "format": "%(asctime)s %(filename)s:%(lineno)d %(levelname)s %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": logging_levels[logging_level_name],
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "root": {
                "level": logging_levels[logging_level_name],
                "handlers": ["console"],
            },
        }
    )
