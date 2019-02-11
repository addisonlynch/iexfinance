.. _config:


Configuration
=============

.. _config.auth:

Authentication
--------------

.. note:: IEX Cloud is in public beta, and as such, registration for early beta
    access is required. Registration can be found `here <https://iexcloud.io/>`__.

An IEX Cloud account is required to acecss the IEX Cloud API.

There are two ways to pass your IEX Cloud authentication token to
``iexfinance``: environment variables and arguments.


.. _config.auth.env:

Environment Variable (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest (and recommended) way to authenticate your IEX Cloud account is by
storing your authentication token (secret key beginning with ``sk_``) in the
``IEX_AUTH_TOKEN`` environment variable.

.. _config.auth.env.unix:

macOS/Linux
^^^^^^^^^^^

Type the following command into your terminal:

.. code-block:: bash

    $ export IEX_AUTH_TOKEN=<YOUR AUTH TOKEN>

.. _config.auth.env.windows:

Windows
^^^^^^^

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__


.. _config.auth.argument:

Passing as an Argument
~~~~~~~~~~~~~~~~~~~~~~

The authentication token can also be passed to any function call, or at the instantiation of a ``Stock`` object:

.. code-block:: python

    from iexfinance.stocks import Stock

    a = Stock("AAPL", token="<YOUR AUTH TOKEN>")
    a.get_quote()

.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas', token="<YOUR AUTH TOKEN>")


.. _config.formatting:

Output Formatting
-----------------

By default, ``iexfinance`` returns data formatted *exactly* as received from
the IEX Endpoint. `pandas <https://pandas.pydata.org/>`__ ``DataFrame`` output
formatting is available for most endpoints. Configuring ``iexfinance``'s
output format can be done in two ways:

``output_format`` Argument
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass ``output_format``  as an argument to any function call or at the
instantiation of a ``Stock`` object:

.. ipython:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas').head()

or for the ``Stock`` object:

.. ipython:: python

    from iexfinance.stocks import Stock

    aapl = Stock("AAPL", output_format='pandas')
    aapl.get_quote().head()

Environment Variable
~~~~~~~~~~~~~~~~~~~~

For persistent configuration of a specified output format, use the environment
variable ``IEX_OUTPUT_FORMAT``. This value will be overridden by the
``output_format`` argument if it is passed.

macOS/Linux
^^^^^^^^^^^

Type the following command into your terminal:

.. code-block:: bash

    $ export IEX_OUTPUT_FORMAT=pandas

Windows
^^^^^^^

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__

