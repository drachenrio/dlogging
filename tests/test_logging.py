"""
Test standard logging features
Sample pytest commands:
    pytest -s test_logging.py -k test_simple
    pytest -s test_logging.py -k test_dual
"""
import sys
import os
from os import path
import logging
import shutil

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from dlogging import DLogger, FORMATS, Fmt
from dlogging.utils import (get_all_loggers, show_all_loggers, print_file_contents, compare_files,
                            message_count, write_message)

def setup_module():
    print("\nsetup_module()")

def setup_function():
    print("  setup_function")
    if os.path.exists("logs/"):
        print("    shutil.rmtree('logs')")
        shutil.rmtree("logs")

def teardown_function():
    print("\n  teardown_function()")
    pass

def teardown_module():
    print("teardown_module()")
    logging.shutdown()

def test_propagate():
    print("test_propagate()")
    clog1 = DLogger("main", filename="main.log")
    clog2 = DLogger("main.sub", filename="main.sub.log", propagate=True)
    clog1.info("1 - msg to main.log")
    clog2.info("2 - msg to main.sub.log and propagate to main.log")
    print_file_contents(path.join("logs", "main.log"))
    print_file_contents(path.join("logs", "main.sub.log"))

def test_propagate_root():
    print("test_propagate_root()")
    clog0 = DLogger("", filename="app_root.log", log_enabled=True)  # root logger if name = ""
    clog1 = DLogger("main", filename="app_main.log", log_enabled=True, propagate=True)
    clog2 = DLogger("main.sub", filename="sub.log", log_enabled=True, propagate=True)
    clog0.info("0 - msg to root")
    clog1.info("1 - msg to main")
    clog2.info("2 - msg to sub and propagate to main")
    print_file_contents(path.join("logs", "app_root.log"))
    print_file_contents(path.join("logs", "app_main.log"))
    print_file_contents(path.join("logs", "sub.log"))

def test_propagate_root_stdout():  # error message goes top log file and screen
    print("test_propagate_root_stdout()")
    clog_ = DLogger("root", filename="app_root.log", log_enabled=True)  # root logger if name = ""
    clog0 = DLogger("", filename="app_root.log", log_enabled=True)  # root logger if name = ""
    clog1 = DLogger("main", filename="app_main.log", log_enabled=True, propagate=True)
    clog2 = DLogger("main.sub", filename="sub.log", log_enabled=True, propagate=False)
    clog0.info("clog0 - msg to root")
    clog1.info("clog1 - msg to main")
    clog2.info("clog2 - msg to sub and propagate to main")
    clog2.error("clog2 - error msg goes to file and stdout/stderr")
    print_file_contents(path.join("logs", "app_root.log"))
    print_file_contents(path.join("logs", "app_main.log"))
    print_file_contents(path.join("logs", "sub.log"))

    loggers = get_all_loggers()
    print("len(loggers): ", len(loggers))
    show_all_loggers()

def test_propagate_false():
    print("test_propagate_false()")
    clog1 = DLogger("main", filename="main.log", log_enabled=True)
    clog2 = DLogger("main.sub", filename="sub.log", log_enabled=True, propagate=False)
    clog1.info("1 - msg to main.log")
    clog2.info("2- msg to sub.log and not propagate to main.log")
    print_file_contents(path.join("logs", "main.log"))
    print_file_contents(path.join("logs", "sub.log"))

def test_simple():
    logger = DLogger("main", filename="app_simple.log", log_fmt=FORMATS[Fmt.LEVEL_MSG])
    write_message(logger)
    if os.getcwd().endswith('tests'):
        assert compare_files(path.join("test_data", "app_simple.log"), path.join("logs", "app_simple.log"))
    else:
        assert compare_files(path.join("tests", "test_data", "app_simple.log"), path.join("logs", "app_simple.log"))

def test_dual(capsys):
    clog = DLogger("main", filename="app_simple.log", log_fmt=FORMATS[Fmt.LEVEL_MSG],
                   cout_enabled=True, cout_level=logging.INFO)

    clog.debug('debug message')

    clog.info('info message')
    out, err = capsys.readouterr()
    assert err == "info message\n"

    clog.warning('warn message')
    _, err = capsys.readouterr()
    assert err == "warn message\n"

    clog.error('error message')
    _, err = capsys.readouterr()
    assert err == "error message\n"

    clog.critical('critical message')
    _, err = capsys.readouterr()
    assert err == "critical message\n"

    if os.getcwd().endswith('tests'):
        assert compare_files(path.join("test_data", "app_simple.log"), path.join("logs", "app_simple.log"))
    else:
        assert compare_files(path.join("tests", "test_data", "app_simple.log"), path.join("logs", "app_simple.log"))
