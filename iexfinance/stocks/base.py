import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import _handle_lists, no_pandas
from iexfinance.utils.exceptions import IEXSymbolError, IEXEndpointError


class StockReader(_IEXBase):
    """
    Base class for obtaining data from the Stock endpoints of IEX.
    """
    # Possible option values (first is default)
    _ENDPOINTS = ["chart", "quote", "book", "open-close", "previous",
                  "company", "stats", "peers", "relevant", "news",
                  "financials", "earnings", "dividends", "splits", "logo",
                  "price", "delayed-quote", "effective-spread",
                  "volume-by-venue", "ohlc"]

    def __init__(self, symbols=None, **kwargs):
        """ Initialize the class

        Parameters
        ----------
        symbols : string, array-like object (list, tuple, Series), or DataFrame
            Desired symbols for retrieval
        """
        self.symbols = list(map(lambda x: x.upper(), _handle_lists(symbols)))
        self.n_symbols = len(self.symbols)
        self.endpoints = []
        super(StockReader, self).__init__(**kwargs)

    def get_all(self):
        """
        Returns all endpoints, indexed by endpoint title for each symbol

        Notes
        -----
        Only allows JSON format (pandas not supported).
        """
        self.optional_params = {}
        self.endpoints = self._ENDPOINTS[:10]
        json_data = self.fetch(fmt_p=no_pandas)
        self.endpoints = self._ENDPOINTS[10:20]
        json_data_2 = self.fetch(fmt_p=no_pandas)
        for symbol in self.symbols:
            if symbol not in json_data:
                raise IEXSymbolError(symbol)
            json_data[symbol].update(json_data_2[symbol])
        return json_data[self.symbols[0]] if self.n_symbols == 1 else json_data

    @property
    def url(self):
        return 'stock/market/batch'

    @property
    def params(self):
        temp = {
            "symbols": ','.join(self.symbols),
            "types": ','.join(self.endpoints)
        }
        temp.update(self.optional_params)
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

    def _get_endpoint(self, endpoint, params={}, fmt_p=None,
                      fmt_j=None, filter_=None):
        result = {}
        if filter_:
            params.update({"filter": filter_})
        self.optional_params = params
        self.endpoints = [endpoint]
        data = self.fetch(fmt_j=fmt_j, fmt_p=no_pandas)
        for symbol in self.symbols:
            if symbol not in data:
                raise IEXSymbolError(symbol)
            if endpoint not in data[symbol]:
                result[symbol] = []
            else:
                result[symbol] = data[symbol][endpoint]
        return self._output_format_one(result, fmt_p=fmt_p, fmt_j=fmt_j)

    def _get_field(self, endpoint, field):
        data = getattr(self, "get_%s" % endpoint)(filter_=field)
        if self.output_format == 'json':
            if self.n_symbols == 1:
                data = data[field]
            else:
                data = {symbol: data[symbol][field] for symbol in self.symbols}
        return data

    def _output_format_one(self, out, fmt_p=None, fmt_j=None):
        data = super(StockReader, self)._output_format(out, fmt_p=fmt_p)
        if len(self.symbols) == 1 and self.output_format == 'json':
            return data[self.symbols[0]]
        return data

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
        if isinstance(endpoints, str) and endpoints in self._ENDPOINTS:
            endpoints = list(endpoints)
        if not endpoints or not set(endpoints).issubset(self._ENDPOINTS):
            raise IEXEndpointError("Please provide a valid list of endpoints")
        elif len(endpoints) > 10:
            raise ValueError("Please input up to 10 valid endpoints")
        self.optional_params = {}
        self.endpoints = endpoints
        json_data = self.fetch(fmt_p=no_pandas)
        for symbol in self.symbols:
            if symbol not in json_data:
                raise IEXSymbolError(symbol)
        return json_data[self.symbols[0]] if self.n_symbols == 1 else json_data

    def get_book(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#book

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Book endpoint data
        """
        return self._get_endpoint("book", params=kwargs)

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

        Returns
        -------
        list
            Stocks Chart endpoint data
        """
        def fmt_p(out):
            result = {}
            for symbol in self.symbols:
                d = out.pop(symbol)
                df = pd.DataFrame(d)
                df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
                values = ["open", "high", "low", "close", "volume"]
                df = df[values]
                result.update({symbol: df})
            if len(result) == 1:
                return result[self.symbols[0]]
            else:
                return pd.concat(result.values(), keys=result.keys(), axis=1)

        return self._get_endpoint("chart", fmt_p=fmt_p, params=kwargs)

    def get_company(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#company

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Company endpoint data
        """
        return self._get_endpoint("company", params=kwargs)

    def get_delayed_quote(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#delayed-quote

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Delayed Quote endpoint data
        """
        return self._get_endpoint("delayed-quote", params=kwargs)

    def get_dividends(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#dividends

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of dividends to return

        Returns
        -------
        list or pandas.DataFrame
            Stocks Dividends endpoint data
        """
        def fmt(out):
            return {symbol: out[symbol]["earnings"] for symbol in self.symbols}

        def fmt_p(out):
            results = {}
            for symbol in self.symbols:
                if out[symbol]:
                    data = pd.DataFrame(out[symbol])
                    data = data.set_index("exDate")
                    results[symbol] = data
            if not results:
                return pd.DataFrame([])
            return results if self.n_symbols != 1 else results[self.symbols[0]]

        return self._get_endpoint("dividends", fmt_p=fmt_p, params=kwargs)

    def get_earnings(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#earnings

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Earnings endpoint data
        """
        def fmt(out):
            return {symbol: out[symbol]["earnings"] for symbol in self.symbols}

        def fmt_p(out):
            results = {}
            for symbol in self.symbols:
                if out[symbol]:
                    data = pd.DataFrame(out[symbol]["earnings"])
                    data = data.set_index("EPSReportDate")
                    results[symbol] = data
            if not results:
                return pd.DataFrame([])
            return results if self.n_symbols != 1 else results[self.symbols[0]]

        return self._get_endpoint("earnings", fmt_j=fmt, fmt_p=fmt_p,
                                  params=kwargs)

    def get_effective_spread(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#effective-spread

        Returns
        -------
        list or pandas.DataFrame
            Stocks Effective Spread endpoint data
        """
        return self._get_endpoint("effective-spread", params=kwargs)

    def get_financials(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#financials

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Financials endpoint data
        """
        def fmt(out):
            return {symbol: out[symbol].get("financials", []) for symbol in
                    self.symbols}

        def fmt_p(out):
            results = {}
            for symbol in self.symbols:
                if out[symbol]:
                    data = pd.DataFrame(out[symbol]["financials"])
                    data = data.set_index("reportDate")
                    results[symbol] = data
            if not results:
                return pd.DataFrame([])
            return results if self.n_symbols != 1 else results[self.symbols[0]]

        return self._get_endpoint("financials", fmt_j=fmt,
                                  fmt_p=fmt_p, params=kwargs)

    def get_key_stats(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#key-stats

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Key Stats endpoint data
        """
        return self._get_endpoint("stats", params=kwargs)

    def get_largest_trades(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#largest-trades

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Largest Trades endpoint data
        """
        return self._get_endpoint("largest-trades", params=kwargs)

    def get_logo(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#logo

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Logo endpoint data
        """
        return self._get_endpoint("logo", params=kwargs)

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
        return self._get_endpoint("news", fmt_p=no_pandas, params=kwargs)

    def get_ohlc(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#ohlc

        Returns
        -------
        dict or pandas.DataFrame
            Stocks OHLC endpoint data
        """
        return self._get_endpoint("ohlc", params=kwargs)

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
        return self._get_endpoint("ohlc", params=kwargs)

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
        return self._get_endpoint("peers", fmt_p=no_pandas, params=kwargs)

    def get_previous(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#previous

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Previous endpoint data
        """
        return self._get_endpoint("previous", params=kwargs)

    def get_price(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#price

        Returns
        -------
        float or pandas.DataFrame
            Stocks Price endpoint data
        """
        def fmt_p(out):
            return pd.DataFrame(out, index=self.symbols)

        return self._get_endpoint("price", fmt_p=fmt_p, params=kwargs)

    def get_quote(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#quote

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Quote endpoint data
        """
        return self._get_endpoint("quote", params=kwargs)

    def get_relevant(self, **kwargs):
        """
        Reference: https://iextrading.com/developer/docs/#relevant

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Relevant endpoint data
        """
        return self._get_endpoint("relevant", params=kwargs)

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
        return self._get_endpoint("splits", params=kwargs)

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
        return self._get_endpoint("chart", params=kwargs)

    def get_volume_by_venue(self, **kwargs):
        """
        Reference:  https://iextrading.com/developer/docs/#volume-by-venue

        Returns
        -------
        list or pandas.DataFrame
            Stocks Volume by Venue endpoint data
        """
        return self._get_endpoint("volume-by-venue", params=kwargs)

    # field methods
    def get_company_name(self):
        return self._get_field("quote", "companyName")

    def get_primary_exchange(self):
        return self._get_field("quote", "primaryExchange")

    def get_sector(self):
        return self._get_field("quote", "sector")

    def get_open(self):
        return self._get_field("quote", "open")

    def get_close(self):
        return self._get_field("quote", "close")

    def get_years_high(self):
        return self._get_field("quote", "week52High")

    def get_years_low(self):
        return self._get_field("quote", "week52Low")

    def get_ytd_change(self):
        return self._get_field("quote", "ytdChange")

    def get_volume(self):
        return self._get_field("quote", "latestVolume")

    def get_market_cap(self):
        return self._get_field("quote", "marketCap")

    def get_beta(self):
        return self._get_field("key_stats", "beta")

    def get_short_interest(self):
        return self._get_field("key_stats", "shortInterest")

    def get_short_ratio(self):
        return self._get_field("key_stats", "shortRatio")

    def get_latest_eps(self):
        return self._get_field("key_stats", "latestEPS")

    def get_shares_outstanding(self):
        return self._get_field("key_stats", "sharesOutstanding")

    def get_float(self):
        return self._get_field("key_stats", "float")

    def get_eps_consensus(self):
        return self._get_field("key_stats", "consensusEPS")
