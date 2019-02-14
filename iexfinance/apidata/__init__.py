from iexfinance.apidata.base import APIReader


def get_api_status(output_format=None, **kwargs):
    """
    Retrieves IEX Cloud API status

    Reference: https://iexcloud.io/docs/api/#status

    Data Weighting: ``Free``

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return APIReader(output_format=output_format, **kwargs).fetch()
