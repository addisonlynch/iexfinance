from iexfinance.apidata.base import APIReader


def get_api_status(output_format='json', **kwargs):
    """
    Retrieves IEX Cloud API status

    Reference: https://iexcloud.io/docs/api/#status

    Data Weighting: ``Free``
    """
    return APIReader(output_format=output_format, **kwargs).fetch()
