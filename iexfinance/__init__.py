from .stock import StockReader, HistoricalReader
from .base import _IEXBase
from .market import TOPS, Last, DEEP, Book
from .stats import (IntradayReader, RecentReader, RecordsReader,
                    DailySummaryReader, MonthlySummaryReader)

from .utils.exceptions import IEXQueryError

__author__ = 'Addison Lynch'
__version__ = '0.3.0'
__all__ = ['Batch', 'get_historical_data']

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def Stock(symbolList=None, displayPercent=False, _range="1m",
          last=10, retry_count=3, pause=0.001, session=None):
    """
    Top level function to create Share or Batch instance depending on number
    of symbols given

    Keyword arguments:
        symbol: A string or list of strings that are valid symbols
        options: A valid list of parameters to pass to the api. See _IEXBase
        base class, where these parameters are checked

    """
    if type(symbolList) is str:
        if not symbolList:
            raise ValueError("Please input a symbol or list of symbols")
        else:
            inst = StockReader([symbolList], displayPercent, _range, last,
                               retry_count, pause, session)
    elif type(symbolList) is list:
        if not symbolList:
            raise ValueError("Please input a symbol or list of symbols")
        if len(symbolList) > 100:
            raise ValueError("Invalid symbol list. Maximum 100 symbols.")
        else:
            inst = StockReader(symbolList, displayPercent, _range, last,
                               retry_count, pause, session)
        return inst
    else:
        raise ValueError("Please input a symbol or list of symbols")
    return inst


def get_reference_data():
    """
    Utility function to obtain all available symbols.

    Returns
    -------
    data: json
        Dictionary of all reference data
    """
    _ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"
    handler = _IEXBase()
    response = handler._execute_iex_query(_ALL_SYMBOLS_URL)
    if not response:
        raise IEXQueryError("Could not download all symbols")
    else:
        return response


def get_available_symbols():
    """
    Utility function to obtain IEX Reference Data

    Returns
    -------
    symbols: list
        A list of all available symbols (no additional data)
    """
    return [d["symbol"] for d in get_available_symbols()]


def get_historical_data(symbolList=None, start=None, end=None,
                        outputFormat='json', retry_count=3, pause=0.001,
                        session=None):
    """
    Top-level function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader

    Parameters
    ----------
    symbolList: str or list, default None
        A symbol or list of symbols
    start: datetime.datetime, default None
        Beginning of desired date range
    end: datetime.datetime, default None
        End of required date range
    outputFormat: str, (defaults to json)
        Desired output format (json or pandas)
    retry_count: int, default 3
        Desired number of retries if a request fails
    pause: float, default 0.001
        Pause time between retry attempts
    session: requests.session, default None
        A cached requests-cache session

    Returns
    -------
    df: json or DataFrame
        Historical stock prices over date range, start to end
    """
    return HistoricalReader(symbolList, start,
                            end, outputFormat, retry_count, pause,
                            session).fetch()


def get_market_tops(symbolList=None, outputFormat='json', retry_count=3,
                    pause=0.001, session=None):
    """
    Top-level function to obtain TOPS data for a symbol or list of symbols
    """
    return TOPS(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_market_last(symbolList=None, outputFormat='json', retry_count=3,
                    pause=0.001, session=None):
    """
    Top-level function to obtain Last data for a symbol or list of symbols
    """
    return Last(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_market_deep(symbolList=None, outputFormat='json', retry_count=3,
                    pause=0.001, session=None):
    """
    Top-level function to obtain DEEP data for a symbol or list of symbols
    """
    return DEEP(symbolList, outputFormat, retry_count, pause, session).fetch()


def get_market_book(symbolList=None, outputFormat='json', retry_count=3,
                    pause=0.001, session=None):
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
