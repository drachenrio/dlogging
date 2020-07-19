#pylint: disable=line-too-long, too-few-public-methods

"""
Dynamic logging configuration and constants
"""

import os
import sys
import re
from enum import Enum
import logging
from logging.handlers import TimedRotatingFileHandler

# A dictionary saves created loggers, key - name: str, value - (logger: Logger, conf: Config)
_LOGGERS = {}
_ITEM_OR_DEFAULT = lambda item, default: item if item is not None else default


class Mode(Enum):
    """ Execution Mode """
    DEV = 1
    QA = 2
    TEST = 3
    PRODUCTION = 4

class DateFmt:
    """ Date logging formats """
    DEFAULT = "default"
    US_12H = "US-AM-PM"
    US_24H = "US-24H"

class Fmt:
    """ Logging formats """
    DEFAULT = "name_level_message"
    COMPLEX = "COMPLEX"
    FNAME_LEVEL_MSG = "FNAME_LEVEL_MSG"
    FNAME_LINENO_FUNCNAME = "FNAME_LINENO_FUNCNAME"
    FNAME_LINENO_LEVEL = "FNAME_LINENO_LEVEL"
    LEVEL_MSG = "LEVEL_MSG"
    MSG = "MSG"

FORMATS = {Fmt.DEFAULT: '%(name)s %(levelname)s %(message)s',
           Fmt.COMPLEX: '%(asctime)s %(filename)s:%(lineno)d : %(funcName)s %(name)s %(levelname)s %(message)s',
           Fmt.FNAME_LEVEL_MSG: '%(filename)s %(levelname)s %(message)s',
           Fmt.FNAME_LINENO_FUNCNAME: '%(filename)s:%(lineno)d %(funcName)s %(levelname)s %(message)s',
           Fmt.FNAME_LINENO_LEVEL: '%(filename)s:%(lineno)d %(levelname)s %(message)s',
           Fmt.LEVEL_MSG: '%(levelname)s %(message)s',
           Fmt.MSG: '%(message)s',
           }

DATE_FORMATS = {DateFmt.DEFAULT: None,  # yyyy-mm-dd HH:MM:SS,sss
                DateFmt.US_12H: '%m/%d/%Y %I:%M:%S %p',
                DateFmt.US_24H: '%m/%d/%Y %H:%M:%S',
                }

def _create_log_filename(log_dir: str, sub_dir: str, filename: str) -> str:
    """ create log filename """
    if log_dir is not None:
        file_path = sys.argv[0]
        print("file path: ", file_path)
        file_path = log_dir
        os.makedirs(file_path, exist_ok=True)
        if sub_dir is not None:
            file_path = os.path.join(log_dir, sub_dir)
            os.makedirs(file_path, exist_ok=True)
        filename = os.path.join(file_path, filename)
    return filename

def _handle_logging_override():
    """ handle logging override """
    logger: logging.Logger
    x_conf: Config  # eXisting conf
    for logger, x_conf in _LOGGERS.values():  # loop through all loggers and re-config loggers if need
        if not x_conf.override_allowed:
            continue
        if len(LOG_CONF.logger_name_re_filter) > 0:
            if bool(re.search(LOG_CONF.logger_name_re_filter, x_conf.name)) is False:
                continue

        handler: logging.Handler
        for handler in logger.handlers[:]:
            if not isinstance(handler, (logging.FileHandler, logging.StreamHandler)):
                continue

            conf = merge_config(LOG_CONF, x_conf)
            if not vars(x_conf) == vars(conf):
                config_logger(logger, conf)
                _LOGGERS[conf.name] = (logger, conf)

class Config:
    """ Config """
    #pylint: disable=too-many-instance-attributes, too-many-arguments, too-many-locals
    def __init__(self,
                 name: str = None,
                 filename: str = None,
                 logger_level: int = None,
                 log_fmt: str = None,
                 log_datefmt: str = None,
                 log_level: int = None,
                 log_enabled: str = None,
                 cout_fmt: str = None,
                 cout_datefmt: str = None,
                 cout_level: int = None,
                 cout_enabled: bool = None,
                 propagate: bool = None,
                 log_dir: str = None,
                 sub_dir: str = None,
                 override_allowed: bool = None,
                 ):
        self.name = name
        self.filename = filename
        self.logger_level = logger_level
        self.log_fmt = log_fmt
        self.log_datefmt = log_datefmt
        self.log_level = log_level
        self.log_enabled = log_enabled
        self.cout_fmt = cout_fmt  # console output format
        self.cout_datefmt = cout_datefmt
        self.cout_level = cout_level
        self.cout_enabled = cout_enabled
        self.propagate = propagate
        self.log_dir = log_dir
        self.sub_dir = sub_dir
        self.override_allowed = override_allowed

