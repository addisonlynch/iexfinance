.. _account:

Account
=======

The `Account <https://iexcloud.io/docs/api/#account>`__ endpoints provide information about your IEX Cloud account, which allow tracking of message counts, account metadata, and more.

* :ref:`account.metadata`
* :ref:`account.usage`
* :ref:`account.pay_as_you_go`

Data weighting for all ``iexfinance.account`` endpoints is ``Free``.

.. _account.metadata:

Metadata
--------

.. autofunction:: iexfinance.account.get_metadata


.. _account.metadata.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.account import get_metadata

    get_metadata()

.. _account.usage:

Usage
-----

.. autofunction:: iexfinance.account.get_usage

.. _account.usage.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.account import get_usage

    get_usage()

.. _account.pay_as_you_go:

Pay as you go
-------------

``iexfinance`` provides two methods, ``allow_pay_as_you_go`` and
``disallow_pay_as_you_go`` to toggle Pay-as-you-go for a given account.

.. autofunction:: iexfinance.account.allow_pay_as_you_go

.. autofunction:: iexfinance.account.disallow_pay_as_you_go

.. _account.pay_as_you_go.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.account import allow_pay_as_you_go

    allow_pay_as_you_go()

.. code-block:: python

    from iexfinance.account import disallow_pay_as_you_go

    disallow_pay_as_you_go()
