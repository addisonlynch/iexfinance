import sys
from urllib.parse import urlencode
try: 
    import simplejson as json
except ImportError: 
    import json
import requests
from functools import wraps


class IEXSymbolError(Exception):
    """
    This error is thrown when an invalid symbol is given.
    """
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return "Symbol " + self.symbol + " not found."

class IEXEndpointError(Exception):
    """
    This error is thrown when an invalid endpoint is specified in the custom endpoint lookup method
    """
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def __str__(self):
        return "Endpoint " + self.endpoint + " not found."

class IEXDatapointError(Exception):
    """
    This error is thrown when an invalid datapoint is specified in the custom endpoint lookup method
    """
    def __init__(self, endpoint, datapoint):
        self.datapoint = datapoint
        self.endpoint = endpoint

    def __str__(self):
        return "Datapoint " + self.datapoint + " not found in Endpoint " + self.endpoint

class IEXQueryError(Exception):
    """
    This error is thrown when an error occurs with the query to IEX, be it a network problem or an invalid query.
    """
    def __init__(self):
        return "An error occurred while making the query." 


class IEXRetriever(object):
    """
    Base class for retrieving equities information from the IEX Finance API. Inherited by Share and Batch classes, and conducts query operations including preparing and executing queries from the API.
    """
    _ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0//ref-data/symbols"
    _IEX_API_URL = "https://api.iextrading.com/1.0/"
    
    # Possible option values (first is default)
    _CHART_RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m',  '1d', 'date', 'dynamic']
    _DIVIDENDS_RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m']
    _SPLITS_RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m']
    _OUTPUT_FORMAT_VALUES = ['json', 'dataframe']
  
    def __init__(self, key, symbolList, **kwargs):
        """ Initialize the class

        Positional Arguments:
            key: Subclass identifier ("Share" or "Batch")
            symbolList: A nonempty list of symbols

        Keyword Arguments:
            displayPercent: boolean 
            chartRange: The range to use for the chart endpoint. Must be contained in _CHART_RANGE_VALUES 
            dividendsRange: Range to use for the dividends endpoint. Must be contained in _DIVIDENDS_RANGE_VALUES
            splitsRange: Range to use for the splits endpoint. Must be contained in _SPLITS_RANGE_VALUES
            last: Range to use for the "last" attribute of the news endpoint.
            outputFormat: Desired output format for batch requests. Currently only supports JSON
        """
        self.symbolList = list(map(lambda x:x.upper(), symbolList))
        self.displayPercent = kwargs.pop('displayPercent', False)
        self.chartRange = kwargs.pop('chartRange', '1m')
        self.dividendsRange = kwargs.pop('dividendsRange', '1m')
        self.splitsRange = kwargs.pop('splitsRange', '1m')
        self.last = kwargs.pop('last', 10)
        self.outputFormat = kwargs.pop('outputFormat', 'json')
        self._key = key

        # Parameter checking
        if type(self.displayPercent) is not bool:
            raise TypeError("displayPercent must be a boolean value")
        if self.outputFormat not in self._OUTPUT_FORMAT_VALUES:
            raise ValueError("Invalid output format.")
        elif self.chartRange not in self._CHART_RANGE_VALUES:
            raise ValueError("Invalid chart range.")
        elif int(self.last) > 50 or int(self.last) < 1:
            raise ValueError("Invalid news last range. Enter a value between 1 and 50.")
        elif self.splitsRange not in self._SPLITS_RANGE_VALUES:
            raise ValueError("Invalid splits range.")
        elif self.dividendsRange not in self._DIVIDENDS_RANGE_VALUES:
            raise ValueError("Invalid dividends range.")


        self._ENDPOINTS = {
                    "chart" : {"options" : [("range", self.chartRange)]},
                    "quote" : { "options" : [("displayPercent",self.displayPercent)]},
                    "book" : {"options" : None},
                    "open-close" : {"options" : None},
                    "previous" : {"options" : None},
                    "company" : {"options" : None},
                    "stats" : {"options" : None},
                    "peers" : {"options" : None},
                    "relevant" : {"options" : None},
                    "news" : {"options" : [("last", self.last)] },
                    "financials" : {"options" : None},
                    "earnings" : {"options" : None},
                    "dividends" : {"options" : [("range", self.dividendsRange)]},
                    "splits" : {"options" : [("range", self.splitsRange)]},
                    "logo" : {"options" : None},
                    "price" : {"options" : None},
                    "delayed-quote" : {"options" : None},
                    "effective-spread" : {"options" : None},
                    "volume-by-venue" : {"options" : None}
                 }

    def _default_options(self):
     """ Returns true if all parameters are set to default values (as specified in IEX docs), false otherwise"""
     return self.displayPercent == False and self.dividendsRange == '1m' and self.splitsRange == '1m' and self.chartRange == '1m' and self.last == 10

    @staticmethod
    def _validate_response(response):
        """ Ensures response from IEX server is valid. 

        Positional Parameters:
            response: A request object

        """
        if response.text == "Unknown symbol":
            raise IEXSymbolError(self.symbolList[0])

        json_response = response.json()
        if not json_response:
            raise IEXQueryError()
        elif "Error Message" in json_response:
            raise IEXQueryError()
        return json_response

    """ 
    Given a URL, execute HTTP request from IEX server using helper function _api_call()

    Positional Arguments:
        url: A properly-formatted url

    """
    @classmethod
    def _executeIEXQuery(cls, url):
        def _api_call(cls, url):
            try:
                r = requests.get(url=url)
                r.raise_for_status
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.TooManyRedirects:
                pass
            except requests.exceptions.RequestException as e:
                pass
            return cls._validate_response(r)
        return _api_call(cls, url)

    @classmethod
    def _output_format(cls, func):
        """ A decorator function which formats the output based on the output_format attribute which is selected at instantiation of the class. 

        Positional Arguments:
            func: A function to be wrapped

        """
        @wraps(func)
        def _format_wrapper(self, *args, **kwargs):
            response = func( 
                self, *args, **kwargs) # type dict
            outform = self.outputFormat 
            if outform == 'json':
                return response
            elif outform == 'pandas':
                data_pandas = pandas.DataFrame.from_dict(data,
                                                         orient='index',
                                                         dtype=float)
                return data_pandas
            else:
                raise ValueError('Format: {} is not supported'.format(
                    outform))
        return _format_wrapper

    def _prepare_query(self, endpoints, options=""):
        """ Creates a url for a Share or a Batch object to use as a query string to the IEX API. Takes the endpoints specified and converts them to a URL.

        Positional Arguments:
            endpoints: The list of endpoints desired
            options: Any and all options values to be specified

        """
        if self._key == "Batch" :
            endpoints = ','.join(endpoints)
            symbols = ','.join(self.symbolList)
            url = ("{0}{1}?symbols={2}&types={3}&{4}".format(self._IEX_API_URL, self.IEX_ENDPOINT_NAME, symbols, endpoints, options))
        elif self._key == "Share" :
            endpoints = ','.join(endpoints)
            url = ("{0}{1}?&types={2}&{3}".format(self._IEX_API_URL, self.IEX_ENDPOINT_NAME, endpoints, options))
        return url

    def _fetch_default_options(self):
        """
        Conducts the IEX query when default options are specified. Returns IEXQueryError if problems arise.
        """
        data_set = dict.fromkeys(self.symbolList, {})
        eps = list(self._ENDPOINTS.keys())
        query = self._prepare_query(eps)
        response = self._executeIEXQuery(query)
        if self._key == "Share":
            response = {self.symbol : response}
        for symbol in self.symbolList:
            try:
                diff = set(self._ENDPOINTS) - set(response[symbol]) 
            except:
                raise IEXSymbolError(symbol)  
            if set(response[symbol]) != set(self._ENDPOINTS):
                raise ValueError("Not all endpoints downloaded")
        return response 

    def _fetch(self):
        """
        Conducts the IEX query when custom options are specified. This function msut conduct the query using individual endpoints, one at a time, as the IEX API has colliding parameters between the ranges for chart, dividends, and splits. We have contacted them about this issue. Will return IEXQueryError if problems arise.
        """
        if self._default_options():
            return self._fetch_default_options()
        else:
            data_set = dict.fromkeys(self.symbolList, {})
            norms = [endpoint for endpoint in self._ENDPOINTS if self._ENDPOINTS[endpoint]["options"] == None ]
            opts = set(self._ENDPOINTS) - set(norms)

            # fetch endpoints with no options
            nquery = self._prepare_query(norms)
            nresponse = self._executeIEXQuery(nquery)
            #update the data set
            for symbol in self.symbolList:
                try:
                    if self._key == "Batch":
                        data_set[symbol].update(nresponse[symbol])
                    else:
                        data_set[symbol].update(nresponse)
                except:
                    raise IEXSymbolError(symbol)


        # fetch endpoints with options
        for endpoint in opts:
            options = urlencode(self._ENDPOINTS[endpoint]["options"])
            oquery = self._prepare_query([endpoint], options)
            oresponse = self._executeIEXQuery(oquery)
        #update the dataset
            for symbol in self.symbolList:
                try:
                    if self._key == "Batch":
                        data_set[symbol].update(oresponse[symbol])
                    else:
                        data_set[symbol].update(oresponse)
                except:
                    raise IEXSymbolError(symbol)
                diff = set(self._ENDPOINTS) - set(data_set[symbol])
                for item in diff:
                    data_set[symbol].update({item: []})
                if set(data_set[symbol]) != set(self._ENDPOINTS):
                    raise ValueError("Not all endpoints downloaded")
        return data_set




