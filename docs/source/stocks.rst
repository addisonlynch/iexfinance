.. _stocks:


Stocks
======

Overview
--------

Access to the `Stocks <https://iextrading.com/developer/#stocks>`__
endpoints of the `IEX Developer API <https://iextrading.com/developer/>`__ is
available through the top-level ``Stock`` function.

Calling this function with a symbol (*str*) or list of symbols (*list*)
will return a ``StockReader`` instance, which allows retrieval of
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



Formatting
----------


Supported Formats
~~~~~~~~~~~~~~~~~

1. **JSON** (**All Endpoints**) - For a single symbol, endpoint methods will
return
the endpoint as specified in docs (i.e. *dict* for Quote, *float* for Price)
while multiple symbols will be returned as a symbol-indexed dictionary of the
requested endpoint for each symbol.

2. **Pandas DataFrame** (*most endpoints*) - The DataFrame is often indexed by
the endpoint's dictionary keys, with a column for each requested symbol. For
field methods, the DataFrame is a single column, indexed by each requested
symbol.

Selecting an Output Format
~~~~~~~~~~~~~~~~~~~~~~~~~~

Output formatting is most often selected through the initial call to the
``Stock``
function (which becomes an attribute of the ``StockReader`` instance) by
passing
``output_format`` as a keyword argument:

.. ipython:: python

    from iexfinance.stocks import Stock
    aapl = Stock("aapl", output_format='pandas')
    aapl.get_quote().head()

It is also possible to change the output format of an already-instantiated
``StockReader``:

.. ipython:: python

    aapl.output_format = 'json'
    aapl.get_quote()["close"]

Further, it is possible to customize the integer and floating point JSON parsing (into a type such as ``Decimal.decimal``) by passing the desired types via ``json_parse_float`` and ``json_parse_int`` parameters.

.. ipython:: python

    from decimal import Decimal

    aaplD = Stock("AAPL", json_parse_float=Decimal)


Parameters
----------

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument to the endpoint method. (see :ref:`example
<stocks.passing-parameters>`).

.. ipython:: python

    aapl = Stock("AAPL", output_format='pandas')
    aapl.get_quote(displayPercent=True).loc["ytdChange"]


.. note:: A key IEX optional parameter is ``filter_``, which allows the
         filtering of endpoint requests to return certain fields only. See the
         `IEX docs <https://iextrading.com/developer/docs/#filter-results>`__
         and the examples below for more information.

.. _stocks.endpoints:

Endpoint Methods
----------------

**Endpoint methods** will return a symbol-indexed dictionary of the endpoint
requested. See examples :ref:`below <stocks.examples-endpoint-methods>` for
clarification. The optional Keyword Arguments (in accordance with the IEX docs)
are specified for each method below:

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


.. _stocks.balance-sheet:

Balance Sheet
~~~~~~~~~~~~~

.. warning:: This endpoint is available with IEX Cloud only.

.. automethod:: iexfinance.stocks.base.StockReader.get_balance_sheet

.. _stocks.book:

Book
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_book

.. _stocks.cash-flow:

Cash Flow
~~~~~~~~~

.. warning:: This endpoint is available with IEX Cloud only.

.. automethod:: iexfinance.stocks.base.StockReader.get_cash_flow

.. _stocks.chart:

Chart
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_chart


.. _stocks.company:

Company
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_company


.. _stocks.delayed-quote:

Delayed Quote
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_delayed_quote



.. _stocks.dividends:

Dividends
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_dividends



.. _stocks.earnings:

Earnings
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_earnings



.. _stocks.effective-spread:

Effective Spread
~~~~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_effective_spread


.. _stocks.financials:

Financials
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_financials

.. _stocks.income-statement:

Income Statement
~~~~~~~~~~~~~~~~

.. warning:: This endpoint is available with IEX Cloud only.

.. automethod:: iexfinance.stocks.base.StockReader.get_income_statement

.. _stocks.key-stats:

Key Stats
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_key_stats


.. _stocks.list:

List
~~~~~~~~~~~~~
.. seealso:: :ref:`Market Movers<stocks.movers>`


.. _stocks.largest-trades:

Largest Trades
~~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_largest_trades


