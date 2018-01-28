.. _whatsnew:

**********
What's New
**********

New features, bug fixes, and improvements for each release.

v0.3.0 (January 24, 2018)
-------------------------

This is a major release from 0.2.0, and we recommend that all users
update.

Highlights: - Added **get\_historical\_data** for the retrieval of
time-series data from the
`chart <https://iextrading.com/developer/docs/#chart>`__ endpoint -

What's new in v0.3.0
^^^^^^^^^^^^^^^^^^^^

-  `Improvements <>`__
-  `Bug Fixes <>`__

New Features
~~~~~~~~~~~~

-  Added support for `IEX Market
   Data <https://iextrading.com/developer/docs/#iex-market-data>`__
-  Added support for `IEX
   Stats <https://iextrading.com/developer/docs/#iex-stats>`__
-  Added support for Historical data through the Stocks
   `chart <https://iextrading.com/developer/docs/#chart>`__ endpoint
-  Added `Pandas <https://pandas.pydata.org>`__ as an output format for
   the `Market <market.md>`__ and `Stats <stats.md>`__ endpoints as well
   as for `Historical Data <historical.md>`__.

Improvements
~~~~~~~~~~~~

-  PEP8 formatting
   `GH9 <https://github.com/addisonlynch/iexfinance/issues/9>`__,
   managed by `flake8 <https://flake8.pycqa.org/en/latest>`__
-  Migrated to
   `pytest <https://docs.pytest.org/en/latest/#documentation>`__ for
   testing
-  Migrated to Sphinx and RST for documentation

Bug Fixes
~~~~~~~~~

-  Incorrectly rejects lists of size 51-100
   `GH1 <https://github.com/addisonlynch/iexfinance/issues/1>`__
-  Repaired and improved unit tests
   `GH6 <https://github.com/addisonlynch/iexfinance/issues/6>`__

Changelog
---------

See
`changelog <https://github.com/addisonlynch/iexfinance/blob/master/CHANGELOG.md>`__.
