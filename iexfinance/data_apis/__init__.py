from iexfinance.data_apis.data_points import DataPoints
from iexfinance.data_apis.time_series import TimeSeries


def get_data_points(symbol, key=None, **kwargs):
    """
    DataFrame of datapoints for a symbol (if no additional parameters
    passed) or single data point for a given symbol and data point key

    Reference: https://iexcloud.io/docs/api/#data-apis

    Data Weighting: ``Free`` for list, varies for others

    Parameters
    ----------
    symbol: str
        Valid symbol
    key: str, optional
        Datapoint key
    """
    return DataPoints(symbol, key=key, **kwargs).fetch()


def get_time_series(id_=None, key=None, subkey=None, **kwargs):
    """
    List of time series available (if no parameters passed) or
    time series data for given id, key, and subkey.

    Reference: https://iexcloud.io/docs/api/#time-series

    Data Weighting: ``Free`` for list, varies for others

    Parameters
    ----------
    id: str, optional
        Time Series dataset ID (function returns list of
        all available datasets if argument not passed)
    key: str, optional
        Key used to identify data within a dataset (e.g. ``AAPL``)
    subkey: str, optional
        Key-based. Further refine data
    """
    return TimeSeries(id_=id_, key=key, subkey=subkey, **kwargs).fetch()
