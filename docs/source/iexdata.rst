.. _iexdata:


Investor's Exchange Data
========================

.. note:: These endpoints do not support pandas DataFrame output formatting.


The following endpoints are available under Investor's Exchange Data:

.. contents:: Endpoints
    :depth: 2



.. _iexdata.TOPS:


TOPS
----

`TOPS <https://iexcloud.io/docs/api/#tops>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the function ``get_tops()``:


.. autofunction:: iexfinance.iexdata.get_tops

Usage
~~~~~

.. code-block:: python

    from iexfinance.iexdata import get_tops

    get_tops('AAPL')

.. note:: The /tops endpoint without any parameters will return all symbols. TOPS data with all symbols is 1.78mb uncompressed (270kb compressed) and is throttled at one request per second, per `IEX docs <https://iexcloud.io/docs/api/#tops>`__


.. _iexdata.Last:


Last
----

`Last <https://iexcloud.io/docs/api/#last>`__ is IEX
real-time trade data from the IEX book. This endpoint allows retrieval
of a real-time quote.

Access is available through the function ``get_last()``:

.. autofunction:: iexfinance.iexdata.get_last

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

`DEEP <https://iexcloud.io/docs/api/#deep>`__  is IEX's aggregated real-time depth of book quotes. DEEP also provides last trade price and size information.

Access is available through the function ``get_deep()``:

.. autofunction:: iexfinance.iexdata.get_deep

.. note:: Per IEX, DEEP only accepts one symbol at this time.


.. _iexdata.DEEP.usage:


Usage
~~~~~

.. code-block:: python

    from iexfinance.iexdata import get_deep

    get_deep("AAPL")[:2]


.. _iexdata.DEEP_auction:

DEEP Auction
------------

.. todo:: Coming soon.


.. _iexdata.DEEP_book:

DEEP Book
---------

.. todo:: Coming soon.


.. _iexdata.DEEP_halt_status:

DEEP Operational Halt Status
----------------------------

.. todo:: Coming soon.


.. _iexdata.DEEP_official_price:

DEEP Official Price
-------------------

.. todo:: Coming soon.


.. _iexdata.DEEP_security_event:

DEEP Security Event
-------------------

.. todo:: Coming soon.

.. _iexdata.DEEP_short_sale_status:

DEEP Short Sale Price Test Status
---------------------------------

.. todo:: Coming soon.

.. _iexdata.DEEP_system_event:

DEEP System Event
-----------------

.. todo:: Coming soon.

.. _iexdata.DEEP_trades:

DEEP Trades
-----------

.. todo:: Coming soon.

.. _iexdata.DEEP_trade_break:

DEEP Trade Break
----------------

.. todo:: Coming soon.

.. _iexdata.DEEP_trading_status:

DEEP Trading Status
-------------------

.. todo:: Coming soon.


.. _iexdata.regulation_list:

Listed Regulation SHO Threshold Securities List
-----------------------------------------------

.. todo:: Coming soon.


.. _iexdata.short_interest_list:

Listed Short Interest List
--------------------------

.. todo:: Coming soon.


.. _iexdata.stats_daily:


Stats Historical Daily
----------------------

.. warning:: This endpoint has been marked as *in-dev* by the provider.

`Historical Daily <https://iexcloud.io/docs/api/#historical-daily>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the function ``get_stats_daily()``:

.. autofunction:: iexfinance.iexdata.get_stats_daily

Data retrieval period must be between 1/2014 and today.

.. _iexdata.stats_daily.usage:

Usage
~~~~~

.. ipython:: python
    :okwarning:
    :okexcept:

    from iexfinance.iexdata import get_stats_daily

    get_stats_daily(last=3)


.. _iexdata.stats_monthly:

Stats Historical Summary
------------------------

`Historical Summary <https://iexcloud.io/docs/api/#stats-historical-summary>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the function ``get_stats_summary()``:

.. autofunction:: iexfinance.iexdata.get_stats_summary

Data retrieval period must be between 1/2014 and today.

.. warning:: The Historical Summary accepts requests of one month per request.
            if specifying a long date range, a query will be made for each
            month in the range, significantly impacting performance

.. _iexdata.stats_monthly.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance.iexdata import get_stats_summary
    from datetime import datetime

    get_stats_summary(start=datetime(2019, 1, 1), end=datetime(2020, 1, 1))



.. _iexdata.stats_intraday:

Stats Intraday
--------------

`Intraday <https://iexcloud.io/docs/api/#stats-intraday>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the function ``get_stats_intraday()``:

.. autofunction:: iexfinance.iexdata.get_stats_intraday

.. _iexdata.stats_intraday.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance.iexdata import get_stats_intraday

    get_stats_intraday()

.. _iexdata.stats_recent:


Stats Recent
------------

`Recent <https://iexcloud.io/docs/api/#stats-recent>`__ is IEX's
trading statstics from the previous five trading days.

Access is available through the function ``get_stats_recent()``:

.. autofunction:: iexfinance.iexdata.get_stats_recent

.. _iexdata.stats_recent.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance.iexdata import get_stats_recent

    get_stats_recent()


.. _iexdata.stats_records:

Stats Records
-------------

`Records <https://iexcloud.io/docs/api/#stats-records>`__ is IEX's
trading statstics from the previous trading sessions.

Access is available through the function ``get_stats_records()``:

.. autofunction:: iexfinance.iexdata.get_stats_records

.. _iexdata.stats_records.usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance.iexdata import get_stats_records

    get_stats_records()



