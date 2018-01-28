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

In ``iexfinance`` we provide the method ``get_available_symbols`` which
accesses this endpoint. This method returns a list of dictionary objects
for each symbol, indexed by the key "symbol".

Example
^^^^^^^

.. ipython:: python

    from iexfinance import get_available_symbols

    get_available_symbols()[:15]


