.. _ref:


**************
Reference Data
**************

The following functions retrieve data from the `IEX Reference Data <https://iextrading.com/developer/docs/#reference-data>`__ endpoints.

    - :ref:`Symbols<ref.symbols>`
    - :ref:`IEX Corporate Actions<ref.iex-corporate-actions>`
    - :ref:`IEX Dividends<ref.iex-dividends>`
    - :ref:`IEX Next Day Ex Date<ref.iex-next-day-ex-date>`
    - :ref:`IEX Listed Symbol Directory<ref.iex-listed-symbol-directory>`

.. warning:: These endpoints are not yet operational as of 1/31/2018


All endpoints will return in list format.

.. _ref.symbols:

Symbols
=======

From the `IEX API
Docs <https://iextrading.com/developer/docs/#stocks>`__:

    Use the /ref-data/symbols endpoint to find the symbols that we
    support.

``iexfinance`` provides the top-level function ``get_reference_data`` which
accesses this endpoint. This function returns a list of dictionary objects
for each symbol, indexed by the key "symbol":

.. autofunction::iexfinance.get_reference_data

Further, the function, ``get_available_symbols``
extracts the symbols and returns a list of the symbols only:

.. autofunction::iexfinance.get_available_symbols

.. _ref.symbols-example:

Example
-------

.. ipython:: python

    from iexfinance import get_reference_data

    get_reference_data()[:2]


.. ipython:: python

    from iexfinance import get_available_symbols

    get_available_symbols()[:5]


.. _ref.iex-corporate-actions:

IEX Corporate Actions
=====================

IEX provides a reference list which includes the following

	- Issues (new, deleted)
	- Symbol and name changes
	- Firms (new, deleted for IEX-listed securities)

Access is available through the top-level function ``get_iex_corporate_actions``:

.. autofunction:: iexfinance.get_iex_corporate_actions

.. _ref.iex-corporate-actions-examples:

Examples
-------


.. ipython:: python

	from iexfinance import get_iex_corporate_actions

	get_iex_corporate_actions()[0]


.. _ref.iex-dividends:

IEX Dividends
=============

The Dividends endpoint details upcoming dividend information and other corporate actions (splits, etc.)

Access is available through the top-level function ``get_iex_dividends``

.. autofunction:: iexfinance.get_iex_dividends

.. seealso:: The `Dividends <stock.html#dividends>`__ endpoint provides dividend information on individual or groups of ticker symbols

Examples
-------


.. _ref.iex-dividends-examples:

.. ipython:: pyhton

	from iexfinance import get_iex_dividends

	get_iex_iex_dividends()[0]



.. _ref.iex-next-day-ex-date:

IEX Next Day Ex Date
====================

The IEX Next Day Ex Date retrieves advance notifications of dividend declarations

Per the IEX `docs <https://iextrading.com/developer/docs/#iex-next-day-ex-date>`__, records are added at 8:00 a.m. ET one trading day before the specified ex-date, and updates are posted once per hour from 8:00 a.m to 6:00 p.m. EST daily.

Access is available through the top-level function ``get_iex_next_day_ex_date``

.. autofunction:: iexfinance.get_next_day_ex_date


Examples
-------

.. _ref.iex-next-day-ex-date-examples:


.. ipython:: python

	from iexfinance import get_iex_next_day_ex_date

	get_iex_next_day_ex_date()[0]


.. _ref.iex-listed-symbol-directory:

IEX Listed Symbol Directory
===========================

Similar to `Symbols <ref.symbols>`, IEX Listed Symbol Directory erturns an array of all IEX listed securities.

Access is available through the top-level function ``get_iex_listed_symbol_dir``


..autofunction :: iexfinance.get_iex_listed_symbol_dir


Examples
--------

.. _ref.iex-listed-symbol-directory-examples:

.. ipython:: python

	from iexfinance import get_iex_listed_symbol_dir

	get_iex_listed_symbol_dir()[0]

