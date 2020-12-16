.. _testing:


Testing
=======

.. warning:: Use of the :ref:`Sandbox Environment<testing.sandbox>` is **required** when running the test suite.

Unit and integration tests for iexfinance are handled by the
`pytest <https://docs.pytest.org/en/latest>`__ platform.

.. _testing.dependencies:

Testing & Documentation Dependencies
------------------------------------

.. note:: Running the test suite and linting the code & documentation require Python 3.6 or above.

All testing dependencies can be installed via ``pip install -r requirements-dev.txt``.

**Testing**

-  black
-  codecov
-  flake8
-  flake8-bugbear
-  flake8-rst
-  pytest
-  pytest-runner
-  tox

All documentation dependencies can be installed via ``pip install -r docs/requirements.txt``.

**Docs**

- ipython
- matplotlib
- requests-cache
- sphinx
- sphinx-rtd-theme
- sphinxcontrib-napoleon
- sphinx-autobuild (optional)

.. _testing.sandbox:

Sandbox Environment
-------------------

IEX provides a sandbox_ environment for IEX Cloud. This environment can be accessed by setting ``IEX_API_VERSION`` to ``sandbox``. This will set ``iexfinance`` up for use with the sandbox base URL.

.. note:: Test keys (beginning with ``Tsk`` and ``Tpk``) must be used with the sandbox environment. To obtain these keys, select the **Viewing test data** toggler on the left side of the IEX Cloud console.

.. _sandbox: https://iexcloud.io/docs/api/#testing-sandbox

.. _testing.local_testing:

Local Testing
-------------

A BASH script ``test.sh`` is included in the
top-level iexfinance directory. This script will emulate the tests
needed for a TravisCI build to pass.

Note that your environment needs to export a testing IEX_TOKEN to execute tests.

The ``iexfinance`` documentation can be tested with `Sphinx <https://www.sphinx-doc.org/en/master/>`__ (with extensions napoleon and sphinx_rtd_theme)
using the Makefile. ``make livehtml`` will serve the dev documentation site locally
on 127.0.0.1:8000.

Exceptions
----------

.. automodule:: iexfinance.utils.exceptions
	:members:
