.. _refdata:

.. currentmodule:: iexfinance.refdata

Reference Data
==============

.. contents:: Endpoints
    :depth: 2


.. _refdata.symbols:

Symbols
-------

.. autofunction:: iexfinance.refdata.get_symbols


.. _refdata.symbols_usage:

Usage
~~~~~

.. ipython:: python

    from iexfinance.refdata import get_symbols

    get_symbols()[:2]


.. _refdata.iex_symbols:

IEX Symbols
-----------

.. autofunction:: iexfinance.refdata.get_iex_symbols

.. _refdata.iex_symbols_usage:

Usage
~~~~~

.. code-block:: python

    from iexfinance.refdata import get_iex_symbols

    get_iex_symbols()[:2]


.. _refdata.holidays:

U.S. Holidays & Trading Dates
-----------------------------

.. autofunction:: iexfinance.refdata.get_us_trading_dates_holidays