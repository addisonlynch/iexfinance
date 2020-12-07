.. _data-apis:

Data APIs
=========

IEX Cloud data can be organized into three generic data APIs:
:ref:`time-series<data-apis.time-series>`, data-tables, and data-points. Each API type is self describing and the docs can be accessed without an API token.


.. _data-apis.data-points:

Data Points
-----------

`Data points`_ are available per symbol and return individual plain text
values. Retrieving individual data points is useful for Excel and Google Sheet users, and applications where a single, lightweight value is needed. We also provide update times for some endpoints which allow you to call an endpoint only once it has new data.

.. _`Data points`: https://iexcloud.io/docs/api/#data-points

Full access to the Data Points endpoints is available through the
``get_data_points`` function.

.. autofunction:: iexfinance.data_apis.get_data_points

.. _data-apis.data-points.available:

Available Data Points For a Symbol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain all available data points for a symbol, simply pass the symbol to
``get_data_points`` with no key:

.. ipython:: python

    from iexfinance.data_apis import get_data_points

    get_data_points("AAPL", output_format='pandas').head()

.. _data-apis.data-points.individual:

Individual Data Points For a Symbol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain an individual data point for a single symbol, pass the symbol and the
data point ID to ``get_data_points``:

**Apple Inc. (AAPL) latest price**

.. ipython:: python

    get_data_points("AAPL", "COMMONSTOCK")

.. _data-apis.time-series:

Time Series
-----------

`Time series`_ is the most common type of data available, and consists of a
collection of data points over a period of time. Time series data is indexed by a single date field, and can be retrieved by any portion of time.

.. _`Time Series`: https://iexcloud.io/docs/api/#time-series

Full access to the Time Series endpoints is available through the
``get_time_series`` function.

.. autofunction:: iexfinance.data_apis.get_time_series

.. _data-apis.time-series.all-time-series:

All Available Time Series
~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain a list of all available time series, simply call ``get_time_series``
with no parameters:

.. ipython:: python

    from iexfinance.data_apis import get_time_series

    get_time_series()

.. _data-apis.time-series.individual:

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

