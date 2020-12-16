.. _stocks:


.. currentmodule:: iexfinance

Stocks / Equities
=================

.. _stocks.overview:

Overview
--------

This documentation is organized as a 1:1 mirror of the
IEX Cloud `Stocks/Equities Documentation <https://iexcloud.io/docs/api/#stocks-equities>`__.

The ``Stock`` :ref:`object<stocks.stock_object>` is instantiated with one or
more symbols (equities, ETFs, etc.) and allows access to most endpoints:

.. ipython:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")
    aapl.get_price()

Certain endpoints such as :ref:`Historical Data<stocks.historical>`,
which are unrelated to specific symbols, are supported by top-level functions
(i.e. ``iexfinance.stocks.get_historical_data``). This function is
**optimized** to achieve the lowest possible message count for retrieval in a
single request.

.. ipython:: python

    from iexfinance.stocks import get_historical_data

    get_historical_data("AAPL", start="20190101", end="20200101",
                        output_format='pandas').head()


See :ref:`Additional Methods<stocks.additional-methods>` for more a list of
methods available.

.. _stocks.contents:

Endpoints
---------

.. contents::
    :depth: 2


.. _stocks.stock_object:

The ``Stock`` object
~~~~~~~~~~~~~~~~~~~~

The ``Stock`` object allows retrieval of
endpoints  (`Earnings
<https://iexcloud.io/docs/api/#earnings>`__,
`Quote <https://iexcloud.io/docs/api/#quote>`__, etc) for up to 100 symbols
at once.


.. autoclass:: iexfinance.stocks.base.Stock


.. _stocks.basic_usage:

Basic Usage Example
~~~~~~~~~~~~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import Stock
    aapl = Stock("aapl")
    aapl.get_price()

.. _stocks.advanced_stats:

Advanced Stats
--------------

.. automethod:: iexfinance.stocks.base.Stock.get_advanced_stats


.. _stocks.balance_sheet:

Balance Sheet
-------------

.. automethod:: iexfinance.stocks.base.Stock.get_balance_sheet

.. _stocks.book:

Book
----
.. automethod:: iexfinance.stocks.base.Stock.get_book


.. _stocks.cash_flow:

Cash Flow
---------

.. automethod:: iexfinance.stocks.base.Stock.get_cash_flow

.. _stocks.charts:

Charts
------
.. automethod:: iexfinance.stocks.base.Stock.get_chart


.. _stocks.company:

Company
-------

.. automethod:: iexfinance.stocks.base.Stock.get_company

.. _stocks.delayed_quote:

Delayed Quote
-------------

.. automethod:: iexfinance.stocks.base.Stock.get_delayed_quote

.. _stocks.dividends:

Dividends (Basic)
-----------------

.. automethod:: iexfinance.stocks.base.Stock.get_dividends



.. _stocks.earnings:

Earnings
--------

.. warning:: Beginning December 1, 2020, use of this endpoint will require
             additional entitlements. Full details can be found in the
             IEX Cloud Help Center. See `here <https://intercom.help/iexcloud/en/articles/4529082-iex-cloud-s-2020-data-upgrade>`_
             for additional information.

.. automethod:: iexfinance.stocks.base.Stock.get_earnings

.. _stocks.estimates:

Estimates
---------

.. warning:: Beginning December 1, 2020, use of this endpoint will require
             additional entitlements. Full details can be found in the
             IEX Cloud Help Center. See `here <https://intercom.help/iexcloud/en/articles/4529082-iex-cloud-s-2020-data-upgrade>`_
             for additional information.

.. automethod:: iexfinance.stocks.base.Stock.get_estimates

.. _stocks.financials:

Financials
----------
.. automethod:: iexfinance.stocks.base.Stock.get_financials

.. _stocks.fund_ownership:

Fund Ownership
--------------

.. automethod:: iexfinance.stocks.base.Stock.get_fund_ownership

.. _stocks.historical:

Historical Prices
-----------------

.. note:: The ``Stock.get_historical_prices`` method is an *exact* mirror of
          the Historical Prices (chart) endpoint and accepts all
          parameters, but is **not optimized**. Use ``get_historical_data`` for
          optimized message counts. ``get_historical_data`` accepts ``start``,
          ``end`` (optional) along with the parameter ``close_only``, and no
          other parameters.

The method used to obtain historical prices from a ``Stock`` object:

.. ipython:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")
    aapl.get_historical_prices()


Historical time series data is also available through the **optimized**
top-level ``get_historical_data`` and
``get_historical_intraday`` functions of ``stocks``, which source the
`Historical Prices <https://iexcloud.io/docs/api/#historical-prices>`__
endpoint, and accept a date or date range for retrieval.

Daily data can be retrieved from up to 15 years before the current date.

Daily
~~~~~

To obtain daily historical data, use ``get_historical_data``.

.. autofunction:: iexfinance.stocks.get_historical_data


Example
^^^^^^^


.. ipython:: python
    :okwarning:

    from iexfinance.stocks import get_historical_data
    from datetime import datetime

    start = datetime(2017, 2, 9)
    end = datetime(2017, 5, 24)

    f = get_historical_data('AAPL', start, end, output_format='pandas')
    f.loc["2017-02-09"]


Minutely
~~~~~~~~

To obtain one-minute intraday data for a given date, use
``get_historical_intraday``. **Note: this endpoint has a maximum of one symbol
and a single date.**

.. autofunction:: iexfinance.stocks.get_historical_intraday

.. ipython:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday

    date = datetime(2018, 11, 27)

    data = get_historical_intraday("AAPL", date, output_format='pandas')
    data.head()

Closing Prices Only
^^^^^^^^^^^^^^^^^^^

