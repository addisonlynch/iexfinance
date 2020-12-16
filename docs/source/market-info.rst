.. _market-info:

.. currentmodule:: iexfinance

Market Info
===========

Overview
--------

.. _market-info.endpoint-list:

List of Endpoints
~~~~~~~~~~~~~~~~~

- :ref:`Collections<market-info.collections>` - ``get_collections``
- :ref:`Earnings Today<market-info.earnings_today>` - ``get_earnings_today``
- :ref:`IPO Calendar<market-info.ipo_calendar>`
- :ref:`List<market-info.list>`
- :ref:`Market Volume<market-info.market_volume>` - ``get_market_volume``
- :ref:`Sector Performance<market-info.sector>` - ``get_sector_performance``


.. _market-info.collections:

Collections
-----------

The `Collections <https://iexcloud.io/docs/api/#historical-daily>`__
endpoint of Stocks allows retrieval of certain groups of companies, organized
by:

- sector
- tag
- list (see the :ref:`list endpoint <market-info.list>`)

Use ``get_collections`` to access.


.. autofunction:: iexfinance.stocks.get_collections


.. _market-info.collections.examples:

Examples
~~~~~~~~

.. NOTE: These were converted to code-block as they are currently returning
         errors

**Tag**

.. code-block:: python

    from iexfinance.stocks import get_collections

    get_collections("Computer Hardware", output_format='pandas').head()

**Sector**

.. code-block:: python

    get_collections("Industrials", output_format='pandas').head()


.. _market-info.earnings_today:

Earnings Today
--------------

.. warning:: Beginning December 1, 2020, use of this endpoint will require 
             additional entitlements. Full details can be found in the 
             IEX Cloud Help Center. See `here <https://intercom.help/iexcloud/en/articles/4529082-iex-cloud-s-2020-data-upgrade>`_
             for additional information.

.. warning:: ``get_todays_earnings`` has been deprecated and renamed
            ``get_earnings_today``.

Earnings Today was added to the Stocks endpoints in 2018. Access is provided
through the  ``get_earnings_today`` function.


.. autofunction:: iexfinance.stocks.get_earnings_today


.. note:: ``get_earnings_today`` supports JSON output formatting only.


.. _market-info.earnings.examples:

Examples
~~~~~~~~

.. ipython:: python

    from iexfinance.stocks import get_earnings_today

    get_earnings_today()["bto"]

.. _market-info.ipo_calendar:

IPO Calendar
------------

IPO Calendar was added to the Stocks endpoints in 2018. Access is provided
through the  ``get_ipo_calendar`` function.

.. autofunction:: iexfinance.stocks.get_ipo_calendar

There are two possible values for the ``period`` parameter, of which
``upcoming-ipos`` is the default. ``today-ipos`` is also available.

..  _market-info.ipo_calendar.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.stocks import get_ipo_calendar

    get_ipo_calendar()

.. _market-info.list:

List
----
.. seealso:: :ref:`Market Movers<stocks.movers>`

.. _market-info.market_volume:

Market Volume (U.S)
-------------------

Market Volume returns real-time traded volume on U.S. Markets. Access is
provided through the ``get_market_volume`` function.


.. autofunction:: iexfinance.stocks.get_market_volume


.. _market-info.market_volume.examples:

Examples
~~~~~~~~

.. code-block:: python

    from iexfinance.stocks import get_market_volume

    get_market_volume()


.. _market-info.sector:

Sector Performance
------------------

Sector Performance was added to the Stocks endpoints in 2018. Access to this endpoint is provided through the ``get_sector_performance`` function.

.. autofunction:: iexfinance.stocks.get_sector_performance
