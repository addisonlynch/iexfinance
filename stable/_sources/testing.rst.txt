.. _testing:


Testing
=======

Unit and integration tests for iexfinance are handled by the
`pytest <https://docs.pytest.org/en/latest>`__ platform.

.. _testing.dependencies:

Testing & Documentation Dependencies
------------------------------------

**Testing**

-  pytest
-  pytest-runner
-  flake8
-  flake8-rst
-  requests-cache
-  six

**Docs**

- sphinx
- sphinx-autobuild
- sphinx-rtd-theme
- sphinxcontrib-napoleon
- matplotlib
- ipython

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

Most tests which have a data weighting of over ``1000`` total are marked
``highweight``.


Exceptions
----------

.. automodule:: iexfinance.utils.exceptions
	:members:
