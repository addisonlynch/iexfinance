.. _stock-prices:


.. currentmodule:: iexfinance

Stock Prices
============

Hello

.. toctree::
    :caption: Contents



.. _stocks.book:

Book
----
.. automethod:: iexfinance.stocks.base.Stock.get_book


.. _stocks.chart:

Chart
-----
.. automethod:: iexfinance.stocks.base.Stock.get_chart


.. _stocks.delayed_quote:

Delayed Quote
-------------

.. automethod:: iexfinance.stocks.base.Stock.get_delayed_quote


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


.. _stocks.open_close:

Open/Close Price
----------------
.. seealso:: Time Series is an alias for the :ref:`OHLC <stocks.ohlc>` endpoint


.. automethod:: iexfinance.stocks.base.Stock.get_open_close



.. _stocks.ohlc:

OHLC
----
.. automethod:: iexfinance.stocks.base.Stock.get_ohlc



.. _stocks.previous_day_prices:

Previous Day Prices
-------------------

.. warning:: ``get_previous`` has been deprecated and renamed
            ``get_previous_day_prices``.

.. automethod:: iexfinance.stocks.base.Stock.get_previous_day_prices


.. _stocks.price_only:

Price Only
----------

.. automethod:: iexfinance.stocks.base.Stock.get_price

.. _stocks.quote:

Quote
-----
.. automethod:: iexfinance.stocks.base.Stock.get_quote


.. _stocks.volume_by_venue:

Volume by Venue
---------------

.. automethod:: iexfinance.stocks.base.Stock.get_volume_by_venue
