import requests

from datetime import datetime
from functools import wraps
import pandas as pd
import pandas.compat as compat
from pandas import to_datetime

from iexfinance.utils.exceptions import IEXVersionError


def _init_session(session, retry_count=3):
    if session is None:
        session = requests.session()
    return session


def _sanitize_dates(start, end):
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
        end = datetime.today()
    if start > end:
        raise ValueError('start must be an earlier date than end')
    return start, end


def _handle_lists(l, mult=True, err_msg=None):
    if isinstance(l, (compat.string_types, int)):
        return [l] if mult is True else l
    elif isinstance(l, pd.DataFrame) and mult is True:
        return list(l.index)
    elif mult is True:
        return list(l)
    else:
        raise ValueError(err_msg or "Only 1 symbol/market parameter allowed.")


def no_pandas(out):
    return out


def cloud_endpoint(func):
    @wraps(func)
    def _wrapped_function(self, *args, **kwargs):
        if self.version == 'v1':
            raise IEXVersionError("IEX Cloud")
        return func(self, *args, **kwargs)
    return _wrapped_function


def legacy_endpoint(func):
    @wraps(func)
    def _wrapped_function(self, *args, **kwargs):
        if self.version != 'v1':
            raise IEXVersionError("(legacy) IEX Developer API version 1.0")
        return func(self, *args, **kwargs)
    return _wrapped_function