class LogConf(Config):
    """ Configure logging global attributes """
    #pylint: disable=too-many-instance-attributes, missing-function-docstring
    def __init__(self):
        super(LogConf, self).__init__()
        self._override_logger_settings: bool = None
        self._mode: Mode = Mode.PRODUCTION
        self.logger_name_re_filter: str = ""  # logger name regular expression filter, e.g. "^sys|main$"

    def reset(self):
        self.__init__()

    def override_logger_settings_enabled(self) -> bool:
        return self._override_logger_settings

    def override_logger_settings(self, enable: bool):
        self._override_logger_settings = enable
        if enable:
            _handle_logging_override()

    def set_sub_dir(self, sub_dir: str):
        self.sub_dir = sub_dir
        if self.sub_dir is not None:
            os.makedirs(os.path.join(self.log_dir, self.sub_dir), exist_ok=True)

    def get_mode(self) -> Mode:
        return self._mode

    def set_mode(self, mode: Mode):
        self._mode = mode

def merge_config(log_conf: LogConf, conf: Config) -> Config:
    """
    Create combined config object from system wide logger setting and current logger config
    """
    #pylint: disable=too-many-locals

    name = conf.name  # take individual conf value, ignore common log_conf value
    filename = _ITEM_OR_DEFAULT(log_conf.filename, conf.filename)
    logger_level = _ITEM_OR_DEFAULT(log_conf.logger_level, conf.logger_level)
    log_fmt = _ITEM_OR_DEFAULT(log_conf.log_fmt, conf.log_fmt)
    log_datefmt = _ITEM_OR_DEFAULT(log_conf.log_datefmt, conf.log_datefmt)
    log_level = _ITEM_OR_DEFAULT(log_conf.log_level, conf.log_level)
    log_enabled = _ITEM_OR_DEFAULT(log_conf.log_enabled, conf.log_enabled)
    cout_fmt = _ITEM_OR_DEFAULT(log_conf.cout_fmt, conf.cout_fmt)
    cout_datefmt = _ITEM_OR_DEFAULT(log_conf.cout_datefmt, conf.cout_datefmt)
    cout_level = _ITEM_OR_DEFAULT(log_conf.cout_level, conf.cout_level)
    cout_enabled = _ITEM_OR_DEFAULT(log_conf.cout_enabled, conf.cout_enabled)
    propagate = _ITEM_OR_DEFAULT(log_conf.propagate, conf.propagate)
    log_dir = _ITEM_OR_DEFAULT(log_conf.log_dir, conf.log_dir)
    sub_dir = _ITEM_OR_DEFAULT(log_conf.sub_dir, conf.sub_dir)
    override_allowed = conf.override_allowed  # take individual conf value, ignore common log_conf value

    n_conf: Config = Config(name, filename, logger_level, log_fmt, log_datefmt, log_level, log_enabled, cout_fmt,
                            cout_datefmt, cout_level, cout_enabled, propagate, log_dir, sub_dir, override_allowed)

    return n_conf

def config_logger(logger: logging.Logger, conf: Config) -> None:
    """ Config Logger using conf values """
    logger.setLevel(conf.logger_level)
    logger.propagate = conf.propagate

    # remove existing handlers and filters
    for handler in logger.handlers[:]:
        if isinstance(handler, (logging.FileHandler, logging.StreamHandler)):
            handler.close()
            logger.removeHandler(handler)

    for fltr in logger.filters[:]:
        logger.removeFilter(fltr)

    if conf.log_enabled and conf.filename is not None:
        l_formatter = logging.Formatter(conf.log_fmt, conf.log_datefmt)
        filename = _create_log_filename(conf.log_dir, conf.sub_dir, conf.filename)
        l_handler = TimedRotatingFileHandler(filename=filename, when='midnight')
        l_handler.setLevel(conf.log_level)
        l_handler.setFormatter(l_formatter)
        logger.addHandler(l_handler)

    if conf.cout_enabled:
        c_formatter = logging.Formatter(conf.cout_fmt, conf.cout_datefmt)
        c_handler = logging.StreamHandler()
        c_handler.setLevel(conf.cout_level)
        c_handler.setFormatter(c_formatter)
        logger.addHandler(c_handler)

    if len(logger.handlers) == 0:
        logger.addHandler(logging.NullHandler())

LOG_CONF = LogConf()
