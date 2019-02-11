.. _stocks:


.. currentmodule:: iexfinance

Stocks
======

.. _stocks.overview:

Overview
--------

This documentation is organized as a 1:1 mirror of the
IEX Cloud `Stocks Documentation <https://iexcloud.io/docs/api/#stocks>`__.

The ``Stock`` :ref:`object<stocks.stock_object>` is instantiated with one or
more symbols (equities, ETFs, etc.) and allows access to most endpoints:

.. ipython:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL")
    aapl.get_price()

Certain endpoints, such as `Sector Performance <https://iexcloud.io/docs/api/#sector-performance>`__,
which are unrelated to specific symbols, are supported by top-level functions
(i.e. ``iexfinance.stocks.get_sector_performance``).

.. ipython:: python

    from iexfinance.stocks import get_sector_performance

    get_sector_performance()[0]

Additional utility functions, such as ``get_historical_data`` are provided as
well:

.. ipython:: python

    from iexfinance.stocks import get_historical_data

    get_historical_data("AAPL", output_format='pandas').head()


See :ref:`Additional Methods<stocks.additional_methods>` for more a list of
methods available.

.. _stocks.endpoint_list:

List of Endpoints
~~~~~~~~~~~~~~~~~

All endpoints not available as methods of the ``Stock`` object are noted below.


- :ref:`Balance Sheet<stocks.balance_sheet>`
- :ref:`Book<stocks.book>`
- :ref:`Cash Flow<stocks.cash_flow>`
- :ref:`Chart<stocks.chart>`
- :ref:`Collections<stocks.collections>` - ``get_collections``
- :ref:`Company<stocks.company>`
- :ref:`Crypto<stocks.crypto>` - ``get_crypto_quotes``
- :ref:`Delayed Quote<stocks.delayed_quote>`
- :ref:`Dividends<stocks.dividends>`
- :ref:`Earnings<stocks.earnings>`
- :ref:`Earnings Today<stocks.earnings_today>` - ``get_earnings_today``
- :ref:`Effective Spread<stocks.effective_spread>`
- :ref:`Estimates<stocks.estimates>`
- :ref:`Financials<stocks.financials>`
- :ref:`Historical<stocks.historical>` - ``get_historical_data`` and ``get_historical_intraday``
- :ref:`Key Stats<stocks.key_stats>`
- :ref:`Logo<stocks.logo>`
- :ref:`Market Volume<stocks.market_volume>` - ``get_market_volume``
- :ref:`News<stocks.news>`
- :ref:`OHLC<stocks.ohlc>`
- :ref:`Open/Close<stocks.open_close>`
- :ref:`Peers<stocks.peers>`
- :ref:`Previous Day Prices<stocks.previous_day_prices>`
- :ref:`Price<stocks.price>`
- :ref:`Price Target<stocks.price_target>`
- :ref:`Sector Performance<stocks.sector>` - ``get_sector_performance``
- :ref:`Quote<stocks.quote>`
- :ref:`Relevant Stocks<stocks.relevant_stocks>`
- :ref:`Splits<stocks.splits>`
- :ref:`Time Series<stocks.time_series>`
- :ref:`Volume by Venue<stocks.volume_by_venue>`


.. _stocks.stock_object:

The ``Stock`` object
~~~~~~~~~~~~~~~~~~~~

The ``Stock`` object allows retrieval of
endpoints  (`Earnings
<https://iextrading.com/developer/#earnings>`__,
`Quote <https://iextrading.com/developer/#quote>`__, etc) for up to 100 symbols
at once.


.. autoclass:: iexfinance.stocks.base.Stock


.. _stocks.basic_usage:

Basic Usage Example
~~~~~~~~~~~~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import Stock
    aapl = Stock("aapl")
    aapl.get_price()


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

.. _stocks.chart:

Chart
-----
.. automethod:: iexfinance.stocks.base.Stock.get_chart


.. _stocks.collections:

Collections
-----------

The `Collections <https://iextrading.com/developer/docs/#collections>`__
endpoint of Stocks allows retrieval of certain groups of companies, organized
by:

- sector
- tag
- list (see the :ref:`list endpoint <stocks.list>`)

Use ``get_collections`` to access.


.. autofunction:: iexfinance.stocks.get_collections


.. _stocks.collections.examples:

Examples
~~~~~~~~

**Tag**

.. ipython:: python

    from iexfinance.stocks import get_collections

    get_collections("Computer Hardware", output_format='pandas').head()

**Sector**

.. ipython:: python

    get_collections("Industrials", output_format='pandas').head()



.. _stocks.company:

Company
-------

.. automethod:: iexfinance.stocks.base.Stock.get_company

.. _stocks.crypto:

Cryptocurrencies
----------------

As of the 5/18/2018 IEX Provider update, quotes are provided for certain Cryptocurrencies. Access to these quotes is available by creating a Stock object and using the ``get_quote`` method.

The following tickers are supported:

- Bitcoin USD (BTCUSDT)
- EOS USD (EOSUSDT)
- Ethereum USD (ETHUSDT)
- Binance Coin USD (BNBUSDT)
- Ontology USD (ONTUSDT)
- Bitcoin Cash USD (BCCUSDT)
- Cardano USD (ADAUSDT)
- Ripple USD (XRPUSDT)
- TrueUSD (TUSDUSDT)
- TRON USD (TRXUSDT)
- Litecoin USD (LTCUSDT)
- Ethereum Classic USD (ETCUSDT)
- MIOTA USD (IOTAUSDT)
- ICON USD (ICXUSDT)
- NEO USD (NEOUSDT)
- VeChain USD (VENUSDT)
- Stellar Lumens USD (XLMUSDT)
- Qtum USD (QTUMUSDT)

