from iexfinance.refdata.base import (Symbols, IEXSymbols, CorporateActions,
                                     ListedSymbolDir, NextDay, Dividends)


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

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

    Data Weighting: ``Free``
    """
    return IEXSymbols(**kwargs).fetch()


def get_iex_corporate_actions(start=None, **kwargs):
    """
    Top-level function to retrieve IEX Corporate Actions from the ref-data
    endpoints

    .. warning:: This endpoint is available with the legacy IEX Developer API
                 version 1.0 only.

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

    .. warning:: This endpoint is available with the legacy IEX Developer API
                 version 1.0 only.

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

    .. warning:: This endpoint is available with the legacy IEX Developer API
                 version 1.0 only.

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

    .. warning:: This endpoint is available with the legacy IEX Developer API
                 version 1.0 only.

    Parameters
    ----------
    start: datetime.datetime, default None, optional
        A month to use for retrieval (a datetime object)
    kwargs: Additional Request Parameters (see base class)
    """
    return ListedSymbolDir(start=start, **kwargs).fetch()
