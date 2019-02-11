.. _account:

Account
=======

.. _account.metadata:

Metadata
--------

.. autofunction:: iexfinance.tools.account.get_metadata


.. _account.metadata.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.tools import get_metadata

    get_metadata()

.. _account.usage:

Usage
-----

.. autofunction:: iexfinance.tools.account.get_usage

.. _account.usage.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.tools import get_usage

    get_usage()

.. _account.pay_as_you_go:

Pay as you go
-------------

``iexfinance`` provides two methods, ``allow_pay_as_you_go`` and
``disallow_pay_as_you_go`` to toggle Pay-as-you-go for a given account.

.. autofunction:: iexfinance.tools.account.allow_pay_as_you_go

.. autofunction:: iexfinance.tools.account.disallow_pay_as_you_go

.. _account.pay_as_you_go.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.tools import allow_pay_as_you_go

    allow_pay_as_you_go()

.. code-block:: python

    from iexfinance.tools import disallow_pay_as_you_go

    disallow_pay_as_you_go()
