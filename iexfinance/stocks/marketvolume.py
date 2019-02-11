from iexfinance.base import _IEXBase
from iexfinance.utils import cloud_endpoint


class MarketVolumeReader(_IEXBase):

    @property
    def url(self):
        return "stock/market/volume"

    @cloud_endpoint
    def fetch(self):
        return super(MarketVolumeReader, self).fetch()