To retrieve quotes for all available cryptocurrencies, use the
``get_crypto_quotes`` function:


.. autofunction:: iexfinance.stocks.get_crypto_quotes


.. _stocks.crypto.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_crypto_quotes

    get_crypto_quotes(output_format='pandas').head()



.. _stocks.delayed_quote:

Delayed Quote
-------------

.. automethod:: iexfinance.stocks.base.Stock.get_delayed_quote



.. _stocks.dividends:

Dividends
---------

.. automethod:: iexfinance.stocks.base.Stock.get_dividends



.. _stocks.earnings:

Earnings
--------

.. automethod:: iexfinance.stocks.base.Stock.get_earnings

.. _stocks.earnings_today:

Earnings Today
--------------

.. warning:: ``get_todays_earnings`` has been deprecated and renamed
            ``get_earnings_today``.

Earnings Today was added to the Stocks endpoints in 2018. Access is provided
through the  ``get_earnings_today`` function.


.. autofunction:: iexfinance.stocks.get_earnings_today


.. note:: ``get_earnings_today`` supports JSON output formatting only.


.. _stocks.earnings.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_todays_earnings

    get_todays_earnings()["bto"]




.. _stocks.effective_spread:

Effective Spread
----------------

.. automethod:: iexfinance.stocks.base.Stock.get_effective_spread


.. _stocks.estimates:

Estimates
---------

.. automethod:: iexfinance.stocks.base.Stock.get_estimates

.. _stocks.financials:

Financials
----------
.. automethod:: iexfinance.stocks.base.Stock.get_financials


.. _stocks.historical:

Historical Prices
-----------------

Historical time series data is available through the
``get_historical_data`` and ``get_historical_intraday`` functions of
``stocks``, which
source the
`chart <https://iextrading.com/developer/docs/#chart>`__ endpoint.

Daily data can be retrieved from up to 5 years before the current date, and
historical data up to 3 months prior to the current date.

Daily
~~~~~

To obtain daily historical data, use ``get_historical_data``.

.. autofunction:: iexfinance.stocks.get_historical_data


If no date parameters are passed, the start date will default to 2015/1/1
and the end date will default to the current date.


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



.. _stocks.income_statement:

Income Statement
----------------

.. automethod:: iexfinance.stocks.base.Stock.get_income_statement

.. _stocks.ipo_calendar:

IPO Calendar
------------

IPO Calendar was added to the Stocks endpoints in 2018. Access is provided
through the  ``get_ipo_calendar`` function.

.. autofunction:: iexfinance.stocks.get_ipo_calendar

There are two possible values for the ``period`` parameter, of which
``upcoming-ipos`` is the default. ``today-ipos`` is also available.

..  _stocks.ipo_calendar.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_ipo_calendar

    get_ipo_calendar()["rawData"][0]




.. _stocks.key_stats:

Key Stats
---------

.. automethod:: iexfinance.stocks.base.Stock.get_key_stats


.. _stocks.list:

List
----
.. seealso:: :ref:`Market Movers<stocks.movers>`


.. _stocks.largest_trades:

Largest Trades
--------------
.. automethod:: iexfinance.stocks.base.Stock.get_largest_trades


.. _stocks.logo:

Logo
----

.. automethod:: iexfinance.stocks.base.Stock.get_logo

.. _stocks.market_volume:

Market Volume (U.S)
-------------------

Market Volume returns real-time traded volume on U.S. Markets. Access is
provided through the ``get_market_volume`` function.


.. autofunction:: iexfinance.stocks.get_market_volume


.. _stocks.market_volume.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_market_volume

    get_market_volume()

.. _stocks.news:

News
----
.. automethod:: iexfinance.stocks.base.Stock.get_news


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

Peers
-----
.. automethod:: iexfinance.stocks.base.Stock.get_peers


.. _stocks.previous_day_prices:

Previous Day Prices
-------------------

.. automethod:: iexfinance.stocks.base.Stock.get_previous


.. _stocks.price:

Price
-----

.. automethod:: iexfinance.stocks.base.Stock.get_price


.. _stocks.price_target:

Price Target
------------

.. automethod:: iexfinance.stocks.base.Stock.get_price_target

.. _stocks.quote:

Quote
-----
.. automethod:: iexfinance.stocks.base.Stock.get_quote


.. _stocks.relevant_stocks:


Relevant Stocks
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_relevant

.. _stocks.sector:

Sector Performance
------------------

Sector Performance was added to the Stocks endpoints in 2018. Access to this endpoint is provided through the ``get_sector_performance`` function.

.. autofunction:: iexfinance.stocks.get_sector_performance


.. _stocks.sector.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_sector_performance

    get_sector_performance(output_format='pandas')



.. _stocks.splits:

Splits
------

.. automethod:: iexfinance.stocks.base.Stock.get_splits


.. _stocks.time_series:

Time Series
-----------
.. seealso:: Time Series is an alias for the :ref:`Chart<stocks.chart>` endpoint

.. automethod:: iexfinance.stocks.base.Stock.get_time_series


.. _stocks.volume_by_venue:

Volume by Venue
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_volume_by_venue


.. _stocks.additional_methods:

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

The `List <https://iextrading.com/developer/docs/#list>`__ endpoint of stocks
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

    get_market_gainers()[0]
