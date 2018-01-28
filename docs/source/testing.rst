.. _testing:

*******
Testing
*******

Unit and integration tests for iexfinance are handled by the
`pytest <https://docs.pytest.org/en/latest>`__ platform.

Dependencies
------------

-  mock
-  pytest
-  pytest-runner

Local Testing
-------------

We've provided the BASH script ``test.sh`` which is included in the
top-level iexfinance directory. This script will emulate the tests
needed for a TravisCI build to pass.
