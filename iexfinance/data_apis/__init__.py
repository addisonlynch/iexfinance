from iexfinance.data_apis.time_series import TimeSeries


def get_time_series(id_=None, key=None, subkey=None, **kwargs):
    """
    Retrieves a list of time series available (if no parameters passed) or
    time series data for a given id\_, key, and subkey.

    Reference: https://iexcloud.io/docs/api/#time-series

    Data Weighting: Free for list, varies for others

    Parameters
    ----------
    id\_: str, optional
        ID used to identify a time series dataset (function returns list of
        all available datasets if argument not passed)
    key: str, optional
        Key used to identify data within a dataset. A common example is a
        symbol such as AAPL
    subkey: str, optional
        The optional subkey can be used to further refine data for a particular
        key if available
    """
    return TimeSeries(id_=id_, key=key, subkey=subkey, **kwargs).fetch()
