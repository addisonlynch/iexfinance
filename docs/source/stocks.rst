.. _stocks:


.. currentmodule:: iexfinance.stocks

Stocks
======

Overview
--------

Access to the `Stocks <https://iextrading.com/developer/#stocks>`__
endpoints of the `IEX Developer API <https://iextrading.com/developer/>`__ is
available through the top-level ``Stock`` function.

Calling this function with a symbol (*str*) or list of symbols (*list*)
will return a ``Stock`` instance, which allows retrieval of
endpoints  (`Earnings
<https://iextrading.com/developer/#earnings>`__,
`Quote <https://iextrading.com/developer/#quote>`__, etc) for up to 100 symbols
at once. There are three ways
to access such endpoints:

1. **Endpoint Methods** - Allow retrieval of
individual
endpoints. Most endpoints allow Pandas DataFrame formatting. Examples are
``get_book``, ``get_quote``, etc. Where applicable, parameters (i.e.
``displayPercent`` for the Quote endpoint) may be passed
to these methods as keyword arguments.

2. **Field Methods** - supported by certain endpoints. Allow quick and
lightweight access to select fields of the Quote and Key Stats endpoints.
Examples are ``get_company_name``, ``get_beta``, etc. See below for more examples.

3. ``get_endpoints`` - returns one or more (up to 10) endpoints to be returned
in the *exact* format of the examples in the IEX docs. This method accepts no
additional parameters (it uses the defaults) and does not allow Pandas DataFrame as an output format.

.. ipython:: python

    from iexfinance.stocks import Stock
    aapl = Stock("aapl")
    aapl.get_price()




.. _stocks.balance_sheet:

Balance Sheet
-------------

.. automethod:: base.Stock.get_balance_sheet

.. _stocks.book:

Book
-------------
.. automethod:: base.Stock.get_book


.. _stocks.cash_flow:

Cash Flow
-------------

.. automethod:: base.Stock.get_cash_flow

.. _stocks.chart:

Chart
-------------
.. automethod:: base.Stock.get_chart


.. _stocks.collections:

Collections
-----------

The `Collections <https://iextrading.com/developer/docs/#collections>`__
endpoint of Stocks allows retrieval of certain groups of companies, organized
by:

- sector
- tag
- list (see the :ref:`list endpoint <stocks.list>`)

Use the top-level ``get_collections`` to access.

**Tag**

.. ipython:: python

    from iexfinance.stocks import get_collections

    get_collections("Computer Hardware", output_format='pandas').head()

**Sector**

.. ipython:: python

    get_collections("Industrials", output_format='pandas').head()



.. _stocks.company:

Company
-------------

.. automethod:: base.Stock.get_company

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

To retrieve quotes for all available cryptocurrencies, use the top-level
``get_crypto_quotes`` function:

.. ipython:: python

    from iexfinance.stocks import get_crypto_quotes

    get_crypto_quotes(output_format='pandas').head()



.. _stocks.delayed_quote:

Delayed Quote
-------------

.. automethod:: base.Stock.get_delayed_quote



.. _stocks.dividends:

Dividends
-------------

.. automethod:: base.Stock.get_dividends



.. _stocks.earnings:

Earnings
-------------

.. automethod:: base.Stock.get_earnings

.. _stocks.earnings_today:

.. note:: Earnings Today supports JSON output formatting only.

Earnings Today
--------------

Earnings Today was added to the Stocks endpoints in 2018. Access is provided
through the top-level ``get_todays_earnings`` function.

.. ipython:: python

    from iexfinance.stocks import get_todays_earnings

    get_todays_earnings()["bto"]




.. _stocks.effective_spread:

Effective Spread
-------------

.. automethod:: base.Stock.get_effective_spread


.. _stocks.estimates:

Estimates
-------------

.. automethod:: base.Stock.get_estimates

.. _stocks.financials:

Financials
-------------
.. automethod:: base.Stock.get_financials


.. _stocks.historical

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
^^^^^

To obtain daily historical data, use ``get_historical_data``.

.. autofunction:: get_historical_data


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
^^^^^^^^

To obtain one-minute intraday data for a given date, use
``get_historical_intraday``. **Note: this endpoint has a maximum of one symbol
and a single date.**

.. autofunction:: get_historical_intraday

.. ipython:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday

    date = datetime(2018, 11, 27)

    data = get_historical_intraday("AAPL", date, output_format='pandas')
    data.head()



.. _stocks.income_statement:

Income Statement
----------------

.. automethod:: base.Stock.get_income_statement

.. _stocks.ipo_calendar:

IPO Calendar
------------

IPO Calendar was added to the Stocks endpoints in 2018. Access is provided
through the top-level ``get_ipo_calendar`` function.

There are two possible values for the ``period`` parameter, of which
``upcoming-ipos`` is the default. ``today-ipos`` is also available.

.. ipython:: python

    from iexfinance.stocks import get_ipo_calendar

    get_ipo_calendar()["rawData"][0]




.. _stocks.key_stats:

Key Stats
-------------

.. automethod:: base.Stock.get_key_stats


.. _stocks.list:

List
-------------
.. seealso:: :ref:`Market Movers<stocks.movers>`


.. _stocks.largest_trades:

Largest Trades
-------------
.. automethod:: base.Stock.get_largest_trades


.. _stocks.logo:

Logo
-------------

.. automethod:: base.Stock.get_logo

.. _stocks.market_volume:

Market Volume (U.S)
-------------------

Market Volume returns real-time traded volume on U.S. Markets. Access is
provided through the top-level ``get_market_volume`` function.

.. ipython:: python

    from iexfinance.stocks import get_market_volume

    get_market_volume()

.. _stocks.news:

