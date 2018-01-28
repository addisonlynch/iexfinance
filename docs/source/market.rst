.. _market:

.. currentmodule:: iexfinance


***************
IEX Market Data
***************

The following functions retrieve data from the IEX Market Data endpoints

    - :ref:`TOPS<market.TOPS>`
    - :ref:`Last<market.Last>`
    - :ref:`DEEP<market.DEEP>`
    - :ref:`Book<market.Book>`

.. _market.TOPS:


TOPS
====

`TOPS <https://iextrading.com/developer/docs/#tops>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the top-level function ``get_TOPS()``:

.. autofunction:: get_TOPS

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_TOPS

    get_TOPS('AAPL')


.. _market.Last:


Last
====

`Last <https://iextrading.com/developer/docs/#last>`__ is IEX
real-time trade data from the IEX book. This endpoint allows retrieval
of a real-time quote.

Access is available through the top-level function ``get_Last()``:

.. autofunction:: get_Last

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_Last
    import pandas as pd

    df = get_Last(symbolList="AAPL", outputFormat='pandas')
    df['price']



.. _market.DEEP:


DEEP
====

`DEEP <https://iextrading.com/developer/docs/#DEEP>`__  is IEX's aggregated real-time depth of book quotes. DEEP also provides last trade price and size information.

Access is available through the top-level function ``get_DEEP()``:

.. autofunction:: get_DEEP

.. note:: DEEP may return an error outside of market hours.

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_DEEP

    get_DEEP("AAPL")


.. _market.Book:


Book
====

`Book <https://iextrading.com/developer/docs/#Book>`__ shows IEX's bids and asks
for given symbols.

Access is available through the top-level function ``get_Book()``:

.. autofunction:: get_Book

.. note:: Book may return an error outside of market hours.

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_Book

    get_Book("AAPL")

