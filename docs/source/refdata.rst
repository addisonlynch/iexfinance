.. _refdata:

.. currentmodule:: iexfinance.refdata

Reference Data
==============

.. note:: The ``ref-data/symbols`` endpoint has changed in IEX Cloud. In the v1
    (legacy) Developer API, this endpoint returned the list of symbols IEX
    supports for trading. In IEX cloud, it returns the list of symbols IEX
    supports for *api calls*.

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


.. _refdata.iex_corporate_actions:

IEX Corporate Actions
---------------------

`IEX Corporate Actions <https://iextrading.com/developer/docs/#iex-corporate-actions>`__ is a reference list which includes the following:

    - Issues (new, deleted)
    - Symbol and name changes
    - Firms (new, deleted for IEX-listed securities)

Access is available through the top-level function ``get_iex_corporate_actions``:

.. autofunction:: get_iex_corporate_actions

.. _refdata.iex-corporate_actions_usage:

Usage
~~~~~


.. ipython:: python
    :okexcept:

    from iexfinance.refdata import get_iex_corporate_actions

    get_iex_corporate_actions()


.. _refdata.iex_dividends:

IEX Dividends
-------------

`IEX Dividends <https://iextrading.com/developer/docs/#iex-dividends>`__ details upcoming dividend information and other corporate actions (splits, etc.)

Access is available through the function ``get_iex_dividends``

.. autofunction:: get_iex_dividends

.. seealso:: The `Dividends <stock.html#dividends>`__ endpoint provides dividend information on individual or groups of ticker symbols

Usage
~~~~~


.. _refdata.iex_dividends_usage:

.. ipython:: python
    :okexcept:

    from iexfinance.refdata import get_iex_dividends

    get_iex_dividends()


.. _refdata.iex_next_day_ex_date:

IEX Next Day Ex Date
--------------------

`IEX Next Day Ex Date <https://iextrading.com/developer/docs/#iex-next-day-ex-date>`__ retrieves advance notifications of dividend declarations

Per the IEX `docs <https://iextrading.com/developer/docs/#iex-next-day-ex-date>`__, records are added at 8:00 a.m. ET one trading day before the specified ex-date, and updates are posted once per hour from 8:00 a.m to 6:00 p.m. EST daily.

Access is available through the top-level function ``get_iex_next_day_ex_date``

.. autofunction:: get_iex_next_day_ex_date


Usage
~~~~~

.. _refdata.iex_next-day_ex_date_usage:


.. ipython:: python
    :okexcept:

    from iexfinance.refdata import get_iex_next_day_ex_date

    get_iex_next_day_ex_date()


.. _refdata.iex_listed_symbol_directory:

IEX Listed Symbol Directory
---------------------------

Similar to :ref:`Symbol<refdata.symbols>`, `IEX Listed Symbol Directory
<https://iextrading.com/developer/docs/#iex-listed-symbol-directory>`__ returns an array of all IEX listed securities.

Access is available through the top-level function ``get_iex_listed_symbol_dir``


.. autofunction:: get_iex_listed_symbol_dir


Usage
~~~~~

.. _refdata.iex_listed_symbol_directory_usage:

.. ipython:: python
    :okexcept:

    from iexfinance.refdata import get_iex_listed_symbol_dir

    get_iex_listed_symbol_dir()[0]

