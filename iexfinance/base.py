from functools import wraps
from urllib.parse import urlencode

import requests

import pandas

from iexfinance.utils.exceptions import IEXSymbolError, IEXDatapointError, IEXEndpointError, IEXQueryError


class _IEXBase(object):
    """
    Base class for retrieving equities information from the IEX Finance API. Inherited by Share and Batch classes, and conducts query operations including preparing and executing queries from the API.
    """
    # Base URL
    _IEX_API_URL = "https://api.iextrading.com/1.0/"

    # Possible option values (first is default)
    _CHART_RANGE_VALUES = ['1m', '5y', '2y', '1y',
                           'ytd', '6m', '3m', '1d', 'date', 'dynamic']
    _DIVIDENDS_RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m']
    _SPLITS_RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m']
    _OUTPUT_FORMAT_VALUES = ['json', 'pandas']

    def __init__(self, symbolList, **kwargs):
        """ Initialize the class

        Positional Arguments:
            symbolList: A nonempty list of symbols

        Keyword Arguments:
            displayPercent: boolean
            chartRange: The range to use for the chart endpoint. Must be contained in _CHART_RANGE_VALUES
            dividendsRange: Range to use for the dividends endpoint. Must be contained in _DIVIDENDS_RANGE_VALUES
            splitsRange: Range to use for the splits endpoint. Must be contained in _SPLITS_RANGE_VALUES
            last: Range to use for the "last" attribute of the news endpoint.
            outputFormat: Desiredr output format for batch requests. Currently only supports JSON
        """
        self.symbolList = list(map(lambda x: x.upper(), symbolList))
        self.displayPercent = kwargs.pop('displayPercent', False)
        self.chartRange = kwargs.pop('chartRange', '1m')
        self.dividendsRange = kwargs.pop('dividendsRange', '1m')
        self.splitsRange = kwargs.pop('splitsRange', '1m')
        self.last = kwargs.pop('last', 10)
        self.outputFormat = kwargs.pop('outputFormat', 'json')

        # Parameter checking
        if not isinstance(self.displayPercent, bool):
            raise TypeError("displayPercent must be a boolean value")
        if self.outputFormat not in self._OUTPUT_FORMAT_VALUES:
            raise ValueError("Invalid output format.")
        elif self.chartRange not in self._CHART_RANGE_VALUES:
            raise ValueError("Invalid chart range.")
        elif int(self.last) > 50 or int(self.last) < 1:
            raise ValueError(
                "Invalid news last range. Enter a value between 1 and 50.")
        elif self.splitsRange not in self._SPLITS_RANGE_VALUES:
            raise ValueError("Invalid splits range.")
        elif self.dividendsRange not in self._DIVIDENDS_RANGE_VALUES:
            raise ValueError("Invalid dividends range.")

        self._ENDPOINTS = {
            "chart": {"options": [("range", self.chartRange)]},
            "quote": {"options": [("displayPercent", self.displayPercent)]},
            "book": {"options": None},
            "open-close": {"options": None},
            "previous": {"options": None},
            "company": {"options": None},
            "stats": {"options": None},
            "peers": {"options": None},
            "relevant": {"options": None},
            "news": {"options": [("last", self.last)]},
            "financials": {"options": None},
            "earnings": {"options": None},
            "dividends": {"options": [("range", self.dividendsRange)]},
            "splits": {"options": [("range", self.splitsRange)]},
            "logo": {"options": None},
            "price": {"options": None},
            "delayed-quote": {"options": None},
            "effective-spread": {"options": None},
            "volume-by-venue": {"options": None}
        }

    def _default_options(self):
        """ Returns true if all parameters are set to default values (as specified in IEX docs), false otherwise"""
        return self.displayPercent is False and self.dividendsRange == '1m' and self.splitsRange == '1m' and self.chartRange == '1m' and self.last == 10

    @property
    def key(self):
        raise NotImplementedError

    @property
    def url(self):
        raise NotImplementedError

    @property
    def params(self):
        return {}

    @staticmethod
    def _validate_response(response):
        """ Ensures response from IEX server is valid.

        Positional Parameters:
            response: A request object

        """
        if response.text == "Unknown symbol":
            raise ValueError("Invalid Symbol")
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
    def _execute_iex_query(cls, url):
        def _api_call(cls, url):
            try:
                r = requests.get(url=url)
                r.raise_for_status
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.TooManyRedirects:
                pass
            except requests.exceptions.RequestException:
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
                self, *args, **kwargs)  # type dict
            outform = self.outputFormat
            if outform == 'json':
                return response
            elif outform == 'pandas':
                result = {}
                if self.type is "single":
                    syms = [self.symbols]
                else:
                    syms = self.symbols
                for symbol in syms:
                    d = response.pop(symbol)["chart"]
                    df = pandas.DataFrame(d)
                    df.set_index("date", inplace=True)
                    values = ["open", "high", "low", "close", "volume"]
                    df = df[values]
                    sstart = self.start.strftime('%Y-%m-%d')
                    send = self.end.strftime('%Y-%m-%d')
                    df = df.loc[sstart:send]
                    result.update({symbol: df})
                if len(result) > 1:
                    return pandas.Panel(result)
                else:
                    return pandas.DataFrame(result)
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
        if "chart" in endpoints:
            endpoints.remove("chart")
            endpoints.insert(0, "chart")
        endpoints = ','.join(endpoints)
        params = self.params
        params.update({"types": endpoints})
        p = "?" + "&".join("{}={}".format(*i) for i in params.items())
        url = self._IEX_API_URL + self.url + p
        return url

    def _fetch_default_options(self):
        """
        Conducts the IEX query when default options are specified. Returns IEXQueryError if problems arise.
        """
        data_set = dict.fromkeys(self.symbolList, {})
        query = self._prepare_query(list(self._ENDPOINTS))
        response = self._execute_iex_query(query)
        if self.key == "Share":
            response = {self.symbol: response}
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
            norms = [endpoint for endpoint in self._ENDPOINTS if self._ENDPOINTS[
                endpoint]["options"] == None]
            opts = set(self._ENDPOINTS) - set(norms)

            # fetch endpoints with no options
            nquery = self._prepare_query(norms)
            nresponse = self._execute_iex_query(nquery)
            # update the data set
            for symbol in self.symbolList:
                try:
                    if self.key == "Batch":
                        data_set[symbol].update(nresponse[symbol])
                    else:
                        data_set[symbol].update(nresponse)
                except:
                    raise IEXSymbolError(symbol)

        # fetch endpoints with options
        for endpoint in opts:
            options = urlencode(self._ENDPOINTS[endpoint]["options"])
            oquery = self._prepare_query([endpoint], options)
            oresponse = self._execute_iex_query(oquery)
        # update the dataset
            for symbol in self.symbolList:
                try:
                    if self.key == "Batch":
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
