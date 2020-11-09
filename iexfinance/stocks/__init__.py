from iexfinance.stocks.base import Stock  # noqa
from iexfinance.stocks.collections import CollectionsReader
from iexfinance.stocks.historical import HistoricalReader, IntradayReader
from iexfinance.stocks.ipocalendar import IPOReader
from iexfinance.stocks.marketvolume import MarketVolumeReader
from iexfinance.stocks.movers import MoversReader
from iexfinance.stocks.options import OptionsReader
from iexfinance.stocks.sectorperformance import SectorPerformanceReader
from iexfinance.stocks.todayearnings import EarningsReader

from iexfinance.utils.exceptions import ImmediateDeprecationError


def get_historical_data(symbols, start=None, end=None, close_only=False, **kwargs):
    """
    Function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader

    Reference: https://iextrading.com/developer/docs/#chart

    Parameters
    ----------
    symbols: str or list
        A symbol or list of symbols
    start : string, int, date, datetime, Timestamp
        Starting date. Parses many different kind of date
        representations (e.g., 'JAN-01-2010', '1/1/10', 'Jan, 1, 1980').
        Defaults to 1 year before current date.
    end : string, int, date, datetime, Timestamp
        Ending date
    close_only: bool, default False
        Returns adjusted data only with keys ``date``, ``close``, and
        ``volume``
    kwargs:
        Additional Request Parameters (see base class)

    Returns
    -------
    list or DataFrame
        Historical stock prices over date range, start to end
    """
    return HistoricalReader(
        symbols, start=start, end=end, close_only=close_only, **kwargs
    ).fetch()


def get_historical_intraday(symbol, date=None, **kwargs):
    """
    Function to obtain intraday one-minute pricing data for one
    symbol on a given date (defaults to current date)

    Parameters
    ----------
    symbol: str
        A single ticker
    date: datetime.datetime, default current date
        Desired date for intraday retrieval, defaults to today
    kwargs:
        Additional Request Parameters (see base class)

    Returns
    -------
    list or DataFrame
        Intraday pricing data for specified symbol on given date
    """
    return IntradayReader(symbol, date, **kwargs).fetch()


def get_sector_performance(**kwargs):
    """Sector Performance

    This returns an array of each sector and performance for the current
    trading day. Performance is based on each sector ETF.

    Reference: https://iexcloud.io/docs/api/#sector-performance

    Data Weighting: ``1`` per sector

    Returns
    -------
    data: list
        List of dictionary sector performance items
    """
    return SectorPerformanceReader(**kwargs).fetch()


def get_collections(collection_name, collection_type="tag", **kwargs):
    """Collections

    Returns an array of ``quote`` objects for a given collection type.
    Currently supported collection types are ``sector``, ``tag``, and ``list``

    .. note:: Proper capitalization must be used with sector names. For instance,
              "Technology" must be capitalized or no results will be returned.

    Reference: https://iexcloud.io/docs/api/#collections

    Data Weighting: Weight of ``/stock/quote`` per method

    Parameters
    =================
    collection_name: str
        Desired collection name
    collection_type: str, default "tag", optional
        Desired collection type (sector, tag, or list)
        kwargs:
        Additional Request Parameters (see base class)
    """
    return CollectionsReader(collection_name, collection_type, **kwargs).fetch()


def get_market_volume(**kwargs):
    """Market Volume

    This endpoint returns real time traded volume on U.S. markets.

    Data Weighting: ``1`` per call

    .. warning:: Data only available from 7:45am-5:15pm ET Mon-Fri.
    """
    return MarketVolumeReader(**kwargs).fetch()


def get_earnings_today(**kwargs):
    """Earnings Today

    Returns earnings that will be reported today as two arrays: before the open
    ``bto`` and after market close ``amc``. Each array contains an object with
    all keys from ``earnings``, a ``quote`` object, and a ``headline`` key.

    .. note:: Pandas output formatting is not available for this endpoint.

    Reference: https://iexcloud.io/docs/api/#earnings-today

    Data Weighting: ``1051`` per symbol returned
    """
    return EarningsReader(**kwargs).fetch()


def get_ipo_calendar(period=None, **kwargs):
    """IPO Calendar

    This returns a list of upcoming or today IPOs scheduled for the current and
    next month. The response is split into two structures: ``rawData`` and
    ``viewData``. ``rawData`` represents all available data for an IPO.
    ``viewData`` represents data structured for display to a user.

    .. note:: Pandas output formatting is not available for this endpoint.

    Reference: https://iexcloud.io/docs/api/#ipo-calendar

    Data Weighting: ``100`` per IPO returned for ``upcoming-ipos``, ``500``
    returned for ``today-ipos``

    Parameters
    ----------
    period: str, default "upcoming-ipos", optional
        Desired period (options are "upcoming-ipos" and "today-ipos")
    """
    return IPOReader(period, **kwargs).fetch()


def get_market_gainers(**kwargs):
    """Market Gainers

    Function for obtaining top 10 market gainers from the
    Stocks list endpoint

    Reference: https://iexcloud.io/docs/api/#list

    Data Weighting: Weight of ``/stock/quote`` for each quote returned in the
    list
    """
    return MoversReader(mover="gainers", **kwargs).fetch()


def get_market_losers(**kwargs):
    """Market Losers

    Function for obtaining top 10 market losers from the
    Stocks list endpoint

    Reference: https://iexcloud.io/docs/api/#list

    Data Weighting: Weight of ``/stock/quote`` for each quote returned in the
    list
    """
    return MoversReader(mover="losers", **kwargs).fetch()


def get_market_most_active(**kwargs):
    """Market Most Active

    Function for obtaining top 10 most active symbols from
    the Stocks list endpoint

    Reference: https://iexcloud.io/docs/api/#list

    Data Weighting: Weight of ``/stock/quote`` for each quote returned in the
    list
    """
    return MoversReader(mover="mostactive", **kwargs).fetch()


def get_market_iex_volume(**kwargs):
    """Market IEX Volume

    Function for obtaining the 10 symbols with the highest
    IEX volume from the Stocks list endpoint

    Reference: https://iexcloud.io/docs/api/#list

    Data Weighting: Weight of ``/stock/quote`` for each quote returned in the
    list
    """
    return MoversReader(mover="iexvolume", **kwargs).fetch()


def get_market_iex_percent(**kwargs):
    """Market IEX Percent

    Function for obtaining the 10 symbols with the highest
    percent change on the IEX exchange from the Stocks list endpoint

    Reference: https://iexcloud.io/docs/api/#list

    Data Weighting: Weight of ``/stock/quote`` for each quote returned in the
    list
    """
    return MoversReader(mover="iexpercent", **kwargs).fetch()


def get_market_in_focus(**kwargs):
    """Market in Focus
    DEPRECATED
    """
    raise ImmediateDeprecationError("get_market_in_focus")


def get_eod_options(symbol, expiration=None, option_side=None, **kwargs):
    """
    End of Day Options

    Returns a list of option expiration dates for a given symbol

    Reference: https://iexcloud.io/docs/api/#end-of-day-options


    Parameters
    ----------
    symbol: str
        A valid symbol
    expiration: str, optional
        A valid expiration date
    option_side: str, optional
        Option side - ``put`` or ``call`` will return only those types of
        contracts
    """
    return OptionsReader(
        symbol, expiration=expiration, option_side=option_side, **kwargs
    ).fetch()
