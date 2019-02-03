import datetime
import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import cloud_endpoint


class APIReader(_IEXBase):

    @property
    def url(self):
        return "status"

    @cloud_endpoint
    def fetch(self):
        return super(APIReader, self).fetch()

    def _convert_output(self, out):
        return pd.DataFrame({datetime.datetime.now(): out})


def get_api_status(output_format=None):
    """
    Retrieves IEX Cloud API status

    Reference: https://iexcloud.io/docs/api/#status
    """
    a = APIReader(output_format=output_format)
    return a.fetch()
