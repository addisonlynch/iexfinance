from iexfinance.altdata.base import CloudCrypto, SocialSentiment, CEOCompensation


def get_crypto_quote(symbol, **kwargs):
    """
    Crypto Quotes

    Single quote for Cryptocurrency supported by IEX Cloud.

    Reference: https://iexcloud.io/docs/api/#crypto
    Data Weighting: ``1`` per symbol

    Parameters
    ----------
    symbol: str
        A cryptocurrency symbol for retrieval

    Notes
    -----
    Each element contains Stocks ``quote`` fields.
    """
    return CloudCrypto(symbol, **kwargs).fetch()


def get_social_sentiment(symbol, period_type=None, date=None, **kwargs):
    """
    Social Sentiment

    .. warning:: This premium-only endpoint is not tested by
                 ``iexfinance`` and may be unstable.

    Social sentiment data from StockTwits. Data can be
    viewed as a daily value, or by minute for a given date.

    Reference: https://iexcloud.io/docs/api/#social-sentiment

    Data Weighting: ``30,000`` per symbol per sentiment record

    Parameters
    ----------
    symbol: str
        One valid symbol
    period_type: str, default ``daily``, optional
        ``daily`` or ``minute``. Translates to ``type`` parameter in IEX Cloud
        documentation
    date: str or datetime.datetime
        Date to retrieve
    """
    import warnings

    warnings.warn(
        "UNSTABLE ENDPOINT: This premium-only endpoint is not "
        "tested by iexfinance and may be unstable."
    )
    return SocialSentiment(symbol, period_type, date, **kwargs).fetch()


def get_ceo_compensation(symbol, **kwargs):
    """
    CEO Compensation

    This endpoint provides CEO compensation for a company by symbol

    Reference: https://iexcloud.io/docs/api/#ceo-compensation

    Data Weighting: ``20`` per symbol

    Parameters
    ----------
    symbol: str
        A single symbol for retrieval
    """
    return CEOCompensation(symbol, **kwargs).fetch()
