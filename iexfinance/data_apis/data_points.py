import pandas as pd

from iexfinance.base import _IEXBase


class DataPoints(_IEXBase):
    def __init__(self, symbol, key=None, **kwargs):
        self.symbol = symbol
        self.key = key
        super(DataPoints, self).__init__(**kwargs)

    @property
    def url(self):
        if self.key is None:
            return "data-points/%s" % self.symbol
        return "data-points/%s/%s" % (self.symbol, self.key)

    def _convert_output(self, out):
        if self.key is not None:
            return out
        return pd.DataFrame(out)
