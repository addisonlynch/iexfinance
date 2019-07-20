from iexfinance.refdata.base import (Symbols, IEXSymbols, CorporateActions,
                                     ListedSymbolDir, NextDay, Dividends)


def get_symbols(**kwargs):
    """
    Returns array of all symbols that IEX Cloud supports
    for API calls

    Reference: https://iexcloud.io/docs/api/#symbols
    Data Weighting: ``100`` per call
    """
    return Symbols(**kwargs).fetch()


def get_iex_symbols(**kwargs):
    """
    Returns array of all symbols the Investor's Exchange
    supports for trading

    Reference: https://iexcloud.io/docs/api/#iex-symbols

    Data Weighting: ``Free``
    """
    return IEXSymbols(**kwargs).fetch()


def get_iex_corporate_actions(start=None, **kwargs):
    """
    DEPRECATED
    """
    return CorporateActions(start=start, **kwargs).fetch()


def get_iex_dividends(start=None, **kwargs):
    """
    DEPRECATED
    """
    return Dividends(start=start, **kwargs).fetch()


def get_iex_next_day_ex_date(start=None, **kwargs):
    """
    DEPRECATED
    """
    return NextDay(start=start, **kwargs).fetch()


def get_iex_listed_symbol_dir(start=None, **kwargs):
    """
    DEPRECATED
    """
    return ListedSymbolDir(start=start, **kwargs).fetch()
