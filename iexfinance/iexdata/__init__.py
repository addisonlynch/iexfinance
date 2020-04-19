from iexfinance.iexdata.base import (
    TOPS,
    Last,
    DEEP,
    Book,
    IntradayReader,
    RecentReader,
    RecordsReader,
    DailySummaryReader,
    MonthlySummaryReader,
)


def get_tops(symbols=None, **kwargs):
    """
    TOPS data for a symbol or list of symbols.

    TOPS provides IEX's aggregated best quoted bid and offer position in near
    real time for all securities on IEX's displayed limit order book. TOPS is
    ideal for developers needing both quote and trade data.

    Reference: https://iexcloud.io/docs/api/#tops

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index),
             default ``None``, optional
        Symbol or list-like collection of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return TOPS(symbols, **kwargs).fetch()


def get_last(symbols=None, **kwargs):
    """
    Last data for a symbol or list of symbols

    Last provides trade data for executions on IEX. It is a near real time,
    intraday API that provides IEX last sale price, size and time. Last is
    ideal for developers that need a lightweight stock quote.

    Reference: https://iexcloud.io/docs/api/#last

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index),
             default ``None``, optional
    kwargs:
        Additional Request Parameters (see base class)
    """
    return Last(symbols, **kwargs).fetch()


def get_deep(symbols=None, **kwargs):
    """
    DEEP data for a symbol or list of symbols

    DEEP is used to receive real-time depth of book quotations direct from IEX.
    The depth of book quotations received via DEEP provide an aggregated size
    of resting displayed orders at a price and side, and do not indicate the
    size or number of individual orders at any price level. Non-displayed
    orders and non-displayed portions of reserve orders are not represented in
    DEEP.

    DEEP also provides last trade price and size information. Trades resulting
    from either displayed or non-displayed orders matching on IEX will be
    reported. Routed executions will not be reported.

    Reference: https://iexcloud.io/docs/api/#deep

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index),
             default ``None``, optional
    kwargs:
        Additional Request Parameters (see base class)

    Notes
    -----
    Pandas not supported as an output format for the DEEP endpoint.
    """
    return DEEP(symbols, **kwargs).fetch()


def get_deep_book(symbols=None, **kwargs):
    """
    Book data for a symbol or list of symbols

    Book shows IEX's bids and asks for given symbols.

    Reference: https://iexcloud.io/docs/api/#deep-book
    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list-like (list, tuple, pandas.Series, pandas.Index),
             default ``None``, optional
    kwargs:
        Additional Request Parameters (see base class)
    """
    return Book(symbols, **kwargs).fetch()


def get_stats_intraday(**kwargs):
    """
    Stats Intraday

    Reference: https://iexcloud.io/docs/api/#stats-intraday

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return IntradayReader(**kwargs).fetch()


def get_stats_recent(**kwargs):
    """
    Stats Recent

    This call will return a minimum of the last five trading days up to all
    trading days of the current month.

    Reference: https://iexcloud.io/docs/api/#stats-recent

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return RecentReader(**kwargs).fetch()


def get_stats_records(**kwargs):
    """
    Stats Records

    Reference: https://iexcloud.io/docs/api/#stats-records

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return RecordsReader(**kwargs).fetch()


def get_stats_daily(start=None, end=None, last=None, **kwargs):
    """
    Stats Historical Daily

    This call will return daily stats for a given month or day.

    .. warning:: This endpoint is marked as "in development" by the provider.

    Reference: https://iexcloud.io/docs/api/#stats-historical-daily-in-dev

    Data Weighting: ``Free``

    Parameters
    ----------
    start : string, int, date, datetime, Timestamp
        Starting date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980').
        Defaults to 15 years before current date.
    end : string, int, date, datetime, Timestamp
        Ending date
    last: int, default None, optional
        Used in place of date range to retrieve previous number of trading days
        (up to 90)
    kwargs:
        Additional Request Parameters (see base class)
    """
    return DailySummaryReader(start=start, end=end, last=last, **kwargs).fetch()


def get_stats_summary(start=None, end=None, **kwargs):
    """
    Stats Historical Summary

    Reference: https://iexcloud.io/docs/api/#stats-historical-summary
    Data Weighting: ``Free``

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        Start of data retrieval period
    end: datetime.datetime, default None, optional
        End of data retrieval period
    kwargs:
        Additional Request Parameters (see base class)
    """
    return MonthlySummaryReader(start=start, end=end, **kwargs).fetch()
