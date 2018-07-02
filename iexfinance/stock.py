import datetime
from functools import wraps

import pandas as pd

from .base import _IEXBase
from iexfinance.utils.exceptions import IEXSymbolError, IEXEndpointError

# Data provided for free by IEX
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
                    if self.key is 'share':
                        return response[self.symbols[0]]
                    else:
                        return response
            else:
                if self.key is 'share':
                    return response[self.symbols[0]]
                return response
        return _format_wrapper
    return _output_format


def price_output_format(override=None):
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
                    if self.key is 'share':
                        return pd.DataFrame({"price": response})
                    else:
                        return pd.DataFrame({"price": response})
                else:
                    import warnings
                    warnings.warn("Pandas output not supported for this "
                                  "endpoint. Defaulting to JSON.")
                    if self.key is 'share':
                        return response[self.symbols[0]]
                    else:
                        return response
            else:
                if self.key is 'share':
                    return response[self.symbols[0]]
                return response
        return _format_wrapper
    return _output_format


def field_output_format(override=None, field_name=None):
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
            data = func(self, *args, **kwargs)

            if self.output_format is 'pandas':
                return data.transpose()
            else:
                if self.key is 'share':
                    return data[field_name]
                else:
                    return {symbol: data[symbol][field_name] for symbol in
                            list(data)}
        return _format_wrapper
    return _output_format


