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

Certain endpoints such as :ref:`Historical Data<stocks.historical>`,
which are unrelated to specific symbols, are supported by top-level functions
(i.e. ``iexfinance.stocks.get_historical_data``). This function is
**optimized** to achieve the lowest possible message count for retrieval in a
single request.

.. ipython:: python

    from iexfinance.stocks import get_historical_data

    get_historical_data("AAPL", start="20190101", end="20200101", 
                        output_format='pandas').head()


See :ref:`Additional Methods<stocks.additional_methods>` for more a list of
methods available.

.. _stocks.endpoint_list:

List of Endpoints
~~~~~~~~~~~~~~~~~

All endpoints not available as methods of the ``Stock`` object are noted below.

Endpoints which are supported by top-level functions are noted.


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
- :ref:`Estimates<stocks.estimates>`
- :ref:`Financials<stocks.financials>`
- :ref:`Fund Ownership<stocks.fund_ownership>`
- :ref:`Historical Prices<stocks.historical>` - ``get_historical_data`` and ``get_historical_intraday``
- :ref:`Income Statement<stocks.income_statement>`
- :ref:`Insider Roster<stocks.insider_roster>`
- :ref:`Insider Summary<stocks.insider_summary>`
- :ref:`Insider Transactions<stocks.insider_transactions>`
- :ref:`Institutional Ownership<stocks.institutional_ownership>`
- :ref:`IPO Calendar<stocks.ipo_calendar>`
- :ref:`Key Stats<stocks.key_stats>`
- :ref:`Largest Trades<stocks.largest_trades>`
- :ref:`List<stocks.list>`
- :ref:`Logo<stocks.logo>`
- :ref:`Market Volume<stocks.market_volume>` - ``get_market_volume``
- :ref:`News<stocks.news>`
- :ref:`OHLC<stocks.ohlc>`
- :ref:`Open/Close<stocks.open_close>`
- :ref:`End of Day Options<stocks.eod_options>` - ``get_eod_options``
- :ref:`Peers<stocks.peers>`
- :ref:`Previous Day Prices<stocks.previous_day_prices>`
- :ref:`Price<stocks.price>`
- :ref:`Price Target<stocks.price_target>`
- :ref:`Quote<stocks.quote>`
- :ref:`Relevant Stocks<stocks.relevant_stocks>`
- :ref:`Sector Performance<stocks.sector>` - ``get_sector_performance``
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


.. _stocks.cash_flow:

Cash Flow
---------

.. automethod:: iexfinance.stocks.base.Stock.get_cash_flow


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

.. NOTE: These were converted to code-block as they are currently returning
         errors

**Tag**

.. code-block:: python

    from iexfinance.stocks import get_collections

    get_collections("Computer Hardware", output_format='pandas').head()

**Sector**

.. code-block:: python

    get_collections("Industrials", output_format='pandas').head()



.. _stocks.company:

Company
-------

.. automethod:: iexfinance.stocks.base.Stock.get_company

.. _stocks.crypto:

Cryptocurrencies
----------------

To retrieve quotes for all available cryptocurrencies, create a ``Stock`` object
using a cryptocurrency ticker.

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


.. _stocks.crypto.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.stocks import Stock

    btc = Stock("BTCUSDT")
    btc.get_quote()




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

    from iexfinance.stocks import get_earnings_today

    get_earnings_today()["bto"]


.. _stocks.eod_options:

End of Day Options
------------------

End of day options prices are available through the top-level function ``get_eod_options``.

.. autofunction:: iexfinance.stocks.get_eod_options

.. _stocks.estimates:

Estimates
---------

.. automethod:: iexfinance.stocks.base.Stock.get_estimates

.. _stocks.financials:

Financials
----------
.. automethod:: iexfinance.stocks.base.Stock.get_financials

.. _stocks.fund_ownership:

Fund Ownership
--------------

.. automethod:: iexfinance.stocks.base.Stock.get_fund_ownership


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

    get_ipo_calendar()




.. _stocks.key_stats:

Key Stats
---------

.. automethod:: iexfinance.stocks.base.Stock.get_key_stats


.. _stocks.advanced_stats:

Advanced Stats
---------

.. automethod:: iexfinance.stocks.base.Stock.get_advanced_stats


.. _stocks.largest_trades:

Largest Trades
--------------
.. automethod:: iexfinance.stocks.base.Stock.get_largest_trades


.. _stocks.list:

List
----
.. seealso:: :ref:`Market Movers<stocks.movers>`


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

.. code-block:: python

    from iexfinance.stocks import get_market_volume

    get_market_volume()

.. _stocks.news:

News
----
.. automethod:: iexfinance.stocks.base.Stock.get_news


.. _stocks.peers:

Peers
-----
.. automethod:: iexfinance.stocks.base.Stock.get_peers




.. _stocks.price_target:

Price Target
------------

.. automethod:: iexfinance.stocks.base.Stock.get_price_target



.. _stocks.relevant_stocks:


Relevant Stocks
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_relevant_stocks

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

    get_market_gainers()
