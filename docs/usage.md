# Usage

*Note: for a thorough, step-by-step walkthrough, see [tutorial](tutorial.md).*

The simplest way to obtain data using the iexfinance wrapper is by calling the `IexFinance` function with a symbol (*str*) or list of symbols (*list*). `IexFinance` will return a [```Share```](share.md) object instance if given a single symbol and a [```Batch```](batch.md) object instance if given a list. 

```python
>>> from iexfinance import IexFinance as iex
>>> aapl = iex("aapl")
>>> aapl.get_price()
#171.32
```

IEX provides a list of symbols that are available for access, and as such, we provide a function ```get_available_symbols``` to obtain this list. Invalid symbols will be met with a ```IEXSymbolError```, and duplicate symbols will be kept intact without alteration.

### Endpoints

The Stock endpoints of the [IEX Developer API](https://iextrading.com/developer/) are below, each of which contains data regarding a different aspect of the security/securities. Both the [```Share```](share.md) and [```Batch```](batch.md) objects contain identically-signatured functions which can obtain each of these endpoints. Requests for single symbols ([```Share```](share.md)) will return the *exact* results from that endpoint as shown in the IEX API documentation (see below). Requests for multiple symbols ([```Batch```](batch.md)) will return a symbol-indexed dictionary of the endpoint requested.

- [Quote](https://iextrading.com/developer/docs/#quote)
- [Chart](https://iextrading.com/developer/docs/#chart)
- [Book](https://iextrading.com/developer/docs/#book)
- [Open / Close](https://iextrading.com/developer/docs/#open-close)
- [Previous](https://iextrading.com/developer/docs/#previous)
- [Company](https://iextrading.com/developer/docs/#company)
- [Key Stats](https://iextrading.com/developer/docs/#key-stats)
- [Relevant](https://iextrading.com/developer/docs/#relevant)
- [News](https://iextrading.com/developer/docs/#news)
- [Financials](https://iextrading.com/developer/docs/#financials)
- [Earnings](https://iextrading.com/developer/docs/#earnings)
- [Dividends](https://iextrading.com/developer/docs/#dividends) 
- [Splits](https://iextrading.com/developer/docs/#splits) 
- [Logo](https://iextrading.com/developer/docs/#logo) 
- [Price](https://iextrading.com/developer/docs/#price)
- [Delayed Quote](https://iextrading.com/developer/docs/#delayed-quote)
- ~~List~~ (*not supported*)
- [Effective Spread](https://iextrading.com/developer/docs/#effective-spread)
- [Volume by Venue](https://iextrading.com/developer/docs/#volume-by-venue)


*Endpoint Method* Examples
`get_quote()`, 
`get_volume_by_venue()`



**Share (single symbol)**

```python
>>> aapl.get_previous()

#{"symbol":"AAPL","date":"2017-11-16","open":171.18,"high":171.87,"low":170.3,"close":171.1,
#"volume":23637484,"unadjustedVolume":23637484,"change":2.02,"changePercent":1.195,
#"vwap":171.1673}


```

For a detailed list of the *endpoint methods*, see [```Share```](share.md) or [```Batch```](batch.md). 

### Datapoints

To obtain individual datapoints from an endpoint, select *datapoint methods* are also provided.

Examples
`get_open()`, 
`get_name()`

**Share (single symbol)**

```python
>>> aapl.get_open()
# 111.99
>>> aapl.get_name()
# Apple Inc.


```


**Batch (multiple symbols)**

```python

>>> from iexfinance import IexFinance as iex
>>> b = iex(["AAPL", "TSLA"])
>>> b.get_open()
#{"AAPL" : 111.99, "TSLA" : 299.93}
>>> b.get_open()
#{"AAPL" : "Apple Inc.", "TSLA" : "Tesla Inc."}
```


For a detailed list of these functions, see [```Share```](share.md) or [```Batch```](batch.md).




### Parameters

Certain endpoints (such as quote and chart) allow customizable parameters. To specify one of these parameters, merely pass it as a keyword argument.

```python
aapl = iex("AAPL", displayPercent=True)
```


| Option        | Endpoint         | Default | 
| ------------- |:-------------:| :-----:| 
| ```displayPercent```  | [quote](https://iextrading.com/developer/docs/#quote) | ```False``` | 
| ```chartRange```  | [chart](https://iextrading.com/developer/docs/#chart) | ```1m``` | 
| ```last```  | [news](https://iextrading.com/developer/docs/#news) | ```10``` |
| ```dividendsRange```  | [dividends](https://iextrading.com/developer/docs/#dividends) | ```1m``` |
| ```splitsRange```  | [splits](https://iextrading.com/developer/docs/#splits) | ```1m``` | 

*Note: specifying options other than the defaults will **significantly** impact performance due to collision between the dividends and splits range options that require separate requests and merging. We have contacted IEX about this issue and hope to resolve it soon.*
