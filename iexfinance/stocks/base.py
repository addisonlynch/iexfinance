import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import _handle_lists, no_pandas
from iexfinance.utils.exceptions import ImmediateDeprecationError


class Stock(_IEXBase):
    """
    Base class for obtaining data from the Stock endpoints of IEX.

    Attributes
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index)
        Symbol or list-like collection of symbols
    output_format: str, default 'pandas', optional
    token: str, optional
        Authentication token (required for use with IEX Cloud)
    """

    def __init__(self, symbols=None, **kwargs):
        if isinstance(symbols, str) and symbols:
            self.symbols = [symbols]
        elif isinstance(symbols, list) and 0 < len(symbols) <= 100:
            self.symbols = symbols
        elif isinstance(symbols, list) and 100 < len(symbols):
            raise ValueError(
                "Please input a symbols list containing between" " 0 and 100 symbols"
            )
        else:
            raise ValueError("Please input a symbol or list of symbols")
        self.symbols = list(map(lambda x: x.upper(), _handle_lists(symbols)))
        self.endpoints = []
        super(Stock, self).__init__(**kwargs)

    def __repr__(self):
        return "{}(symbols={}, output_format={!r})".format(
            self.__class__.__name__, ",".join(self.symbols), self.output_format
        )

    @property
    def single_symbol(self):
        return True if len(self.symbols) == 1 else False

    @property
    def url(self):
        return "stock/market/batch"

    @property
    def params(self):
        temp = {"symbols": ",".join(self.symbols), "types": ",".join(self.endpoints)}
        temp.update(self.optional_params)
        if "filter_" in temp:
            if isinstance(temp["filter_"], list):
                temp["filter"] = ",".join(temp.pop("filter_"))
            else:
                temp["filter"] = temp.pop("filter_")
        if "range_" in temp:
            temp["range"] = temp.pop("range_")
        params = {
            k: str(v).lower() if v is True or v is False else str(v)
            for k, v in temp.items()
        }
        return params

    def _get_endpoint(self, endpoint, params=(), format=None, filter_=None):
        result = {}
        if filter_:
            params.update({"filter": filter_})
        self.optional_params = params
        self.endpoints = [endpoint]

        data = self.fetch(format=no_pandas)
        # IEX Cloud returns multiple symbol requests as as a list of dicts
        # so convert to dict of dicts
        if isinstance(data, list):
            data = data[0]
        for symbol in self.symbols:
            if symbol not in data:
                continue
            if endpoint not in data[symbol]:
                result[symbol] = []
            else:
                result[symbol] = data[symbol][endpoint]
        return self._output_format_one(result, format=format)

    def _get_field(self, endpoint, field):
        try:
            data = getattr(self, "get_%s" % endpoint)(filter_=field)
        except AttributeError:
            raise NotImplementedError("Endpoint %s not implemented." % endpoint)
        if field not in data:
            raise KeyError("Field %s not found in %s." % (field, endpoint))
        if self.output_format == "json":
            if self.single_symbol:
                data = data[field]
            else:
                data = {symbol: data[symbol][field] for symbol in self.symbols}
        else:
            if self.single_symbol:
                return data[field][0]
        return data

    def _output_format_one(self, out, format=None):
        data = super(Stock, self)._format_output(out, format=format)
        # transpose DF
        try:
            data = data.T if self.output_format == "pandas" else data
        except Exception:
            pass
        if self.single_symbol and self.output_format == "json":
            return data[self.symbols[0]]
        return data

    def get_endpoints(self, endpoints=()):
        """
        DEPRECATED: This method has been deprecated as of 0.5.0
        """
        raise ImmediateDeprecationError("get_endpoints")

    """
    STOCK PRICES
    """

    def get_book(self):
        """Book

        Reference: https://iexcloud.io/docs/api/#book

        .. note:: This endpoint does not support pandas ``DataFrame`` output
                  formatting.

        Data Weighting: ``1`` per quote returned
        """
        return self._get_endpoint("book", format=no_pandas)

    def get_chart(self, **kwargs):
        """Chart

        .. seealso:: ``get_historical_prices``
        """
        return self.get_historical_prices(**kwargs)

    def get_delayed_quote(self):
        """Delayed Quote

        Reference: https://iexcloud.io/docs/api/#delayed-quote

        Data Weighting: ``1`` per symbol per quote
        """
        return self._get_endpoint("delayed-quote")

    def get_historical_prices(self, **kwargs):
        """Historical Prices

        Reference: https://iexcloud.io/docs/api/#chart

        Data Weighting: See IEX Cloud documentation

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
        """

        def format(out):
            if len(self.symbols) > 1:
                out = {
                    (symbol, day["date"]): day for symbol in out for day in out[symbol]
                }
                return pd.DataFrame.from_dict(out, orient="columns").drop("date")
            else:
                out = {entr["date"]: entr for entr in out[self.symbols[0]]}
                return pd.DataFrame.from_dict(out, orient="columns").drop("date")

        return self._get_endpoint("chart", format=format, params=kwargs)

    def get_intraday_prices(self, **kwargs):
        """Intraday Prices

        Reference: https://iexcloud.io/docs/api/#intraday-prices

        Data Weighting:
        ``1`` per symbol per time interval up to a max use of 50 messages
        Example: If you query for twtr 1d at 11:00am, it will return 90
        minutes of data for a total of 50.

        IEX Only intraday minute bar - Free
        This will only return IEX data with keys minute, high, low, average,
        volume, notional, and numberOfTrades.
        Use the chartIEXOnly param

        : boolean, optional

        Parameters
        ----------
        last: int, default 10, optional
            Number of news listings to return.
        chartIEXOnly: boolean, optional
            Limits the return of intraday prices to IEX only data.
        chartReset: boolean, optional
            If true, chart will reset at midnight instead of the default
            behavior of 9:30am ET.
        chartSimplify: boolean, optional
            If true, runs a polyline simplification using the Douglas-Peucker
            algorithm. This is useful if plotting sparkline charts.
        chartInterval: number, optional
            If passed, chart data will return every Nth element as defined by
            chartInterval
        changeFromClose: boolean, optional
            If true, changeOverTime and marketChangeOverTime will be relative
            to previous day close instead of the first value.
        chartLast: number, optional
            If passed, chart data will return the last N elements
        exactDate: string, optional
            Formatted as YYYYMMDD. This can be used for batch calls when range
            is 1d or date.
        chartIEXWhenNull: boolean, optional
            By default, all market prefixed fields are 15 minute delayed,
            meaning the most recent 15 objects will be null.
            If this parameter is passed as true, all market prefixed fields
            that are null will be populated with IEX data if available.
        """

        def format(out):
            if len(self.symbols) > 1:
                out = {
                    (symbol, "{} {}".format(day["date"], day["label"])): day
                    for symbol in out
                    for day in out[symbol]
                }
                return pd.DataFrame.from_dict(out, orient="columns").drop("date")
            else:
                out = {
                    "{} {}".format(entr["date"], entr["label"]): entr
                    for entr in out[self.symbols[0]]
                }
                return pd.DataFrame.from_dict(out, orient="columns").drop("date")

        return self._get_endpoint("intraday-prices", format=format, params=kwargs)

    def get_largest_trades(self):
        """
        Reference: https://iexcloud.io/docs/api/#largest-trades
        """
        return self._get_endpoint("largest-trades")

    def get_open_close(self):
        """Open/Close Price

        Reference: https://iexcloud.io/docs/api/#open-close-price

        Data Weighting: ``2`` per symbol

        Notes
        -----
        Open/Close Price is an alias for the OHLC endpoint, and will return the
        same
        """
        return self._get_endpoint("ohlc")

    def get_ohlc(self):
        """OHLC

        Returns the official open and close for a give symbol.

        Reference:  https://iexcloud.io/docs/api/#ohlc

        Data Weighting: ``2`` per symbol
        """
        return self._get_endpoint("ohlc")

    def get_previous_day_prices(self):
        """Previous Day Prices

        This returns previous day adjusted price data for one or more stocks

        Reference: https://iexcloud.io/docs/api/#previous

        Data Weighting: ``2`` per symbol
        """
        return self._get_endpoint("previous")

    def get_price(self):
        """Price

        Reference: https://iexcloud.io/docs/api/#price

        ``1`` per symbol
        """

        def format(out):
            return pd.DataFrame.from_dict(out, orient="index", columns=["price"])

        return self._get_endpoint("price", format=format)

    def get_quote(self, **kwargs):
        """Quote

        Reference: https://iexcloud.io/docs/api/#quote

        Data Weighting: ``1`` per quote

        Parameters
        ----------
        displayPercent: bool, defaults to false, optional
            If set to true, all percentage values will be
            multiplied by a factor of 100.
        """
        return self._get_endpoint("quote", params=kwargs)

    def get_time_series(self, **kwargs):
        """Time Series

        .. seealso:: ``get_historical_prices``
        """
        return self.get_historical_prices(**kwargs)

    def get_volume_by_venue(self):
        """Volume by Venue

        Reference:  https://iexcloud.io/docs/api/#volume-by-venue

        Data Weighting: ``20`` per call
        """

        def format(out):
            data = {
                (symbol, sheet["venueName"]): sheet
                for symbol in out
                for sheet in out[symbol]
            }
            return pd.DataFrame(data)

        return self._get_endpoint("volume-by-venue", format=format)

    """
    STOCK PROFILES
    """

    def get_company(self, **kwargs):
        """Company

        Reference: https://iexcloud.io/docs/api/#company

        Data Weighting: ``1``
        """
        return self._get_endpoint("company", params=kwargs)

    def get_insider_roster(self):
        """Insider Roster

        Returns the top 10 insiders, with the most recent information.

        Reference: https://iexcloud.io/docs/api/#insider-roster

        Data Weighting: ``5000`` per symbol
        """

        def format(out):
            out = {
                (symbol, owner["entityName"]): owner
                for symbol in out
                for owner in out[symbol]
            }
            return pd.DataFrame(out)

        return self._get_endpoint("insider-roster", format=format)

    def get_insider_summary(self):
        """Insider Summary

        Returns aggregated insiders summary data for the last 6 months.

        Reference: https://iexcloud.io/docs/api/#insider-summary

        Data Weighting: ``5000`` per symbol
        """

        def format(out):
            out = {
                (symbol, owner["fullName"]): owner
                for symbol in out
                for owner in out[symbol]
            }
            return pd.DataFrame(out)

        return self._get_endpoint("insider-summary", format=format)

    def get_insider_transactions(self):
        """Insider Transactions

        Returns insider transactions.

        Reference: https://iexcloud.io/docs/api/#insider-transactions

        Data Weighting: ``50`` per transaction
        """

        def format(out):
            out = {
                (symbol, owner["fullName"]): owner
                for symbol in out
                for owner in out[symbol]
            }
            return pd.DataFrame(out)

        return self._get_endpoint("insider-transactions", format=format)

    def get_logo(self):
        """
        Reference: https://iexcloud.io/docs/api/#logo
        """
        return self._get_endpoint("logo")

    def get_peers(self):
        """Peers

        Reference:https://iexcloud.io/docs/api/#peers

        Data Weighting: ``500`` per call

        Notes
        -----
        Only allows JSON format (pandas not supported).
        """
        return self._get_endpoint("peers")

    """
    STOCK FUNDAMENTALS
    """

    def get_balance_sheet(self, **kwargs):
        """Balance Sheet

        Pulls balance sheet data. Available quarterly (12 quarters) and annually
        (4 years)

        Reference: https://iexcloud.io/docs/api/#balance-sheet

        Data Weighting: ``3000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarter', optional
            Allows you to specify annual or quarterly balance sheet.
            Value should be `annual` or `quarter`.
        last: int, default 1, optional
            Specify the number of quarters or years to return. You can specify
            up to 12 quarters or 4 years.
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["reportDate"]: d for d in out[symbol]["balancesheet"]},
                        orient="index",
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("balance-sheet", format=format, params=kwargs)

    def get_cash_flow(self, **kwargs):
        """Cash Flow

        Pulls cash flow data. Available quarterly (4 quarters) or annually
        (4 years).

        Reference: https://iexcloud.io/docs/api/#cash-flow

        Data Weighting: ``1000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarter', optional
            Allows you to specify annual or quarterly cash flows.
            Value should be `annual` or `quarter`.
        last: int, default 1, optional
            Specify the number of quarters or years to return. You can specify
            up to 12 quarters or 4 years.
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["reportDate"]: d for d in out[symbol]["cashflow"]},
                        orient="index",
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("cash-flow", format=format, params=kwargs)

    def get_dividends(self, **kwargs):
        """Dividends

        Reference: https://iexcloud.io/docs/api/#dividends

        Data Weighting: ``10`` per symbol per period returned

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of dividends to return
            Choose from [`5y`,`2y`,`1y`,`ytd`,`6m`,`3m`,`1m`, `next`]
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["exDate"]: d for d in out[symbol]}, orient="index"
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("dividends", format=format, params=kwargs)

    def get_earnings(self, **kwargs):
        """Earnings

        Earnings data for a given company including the actual EPS, consensus,
        and fiscal period. Earnings are available quarterly (last 4 quarters)
        and annually (last 4 years).

        Reference: https://iexcloud.io/docs/api/#earnings

        Data Weighting: ``1000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarter', optional
            Allows you to specify annual or quarterly earnings.
            Value should be `annual` or `quarter`.
        last: int, default 1, optional
            Specify the number of quarters or years to return. You can specify
            up to 4 quarters or 4 years.
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["EPSReportDate"]: d for d in out[symbol]["earnings"]},
                        orient="index",
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("earnings", format=format, params=kwargs)

    def get_financials(self, **kwargs):
        """Financials

        Pulls income statement, balance sheet, and cash flow data from the
        most recent reported quarter.

        Reference: https://iexcloud.io/docs/api/#financials

        Data Weighting: ``5000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarter', optional
            Allows you to specify annual or quarterly financials.
            Value should be `annual` or `quarter`.
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["reportDate"]: d for d in out[symbol]["financials"]},
                        orient="index",
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("financials", format=format, params=kwargs)

    def get_income_statement(self, **kwargs):
        """Income Statement

        Pulls income statement data. Available quarterly (4 quarters) or
        annually (4 years).

        Reference: https://iexcloud.io/docs/api/#income-statement

        Data Weighting: ``1000`` per symbol per period

        Parameters
        ----------
        period: str, default 'quarterly', optional
             Allows you to specify annual or quarterly income statement.
             Defaults to quarterly. Values should be annual or quarter
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["reportDate"]: d for d in out[symbol]["income"]},
                        orient="index",
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("income", format=format, params=kwargs)

    def get_splits(self, **kwargs):
        """Splits


        Reference: https://iexcloud.io/docs/api/#splits

        Parameters
        ----------
        range: str, default '1m', optional
            Time period of splits to return.
            Choose from [`5y`,`2y`,`1y`,`ytd`,`6m`,`3m`,`1m`, `next`].
        """

        def format(out):
            results = {}
            for symbol in out:
                if out[symbol]:
                    results[symbol] = pd.DataFrame.from_dict(
                        {d["exDate"]: d for d in out[symbol]}, orient="index"
                    )
                else:
                    results[symbol] = pd.DataFrame()
            return results[self.symbols[0]].T if self.single_symbol else results

        return self._get_endpoint("splits", params=kwargs, format=format)

    """
    STOCK RESEARCH
    """

    def get_advanced_stats(self, **kwargs):
        """
        Reference: https://iexcloud.io/docs/api/#advanced-stats

        Data Weighting: ``3,000`` per symbol + Key Stats weight

        Notes
        -------
        Only included with paid subscription plans.
        """
        return self._get_endpoint("advanced-stats", params=kwargs)

    def get_estimates(self, **kwargs):
        """Estimates

        Provides the latest consensus estimate for the next fiscal period

        Reference: https://iexcloud.io/docs/api/#estimates

        Data Weighting: ``10000`` per symbol per period

        Parameters
        ----------
        last: int, default 1, optional
        period: str, default `quarter`, optional
        """

        def format(out):
            data = {
                (symbol, sheet["reportDate"]): sheet
                for symbol in out
                for sheet in out[symbol]["estimates"]
            }
            return pd.DataFrame(data)

        return self._get_endpoint("estimates", format=format, params=kwargs)

    def get_fund_ownership(self):
        """Fund Ownership

        Returns the top 10 fund holders, meaning any firm not defined as
        buy-side or sell-side such as mutual funds, pension funds, endowments,
        investment firms, and other large entities that manage funds on behalf
        of others.

        Reference: https://iexcloud.io/docs/api/#fund-ownership

        Data Weighting: ``10000`` per symbol per period
        """

        def format(out):
            out = {
                (symbol, owner["entityProperName"]): owner
                for symbol in out
                for owner in out[symbol]
            }
            return pd.DataFrame(out)

        return self._get_endpoint("fund-ownership", format=format)

    def get_institutional_ownership(self):
        """Institutional Ownership

        Returns the top 10 institutional holders, defined as buy-side or
        sell-side firms.

        Reference: https://iexcloud.io/docs/api/#institutional-ownership

        Data Weighting: ``10000`` per symbol per period
        """

        def format(out):
            out = {
                (symbol, owner["entityProperName"]): owner
                for symbol in out
                for owner in out[symbol]
            }
            return pd.DataFrame(out)

        return self._get_endpoint("institutional-ownership", format=format)

    def get_key_stats(self, **kwargs):
        """
        Reference: https://iexcloud.io/docs/api/#key-stats

        Parameters
        ----------
        stat: str, optional
            Case sensitive string matching the name of a single key
            to return one value.Ex: If you only want the next earnings
            date, you would use `nextEarningsDate`.
        """
        return self._get_endpoint("stats", params=kwargs)

    def get_price_target(self):
        """Price Target

        Provides the latest avg, high, and low analyst price target for a
        symbol.

        Reference: https://iexcloud.io/docs/api/#price-target

        Data Weighting: ``500`` per symbol
        """

        def format(out):
            if self.symbols[0] in out:
                pass

        return self._get_endpoint("price-target")

    """
    NEWS
    """

    def get_news(self, **kwargs):
        """News

        Reference: https://iexcloud.io/docs/api/#news

        Data Weighting: ``1`` per symbol per news item returned

        Parameters
        ----------
        last: int, default 10, optional
            Number of news listings to return. Value must be between
            1 and 50.
        """

        def format(out):
            if len(self.symbols) > 1:
                out = {
                    (symbol, day["datetime"]): day
                    for symbol in out
                    for day in out[symbol]
                }
                return pd.DataFrame.from_dict(out, orient="columns").drop("datetime")
            else:
                out = {entr["datetime"]: entr for entr in out[self.symbols[0]]}
                return pd.DataFrame.from_dict(out, orient="columns").drop("datetime")

        return self._get_endpoint("news", format=format, params=kwargs)

    def get_relevant_stocks(self, **kwargs):
        """Relevant Stocks

        Similar to the peers endpoint, except this will return most active
        market symbols when peers are not available. If the symbols
        returned are not peers, the peers key will be false.
        This is not intended to represent a definitive or accurate
        list of peers, and is subject to change at any time.

        Reference: https://iexcloud.io/docs/api/#relevant-stocks

        Data Weighting: ``500`` per call
        """
        raise ImmediateDeprecationError("get_relevant_stocks")

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
        raise ImmediateDeprecationError("get_short_interest")

    def get_short_ratio(self):
        raise ImmediateDeprecationError("get_short_ratio")

    def get_latest_eps(self):
        raise ImmediateDeprecationError("get_latest_eps")

    def get_shares_outstanding(self):
        return self._get_field("key_stats", "sharesOutstanding")

    def get_float(self):
        return self._get_field("key_stats", "float")

    def get_eps_consensus(self):
        raise ImmediateDeprecationError("get_eps_conesnsus")
