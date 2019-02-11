.. _historical:

.. currentmodule:: iexfinance.stocks


Historical Data
===============

Historical time series data is available through the
``get_historical_data`` and ``get_historical_intraday`` functions of
``stocks``, which
source the
`chart <https://iextrading.com/developer/docs/#chart>`__ endpoint.

Daily data can be retrieved from up to 5 years before the current date, and
historical data up to 3 months prior to the current date.

Usage
-----

Daily
^^^^^

To obtain daily historical data, use ``get_historical_data``.

.. autofunction:: get_historical_data


If no date parameters are passed, the start date will default to 2015/1/1
and the end date will default to the current date.


.. ipython:: python
    :okwarning:

    from iexfinance.stocks import get_historical_data
    from datetime import datetime

    start = datetime(2017, 2, 9)
    end = datetime(2017, 5, 24)

    f = get_historical_data('AAPL', start, end, output_format='pandas')
    f.loc["2017-02-09"]


Minutely
^^^^^^^^

To obtain one-minute intraday data for a given date, use
``get_historical_intraday``. **Note: this endpoint has a maximum of one symbol
and a single date.**

.. autofunction:: get_historical_intraday

.. ipython:: python

    from datetime import datetime
    from iexfinance.stocks import get_historical_intraday

    date = datetime(2018, 11, 27)

    data = get_historical_intraday("AAPL", date, output_format='pandas')
    data.head()


Plotting
--------

With Pandas output formatting, we are able to plot historical price
movements using matplotlib.

.. ipython:: python


    from iexfinance.stocks import get_historical_data
    from datetime import datetime
    import matplotlib.pyplot as plt
    start = datetime(2017, 2, 9)
    end = datetime(2017, 5, 24)

    f = get_historical_data("AAPL", start, end, output_format='pandas')
    plt.plot(f["close"])
    plt.title('Time series chart for AAPL')
    plt.show()

.. image:: images/plotdailyaapl.jpg
