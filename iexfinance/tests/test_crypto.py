import pandas as pd
import pytest

from iexfinance.crypto import get_crypto_book, get_crypto_price, get_crypto_quote
from iexfinance.crypto.base import Crypto
from iexfinance.utils.exceptions import IEXQueryError


class TestCryptoBase(object):
    def test_crypto_base_no_sym(self):
        with pytest.raises(TypeError):
            Crypto("quote")

    def test_crypto_base_multiple_syms(self):
        with pytest.raises(ValueError):
            Crypto("quote", ["BTCUSDT", "BAD"])

    def test_crypto_base_bad_sym(self):
        with pytest.raises(IEXQueryError):
            Crypto("quote", "BADSYMBOL").fetch()


class TestCrypto(object):
    def test_crypto_book(self):
        symbol = "BTCUSD"
        data = get_crypto_book(symbol)

        assert isinstance(data, dict)
        assert "bids" in data.keys()
        assert "asks" in data.keys()

    def test_crypto_price(self):
        symbol = "BTCUSD"
        data = get_crypto_price(symbol)

        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 2
        assert data.index[0] == symbol

    def test_crypto_quote(self):
        symbol = "BTCUSD"
        data = get_crypto_quote(symbol)

        assert isinstance(data, pd.DataFrame)
        assert len(data.columns) == 11
        assert data.index[0] == symbol
