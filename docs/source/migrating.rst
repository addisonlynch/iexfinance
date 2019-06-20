.. _migrating:

Migrating to IEX Cloud
======================

**IEX ended support for the Legacy v1 Devleoper API on June 1st, 2019.** The
use of ``iexfinance`` now requires an IEX Cloud account_. In
addition, support for all *legacy only* endpoints has been discontinued.

IEX supports a number of subscription plans ranging from free tier to
enterprise-level service.

.. _account: https://iexcloud.io/pricing/


.. _migrating.basics:

Migration Overview
------------------

* Use of ``iexfinance`` now requires an authentication token, which
  can be obtained through the creation of an IEX Cloud account. This token can be passed via :ref:`argument<config.auth.argument>` or by
  :ref:`setting<config.auth.env>` the environment variable ``IEX_TOKEN``
* ``iexfinance`` defaults IEX Cloud for all API calls. Setting
  ``IEX_API_VERSION`` to ``v1`` or ``iexcloud-beta``
  returns the equivalent to that of ``iexcloud-v1``



.. _migrating.incompatible:

Backwards Incompatible Changes
------------------------------

The following endpoints are **no longer supported** by IEX Cloud and have been
deprecated:

Stocks
~~~~~~

* Crypto Quotes - ``stocks.get_crypto_quotes``
* Effective Spread - ``stocks.Stock.get_effective_spread``

Reference Data
~~~~~~~~~~~~~~

* IEX Corporate Actions - ``refdata.get_iex_corporate_actions``
* IEX Dividends - ``refdata.get_iex_dividends``
* IEX Next Day Ex Date - ``refdata.get_iex_next_day_ex_date``
* IEX Listed Symbol Directory - ``refdata.get_iex_listed_symbol_dir``


.. _migrating.additional_info:

Additional Information
----------------------

- The ``ref-data/symbols`` endpoint has changed in IEX Cloud. In the v1
  (legacy) Developer API, this endpoint returned the list of symbols IEX
  supports for trading. In IEX cloud, it returns the list of symbols IEX
  supports for *api calls*.


