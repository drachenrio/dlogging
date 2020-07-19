"""
Logging utilities
"""
import os
import logging
from os import path
from logging import Logger
from typing import List

def get_all_loggers():
    """ get all loggers including root logger """
    loggers = [logging.getLogger()]
    loggers = loggers + [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    return loggers

def _display_details(logger: Logger):
    """ display specified logger details """
    print(f"logger: {id(logger)} {logger}")
    if logger.parent is not None:
        print(f"  {id(logger.root)} root: {logger.root}")
    else:
        print(f"  root: {logger.root}")

    if logger.parent is not None:
        print(f"  {id(logger.parent)} parent: {logger.parent}")
    else:
        print(f"  parent: {logger.parent}")

    for hdlr in logger.handlers:
        print(f"  {id(hdlr)} handler: {hdlr}")

    for fltr in logger.filters:
        print(f"  {id(fltr)} filter: {fltr}")
    print()

def show_all_loggers():
    """ show all loggers """
    for logger in get_all_loggers():
        _display_details(logger)

def update_logger_subdir(logger: Logger, subdir):
    """ update logger logging subdir """
    for hdlr in logger.handlers[:]:
        if not isinstance(hdlr, logging.FileHandler):
            continue
        basename = os.path.basename(hdlr.stream.buffer.name)
        filename = os.path.join(subdir, basename)
        h_file = logging.FileHandler(filename, 'a')
        h_file.setFormatter(hdlr.formatter)
        hdlr.close()
        logger.removeHandler(hdlr)
        logger.addHandler(h_file)

def update_handlers_log_level(logger: Logger, log_level):
    """ update log level of handlers for specified logger """
    for handler in logger.handlers:
        if isinstance(logger, (logging.FileHandler, logging.StreamHandler)):
            handler.setLevel(log_level)

def update_log_level(logger: Logger, log_level):
    """ update log level for specified logger """
    logger.setLevel(log_level)
    update_handlers_log_level(logger, log_level)

def print_file_contents(filename: str):
    """ print file contents for specified file """
    if os.path.exists(filename):
        print("\ncat {}:".format(filename))
        with open(filename, "r") as f:
            for line in f.readlines():
                line = line.strip()
                print(line)

def write_message(logger: logging.Logger) -> None:
    """ help method to write test messages to specified logger """
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')

def message_count(filename: str) -> int:
    """ count number of messages in specified file """
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return len(f.readlines())
    return 0

def compare_files(file_1: str, file_2: str) -> bool:
    """
    compare the contents of two files
    return True if contents are the same, False otherwise
    """
    if not path.exists(file_1) or not path.exists(file_2):
        return False
    lines_1: List[str]
    lines_2: List[str]
    with open(file_1, "r") as f1:
        with open(file_2, "r") as f2:
            lines_1 = f1.readlines()
            lines_2 = f2.readlines()

    return lines_1 == lines_2
