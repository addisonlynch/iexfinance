.. _stocks:


******
Stocks
******

.. _stocks.Share:

Share
=====

.. autoclass:: iexfinance.stock.Share

.. _share-utility-methods:

Utility Methods
---------------

.. _share-endpoint-methods:

Endpoint Methods
----------------

.. automethod:: iexfinance.stock.Share.get_quote
.. automethod:: iexfinance.stock.Share.get_chart
.. automethod:: iexfinance.stock.Share.get_book
.. automethod:: iexfinance.stock.Share.get_open_close
.. automethod:: iexfinance.stock.Share.get_previous
.. automethod:: iexfinance.stock.Share.get_company
.. automethod:: iexfinance.stock.Share.get_key_stats
.. automethod:: iexfinance.stock.Share.get_relevant
.. automethod:: iexfinance.stock.Share.get_news
.. automethod:: iexfinance.stock.Share.get_financials
.. automethod:: iexfinance.stock.Share.get_earnings
.. automethod:: iexfinance.stock.Share.get_dividends
.. automethod:: iexfinance.stock.Share.get_splits
.. automethod:: iexfinance.stock.Share.get_logo
.. automethod:: iexfinance.stock.Share.get_price
.. automethod:: iexfinance.stock.Share.get_delayed_quote
.. automethod:: iexfinance.stock.Share.get_effective_spread
.. automethod:: iexfinance.stock.Share.get_volume_by_venue


.. note:: There is no support for the `list <https://iextrading.com/developer/docs/#list>`__ endpoint at this time.

.. _share-datapoint-methods:

Datapoint Methods
-----------------

.. automethod:: iexfinance.stock.Share.get_company_name
.. automethod:: iexfinance.stock.Share.get_sector
.. automethod:: iexfinance.stock.Share.get_open
.. automethod:: iexfinance.stock.Share.get_close
.. automethod:: iexfinance.stock.Share.get_years_high
.. automethod:: iexfinance.stock.Share.get_years_low
.. automethod:: iexfinance.stock.Share.get_ytd_change
.. automethod:: iexfinance.stock.Share.get_volume
.. automethod:: iexfinance.stock.Share.get_market_cap
.. automethod:: iexfinance.stock.Share.get_beta
.. automethod:: iexfinance.stock.Share.get_short_interest
.. automethod:: iexfinance.stock.Share.get_short_ratio
.. automethod:: iexfinance.stock.Share.get_latest_eps
.. automethod:: iexfinance.stock.Share.get_shares_outstanding
.. automethod:: iexfinance.stock.Share.get_float
.. automethod:: iexfinance.stock.Share.get_eps_consensus

.. _share-parameters:

Parameters
----------

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)

+----------------------+------------------------------------------------------------+-------------+
| Option               | Endpoint                                                   | Default     |
+======================+============================================================+=============+
| ``displayPercent``   | `quote <https://iextrading.com/developer/docs/#quote>`__   | ``False``   |
+----------------------+------------------------------------------------------------+-------------+
| ``_range``            | `chart <https://iextrading.com/developer/docs/#chart>`__   | ``1m``      |
+----------------------+------------------------------------------------------------+-------------+
| ``last``             | `news <https://iextrading.com/developer/docs/#news>`__     | ``10``      |
+----------------------+------------------------------------------------------------+-------------+

.. note:: Due to collisions between the dividends and splits range options that require separate requests and merging. The single _range value specified will apply to the chart, dividends, and splits endpoints. We have contacted IEX about this issue and hope to resolve it soon.


.. _share-examples:

Examples
-----

.. ipython:: python

    from iexfinance import Stock as iex
    tsla = Stock('TSLA')
    print(tsla.get_open())
    print(tsla.get_price())


.. _stocks.Batch:

Batch
=====

.. autoclass:: iexfinance.stock.Batch

``Batch`` acts the same as ``Share``, except it allows us to access data
for up to 100 symbols at once, returning a dictionary of the results
indexed by each symbol.


.. _batch-utility-methods:

Utility Methods
---------------

.. _batch-endpoint-methods:

Endpoint Methods
----------------

.. automethod:: iexfinance.stock.Batch.get_quote
.. automethod:: iexfinance.stock.Batch.get_chart
.. automethod:: iexfinance.stock.Batch.get_book
.. automethod:: iexfinance.stock.Batch.get_open_close
.. automethod:: iexfinance.stock.Batch.get_previous
.. automethod:: iexfinance.stock.Batch.get_company
.. automethod:: iexfinance.stock.Batch.get_key_stats
.. automethod:: iexfinance.stock.Batch.get_relevant
.. automethod:: iexfinance.stock.Batch.get_news
.. automethod:: iexfinance.stock.Batch.get_financials
.. automethod:: iexfinance.stock.Batch.get_earnings
.. automethod:: iexfinance.stock.Batch.get_dividends
.. automethod:: iexfinance.stock.Batch.get_splits
.. automethod:: iexfinance.stock.Batch.get_logo
.. automethod:: iexfinance.stock.Batch.get_price
.. automethod:: iexfinance.stock.Batch.get_delayed_quote
.. automethod:: iexfinance.stock.Batch.get_effective_spread
.. automethod:: iexfinance.stock.Batch.get_volume_by_venue


note: there is no support for the
`list <https://iextrading.com/developer/docs/#list>`__ endpoint at this
time.

.. _batch-datapoint-methods:

Datapoint Methods
-----------------

.. automethod:: iexfinance.stock.Batch.get_company_name
.. automethod:: iexfinance.stock.Batch.get_sector
.. automethod:: iexfinance.stock.Batch.get_open
.. automethod:: iexfinance.stock.Batch.get_close
.. automethod:: iexfinance.stock.Batch.get_years_high
.. automethod:: iexfinance.stock.Batch.get_years_low
.. automethod:: iexfinance.stock.Batch.get_ytd_change
.. automethod:: iexfinance.stock.Batch.get_volume
.. automethod:: iexfinance.stock.Batch.get_market_cap
.. automethod:: iexfinance.stock.Batch.get_beta
.. automethod:: iexfinance.stock.Batch.get_short_interest
.. automethod:: iexfinance.stock.Batch.get_short_ratio
.. automethod:: iexfinance.stock.Batch.get_latest_eps
.. automethod:: iexfinance.stock.Batch.get_shares_outstanding
.. automethod:: iexfinance.stock.Batch.get_float
.. automethod:: iexfinance.stock.Batch.get_eps_consensus

.. _batch-parameters:

Parameters
----------

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)

+----------------------+------------------------------------------------------------+-------------+
| Option               | Endpoint                                                   | Default     |
+======================+============================================================+=============+
| ``displayPercent``   | `quote <https://iextrading.com/developer/docs/#quote>`__   | ``False``   |
+----------------------+------------------------------------------------------------+-------------+
| ``_range``            | `chart <https://iextrading.com/developer/docs/#chart>`__   | ``1m``      |
+----------------------+------------------------------------------------------------+-------------+
| ``last``             | `news <https://iextrading.com/developer/docs/#news>`__     | ``10``      |
+----------------------+------------------------------------------------------------+-------------+

.. note:: Due to collisions between the dividends and splits range options that require separate requests and merging. The single _range value specified will apply to the chart, dividends, and splits endpoints. We have contacted IEX about this issue and hope to resolve it soon.


.. _batch-examples:

Examples
--------

.. ipython:: python

    from iexfinance import Stock as iex
    air_transport = Stock(['AAL', 'DAL', 'LUV'])
    air_transport.get_open()
    air_transport.get_price()
