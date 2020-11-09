import pandas as pd

from iexfinance.base import _IEXBase


class CloudCrypto(_IEXBase):
    def __init__(self, symbol, **kwargs):
        if not isinstance(symbol, str):
            raise ValueError("Single symbol required.")
        self.symbol = symbol
        super(CloudCrypto, self).__init__(**kwargs)

    @property
    def url(self):
        return "crypto/%s/quote" % self.symbol

    def fetch(self):
        return super(CloudCrypto, self).fetch()

    def _convert_output(self, out):
        return pd.DataFrame(out, index=[out["symbol"]])


class SocialSentiment(_IEXBase):

    _VALID_PERIOD_TYPES = ("daily", "minute")

    def __init__(self, symbol, period_type=None, date=None, **kwargs):
        self.period_type = period_type or "daily"
        if self.period_type not in self._VALID_PERIOD_TYPES:
            raise ValueError("Period_type %s is not valid." % period_type)
        self.symbol = symbol
        try:
            self.date = date.strftime("%Y%M%d")
        except AttributeError:
            self.date = date
        super(SocialSentiment, self).__init__(**kwargs)

    @property
    def url(self):
        if self.date:
            return "/stock/%s/sentiment/%s/%s" % (
                self.symbol,
                self.period_type,
                self.date,
            )
        else:
            return "/stock/%s/sentiment/%s" % (self.symbol, self.period_type)

    def fetch(self):
        return super(SocialSentiment, self).fetch()


class CEOCompensation(_IEXBase):
    def __init__(self, symbol, **kwargs):
        self.symbol = symbol
        super(CEOCompensation, self).__init__(**kwargs)

    @property
    def url(self):
        return "/stock/%s/ceo-compensation" % self.symbol

    def fetch(self):
        return super(CEOCompensation, self).fetch()

    def _convert_output(self, out):
        return pd.DataFrame(out, index=[out["symbol"]])