News
-------------
.. automethod:: base.Stock.get_news


.. _stocks.ohlc:

OHLC
-------------
.. automethod:: base.Stock.get_ohlc


.. _stocks.open_close:

Open/Close Price
----------------
.. seealso:: Time Series is an alias for the :ref:`OHLC <stocks.ohlc>` endpoint


.. automethod:: base.Stock.get_open_close


.. _stocks.peers:

Peers
-------------
.. automethod:: base.Stock.get_peers


.. _stocks.previous_day_prices:

Previous Day Prices
-------------

.. automethod:: base.Stock.get_previous


.. _stocks.price:

Price
-------------

.. automethod:: base.Stock.get_price


.. _stocks.price_target:

Price Target
-------------

.. automethod:: base.Stock.get_price_target

.. _stocks.quote:

Quote
-------------
.. automethod:: base.Stock.get_quote


.. _stocks.relevant_stocks:


Relevant Stocks
-------------

.. automethod:: base.Stock.get_relevant

.. _stocks.sector:

Sector Performance
------------------

Sector Performance was added to the Stocks endpoints in 2018. Access to this endpoint is provided through the ``get_sector_performance`` function.

.. ipython:: python

    from iexfinance.stocks import get_sector_performance

    get_sector_performance(output_format='pandas')



.. _stocks.splits:

Splits
-------------

.. automethod:: base.Stock.get_splits


.. _stocks.time_series:

Time Series
-------------
.. seealso:: Time Series is an alias for the :ref:`Chart<stocks.chart>` endpoint

.. automethod:: base.Stock.get_time_series


.. _stocks.volume_by_venue:

Volume by Venue
-------------

.. automethod:: base.Stock.get_volume_by_venue


.. _stocks.field_methods:

Field Methods
-------------

In addition, various **Field Methods** are provided for certain endpoints.
These methods will allow retrieval of a single datapoint, such as ``get_open``,
``get_company_name``, etc. Field methods are displayed below the endpoint
methods for which they are available (namely :ref:`Quote<stocks.quote>`
and :ref:`Key Stats<stocks.key-stats>`).


.. _stocks.key_stats_field_methods:

Key Stats
-------------

.. automethod:: base.Stock.get_beta
.. automethod:: base.Stock.get_short_interest
.. automethod:: base.Stock.get_short_ratio
.. automethod:: base.Stock.get_latest_eps
.. automethod:: base.Stock.get_shares_outstanding
.. automethod:: base.Stock.get_float
.. automethod:: base.Stock.get_eps_consensus


.. _stocks.quote_field_methods:

Quote
-------------

.. automethod:: base.Stock.get_company_name
.. automethod:: base.Stock.get_sector
.. automethod:: base.Stock.get_open
.. automethod:: base.Stock.get_close
.. automethod:: base.Stock.get_years_high
.. automethod:: base.Stock.get_years_low
.. automethod:: base.Stock.get_ytd_change
.. automethod:: base.Stock.get_volume
.. automethod:: base.Stock.get_market_cap


.. _stocks.examples:


Examples
--------

.. _stocks.examples_endpoint_methods:

Endpoint Methods
~~~~~~~~~~~~~~~~

A single symbol request will return data *exactly* as it appears in the IEX docs examples:

.. ipython:: python

    from iexfinance.stocks import Stock
    aapl = Stock("AAPL")
    aapl.get_price()

While multi-symbol requests will return a symbol-indexed list of the endpoint's data

.. ipython::python

    batch = Stock(["AAPL", "TSLA"])
    batch.get_price()

Most endpoints can be formatted as a `pandas.DataFrame`. Multi-symbol requests will concatenate the dataframes for each:

.. ipython:: python

    air_transport = Stock(['AAL', 'DAL', 'LUV'], output_format='pandas')
    air_transport.get_quote().head()


.. _stocks.filtering:

Filtering
~~~~~~~~~

Per the IEX Docs, the
`filter <https://iextrading.com/developer/docs/#filter-results>`__,
paramter may be passed to any endpoint request to restrict single endpoint
queries to certain fields. iexfinance uses ``filter_``, as ``filter`` is a
reserved word in Python:

.. ipython:: python

    aapl = Stock("AAPL", output_format='pandas')
    aapl.get_quote(filter_='ytdChange')

Lists of fields are acceptable as well:

.. ipython:: python

    aapl.get_quote(filter_=['ytdChange', 'open', 'close'])

.. note:: The desired fields must **exactly** match the field key names as
        listed in the IEX docs.

.. _stocks.passing_parameters:

Passing Parameters
~~~~~~~~~~~~~~~~~~

**Endpoint-specific**

We show an example using the `last` parameter for the News endpoint:

.. ipython:: python

    aapl = Stock("AAPL")

    len(aapl.get_news())

by default, News returns the last 10 items (`last is 10 by default`), but we can specify a custom value:

.. ipython:: python

    aapl = Stock("AAPL")

    len(aapl.get_news(last=35))

With a custom value specified, News now returns the previous 35 items.

.. _stocks.output_formatting:

Output Formatting
~~~~~~~~~~~~~~~~~

Most endpoints allow for pandas DataFrame-formatted output:

.. ipython:: python

    aapl = Stock("AAPL", output_format='pandas')

    aapl.get_quote().head()

We can also change the output format once our ``Stock`` object has been
instantiated:

.. ipython:: python

    aapl.output_format == 'json'
    aapl.get_ohlc()



.. _stocks.examples_field-methods:

Field Methods
~~~~~~~~~~~~~

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

Format as a DataFrame

.. ipython:: python

    b = Stock(["AAPL", "TSLA"], output_format=('pandas'))
    b.get_beta()

.. _stocks.movers:

Market Movers
-------------

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


