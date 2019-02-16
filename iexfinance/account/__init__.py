from iexfinance.account.base import Usage, Metadata, PayAsYouGo


def get_metadata(**kwargs):
    """Metadata

    Get account metadata

    Reference: https://iexcloud.io/docs/api/#metadata

    Data Weighting: ``Free``

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return Metadata(**kwargs).fetch()


def get_usage(quota_type=None, **kwargs):
    """Usage

    Used to retrieve account details such as current tier, payment status,
    message quote usage, etc

    Reference: https://iexcloud.io/docs/api/#usage

    Data Weighting: ``Free``

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.

    Parameters
    ----------
    quota_type: str, default "messages", optional
        Used to specify quota to return Ex. ``messages``, ``rules``,
        ``rule-records``, ``alerts``, ``alert-records``
    """
    return Usage(quota_type=quota_type, **kwargs).fetch()


def allow_pay_as_you_go(**kwargs):
    """Allow Pay As You Go

    Set pay as you go account settings to ``allow=True``

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    Data Weighting: ``Free``

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return PayAsYouGo(allow=True, **kwargs).fetch()


def disallow_pay_as_you_go(**kwargs):
    """Disallow Pay As You Go

    Set pay as you go account settings to ``allow=False``

    Data Weighting: ``Free``

    Reference: https://iexcloud.io/docs/api/#pay-as-you-go

    .. warning:: This endpoint is only available using IEX Cloud. See
                 :ref:`Migrating` for more information.
    """
    return PayAsYouGo(**kwargs).fetch()
