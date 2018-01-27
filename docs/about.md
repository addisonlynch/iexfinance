# Filling a Void

It seemed for a number of years that the primary sources of free US equities data for Python developers were the Yahoo Finance and Google Finance APIs. Given that both of these services were [discontinued](https://forums.yahoo.net/t5/Yahoo-Finance-help/Is-Yahoo-Finance-API-broken/td-p/250503) earlier this year, analysts and developers have begun the search for their replacement. A strong contender for live equities data is the [Investors' Exchange](https://iextrading.com) [Developer Platform](https://iextrading.com/developer), a "reliable, enterprise API" that is "free for everyone." 

For those with concerns that the service will not remain reliable and will not
remain free, see below for further discussion. For now, we've benchmarked the
API's performance against that of the late Yahoo and Google services and found
that, for daily and intraday information, the IEX service is actually quite
comparable. And thus with a Python wrapper for IEX's [Stocks]
(https://iextrading.com/developer/docs/#stocks) and [IEX Market Data]
(https://iextrading.com/developer/docs/#iex-market-data) endpoints we can
access this data in a similar way as past. 

iexfinance, a wrapper for this service, is written in a similar fashion as both Lukasz Banasiak's Yahoo Finance wrapper and Hongtao Cai's Google Finance wrapper, allowing for lookup of both individual symbols as well as batch requests. 

I would like to thank [Lukasz Banasiak](https://github.com/lukaszbanasiak) and [Hongtao Cai](https://github.com/hongtaocai) for their inspiration on this project. 