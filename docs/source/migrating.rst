.. _migrating:

Migrating to IEX Cloud
======================


.. _migrating.cloud_only:

Cloud Endpoints (Added in IEX Cloud)
------------------------------------

Stocks
~~~~~~

* Market Volume - ``stocks.get_market_volume``

Reference Data
~~~~~~~~~~~~~~

* IEX Symbols - ``refdata.get_iex_symbols``
*


.. _migrating.legacy_only:

Legacy Endpoints (Removed in IEX Cloud)
---------------------------------------

Stocks
~~~~~~

* Crypto Quotes - ``stocks.get_crypto_quotes``

Reference Data
~~~~~~~~~~~~~~

* IEX Corporate Actions - ``refdata.get_iex_corporate_actions``
* IEX Dividends - ``refdata.get_iex_dividends``
* IEX Next Day Ex Date - ``refdata.get_iex_next_day_ex_date``
* IEX Listed Symbol Directory - ``refdata.get_iex_listed_symbol_dir``


.. _migrating.ref_data:

Reference Data
--------------

- The ``ref-data/symbols`` endpoint has changed in IEX Cloud. In the v1
  (legacy) Developer API, this endpoint returned the list of symbols IEX
  supports for trading. In IEX cloud, it returns the list of symbols IEX
  supports for *api calls*.


