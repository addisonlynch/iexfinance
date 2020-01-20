from iexfinance.refdata.base import Symbols, IEXSymbols


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
