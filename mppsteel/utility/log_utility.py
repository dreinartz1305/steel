"""Utility Script for logger"""

import logging
import os
import sys

from pathlib import Path

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from mppsteel.config.model_config import DATETIME_FORMAT, LOG_PATH

LOG_FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
)


def get_console_handler() -> logging.StreamHandler:
    """Formats the log for console output.

    Returns:
        StreamHandler: A formatted stream handler.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(LOG_FORMATTER)
    return console_handler


def get_file_handler() -> TimedRotatingFileHandler:
    """Formats the log for file output.

    Returns:
        [type]: A formatted file handler.
    """
    today_time = datetime.now().strftime(DATETIME_FORMAT)
    if not Path(LOG_PATH).is_dir():
        try:
            os.mkdir(LOG_PATH)
        except OSError as error:
            print(error)
    log_filepath = f"{LOG_PATH}/mppsteel_{today_time}.log"
    file_handler = TimedRotatingFileHandler(log_filepath, when="midnight")
    file_handler.setFormatter(LOG_FORMATTER)
    return file_handler


def get_logger(logger_name: str, create_logfile: bool = True) -> logging.Logger:
    """Creates a log object that can be outputted to file or console output.

    Args:
        logger_name (str): Defines the name of the log based on the user input.
        create_logfile (bool, optional): Determines whether to create a logfile. Defaults to False.

    Returns:
        logging.Logger: A logger that can used to log runtime code.
    """
    generic_logger = logging.getLogger(logger_name)
    generic_logger.setLevel(
        logging.DEBUG
    )  # better to have too much log than not enough
    generic_logger.addHandler(get_console_handler())
    if create_logfile:
        generic_logger.addHandler(get_file_handler())
    generic_logger.propagate = (
        False  # rarely necessary to propagate the error up to parent
    )
    return generic_logger
