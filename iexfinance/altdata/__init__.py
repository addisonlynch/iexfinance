from iexfinance.altdata.base import CloudCrypto, SocialSentiment


def get_crypto_quote(symbol, **kwargs):
    """
    Crypto Quotes

    This will return a quote for Cryptocurrencies supported by IEX Cloud.
    Each element is a standard ``quote``.

    Reference: https://iexcloud.io/docs/api/#crypto
    Data Weighting: ``1`` per symbol

    Parameters
    ----------
    symbol: str
        A cryptocurrency symbol for retrieval
    """
    return CloudCrypto(symbol, **kwargs).fetch()


def get_social_sentiment(symbol, period_type=None, date=None, **kwargs):
    """
    Social Sentiment

    .. warning:: Unstable endpoint. May return unexpected results.

    This endpoint provides social sentiment data from StockTwits. Data can be
    viewed as a daily value, or by minute for a given date.

    Reference: https://iexcloud.io/docs/api/#social-sentiment

    Data Weighting: ``100`` per date for ``daily``, ``200`` per symbol for
    ``minute``

    Parameters
    ----------
    symbol: str
        A single symbol for retrieval
    period_type: str, default ``daily``, optional
        Can only be ``daily`` or ``minute``. Translates to the "type" path
        parameter in the IEX Cloud documentation
    date: str or datetime.datetime
        Specify date to obtain sentiment data
    """
    import warnings
    warnings.warn("UNSTABLE ENDPOINT: Not yet fully implemented by the "
                  "provider.")
    return SocialSentiment(symbol, period_type, date, **kwargs).fetch()
