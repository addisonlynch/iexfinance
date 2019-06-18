from iexfinance.data_apis.data_points import DataPoints
from iexfinance.data_apis.time_series import TimeSeries


def get_data_points(symbol, key=None, **kwargs):
    """
    Retrieves a list of data point for a symbol (if no additional parameters
    are passed) or a data point for a given symbol and data point key

    Reference: https://iexcloud.io/docs/api/#data-apis

    Data Weighting: Free for list, varies for others

    Parameters
    ----------
    symbol: str
        A valid symbol
    key: str, optional
        Data point key to retrieve
    """
    return DataPoints(symbol, key=key, **kwargs).fetch()


def get_time_series(id_=None, key=None, subkey=None, **kwargs):
    """
    Retrieves a list of time series available (if no parameters passed) or
    time series data for a given id, key, and subkey.

    Reference: https://iexcloud.io/docs/api/#time-series

    Data Weighting: Free for list, varies for others

    Parameters
    ----------
    id: str, optional
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
