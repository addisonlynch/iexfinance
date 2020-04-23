.. _testing:


Testing
=======

.. warning:: Use of the :ref:`Sandbox Environment<testing.sandbox>` is **required** when running the test suite.

Unit and integration tests for iexfinance are handled by the
`pytest <https://docs.pytest.org/en/latest>`__ platform.

.. _testing.dependencies:

Testing & Documentation Dependencies
------------------------------------

All testing & documentation dependencies can be installed via ``pip install -r requirements-dev.txt``.

**Testing**

-  pytest
-  pytest-runner
-  flake8
-  flake8-rst
-  requests-cache
-  six

**Docs**

- sphinx
- sphinx_rtd_theme
- sphinxcontrib-napoleon
- matplotlib
- ipython


.. _testing.sandbox:

Sandbox Environment
-------------------

IEX provides a sandbox_ environment for IEX Cloud. This environment can be accessed by setting ``IEX_API_VERSION`` to ``iexcloud-sandbox``. This will set ``iexfinance`` up for use with the sandbox base URL.

.. note:: Test keys (beginning with ``Tsk`` and ``Tpk``) must be used with the sandbox environment. To obtain these keys, select the "Viewing test data" toggler on the left side of the IEX Cloud console.

.. _sandbox: https://iexcloud.io/docs/api/#sandbox

.. _testing.local_testing:

Local Testing
-------------

We've provided the BASH script ``test.sh`` which is included in the
top-level iexfinance directory. This script will emulate the tests
needed for a TravisCI build to pass.

Docs can be tested with `Sphinx <https://www.sphinx-doc.org/en/stable>`__ (with extensions napoleon and sphinx_rtd_theme)
using the Makefile. ``make livehtml`` will serve the dev documentation site locally
on 127.0.0.1:8000.


.. _testing.test_weighting:

Test Weighting
--------------

Many tests which have a data weighting of over ``1000`` total are marked
``highweight``.


Exceptions
----------

.. automodule:: iexfinance.utils.exceptions
	:members:

.. _testing.releases:

Release Procedure
=================

