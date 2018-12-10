.. _market:

.. currentmodule:: iexfinance


IEX Market Data
===============

The following functions retrieve data from the `IEX Market Data <https://iextrading.com/developer/docs/#iex-market-data>`__ endpoints.

    - :ref:`TOPS<market.TOPS>`
    - :ref:`Last<market.Last>`
    - :ref:`DEEP<market.DEEP>`
    - :ref:`Book<market.Book>`

.. warning:: IEX Market Data endpoints may return empty or raise an exception outside of market hours.

.. _market.TOPS:


TOPS
----

`TOPS <https://iextrading.com/developer/docs/#tops>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the top-level function ``get_market_tops()``:


.. autofunction:: get_market_tops

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_market_tops

    get_market_tops('AAPL')

.. note:: The /tops endpoint without any parameters will return all symbols. TOPS data with all symbols is 1.78mb uncompressed (270kb compressed) and is throttled at one request per second, per `IEX docs <https://iextrading.com/developer/docs/#tops>`__


.. _market.Last:


Last
----

`Last <https://iextrading.com/developer/docs/#last>`__ is IEX
real-time trade data from the IEX book. This endpoint allows retrieval
of a real-time quote.

Access is available through the top-level function ``get_market_last()``:

.. autofunction:: get_market_last

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_market_last

    df = get_market_last(symbols="AAPL", output_format='pandas')
    df['price']

.. note:: The /tops/last endpoint without any parameters will return all symbols.

.. _market.DEEP:


DEEP
----

`DEEP <https://iextrading.com/developer/docs/#DEEP>`__  is IEX's aggregated real-time depth of book quotes. DEEP also provides last trade price and size information.

Access is available through the top-level function ``get_market_deep()``:

.. autofunction:: get_market_deep

.. note:: Per IEX, DEEP only accepts one symbol at this time.

Usage
~~~~~

.. ipython:: python
    :okexcept:

    from iexfinance import get_market_deep

    get_market_deep("AAPL")[:2]


.. _market.Book:


Book
----

`Book <https://iextrading.com/developer/docs/#Book>`__ shows IEX's bids and asks
for given symbols.

Access is available through the top-level function ``get_market_book()``:

.. autofunction:: get_market_book


Usage
~~~~~

.. ipython:: python

    from iexfinance import get_market_book

    get_market_book("AAPL")


.. todo:: Integrate WebSocket support for all IEX Market Data services.
