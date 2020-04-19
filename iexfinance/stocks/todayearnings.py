from iexfinance.base import _IEXBase


class EarningsReader(_IEXBase):
    @property
    def url(self):
        return "stock/market/today-earnings"

    def _convert_output(self, out):
        return out
