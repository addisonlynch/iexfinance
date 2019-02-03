import pandas as pd

from iexfinance.base import _IEXBase
from iexfinance.utils import cloud_endpoint

__all__ = ["get_usage", "get_metadata", "allow_pay_as_you_go",
           "disallow_pay_as_you_go"]


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


def get_usage(quota_type=None, **kwargs):
    """
    Get account usage statistics.

    Reference: https://iexcloud.io/docs/api/#usage

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

    Parameters
    ----------
    quota_type: str, default "messages", optional
        Used to specify quota to return Ex. ``messages``, ``rules``,
        ``rule-records``, ``alerts``, ``alert-records``
    """
    return Usage(quota_type=quota_type, **kwargs).fetch()


def get_metadata(**kwargs):
    """
    Get account metadata

    Reference: https://iexcloud.io/docs/api/#metadata

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return Metadata(**kwargs).fetch()


def allow_pay_as_you_go(**kwargs):
    """
    Set pay as you go account settings to ``allow=True``

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return PayAsYouGo(allow=True, **kwargs).fetch()


def disallow_pay_as_you_go(**kwargs):
    """
    Set pay as you go account settings to ``allow=False``

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return PayAsYouGo(**kwargs).fetch()
