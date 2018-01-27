# Reference Data



### All available symbols

From the [IEX API Docs](https://iextrading.com/developer/docs/#stocks):

> Use the /ref-data/symbols endpoint to find the symbols that we support.

In ```iexfinance``` we provide the method ```get_available_symbols``` which accesses this endpoint. This method returns a list of dictionary objects for each symbol, indexed by the key "symbol".


#### Example


```python
from iexfinance import get_available_symbols

data = get_available_symbols()

# {"symbol":"A","name":"Agilent Technologies Inc.","date":"2017-11-27","isEnabled":true,"type":"cs","iexId":"2"}...

```