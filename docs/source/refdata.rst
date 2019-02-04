.. _refdata:



Reference Data
==============

The following functions retrieve data from the `IEX Reference Data <https://iextrading.com/developer/docs/#reference-data>`__ endpoints:

    - :ref:`Symbols<refdata.symbols>`
    - :ref:`IEX Corporate Actions<refdata.iex-corporate-actions>`
    - :ref:`IEX Dividends<refdata.iex-dividends>`
    - :ref:`IEX Next Day Ex Date<refdata.iex-next-day-ex-date>`
    - :ref:`IEX Listed Symbol Directory<refdata.iex-listed-symbol-directory>`


All endpoints will return in list format.

.. _refdata.symbols:

Symbols
-------

.. autofunction::iexfinance.refdata.get_symbols


.. _refdata.symbols_usage:

Usage
~~~~~

.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols()[:2]


.. _refdata.iex_symbols:

IEX Symbols
-----------

.. autofunction::iexfinance.refdata.get_iex_symbols

.. _refdata.iex_symbols_usage:

Usage
~~~~~

.. code-block:: python

    from iexfinance.refdata import get_iex_symbols

    get_iex_symbols()[:2]


.. _refdata.iex_corporate_actions:

IEX Corporate Actions
---------------------

`IEX Corporate Actions <https://iextrading.com/developer/docs/#iex-corporate-actions>`__ is a reference list which includes the following:

    - Issues (new, deleted)
    - Symbol and name changes
    - Firms (new, deleted for IEX-listed securities)

Access is available through the top-level function ``get_iex_corporate_actions``:

.. autofunction:: iexfinance.get_iex_corporate_actions

.. _refdata.iex-corporate-actions-usage:

Usage
~~~~~


.. ipython:: python
    :okexcept:

    from iexfinance import get_iex_corporate_actions

    get_iex_corporate_actions()[0]


.. _refdata.iex-dividends:

IEX Dividends
-------------

`IEX Dividends <https://iextrading.com/developer/docs/#iex-dividends>`__ details upcoming dividend information and other corporate actions (splits, etc.)

Access is available through the top-level function ``get_iex_dividends``

.. autofunction:: iexfinance.get_iex_dividends

.. seealso:: The `Dividends <stock.html#dividends>`__ endpoint provides dividend information on individual or groups of ticker symbols

Usage
~~~~~


.. _refdata.iex-dividends-usage:

.. ipython:: python
    :okexcept:

    from iexfinance import get_iex_dividends

    get_iex_iex_dividends()[0]



.. _refdata.iex-next-day-ex-date:

IEX Next Day Ex Date
--------------------

`IEX Next Day Ex Date <https://iextrading.com/developer/docs/#iex-next-day-ex-date>`__ retrieves advance notifications of dividend declarations

Per the IEX `docs <https://iextrading.com/developer/docs/#iex-next-day-ex-date>`__, records are added at 8:00 a.m. ET one trading day before the specified ex-date, and updates are posted once per hour from 8:00 a.m to 6:00 p.m. EST daily.

Access is available through the top-level function ``get_iex_next_day_ex_date``

.. autofunction:: iexfinance.get_iex_next_day_ex_date


Usage
~~~~~

.. _refdata.iex-next-day-ex-date-usage:


.. ipython:: python
    :okexcept:

    from iexfinance import get_iex_next_day_ex_date

    get_iex_next_day_ex_date()[0]


.. _refdata.iex-listed-symbol-directory:

IEX Listed Symbol Directory
---------------------------

Similar to :ref:`Symbol<refdata.symbols>`, `IEX Listed Symbol Directory
<https://iextrading.com/developer/docs/#iex-listed-symbol-directory>`__ returns an array of all IEX listed securities.

Access is available through the top-level function ``get_iex_listed_symbol_dir``


.. autofunction:: iexfinance.get_iex_listed_symbol_dir


Usage
~~~~~

.. _refdata.iex-listed-symbol-directory-usage:

.. ipython:: python
    :okexcept:

    from iexfinance import get_iex_listed_symbol_dir

    get_iex_listed_symbol_dir()[0]

