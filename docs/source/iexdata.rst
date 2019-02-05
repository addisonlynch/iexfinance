.. _iexdata:

.. currentmodule:: iexfinance.iexdata

Investor's Exchange Data
========================


The following endpoints are available under Investor's Exchange Data:

**Market Data**

- :ref:`TOPS`
- :ref:`Last`
- :ref:`DEEP`

**Market Statistics**

- :ref:`stats_monthly`
- :ref:`stats_intraday`
- :ref:`stats_recent`
- :ref:`stats_records`
- :ref:`stats_daily`


.. _iexdata.TOPS:


TOPS
----

`TOPS <https://iexcloud.io/docs/api/#tops>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the function ``get_tops()``:


.. autofunction:: get_tops

Usage
~~~~~

.. code-block:: python

    from iexfinance.iexdata import get_tops

    get_tops('AAPL')

.. note:: The /tops endpoint without any parameters will return all symbols. TOPS data with all symbols is 1.78mb uncompressed (270kb compressed) and is throttled at one request per second, per `IEX docs <https://iextrading.com/developer/docs/#tops>`__


.. _iexdata.Last:


Last
----

`Last <https://iexcloud.io/docs/api/#last>`__ is IEX
real-time trade data from the IEX book. This endpoint allows retrieval
of a real-time quote.

Access is available through the function ``get_last()``:

.. autofunction:: get_last

Usage
~~~~~

.. code-block:: python

    from iexfinance.iexdata import get_last

    df = get_last(symbols="AAPL", output_format='pandas')
    df['price']

.. note:: The /tops/last endpoint without any parameters will return all symbols.

.. _iexdata.DEEP:


DEEP
----

`DEEP <https://iexcloud.io/docs/api/#DEEP>`__  is IEX's aggregated real-time depth of book quotes. DEEP also provides last trade price and size information.

Access is available through the function ``get_deep()``:

.. autofunction:: get_deep

.. note:: Per IEX, DEEP only accepts one symbol at this time.

Usage
~~~~~

.. code-block:: python

    from iexfinance.iexdata import get_deep

    get_deep("AAPL")[:2]


.. _iexdata.stats_monthly:

Stats Historical Summary
------------------------

`Historical Summary <https://iextrading.com/developer/docs/#historical-summary>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_monthly()``:

.. autofunction:: get_stats_monthly

Data retrieval period must be between 1/2014 and today.

.. warning:: The Historical Summary accepts requests of one month per request.
            if specifying a long date range, a query will be made for each
            month in the range, significantly impacting performance

.. _iexdata.stats_monthly.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_stats_monthly
    from datetime import datetime

    get_stats_monthly(start=datetime(2017, 2, 9), end=datetime(2017, 5, 24))[0]



.. _iexdata.stats_intraday:

Stats Intraday
--------------

`Intraday <https://iextrading.com/developer/docs/#intraday>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the top-level function ``get_stats_intraday()``:

.. autofunction:: get_stats_intraday

.. _iexdata.stats_intraday.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_stats_intraday

    get_stats_intraday()

.. _iexdata.stats_recent:


Recent
------

`Recent <https://iextrading.com/developer/docs/#recent>`__ is IEX's
trading statstics from the previous five trading days.

Access is available through the top-level function ``get_stats_recent()``:

.. autofunction:: get_stats_recent

.. _iexdata.stats_recent.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_stats_recent

    get_stats_recent()[0]


.. _iexdata.stats_records:

Records
-------

`Records <https://iextrading.com/developer/docs/#records>`__ is IEX's
trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_records()``:

.. autofunction:: get_stats_records

.. _iexdata.stats_records.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance import get_stats_records

    get_stats_records()



.. _iexdata.stats_daily:


Historical Daily
----------------

`Historical Daily <https://iextrading.com/developer/docs/#historical-daily>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_daily()``:

.. autofunction:: get_stats_daily

Data retrieval period must be between 1/2014 and today.

.. _iexdata.stats_daily.usage:

Usage
~~~~~

.. ipython:: python
    :okwarning:
    :okexcept:

    from iexfinance import get_stats_daily

    get_stats_daily(last=3)


