from iexfinance.base import _IEXBase


class CryptoReader(_IEXBase):

    @property
    def url(self):
        return 'stock/market/crypto'

    def _convert_output(self, out):
        import pandas as pd
        return pd.DataFrame(out).set_index("symbol").T
