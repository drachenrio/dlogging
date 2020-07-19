Dynamic Logging for python
==========================

Dynamic Logging, dlogging, is a Python library to provide the capability to change logger behaviour at runtime.

Installation
------------

Install using pip::

    pip install dlogging


Usage
-----
Example 1 - general logging

Python::

    from dlogging import DLogger, FORMATS, Fmt

    log1 = DLogger("log1")  # use default logging format, filename
    log2 = DLogger("log2", log_fmt=FORMATS[Fmt.FNAME_LINENO_LEVEL])
    log3 = DLogger("log3", log_enabled=False, cout_enabled=True)  # log to file disabled

    def log_messages():
        log1.info("msg #2")
        log2.info("msg #3")
        log3.error("msg #4") # message not logged to file, but display on stdout

    log1.info("msg #1")
    log_messages()

By default, messages are logged in logs/app.log

See tests/test_logging.py for more examples

Example 2 - logging override

Python::

    import os
    import logging
    from dlogging import DLogger, LOG_CONF

    def write_message(logger: logging.Logger) -> None:
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')

    def message_count(filename: str) -> int:
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return len(f.readlines())
        return 0

    logger = DLogger(name="main", filename="app.log", log_level=logging.INFO)

    write_message(logger)  # expect 4 messages written into logs/app.log
    assert message_count("logs/app.log") == 4

    # override log_level 'logging.INFO' w/ new log level 'logging.WARNING'
    LOG_CONF.log_level = logging.WARNING  # set new log_level at LOG_CONF
    LOG_CONF.override_logger_settings(True)  # this triggers log_level override

    write_message(logger)  # expect 3 messages written into logs/app.log
    assert message_count("logs/app.log") == 7  # expect total 7 messages

See tests/test_override.py for more examples

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
-------
`MIT <https://choosealicense.com/licenses/mit/>`_
