import logging
import os

from iexfinance.utils.exceptions import ImmediateDeprecationError

__author__ = 'Addison Lynch'
__version__ = '0.4.3'


# Data provided for free by IEX
# Data is furnished in compliance with the guidelines promulgated in the IEX
# API terms of service and manual
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use

# Configure logging
###################

# Deterimine log level, WARNING by default
LOG_LEVEL = getattr(logging, os.getenv("IEX_LOG_LEVEL", "WARNING").upper())

# Set log level
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

# Set log stream handler formatting
console_format = logging.Formatter(
        '%(levelname)s - %(message)s'
    )
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_format)
logger.addHandler(console_handler)


def get_market_gainers(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_gainers
    """
    raise ImmediateDeprecationError("get_market_gainers")


def get_market_losers(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_losers
    """
    raise ImmediateDeprecationError("get_market_losers")


def get_market_most_active(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_most_active
    """
    raise ImmediateDeprecationError("get_market_most_active")


def get_market_iex_volume(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_iex_volume
    """
    raise ImmediateDeprecationError("get_market_iex_volume")


def get_market_iex_percent(*args, **kwargs):
    """
    MOVED to iexfinance.stocks.get_market_iex_percent
    """
    raise ImmediateDeprecationError("get_market_iex_percent")


def get_available_symbols(**kwargs):
    """
    MOVED to iexfinance.refdata.get_symbols
    """
    raise ImmediateDeprecationError("get_available_symbols")


def get_iex_corporate_actions(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_corporate_actions
    """
    raise ImmediateDeprecationError("get_iex_corporate_actions")


def get_iex_dividends(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_dividends
    """
    raise ImmediateDeprecationError("get_iex_dividends")


def get_iex_next_day_ex_date(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_iex_next_day_ex_date
    """
    raise ImmediateDeprecationError("get_iex_next_day_ex_date")


def get_iex_listed_symbol_dir(start=None, **kwargs):
    """
    MOVED to iexfinance.refdata.get_listed_symbol_dir
    """
    raise ImmediateDeprecationError("get_iex_listed_symbol_dir")


def get_market_tops(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_tops
    """
    raise ImmediateDeprecationError("get_market_tops")


def get_market_last(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_last
    """
    raise ImmediateDeprecationError("get_market_last")


def get_market_deep(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_deep
    """
    raise ImmediateDeprecationError("get_market_deep")


def get_market_book(symbols=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_deep_book
    """
    raise ImmediateDeprecationError("get_market_book")


def get_stats_intraday(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_intraday
    """
    raise ImmediateDeprecationError("get_stats_intraday")


def get_stats_recent(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_recent
    """
    raise ImmediateDeprecationError("get_stats_recent")


def get_stats_records(**kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_records
    """
    raise ImmediateDeprecationError("get_stats_records")


def get_stats_daily(start=None, end=None, last=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_daily
    """
    raise ImmediateDeprecationError("get_stats_daily")


def get_stats_monthly(start=None, end=None, **kwargs):
    """
    MOVED to iexfinance.iexdata.get_stats_summary
    """
    raise ImmediateDeprecationError("get_stats_monthly")
