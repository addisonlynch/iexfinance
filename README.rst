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

Now Supporting IEX Cloud
------------------------

Python SDK for `IEX Cloud <https://iexcloud.io>`__. Architecture mirrors
that of the IEX Cloud API (and its `documentation <https://iexcloud.io/docs/api/>`__).

``iexfinance`` will maintain compatibility and support for the
IEX Version `Developer API <https://iextrading.com/developer/>`__ until June
2019.

An easy-to-use toolkit to obtain data for Stocks, ETFs, Mutual Funds,
Forex/Currencies, Options, Commodities, Bonds, and Cryptocurrencies:

- Real-time and delayed quotes
- Historical data (daily and minutely)
- Financial statements (Balance Sheet, Income Statement, Cash Flow)
- Institutional and Fund ownership
- Analyst estimates, Price targets
- Corporate actions (Dividends, Splits)
- Sector performance
- Market analysis (gainers, losers, volume, etc.)
- IEX market data & statistics (IEX supported/listed symbols, volume, etc)
- Social Sentiment and CEO Compensation

Example
-------

.. image:: https://addisonlynch.github.io/public/img/iexexample.gif


Documentation
-------------

Stable documentation is hosted on
`github.io <https://addisonlynch.github.io/iexfinance/stable/>`__.

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



Authentication
--------------

An IEX Cloud account is required to acecss the IEX Cloud API. Various `plans <https://iexcloud.io/pricing/>`__
are availalbe, free, paid, and pay-as-you-go.

Your IEX Cloud (secret) authentication token can be passed to any function or at the instantiation of a ``Stock`` object.
The easiest way to store a token is in the ``IEX_TOKEN`` environment variable.

Passing as an Argument
~~~~~~~~~~~~~~~~~~~~~~

The authentication token can also be passed to any function call:


.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas', token="<YOUR AUTH TOKEN>")

or at the instantiation of a ``Stock`` object:

.. code-block:: python

    from iexfinance.stocks import Stock

    a = Stock("AAPL", token="<YOUR AUTH TOKEN>")
    a.get_quote()


How This Package is Structured
------------------------------

``iexfinance`` is designed to mirror the structure of the IEX Cloud API. The
following IEX Cloud endpoint groups are mapped to their respective
``iexfinance`` modules:

