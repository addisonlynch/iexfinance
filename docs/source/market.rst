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

Access is available through the top-level function ``get_tops()``:

.. code:: python

    get_tops(symbolList=None, outputFormat='json', retry_count=3,
             pause=0.001, session=None)

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_TOPS

    get_TOPS('AAPL')

Parameters
^^^^^^^^^^

+--------------------+-----------------------------------------+-------------+
| Option             | Description                             | Optional?   |
+====================+=========================================+=============+
| ``symbolList``     | A symbol or list of symbols             | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``outputFormat``   | Output format (json or pandas)          | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``retry_count``    | Retry count if request fails            | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``pause``          | Pause duration between retry attempts   | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``session``        | A requests-cache session                | Yes         |
+--------------------+-----------------------------------------+-------------+

.. _market.Last:


Last
====

`Last <https://iextrading.com/developer/docs/#last>`__ retrieves
real-time trade data from the IEX book. This endpoint allows retrieval
of a real-time quote.

.. code:: python

    get_Last(symbol, outputFormat='json', retry_count=3, pause=0.001,
             session=None)

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_Last
    import pandas as pd

    df = get_Last(symbolList="AAPL", outputFormat='pandas')


Parameters
^^^^^^^^^^

+--------------------+-----------------------------------------+-------------+
| Option             | Description                             | Optional?   |
+====================+=========================================+=============+
| ``symbolList``     | A symbol or list of symbols             | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``outputFormat``   | Output format (json or pandas)          | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``retry_count``    | Retry count if request fails            | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``pause``          | Pause duration between retry attempts   | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``session``        | A requests-cache session                | Yes         |
+--------------------+-----------------------------------------+-------------+

.. _market.DEEP:


DEEP
====

.. code:: python

    get_DEEP(symbol, outputFormat='json', session=None)

DEEP is IEX's aggregated real-time depth of book quotes. DEEP also
provides last trade price and size information

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_TOPS
    import pandas as pd


Parameters
^^^^^^^^^^

+--------------------+-----------------------------------------+-------------+
| Option             | Description                             | Optional?   |
+====================+=========================================+=============+
| ``symbolList``     | A symbol or list of symbols             | No          |
+--------------------+-----------------------------------------+-------------+
| ``outputFormat``   | Output format (**json only**)           | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``retry_count``    | Retry count if request fails            | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``pause``          | Pause duration between retry attempts   | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``session``        | A requests-cache session                | Yes         |
+--------------------+-----------------------------------------+-------------+

.. _market.Book:


Book
====

.. code:: python

    get_Book(symbol, outputFormat='json', session=None)

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_TOPS
    import pandas as pd

Parameters
^^^^^^^^^^

+--------------------+-----------------------------------------+-------------+
| Option             | Description                             | Optional?   |
+====================+=========================================+=============+
| ``symbolList``     | A symbol or list of symbols             | No          |
+--------------------+-----------------------------------------+-------------+
| ``outputFormat``   | Output format (json or pandas)          | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``retry_count``    | Retry count if request fails            | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``pause``          | Pause duration between retry attempts   | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``session``        | A requests-cache session                | Yes         |
+--------------------+-----------------------------------------+-------------+
