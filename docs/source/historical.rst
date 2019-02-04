.. _historical:

.. currentmodule:: iexfinance.stocks

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

