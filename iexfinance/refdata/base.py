import datetime
import pandas as pd

from iexfinance.base import _IEXBase

# Data provided for free by IEX
# See https://iextrading.com/api-exhibit-a/ for additional information
# and conditions of use


class ReferenceReader(_IEXBase):
    """
    Base class to retrieve data from the IEX Reference Data endpoints
    """
    def __init__(self, start=None, **kwargs):
        self.start = start
        super(ReferenceReader, self).__init__(**kwargs)

    @property
    def url(self):
        if isinstance(self.start, datetime.datetime):
            return 'daily-list/%s/%s' % (self.endpoint,
                                         self.start.strftime('%Y%m%d'))
        else:
            return 'daily-list/%s' % self.endpoint


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
    def __init__(self, type_, direction=None, last=1,
                 startDate=None, **kwargs):
        if isinstance(startDate, datetime.date):
            self.startDate = startDate.strftime('%Y%m%d')
        else:
            self.startDate = startDate
        self.type = type_
        if direction not in {"next", "last"}:
            raise ValueError("direction must be either next or last")
        self.direction = direction
        self.last = last
        super(TradingDatesReader, self).__init__(**kwargs)

    @property
    def endpoint(self):
        ret = "us/dates/%s/%s" % (self.type,
                                  self.direction)
        ret += "/" + str(self.last)
        if self.startDate is not None:
            ret += "/" + self.startDate
        print(f"{ret=}")
        return ret

    def _output_format(self, out, fmt_j=None, fmt_p=None):
        out = [{k: pd.to_datetime(v) for k, v in day.items()} for day in out]
        return super()._output_format(out, fmt_j=fmt_j, fmt_p=fmt_p)


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
