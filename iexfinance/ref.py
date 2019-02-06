import datetime

from .base import _IEXBase
from iexfinance.utils import cloud_endpoint

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
                                         self.start.strftime('%Y%m'))
        else:
            return 'daily-list/%s' % self.endpoint


class CorporateActions(ReferenceReader):

    @property
    def endpoint(self):
        return 'corporate-actions'


class Dividends(ReferenceReader):

    @property
    def endpoint(self):
        return 'dividends'


class NextDay(ReferenceReader):

    @property
    def endpoint(self):
        return 'next-day-ex-date'


class ListedSymbolDir(ReferenceReader):

    @property
    def endpoint(self):
        return 'symbol-directory'


class CloudRef(_IEXBase):

    @cloud_endpoint
    def fetch(self):
        return super(CloudRef, self).fetch()

    @property
    def url(self):
        return "ref-data/%s" % self.endpoint

    @property
    def endpoint(self):
        raise NotImplementedError


class Symbols(_IEXBase):

    @property
    def endpoint(self):
        return "symbols"


class IEXSymbols(_IEXBase):

    @property
    def endpoint(self):
        return "iex/symbols"
