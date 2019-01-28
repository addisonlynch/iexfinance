from iexfinance.stocks.base import StockReader
from iexfinance.stocks.collections import CollectionsReader
from iexfinance.stocks.crypto import CryptoReader
from iexfinance.stocks.historical import HistoricalReader, IntradayReader
from iexfinance.stocks.ipocalendar import IPOReader
from iexfinance.stocks.movers import MoversReader
from iexfinance.stocks.sectorperformance import SectorPerformanceReader
from iexfinance.stocks.todayearnings import EarningsReader
from iexfinance.utils import _sanitize_dates

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def Stock(symbols=None, **kwargs):
    """
    Function to to retrieve data from the IEX Stocks endpoints

    Parameters
    ----------
    symbols: str or list
        A string or list of strings that are valid symbols
    output_format: str, default 'json', optional
        Desired output format for requests
    kwargs:
        Additional Request Parameters (see base class)
    Returns
    -------
    stock.StockReader
        A StockReader instance
    """
    if isinstance(symbols, str) and symbols:
        return StockReader([symbols], **kwargs)
    elif isinstance(symbols, list) and 0 < len(symbols) <= 100:
        return StockReader(symbols, **kwargs)
    else:
        raise ValueError("Please input a symbol or list of symbols")


def get_historical_data(symbols, start=None, end=None, **kwargs):
    """
    Top-level function to obtain historical date for a symbol or list of
    symbols. Return an instance of HistoricalReader

    Parameters
    ----------
    symbols: str or list
        A symbol or list of symbols
    start: datetime.datetime, default None
        Beginning of desired date range
    end: datetime.datetime, default None
        End of required date range
    kwargs:
        Additional Request Parameters (see base class)

    Returns
    -------
    list or DataFrame
        Historical stock prices over date range, start to end
    """
    start, end = _sanitize_dates(start, end)
    return HistoricalReader(symbols, start=start, end=end, **kwargs).fetch()


def get_historical_intraday(symbol, date=None, **kwargs):
    """
    Top-level function to obtain intraday one-minute pricing data for one
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
    """
    This function returns an array of each sector and performance
    for the current trading day. Performance is based on each sector ETF.
    Parameters
    ----------
    kwargs:
        Additional Request Parameters (see base class)
    Returns
    -------
    data: list
        List of dictionary sector performance items
    """
    return SectorPerformanceReader(**kwargs).fetch()


def get_collections(collection_name, collection_type="tag", **kwargs):
    """
    Top-level function for obtaining data from the Collections endpoint

    Parameters
    ----------
    collection_name: str
        Desired collection name
    collection_type: str, default "tag", optional
        Desired collection type (sector, tag, or list)
        kwargs:
        Additional Request Parameters (see base class)
    """
    return CollectionsReader(collection_name,
                             collection_type, **kwargs).fetch()


def get_crypto_quotes(**kwargs):
    """
    Top-level function for obtaining all available cryptocurrency quotes
    """
    return CryptoReader(**kwargs).fetch()


def get_todays_earnings(**kwargs):
    """
    Top-level function for obtaining all earnings results which are released on
    the current date.
    """
    return EarningsReader(**kwargs).fetch()


def get_ipo_calendar(period="upcoming-ipos", **kwargs):
    """
    Top-level function for obtaining today's and upcoming IPOs

    Parameters
    ----------
    period: str, default "upcoming-ipos", optional
        Desired period (options are "upcoming-ipos" and "today-ipos")
    """
    return IPOReader(period, **kwargs).fetch()


def get_market_gainers(**kwargs):
    """
    Top-level function for obtaining top 10 market gainers from the
    Stocks list endpoint
    """
    return MoversReader(mover='gainers', **kwargs).fetch()


def get_market_losers(**kwargs):
    """
    Top-level function for obtaining top 10 market losers from the
    Stocks list endpoint
    """
    return MoversReader(mover='losers', **kwargs).fetch()


def get_market_most_active(**kwargs):
    """
    Top-level function for obtaining top 10 most active symbols from
    the Stocks list endpoint
    """
    return MoversReader(mover='mostactive', **kwargs).fetch()


def get_market_iex_volume(**kwargs):
    """
    Top-level function for obtaining the 10 symbols with the highest
    IEX volume from the Stocks list endpoint
    """
    return MoversReader(mover='iexvolume', **kwargs).fetch()


def get_market_iex_percent(**kwargs):
    """
    Top-level function for obtaining the 10 symbols with the highest
    percent change on the IEX exchange from the Stocks list endpoint
    """
    return MoversReader(mover='iexpercent', **kwargs).fetch()


def get_market_in_focus(**kwargs):
    """
    Top-level function for obtaining top 10 in focus symbols from the
    Stocks list endpoint
    """
    return MoversReader(mover='infocus', **kwargs).fetch()
