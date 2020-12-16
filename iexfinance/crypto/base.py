import pandas as pd

from iexfinance.base import _IEXBase


class Crypto(_IEXBase):
    def __init__(self, endpoint, symbol, **kwargs):
        self._endpoint = endpoint
        if not isinstance(symbol, str):
            raise ValueError("Single symbol required.")
        self.symbol = symbol
        super(Crypto, self).__init__(**kwargs)

    @property
    def url(self):
        return "crypto/%s/%s" % (self.symbol, self._endpoint)

    def _convert_output(self, out):
        if self._endpoint == "book":
            return out
        return pd.DataFrame(out, index=[out["symbol"]])
