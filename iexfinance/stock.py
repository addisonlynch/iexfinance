import datetime
from functools import wraps

from dateutil.relativedelta import relativedelta

import pandas as pd

from .base import _IEXBase
from iexfinance.utils.exceptions import (IEXSymbolError, IEXFieldError,
                                         IEXEndpointError)

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def output_format(override=None):

    def _output_format(func):
        """
        Decorator in charge of giving the output its correct format, either
        json or pandas

        Parameters
        ----------
        func: function
            The function to be decorated
        override: str
            Override the internal format of the call, default none
        """
        @wraps(func)
        def _format_wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if self.output_format is 'json':
                return response
            if self.output_format is 'pandas' and override is 'json':
                import warnings
                warnings.warn("Pandas output not supported for this endpoint."
                              " Defaulting to JSON.")
                return response
            else:
                df = pd.DataFrame(response)
                return df
        return _format_wrapper
    return _output_format


class StockReader(_IEXBase):
    """
    Base class for obtaining data from the Stock endpoints of IEX. Subclass of
    _IEXBase, subclassed by Share, Batch, and HistoricalReader
    """
    # Possible option values (first is default)
    _RANGE_VALUES = ['1m', '5y', '2y', '1y', 'ytd', '6m', '3m', '1d']
    _ENDPOINTS = ["chart", "quote", "book", "open-close", "previous",
                  "company", "stats", "peers", "relevant", "news",
                  "financials", "earnings", "dividends", "splits", "logo",
                  "price", "delayed-quote", "effective-spread",
                  "volume-by-venue"]
    _PANDAS_BLACKLIST = ['chart', 'price']
    _ALL_ENDPOINTS_STR = ",".join(_ENDPOINTS)

    def __init__(self, symbolList=None, displayPercent=False, _range="1m",
                 last=10, output_format='json', retry_count=3, pause=0.001,
                 session=None):
        """ Initialize the class

        Parameters
        ----------
        symbolList: str or list
            A nonempty list of symbols
        displayPercent: boolean
        range: str
            The range to use for the chart endpoint. Must be
            contained in _RANGE_VALUES
        last: int
            Range to use for the "last" attribute of the news endpoint.
        output_format: str
            Desired output format
        """
        self.symbolList = list(map(lambda x: x.upper(), symbolList))
        if len(symbolList) == 1:
            self.key = "share"
        else:
            self.key = "batch"
        self.output_format = output_format
        self.displayPercent = displayPercent
        self.range = _range
        self.last = last
        super(StockReader, self).__init__(retry_count, pause,
                                          session)

        # Parameter checking
        if not isinstance(self.displayPercent, bool):
            raise TypeError("displayPercent must be a boolean value")
        elif self.range not in self._RANGE_VALUES:
            raise ValueError("Invalid chart range.")
        elif int(self.last) > 50 or int(self.last) < 1:
            raise ValueError(
                "Invalid news last range. Enter a value between 1 and 50.")
        self.refresh()

    def refresh(self):
        """
        Downloads latest data from all Stock endpoints
        """
        self.data_set = self.fetch()
        for symbol in self.symbolList:
            if symbol not in self.data_set:
                raise IEXSymbolError(symbol)

    @property
    def url(self):
        return 'stock/market/batch'

    @property
    def params(self):
        params = {
            "symbols": ','.join(self.symbolList),
            "types": self._ALL_ENDPOINTS_STR
        }
        return params

    def get_all(self):
        return self.data_set

    # universal selectors
    def get_select_endpoints(self, endpoints=[]):
        """
        Universal selector method to obtain custom endpoints from the data
        set. Will throw a IEXEndpointError if an invalid endpoint is specified
        and an IEXQueryError if the endpoint cannot be retrieved.

        Postional arguments:
            endpointList: A string or list of strings that specifies the
            endpoints desired
        """
        if type(endpoints) is str:
            endpoints = [endpoints]
        elif not endpoints:
            raise ValueError("Please provide a valid list of endpoints")
        result = {}
        for symbol in self.symbolList:
            temp = {}
            try:
                ds = self.data_set[symbol]
            except KeyError:
                IEXSymbolError(symbol)
            for endpoint in endpoints:
                try:
                    query = ds[endpoint]
                except KeyError:
                    raise IEXEndpointError(endpoint)
                temp.update({endpoint: query})
            result.update({symbol: temp})
        return result

    def get_select_fields(self, endpoint, attrList=[]):
        """
        Universal selector method to obtain custom fields from an
        individual endpoint. If an invalid endpoint is specified, throws an
        IEXEndpointError. If an invalid field is specified, throws an
        IEXFieldError. If there are issues with the query, throws an
        IEXQueryError.

        Positional Arguments:
            endpoint: A valid endpoint (string)
            attrList: A valid list of fields desired from the given
             endpoint
        """
        if type(attrList) is str:
            attrList = [attrList]
        result = {}
        if not attrList:
            raise ValueError("Please give a valid attribute list")
        for symbol in self.symbolList:
            try:
                ep = self.data_set[symbol][endpoint]
            except KeyError:
                raise IEXEndpointError(endpoint)
            temp = {}
            for attr in attrList:
                try:
                    query = ep[attr]
                except KeyError:
                    raise IEXFieldError(endpoint, attr)
                temp.update({attr: query})
            result.update({symbol: temp})
        return result

    # endpoint methods
    @output_format(override=None)
    def get_quote(self):
        """Retrieves Stocks Quote endpoint

        Reference
        ---------
        https://iextrading.com/developer/docs/#quote
        """
        return {symbol: self.data_set[symbol]["quote"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_book(self):
        """Returns the Stocks Book endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#book
        """
        return {symbol: self.data_set[symbol]["book"] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_chart(self):
        """Returns the Stocks Chart endpoint in JSON format

        Notes
        -----
        Only allows JSON format (pandas not supported).

        Reference
        ---------
        https://iextrading.com/developer/docs/#chart
        """
        return {symbol: self.data_set[symbol]["chart"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_open_close(self):
        """Returns the Stocks Open/Close endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#open-close
        """
        return {symbol: self.data_set[symbol]["open-close"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_previous(self):
        """Returns the Stocks Previous endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#previous
        """
        return {symbol: self.data_set[symbol]["previous"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_company(self):
        """Returns the Stocks Company endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#company
        """
        return {symbol: self.data_set[symbol]["company"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_key_stats(self):
        """Returns the Stocks Key Stats endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#key-stats
        """
        return {symbol: self.data_set[symbol]["stats"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_peers(self):
        """Returns the Stocks Peers endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#peers
        """
        return {symbol: self.data_set[symbol]["peers"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_relevant(self):
        """Returns the Stocks Relevant endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#relevant
        """
        return {symbol: self.data_set[symbol]["relevant"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_news(self):
        """Returns the Stocks News endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#news
        """
        return {symbol: self.data_set[symbol]["news"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_financials(self):
        """Returns the Stocks Financials endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#financials
        """
        return {symbol: self.data_set[symbol]["financials"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_earnings(self):
        """Returns the Stocks Earnings endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#earnings
        """
        return {symbol: self.data_set[symbol]["earnings"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_dividends(self):
        """Returns the Stocks Dividends endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#dividends
        """
        return {symbol: self.data_set[symbol]["dividends"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_splits(self):
        """Returns the Stocks Splits endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#splits
        """
        return {symbol: self.data_set[symbol]["splits"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_logo(self):
        """Returns the Stocks Logo endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#logo
        """
        return {symbol: self.data_set[symbol]["logo"] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_price(self):
        """Returns the Stocks Price endpoint in JSON format

        Notes
        -----
        Only allows JSON format (pandas not supported).

        Reference
        ---------
        https://iextrading.com/developer/docs/#price
        """
        return {symbol: self.data_set[symbol]["price"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_delayed_quote(self):
        """Returns the Stocks Delayed Quote endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#delayed-quote
        """
        return {symbol: self.data_set[symbol]["delayed-quote"] for symbol in
                self.data_set.keys()}

    @output_format(override=None)
    def get_effective_spread(self):
        """Returns the Stocks Effective Spread endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#effective-spread
        """
        return {symbol: self.data_set[symbol]["effective-spread"] for symbol
                in self.data_set.keys()}

    @output_format(override=None)
    def get_volume_by_venue(self):
        """Returns the Stocks Volume by Venue endpoint in JSON format

        Reference
        ---------
        https://iextrading.com/developer/docs/#volume-by-venue
        """
        return {symbol: self.data_set[symbol]["volume-by-venue"] for symbol
                in self.data_set.keys()}

    # field methods
    def get_company_name(self):
        return {symbol: self.get_quote()[symbol]["companyName"] for symbol in
                self.data_set.keys()}

    def get_primary_exchange(self):
        return {symbol: self.get_quote()[symbol]["primaryExchange"] for symbol
                in self.data_set.keys()}

    def get_sector(self):
        return {symbol: self.get_quote()[symbol]["sector"] for symbol in
                self.data_set.keys()}

    def get_open(self):
        return {symbol: self.get_quote()[symbol]["open"] for symbol in
                self.data_set.keys()}

    def get_close(self):
        return {symbol: self.get_quote()[symbol]["close"] for symbol in
                self.data_set.keys()}

    def get_years_high(self):
        return {symbol: self.get_quote()[symbol]["week52High"] for symbol in
                self.data_set.keys()}

    def get_years_low(self):
        return {symbol: self.get_quote()[symbol]["week52Low"] for symbol in
                self.data_set.keys()}

    def get_ytd_change(self):
        return {symbol: self.get_quote()[symbol]["ytdChange"] for symbol in
                self.data_set.keys()}

    def get_volume(self):
        return {symbol: self.get_quote()[symbol]["latestVolume"] for symbol in
                self.data_set.keys()}

    def get_market_cap(self):
        return {symbol: self.get_quote()[symbol]["marketCap"]for symbol in
                self.data_set.keys()}

    def get_beta(self):
        return {symbol: self.get_key_stats()[symbol]["beta"] for symbol in
                self.data_set.keys()}

    def get_short_interest(self):
        return {symbol: self.get_key_stats()[symbol]["shortInterest"] for
                symbol in self.data_set.keys()}

    def get_short_ratio(self):
        return {symbol: self.get_key_stats()[symbol]["shortRatio"] for
                symbol in self.data_set.keys()}

    def get_latest_eps(self):
        return {symbol: self.get_key_stats()[symbol]["latestEPS"] for symbol
                in self.data_set.keys()}

    def get_shares_outstanding(self):
        return {symbol: self.get_key_stats()[symbol]["sharesOutstanding"] for
                symbol in self.data_set.keys()}

    def get_float(self):
        return {symbol: self.get_key_stats()[symbol]["float"] for symbol in
                self.data_set.keys()}

    def get_eps_consensus(self):
        return {symbol: self.get_key_stats()[symbol]["consensusEPS"] for
                symbol in self.data_set.keys()}


class HistoricalReader(_IEXBase):
    """
    A class to download historical data from the chart endpoint

    Positional Arguments:
        symbol: A symbol or list of symbols
        start: A datetime object
        end: A datetime object

    Keyword Arguments:
        output_format: Desired output format (json by default)

    Reference: https://iextrading.com/developer/docs/#chart
    """

    def __init__(self, symbolList, start, end, output_format='json',
                 retry_count=3, pause=0.001, session=None):
        if isinstance(symbolList, list) and len(symbolList) > 1:
            self.type = "Batch"
            self.symlist = symbolList
        elif isinstance(symbolList, str):
            self.type = "Share"
            self.symlist = [symbolList]
        else:
            raise ValueError("Please input a symbol or list of symbols")
        self.symbols = symbolList
        self.start = start
        self.end = end
        self.output_format = output_format
        super(HistoricalReader, self).__init__(retry_count,
                                               pause, session)

    @property
    def url(self):
        return "stock/market/batch"

    @property
    def key(self):
        return self.type

    @property
    def chart_range(self):
        """ Calculates the chart range from start and end. Downloads larger
        datasets (5y and 2y) when necessary, but defaults to 1y for performance
        reasons
        """
        delta = relativedelta(self.start, datetime.datetime.now())
        if 2 <= (delta.years * -1) <= 5:
            return "5y"
        elif 1 <= (delta.years * -1) <= 2:
            return "2y"
        elif 0 <= (delta.years * -1) < 1:
            return "1y"
        else:
            raise ValueError(
                "Invalid date specified. Must be within past 5 years.")

    @property
    def params(self):
        if self.type is "Batch":
            syms = ",".join(self.symbols)
        else:
            syms = self.symbols
        params = {
            "symbols": syms,
            "types": "chart",
            "range": self.chart_range
        }
        return params

    def fetch(self):
        response = super(HistoricalReader, self).fetch()
        for sym in self.symlist:
            if sym not in list(response):
                raise IEXSymbolError(sym)
        return self._output_format(response)

    def _output_format(self, out):
        result = {}
        for symbol in self.symlist:
            d = out.pop(symbol)["chart"]
            df = pd.DataFrame(d)
            df.set_index("date", inplace=True)
            values = ["open", "high", "low", "close", "volume"]
            df = df[values]
            sstart = self.start.strftime('%Y-%m-%d')
            send = self.end.strftime('%Y-%m-%d')
            df = df.loc[sstart:send]
            result.update({symbol: df})
        if self.output_format is "pandas":
            if len(result) > 1:
                return result
            return result[self.symbols]
        else:
            for sym in list(result):
                result[sym] = result[sym].to_dict('index')
            return result
