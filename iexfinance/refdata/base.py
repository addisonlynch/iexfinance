import datetime
import pandas as pd

from iexfinance.base import _IEXBase

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class CloudRef(_IEXBase):
    @property
    def url(self):
        return "ref-data/%s" % self.endpoint

    @property
    def endpoint(self):
        raise NotImplementedError


class TradingDatesReader(CloudRef):
    """
    Base class to retrieve trading holiday information
    """

    def __init__(self, type_, direction=None, last=1, startDate=None, **kwargs):
        if isinstance(startDate, datetime.date) or isinstance(
            startDate, datetime.datetime
        ):
            self.startDate = startDate.strftime("%Y%m%d")
        else:
            self.startDate = startDate
        self.type = type_
        if direction not in ("next", "last"):
            raise ValueError("direction must be either next or last")
        self.direction = direction
        self.last = last
        super(TradingDatesReader, self).__init__(**kwargs)

    @property
    def endpoint(self):
        ret = "us/dates/%s/%s/%s" % (self.type, self.direction, self.last)
        if self.startDate:
            ret += "/%s" % self.startDate
        return ret

    def _format_output(self, out):
        out = [{k: pd.to_datetime(v) for k, v in day.items()} for day in out]
        return super(TradingDatesReader, self)._format_output(out)


class Symbols(CloudRef):
    @property
    def endpoint(self):
        return "symbols"


class IEXSymbols(CloudRef):
    def fetch(self):
        return super(CloudRef, self).fetch()

    @property
    def endpoint(self):
        return "iex/symbols"
