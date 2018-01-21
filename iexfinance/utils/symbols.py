from iexfinance import _IEXBase

_ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"

def get_available_symbols():
    """
    Utility function to obtain all available symbols.
    """
    response = _IEXBase._execute_iex_query(_ALL_SYMBOLS_URL)
    if not response:
        raise ValueError("Could not download all symbols")
    else:
        return [d["symbol"] for d in response]

