from .stock import Share, Batch, HistoricalReader
from .base import _IEXBase
from .market import TOPS, Last, DEEP, Book
from .stats import (IntradayReader, RecentReader, RecordsReader,
                    DailySummaryReader, MonthlySummaryReader)

__author__ = 'Addison Lynch'
__version__ = '0.3.0'
__all__ = ['Share', 'Batch']

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def IexFinance(symbol=None, displayPercent=False, _range="1m",
               last=10, retry_count=3, pause=0.001, session=None):
    """
    Top level function to create Share or Batch instance depending on number
    of symbols given

    Keyword arguments:
        symbol: A string or list of strings that are valid symbols
        options: A valid list of parameters to pass to the api. See _IEXBase
        base class, where these parameters are checked

    """
    if type(symbol) is str:
        if not symbol:
            raise ValueError("Please input a symbol or list of symbols")
        else:
            inst = Share(symbol, displayPercent, _range, last, retry_count,
                         pause, session)
    elif type(symbol) is list:
        if not symbol:
            raise ValueError("Please input a symbol or list of symbols")
        if len(symbol) == 1:
            inst = Share(symbol[0], displayPercent, _range, last, retry_count,
                         pause, session)
        if len(symbol) > 100:
            raise ValueError("Invalid symbol list. Maximum 100 symbols.")
        else:
            inst = Batch(symbol, displayPercent, _range, last, retry_count,
                         pause, session)
        return inst
    else:
        raise TypeError("Please input a symbol or list of symbols")
    return inst


def get_available_symbols():
    """
    Utility function to obtain all available symbols.
    """
    _ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"
    handler = _IEXBase()
    response = handler._execute_iex_query(_ALL_SYMBOLS_URL)
    if not response:
        raise ValueError("Could not download all symbols")
    else:
        return [d["symbol"] for d in response]


def get_historical_data(symbolList, start, end, outputFormat='json',
                        retry_count=3, pause=0.001, session=None):
    """
    Top-level function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader
    """
    return HistoricalReader(symbolList, start,
                            end, outputFormat, retry_count, pause,
                            session).fetch()


def get_TOPS(symbolList=None, outputFormat='json', retry_count=3, pause=0.001,
             session=None):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols
    """
    return TOPS(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_Last(symbolList=None, outputFormat='json', retry_count=3, pause=0.001,
             session=None):
    """
    Top-level function to obtain Last data for a symbol or list of symbols
    """
    return Last(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_DEEP(symbolList=None, outputFormat='json', retry_count=3, pause=0.001,
             session=None):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols
    """
    return DEEP(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_Book(symbolList=None, outputFormat='json', retry_count=3, pause=0.001,
             session=None):
    """
    Returns a list of all equity symbols available for trading on IEX. Accepts
    no additional parameters.

    Reference: https://www.iextrading.com/developer/docs/#symbols

    :return: DataFrame
    """
    return Book(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_stats_intraday(outputFormat='json', retry_count=3, pause=0.001,
                       session=None):

    return IntradayReader(outputFormat=outputFormat, retry_count=retry_count,
                          pause=pause, session=session).fetch()


def get_stats_recent(outputFormat='json', retry_count=3, pause=0.001,
                     session=None):

    return RecentReader(outputFormat=outputFormat, retry_count=retry_count,
                        pause=pause, session=session).fetch()


def get_stats_records(outputFormat='json', retry_count=3, pause=0.001,
                      session=None):

    return RecordsReader(outputFormat=outputFormat, retry_count=retry_count,
                         pause=pause, session=session).fetch()


def get_stats_daily(start=None, end=None, outputFormat='json', last=None,
                    retry_count=3, pause=0.001, session=None):

    return DailySummaryReader(start=start, end=end, last=last,
                              outputFormat=outputFormat,
                              retry_count=retry_count, pause=pause,
                              session=session).fetch()


def get_stats_monthly(start=None, end=None, outputFormat='json', retry_count=3,
                      pause=0.001, session=None):

    return MonthlySummaryReader(start=start, end=end,
                                outputFormat=outputFormat,
                                retry_count=retry_count, pause=pause,
                                session=session).fetch()
