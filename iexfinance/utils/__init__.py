import sys
import os
import simplejson as json
from iexfinance import IEXRetriever

_ALL_SYMBOLS_URL = "https://api.iextrading.com/1.0/ref-data/symbols"

def get_available_symbols():
    """
    Utility function to obtain all available symbols.
    """
    response = IEXRetriever._executeIEXQuery(_ALL_SYMBOLS_URL)
    if not response:
        raise ValueError("Could not download all symbols")
    else:
        return [d["symbol"] for d in response]