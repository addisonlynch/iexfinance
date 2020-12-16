.. _caching:

Caching Queries
===============

In some cases it is sensible to cache queries to avoid overloading the
IEX servers. ``iexfinance`` supports the caching of queries through
``requests_cache_``.

Tutorial
--------

Install ``requests-cache`` using pip:

.. code:: bash

    $ pip install requests-cache

To use a cached session, pass a ``requests_cache.Session`` object to the
top-level function you are using:

.. code-block:: python

    import datetime
    from iexfinance.stocks import Stock
    import requests_cache

    expiry = datetime.timedelta(days=3)
    session = requests_cache.CachedSession(cache_name='cache',
                                           backend='sqlite',
                                           expire_after=expiry)

    f = Stock("AAPL", session=session)
    f.get_price()

A `SQLite <https://www.sqlite.org/index.html>`__ file named ``cache.sqlite`` will
be created in the working directory, storing the request until the
expiry date.

For more information about ``requests-cache``, see its `Documentation
<https://readthedocs.org/projects/requests-cache/>`__.

Caching mechanism similar to `Pandas Datareader
<https://pandas-datareader.readthedocs.io/en/latest/cache.html>`__.
