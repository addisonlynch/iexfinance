# Caching Queries

In some cases it is sensible to cache queries to avoid overloading the IEX
servers. ```iexfinance``` supports the caching of queries through
```requests_cache_```.

## Tutorial

Install ```requests-cache``` using pip:

```bash
>>> pip install requests-cache
```

To use a cached session, pass a ```requests_cache.Session``` object to the
top-level function you are using:

```python
>>> from datetime import timedelta
>>> from iexfinance import IexFinance as iex
>>> import requests-cache
>>>
>>> expiry = datetime.timedelta(days=3)
>>> session = requests-cache.CachedSession(cache_name='cache',
	backend='sqllite', expire_after=expiry)
>>>
>>> f = iex("AAPL", session=session)
```

A [SQLite](https://www.sqlite.org/) file named ```cache.sqlite``` will be
created in the working directory, storing the request until the expiry date.

For more information about ```requests-cache```, see its [Documentation] 
(https://readthedocs.org/projects/requests-cache/). 

*Caching mechanism similar to [Pandas Datareader]
(https://pandas-datareader.readthedocs.io/en/latest/cache.html).* 