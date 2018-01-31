import datetime
from functools import wraps

import pandas as pd

from .base import _IEXBase
from iexfinance.utils.exceptions import IEXSymbolError, IEXEndpointError

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def output_format(override=None):
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
    def _output_format(func):

        @wraps(func)
        def _format_wrapper(self, *args, **kwargs):
            response = func(self, *args, **kwargs)
            if self.output_format is 'pandas':
                if override is None:
                    df = pd.DataFrame(response)
                    return df
                else:
                    import warnings
                    warnings.warn("Pandas output not supported for this "
                                  "endpoint. Defaulting to JSON.")
            else:
                if self.key is 'share':
                    return response[self.symbols[0]]
                return response
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
                  "volume-by-venue", "ohlc"]
    ALL_ENDPOINTS_STR_1 = ",".join(_ENDPOINTS[:10])
    ALL_ENDPOINTS_STR_2 = ','.join(_ENDPOINTS[10:20])

    def __init__(self, symbols=None, displayPercent=False, _range="1m",
                 last=10, output_format='json', **kwargs):
        """ Initialize the class

        Parameters
        ----------
        symbols: str or list
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
        self.symbols = list(map(lambda x: x.upper(), symbols))
        if len(symbols) == 1:
            self.key = "share"
        else:
            self.key = "batch"
        self.output_format = output_format
        self.displayPercent = displayPercent
        self.range = _range
        self.last = last
        super(StockReader, self).__init__(**kwargs)

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
        self.endpoints = self.ALL_ENDPOINTS_STR_1
        self.data_set = self.fetch()
        self.endpoints = self.ALL_ENDPOINTS_STR_2
        data2 = self.fetch()

        for symbol in self.symbols:
            if symbol not in self.data_set:
                raise IEXSymbolError(symbol)
            self.data_set[symbol].update(data2[symbol])

    @property
    def url(self):
        return 'stock/market/batch'

    @property
    def params(self):
        params = {
            "symbols": ','.join(self.symbols),
            "types": self.endpoints
        }
        return params

    @output_format(override='json')
    def get_all(self):
        """
        Returns all endpoints, indexed by endpoint title for each symbol

        Notes
        -----
        Only allows JSON format (pandas not supported).
        """
        return self.data_set

    @output_format(override='json')
    def get_select_endpoints(self, endpoints=[]):
        """
        Universal selector method to obtain specific endpoints from the
        data set.

        Parameters
        ----------
        endpoints: str or list
            Desired valid endpoints for retrieval

        Notes
        -----
        Only allows JSON format (pandas not supported).

        Raises
        ------
        IEXEndpointError
            If an invalid endpoint is specified
        IEXQueryError
            If issues arise during query
        """
        if isinstance(endpoints, str):
            endpoints = [endpoints]
        elif not endpoints:
            raise ValueError("Please provide a valid list of endpoints")
        result = {}
        for symbol in self.symbols:
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
                temp[endpoint] = query
            result[symbol] = temp
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

    @output_format(override=None)
    def get_ohlc(self):
        """Returns the Stocks OHLC endpoint

        Reference
        ---------
        https://iextrading.com/developer/docs/#ohlc
        """
        return {symbol: self.data_set[symbol]["ohlc"] for symbol
                in self.data_set.keys()}

    def get_time_series(self):
        """Returns the Stocks Time Series endpoint

        Notes
        -----
        Time Series is an alias for the Chart endpoint, and will return the
        same

        Reference
        ---------
        https://iextrading.com/developer/docs/#time-series
        """
        return self.get_chart()

    # field methods
    @output_format(override='json')
    def get_company_name(self):
        return {symbol: self.get_quote()[symbol]["companyName"]
                if self.key == 'batch' else self.get_quote()['companyName']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_primary_exchange(self):
        return {symbol: self.get_quote()[symbol]["primaryExchange"]
                if self.key == 'batch' else self.get_quote()['primaryExchange']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_sector(self):
        return {symbol: self.get_quote()[symbol]["sector"]
                if self.key == 'batch' else self.get_quote()['sector']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_open(self):
        return {symbol: self.get_quote()[symbol]["open"]
                if self.key == 'batch' else self.get_quote()['open']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_close(self):
        return {symbol: self.get_quote()[symbol]["close"]
                if self.key == 'batch' else self.get_quote()['close']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_years_high(self):
        return {symbol: self.get_quote()[symbol]["week52High"]
                if self.key == 'batch' else self.get_quote()['week52High']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_years_low(self):
        return {symbol: self.get_quote()[symbol]["week52Low"]
                if self.key == 'batch' else self.get_quote()['week52Low']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_ytd_change(self):
        return {symbol: self.get_quote()[symbol]["ytdChange"]
                if self.key == 'batch' else self.get_quote()['ytdChange']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_volume(self):
        return {symbol: self.get_quote()[symbol]["latestVolume"]
                if self.key == 'batch' else self.get_quote()['latestVolume']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_market_cap(self):
        return {symbol: self.get_quote()[symbol]["marketCap"]
                if self.key == 'batch' else self.get_quote()['marketCap']
                for symbol in self.data_set.keys()}

    @output_format(override='json')
    def get_beta(self):
        return {symbol: self.get_key_stats()[symbol]["beta"]
                if self.key == 'batch' else
                self.get_key_stats()['beta'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_short_interest(self):
        return {symbol: self.get_key_stats()[symbol]["shortInterest"]
                if self.key == 'batch' else
                self.get_key_stats()['shortInterest'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_short_ratio(self):
        return {symbol: self.get_key_stats()[symbol]["shortRatio"]
                if self.key == 'batch' else
                self.get_key_stats()['shortRatio'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_latest_eps(self):
        return {symbol: self.get_key_stats()[symbol]["latestEPS"]
                if self.key == 'batch' else
                self.get_key_stats()['latestEPS'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_shares_outstanding(self):
        return {symbol: self.get_key_stats()[symbol]["sharesOutstanding"]
                if self.key == 'batch' else
                self.get_key_stats()['sharesOutstanding'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_float(self):
        return {symbol: self.get_key_stats()[symbol]["float"]
                if self.key == 'batch' else
                self.get_key_stats()['float'] for symbol in
                self.data_set.keys()}

    @output_format(override='json')
    def get_eps_consensus(self):
        return {symbol: self.get_key_stats()[symbol]["consensusEPS"]
                if self.key == 'batch' else
                self.get_key_stats()['consensusEPS'] for symbol in
                self.data_set.keys()}


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

    def __init__(self, symbols, start, end, output_format='json', **kwargs):
        if isinstance(symbols, list) and len(symbols) > 1:
            self.type = "Batch"
            self.symlist = symbols
        elif isinstance(symbols, str):
            self.type = "Share"
            self.symlist = [symbols]
        else:
            raise ValueError("Please input a symbol or list of symbols")
        self.symbols = symbols
        self.start = start
        self.end = end
        self.output_format = output_format
        super(HistoricalReader, self).__init__(**kwargs)

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
        delta = datetime.datetime.now().year - self.start.year
        if 2 <= delta <= 5:
            return "5y"
        elif 1 <= delta <= 2:
            return "2y"
        elif 0 <= delta < 1:
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
