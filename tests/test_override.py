"""
Test override features

PyTest commands:
    pytest -s test_override.py -k test_override_log_level
    pytest -s test_override.py -k test_override_log_filename
    pytest -s test_override.py -k test_override_log_dir
    pytest -s test_override.py -k test_override_subdir
    pytest -s test_override.py -k test_override_multi_attributes
    pytest -s test_override.py -k test_override_log_filenames
"""
import sys
import os
import logging
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from dlogging import DLogger, FORMATS, Fmt, LOG_CONF
from .utils import print_file_contents, message_count, write_message


_DIR_LIST: str = ["logs/", "test_logs/"]
_FILE_LIST: str = ["logs/sys.log", "logs/app.log", "logs/main.log", "logs/app_new.log",
                   "test_logs/app.log", "logs/sys1.log", "logs/sys2.log",
                   "logs/sys/app.log", "test_logs/sys/app_new.log"]

def reset():
    """reset"""
    LOG_CONF.reset()

    # truncate log files
    for file in _FILE_LIST:
        if os.path.exists(file):
            with open(file, 'w'):
                pass

def setup_module():
    """setup_module"""
    print("\nsetup_module()")
    for log_dir in _DIR_LIST:
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)

def setup_function():
    """setup_function"""
    print(" " * 2, "setup_function")
    reset()

def teardown_function():
    """teardown_function"""
    print("\n", "  teardown_function()")

def teardown_module():
    """teardown_module"""
    print("teardown_module()")
    logging.shutdown()

def test_override_log_level():
    """test_override_log_level"""
    print(" " * 4, "test_override_log_level")
    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    # override log_level 'logging.INFO' w/ 'logging.WARNING'
    LOG_CONF.log_level = logging.WARNING
    LOG_CONF.override_logger_settings(True)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 7

def test_override_log_filename():
    """test_override_log_filename"""
    print(" " * 4, "test_override_log_filename")
    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    # override log filename 'app.log' w/ 'app_new.log'
    LOG_CONF.filename = "app_new.log"
    LOG_CONF.override_logger_settings(True)

    write_message(logger)

    print_file_contents("logs/app_new.log")
    assert message_count("logs/app.log") == 4
    assert message_count("logs/app_new.log") == 4

def test_override_log_filenames():
    """
    test_override_log_filenames
    """
    print(" " * 4, "test_override_log_filenames")
    logger1 = DLogger(name="sys", filename="sys.log", log_level=logging.WARNING)
    logger2 = DLogger(name="app", filename="app.log", log_level=logging.INFO,
                      log_fmt=FORMATS[Fmt.FNAME_LEVEL_MSG])

    write_message(logger1)
    write_message(logger2)
    print_file_contents("logs/sys.log")
    assert message_count("logs/sys.log") == 3
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    # move all messages to 'logs/main.log'
    LOG_CONF.filename = "main.log"
    LOG_CONF.override_logger_settings(True)

    write_message(logger1)
    write_message(logger2)

    assert message_count("logs/sys.log") == 3
    assert message_count("logs/app.log") == 4

    print_file_contents("logs/main.log")
    assert message_count("logs/main.log") == 7

def test_override_log_dir():
    """override default log dir, 'logs', which is under current directory"""
    print(" " * 4, "test_override_log_dir")
    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    # override default log dir 'logs' w/ 'test_logs'
    LOG_CONF.log_dir = "test_logs"
    LOG_CONF.override_logger_settings(True)

    write_message(logger)
    print_file_contents("test_logs/app.log")

    assert message_count("logs/app.log") == 4
    assert message_count("test_logs/app.log") == 4

def test_override_subdir():
    """test_override_subdir"""
    print(" " * 4, "test_override_subdir")
    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    # override default empty log subdir w/ 'sys'
    LOG_CONF.sub_dir = "sys"
    LOG_CONF.override_logger_settings(True)

    write_message(logger)
    print_file_contents("logs/sys/app.log")

    assert message_count("logs/app.log") == 4
    assert message_count("logs/sys/app.log") == 4

def test_override_multi_attributes():
    """test_override_multi_attributes"""
    print(" " * 4, "test_override_multiple_attributes")
    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)
    print_file_contents("logs/app.log")
    assert message_count("logs/app.log") == 4

    LOG_CONF.log_dir = "test_logs" # override default log dir 'logs' w/ 'test_logs'
    LOG_CONF.sub_dir = "sys"  # override default empty log subdir w/ 'sys'
    LOG_CONF.filename = "app_new.log"
    LOG_CONF.log_level = logging.WARNING
    LOG_CONF.log_fmt = FORMATS[Fmt.FNAME_LINENO_FUNCNAME]
    LOG_CONF.override_logger_settings(True)

    write_message(logger)
    print_file_contents("test_logs/sys/app_new.log")

    assert message_count("logs/app.log") == 4  # no changes
    assert message_count("test_logs/sys/app_new.log") == 3

def test_override_name_re_filter():
    """override apply to logger names match regular expression """
    print(" " * 4, "test_override_name_re_filter")
    logger1 = DLogger(name="main", filename="app.log", log_level=logging.WARNING)
    logger2 = DLogger(name="sys1", filename="sys1.log", log_level=logging.ERROR)
    logger3 = DLogger(name="sys2", filename="sys2.log", log_level=logging.WARNING)

    write_message(logger1)
    write_message(logger2)
    write_message(logger3)
    assert message_count("logs/app.log") == 3
    assert message_count("logs/sys1.log") == 2
    assert message_count("logs/sys2.log") == 3

    LOG_CONF.logger_name_re_filter = "^sys"  # apply to logger names start with "sys"
    LOG_CONF.log_level = logging.INFO
    LOG_CONF.override_logger_settings(True)

    write_message(logger1)
    write_message(logger2)
    write_message(logger3)

    assert message_count("logs/app.log") == 3 + 3
    assert message_count("logs/sys1.log") == 2 + 4
    assert message_count("logs/sys2.log") == 3 + 4

def test_override_name_re_filter_2():
    """
    override apply to logger names match regular expression
    skip override_allowed=False loggers
    """
    print(" " * 4, "test_override_name_re_filter_2")
    logger1 = DLogger(name="main", filename="app.log", log_level=logging.WARNING)
    logger2 = DLogger(name="sys1", filename="sys1.log", log_level=logging.ERROR, override_allowed=False)
    logger3 = DLogger(name="sys2", filename="sys2.log", log_level=logging.WARNING)

    write_message(logger1)
    write_message(logger2)
    write_message(logger3)
    assert message_count("logs/app.log") == 3
    assert message_count("logs/sys1.log") == 2
    assert message_count("logs/sys2.log") == 3

    # apply to logger names start w/ "sys" & override_allowed=True
    LOG_CONF.logger_name_re_filter = "^sys"
    LOG_CONF.log_level = logging.INFO
    LOG_CONF.override_logger_settings(True)

    write_message(logger1)
    write_message(logger2)
    write_message(logger3)

    assert message_count("logs/app.log") == 3 + 3
    assert message_count("logs/sys1.log") == 2 + 2  # logger 'sys1' override_allowed=False
    assert message_count("logs/sys2.log") == 3 + 4
