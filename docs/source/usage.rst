.. _usage:


*****
Usage
*****


.. _usage.stocks:

Stocks
------

*Note: for a thorough, step-by-step walkthrough, see
`tutorial <tutorial.md>`__.*

The simplest way to obtain data using the iexfinance wrapper is by
calling the ``Stock`` function with a symbol (*str*) or list of
symbols (*list*). ``Stock`` will return a ```Share`` <share.md>`__
object instance if given a single symbol and a ```Batch`` <batch.md>`__
object instance if given a list.

.. ipython:: python

    from iexfinance import IexFinance as iex
    aapl = Stock("aapl")
    aapl.get_price()


IEX provides a list of symbols that are available for access, and as
such, we provide a function ``get_available_symbols`` to obtain this
list. Invalid symbols will be met with a ``IEXSymbolError``, and
duplicate symbols will be kept intact without alteration.

**Endpoints**

The Stock endpoints of the `IEX Developer
API <https://iextrading.com/developer/>`__ are below, each of which
contains data regarding a different aspect of the security/securities.
Both the ```Share`` <share.md>`__ and ```Batch`` <batch.md>`__ objects
contain identically-signatured functions which can obtain each of these
endpoints. Requests for single symbols (```Share`` <share.md>`__) will
return the *exact* results from that endpoint as shown in the IEX API
documentation (see below). Requests for multiple symbols
(```Batch`` <batch.md>`__) will return a symbol-indexed dictionary of
the endpoint requested.

-  `Quote <https://iextrading.com/developer/docs/#quote>`__
-  `Chart <https://iextrading.com/developer/docs/#chart>`__
-  `Book <https://iextrading.com/developer/docs/#book>`__
-  `Open / Close <https://iextrading.com/developer/docs/#open-close>`__
-  `Previous <https://iextrading.com/developer/docs/#previous>`__
-  `Company <https://iextrading.com/developer/docs/#company>`__
-  `Key Stats <https://iextrading.com/developer/docs/#key-stats>`__
-  `Relevant <https://iextrading.com/developer/docs/#relevant>`__
-  `News <https://iextrading.com/developer/docs/#news>`__
-  `Financials <https://iextrading.com/developer/docs/#financials>`__
-  `Earnings <https://iextrading.com/developer/docs/#earnings>`__
-  `Dividends <https://iextrading.com/developer/docs/#dividends>`__
-  `Splits <https://iextrading.com/developer/docs/#splits>`__
-  `Logo <https://iextrading.com/developer/docs/#logo>`__
-  `Price <https://iextrading.com/developer/docs/#price>`__
-  `Delayed
   Quote <https://iextrading.com/developer/docs/#delayed-quote>`__
-  [STRIKEOUT:List] (*not supported*)
-  `Effective
   Spread <https://iextrading.com/developer/docs/#effective-spread>`__
-  `Volume by
   Venue <https://iextrading.com/developer/docs/#volume-by-venue>`__

*Endpoint Method* Examples ``get_quote()``, ``get_volume_by_venue()``

**Share (single symbol)**

.. ipython:: python

    aapl.get_previous()


For a detailed list of the *endpoint methods*, see
```Share`` <share.md>`__ or ```Batch`` <batch.md>`__.

**Datapoints**

To obtain individual datapoints from an endpoint, select *datapoint
methods* are also provided.

Examples ``get_open()``, ``get_name()``

**Share (single symbol)**

.. ipython:: python

    aapl.get_open()
    aapl.get_name()

**Batch (multiple symbols)**

.. ipython:: python

    b = Stock(["AAPL", "TSLA"])
    b.get_open()


For a detailed list of these functions, see ```Share`` <share.md>`__ or
```Batch`` <batch.md>`__.

**Parameters**

Certain endpoints (such as quote and chart) allow customizable
parameters. To specify one of these parameters, merely pass it as a
keyword argument.

.. ipython:: python

    aapl = Stock("AAPL", displayPercent=True)

+----------------------+--------------------------------------------------------------------+-------------+
| Option               | Endpoint                                                           | Default     |
+======================+====================================================================+=============+
| ``displayPercent``   | `quote <https://iextrading.com/developer/docs/#quote>`__           | ``False``   |
+----------------------+--------------------------------------------------------------------+-------------+
| ``chartRange``       | `chart <https://iextrading.com/developer/docs/#chart>`__           | ``1m``      |
+----------------------+--------------------------------------------------------------------+-------------+
| ``last``             | `news <https://iextrading.com/developer/docs/#news>`__             | ``10``      |
+----------------------+--------------------------------------------------------------------+-------------+
| ``dividendsRange``   | `dividends <https://iextrading.com/developer/docs/#dividends>`__   | ``1m``      |
+----------------------+--------------------------------------------------------------------+-------------+
| ``splitsRange``      | `splits <https://iextrading.com/developer/docs/#splits>`__         | ``1m``      |
+----------------------+--------------------------------------------------------------------+-------------+

*Note: specifying options other than the defaults will **significantly**
impact performance due to collision between the dividends and splits
range options that require separate requests and merging. We have
contacted IEX about this issue and hope to resolve it soon.*

IEX Market Data
---------------

IEX Stats
---------