To retrieve closing prices only, use ``get_historical_data`` and set
``close_only=True``:

.. ipython:: python

    from iexfinance.stocks import get_historical_data

    get_historical_data("AAPL", "20190617", close_only=True)



.. _stocks.income_statement:

Income Statement
----------------

.. automethod:: iexfinance.stocks.base.Stock.get_income_statement


.. _stocks.insider_roster:

Insider Roster
--------------

.. automethod:: iexfinance.stocks.base.Stock.get_insider_roster

.. _stocks.insider_summary:

Insider Summary
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_insider_summary


.. _stocks.insider_transactions:

Insider Transactions
--------------------

.. automethod:: iexfinance.stocks.base.Stock.get_insider_transactions


.. _stocks.institutional_ownership:

Institutional Ownership
-----------------------

.. automethod:: iexfinance.stocks.base.Stock.get_institutional_ownership


.. _stocks.key_stats:

Key Stats
---------

.. automethod:: iexfinance.stocks.base.Stock.get_key_stats


.. _stocks.largest_trades:

Largest Trades
--------------
.. automethod:: iexfinance.stocks.base.Stock.get_largest_trades


.. _stocks.logo:

Logo
----

.. automethod:: iexfinance.stocks.base.Stock.get_logo

.. _stocks.ohlc:

OHLC
----
.. automethod:: iexfinance.stocks.base.Stock.get_ohlc


.. _stocks.open_close:

Open/Close Price
----------------
.. seealso:: Time Series is an alias for the :ref:`OHLC <stocks.ohlc>` endpoint


.. automethod:: iexfinance.stocks.base.Stock.get_open_close




.. _stocks.peers:

Peer Groups
-----------
.. automethod:: iexfinance.stocks.base.Stock.get_peers


.. _stocks.previous_day_prices:

Previous Day Price
------------------

.. warning:: ``get_previous`` has been deprecated and renamed
            ``get_previous_day_prices``.

.. automethod:: iexfinance.stocks.base.Stock.get_previous_day_prices



.. _stocks.price-only:

Price Only
----------

.. automethod:: iexfinance.stocks.base.Stock.get_price


.. _stocks.price_target:

Price Target
------------

.. warning:: Beginning December 1, 2020, use of this endpoint will require
             additional entitlements. Full details can be found in the
             IEX Cloud Help Center. See `here <https://intercom.help/iexcloud/en/articles/4529082-iex-cloud-s-2020-data-upgrade>`_
             for additional information.

.. automethod:: iexfinance.stocks.base.Stock.get_price_target

.. _stocks.quote:

Quote
-----
.. automethod:: iexfinance.stocks.base.Stock.get_quote


.. _stocks.relevant_stocks:


Relevant Stocks
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_relevant_stocks

.. _stocks.sector.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_sector_performance

    get_sector_performance(output_format='pandas')



.. _stocks.splits:

Splits (Basic)
--------------

.. automethod:: iexfinance.stocks.base.Stock.get_splits


.. _stocks.time_series:

Time Series
-----------
.. seealso:: Time Series is an alias for the :ref:`Chart<stocks.charts>` endpoint

.. automethod:: iexfinance.stocks.base.Stock.get_time_series


.. _stocks.volume_by_venue:

Volume by Venue
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_volume_by_venue


.. _stocks.additional-methods:

Additional Methods
------------------

In addition, various additional ``Stock`` methods are provided for certain
endpoints. These methods will allow retrieval of a single datapoint, such as ``get_open``,
``get_company_name``, etc. Field methods are displayed below the endpoint
methods for which they are available (namely :ref:`Quote<stocks.quote>`
and :ref:`Key Stats<stocks.key_stats>`).


.. _stocks.key_stats_field_methods:

Key Stats
~~~~~~~~~

.. automethod:: iexfinance.stocks.base.Stock.get_beta
.. automethod:: iexfinance.stocks.base.Stock.get_short_interest
.. automethod:: iexfinance.stocks.base.Stock.get_short_ratio
.. automethod:: iexfinance.stocks.base.Stock.get_latest_eps
.. automethod:: iexfinance.stocks.base.Stock.get_shares_outstanding
.. automethod:: iexfinance.stocks.base.Stock.get_float
.. automethod:: iexfinance.stocks.base.Stock.get_eps_consensus


.. _stocks.quote_field_methods:

Quote
~~~~~

.. automethod:: iexfinance.stocks.base.Stock.get_company_name
.. automethod:: iexfinance.stocks.base.Stock.get_sector
.. automethod:: iexfinance.stocks.base.Stock.get_open
.. automethod:: iexfinance.stocks.base.Stock.get_close
.. automethod:: iexfinance.stocks.base.Stock.get_years_high
.. automethod:: iexfinance.stocks.base.Stock.get_years_low
.. automethod:: iexfinance.stocks.base.Stock.get_ytd_change
.. automethod:: iexfinance.stocks.base.Stock.get_volume
.. automethod:: iexfinance.stocks.base.Stock.get_market_cap


.. _stocks.movers:

Market Movers
~~~~~~~~~~~~~

The `List <hhttps://iexcloud.io/docs/api/#list>`__ endpoint of stocks
provides information about market movers from a given trading day. iexfinance
implements these market mover lists with the functions listed
below. These functions return a list of quotes of the top-10 symbols in each list.

* Gainers (``stocks.get_market_gainers``)
* Losers (``stocks.get_market_losers``)
* Most Active (``stocks.get_market_most_active``)
* IEX Volume (``stocks.get_market_iex_volume``)
* IEX Percent (``stocks.get_market_iex_percent``)
* In Focus (``stocks.get_market_in_focus``)

.. ipython:: python

    from iexfinance.stocks import get_market_gainers

    get_market_gainers()
