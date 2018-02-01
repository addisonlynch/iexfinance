.. _stocks:


******
Stocks
******

iexfinance takes an object-oriented approach to the `Stocks <https://iextrading.com/developer/#stocks>`__ endpoints of the `IEX Developer API <https://iextrading.com/developer/>`__.

The simplest way to obtain data from these endpoints is by calling the top-level ``Stock`` function with a symbol (*str*) or list of
symbols (*list*). ``Stock`` will return a ``StockReader`` instance.

.. ipython:: python

    from iexfinance import Stock
    aapl = Stock("aapl")
    aapl.get_price()


```StockReader``` allows us to access data for up to 100 symbols at once, returning a dictionary of the results indexed by each symbol.


.. autoclass:: iexfinance.stock.StockReader


**Parameters**

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument to the Stock function at instantiation (see :ref:`example <stocks.passing-parameters>`). Further, iexfinance supports pandas DataFrame as an output format for most endpoints of 'pandas' is specified as the `output_format` parameter.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)

+----------------------+------------------------------------------------------------+-------------+
| Option               | Endpoint                                                   | Default     |
+======================+============================================================+=============+
| ``displayPercent``   | `Quote <https://iextrading.com/developer/docs/#quote>`__   | ``False``   |
+----------------------+------------------------------------------------------------+-------------+
| ``_range``           | `Chart <https://iextrading.com/developer/docs/#chart>`__   | ``1m``      |
+----------------------+------------------------------------------------------------+-------------+
| ``last``             | `News <https://iextrading.com/developer/docs/#news>`__     | ``10``      |
+----------------------+------------------------------------------------------------+-------------+
| ``output_format``    | All (some, such as Chart and Price, are JSON only)         | ``json``    |
+----------------------+------------------------------------------------------------+-------------+

.. note:: Due to collisions between the dividends and splits range options that require separate requests and merging. The single _range value specified will apply to the chart, dividends, and splits endpoints. We have contacted IEX about this issue and hope to resolve it soon.



Endpoints
=========

Endpoint methods will return a symbol-indexed dictionary of the endpoint requested. If :code:`Stock` is passed a single symbol, these methods will return the *data only* (verbatim from IEX docs examples). See examples :ref:`below <stocks.examples-endpoint-methods>` for clarification.

    - :ref:`Book<stocks.book>`
    - :ref:`Chart<stocks.chart>`
    - :ref:`Company<stocks.company>`
    - :ref:`Delayed Quote<stocks.delayed-quote>`
    - :ref:`Dividends<stocks.dividends>`
    - :ref:`Earnings<stocks.earnings>`
    - :ref:`Effective Spread<stocks.effective-spread>`
    - :ref:`Financials<stocks.financials>`
    - :ref:`Key Stats<stocks.key-stats>`
    - :ref:`Logo<stocks.logo>`
    - :ref:`News<stocks.news>`
    - :ref:`OHLC<stocks.ohlc>`
    - :ref:`Open/Close<stocks.open-close>`
    - :ref:`Peers<stocks.peers>`
    - :ref:`Previous<stocks.previous>`
    - :ref:`Price<stocks.price>`
    - :ref:`Quote<stocks.quote>`
    - :ref:`Relevant<stocks.relevant>`
    - :ref:`Splits<stocks.splits>`
    - :ref:`Time Series<stocks.time-series>`
    - :ref:`Volume by Venue<stocks.volume-by-venue>`


.. _stocks.book:

Book
----

.. automethod:: iexfinance.stock.StockReader.get_book

.. _stocks.chart:

Chart
-----

.. automethod:: iexfinance.stock.StockReader.get_chart


.. _stocks.company:

Company
-------


.. automethod:: iexfinance.stock.StockReader.get_company


.. _stocks.delayed-quote:

Delayed Quote
-------------


.. automethod:: iexfinance.stock.StockReader.get_delayed_quote



.. _stocks.dividends:

Dividends
---------


.. automethod:: iexfinance.stock.StockReader.get_dividends



.. _stocks.earnings:

Earnings
--------

.. automethod:: iexfinance.stock.StockReader.get_earnings



.. _stocks.effective-spread:

Effective Spread
----------------


.. automethod:: iexfinance.stock.StockReader.get_effective_spread


.. _stocks.financials:

Financials
----------

.. automethod:: iexfinance.stock.StockReader.get_financials


.. _stocks.key-stats:

Key Stats
---------


.. automethod:: iexfinance.stock.StockReader.get_key_stats

.. _stocks.key-stats-field-methods:

Field methods
^^^^^^^^^^^^^

