.. _options:

Options
=======

.. _options.eod:

End of Day Options
------------------

End of day options prices are available through the top-level function
``get_eod_options`` for a single symbol.

.. autofunction:: iexfinance.stocks.get_eod_options

.. _options.eod.expiry_list:

List of Expiration Dates
~~~~~~~~~~~~~~~~~~~~~~~~

To obtain a list of all options expiration dates for a symbol, simply call ``get_eod_options`` with a symbol only:

.. ipython:: python

    from iexfinance.stocks import get_eod_options

    get_eod_options("AAPL", output_format='pandas').head()


.. _options.eod.single_date:

Options For A Single Date
~~~~~~~~~~~~~~~~~~~~~~~~~

To obtain the end-of-day prices of options contracts for a single expiration date (in the form ``YYYYMM``):

.. code-block:: python

    get_eod_options("AAPL", "201906")


.. _options.eod.filter:

Calls/Puts Only
~~~~~~~~~~~~~~~

It is possible to limit option results to calls or puts only:

.. code-block:: python

    get_eod_options("AAPL", "201906", "calls")

or:

.. code-block:: python

    get_eod_options("AAPL", "201906", "puts")
