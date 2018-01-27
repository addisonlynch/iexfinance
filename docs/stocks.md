# Share


```python
Share(symbol, displayPercent=False, last=10, range='1m'):
```




### Endpoint Methods

| Method        | Options         | Return Type | Description / Endpoint |
| ------------- |:-------------:| :-----:| :--------: |
| ``` refresh ```  | - | - | Updates market data | 
| **Universal Selectors**
| ``` get_all ```  | - | json | Returns JSON of all endpoints | 
| ``` get_select_endpoints ```    | module (string) | varies | Returns selected  endpoint|
|                      **Individual Endpoints**                         |
| ``` get_quote ```  | displayPercent| json | [Quote](https://iextrading.com/developer/docs/#quote) | 
| ``` get_chart ```    | - | list | [Chart](https://iextrading.com/developer/docs/#chart)|
| ``` get_book ```   | - | json | [Book](https://iextrading.com/developer/docs/#book) |
| ``` get_open_close ```  | - | json | [Open / Close](https://iextrading.com/developer/docs/#open-close) | 
| ``` get_previous ```    | - | json | [Previous](https://iextrading.com/developer/docs/#previous) |
| ``` get_company ```   | - | json | [Company](https://iextrading.com/developer/docs/#company) |
| ``` get_key_stats ```  | - | json | [Key Stats](https://iextrading.com/developer/docs/#key-stats) | 
| ``` get_relevant ```    | - | json | [Relevant](https://iextrading.com/developer/docs/#relevant) |
| ``` get_news ```   | last | list | [News](https://iextrading.com/developer/docs/#news) |
| ``` get_financials ```  | - | json | [Financials](https://iextrading.com/developer/docs/#financials) | 
| ``` get_earnings ```    | - | json | [Earnings](https://iextrading.com/developer/docs/#earnings) |
| ``` get_dividends ```  | range | json | [Dividends](https://iextrading.com/developer/docs/#dividends) 
| ``` get_splits ```  | range | json | [Splits](https://iextrading.com/developer/docs/#splits) 
| ``` get_logo ```   | - | json | [Logo](https://iextrading.com/developer/docs/#logo) |
| ``` get_price ```   | - | float | [Price](https://iextrading.com/developer/docs/#price) |
| ``` get_delayed_quote ```   | - | json | [Delayed Quote](https://iextrading.com/developer/docs/#delayed-quote) |
| ``` get_effective_spread ```   | - | list | [Effective Spread](https://iextrading.com/developer/docs/#effective-spread) |
| ``` get_volume_by_venue ```   | - | list | [Volume by Venue](https://iextrading.com/developer/docs/#volume-by-venue) |

Note: there is no support for the [list](https://iextrading.com/developer/docs/#list) endpoint at this time.

### Datapoint Methods

| Method        | Options         | Return Type | Description |
| ------------- |:-------------:| :-----:| -------- |
| **Universal Selectors**
| ``` get_select_datapoints ``` | endpoint (string), datapoints (list) | json | Returns selected data point from selected endpoint
| 
|                      **Individual Datapoints**                         |
| ``` get_company_name ```  	| - | string | |
| ``` get_primary_exchange ```  | - | string | |
| ``` get_sector ```   			| - | string |  |
| ``` get_open ```  			| - | float |  | 
| ``` get_close ```    			| - | float | |
| ``` get_years_high ```   		| - | float |  |
| ``` get_years_low ```  		| - | float |  | 
| ``` get_ytd_change ```    	| - | float | |
| ``` get_volume ```   			| - | int |  |
| ``` get_market_cap ```  		| - | int |  | 
| ``` get_beta ```    			| - | float | |
| ``` get_short_interest ```   	| - | int |  |
| ``` get_short_ratio ```   	| - | float |  |
| ``` get_latest_eps ```   		| - | float |  |
| ``` get_shares_outstanding ```| - | int  |  |
| ``` get_float ```   			| - | int |  |
| ``` get_eps_consensus ```   	| - | float |  |


### Parameters

Certain endpoints (such as quote and chart) allow customizable parameters. To specify one of these parameters, merely pass it as a keyword argument.

```python
aapl = iex("AAPL", displayPercent=True)
```


| Option        | Endpoint         | Default | 
| ------------- |:-------------:| :-----:| 
| ```displayPercent```  | [quote](https://iextrading.com/developer/docs/#quote) | ```False``` | 
| ```range```  | [chart](https://iextrading.com/developer/docs/#chart) | ```1m``` | 
| ```last```  | [news](https://iextrading.com/developer/docs/#news) | ```10``` |



### Examples

```python
>>> from iexfinance import IexFinance as iex
>>> tsla = iex('TSLA')
>>> print(tsla.get_open())
'299.64'
>>> print(tsla.get_price())
'301.84'
```




# Batch

`Batch` acts the same as `Share`, except it allows us to access data for up to 100 symbols at once, returning a dictionary of the results indexed by each symbol.

```python
Batch(symbolList=[], displayPercent=False, range='1m', last='10'):
```


### Utility Methods

| Method        | Options         | Return Type | Description |
| ------------- |:-------------:| :-----:| -------- |
| ```refresh ```  | - | - | Update market data | 

### Endpoint Methods

| Method        | Options         | Return Type | Endpoint Name |
| ------------- |:-------------:| :-----:| :--------: |
| **Universal Selectors**
| ``` get_all ```  | - | json | Returns JSON of all endpoints | 
| ``` get_select_endpoints ```    | module (string) | json | Returns selected  endpoint|
|                      **Individual Endpoints**                         |
| ``` get_quote ```  | displayPercent| json | [Quote](https://iextrading.com/developer/docs/#quote) | 
| ``` get_chart ```    | - | json | [Chart](https://iextrading.com/developer/docs/#chart)|
| ``` get_book ```   | - | json | [Book](https://iextrading.com/developer/docs/#book) |
| ``` get_open_close ```  | - | json | [Open / Close](https://iextrading.com/developer/docs/#open-close) | 
| ``` get_previous ```    | - | json | [Previous](https://iextrading.com/developer/docs/#previous) |
| ``` get_company ```   | - | json | [Company](https://iextrading.com/developer/docs/#company) |
| ``` get_key_stats ```  | - | json | [Key Stats](https://iextrading.com/developer/docs/#key-stats) | 
| ``` get_relevant ```    | - | json | [Relevant](https://iextrading.com/developer/docs/#relevant) |
| ``` get_news ```   | last | json | [News](https://iextrading.com/developer/docs/#news) |
| ``` get_financials ```  | - | json | [Financials](https://iextrading.com/developer/docs/#financials) | 
| ``` get_earnings ```    | - | json | [Earnings](https://iextrading.com/developer/docs/#earnings) |
| ``` get_dividends ```  | range | json | [Dividends](https://iextrading.com/developer/docs/#dividends) 
| ``` get_splits ```  | range | json | [Splits](https://iextrading.com/developer/docs/#splits) 
| ``` get_logo ```   | - | json | [Logo](https://iextrading.com/developer/docs/#logo) |
| ``` get_price ```   | - | json | [Price](https://iextrading.com/developer/docs/#price) |
| ``` get_delayed_quote ```   | - | json | [Delayed Quote](https://iextrading.com/developer/docs/#delayed-quote) |
| ``` get_effective_spread ```   | - | json | [Effective Spread](https://iextrading.com/developer/docs/#effective-spread) |
| ``` get_volume_by_venue ```   | - | json | [Volume by Venue](https://iextrading.com/developer/docs/#volume-by-venue) |

note: there is no support for the [list](https://iextrading.com/developer/docs/#list) endpoint at this time.

### Datapoint Methods

| Method        | Options         | Return Type | Description |
| ------------- |:-------------:| :-----:| :--------: |
| **Universal Selectors**
| ``` get_select_datapoints ``` | endpoint (string), datapoints (list) | json | Returns selected datapoint from selected endpoint
|                      **Individual Datapoints**   
| ``` get_company_name ```  	| - | json | - |
| ``` get_primary_exchange ```  | - | json |- |
| ``` get_sector ```   			| - | json | - |
| ``` get_open ```  			| - | json | - | 
| ``` get_close ```    			| - | json |- |
| ``` get_years_high ```   		| - | json | - |
| ``` get_years_low ```  		| - | json | - | 
| ``` get_ytd_change ```    	| - | json |- |
| ``` get_volume ```   			| - | json | - |
| ``` get_market_cap ```  		| - | json | - | 
| ``` get_beta ```    			| - | json |- |
| ``` get_short_interest ```   	| - | json | - |
| ``` get_short_ratio ```   	| - | json | - |
| ``` get_latest_eps ```   		| - | json | - |
| ``` get_shares_outstanding ```| - | json  | - |
| ``` get_float ```   			| - | json | - |
| ``` get_eps_consensus ```   	| - | json | - |



### Parameters

Certain endpoints (such as quote and chart) allow customizable parameters. To specify one of these parameters, merely pass it as a keyword argument.

```python
aapl = iex("AAPL", displayPercent=True)
```


| Option        | Endpoint         | Default | 
| ------------- |:-------------:| :-----:| 
| ```displayPercent```  | [quote](https://iextrading.com/developer/docs/#quote) | ```False``` | 
| ```range```  | [chart](https://iextrading.com/developer/docs/#chart) | ```1m``` | 
| ```last```  | [news](https://iextrading.com/developer/docs/#news) | ```10``` |




### Examples

```python
>>> from iexfinance import IexFinance as iex
>>> air_transport = iex(['AAL', 'DAL', 'LUV'])
>>> print(air_transport.get_open())
{'AAL' : 299.64, 'DAL' : 49.08, 'LUV' : 0.33}
>>> print(air_transport.get_price())
{'AAL' : 222.33, 'DAL' : 5.25, 'LUV' : 0.23}
```