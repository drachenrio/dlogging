"""
Dynamic Logger
"""
import logging
from typing import Tuple

from .config import (Config, LOG_CONF, FORMATS, DATE_FORMATS, Fmt, DateFmt, _LOGGERS,
                     merge_config, config_logger)

class DLogger:
    """
    Dynamic logger factory
    Create logging.Logger instance from arguments provided
    """
    #pylint: disable=too-many-arguments,too-many-locals,too-many-branches,too-many-statements
    #pylint: disable=too-many-locals,too-few-public-methods
    def __new__(cls,
                name: str,
                filename: str = "app.log",
                logger_level: int = logging.DEBUG,
                log_fmt: str = FORMATS[Fmt.DEFAULT],
                log_datefmt: str = DATE_FORMATS[DateFmt.DEFAULT],
                log_level: int = logging.INFO,
                log_enabled: str = True,
                cout_fmt: str = FORMATS[Fmt.MSG],
                cout_datefmt: str = DATE_FORMATS[DateFmt.DEFAULT],
                cout_level: int = logging.WARN,
                cout_enabled: bool = False,
                propagate: bool = False,
                log_dir: str = "logs",
                sub_dir: str = None,
                override_allowed: bool = True) -> logging.Logger:

        conf: Config = Config(name, filename, logger_level, log_fmt, log_datefmt, log_level,
                              log_enabled, cout_fmt, cout_datefmt, cout_level, cout_enabled,
                              propagate, log_dir, sub_dir, override_allowed)

        if override_allowed and LOG_CONF.override_logger_settings_enabled():
            conf = merge_config(LOG_CONF, conf)

        logger: logging.Logger = None
        configure_logger = True
        if name is not None and len(name) > 0:
            obj: Tuple[logging.Logger, Config] = _LOGGERS.get(name)
            if obj is None:
                logger = logging.getLogger(name)
            else:  # existing logger
                logger, x_conf = obj
                if vars(x_conf) == vars(conf):
                    configure_logger = False

        if logger is None:
            logger = logging.getLogger()  # root logger

        if configure_logger:
            config_logger(logger, conf)
            _LOGGERS[name] = (logger, conf)

        return logger
