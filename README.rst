iexfinance
==========

.. image:: https://travis-ci.org/addisonlynch/iexfinance.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/iexfinance

.. image:: https://codecov.io/gh/addisonlynch/iexfinance/branch/master/graphs/badge.svg?branch=master
	:target: https://codecov.io/gh/addisonlynch/iexfinance

.. image:: https://badge.fury.io/py/iexfinance.svg
    :target: https://badge.fury.io/py/iexfinance

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0


Python wrapper around `IEX Cloud <https://iexcloud.io>`__ and the legacy
`Investors Exchange (IEX) <https://iextrading.com/>`__
`Developer API <https://iextrading.com/developer/>`__.

An easy-to-use interface to obtain:

- Real-time quotes
- Historical data
- Fundamentals,
- Actions (dividends, splits), Sector Performance
- Trading analyses (gainers, losers, etc.)
- IEX Market Data & Stats

iexfinance provides real-time financial data from the various IEX
endpoints, including:

- Stocks (`iexfinance docs <https://addisonlynch.github.io/iexfinance/stable/stocks.html>`__ | `IEX Docs <https://iexcloud.io/api/docs/#stocks>`__)
- Reference Data (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/refdata.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#reference-data>`__)
- Investors Exchange Data (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/iexdata.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#investors-exchange-data>`__)
- API System Metadata (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/apistatus.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#api-system-metadata>`__)

Documentation
-------------

`Stable documentation <https://addisonlynch.github.io/iexfinance/stable/>`__ is hosted on `github.io <https://addisonlynch.github.io/iexfinance/index.html#documentation>`__.

`Development documentation <https://addisonlynch.github.io/iexfinance/devel/>`__ is also available for the latest changes in master.

Install
-------

From PyPI with pip (latest stable release):

``$ pip3 install iexfinance``

From development repository (dev version):

.. code:: bash

     $ git clone https://github.com/addisonlynch/iexfinance.git
     $ cd iexfinance
     $ python3 setup.py install

Selecting an API version
------------------------

IEX is continuing support for their version 1 (current) API until at least May 29th, 2019. IEX cloud beta is now available and includes a variety of additional endpoints. IEX is also introducing versioning through URL routing which will allow users to query from each version of the IEX Cloud API as more become available.

The IEX api version can be selected by setting the environment variable ``IEX_API_VERSION`` to one of the following values:

- ``v1``: IEX legacy v1.0 `Developer API <https://iextrading.com/developer/docs/>`__
- ``iexcloud-beta`` for the current beta of `IEX Cloud <https://iexcloud.io/docs/api/>`__
- ``iexcloud-v1`` for version 1 of IEX cloud (not yet available)

Common Usage Examples
---------------------

The `iex-examples <https://github.com/addisonlynch/iex-examples>`__ repository provides a number of detailed examples of iexfinance usage. Basic examples are also provided below.

Using iexfinance to access data from IEX is quite easy. The most commonly-used
endpoints are the `Stocks <https://iexcloud.io/docs/api/#stocks>`__
endpoints, which allow access to various information regarding equities,
including quotes, historical prices, dividends, and much more.

Real-time Quotes
^^^^^^^^^^^^^^^^

To obtain real-time quotes for one or more symbols, use the ``get_price``
method of the ``Stock`` object:

.. code:: python

    from iexfinance.stocks import Stock
    tsla = Stock('TSLA')
    tsla.get_price()

or for multiple symbols, use a list or list-like object (Tuple, Pandas Series,
etc.):

.. code:: python

    batch = Stock(["TSLA", "AAPL"])
    batch.get_price()


Historical Data
^^^^^^^^^^^^^^^

It's possible to obtain historical data the ``get_historical_data`` and
``get_historical_intraday``.

Daily
~~~~~

To obtain daily historical price data for one or more symbols, use the
``get_historical_data`` function. This will return a daily time-series of the ticker
requested over the desired date range (``start`` and ``end`` passed as
``datetime.datetime`` objects):

.. code:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_data

    start = datetime(2017, 1, 1)
    end = datetime(2018, 1, 1)

    df = get_historical_data("TSLA", start, end)


For Pandas DataFrame output formatting, pass ``output_format``:

.. code:: python

    df = get_historical_data("TSLA", start, end, output_format='pandas')

It's really simple to plot this data, using `matplotlib <https://matplotlib.org/>`__:

.. code:: python

    import matplotlib.pyplot as plt

    df.plot()
    plt.show()


Minutely (Intraday)
~~~~~~~~~~~~~~~~~~~

To obtain historical intraday data, use ``get_historical_intraday`` as follows.
Pass an optional ``date`` to specify a date within three months prior to the
current day (default is current date):

.. code:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday

    date = datetime(2018, 11, 27)

    get_historical_intraday("AAPL", date)

or for a Pandas Dataframe indexed by each minute:

.. code:: python

    get_historical_intraday("AAPL", output_format='pandas')


Endpoints
---------

Stock Endpoints
^^^^^^^^^^^^^^^

The ``Stock`` function creates a ``Stock`` instance which has a method to
retrieve each of the Stocks endpoints (``get_quote``, ``get_book``,
``get_volume_by_venue``, etc.):

.. code:: python

    from iexfinance.stocks import Stock
    tsla = Stock('TSLA')
    tsla.get_open()
    tsla.get_price()

Pandas DataFrame and JSON (dict) output formatting are selected with the
``output_format`` parameter when calling ``Stock``.

.. code:: python

    tsla = Stock("TSLA", output_format='pandas')
    tsla.get_quote()


IEX Reference Data
^^^^^^^^^^^^^^^^^^

Support for the `IEX Reference Data
<https://iextrading.com/developer/docs/#reference-data>`__ endpoints is
available through the top level functions ``get_available_symbols``,
``get_corporate_actions``, ``get_dividends``, ``get_next_day_ex_date``, and
``get_listed_symbol_dir``. As with all endpoints, request parameters such as
``retry_count`` and output format selection (through ``output_format``) can be
passed to the call.

.. code:: python

	from iexfinance import get_available_symbols

	get_available_symbols(output_format='pandas')[:2]


IEX Market Data
^^^^^^^^^^^^^^^

The `IEX Market Data
<https://iextrading.com/developer/docs/#iex-market-data>`__ endpoints are
supported through various top-level functions, including ``get_market_tops``
and ``get_market_deep``.

.. code:: python

	from iexfinance import get_market_tops

	get_market_tops()


IEX Stats
^^^^^^^^^

The `IEX Stats
<https://iextrading.com/developer/docs/#iex-stats>`__ endpoints are
supported through various top-level functions, including ``get_stats_intraday``
and ``get_stats_recent``. These endpoints provide IEX's trading statistics for
a given ticker.

.. code:: python

	from iexfinance import get_stats_intraday

	get_stats_intraday()


Debugging \& Caching
--------------------

All functions (including ``Stock`` and ``get_historical_data``) allow
for `Request Parameters <https://addisonlynch.github.io/usage.html#parameters>`__, which
include ``retry_count``, ``pause``, and ``session``. These parameters are
entirely optional. The first two deal with how unsuccessful requests are
handled, and the third allows for the passing of a cached ``requests-cache``
session (see `caching <https://addisonlynch.github.io/iexfinance/stable/caching.html>`__).

Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2019 Addison Lynch

See LICENSE for details
