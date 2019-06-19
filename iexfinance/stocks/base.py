import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import _handle_lists, no_pandas
from iexfinance.utils.exceptions import (IEXSymbolError, IEXEndpointError,
                                         ImmediateDeprecationError)
from iexfinance.utils import legacy_endpoint


class Stock(_IEXBase):
    """
    Base class for obtaining data from the Stock endpoints of IEX.

    Attributes
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index)
        A symbol or list of symbols for which to obtain data
    output_format: str
        Desired output format for requests (default is ``json``, also accepts
        ``pandas`` for a ``pandas.DataFrame`` output format)
    token: str, optional
        Authentication token (required for use with IEX Cloud)
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
        if isinstance(symbols, str) and symbols:
            self.symbols = [symbols]
        elif isinstance(symbols, list) and 0 < len(symbols) <= 100:
            self.symbols = symbols
        else:
            raise ValueError("Please input a symbol or list of symbols")
        self.symbols = list(map(lambda x: x.upper(), _handle_lists(symbols)))
        self.endpoints = []
        super(Stock, self).__init__(**kwargs)

    @legacy_endpoint
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
    def n_symbols(self):
        return len(self.symbols)

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
        # IEX Cloud returns multiple symbol requests as as a list of dicts
        # so convert to dict of dicts
        if isinstance(data, list):
            data = data[0]
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
        data = super(Stock, self)._output_format(out, fmt_p=fmt_p)
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

    def get_balance_sheet(self, **kwargs):
        """Balance Sheet

        Pulls balance sheet data. Available quarterly (4 quarters) and annually
        (4 years)

        Reference: https://iexcloud.io/docs/api/#balance-sheet

        Data Weighting: ``3000`` per symbol per period

        .. warning:: This endpoint is only available using IEX Cloud. See
                     :ref:`Migrating` for more information.

        Parameters
        ----------
        period: str, default 'quarter', optional
            Allows you to specify annual or quarterly balance sheet.
            Value should be `annual` or `quarter`.
        """
        def fmt_p(out):
            data = {(symbol, sheet["reportDate"]): sheet for symbol in out
                    for sheet in out[symbol]["balancesheet"]}
            return pd.DataFrame(data)

        return self._get_endpoint("balance-sheet", fmt_p=fmt_p, params=kwargs)

    def get_book(self):
        """Book

        Reference: https://iexcloud.io/docs/api/#book

        Data Weighting: ``1`` per quote returned

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Book endpoint data
        """
        return self._get_endpoint("book")

    def get_cash_flow(self, **kwargs):
        """Cash Flow

        Pulls cash flow data. Available quarterly (4 quarters) or annually
        (4 years).

        Reference: https://iexcloud.io/docs/api/#cash-flow

        Data Weighting: ``1000`` per symbol per period

        .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

        Parameters
        ----------
        period: str, default 'quarterly', optional
            Allows you to specify annual or quarterly cash flows. Defaults to
            quarterly. Values should be annual or quarter.

        Returns
        ------
        dict or pandas.DataFrame
            Stocks Cash Flow endpoint data
        """
        def fmt_p(out):
            data = {(symbol, sheet["reportDate"]): sheet for symbol in out
                    for sheet in out[symbol]["cashflow"]}
            return pd.DataFrame(data)
        return self._get_endpoint("cash-flow", fmt_p=fmt_p, params=kwargs)

    def get_chart(self, **kwargs):
        """Chart

        MOVED in IEX Cloud

        .. seealso:: ``get_historical_prices``
        """
        return self.get_historical_prices(**kwargs)

    def get_company(self, **kwargs):
        """Company

        Reference: https://iexcloud.io/docs/api/#company

        Data Weighting: ``1``

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Company endpoint data
        """
        return self._get_endpoint("company", params=kwargs)

    def get_delayed_quote(self):
        """Delayed Quote

        Reference: https://iexcloud.io/docs/api/#delayed-quote

        Data Weighting: ``1`` per symbol per quote

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Delayed Quote endpoint data
        """
        return self._get_endpoint("delayed-quote")

    def get_dividends(self, **kwargs):
        """Dividends

        Reference: https://iexcloud.io/docs/api/#dividends

        Data Weighting: ``10`` per symbol per period returned

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of dividends to return
            Choose from [`5y`,`2y`,`1y`,`ytd`,`6m`,`3m`,`1m`, `next`]

        Returns
        -------
        list of dict or pandas.DataFrame
            Stocks Dividends endpoint data
        """
        def fmt_p(out):
            data = {(symbol, sheet["exDate"]): sheet for symbol in out
                    for sheet in out[symbol]}
            return pd.DataFrame(data)
        return self._get_endpoint("dividends", fmt_p=fmt_p, params=kwargs)

    def get_earnings(self, **kwargs):
        """Earnings

        Earnings data for a given company including the actual EPS, consensus,
        and fiscal period. Earnings are available quarterly (last 4 quarters)
        and annually (last 4 years).

        Reference: https://iexcloud.io/docs/api/#earnings

        Data Weighting: ``1000`` per symbol per period

        Parameters
        ----------
        last: int, default 1, optional
            Number of quarters or years to return.

        Returns
        -------
        list or pandas.DataFrame
            Stocks Earnings endpoint data
        """
        def fmt(out):
            return {symbol: out[symbol]["earnings"] for symbol in self.symbols}

        def fmt_p(out):
            data = {(symbol, sheet["EPSReportDate"]): sheet for symbol in out
                    for sheet in out[symbol]["earnings"]}
            return pd.DataFrame(data)
        return self._get_endpoint("earnings", fmt_j=fmt, fmt_p=fmt_p,
                                  params=kwargs)

    def get_effective_spread(self):
        """
        DEPRECATED: Deprecated in IEX Cloud. No longer available.
        """
        raise ImmediateDeprecationError()
        return self._get_endpoint("effective-spread")

    def get_estimates(self):
        """Estimates

        Provides the latest consensus estimate for the next fiscal period

        Reference: https://iexcloud.io/docs/api/#estimates

        Data Weighting: ``10000`` per symbol per period

        .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

        Returns
        -------
        dict or pandas.DataFrame
        """
        def fmt_p(out):
            data = {(symbol, sheet["reportDate"]): sheet for symbol in out
                    for sheet in out[symbol]["estimates"]}
            return pd.DataFrame(data)

        return self._get_endpoint("estimates", fmt_p=fmt_p)

    def get_financials(self, **kwargs):
        """Financials

        Pulls income statement, balance sheet, and cash flow data from the
        most recent reported quarter.

        Reference: https://iexcloud.io/docs/api/#financials

        Data Weighting: ``5000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarter', choose between 'annual' and 'quarter'

        Returns
        -------
        list or pandas.DataFrame
            Stocks Financials endpoint data
        """
        # def fmt(out):
        #     return {symbol: out[symbol].get("financials", [])
        #             for symbol in self.symbols}
        def fmt(out):
            return {symbol: out[symbol]["financials"]
                    for symbol in self.symbols}

        def fmt_p(out):
            out = {symbol: out[symbol].get("financials", [])
                   for symbol in self.symbols}
            data = {(symbol, sheet["reportDate"]): sheet
                    for symbol in out
                    for sheet in out[symbol]}
            return pd.DataFrame(data)
        return self._get_endpoint("financials", fmt_j=fmt,
                                  fmt_p=fmt_p, params=kwargs)

    def get_fund_ownership(self):
        """Fund Ownership

        Returns the top 10 fund holders, meaning any firm not defined as
        buy-side or sell-side such as mutual funds, pension funds, endowments,
        investment firms, and other large entities that manage funds on behalf
        of others.

        Reference: https://iexcloud.io/docs/api/#fund-ownership

        Data Weighting: ``10000`` per symbol per period

        Returns
        -------
        list or pandas.DataFrame
            Stocks Fund Ownership endpoint data
        """
        def fmt_p(out):
            out = {(symbol, owner["entityProperName"]): owner
                   for symbol in out
                   for owner in out[symbol]}
            return pd.DataFrame(out)

        return self._get_endpoint("fund-ownership", fmt_p=fmt_p)

    def get_historical_prices(self, **kwargs):
        """Historical Prices

        Reference: https://iexcloud.io/docs/api/#chart

        Data Weighting: See IEX Cloud Docs

        Parameters
        ----------
        range: str, default '1m', optional
            Chart range to return. See docs.
            Choose from [`5y`,`2y`,`1y`,`ytd`,`6m`,`3m`,`1m`,`1d`,`date`,
            `dynamic`]
            Choosing `date` will return  IEX-only data by minute for a
            specified date in the format YYYYMMDD if available.
            Currently supporting trailing 30 calendar days.
            Choosing `dynamic` will return `1d` or `1m` data depending on
            the day or week and time of day.
            Intraday per minute data is only returned during market hours.
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
        chartCloseOnly: boolean, default False, optional
            Specify to return adjusted data only with keys ``date``, ``close``,
            and ``volume``.
        chartIEXOnly: boolean, default False, optional
            Only for ``1d``. Limits the return of intraday prices to IEX only
            data

        Returns
        -------
        list or pandas DataFrame
            Stocks Historical Prices endpoint data
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

    def get_income_statement(self, **kwargs):
        """Income Statement

        Pulls income statement data. Available quarterly (4 quarters) or
        annually (4 years).

        Reference: https://iexcloud.io/docs/api/#income-statement

        Data Weighting: ``1000`` per symbol per period

        .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

        Parameters
        ----------
        period: str, default 'quarterly', optional
             Allows you to specify annual or quarterly income statement.
             Defaults to quarterly. Values should be annual or quarter

        Returns
        -------
        list or pandas.DataFrame
            Stocks Income Statement endpoint data
        """
        def fmt(out):
            return {symbol: out[symbol]["income"]
                    for symbol in self.symbols}

        def fmt_p(out):
            data = {(symbol, sheet["reportDate"]): sheet for symbol in out
                    for sheet in out[symbol]["income"]}
            return pd.DataFrame(data)

        return self._get_endpoint("income", fmt_j=fmt, fmt_p=fmt_p,
                                  params=kwargs)

    def get_insider_roster(self):
        """Insider Roster

        Returns the top 10 insiders, with the most recent information.

        Reference: https://iexcloud.io/docs/api/#insider-roster

        Data Weighting: ``5000`` per symbol

        Returns
        -------
        list or pandas.DataFrame
            Stocks Insider Roster Endpoint data
        """
        def fmt_p(out):
            out = {(symbol, owner["entityName"]): owner
                   for symbol in out
                   for owner in out[symbol]}
            return pd.DataFrame(out)

        return self._get_endpoint("insider-roster", fmt_p=fmt_p)

    def get_insider_summary(self):
        """Insider Summary

        Returns aggregated insiders summary data for the last 6 months.

        Reference: https://iexcloud.io/docs/api/#insider-summary

        Data Weighting: ``5000`` per symbol

        Returns
        -------
        list or pandas.DataFrame
            Stocks Insider Summary Endpoint data
        """
        def fmt_p(out):
            out = {(symbol, owner["fullName"]): owner
                   for symbol in out
                   for owner in out[symbol]}
            return pd.DataFrame(out)

        return self._get_endpoint("insider-summary", fmt_p=fmt_p)

    def get_insider_transactions(self):
        """Insider Transactions

        Returns insider transactions.

        Reference: https://iexcloud.io/docs/api/#insider-transactions

        Data Weighting: ``50`` per transaction

        Returns
        -------
        list or pandas.DataFrame
            Stocks Insider Transactions Endpoint data
        """
        def fmt_p(out):
            out = {(symbol, owner["fullName"]): owner
                   for symbol in out
                   for owner in out[symbol]}
            return pd.DataFrame(out)

        return self._get_endpoint("insider-transactions", fmt_p=fmt_p)

    def get_institutional_ownership(self):
        """Institutional Ownership

        Returns the top 10 institutional holders, defined as buy-side or
        sell-side firms.

        Reference: https://iexcloud.io/docs/api/#institutional-ownership

        Data Weighting: ``10000`` per symbol per period

        Returns
        -------
        list or pandas.DataFrame
            Stocks Institutional Ownership endpoint data
        """
        def fmt_p(out):
            out = {(symbol, owner["entityProperName"]): owner
                   for symbol in out
                   for owner in out[symbol]}
            return pd.DataFrame(out)

        return self._get_endpoint("institutional-ownership", fmt_p=fmt_p)

    def get_key_stats(self, **kwargs):
        """
        Reference: https://iexcloud.io/docs/api/#key-stats

        Parameters
        ----------
        stat: str, optional
            Case sensitive string matching the name of a single key
            to return one value.Ex: If you only want the next earnings
            date, you would use `nextEarningsDate`.

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Key Stats endpoint data
        """
        return self._get_endpoint("stats", params=kwargs)

    def get_largest_trades(self):
        """
        Reference: https://iexcloud.io/docs/api/#largest-trades

        Returns
        -------
        list or pandas.DataFrame
            Stocks Largest Trades endpoint data
        """
        return self._get_endpoint("largest-trades")

    def get_logo(self):
        """
        Reference: https://iexcloud.io/docs/api/#logo

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Logo endpoint data
        """
        return self._get_endpoint("logo")

    def get_news(self, **kwargs):
        """News

        Reference: https://iexcloud.io/docs/api/#news

        Data Weighting: ``10`` per symbol per news item returned

        Parameters
        ----------
        last: int, default 10, optional
            Number of news listings to return.

        Returns
        -------
        list or dict
            Stocks News endpoint data
        """
        return self._get_endpoint("news", fmt_p=no_pandas, params=kwargs)

    def get_ohlc(self):
        """OHLC

        Returns the official open and close for a give symbol.

        Reference:  https://iexcloud.io/docs/api/#ohlc

        Data Weighting: ``2`` per symbol

        Returns
        -------
        dict or pandas.DataFrame
            Stocks OHLC endpoint data
        """
        return self._get_endpoint("ohlc")

    def get_open_close(self):
        """Open/Close Price

        Reference: https://iexcloud.io/docs/api/#open-close-price

        Data Weighting: ``2`` per symbol

        Notes
        -----
        Open/Close Price is an alias for the OHLC endpoint, and will return the
        same

        Returns
        -------
        list or pandas.DataFrame
            Stocks Open/Close (OHLC) endpoint data
        """
        return self._get_endpoint("ohlc")

    def get_peers(self):
        """Peers

        Reference:https://iexcloud.io/docs/api/#peers

        Data Weighting: ``500`` per call

        Notes
        -----
        Only allows JSON format (pandas not supported).

        Returns
        -------
        list
            Stocks Peers endpoint data
        """
        return self._get_endpoint("peers")

    def get_previous(self, **kwargs):
        """
        DEPRECATED: Renamed ``get_previous_day_prices``
        """
        raise ImmediateDeprecationError("get_previous")

    def get_previous_day_prices(self):
        """Previous Day Prices

        This returns previous day adjusted price data for one or more stocks

        Reference: https://iexcloud.io/docs/api/#previous

        Data Weighting: ``2`` per symbol

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Previous Day Prices endpoint data
        """
        return self._get_endpoint("previous")

    def get_price(self):
        """Price

        Reference: https://iexcloud.io/docs/api/#price

        ``1`` per symbol

        Returns
        -------
        float or pandas.DataFrame
            Stocks Price endpoint data
        """
        def fmt_p(out):
            return pd.DataFrame(out, index=self.symbols)

        return self._get_endpoint("price", fmt_p=fmt_p)

    def get_price_target(self):
        """Price Target

        Provides the latest avg, high, and low analyst price target for a
        symbol.

        Reference: https://iexcloud.io/docs/api/#price-target

        Data Weighting: ``500`` per symbol

        .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

        Returns
        -------
        dict or pandas.DataFrame
            Latest average, high, and low price targets for a symbol
        """
        def fmt_p(out):
            if len(self.symbols) == 1:
                return pd.DataFrame(out, index=self.symbols[0])
            return pd.DataFrame(out)

        return self._get_endpoint('price-target')

    def get_quote(self, **kwargs):
        """Quote

        Reference: https://iexcloud.io/docs/api/#quote

        Data Weighting: ``1`` per quote

        Parameters
        ----------
        displayPercent: bool, defaults to false, optional
            If set to true, all percentage values will be
            multiplied by a factor of 100.

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Quote endpoint data
        """
        return self._get_endpoint("quote", params=kwargs)

    def get_relevant(self, **kwargs):
        """
        DEPRECATED: Renamed ``get_relevant_stocks``
        """
        raise ImmediateDeprecationError("get_relevant")

    def get_relevant_stocks(self, **kwargs):
        """Relevant Stocks

        Similar to the peers endpoint, except this will return most active
        market symbols when peers are not available. If the symbols
        returned are not peers, the peers key will be false.
        This is not intended to represent a definitive or accurate
        list of peers, and is subject to change at any time.

        Reference: https://iexcloud.io/docs/api/#relevant-stocks

        Data Weighting: ``500`` per call

        Returns
        -------
        dict or pandas.DataFrame
            Stocks Relevant Stocks endpoint data
        """
        return self._get_endpoint("relevant", params=kwargs)

    def get_splits(self, **kwargs):
        """Splits


        Reference: https://iexcloud.io/docs/api/#splits

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of splits to return.
            Choose from [`5y`,`2y`,`1y`,`ytd`,`6m`,`3m`,`1m`, `next`].

        Returns
        -------
        list
            Stocks Splits endpoint data
        """
        return self._get_endpoint("splits", params=kwargs, fmt_p=no_pandas)

    def get_time_series(self, **kwargs):
        """Time Series

        MOVED in IEX Cloud

        .. seealso:: ``get_historical_prices``
        """
        return self._get_endpoint("chart", params=kwargs)

    def get_volume_by_venue(self):
        """Volume by Venue

        Reference:  https://iexcloud.io/docs/api/#volume-by-venue

        Data Weighting: ``20`` per call

        Returns
        -------
        list or pandas.DataFrame
            Stocks Volume by Venue endpoint data
        """
        def fmt_p(out):
            data = {(symbol, sheet["venueName"]): sheet for symbol in out
                    for sheet in out[symbol]}
            return pd.DataFrame(data)

        return self._get_endpoint("volume-by-venue",
                                  fmt_p=fmt_p)

    # field methods
    def get_company_name(self):
        return self._get_field("quote", "companyName")

    def get_primary_exchange(self):
        return self._get_field("company", "exchange")

    def get_sector(self):
        return self._get_field("company", "sector")

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
