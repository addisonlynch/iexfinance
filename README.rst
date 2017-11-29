IEX Finance API
===============

.. image:: https://travis-ci.org/addisonlynch/iexfinance.svg?branch=master
    :target: https://travis-ci.org/addisonlynch/iexfinance

Python module to get stock data from the Investors Exchange (IEX) Developer API platform. iexfinance provides real-time financial data from the various IEX Stock endpoints. 


Documentation
-------------

See `IEX Finance
Documentation <https://addisonlynch.github.io/iexfinance>`__

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

.. code:: python

    >>> from iexfinance import Share
    >>> tsla = Share('TSLA')
    >>> print(tsla.get_open())
    '299.64'
    >>> print(tsla.get_price())
    '301.84'

Contact
-------

Email: `ahlshop@gmail.com <ahlshop@gmail.com>`__

Twitter: `alynchfc <https://www.twitter.com/alynchfc>`__

License
-------

Copyright © 2017 Addison Lynch

See LICENSE for details