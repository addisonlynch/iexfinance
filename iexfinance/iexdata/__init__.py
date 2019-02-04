from iexfinance.iexdata.base import TOPS, Last, DEEP, Book


def get_tops(symbols=None, **kwargs):
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


def get_last(symbols=None, **kwargs):
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


def get_deep(symbols=None, **kwargs):
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


def get_book(symbols=None, **kwargs):
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
