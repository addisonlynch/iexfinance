from iexfinance.base import _IEXBase


class SectorPerformanceReader(_IEXBase):

    @property
    def url(self):
        return "stock/market/sector-performance"

    def _convert_output(self, out):
        return out
