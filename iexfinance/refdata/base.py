import datetime

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
