## TOPS

TOPS is IEX's aggregated best quoted bid and offer position in near real time.

Access is available through the top-level function ```get_tops()```:

```python
get_tops(symbol, outputFormat='json', session=None)
```

### Usage

```python
>>> from iexfinance import get_TOPS
>>>
>>> get_TOPS('AAPL')
# [{'time': 1516395598645, 'symbol': 'AAPL', 'size': 100, 'price': 178.45}]

```

## Last

```python
get_Last(symbol, outputFormat='json', session=None)
```

### Usage

```python
>>> from iexfinance import get_TOPS
>>> import pandas as pd
>>>
```

## DEEP

```python
get_DEEP(symbol, outputFormat='json', session=None)
```

DEEP is IEX's aggregated real-time depth of book quotes. DEEP also provides 
last trade price and size information


### Usage

```python
>>> from iexfinance import get_TOPS
>>> import pandas as pd
>>>
```
## Book

```python
get_Book(symbol, outputFormat='json', session=None)
```


### Usage

```python
>>> from iexfinance import get_TOPS
>>> import pandas as pd
>>>
```