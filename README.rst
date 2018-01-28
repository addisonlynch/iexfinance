iexfinance
===============

.. image:: https://travis-ci.org/addisonlynch/iexfinance.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/iexfinance

.. image:: https://codecov.io/gh/addisonlynch/iexfinance/branch/master/graphs/badge.svg?branch=master
	:target: https://codecov.io/gh/addisonlynch/iexfinance


Python module to get stock data from the Investors Exchange (IEX) Developer API platform. iexfinance provides real-time financial data from the various IEX Stock endpoints. 


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

.. ipython:: python

    from iexfinance import Stock
    tsla = Stock('TSLA')
    tsla.get_open()
    tsla.get_price()

Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2017 Addison Lynch

See LICENSE for details