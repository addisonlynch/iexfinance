# What's New

New features, bug fixes, and improvements for each release.

## v0.3.0 (January 24, 2018)

This is a major release from 0.2.0, and we recommend that all users update.

Highlights:
	- Added **get_historical_data** for the retrieval of time-series data from the [chart](https://iextrading.com/developer/docs/#chart) endpoint
	- 

#### What's new in v0.3.0
- [New Features]()
- [Improvements]()
- [Bug Fixes]()

### New Features

- Added support for [IEX Market Data](https://iextrading.com/developer/docs/#iex-market-data)
- Added support for [IEX Stats](https://iextrading.com/developer/docs/#iex-stats)
- Added support for Historical data through the Stocks [chart](https://iextrading.com/developer/docs/#chart) endpoint
- Added [Pandas](https://pandas.pydata.org) as an output format for the [Market](market.md) and [Stats](stats.md) endpoints as well as for [Historical Data](historical.md).


### Improvements

- PEP8 formatting [GH9](https://github.com/addisonlynch/iexfinance/issues/9), managed by [flake8](https://flake8.pycqa.org/en/latest)
- Migrated to [pytest](https://docs.pytest.org/en/latest/#documentation) for testing


### Bug Fixes

- Incorrectly rejects lists of size 51-100 [GH1](https://github.com/addisonlynch/iexfinance/issues/1)
- Repaired and improved unit tests [GH6](https://github.com/addisonlynch/iexfinance/issues/6)

## Changelog

See [changelog](https://github.com/addisonlynch/iexfinance/blob/master/CHANGELOG.md).
