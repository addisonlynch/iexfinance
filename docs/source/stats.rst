.. _stats:

.. currentmodule:: iexfinance

*********
IEX Stats
*********

The following functions retrieve data from the IEX Stats endpoints

	- :ref:`Intraday<stats.intraday>`
	- :ref:`Recent<stats.recent>`
	- :ref:`Records<stats.records>`
	- :ref:`Historical Summary<stats.monthly>`
	- :ref:`Historical Daily<stats.daily>`




.. stats.intraday:


Intraday
====

`Intraday <https://iextrading.com/developer/docs/#intraday>`__ is IEX's
aggregated best quoted bid and offer position in near real time.

Access is available through the top-level function ``get_stats_intraday()``:

.. autofunction:: get_stats_intraday

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_stats_intraday

    get_stats_intraday()

.. stats.recent:


Recent
====

`Recent <https://iextrading.com/developer/docs/#recent>`__ is IEX's
trading statstics from the previous five trading days.

Access is available through the top-level function ``get_stats_recent()``:

.. autofunction:: get_stats_recent

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_stats_recent

    get_stats_recent()[0]


.. stats.records:

Records
====

`Records <https://iextrading.com/developer/docs/#records>`__ is IEX's
trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_records()``:

.. autofunction:: get_stats_records

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_stats_records

    get_stats_records()


.. stats.monthly:

Historical Summary
==================

`Historical Summary <https://iextrading.com/developer/docs/#historical-summary>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_monthly()``:

.. autofunction:: get_stats_monthly

.. warning:: The Historical Summary accepts requests of one month per request.
			if specifying a long date range, a query will be made for each
			month in the range, significantly impacting


Usage
^^^^^

.. ipython:: python

    from iexfinance import get_stats_monthly

    get_stats_monthly()

Parameters
^^^^^^^^^^

+--------------------+-----------------------------------------+-------------+
| Option             | Description                             | Optional?   |
+====================+=========================================+=============+
| ``start``          | Start of desired retrieval period       | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``end``	         | End of desired retrieval period         | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``output_format``   | Output format (json or pandas)          | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``retry_count``    | Retry count if request fails            | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``pause``          | Pause duration between retry attempts   | Yes         |
+--------------------+-----------------------------------------+-------------+
| ``session``        | A requests-cache session                | Yes         |
+--------------------+-----------------------------------------+-------------+




.. stats.daily:


Historical Daily
================

`Historical Daily <https://iextrading.com/developer/docs/#historical-daily>`__
is IEX's trading statstics from the previous trading sessions.

Access is available through the top-level function ``get_stats_daily()``:

.. autofunction:: get_stats_daily

Usage
^^^^^

.. ipython:: python

    from iexfinance import get_stats_daily

    get_stats_daily()

