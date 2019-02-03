from iexfinance import stocks
from iexfinance.base import _IEXBase
from iexfinance.stocks.base import StockReader
from iexfinance.market import TOPS, Last, DEEP, Book
from iexfinance.stats import (IntradayReader, RecentReader, RecordsReader,
                              DailySummaryReader, MonthlySummaryReader)
from iexfinance.ref import (CorporateActions, Dividends, NextDay,
                            ListedSymbolDir, Symbols, IEXSymbols)
from iexfinance.utils import _sanitize_dates
from iexfinance.utils.exceptions import IEXQueryError

__author__ = 'Addison Lynch'
__version__ = '0.3.5'

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def get_market_gainers(*args, **kwargs):
    return stocks.get_market_gainers(*args, **kwargs)


def get_market_losers(*args, **kwargs):
    return stocks.get_market_losers(*args, **kwargs)


def get_market_most_active(*args, **kwargs):
    return stocks.get_market_most_active(*args, **kwargs)


def get_market_iex_volume(*args, **kwargs):
    return stocks.get_market_iex_volume(*args, **kwargs)


def get_market_iex_percent(*args, **kwargs):
    return stocks.get_market_iex_percent(*args, **kwargs)


def get_available_symbols(**kwargs):
    """
    Top-level function to obtain IEX available symbols

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)

    Returns
    -------
    data: list
        List of dictionary reference items for each symbol
    """
    _ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"
    handler = _IEXBase(**kwargs)
    response = handler._execute_iex_query(_ALL_SYMBOLS_URL)
    if not response:
        raise IEXQueryError("Could not download all symbols")
    else:
        return response


def get_iex_corporate_actions(start=None, **kwargs):
    """
    Top-level function to retrieve IEX Corporate Actions from the ref-data
    endpoints

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        A month to use for retrieval (a datetime object)
    kwargs: Additional Request Parameters (see base class)
    """
    return CorporateActions(start=start, **kwargs).fetch()


def get_iex_dividends(start=None, **kwargs):
    """
    Top-level function to retrieve IEX Dividends from the ref-data
    endpoints

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        A month to use for retrieval (a datetime object)
    kwargs: Additional Request Parameters (see base class)
    """
    return Dividends(start=start, **kwargs).fetch()


def get_iex_next_day_ex_date(start=None, **kwargs):
    """
    Top-level function to retrieve IEX Next Day Ex Date from the ref-data
    endpoints

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        A month to use for retrieval (a datetime object)
    kwargs: Additional Request Parameters (see base class)
    """
    return NextDay(start=start, **kwargs).fetch()


def get_iex_listed_symbol_dir(start=None, **kwargs):
    """
    Top-level function to retrieve IEX Listed Symbol Directory from the
    ref-data endpoints

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        A month to use for retrieval (a datetime object)
    kwargs: Additional Request Parameters (see base class)
    """
    return ListedSymbolDir(start=start, **kwargs)


# IEX Cloud reference endpoints

def get_symbols(**kwargs):
    """
    Top-level function to retrieve array of all symbols that IEX Cloud supports
    for API calls

    Reference: https://iexcloud.io/docs/api/#symbols

    Data Weighting: ``100`` per call
    """
    return Symbols(**kwargs).fetch()


def get_iex_symbols(**kwargs):
    """
    Top-level function to retrieve array of all symbols the Investor's Exchange
    supports for trading

    Reference: https://iexcloud.io/docs/api/#iex-symbols

    Data Weighting: ``Free``
    """
    return IEXSymbols(**kwargs).fetch()


def get_market_tops(symbols=None, **kwargs):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return TOPS(symbols, **kwargs).fetch()


def get_market_last(symbols=None, **kwargs):
    """
    Top-level function to obtain Last data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    kwargs:
        Additional Request Parameters (see base class)
    """
    return Last(symbols, **kwargs).fetch()


def get_market_deep(symbols=None, **kwargs):
    """
    Top-level function to obtain DEEP data for a symbol or list of symbols

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


def get_market_book(symbols=None, **kwargs):
    """
    Top-level function to obtain Book data for a symbol or list of symbols

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

    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    """
    return IntradayReader(**kwargs).fetch()


def get_stats_recent(**kwargs):
    """
    Top-level function for obtaining data from the Recent endpoint of IEX Stats

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
