from iexfinance.base import _IEXBase
from iexfinance.utils import legacy_endpoint


class CryptoReader(_IEXBase):

    @property
    def url(self):
        return 'stock/market/crypto'

    def _convert_output(self, out):
        import pandas as pd
        return pd.DataFrame(out).set_index("symbol").T

    @legacy_endpoint
    def fetch(self):
        return super(CryptoReader, self).fetch()
