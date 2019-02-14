from iexfinance.account.base import Usage, Metadata, PayAsYouGo


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
