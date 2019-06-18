.. _logging:

Logging & Message Counting
==========================

``iexfinance`` 0.4.2 adds logging support for queries, including message count
usage and debugging information. Logging level defaults to ``WARNING``, and can
be changed via the ``IEX_LOG_LEVEL`` environment variable. The
following levels provide various information:

    - ``WARNING`` - errors only
    - ``INFO`` - message count used
    - ``DEBUG`` - request information
