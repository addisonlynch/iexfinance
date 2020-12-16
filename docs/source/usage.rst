.. _usage:


Common Usage Examples
=====================


The `iex-examples <https://github.com/addisonlynch/iex-examples>`__ repository provides a number of detailed examples of iexfinance usage. Basic examples are also provided below.

Using iexfinance to access data from IEX is quite easy. The most commonly-used
endpoints are the `Stocks <https://iexcloud.io/docs/api/#stocks-equities>`__
endpoints, which allow access to various information regarding equities,
including quotes, historical prices, dividends, and much more.

The iexfinance codebase and documentation are structured in a way that emulates much of the `IEX Cloud Documentation <https://iexcloud.io/docs/api/>`__ for readability and ease of use.

  - :ref:`Account<usage.account>`
  - :ref:`Stocks<usage.stocks>`
  - :ref:`Reference Data<usage.refdata>`
  - :ref:`Investor's Exchange Data<usage.iexdata>`
  - :ref:`API System Metadata<usage.apistatus>`

These modules provide classes and functions to execute queries to IEX Cloud.

.. _usage.account:

Account
-------

.. seealso:: :ref:`Account<account>`


.. _usage.stocks:

Stocks
------

.. seealso:: For more information, see :ref:`Stocks<stocks>`.



Real-time Quotes
----------------

To obtain real-time quotes for one or more symbols, use the ``get_price``
method of the ``Stock`` object:

.. ipython:: python

    from iexfinance.stocks import Stock
    tsla = Stock('TSLA')
    tsla.get_price()

or for multiple symbols, use a list or list-like object (Tuple, Pandas Series,
etc.):

.. ipython:: python

    batch = Stock(["TSLA", "AAPL"])
    batch.get_price()


Historical Data
---------------

It's possible to obtain historical data the ``get_historical_data`` and
``get_historical_intraday``.

Daily
~~~~~

To obtain daily historical price data for one or more symbols, use the
``get_historical_data`` function. This will return a daily time-series of the ticker
requested over the desired date range (``start`` and ``end`` passed as
``datetime.datetime`` objects):

.. ipython:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_data

    start = datetime(2017, 1, 1)
    end = datetime(2018, 1, 1)

    df = get_historical_data("TSLA", start, end)


For Pandas DataFrame output formatting, pass ``output_format``:

.. ipython:: python

    df = get_historical_data("TSLA", start, end, output_format='pandas')


Minutely (Intraday)
~~~~~~~~~~~~~~~~~~~

To obtain historical intraday data, use ``get_historical_intraday`` as follows.
Pass an optional ``date`` to specify a date within three months prior to the
current day (default is current date):

.. ipython:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday

    date = datetime(2019, 5, 10)

    get_historical_intraday("AAPL", date)

or for a ``pandas.DataFrame`` indexed by each minute:

.. ipython:: python

    get_historical_intraday("AAPL", output_format='pandas').head()


Endpoints
~~~~~~~~~

The  ``Stock`` object can obtain each
of these endpoints. Requests for single symbols will return the *exact* results
from that endpoint as shown in the IEX API documentation (see below). Requests
for multiple symbols will return a symbol-indexed dictionary of
the endpoint requested.

**Endpoint Method** examples ``get_quote()``, ``get_volume_by_venue()``

.. ipython:: python

	from iexfinance.stocks import Stock
	aapl = Stock("AAPL")
    aapl.get_previous_day_prices()


For a detailed list of the *endpoint methods*, see
:ref:`here <stocks.contents>`.

Fields
~~~~~~

To obtain individual fields from an endpoint, select :ref:`Additional Methods
<stocks.additional-methods>` are also provided.

Examples ``get_open()``, ``get_name()``

**Single Symbol**

.. ipython:: python

    aapl = Stock("AAPL")
    aapl.get_open()
    aapl.get_price()

**Multiple Symbols**

.. ipython:: python

    b = Stock(["AAPL", "TSLA"])
    b.get_open()


For a detailed list of these functions, see :ref:`here <stocks>`.

Endpoint-Specific Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Top-level parameters may be passed to the ``Stock`` function, including
``output_format`` and request parameters (such as ``retry_count``, and
``pause``) - the latter of which will be used should any queries made by
the object fail. These parameters are passed keyword arguments, and are
entirely optional.

Certain endpoints (such as quote and chart), however, allow customizable
parameters. To specify one of these parameters, merely pass it to an endpoint
method as a keyword argument.

.. code-block:: python

    aapl = Stock("AAPL", output_format='pandas')
    aapl.get_quote(displayPercent=True).loc["ytdChange"]

.. note:: The ``output_format`` from the initial
  call to the ``Stock`` function will be used (if the output format has not been
  change through ``change_output_format`` since) and **cannot be changed**
  through calls to endpoint methods. See :ref:`Stocks/Equities <stocks>` for
  more information.


.. _usage.refdata:

Reference Data
--------------

.. seealso:: :ref:`Reference Data<refdata>`


.. _usage.iexdata:

Investor's Exchange Data
------------------------

.. seealso:: :ref:`Investor's Exchange Data<iexdata>`

.. _usage.apistatus:

API System Metadata
-------------------

.. seealso:: :ref:`API System Metadata<apidata>`


.. _usage.caching:

Caching
-------

iexfinance supports the caching of HTTP requests to IEX using the
`requests-cache <https://pypi.python.org/pypi/requests-cache>`__ package.

.. seealso:: :ref:`Caching Queries<caching>`
