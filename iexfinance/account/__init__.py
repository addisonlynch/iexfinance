from iexfinance.account.base import Metadata, PayAsYouGo, Usage


def get_metadata(**kwargs):
    """
    Metadata

    Account metadata

    Reference: https://iexcloud.io/docs/api/#metadata

    Data Weighting: ``Free``
    """
    return Metadata(**kwargs).fetch()


def get_usage(quota_type=None, **kwargs):
    """
    Usage

    Account details, including current tier, payment status,
    message quote usage

    Reference: https://iexcloud.io/docs/api/#usage

    Data Weighting: ``Free``

    Parameters
    ----------
    quota_type: str, default "messages", optional
        Quotat category (``messages``, ``rules``,
        ``rule-records``, ``alerts``, ``alert-records``)
    """
    return Usage(quota_type=quota_type, **kwargs).fetch()


def allow_pay_as_you_go(**kwargs):
    """
    Allow Pay As You Go

    Toggle ON pay-as-you-go messages

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    Data Weighting: ``Free``
    """
    return PayAsYouGo(allow=True, **kwargs).fetch()


def disallow_pay_as_you_go(**kwargs):
    """
    Disallow Pay As You Go

    Toggle OFF pay-as-you-go messages

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    Data Weighting: ``Free``
    """
    return PayAsYouGo(**kwargs).fetch()
