from iexfinance.apidata.base import APIReader


def get_api_status(**kwargs):
    """
    IEX Cloud API status

    Reference: https://iexcloud.io/docs/api/#status

    Data Weighting: ``Free``
    """
    return APIReader(**kwargs).fetch()