- Account - ``account`` (`iexfinance docs <https://addisonlynch.github.io/iexfinance/stable/account.html>`__ | `IEX Docs <https://iexcloud.io/docs/api/#account>`__)
- Stocks - ``stocks`` (`iexfinance docs <https://addisonlynch.github.io/iexfinance/stable/stocks.html>`__ | `IEX Docs <https://iexcloud.io/api/docs/#stocks>`__)
- Alternative Data - ``altdata`` (`iexfinance docs <https://addisonlynch.github.io/iexfinance/stable/altdata.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#alternative-data>`__)
- Reference Data - ``refdata`` (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/refdata.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#reference-data>`__)
- Investors Exchange Data - ``iexdata`` (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/iexdata.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#investors-exchange-data>`__)
- API System Metadata - ``apidata`` (`iexfinance docs <http://addisonlynch.github.io/iexfinance/stable/apistatus.html>`__ | `IEX Cloud Docs <https://iexcloud.io/docs/api/#api-system-metadata>`__)

The most commonly-used
endpoints are the `Stocks <https://iexcloud.io/docs/api/#stocks>`__
endpoints, which allow access to various information regarding equities,
including quotes, historical prices, dividends, and much more.

The ``Stock`` `object <https://addisonlynch.github.io/iexfinance/stable/stocks.html#the-stock-object>`__
provides access to most endpoints, and can be instantiated with a symbol or
list of symbols:

.. code-block:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")
    aapl.get_balance_sheet()

The rest of the package is designed as a 1:1 mirror. For example, using the
`Alternative Data <https://iexcloud.io/docs/api/#alternative-data>`__ endpoint
group, obtain the `Social Sentiment <https://iexcloud.io/docs/api/#social-sentiment>`__ endpoint with
``iexfinance.altdata.get_social_sentiment``:

.. code-block:: python

    from iexfinance.altdata import get_social_sentiment

    get_social_sentiment("AAPL")


Configuration
-------------

Selecting an API Version
~~~~~~~~~~~~~~~~~~~~~~~~

``iexfinance`` now defaults to IEX Cloud for all calls. The use of
``v1`` as ``IEX_API_VERSION`` will be warned in ``iexfinance``
0.4.1 and deprecated in 0.4.2.

The desired IEX API version can be specified using the ``IEX_API_VERSION``
environment variable. The following versions are currently supported:

* ``v1`` - *note: this will be deprecated in* ``iexfinance`` *version 0.4.2*
* ``iexcloud-beta``
* ``iexcloud-v1`` - **default**

Output Formatting
~~~~~~~~~~~~~~~~~

By default, ``iexfinance`` returns data formatted *exactly* as received from
the IEX Endpoint. `pandas <https://pandas.pydata.org/>`__ ``DataFrame`` output
formatting is available for most endpoints.

pandas ``DataFrame`` output formatting can be selected by setting the
``IEX_OUTPUT_FORMAT`` environment variable to ``pandas`` or by passing
``output_format`` as an argument to any function call (or at the instantiation
of a ``Stock`` object).

Common Usage Examples
---------------------

The `iex-examples <https://github.com/addisonlynch/iex-examples>`__ repository provides a number of detailed examples of iexfinance usage. Basic examples are also provided below.


Real-time Quotes
~~~~~~~~~~~~~~~~

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
~~~~~~~~~~~~~~~

It's possible to obtain historical data using ``get_historical_data`` and
``get_historical_intraday``.

Daily
^^^^^

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
^^^^^^^^^^^^^^^^^^^

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

Fundamentals
~~~~~~~~~~~~

Financial Statements
^^^^^^^^^^^^^^^^^^^^

`Balance Sheet <https://addisonlynch.github.io/iexfinance/stable/stocks.html#balance-sheet>`__

.. code-block:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")
    aapl.get_balance_sheet()

`Income Statement <https://addisonlynch.github.io/iexfinance/stable/stocks.html#income-statement>`__

.. code-block:: python

    aapl.get_income_statement()

`Cash Flow <https://addisonlynch.github.io/iexfinance/stable/stocks.html#cash-flow>`__

.. code-block:: python

    aapl.get_cash_flow()


Modeling/Valuation Tools
^^^^^^^^^^^^^^^^^^^^^^^^

`Analyst Estimates <https://addisonlynch.github.io/iexfinance/stable/stocks.html#estimates>`__

.. code-block:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")

    aapl.get_estimates()


`Price Target <https://addisonlynch.github.io/iexfinance/stable/stocks.html#price-target>`__

.. code-block:: python

    aapl.get_price_target()


Social Sentiment
^^^^^^^^^^^^^^^^

.. code-block:: python

    from iexfinance.altdata import get_social_sentiment
    get_social_sentiment("AAPL")


CEO Compensation
^^^^^^^^^^^^^^^^

.. code-block:: python

    from iexfinance.altdata import get_ceo_compensation
    get_ceo_compensation("AAPL")

Fund and Institutional Ownership
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from iexfinance.stocks import Stock
    aapl = Stock("AAPL")

    # Fund ownership
    aapl.get_fund_ownership()

    # Institutional ownership
    aapl.get_institutional_ownership()

Reference Data
~~~~~~~~~~~~~~

`List of Symbols IEX supports for API calls <https://addisonlynch.github.io/iexfinance/stable/refdata.html#symbols>`__

.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols()

`List of Symbols IEX supports for trading <https://addisonlynch.github.io/iexfinance/stable/refdata.html#iex-symbols>`__

.. code-block:: python

    from iexfinance.refdata import get_iex_symbols

    get_iex_symbols()

Account Usage
~~~~~~~~~~~~~

`Message Count <https://addisonlynch.github.io/iexfinance/stable/account.html#usage>`__

.. code-block:: python

    from iexfinance.account import get_usage

    get_usage(quota_type='messages')

API Status
~~~~~~~~~~

`IEX Cloud API Status <http://addisonlynch.github.io/iexfinance/stable/apistatus.html#iexfinance.tools.api.get_api_status>`__

.. code-block:: python

    from iexfinance.account import get_api_status

    get_api_status()

Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2019 Addison Lynch

See LICENSE for details