.. automethod:: iexfinance.stock.StockReader.get_beta
.. automethod:: iexfinance.stock.StockReader.get_short_interest
.. automethod:: iexfinance.stock.StockReader.get_short_ratio
.. automethod:: iexfinance.stock.StockReader.get_latest_eps
.. automethod:: iexfinance.stock.StockReader.get_shares_outstanding
.. automethod:: iexfinance.stock.StockReader.get_float
.. automethod:: iexfinance.stock.StockReader.get_eps_consensus



.. _stocks.list:

List
----

.. warning:: `list <https://iextrading.com/developer/docs/#list>`__  endpoint not supported at this time.




.. _stocks.logo:

Logo
----



.. automethod:: iexfinance.stock.StockReader.get_logo


.. _stocks.news:

News
----

.. automethod:: iexfinance.stock.StockReader.get_news


.. _stocks.ohlc:

OHLC
----

.. automethod:: iexfinance.stock.StockReader.get_ohlc


.. _stocks.open-close:

Open/Close
----------

.. seealso:: Time Series is an alias for the :ref:`OHLC <stocks.ohlc>` endpoint


.. automethod:: iexfinance.stock.StockReader.get_open_close


.. _stocks.peers:

Peers
-----

.. automethod:: iexfinance.stock.StockReader.get_peers




.. _stocks.previous:

Previous
--------


.. automethod:: iexfinance.stock.StockReader.get_previous


.. _stocks.price:

Price
-----


.. automethod:: iexfinance.stock.StockReader.get_price


.. _stocks.quote:

Quote
-----

.. automethod:: iexfinance.stock.StockReader.get_quote

.. _stocks.quote-field-methods:

Field methods
^^^^^^^^^^^^^

.. automethod:: iexfinance.stock.StockReader.get_company_name
.. automethod:: iexfinance.stock.StockReader.get_sector
.. automethod:: iexfinance.stock.StockReader.get_open
.. automethod:: iexfinance.stock.StockReader.get_close
.. automethod:: iexfinance.stock.StockReader.get_years_high
.. automethod:: iexfinance.stock.StockReader.get_years_low
.. automethod:: iexfinance.stock.StockReader.get_ytd_change
.. automethod:: iexfinance.stock.StockReader.get_volume
.. automethod:: iexfinance.stock.StockReader.get_market_cap


.. _stocks.relevant:


Relevant
--------


.. automethod:: iexfinance.stock.StockReader.get_relevant




.. _stocks.splits:

Splits
------


.. automethod:: iexfinance.stock.StockReader.get_splits


.. _stocks.time-series:

Time Series
-----------

.. seealso:: Time Series is an alias for the :ref:`Chart<stocks.chart>` endpoint

.. automethod:: iexfinance.stock.StockReader.get_time_series


.. _stocks.volume-by-venue:

Volume by Venue
---------------


.. automethod:: iexfinance.stock.StockReader.get_volume_by_venue



.. _stocks.utility-methods:

Utility Methods
===============

.. automethod:: iexfinance.stock.StockReader.refresh


.. _stocks.examples:

Examples
========

.. _stocks.examples-endpoint-methods:

Endpoint Methods
----------------

A single symbol request will return data *exactly* as it appears in the IEX docs examples:

.. ipython:: python

    from iexfinance import Stock
    aapl = Stock("AAPL")
    a.get_price()

While multi-symbol requests will return a symbol-indexed list of the endpoint's data

.. ipython::python

    batch = Stock(["AAPL", "TSLA"])
    batch.get_price()

Most endpoints can be formatted as a `pandas.DataFrame`. Multi-symbol requests will concatenate the dataframes for each:

.. ipython:: python

    from iexfinance import Stock as iex
    air_transport = Stock(['AAL', 'DAL', 'LUV'], outputFormat='pandas')
    air_transport.get_quote().head()

.. _stocks.passing-parameters:

Passing Parameters
^^^^^^^^^^^^^^^^^^

**Endpoint-specific**

We show an example using the `last` parameter for the News endpoint:

.. ipython:: python

    aapl = Stock("AAPL")

    len(aapl.get_news())

by default, News returns the last 10 items (`last is 10 by default`), but we can specify a custom value:

.. ipython:: python

    aapl = Stock("AAPL", last=35)

    len(aapl.get_news())

With a custom value specified, News now returns the previous 35 items.

.. _stocks.output-formatting:

Output Formatting
^^^^^^^^^^^^^^^^^

Most endpoints allow for pandas DataFrame-formatted output:

.. ipython:: python

    aapl = Stock("AAPL", output_format='pandas')

    aapl.get_quote().head()




.. _stocks.examples-field-methods:

Field Methods
-----------------


``get_open()``, ``get_company_name()``

Single symbol

.. ipython:: python

    aapl.get_open()
    aapl.get_company_name()

Multiple symbols

.. ipython:: python

    b = Stock(["AAPL", "TSLA"])
    b.get_open()
    b.get_company_name()
