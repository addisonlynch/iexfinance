import datetime
import pandas as pd

from iexfinance.base import _IEXBase


class APIReader(_IEXBase):

    @property
    def url(self):
        return "status"

    def fetch(self):
        return super(APIReader, self).fetch()

    def _convert_output(self, out):
        return pd.DataFrame({datetime.datetime.now(): out})
