from iexfinance.crypto.base import Crypto


def get_crypto_book(symbol, **kwargs):
    """
    Cryptocurrency Book

    This returns a current snapshot of the book for a specified cryptocurrency.

    .. note:: pandas ``DataFrame`` output formatting is not supported for this
              endpoint.

    Reference: https://iexcloud.io/docs/api/#cryptocurrency-book

    Data Weighting: ``10`` per symbol per update

    Parameters
    ----------
    symbol: str
        A cryptocurrency symbol for retrieval
    """
    return Crypto("book", symbol, **kwargs).fetch()


def get_crypto_price(symbol, **kwargs):
    """
    Cryptocurrency Price

    This returns the price for a specified cryptocurrency.

    Reference: https://iexcloud.io/docs/api/#cryptocurrency-price

    Data Weighting: ``1``

    Parameters
    ----------
    symbol: str
        A cryptocurrency symbol for retrieval
    """
    return Crypto("price", symbol, **kwargs).fetch()


def get_crypto_quote(symbol, **kwargs):
    """
    Cryptocurrency Quote

    Single quote for Cryptocurrency supported by IEX Cloud.

    Reference: https://iexcloud.io/docs/api/#cryptocurrency-quote

    Data Weighting: ``2`` per symbol

    Parameters
    ----------
    symbol: str
        A cryptocurrency symbol for retrieval

    Notes
    -----
    Each element contains Stocks ``quote`` fields.
    """
    return Crypto("quote", symbol, **kwargs).fetch()
