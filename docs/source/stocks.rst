.. _stocks:


******
Stocks
******


The simplest way to obtain data using the `Stocks <https://iextrading.com/developer/docs/#stocks>`__ endpoint is by calling the ``Stock`` function with a symbol (*str*) or list of
symbols (*list*). ``Stock`` will return a :ref:`StockReader<stocks.StockReader>` instance.

.. ipython:: python

    from iexfinance import Stock
    aapl = Stock("aapl")
    aapl.get_price()

The Stock endpoints of the `IEX Developer API <https://iextrading.com/developer/>`__ are below, each of which contains data regarding a different aspect of the security/securities.
Requests (:ref:`StockReader<stocks.StockReader>`) will return a symbol-indexed dictionary of
the endpoint requested.

.. autoclass:: iexfinance.stock.StockReader

```StockReader``` allows us to access data for up to 100 symbols at once, returning a dictionary of the results indexed by each symbol.

Endpoints
=========

.. _stocks.quote

Quote
-----

.. automethod:: iexfinance.stock.StockReader.get_quote

.. _stocks.quote-field-methods

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

.. _stocks.chart


Chart
-----

.. automethod:: iexfinance.stock.StockReader.get_chart


.. _stocks.book

Book
----

.. automethod:: iexfinance.stock.StockReader.get_book


.. _stocks.open-close

Open/Close
----------


.. automethod:: iexfinance.stock.StockReader.get_open_close


.. _stocks.previous

Previous
--------


.. automethod:: iexfinance.stock.StockReader.get_previous


.. _stocks.company

Company
-------


.. automethod:: iexfinance.stock.StockReader.get_company


.. _stocks.key-stats

Key Stats
---------


.. automethod:: iexfinance.stock.StockReader.get_key_stats

.. _stocks.key-stats-field-methods

Field methods
^^^^^^^^^^^^^

.. automethod:: iexfinance.stock.StockReader.get_beta
.. automethod:: iexfinance.stock.StockReader.get_short_interest
.. automethod:: iexfinance.stock.StockReader.get_short_ratio
.. automethod:: iexfinance.stock.StockReader.get_latest_eps
.. automethod:: iexfinance.stock.StockReader.get_shares_outstanding
.. automethod:: iexfinance.stock.StockReader.get_float
.. automethod:: iexfinance.stock.StockReader.get_eps_consensus


.. _stocks.peers

Peers
-----

.. automethod:: iexfinance.stock.StockReader.get_peers


.. _stocks.relevant

Relevant
--------


.. automethod:: iexfinance.stock.StockReader.get_relevant


.. _stocks.news

News
----

.. automethod:: iexfinance.stock.StockReader.get_news


.. _stocks.financials

Financials
----------

.. automethod:: iexfinance.stock.StockReader.get_financials


.. _stocks.earnings

Earnings
--------

.. automethod:: iexfinance.stock.StockReader.get_earnings


.. _stocks.dividends

Dividends
---------


.. automethod:: iexfinance.stock.StockReader.get_dividends


.. _stocks.splits

Splits
------


.. automethod:: iexfinance.stock.StockReader.get_splits


.. _stocks.logo

Logo
----



.. automethod:: iexfinance.stock.StockReader.get_logo


.. _stocks.price

Price
-----


.. automethod:: iexfinance.stock.StockReader.get_price


.. _stocks.delayed-quote

Delayed Quote
-------------


.. automethod:: iexfinance.stock.StockReader.get_delayed_quote


.. _stocks.list

List
----

.. warning:: `list <https://iextrading.com/developer/docs/#list>`__  endpoint not supported at this time.


.. _stocks.effective-spread

Effective Spread
----------------


.. automethod:: iexfinance.stock.StockReader.get_effective_spread


.. _stocks.volume-by-venue

Volume by Venue
---------------


.. automethod:: iexfinance.stock.StockReader.get_volume_by_venue



.. _stocks.parameters:

Parameters
==========

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)

+----------------------+------------------------------------------------------------+-------------+
| Option               | Endpoint                                                   | Default     |
+======================+============================================================+=============+
| ``displayPercent``   | `quote <https://iextrading.com/developer/docs/#quote>`__   | ``False``   |
+----------------------+------------------------------------------------------------+-------------+
| ``_range``            | `chart <https://iextrading.com/developer/docs/#chart>`__   | ``1m``      |
+----------------------+------------------------------------------------------------+-------------+
| ``last``             | `news <https://iextrading.com/developer/docs/#news>`__     | ``10``      |
+----------------------+------------------------------------------------------------+-------------+

.. note:: Due to collisions between the dividends and splits range options that require separate requests and merging. The single _range value specified will apply to the chart, dividends, and splits endpoints. We have contacted IEX about this issue and hope to resolve it soon.


.. _stocks.utility-methods:

Utility Methods
===============

.. automethod:: iexfinance.stock.StockReader.refresh


.. _stocks.examples:

Examples
========

.. _stocks.examples-endpoint-methods

Endpoint Methods
----------------

.. ipython:: python

    from iexfinance import Stock as iex
    air_transport = Stock(['AAL', 'DAL', 'LUV'], output_format='pandas')
    air_transport.get_quote().head()

.. _stocks.examples-field-methods

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
