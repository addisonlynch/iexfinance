import requests

import datetime as dt
import pandas as pd
from pandas import to_datetime
from pandas.api.types import is_number


def _init_session(session, retry_count=3):
    if session is None:
        session = requests.session()
    return session


def _sanitize_dates(start, end):
    """
    Return (timestamp_start, timestamp_end) tuple
    if start is None - default is 15 years before the current date
    if end is None - default is today
    Parameters
    ----------
    start : str, int, date, datetime, Timestamp
        Desired start date
    end : str, int, date, datetime, Timestamp
        Desired end date
    """
    today = dt.date.today()
    today = to_datetime(today)

    if is_number(start):
        # regard int as year
        start = dt.datetime(start, 1, 1)
    start = to_datetime(start)

    if is_number(end):
        end = dt.datetime(end, 1, 1)
    end = to_datetime(end)

    if start is None:
        # default to 5 years before today
        start = today - dt.timedelta(days=365 * 15)
    if end is None:
        # default to today
        end = today
    try:
        start = to_datetime(start)
        end = to_datetime(end)
    except (TypeError, ValueError):
        raise ValueError("Invalid date format.")
    if start > end:
        raise ValueError("start must be an earlier date than end")
    if start > today or end > today:
        raise ValueError("Start and end dates must be before current date")
    return start, end


def _handle_lists(lister, mult=True, err_msg=None):
    if isinstance(lister, (str, int)):
        return [lister] if mult is True else lister
    elif isinstance(lister, pd.DataFrame) and mult is True:
        return list(lister.index)
    elif mult is True:
        return list(lister)
    else:
        raise ValueError(err_msg or "Only 1 symbol/market parameter allowed.")


def no_pandas(out):
    return out
