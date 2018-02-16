iexfinance
===============

.. image:: https://travis-ci.org/addisonlynch/iexfinance.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/iexfinance

.. image:: https://codecov.io/gh/addisonlynch/iexfinance/branch/master/graphs/badge.svg?branch=master
	:target: https://codecov.io/gh/addisonlynch/iexfinance


Python module to get stock data from the Investors Exchange (IEX) Developer API
platform. iexfinance provides real-time financial data from the various IEX
endpoints, as well as historical data.

- `Stocks <https://iextrading.com/developer/docs/#stocks>`__
	- Historical Data
- `Reference Data <https://iextrading.com/developer/docs/#reference-data>`__
- `IEX Market Data <https://iextrading.com/developer/docs/#iex-market-data>`__
- `IEX Stats <https://iextrading.com/developer/docs/#iex-stats>`__

Documentation
-------------

See `IEX Finance
Documentation <https://addisonlynch.github.io/iexfinance/index.html#Documentation>`__

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

Stock Endpoints
^^^^^^^^^^^^^^^

.. code:: python

    from iexfinance import Stock
    tsla = Stock('TSLA')
    tsla.get_open()
    tsla.get_price()

**Historical Data**

.. code:: python
	
	from iexfinance import get_historical_data
	from datetime import datetime

	start = datetime(2017, 2, 9)
	end = datetime(2017, 5, 24)

	df = get_historical_data("AAPL", start=start, end=end, output_format='pandas')
	df.head()


IEX Reference Data
^^^^^^^^^^^^^^^^^^

.. code:: python

	from iexfinance import get_available_symbols

	get_available_symbols()[:2]


IEX Market Data
^^^^^^^^^^^^^^^

.. code:: python

	from iexfinance import get_market_tops

	get_market_tops()

IEX Stats
^^^^^^^^^

.. code:: python

	from iexfinance import get_stats_intraday

	get_stats_intraday()




Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2017 Addison Lynch

See LICENSE for details
