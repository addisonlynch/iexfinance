import requests

from datetime import datetime
from functools import wraps
import pandas as pd
from pandas import to_datetime

from iexfinance.utils.exceptions import ImmediateDeprecationError


def _init_session(session, retry_count=3):
    if session is None:
        session = requests.session()
    return session


def _sanitize_dates(start, end, default_end=datetime.today()):
    """
    Return (datetime_start, datetime_end) tuple
    if start is None - default is 2015/01/01
    if end is None - default is today
    """
    if isinstance(start, int):
        # regard int as year
        start = datetime(start, 1, 1)
    start = to_datetime(start)

    if isinstance(end, int):
        end = datetime(end, 1, 1)
    end = to_datetime(end)

    if start is None:
        start = datetime(2015, 1, 1)
    if end is None:
        end = default_end
    if default_end is not None and start > end:
        raise ValueError('start must be an earlier date than end')
    return start, end


def _handle_lists(l, mult=True, err_msg=None):
    if isinstance(l, (str, int)):
        return [l] if mult is True else l
    elif isinstance(l, pd.DataFrame) and mult is True:
        return list(l.index)
    elif mult is True:
        return list(l)
    else:
        raise ValueError(err_msg or "Only 1 symbol/market parameter allowed.")


def no_pandas(out):
    return out


def legacy_endpoint(func):
    """
    Decorator to denote a function or method which calls an endpoint that is
    not supported by IEX Cloud.

    These endpoints will be deprecated in 0.4.2.
    """
    @wraps(func)
    def _wrapped_function(self, *args, **kwargs):
        raise ImmediateDeprecationError()
    return _wrapped_function
