import sys
import os
import shutil
import logging
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from dlogging import DLogger, FORMATS, Fmt, LOG_CONF, Mode
from .utils import show_logger_details

def setup_module():
    print("setup_module()")
    LOG_CONF.set_mode(Mode.TEST)
    LOG_CONF.stdout_fmt = FORMATS[Fmt.FNAME_LINENO_FUNCNAME]
    LOG_CONF.log_enabled = True

def teardown_module():
    print("teardown_module()")

def setup_function():
    print("setup_function()")
    if os.path.exists("logs/"):
        shutil.rmtree("logs")

def teardown_function():
    print("teardown_function, contents of logs/app.log:")
    with open("logs/app.log", "r") as f:
        for line in f.readlines():
            line = line.strip()
            print(line)

def expect(no_items_in_log, no_items_in_cout):
    print("expect %d lines in cout, %d lines in log" % (no_items_in_cout, no_items_in_log))

@pytest.mark.dependency(name="t1")
@pytest.mark.debug_debug
def test_debug_debug():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.DEBUG, cout_level=logging.DEBUG, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=5, no_items_in_cout=5)

@pytest.mark.info_info
@pytest.mark.dependency(name="t2", depends=["t1"])
def test_info_info():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.INFO, cout_level=logging.INFO, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=4, no_items_in_cout=4)

@pytest.mark.warn_warn
@pytest.mark.dependency(name="t3", depends=["t2"])
def test_warn_warn():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.WARN, cout_level=logging.WARN, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=3, no_items_in_cout=3)

@pytest.mark.error_error
@pytest.mark.dependency(name="t4", depends=["t3"])
def test_error_error():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.ERROR, cout_level=logging.ERROR, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=2, no_items_in_cout=2)

@pytest.mark.fatal_fatal
@pytest.mark.dependency(name="t5", depends=["t4"])
def test_fatal_fatal():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.FATAL, cout_level=logging.FATAL, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=1, no_items_in_cout=1)

@pytest.mark.info_warn
@pytest.mark.dependency(name="t6", depends=["t5"])
def test_info_warn():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.INFO, cout_level=logging.WARN, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=4, no_items_in_cout=3)

@pytest.mark.debug_info
@pytest.mark.dependency(name="t7", depends=["t6"])
def test_debug_info():
    clog1 = DLogger("system", cout_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG], log_level=logging.DEBUG, cout_level=logging.INFO, cout_enabled=True)
    show_logger_details(clog1)
    clog1.debug('1 - msg debug')
    clog1.info('2 - msg info')
    clog1.warning('3 - msg warn')
    clog1.error('4 - msg error')
    clog1.critical('5 - msg critical')
    expect(no_items_in_log=5, no_items_in_cout=4)
