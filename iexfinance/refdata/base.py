import datetime
import pandas as pd

from iexfinance.base import _IEXBase


class ReferenceData(_IEXBase):
    @property
    def url(self):
        return "ref-data/%s" % self.endpoint

    @property
    def endpoint(self):
        raise NotImplementedError


class TradingDatesReader(ReferenceData):
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

    def _format_output(self, out, format=None):
        out = [{k: pd.to_datetime(v) for k, v in day.items()} for day in out]
        return super(TradingDatesReader, self)._format_output(out)


class Symbols(ReferenceData):
    @property
    def endpoint(self):
        return "symbols"


class IEXSymbols(ReferenceData):
    @property
    def endpoint(self):
        return "iex/symbols"


class IntlRegionSymbols(ReferenceData):
    def __init__(self, region, **kwargs):
        self.region = region
        super(IntlRegionSymbols, self).__init__(**kwargs)

    @property
    def endpoint(self):
        return "region/%s/symbols" % self.region


class IntlExchangeSymbols(ReferenceData):
    def __init__(self, exchange, **kwargs):
        self.exchange = exchange
        super(IntlExchangeSymbols, self).__init__(**kwargs)

    @property
    def endpoint(self):
        return "exchange/%s/symbols" % self.exchange


class Sectors(ReferenceData):
    @property
    def endpoint(self):
        return "sectors"
