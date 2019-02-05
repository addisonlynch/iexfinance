.. _auth:

Authentication
==============

.. note:: IEX Cloud is in public beta, and as such, registration for early beta
    access is required. Registration can be found `here <https://iexcloud.io/>`__.

An IEX Cloud account is required to acecss the IEX Cloud API.

.. _auth.configuring:

Configuring ``iexfinance`` authentication
-----------------------------------------

There are two ways to pass your IEX Cloud authentication token to
``iexfinance``


.. _auth.configuring.env:

Environment Variable (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest (and recommended) way to authenticate your IEX Cloud account is by
storing your authentication token (secret key beginning with ``sk_``) in the
``IEX_AUTH_TOKEN`` environment variable.

.. _auth.configuring.env.unix:

macOS/Linux
^^^^^^^^^^^

Type the following command into your terminal:

.. code-block:: bash

    $ export IEX_AUTH_TOKEN=<YOUR AUTH TOKEN>

Windows
^^^^^^^

See `here <https://superuser.com/questions/949560/how-do-i-set-system-environment-variables-in-windows-10>`__


.. _auth.configuring.parameter:

Passing as a Parameter
----------------------

The authentication token can also be passed to any function call, or at the
instantiation of a ``Stock`` object:

.. code-block:: python

    from iexfinance.stocks import Stock

    a = Stock("AAPL", token="<YOUR AUTH TOKEN>")
    a.get_quote()

.. code-block:: python

    from iexfinance.refdata import get_symbols

    get_symbols(output_format='pandas', token="<YOUR AUTH TOKEN>")
