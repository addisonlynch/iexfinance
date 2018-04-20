iexfinance
===============

.. image:: https://travis-ci.org/addisonlynch/iexfinance.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/iexfinance

.. image:: https://codecov.io/gh/addisonlynch/iexfinance/branch/master/graphs/badge.svg?branch=master
	:target: https://codecov.io/gh/addisonlynch/iexfinance

.. image:: https://badge.fury.io/py/iexfinance.svg
    :target: https://badge.fury.io/py/iexfinance

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0


Python module to retrieve stock data from the 
`Investors Exchange (IEX) <https://iextrading.com/>`__ 
`Developer API <https://iextrading.com/developer/>`__
platform. iexfinance provides real-time financial data from the various IEX
endpoints, as well as historical time-series data.

This data includes stock quotes, fundamentals, actions, and information. In
addition, support for IEX market data and statistics is provided. 

- `Stocks <https://iextrading.com/developer/docs/#stocks>`__
- `Reference Data <https://iextrading.com/developer/docs/#reference-data>`__
- `IEX Market Data <https://iextrading.com/developer/docs/#iex-market-data>`__
- `IEX Stats <https://iextrading.com/developer/docs/#iex-stats>`__

Documentation
-------------

See `IEX Finance
Documentation <https://addisonlynch.github.io/iexfinance/index.html#documentation>`__

Install
-------

From PyPI with pip (latest stable release):

``$ pip3 install iexfinance``

From development repository (dev version):

.. code:: bash

     $ git clone https://github.com/addisonlynch/iexfinance.git  
     $ cd iexfinance  
     $ python3 setup.py install  

Usage Examples
--------------


Using iexfinance to access data from IEX is quite easy. The most commonly-used
endpoints are the `Stocks <https://iextrading.com/developer/docs/#stocks>`__
endpoints, which allow access to various information regarding equities,
including quotes, historical prices, dividends, and much more. 

All top-level functions (such as ``Stock`` and ``get_historical_data``), allow
for `Request Parameters
<https://addisonlynch.github.io/usage.html#parameters>`__, which
include ``retry_count``, ``pause``, and ``session``. These parameters are
entirely optional. The first two deal with how unsuccessful requests are
handled, and the third allows for the passing of a cached ``requests-cache``
session (see `caching
<https://addisonlynch.github.io/iexfinance/caching.html>`__).

Stock Endpoints
^^^^^^^^^^^^^^^

.. code:: python

    from iexfinance import Stock
    tsla = Stock('TSLA')
    tsla.get_open()
    tsla.get_price()

It's also possible to obtain historical data from the ``get_historical_data``
top-level function. This will return a daily time-series of the ticker
requested over the desired date range (``start`` and ``end`` passed as
``datetime.datetime`` objects).

Pandas DataFrame and JSON (dict) output formatting are selected with the
``output_format`` parameter.

**Historical Data**

.. code:: python
	
	from iexfinance import get_historical_data
	from datetime import datetime

	start = datetime(2017, 2, 9)
	end = datetime(2017, 5, 24)

	df = get_historical_data("AAPL", start=start, end=end, output_format='pandas')
	df.head()

The resulting DataFrame will indexed by date, with a column for each OHLC
datapoint:

.. image:: /docs/source/images/dfdailyaapl.JPG

It's really simple to plot this data, using `matplotlib:

.. code:: python

	import matplotlib.pyplot as plt

	df.plot()
	plt.show()

<https://matplotlib.org/>`__

.. image:: /docs/source/images/plotdailyaapl.jpg

IEX Reference Data
^^^^^^^^^^^^^^^^^^

Support for the `IEX Reference Data
<https://iextrading.com/developer/docs/#reference-data>`__ endpoints is
available through the top level functions ``get_symbols``,
``get_corporate_actions``, ``get_dividends``, ``get_next_day_ex_date``, and
``get_listed_symbol_dir``. As with all endpoints, request parameters such as
``retry_count`` and output format selection (through ``output_format``) can be
passed to the call.

.. code:: python

	from iexfinance import get_available_symbols

	get_available_symbols(output_format='pandas')[:2]


IEX Market Data
^^^^^^^^^^^^^^^

The `IEX Market Data
<https://iextrading.com/developer/docs/#iex-market-data>`__ endpoints are
supported through various top-level functions, including ``get_market_tops``
and ``get_market_deep``. 

.. code:: python

	from iexfinance import get_market_tops

	get_market_tops()



IEX Stats
^^^^^^^^^

The `IEX Stats
<https://iextrading.com/developer/docs/#iex-stats>`__ endpoints are
supported through various top-level functions, including ``get_stats_intraday``
and ``get_stats_recent``. These endpoints provide IEX's trading statistics for
a given ticker.

.. code:: python

	from iexfinance import get_stats_intraday

	get_stats_intraday()



Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2018 Addison Lynch

See LICENSE for details
