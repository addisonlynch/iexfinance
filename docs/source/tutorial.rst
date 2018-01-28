.. _tutorial:

********
Tutorial
********

Setting up a new environment
----------------------------

Ideally, before installing or using iexfinance, we'll create a new
virtual environment using
`virtualenv <https://virtualenv.pypa.io/en/stable/>`__. This will ensure
that our packages are isolated from other projects and configured
correctly.

.. code:: bash

    $ virtualenv env
    $ source env/bin/activate

Getting started
---------------

Once our environment is created, we can now install iexfinance. We do so
by the following from iexfinance's pypl repository.

.. code:: bash

    (env) $ pip install iexfinance

This will install the latest stable release of iexfinance that is ready
for use. Once installed, we can import the library and begin downloading
data!

Retrieving Data
~~~~~~~~~~~~~~~

iexfinance uses two internal objects, ```Share`` <share.md>`__ and
```Batch`` <batch.md>`__ to retrieve equities data.
```Share`` <share.md>`__ is used for single symbols and uses the
``/stock/<symbolname>`` endpoint from IEX.
```Batch`` <https://addisonlynch.github.io/iexfinance/batch>`__,
however, uses the ``market`` endpoint from `Batch
Requests <https://iextrading.com/developer/docs/#batch-requests>`__ to
conduct the retrieval for multiple symbols.

Single Symbol
^^^^^^^^^^^^^

We'll first work with the following instantiation:

.. ipython:: python

    from iexfinance import IexFinance as iex
    aapl = Stock("aapl")

So, we've called the ``IexFinance`` function and passed it the symbol
"aapl", for Apple Inc. We've receieved a ```Share`` <share.md>`__ object
in return whose symbol is "aapl." Notice that we have not passed any
parameters at instantiation, so our object has used its defaults (see
```Share`` <share.md#parameters>`__ for more information). Should we
attempt to pass a symbol not contained in the available symbol list (see
`Utilities <utilities.md>`__), an ``IEXSymbolError`` will be raised:

.. ipython:: python

    aapl = Stock("aapleee")

At this point, the wrapper has downloaded all avaiable data for Apple
Inc., and we can quickly access certain endpoints and datapoints without
the overhead of making multiple API calls for the information. We'll
first work with the
`Quote <https://iextrading.com/developer/docs/#quote>`__ endpoint. The
IEX Docs for quote:

We see on the right an exact representation of the Quote endpoint's
response, in this case a JSON of various datapoints including "symbol"
and "companyName", among others. To retrieve the endpoint as
represented, we use the provided *endpoint method* ``get_quote``:

.. ipython:: python

    aapl.get_quote()

We see that ``get_quote`` returns the same as the IEX docs! But what if
we don't want the entire endpoint? iexfinance provides a number of
*datapoint methods* which allow access to specific items within certain
endpoints. For instance, we could use ``get_open`` or
``get_company_name`` to obtain the relevant information:

.. ipython:: python

    aapl.get_open()

    aapl.get_company_name()

A full list of the avaiable *datapoint methods* is provided in the
`Share <share.md>`__ documentation. In addition to these methods, it is
possible to obtain one or more datapoints from a specific endpoint,
using the ``get_select_datapoints`` method, passing the desired endpoint
and a *string* or *list* of desired datapoint(s) as below:

.. ipython:: python

    aapl.get_select_datapoints("quote", "symbol")

    aapl.get_select_datapoints("quote", ["symbol", "calculationPrice", "open"])

We see that ``get_select_datapoints`` returns a *dict* of these
datapoints, indexed by the keys provided. *Note: the datapoint names
must be entered in the exact formatting as the IEX documentation*. If we
attempt to select an invalid datapoint, an ``IEXDatapointError`` will be
raised:

.. ipython:: python

    aapl.get_select_datapoints("quote", ["symbol", "todaysHigh", "open"])

Multiple Symbols
^^^^^^^^^^^^^^^^

For batch requests, ``IexFinance`` returns a ```Batch`` <batch.md>`__
object, which contains many of the same methods as
```Share`` <share.md>`__, but returns data in a *dict* indexed by each
symbol provided.

.. ipython:: python

    b = Stock(["aapl", "tsla"])
    b.get_all()


We can see that the entire dataset, indexed by "AAPL" and "TSLA",
contains each endpoint. To obtain an individual endpoint, we use an
*endpoint method* as we would with single symbols:

.. ipython:: python

    b.get_quote()



We see that the response of an *endpoint method* is also symbol-indexed.
This remains true for all methods in ```Batch`` <batch.md>`__, including
*datapoint methods*:

.. ipython:: python

    b.get_open()

Obtaining multiple endpoints or multiple datapoints from a certain
endpoint is easy for multiple symbols:

.. ipython:: python


    b.get_select_datapoints("quote", ["open", "close"])

Updating Data
^^^^^^^^^^^^^

When we call the ``IexFinance`` function, the resulting object calls the
``refresh`` method at instantiation. This method downloads and obtains
the latest market data from IEX. Realtime data is updated to the latest
15 minutes, per the IEX documentation.

.. ipython:: python

    aapl.refresh()
