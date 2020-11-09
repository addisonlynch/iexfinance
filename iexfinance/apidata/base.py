from datetime import datetime
import pandas as pd

from iexfinance.base import _IEXBase


class APIReader(_IEXBase):
    @property
    def url(self):
        return "status"

    def fetch(self):
        return super(APIReader, self).fetch()

    def _convert_output(self, out):
        converted_date = datetime.fromtimestamp(out["time"] / 1000).strftime("%c")
        return pd.DataFrame(out, index=[converted_date])
