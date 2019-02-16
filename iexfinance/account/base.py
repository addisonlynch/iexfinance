import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import cloud_endpoint


class Account(_IEXBase):

    @property
    def url(self):
        return "account/%s" % self.endpoint

    @property
    def endpoint(self):
        raise NotImplementedError

    @cloud_endpoint
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
    Dev note: the "type" (quota_type) parameter is listed as optional by IEX.
    However, it must be passed for the call to work. This reader will default
    the parameter's value to "messages" until this issue is resolved.
    """
    _TYPES = ["messages", "rules", "rule-records", "alerts", "alert-records"]

    def __init__(self, quota_type=None, **kwargs):
        if quota_type and quota_type not in self._TYPES:
            raise ValueError("Please enter a valid quota type")
        # defaulting to "messages" for now
        self.quota_type = quota_type or "messages"
        super(Usage, self).__init__(**kwargs)

    @property
    def endpoint(self):
        if self.quota_type is not None:
            return "usage/%s" % self.quota_type
        else:
            return "usage"


class PayAsYouGo(Account):

    def __init__(self, allow=False, **kwargs):
        self.allow = allow
        super(PayAsYouGo, self).__init__(**kwargs)

    @property
    def endpoint(self):
        return "payasyougo"

    @property
    def params(self):
        return {
            "allow": self.allow
        }
