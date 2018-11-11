import requests

from datetime import datetime
import pandas as pd
import pandas.compat as compat
from pandas import to_datetime


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
