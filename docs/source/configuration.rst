.. _config:


Configuration
=============

There are four core components of ``iexfinance``'s configuration:

* :ref:`config.api_version` - specifying use of IEX Cloud or the IEX legacy v1 Developer API
* :ref:`config.auth` - setting your IEX Cloud Authentication Token
* :ref:`config.formatting` - configuring desired output format (mirror IEX output or Pandas DataFrame)
* :ref:`config.debugging` - cached sessions, request retries, and more


.. _config.api_version:

API Version
-----------

By default, ``iexfinance`` makes its requests to the legacy
`v1 IEX Developer API <https://iextrading.com/developer/docs/>`__. IEX recommends migrating to IEX Cloud.

.. seealso:: :ref:`migrating`

To select an API version, set the environment variable ``IEX_API_VERSION`` to one of the following values:

- ``v1``: IEX legacy v1.0 `Developer API <https://iextrading.com/developer/docs/>`__
- ``iexcloud-beta`` for the current beta of `IEX Cloud <https://iexcloud.io/docs/api/>`__


.. _config.auth:

Authentication
--------------

.. note:: IEX Cloud is in public beta, and as such, registration for early beta
    access is required. Registration can be found `here <https://iexcloud.io/>`__.

An IEX Cloud account is required to acecss the IEX Cloud API.

Your IEX Cloud (secret) authentication token can be passed to any function or at the instantiation of a ``Stock`` :ref:`object <stocks.stock_object>` It can also be stored in the ``IEX_API_KEY`` environment variable.

.. _config.auth.argument:

Passing as an Argument
~~~~~~~~~~~~~~~~~~~~~~

The authentication token can also be passed to any function call:


.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas', token="<YOUR AUTH TOKEN>")

or at the instantiation of a ``Stock`` object:

.. code-block:: python

    from iexfinance.stocks import Stock

    a = Stock("AAPL", token="<YOUR AUTH TOKEN>")
    a.get_quote()



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



.. _config.formatting:

Output Formatting
-----------------

By default, ``iexfinance`` returns data formatted *exactly* as received from
the IEX Endpoint. `pandas <https://pandas.pydata.org/>`__ ``DataFrame`` output
formatting is available for most endpoints. Configuring ``iexfinance``'s
output format can be done in two ways:

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

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__


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
