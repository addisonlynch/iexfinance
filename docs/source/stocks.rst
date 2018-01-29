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



Endpoints
=========

The Stock endpoints of the `IEX Developer API <https://iextrading.com/developer/>`__ are below, each of which contains data regarding a different aspect of the security/securities.
Requests (:ref:`StockReader<stocks.StockReader>`) will return a symbol-indexed dictionary of
the endpoint requested.

-  `Quote <https://iextrading.com/developer/docs/#quote>`__
-  `Chart <https://iextrading.com/developer/docs/#chart>`__
-  `Book <https://iextrading.com/developer/docs/#book>`__
-  `Open / Close <https://iextrading.com/developer/docs/#open-close>`__
-  `Previous <https://iextrading.com/developer/docs/#previous>`__
-  `Company <https://iextrading.com/developer/docs/#company>`__
-  `Key Stats <https://iextrading.com/developer/docs/#key-stats>`__
-  `Relevant <https://iextrading.com/developer/docs/#relevant>`__
-  `News <https://iextrading.com/developer/docs/#news>`__
-  `Financials <https://iextrading.com/developer/docs/#financials>`__
-  `Earnings <https://iextrading.com/developer/docs/#earnings>`__
-  `Dividends <https://iextrading.com/developer/docs/#dividends>`__
-  `Splits <https://iextrading.com/developer/docs/#splits>`__
-  `Logo <https://iextrading.com/developer/docs/#logo>`__
-  `Price <https://iextrading.com/developer/docs/#price>`__
-  `Delayed
   Quote <https://iextrading.com/developer/docs/#delayed-quote>`__
-   List (*not supported*)
-  `Effective
   Spread <https://iextrading.com/developer/docs/#effective-spread>`__
-  `Volume by
   Venue <https://iextrading.com/developer/docs/#volume-by-venue>`__

*Endpoint Method* Examples ``get_quote()``, ``get_volume_by_venue()``


Fields
======

To obtain individual Fields from an endpoint, select *field
methods* are also provided.

Examples ``get_open()``, ``get_name()``

**Share (single symbol)**

.. ipython:: python

    aapl.get_open()
    aapl.get_price()

**Batch (multiple symbols)**

.. ipython:: python

    b = Stock(["AAPL", "TSLA"])
    b.get_open()


For a detailed list of these functions, see :ref:`Share<stocks.Share>` or
:ref:`StockReader<stocks.StockReader>`.


.. _stocks.StockReader:


StockReader
===========

.. autoclass:: iexfinance.stock.StockReader

```StockReader``` allows us to access data for up to 100 symbols at once, returning a dictionary of the results indexed by each symbol.

.. _stocks.utility-methods:

Utility Methods
---------------

.. automethod:: iexfiannce.stock.StockReader.refresh

.. _stocks.endpoint-methods:

Endpoint Methods
----------------

.. automethod:: iexfinance.stock.StockReader.get_quote
.. automethod:: iexfinance.stock.StockReader.get_chart
.. automethod:: iexfinance.stock.StockReader.get_book
.. automethod:: iexfinance.stock.StockReader.get_open_close
.. automethod:: iexfinance.stock.StockReader.get_previous
.. automethod:: iexfinance.stock.StockReader.get_company
.. automethod:: iexfinance.stock.StockReader.get_key_stats
.. automethod:: iexfinance.stock.StockReader.get_relevant
.. automethod:: iexfinance.stock.StockReader.get_news
.. automethod:: iexfinance.stock.StockReader.get_financials
.. automethod:: iexfinance.stock.StockReader.get_earnings
.. automethod:: iexfinance.stock.StockReader.get_dividends
.. automethod:: iexfinance.stock.StockReader.get_splits
.. automethod:: iexfinance.stock.StockReader.get_logo
.. automethod:: iexfinance.stock.StockReader.get_price
.. automethod:: iexfinance.stock.StockReader.get_delayed_quote
.. automethod:: iexfinance.stock.StockReader.get_effective_spread
.. automethod:: iexfinance.stock.StockReader.get_volume_by_venue


note: there is no support for the
`list <https://iextrading.com/developer/docs/#list>`__ endpoint at this
time.

.. _stocks.field-methods:

Field Methods
-----------------

.. automethod:: iexfinance.stock.StockReader.get_company_name
.. automethod:: iexfinance.stock.StockReader.get_sector
.. automethod:: iexfinance.stock.StockReader.get_open
.. automethod:: iexfinance.stock.StockReader.get_close
.. automethod:: iexfinance.stock.StockReader.get_years_high
.. automethod:: iexfinance.stock.StockReader.get_years_low
.. automethod:: iexfinance.stock.StockReader.get_ytd_change
.. automethod:: iexfinance.stock.StockReader.get_volume
.. automethod:: iexfinance.stock.StockReader.get_market_cap
.. automethod:: iexfinance.stock.StockReader.get_beta
.. automethod:: iexfinance.stock.StockReader.get_short_interest
.. automethod:: iexfinance.stock.StockReader.get_short_ratio
.. automethod:: iexfinance.stock.StockReader.get_latest_eps
.. automethod:: iexfinance.stock.StockReader.get_shares_outstanding
.. automethod:: iexfinance.stock.StockReader.get_float
.. automethod:: iexfinance.stock.StockReader.get_eps_consensus

.. _stocks.parameters:

Parameters
----------

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


.. _stocks.examples:

Examples
--------

.. ipython:: python

    from iexfinance import Stock as iex
    air_transport = Stock(['AAL', 'DAL', 'LUV'])
    air_transport.get_open()
    air_transport.get_price()
