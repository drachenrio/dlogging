Dynamic Logging for python
==========================

Dynamic Logging, dlogging, is a Python library to provide the capability to change logger behaviour at runtime.

Installation
------------

Install using pip::

    pip install dlogging


Usage
-----

Python::

    from dlogging import DLogger, FORMATS, Fmt

    log1 = DLogger("log1")
    log2 = DLogger("log2", log_fmt=FORMATS[Fmt.FNAME_LINENO_FUNCNAME])
    log_null = DLogger("log_null", log_enabled=False)  # log to file disabled

    def log_messages():
        log1.info("msg #2")
        log2.info("msg #3")
        log_null.error("msg #4") # message ignored

    log1.info("msg #1")
    log_messages()

By default, messages are logged in logs/app.log

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

License
-------
`MIT <https://choosealicense.com/licenses/mit/>`_
