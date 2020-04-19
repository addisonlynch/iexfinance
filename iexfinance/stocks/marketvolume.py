from iexfinance.base import _IEXBase


class MarketVolumeReader(_IEXBase):
    @property
    def url(self):
        return "stock/market/volume"

    def fetch(self):
        return super(MarketVolumeReader, self).fetch()
