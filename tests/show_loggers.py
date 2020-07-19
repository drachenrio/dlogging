
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from dlogging import DLogger, FORMATS, Fmt
from dlogging.utils import show_all_loggers

log1 = DLogger("log1")
log2 = DLogger("log2", log_fmt=FORMATS[Fmt.FNAME_LINENO_FUNCNAME])
log_null = DLogger("log_null", log_enabled=False)  # NullHandler

show_all_loggers()

def log_messages():
    log1.info("msg #3")
    log2.info("msg #4")
    log_null.error("msg #5") # message ignored

log1.info("msg #2 goes to log1_n.log")
log_messages()
