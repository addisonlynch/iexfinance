from iexfinance.iexdata.base import (TOPS, Last, DEEP, Book, IntradayReader,
                                     RecentReader, RecordsReader,
                                     DailySummaryReader, MonthlySummaryReader)
from iexfinance.utils import _sanitize_dates


def get_tops(symbols=None, **kwargs):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return TOPS(symbols, **kwargs).fetch()


def get_last(symbols=None, **kwargs):
    """
    Top-level function to obtain Last data for a symbol or list of symbols

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return Last(symbols, **kwargs).fetch()


def get_deep(symbols=None, **kwargs):
    """
    Top-level function to obtain DEEP data for a symbol or list of symbols

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list, default None
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)

    Notes
    -----
    Pandas not supported as an output format for the DEEP endpoint.
    """
    return DEEP(symbols, **kwargs).fetch()


def get_deep_book(symbols=None, **kwargs):
    """
    Top-level function to obtain Book data for a symbol or list of symbols

    Data Weighting: ``Free``

    Parameters
    ----------
    symbols: str or list, default None
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return Book(symbols, **kwargs).fetch()


def get_stats_intraday(**kwargs):
    """
    Top-level function for obtaining data from the Intraday endpoint of IEX
    Stats

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return IntradayReader(**kwargs).fetch()


def get_stats_recent(**kwargs):
    """
    Top-level function for obtaining data from the Recent endpoint of IEX Stats

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return RecentReader(**kwargs).fetch()


def get_stats_records(**kwargs):
    """
    Top-level function for obtaining data from the Records endpoint of IEX
    Stats

    Data Weighting: ``Free``

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return RecordsReader(**kwargs).fetch()


def get_stats_daily(start=None, end=None, last=None, **kwargs):
    """
    Top-level function for obtaining data from the Historical Daily endpoint
    of IEX Stats

    Data Weighting: ``Free``

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        Start of data retrieval period
    end: datetime.datetime, default None, optional
        End of data retrieval period
    last: int, default None, optional
        Used in place of date range to retrieve previous number of trading days
        (up to 90)
    kwargs:
        Additional Request Parameters (see base class)
    """
    start, end = _sanitize_dates(start, end)
    return DailySummaryReader(start=start, end=end, last=last,
                              **kwargs).fetch()


def get_stats_monthly(start=None, end=None, **kwargs):
    """
    Top-level function for obtaining data from the Historical Summary endpoint
    of IEX Stats

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