class StockReader(_IEXBase):
    """
    Base class for obtaining data from the Stock endpoints of IEX. Subclass of
    _IEXBase.
    """
    # Possible option values (first is default)
    _ENDPOINTS = ["chart", "quote", "book", "open-close", "previous",
                  "company", "stats", "peers", "relevant", "news",
                  "financials", "earnings", "dividends", "splits", "logo",
                  "price", "delayed-quote", "effective-spread",
                  "volume-by-venue", "ohlc"]

    def __init__(self, symbols=None, output_format='json', **kwargs):
        """ Initialize the class

        Parameters
        ----------
        symbols: str or list
            A nonempty list of symbols
        output_format: str, default 'json', optional
            Desired output format
        """
        self.symbols = list(map(lambda x: x.upper(), symbols))
        if len(symbols) == 1:
            self.key = "share"
        else:
            self.key = "batch"
        self.output_format = output_format
        self.endpoints = []
        super(StockReader, self).__init__(**kwargs)

    def change_output_format(self, new_format):
        if new_format.lower() not in ['pandas', 'json']:
            raise ValueError("Please specify a valid output format")
        else:
            self.output_format = new_format

    @output_format(override='json')
    def get_all(self):
        """
        Returns all endpoints, indexed by endpoint title for each symbol

        Notes
        -----
        Only allows JSON format (pandas not supported).
        """
        self.optional_params = {}
        self.endpoints = self._ENDPOINTS[:10]
        json_data = self.fetch()
        self.endpoints = self._ENDPOINTS[10:20]
        json_data_2 = self.fetch()
        for symbol in self.symbols:
            if symbol not in json_data:
                raise IEXSymbolError(symbol)
            json_data[symbol].update(json_data_2[symbol])
        return json_data

    @property
    def url(self):
        return 'stock/market/batch'

    @property
    def params(self):
        temp = {
            "symbols": ','.join(self.symbols),
            "types": ','.join(self.endpoints)
        }
        temp.update({key: self.optional_params[key]
                     for key in self.optional_params})
        if "filter_" in temp:
            if isinstance(temp["filter_"], list):
                temp["filter"] = ",".join(temp.pop("filter_"))
            else:
                temp["filter"] = temp.pop("filter_")
        if "range_" in temp:
            temp["range"] = temp.pop("range_")
        params = {k: str(v).lower() if v is True or v is False else str(v)
                  for k, v in temp.items()}
        return params

    def _get_endpoint(self, endpoint, params={}):
        self.optional_params = params
        self.endpoints = [endpoint]
        data = self.fetch()
        for symbol in self.symbols:
            if symbol not in data:
                raise IEXSymbolError(symbol)
            elif endpoint in data[symbol]:
                if data[symbol][endpoint] is None:
                    raise IEXEndpointError(endpoint)
            else:
                raise IEXEndpointError(endpoint)
        return data

    @output_format(override='json')
    def get_endpoints(self, endpoints=[]):
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
        IEXSymbolError
            If a symbol is invalid
        IEXQueryError
            If issues arise during query
        """
        if isinstance(endpoints, str):
            return self._get_endpoint(endpoints)
        elif not endpoints:
            raise ValueError("Please provide a valid list of endpoints")
        elif len(endpoints) > 10:
            raise ValueError("Please input up to 10 valid endpoints")
        self.optional_params = {}
        self.endpoints = endpoints
        json_data = self.fetch()
        for symbol in self.symbols:
            if symbol not in json_data:
                raise IEXSymbolError(symbol)
        for endpoint in endpoints:
            if endpoint in json_data[self.symbols[0]]:
                if json_data[self.symbols[0]][endpoint] is None:
                    raise IEXEndpointError(endpoint)
            else:
                raise IEXEndpointError(endpoint)
        return json_data

    @output_format(override=None)
    def get_book(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#book

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Book endpoint data
        """
        data = self._get_endpoint("book", kwargs)
        return {symbol: data[symbol]["book"] for symbol in list(data)}

    @output_format(override='json')
    def get_chart(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#chart

        Parameters
        ----------
        range: str, default '1m', optional
            Chart range to return. See docs.
        chartReset: boolean, default True, optional
            If true, 1d chart will reset at midnight instead of the default
            behavior of 9:30am EST.
        chartSimplify: boolean, default True, optional
            If true, runs polyline simplification using Douglas-Peucker
            algorithm. Useful for plotting spotline charts
        chartInterval: int, default None, optional
            Chart data will return every nth element (where n is chartInterval)
        changeFromClose: bool, default False, optional
            If true, changeOverTime and marketChangeOverTime will be relative
            to previous day close instead of the first value.
        chartLast: int, optional
            return the last N elements

        Notes
        -----
        Pandas not supported for this method. list will be returned.

        Returns
        -------
        list
            Stocks Chart endpoint data
        """
        data = self._get_endpoint("chart", kwargs)
        return {symbol: data[symbol]["chart"] for symbol in list(data)}

    @output_format(override=None)
    def get_company(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#company

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Company endpoint data
        """
        data = self._get_endpoint("company", kwargs)
        return {symbol: data[symbol]["company"] for symbol in list(data)}

    @output_format(override=None)
    def get_delayed_quote(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#delayed-quote

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Delayed Quote endpoint data
        """
        data = self._get_endpoint("delayed-quote", kwargs)
        return {symbol: data[symbol]["delayed-quote"] for symbol in
                list(data)}

    @output_format(override='json')
    def get_dividends(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#dividends

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of dividends to return
        Notes
        -----
        Pandas not supported for this method. list will be returned.

        Returns
        -------
        list
            Stocks Dividends endpoint data
        """
        data = self._get_endpoint("dividends", kwargs)
        return {symbol: data[symbol]["dividends"] for symbol in list(data)}

    @output_format(override=None)
    def get_earnings(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#earnings

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Earnings endpoint data
        """
        data = self._get_endpoint("earnings", kwargs)
        return {symbol: data[symbol]["earnings"].get("earnings", [])
                for symbol in list(data)}

    @output_format(override=None)
    def get_effective_spread(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#effective-spread

        Returns
        -------
        list or pandas.DataFrame
            Stocks Effective Spread endpoint data
        """
        data = self._get_endpoint("effective-spread", kwargs)
        return {symbol: data[symbol]["effective-spread"] for symbol
                in list(data)}

    @output_format(override=None)
    def get_financials(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#financials

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Financials endpoint data
        """
        data = self._get_endpoint("financials", kwargs)
        return {symbol: data[symbol]["financials"].get("financials", [])
                for symbol in list(data)}

    @output_format(override=None)
    def get_key_stats(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#key-stats

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Key Stats endpoint data
        """
        data = self._get_endpoint("stats", kwargs)
        return {symbol: data[symbol]["stats"] for symbol in list(data)}

    @output_format(override=None)
    def get_largest_trades(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#largest-trades

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Largest Trades endpoint data
        """
        data = self._get_endpoint("largest-trades", kwargs)
        return {symbol: data[symbol]["largest-trades"] for symbol in
                list(data)}

    @output_format(override=None)
    def get_logo(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#logo

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Logo endpoint data
        """
        data = self._get_endpoint("logo", kwargs)
        return {symbol: data[symbol]["logo"] for symbol in list(data)}

    @output_format(override='json')
    def get_news(self, **kwargs):
        """Returns the Stocks News endpoint (list or pandas)

        Reference: https://iextrading.com/developer/docs/#news

        Parameters
        ----------
        range: int, default 10, optional
            Time period of news to return (in days)

        Returns
        -------
        list or dict
            Stocks News endpoint data
        """
        data = self._get_endpoint("news", kwargs)
        return {symbol: data[symbol]["news"] for symbol in list(data)}

    @output_format(override=None)
    def get_ohlc(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#ohlc

        Returns
        -------
        dict or pandas.DataFrame
            Stocks OHLC endpoint data
        """
        data = self._get_endpoint("ohlc", kwargs)
        return {symbol: data[symbol]["ohlc"] for symbol
                in list(data)}

    def get_open_close(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#open-close

        Notes
        -----
        Open/Close is an alias for the OHLC endpoint, and will return the
        same

        Returns
        -------
        list or pandas.DataFrame
            Stocks Open/Close (OHLC) endpoint data
        """
        return self.get_ohlc()

    @output_format(override='json')
    def get_peers(self, **kwargs):
        """
        Reference:https://iextrading.com/developer/docs/#peers

        Notes
        -----
        Only allows JSON format (pandas not supported).

        Returns
        -------
        list
            Stocks Peers endpoint data
        """
        data = self._get_endpoint("peers", kwargs)
        return {symbol: data[symbol]["peers"] for symbol in list(data)}

    @output_format(override=None)
    def get_previous(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#previous

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Previous endpoint data
        """
        data = self._get_endpoint("previous", kwargs)
        return {symbol: data[symbol]["previous"] for symbol in list(data)}

    @price_output_format(override=None)
    def get_price(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#price

        Returns
        -------
        float or pandas.DataFrame
            Stocks Price endpoint data
        """
        data = self._get_endpoint("price", kwargs)
        return {symbol: data[symbol]["price"] for symbol in list(data)}

    @output_format(override=None)
    def get_quote(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#quote

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Quote endpoint data
        """
        data = self._get_endpoint("quote", kwargs)
        return {symbol: data[symbol]["quote"] for symbol in list(data)}

    @output_format(override=None)
    def get_relevant(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#relevant

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Relevant endpoint data
        """
        data = self._get_endpoint("relevant", kwargs)
        return {symbol: data[symbol]["relevant"] for symbol in list(data)}

    @output_format(override=None)
    def get_splits(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#splits

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of splits to return

        Returns
        -------
        list or pandas.DataFrame
            Stocks Splits endpoint data
        """
        data = self._get_endpoint("splits", kwargs)
        return {symbol: data[symbol]["splits"] for symbol in list(data)}

    def get_time_series(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#time-series

        Notes
        -----
        Time Series is an alias for the Chart endpoint, and will return the
        same

        Returns
        -------
        list or pandas.DataFrame
            Stocks Time Series (Chart) endpoint data
        """
        return self.get_chart()

    @output_format(override=None)
    def get_volume_by_venue(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#volume-by-venue

        Returns
        -------
        list or pandas.DataFrame
            Stocks Volume by Venue endpoint data
        """
        data = self._get_endpoint("volume-by-venue", kwargs)
        return {symbol: data[symbol]["volume-by-venue"] for symbol
                in list(data)}

    # field methods
    @field_output_format(override=None, field_name="companyName")
    def get_company_name(self):
        return self.get_quote(filter_="companyName")

    @field_output_format(override=None, field_name="primaryExchange")
    def get_primary_exchange(self):
        return self.get_quote(filter_="primaryExchange")

    @field_output_format(override=None, field_name="sector")
    def get_sector(self):
        return self.get_quote(filter_="sector")

    @field_output_format(override=None, field_name="open")
    def get_open(self):
        return self.get_quote(filter_="open")

    @field_output_format(override=None, field_name="close")
    def get_close(self):
        return self.get_quote(filter_="close")

    @field_output_format(override=None, field_name="week52High")
    def get_years_high(self):
        return self.get_quote(filter_="week52High")

    @field_output_format(override=None, field_name="week52Low")
    def get_years_low(self):
        return self.get_quote(filter_="week52Low")

    @field_output_format(override=None, field_name="ytdChange")
    def get_ytd_change(self):
        return self.get_quote(filter_="ytdChange")

    @field_output_format(override=None, field_name="latestVolume")
    def get_volume(self):
        return self.get_quote(filter_="latestVolume")

    @field_output_format(override=None, field_name="marketCap")
    def get_market_cap(self):
        return self.get_quote(filter_="marketCap")

    @field_output_format(override=None, field_name="beta")
    def get_beta(self):
        return self.get_key_stats(filter_="beta")

    @field_output_format(override=None, field_name="shortInterest")
    def get_short_interest(self):
        return self.get_key_stats(filter_="shortInterest")

    @field_output_format(override=None, field_name="shortRatio")
    def get_short_ratio(self):
        return self.get_key_stats(filter_="shortRatio")

    @field_output_format(override=None, field_name="latestEPS")
    def get_latest_eps(self):
        return self.get_key_stats(filter_="latestEPS")

    @field_output_format(override=None, field_name="sharesOutstanding")
    def get_shares_outstanding(self):
        return self.get_key_stats(filter_="sharesOutstanding")

    @field_output_format(override=None, field_name="float")
    def get_float(self):
        return self.get_key_stats(filter_="float")

    @field_output_format(override=None, field_name="consensusEPS")
    def get_eps_consensus(self):
        return self.get_key_stats(filter_="consensusEPS")


class HistoricalReader(_IEXBase):
    """
    A class to download historical data from the chart endpoint

    Parameters
    ----------
    symbol: str or list
        A symbol or list of symbols
    start: datetime.datetime
        The desired start date (defaults to 1/1/2015)
    end: datetime.datetime
        The desired end date (defaults to today's date)
    output_format: str, default 'json', optional
        Desired output format.

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


class MoversReader(_IEXBase):
    """
    Base class for retrieving market movers from the Stocks List endpoint

    Parameters
    ----------
    mover: str
        Desired mover
    """
    _AVAILABLE_MOVERS = ["mostactive", "gainers", "losers", "iexvolume",
                         "iexpercent"]

    def __init__(self, mover=None, **kwargs):
        super(MoversReader, self).__init__(**kwargs)
        if mover in self._AVAILABLE_MOVERS:
            self.mover = mover
        else:
            raise ValueError("Please input a valid market mover.")

    @property
    def url(self):
        return 'stock/market/list/' + self.mover
