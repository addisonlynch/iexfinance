## Setting up a new environment

Ideally, before installing or using iexfinance, we'll create a new virtual environment using [virtualenv](https://virtualenv.pypa.io/en/stable/). This will ensure that our packages are isolated from other projects and configured correctly.

```bash
$ virtualenv env
$ source env/bin/activate
```

## Getting started

Once our environment is created, we can now install iexfinance. We do so by the following from iexfinance's pypl repository. 

```bash
(env) $ pip install iexfinance
```

This will install the latest stable release of iexfinance that is ready for use. Once installed, we can import the library and begin downloading data!


### Retrieving Data

iexfinance uses two internal objects, [```Share```](share.md) and [```Batch```](batch.md) to retrieve equities data. [```Share```](share.md) is used for single symbols and uses the ```/stock/<symbolname>``` endpoint from IEX. [```Batch```](https://addisonlynch.github.io/iexfinance/batch), however, uses the  ```market``` endpoint from [Batch Requests](https://iextrading.com/developer/docs/#batch-requests) to conduct the retrieval for multiple symbols. 

#### Single Symbol

We'll first work with the following instantiation:

```python
>>> from iexfinance import IexFinance as iex

>>> aapl = iex("aapl")
```

So, we've called the `IexFinance` function and passed it the symbol "aapl", for Apple Inc. We've receieved a [`Share`](share.md) object in return whose symbol is "aapl." Notice that we have not passed any parameters at instantiation, so our object has used its defaults (see [`Share`](share.md#parameters) for more information). Should we attempt to pass a symbol not contained in the available symbol list (see [Utilities](utilities.md)), an `IEXSymbolError` will be raised:

```python
>>> aapl = iex("aapleee")
# IEXSymbolError: Symbol aapleee not found.
```



At this point, the wrapper has downloaded all avaiable data for Apple Inc., and we can quickly access certain endpoints and datapoints without the overhead of making multiple API calls for the information. We'll first work with the [Quote](https://iextrading.com/developer/docs/#quote) endpoint. The IEX Docs for quote:



We see on the right an exact representation of the Quote endpoint's response, in this case a JSON of various datapoints including "symbol" and "companyName", among others. To retrieve the endpoint as represented, we use the provided *endpoint method* `get_quote`:

```python
>>> aapl.get_quote()
 {
  "symbol": "AAPL",
  "companyName": "Apple Inc.",
  "primaryExchange": "Nasdaq Global Select",
  "sector": "Technology",
  "calculationPrice": "tops",
  "open": 154,
  "openTime": 1506605400394,
  "close": 153.28,
  "closeTime": 15066054
   ...
   }
```

We see that `get_quote` returns the same as the IEX docs! But what if we don't want the entire endpoint? iexfinance provides a number of *datapoint methods* which allow access to specific items within certain endpoints. For instance, we could use `get_open` or `get_company_name` to obtain the relevant information:

```python
>>> aapl.get_open()
124.55

>>> aapl.get_company_name()
"Apple Inc."
```

A full list of the avaiable *datapoint methods* is provided in the [Share](share.md) documentation. In addition to these methods, it is possible to obtain one or more datapoints from a specific endpoint, using the `get_select_datapoints` method, passing the desired endpoint and a *string* or *list* of desired datapoint(s) as below:

```python
>>> aapl.get_select_datapoints("quote", "symbol")
"AAPL"

>>> aapl.get_select_datapoints("quote", ["symbol", "calculationPrice", "open"])
{ "symbol" : "AAPL", "calculationPrice" : "tops", "open" : 154 } 
```

We see that `get_select_datapoints` returns a *dict* of these datapoints, indexed by the keys provided. *Note: the datapoint names must be entered in the exact formatting as the IEX documentation*. If we attempt to select an invalid datapoint, an `IEXDatapointError` will be raised:

```python
>>> aapl.get_select_datapoints("quote", ["symbol", "todaysHigh", "open"])
#IEXDatapointError: Datapoint todaysHigh not found in endpoint quote
```

#### Multiple Symbols

For batch requests, `IexFinance` returns a [`Batch`](batch.md) object, which contains many of the same methods as [`Share`](share.md), but returns data in a *dict* indexed by each symbol provided.

```python
>>> b = iex(["aapl", "tsla"])
>>> b.get_all()
{
  "AAPL" : {
    "quote": {...},
    "news": [...],
    "chart": [...]
    ...
  },
  "TSLA" : {
    "quote": {...},
    "news": [...],
    "chart": [...]
    ...
  },
}
```
We can see that the entire dataset, indexed by "AAPL" and "TSLA", contains each endpoint. To obtain an individual endpoint, we use an *endpoint method* as we would with single symbols:

```python
>>> b.get_quote()

{
  "AAPL" : {
    "symbol": "AAPL",
    "companyName" : "Apple Inc.",
    "primaryExchange" : "Nasdaq Global Select",
    ...
  },
  "FB" : {
    "symbol": "TSLA",
    "companyName" : "Tesla Inc.",
    "primaryExchange" : "Nasdaq Global Select",
    ...
  },
}
```
We see that the response of an *endpoint method* is also symbol-indexed. This remains true for all methods in [`Batch`](batch.md), including *datapoint methods*:

```python
>>> b.get_open()
{ "AAPL" : 154, "TSLA" : 317.44 }
```

Obtaining multiple endpoints or multiple datapoints from a certain endpoint is easy for multiple symbols:

```python

>>> b.get_select_datapoints("quote", ["open", "close"])

{ "AAPL" : {
        "open" : 154,
        "close" : 155.55
        }
  "TSLA" : {
        "open" : 317.44,
        "close" : 314.55
        } 
}
```


#### Updating Data

When we call the `IexFinance` function, the resulting object calls the `refresh` method at instantiation. This method downloads and obtains the latest market data from IEX. Realtime data is updated to the latest 15 minutes, per the IEX documentation. 

```python
>>> aapl.refresh()
```



