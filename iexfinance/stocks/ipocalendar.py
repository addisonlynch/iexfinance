from iexfinance.base import _IEXBase


class IPOReader(_IEXBase):

    _PERIODS = ["today-ipos", "upcoming-ipos"]

    def __init__(self, period=None, **kwargs):
        period = period or "upcoming-ipos"
        if period not in self._PERIODS:
            raise ValueError("Please enter a valid period.")
        self.period = period
        super(IPOReader, self).__init__(**kwargs)

    @property
    def url(self):
        return "stock/market/%s" % self.period

    def _convert_output(self, out):
        return out
