from .stock import Share, Batch, HistoricalReader
from .base import _IEXBase
__author__ = 'Addison Lynch'
__version__ = '0.3.0'
__all__ = ['Share', 'Batch']

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def IexFinance(symbol, **kwargs):
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
            inst = Share(symbol, **kwargs)
    elif type(symbol) is list:
        if not symbol:
            raise ValueError("Please input a symbol or list of symbols")
        if len(symbol) == 1:
            inst = Share(symbol, **kwargs)
        if len(symbol) > 100:
            raise ValueError("Invalid symbol list. Maximum 100 symbols.")
        else:
            inst = Batch(symbol, **kwargs)
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


def get_historical_data(symbol, start, end, outputFormat='json'):
    """
    Top-level function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader
    """
    return HistoricalReader(symbol, start,
                            end, outputFormat=outputFormat).fetch()
