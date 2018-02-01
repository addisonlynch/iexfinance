.. _usage:

.. role:: strike

*****
Usage
*****

.. note:: For a thorough, step-by-step walkthrough, see `tutorial <tutorial.html>`__

Overview
==================

The iexfinance codebase and documentation are structured in a way that emulates much of the `IEX API Documentation <https://iextrading.com/developer/docs>`__ for readability and ease of use.

Thus there are four main modules of iexfinance, each allowing the retrieval of data from one of IEX's main endpoint groups:

  - :ref:`Stocks<usage.stocks>`
  - :ref:`Reference Data<usage.reference-data>`
  - :ref:`IEX Market Data<usage.iex-market-data>`
  - :ref:`IEX Stats<usage.iex-stats>`

These modules provide classes and top-level functions to execute queries to the IEX API.


Request Parameters
------------------

All classes and functions utilize the _IEXBASE class to make their requests:

.. autoclass:: iexfinance.base._IEXBase


Caching
-------

iexfinance supports the caching of HTTP requests to IEX using the ``requests-cache`` package.

.. seealso:: `Caching Queries <caching.html>`__

.. _usage.stocks:

Stocks
======

.. seealso:: For more information, see `Stocks <stocks.html>`__.


IEX provides a list of symbols that are available for access, and as
such, we provide a function ``get_available_symbols`` to obtain this
list. Invalid symbols will be met with a ``IEXSymbolError``, and
duplicate symbols will be kept intact without alteration.

Endpoints
---------

The Stock endpoints of the `IEX Developer
API <https://iextrading.com/developer/>`__ are below, each of which
contains data regarding a different aspect of the security/securities.
Both the `Share <stocks.html#share>`__ and `Batch <stocks.html#batch>`__
objects contain identically-signatured functions which can obtain each
of these endpoints. Requests for single symbols (`Share <stocks.html#share>`__)
will return the *exact* results from that endpoint as shown in the IEX API
documentation (see below). Requests for multiple symbols
(`Batch <stocks.html#batch>`__) will return a symbol-indexed dictionary of
the endpoint requested.

*Endpoint Method* Examples ``get_quote()``, ``get_volume_by_venue()``

**Share (single symbol)**

.. ipython:: python

	from iexfinance import Stock
	aapl = Stock("AAPL")
    aapl.get_previous()


For a detailed list of the *endpoint methods*, see
`Share <stocks.html#share>`__ or `Batch <stocks.html#batch>`__.

Fields
------

To obtain individual fields from an endpoint, select *datapoint
methods* are also provided.

Examples ``get_open()``, ``get_name()``

**Share (single symbol)**

.. ipython:: python

    aapl.get_open()
    aapl.get_price()

**Batch (multiple symbols)**

.. ipython:: python

    b = Stock(["AAPL", "TSLA"])
    b.get_open()


For a detailed list of these functions, see `Share <stocks.html#share>`__ or
`Batch <stocks.html#batch>`__.

Parameters
----------

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)


.. note:: Due to collisions between the dividends and splits range options that require separate requests and merging. The single _range value specified will apply to the chart, dividends, and splits endpoints. We have contacted IEX about this issue and hope to resolve it soon.


.. _usage.reference-data:

Reference Data
==============

.. seealso:: For more information, see `Reference Data <ref.html>`__


.. _usage.iex-market-data:


IEX Market Data
===============

.. seealso:: For more information, see `IEX Market Data <market.html>`__

The IEX Market Data `endpoints <market.html>`__


.. _usage.iex-stats:

IEX Stats
=========

.. seealso:: For more information, see `IEX Stats <stats.html>`__

The IEX Stats `endpoints <stats.html>`__