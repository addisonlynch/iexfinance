.. _config:


Configuration
=============

There are four core components of ``iexfinance``'s configuration:

* :ref:`config.auth` - setting your IEX Cloud Authentication Token
* :ref:`config.formatting` - configuring desired output format (mirror IEX output or Pandas DataFrame)
* :ref:`config.api_version` - specifying version of IEX Cloud to use
* :ref:`config.debugging` - cached sessions, request retries, and more

.. _config.api_version:

API Version
-----------

The desired IEX API version can be specified using the ``IEX_API_VERSION``
environment variable. The following versions are currently supported:

* ``stable`` - **default**
* ``beta`` 
* ``v1`` 
* ``latest``
* ``sandbox`` *for testing purposes*

.. seealso:: For more information on API versioning, see the IEX Cloud
             documentation_.

.. _documentation: https://iexcloud.io/docs/api/#versioning


.. _config.auth:

Authentication
--------------

An IEX Cloud account and authentication token are required to acecss the IEX Cloud API.

Your IEX Cloud (secret) authentication token can be passed to any function or at the instantiation of a ``Stock`` :ref:`object <stocks.stock_object>`.
It can also be stored in the ``IEX_TOKEN`` environment variable.

The IEX Cloud token is accessible via the IEX Cloud Console.

.. _config.auth.argument:

Passing as an Argument
~~~~~~~~~~~~~~~~~~~~~~

The authentication token can also be passed to any function call:


.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas', token="<YOUR-TOKEN>")

or at the instantiation of a ``Stock`` object:

.. code-block:: python

    from iexfinance.stocks import Stock

    a = Stock("AAPL", token="<YOUR-TOKEN>")
    a.get_quote()

.. _config.auth.env:

Environment Variable (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest (and recommended) way to authenticate your IEX Cloud account is by
storing your authentication token (secret key beginning with ``sk_``) in the
``IEX_TOKEN`` environment variable.

.. _config.auth.env.unix:

macOS/Linux
^^^^^^^^^^^

Type the following command into your terminal:

.. code-block:: bash

    $ export IEX_TOKEN=<YOUR-TOKEN>

.. _config.auth.env.windows:

Windows
^^^^^^^

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__ for instructions on setting environment variables in Windows operating systems.

.. _config.formatting:

Output Formatting
-----------------

By default, ``iexfinance`` returns data for most endpoints in a `pandas <https://pandas.pydata.org/>`__ ``DataFrame``.

Selecting ``json`` as the output format returns data formatted *exactly* as received from
the IEX Endpoint. Configuring ``iexfinance``'s output format can be done in two ways:

``output_format`` Argument
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass ``output_format``  as an argument to any function call:

.. ipython:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas').head()

or at the instantiation of a ``Stock`` object:

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

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__ for instructions on setting environment variables in Windows operating systems.

.. _config.debugging:

Debugging
---------

.. _config.iexbase:

``_IEXBase`` Class
~~~~~~~~~~~~~~~~~~

All ``iexfinance`` requests are made using the base class ``_IEXBase``.

.. autoclass:: iexfinance.base._IEXBase

.. _config.debugging.cached_sessions:

Cached Sessions
~~~~~~~~~~~~~~~

``iexfinance`` import ``requests-cache`` cached sessions. To pass a cached session to your request, pass the ``session`` keyword argument to any function call, or at instantiation of a ``Stock`` :ref:`object <stocks.stock_object>`.

.. _config.debugging.request_params:

Request Parameters
~~~~~~~~~~~~~~~~~~

* Use ``retry_count`` to specify the number of times to retry a failed request. The default value is ``3``.
* Use ``pause`` to specify the time between retry attempts. The default value is ``0.5``.
