.. _market-info:

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

The `Collections <https://iextrading.com/developer/docs/#collections>`__
endpoint of Stocks allows retrieval of certain groups of companies, organized
by:

- sector
- tag
- list (see the :ref:`list endpoint <market-info.list>`)

Use ``get_collections`` to access.


.. autofunction:: iexfinance.market-info.get_collections


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

.. warning:: ``get_todays_earnings`` has been deprecated and renamed
            ``get_earnings_today``.

Earnings Today was added to the Stocks endpoints in 2018. Access is provided
through the  ``get_earnings_today`` function.


.. autofunction:: iexfinance.market-info.get_earnings_today


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

.. autofunction:: iexfinance.market-info.get_ipo_calendar

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
.. seealso:: :ref:`Market Movers<market-info.movers>`

.. _market-info.market_volume:

Market Volume (U.S)
-------------------

Market Volume returns real-time traded volume on U.S. Markets. Access is
provided through the ``get_market_volume`` function.


.. autofunction:: iexfinance.market-info.get_market_volume


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

.. autofunction:: iexfinance.market-info.get_sector_performance
