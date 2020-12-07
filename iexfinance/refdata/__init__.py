from iexfinance.refdata.base import (
    Sectors,
    Symbols,
    IEXSymbols,
    TradingDatesReader,
    IntlRegionSymbols,
    IntlExchangeSymbols,
)


def get_symbols(**kwargs):
    """
    Returns array of all symbols that IEX Cloud supports
    for API calls

    Reference: https://iexcloud.io/docs/api/#symbols
    Data Weighting: ``100`` per call
    """
    return Symbols(**kwargs).fetch()


def get_sectors(**kwargs):
    """
    Returns array of all sectors that IEX Cloud supports
    for API calls

    Reference: https://iexcloud.io/docs/api/#sectors
    Data Weighting: ``1`` per call
    """
    return Sectors(**kwargs).fetch()


def get_iex_symbols(**kwargs):
    """
    Returns array of all symbols the Investor's Exchange
    supports for trading

    Reference: https://iexcloud.io/docs/api/#iex-symbols

    Data Weighting: ``Free``
    """
    return IEXSymbols(**kwargs).fetch()


def get_region_symbols(region, **kwargs):
    """
    Returns array of all international symbols in a give
    region that IEX Cloud supports for API calls

    https://iexcloud.io/docs/api/#international-symbols

    Data Weighting: ``100`` per call

    Parameters
    ----------
    region: str
        2 letter case insensitive string of country codes
        using ISO 3166-1 alpha-2
    """
    return IntlRegionSymbols(region, **kwargs).fetch()


def get_exchange_symbols(exchange, **kwargs):
    """
    Returns array of all international symbols in a given
    exchange that IEX Cloud supports for API calls

    https://iexcloud.io/docs/api/#international-symbols

    Data Weighting: ``100`` per call

    Parameters
    ----------
    exchange: str
        Case insensitive string of Exchange using IEX
        Supported Exchanges list
    """
    return IntlExchangeSymbols(exchange, **kwargs).fetch()


def get_us_trading_dates_holidays(type_, direction, last=1, startDate=None, **kwargs):
    """
    Function to obtain US trading dates or holidays from
    a given date

    Reference: https://iexcloud.io/docs/api/#u-s-holidays-and-trading-dates

    Data Weighting: ``1`` per row returned

    Parameters
    ----------
    type_: str
        can be "trade" or "holiday". Determines whether to return days where
        trading took place or holidays
    direction: str
        can be "next" or "last". Determines whether to return dates in the
        future or the past
    last: int, default 1
        number of days to go backward or forward
    startDate: str, datetime.datetime, default current date
        specify first/last day included in next/last, respectively
    """
    return TradingDatesReader(
        type_, direction, last=last, startDate=startDate, **kwargs
    ).fetch()
