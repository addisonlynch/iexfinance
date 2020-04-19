import pandas as pd

from iexfinance.base import _IEXBase


class OptionsReader(_IEXBase):
    def __init__(self, symbol, expiration=None, option_side=None, **kwargs):
        self.symbol = symbol
        self.expiration = expiration
        self.option_side = option_side
        super(OptionsReader, self).__init__(**kwargs)

    @property
    def url(self):
        if self.expiration is None:
            return "/stock/%s/options" % self.symbol
        if self.option_side is None:
            return "/stock/%s/options/%s" % (self.symbol, self.expiration)
        return "/stock/%s/options/%s/%s" % (
            self.symbol,
            self.expiration,
            self.option_side,
        )

    def _convert_output(self, out):
        if self.expiration is None:
            return pd.DataFrame(out)
        else:
            return pd.DataFrame({item["expirationDate"]: item for item in out})
