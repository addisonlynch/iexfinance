.. _ref:


**************
Reference Data
**************

Symbols
-------

From the `IEX API
Docs <https://iextrading.com/developer/docs/#stocks>`__:

    Use the /ref-data/symbols endpoint to find the symbols that we
    support.

``iexfinance`` provides the top-level function ``get_reference_data`` which
accesses this endpoint. This function returns a list of dictionary objects
for each symbol, indexed by the key "symbol":

.. autofunciton::iexfinance.get_reference_data

Further, the function, ``get_available_symbols``
extracts the symbols and returns a list of the symbols only:

.. autofunction::iexfinance.get_available_symbols

Example
^^^^^^^

.. ipython:: python

    from iexfinance import get_reference_data

    get_reference_data()[:2]


.. ipython:: python

    from iexfinance import get_available_symbols

    get_available_symbols()[:5]