.. _stocks.logo:

Logo
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_logo


.. _stocks.news:

News
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_news


.. _stocks.ohlc:

OHLC
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_ohlc


.. _stocks.open-close:

Open/Close
~~~~~~~~~~~~~
.. seealso:: Time Series is an alias for the :ref:`OHLC <stocks.ohlc>` endpoint


.. automethod:: iexfinance.stocks.base.StockReader.get_open_close


.. _stocks.peers:

Peers
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_peers




.. _stocks.previous:

Previous
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_previous


.. _stocks.price:

Price
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_price


.. _stocks.quote:

Quote
~~~~~~~~~~~~~
.. automethod:: iexfinance.stocks.base.StockReader.get_quote


.. _stocks.relevant:


Relevant
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_relevant




.. _stocks.splits:

Splits
~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_splits


.. _stocks.time-series:

Time Series
~~~~~~~~~~~~~
.. seealso:: Time Series is an alias for the :ref:`Chart<stocks.chart>` endpoint

.. automethod:: iexfinance.stocks.base.StockReader.get_time_series


.. _stocks.volume-by-venue:

Volume by Venue
~~~~~~~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_volume_by_venue


.. _stocks.field-methods:

Field Methods
-------------

In addition, various **Field Methods** are provided for certain endpoints.
These methods will allow retrieval of a single datapoint, such as ``get_open``,
``get_company_name``, etc. Field methods are displayed below the endpoint
methods for which they are available (namely :ref:`Quote<stocks.quote>`
and :ref:`Key Stats<stocks.key-stats>`).


.. _stocks.key-stats-field-methods:

Key Stats
~~~~~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_beta
.. automethod:: iexfinance.stocks.base.StockReader.get_short_interest
.. automethod:: iexfinance.stocks.base.StockReader.get_short_ratio
.. automethod:: iexfinance.stocks.base.StockReader.get_latest_eps
.. automethod:: iexfinance.stocks.base.StockReader.get_shares_outstanding
.. automethod:: iexfinance.stocks.base.StockReader.get_float
.. automethod:: iexfinance.stocks.base.StockReader.get_eps_consensus


.. _stocks.quote-field-methods:

Quote
~~~~~

.. automethod:: iexfinance.stocks.base.StockReader.get_company_name
.. automethod:: iexfinance.stocks.base.StockReader.get_sector
.. automethod:: iexfinance.stocks.base.StockReader.get_open
.. automethod:: iexfinance.stocks.base.StockReader.get_close
.. automethod:: iexfinance.stocks.base.StockReader.get_years_high
.. automethod:: iexfinance.stocks.base.StockReader.get_years_low
.. automethod:: iexfinance.stocks.base.StockReader.get_ytd_change
.. automethod:: iexfinance.stocks.base.StockReader.get_volume
.. automethod:: iexfinance.stocks.base.StockReader.get_market_cap


.. _stocks.examples:


Examples
--------

.. _stocks.examples-endpoint-methods:

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

.. _stocks.passing-parameters:

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

.. _stocks.output-formatting:

Output Formatting
~~~~~~~~~~~~~~~~~

Most endpoints allow for pandas DataFrame-formatted output:

.. ipython:: python

    aapl = Stock("AAPL", output_format='pandas')

    aapl.get_quote().head()

We can also change the output format once our ``StockReader`` object has been
instantiated:

.. ipython:: python

    aapl.output_format == 'json'
    aapl.get_ohlc()



.. _stocks.examples-field-methods:

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

.. _stocks.sector:

Sector Performance
------------------

Sector Performance was added to the Stocks endpoints in 2018. Access to this endpoint is provided through the ``get_sector_performance`` function.

.. ipython:: python

    from iexfinance.stocks import get_sector_performance

    get_sector_performance(output_format='pandas')

.. _stocks.earnings_today:

.. note:: Earnings Today and IPO Calendar support JSON output formatting only.

Earnings Today
--------------

Earnings Today was added to the Stocks endpoints in 2018. Access is provided
through the top-level ``get_todays_earnings`` function.

.. ipython:: python

    from iexfinance.stocks import get_todays_earnings

    get_todays_earnings()["bto"]

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
