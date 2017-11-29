# Batch

`Batch` acts the same as `Share`, except it allows us to access data for up to 100 symbols at once, returning a dictionary of the results indexed by each symbol.

```python
Batch(symbolList=[], output_format='json', displayPercent=False, chartRange='1m', last='10', dividendsRange='1m', splitsRange='1m'):
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
| ```chartRange```  | [chart](https://iextrading.com/developer/docs/#chart) | ```1m``` | 
| ```last```  | [news](https://iextrading.com/developer/docs/#news) | ```10``` |
| ```dividendsRange```  | [dividends](https://iextrading.com/developer/docs/#dividends) | ```1m``` |
| ```splitsRange```  | [splits](https://iextrading.com/developer/docs/#splits) | ```1m``` | 




### Examples

```python
>>> from iexfinance import IexFinance as iex
>>> air_transport = iex(['AAL', 'DAL', 'LUV'])
>>> print(air_transport.get_open())
{'AAL' : 299.64, 'DAL' : 49.08, 'LUV' : 0.33}
>>> print(air_transport.get_price())
{'AAL' : 222.33, 'DAL' : 5.25, 'LUV' : 0.23}
```