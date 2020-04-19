import pandas as pd

from iexfinance.base import _IEXBase


class Account(_IEXBase):
    @property
    def url(self):
        return "account/%s" % self.endpoint

    @property
    def endpoint(self):
        raise NotImplementedError

    def fetch(self):
        return super(Account, self).fetch()


class Metadata(Account):
    @property
    def endpoint(self):
        return "metadata"

    def _convert_output(self, out):
        return pd.DataFrame({"metadata": out})


class Usage(Account):
    """
    Notes
    -----
    Dev note: the "type" (quota_type) parameter is listed as optional by IEX.
    However, it must be passed for the call to work. This reader will default
    the parameter's value to "messages" until this issue is resolved.
    """

    _TYPES = ("messages", "rules", "rule-records", "alerts", "alert-records")

    def __init__(self, quota_type=None, **kwargs):
        # defaulting to "messages" for now
        self.quota_type = quota_type or "messages"
        if quota_type not in self._TYPES:
            raise ValueError("Please enter a valid quota type")
        super(Usage, self).__init__(**kwargs)

    @property
    def endpoint(self):
        if self.quota_type is not None:
            return "usage/%s" % self.quota_type
        else:
            return "usage"


class PayAsYouGo(Account):
    def __init__(self, allow=None, **kwargs):
        self.allow = allow or False
        super(PayAsYouGo, self).__init__(**kwargs)

    @property
    def endpoint(self):
        return "payasyougo"

    @property
    def params(self):
        return {"allow": self.allow}
