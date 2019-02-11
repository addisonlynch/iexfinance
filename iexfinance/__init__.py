from iexfinance import stocks
from iexfinance.base import _IEXBase
from iexfinance.iexdata.base import TOPS, Last, DEEP, Book
from iexfinance.iexdata.base import (IntradayReader, RecentReader,
                                     RecordsReader, DailySummaryReader,
                                     MonthlySummaryReader)
from iexfinance.refdata.base import (CorporateActions, Dividends, NextDay,
                                     ListedSymbolDir)
from iexfinance.utils import _sanitize_dates
from iexfinance.utils.exceptions import IEXQueryError

__author__ = 'Addison Lynch'
__version__ = '0.4.0'

WNG_MSG = "%s is moved to iexfinance.%s. This function will be "\
          "deprecated in 0.4.1."

# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


def get_market_gainers(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_gainers
    """
    import warnings
    warnings.warn(WNG_MSG, ("get_market_gainers", "stocks.get_market_gainers"))
    return stocks.get_market_gainers(*args, **kwargs)


def get_market_losers(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_losers
    """
    import warnings
    warnings.warn(WNG_MSG, ("get_market_losers", "stocks.get_market_losers"))
    return stocks.get_market_losers(*args, **kwargs)


def get_market_most_active(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_most_active
    """
    import warnings
    warnings.warn(WNG_MSG, ("get_market_most_active",
                            "stocks.get_market_most_active"))
    return stocks.get_market_most_active(*args, **kwargs)


def get_market_iex_volume(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_iex_volume
    """
    import warnings
    warnings.warn(WNG_MSG, ("get_market_iex_volume",
                            "stocks.get_market_iex_volume"))
    return stocks.get_market_iex_volume(*args, **kwargs)


def get_market_iex_percent(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_iex_percent
    """
    import warnings
    warnings.warn(WNG_MSG, ("get_market_iex_percent",
                            "stocks.get_market_iex_percent"))
    return stocks.get_market_iex_percent(*args, **kwargs)


def get_available_symbols(**kwargs):
    """
    MOVED to iexfinance.refdata.get_symbols
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_available_symbols", "refdata.get_symbols"))
    _ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"
    handler = _IEXBase(**kwargs)
    response = handler._execute_iex_query(_ALL_SYMBOLS_URL)
    if not response:
        raise IEXQueryError("Could not download all symbols")
    else:
        return response


def get_iex_corporate_actions(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_corporate_actions
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_iex_corporate_actions",
                             "refdata.get_iex_corporate_actions"))
    return CorporateActions(start=start, **kwargs).fetch()


def get_iex_dividends(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_dividends
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_iex_dividends", "refdata.get_iex_dividends"))
    return Dividends(start=start, **kwargs).fetch()


def get_iex_next_day_ex_date(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_next_day_ex_date
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_iex_next_day_ex_date",
                             "refdata.get_iex_next_day_ex_date"))
    return NextDay(start=start, **kwargs).fetch()


def get_iex_listed_symbol_dir(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_listed_symbol_dir
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_iex_listed_symbol_dir",
                             "refdata.get_iex_listed_symbol_dir"))
    return ListedSymbolDir(start=start, **kwargs)


def get_market_tops(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_tops
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_market_tops", "iexdata.get_tops"))
    return TOPS(symbols, **kwargs).fetch()


def get_market_last(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_last
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_market_last", "iexdata.get_last"))
    return Last(symbols, **kwargs).fetch()


def get_market_deep(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_deep
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_market_deep", "iexdata.get_deep"))
    return DEEP(symbols, **kwargs).fetch()


def get_market_book(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_deep_book
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_market_book", "iexdata.get_deep_book"))
    return Book(symbols, **kwargs).fetch()


def get_stats_intraday(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_intraday
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_stats_intraday",
                             "iexdata.get_stats_intraday"))
    return IntradayReader(**kwargs).fetch()


def get_stats_recent(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_recent
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_stats_recent", "iexdata.get_stats_recent"))
    return RecentReader(**kwargs).fetch()


def get_stats_records(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_records
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_stats_records", "iexdata.get_stats_records"))
    return RecordsReader(**kwargs).fetch()


def get_stats_daily(start=None, end=None, last=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_daily
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_stats_daily", "iexdata.get_stats_daily"))
    start, end = _sanitize_dates(start, end)
    return DailySummaryReader(start=start, end=end, last=last,
                              **kwargs).fetch()


def get_stats_monthly(start=None, end=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_summary
    """
    import warnings
    warnings.warn(WNG_MSG % ("get_stats_monthly", "iexdata.get_stats_summary"))
    return MonthlySummaryReader(start=start, end=end, **kwargs).fetch()
