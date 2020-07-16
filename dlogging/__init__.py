"""
logging package
"""
from .config import DateFmt, DATE_FORMATS, FORMATS, Fmt, LOG_CONF, Mode
from .factory import DLogger

__all__ = ("DateFmt", "Fmt", "DATE_FORMATS", "FORMATS", "LOG_CONF", "Mode", "DLogger")

__version__ = "0.5.0"
