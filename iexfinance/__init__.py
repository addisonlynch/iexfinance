from .base import _IEXBase
from .stock import StockReader, HistoricalReader
from .market import TOPS, Last, DEEP, Book
from .stats import (IntradayReader, RecentReader, RecordsReader,
                    DailySummaryReader, MonthlySummaryReader)
from .ref import CorporateActions, Dividends, NextDay, ListedSymbolDir

from .utils.exceptions import IEXQueryError

__author__ = 'Addison Lynch'
__version__ = '0.3.0'

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def Stock(symbols=None, output_format='json', **kwargs):
    """
    Top-level function to to retrieve data from the IEX Stocks endpoints

    Parameters
    ----------
    symbols: str or list
        A string or list of strings that are valid symbols
    output_format: str
    kwargs:
        Additional request options
    Returns
    -------
    stock.StockReader
        A StockReader instance
    """
    if type(symbols) is str:
        if not symbols:
            raise ValueError("Please input a symbol or list of symbols")
        else:
            inst = StockReader([symbols], output_format, **kwargs)
    elif type(symbols) is list:
        if not symbols:
            raise ValueError("Please input a symbol or list of symbols")
        if len(symbols) > 100:
            raise ValueError("Invalid symbol list. Maximum 100 symbols.")
        else:
            inst = StockReader(symbols, output_format, **kwargs)
        return inst
    else:
        raise ValueError("Please input a symbol or list of symbols")
    return inst


def get_historical_data(symbols=None, start=None, end=None,
                        output_format='json', **kwargs):
    """
    Top-level function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader

    Parameters
    ----------
    symbols: str or list, default None
        A symbol or list of symbols
    start: datetime.datetime, default None
        Beginning of desired date range
    end: datetime.datetime, default None
        End of required date range
    output_format: str, (defaults to json)
        Desired output format (json or pandas)
    kwargs:
        Additional request options (see base class)

    Returns
    -------
    list or DataFrame
        Historical stock prices over date range, start to end
    """
    return HistoricalReader(symbols, start, end, output_format,
                            **kwargs).fetch()


def get_available_symbols(**kwargs):
    """
    Top-level function to obtain IEX available symbols

    Parameters
    ----------
    kwargs:
        Additional request options (see base class)

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
    kwargs: Additional request parameters
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
    kwargs: Additional request parameters
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
    kwargs: Additional request parameters
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
    kwargs: Additional request parameters
    """
    return ListedSymbolDir(start=start, **kwargs)


def get_market_tops(symbols=None, output_format='json', **kwargs):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options
    """
    return TOPS(symbols, output_format, **kwargs).fetch()


def get_market_last(symbols=None, output_format='json', **kwargs):
    """
    Top-level function to obtain Last data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None, optional
        A symbol or list of symbols
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options
    """
    return Last(symbols, output_format, **kwargs).fetch()


def get_market_deep(symbols=None, output_format='json', **kwargs):
    """
    Top-level function to obtain DEEP data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None
        A symbol or list of symbols
    output_format: str, default 'json'
        Desired output format. JSON required.
    kwargs:
        Additional request options

    Notes
    -----
    Pandas not supported as an output format for the DEEP endpoint.
    """
    return DEEP(symbols, output_format, **kwargs).fetch()


def get_market_book(symbols=None, output_format='json', **kwargs):
    """
    Top-level function to obtain Book data for a symbol or list of symbols

    Parameters
    ----------
    symbols: str or list, default None
        A symbol or list of symbols
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options
    """
    return Book(symbols, output_format, **kwargs).fetch()


def get_stats_intraday(output_format='json', **kwargs):
    """
    Top-level function for obtaining data from the Intraday endpoint of IEX
    Stats

    Parameters
    ----------
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options
    """
    return IntradayReader(output_format=output_format, **kwargs).fetch()


def get_stats_recent(output_format='json', **kwargs):
    """
    Top-level function for obtaining data from the Recent endpoint of IEX Stats

    Parameters
    ----------
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options

    """
    return RecentReader(output_format=output_format, **kwargs).fetch()


def get_stats_records(output_format='json', **kwargs):
    """
    Top-level function for obtaining data from the Records endpoint of IEX
    Stats

    Parameters
    ----------
    output_format: str, default 'json'
        Desired output format.
    kwargs:
        Additional request options
    """
    return RecordsReader(output_format=output_format, **kwargs).fetch()


def get_stats_daily(start=None, end=None, last=None, output_format='json',
                    **kwargs):
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
    output_format: str, default 'json', optional
        Desired output format.
    kwargs:
        Additional request options
    """
    return DailySummaryReader(start=start, end=end, last=last,
                              output_format=output_format, **kwargs).fetch()


def get_stats_monthly(start=None, end=None, output_format='json', **kwargs):
    """
    Top-level function for obtaining data from the Historical Summary endpoint
    of IEX Stats

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        Start of data retrieval period
    end: datetime.datetime, default None, optional
        End of data retrieval period
    output_format: str, default 'json', optional
        Desired output format.
    kwargs:
        Additional request options
    """
    return MonthlySummaryReader(start=start, end=end,
                                output_format=output_format, **kwargs).fetch()
