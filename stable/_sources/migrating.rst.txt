.. _migrating:

Migrating to IEX Cloud
======================

**IEX will end support for the Legacy v1 Devleoper API on June 1st, 2019.** At
that
time, the use of ``iexfinance`` will require an IEX Cloud account_. In
addition, support for all *legacy only* endpoints will be discontinued.

``iexfinance`` version 0.4.1 uses IEX Cloud by default and adds
warnings to all calls which use the legacy API. In version 0.4.2 (June 1st,
2019), all calls will default to IEX Cloud (most functions will remain
compatible with the new platform) in addition to the deprecation of
legacy-only functions.

IEX supports a number of subscrpition plans ranging from free tier to
enterprise-level service.

.. _account: https://iexcloud.io/pricing/


.. _migrating.basics:

Migration Overview
------------------

* Use of ``iexfinance`` will require an authentication token, which can be
  obtained through the creation of an IEX Cloud account. This token can be
  passed via :ref:`argument<config.auth.argument>` or by
  :ref:`setting<config.auth.env>` the environment variable ``IEX_TOKEN``
* ``iexfinance`` will default to IEX Cloud Version 1 for all API calls. Along
  with the discontinuation of the legacy API on June 1, 2019, the beta period
  for IEX Cloud will end. Setting ``IEX_API_VERSION`` to ``iexcloud-beta`` will
  return the equivalent to that of ``iexcloud-v1``
* An ``ImmediateDeprecationError`` will be thrown by ``iexfinance`` 0.4.2 for
  ``IEX_API_VERSION`` set to ``v1``.



.. _migrating.incompatible:

Backwards Incompatible Changes
------------------------------

THe following endpoints are **no longer supported** by IEX Cloud and will be
deprecated in ``iexfinance`` 0.4.2:

Stocks
~~~~~~

* Crypto Quotes - ``stocks.get_crypto_quotes``

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


