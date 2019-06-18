.. _data_apis:

Data APIs
=========

IEX Cloud data can be organized into three generic data APIs:
:ref:`time-series<time_series>`, data-tables, and data-points. Each API type is
self describing and the docs can be accessed without an API token.


.. _data_apis.time_series:

Time Series
-----------

`Time series`_ is the most common type of data available, and consists of a
collection of data points over a period of time. Time series data is indexed by a single date field, and can be retrieved by any portion of time.

Full access to the Time Series endpoints is available through the
``get_time_series`` function.

.. autofunction:: iexfinance.data_apis.get_time_series

.. _data_apis.time_series.all_time_series:

All Available Time Series
~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain a list of all available time series, simply call ``get_time_series``
with no parameters:

.. ipython:: python

    from iexfinance.data_apis import get_time_series

    get_time_series()

.. _data_apis.time_series.individual:

Individual Time Series
~~~~~~~~~~~~~~~~~~~~~~

Whereas calling ``get_time_series`` with no parameters returns a full inventory
of time series endpoints, calling ``get_time_series`` with an individual series
ID and (optional) keys and subkeys as parameters.

For example, to obtain the ``REPORTED_FINANCIALS`` time series entry for Apple
Inc. (``AAPL``):

.. ipython:: python

    get_time_series("REPORTED_FINANCIALS", "AAPL").head()

Or with a subkey:

.. ipython:: python

    get_time_series("REPORTED_FINANCIALS", "AAPL", "10-Q").head()

Any and all series-specific parameters (such as ``last``, ``to``, ``from``,
etc. should be passed as *keyword arguments*)

Examples
^^^^^^^^

Last Apple Inc. Form 10-K

.. ipython:: python

    get_time_series("REPORTED_FINANCIALS", "AAPL", "10-K", last=1).head()

