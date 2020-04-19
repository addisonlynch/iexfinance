import pytest

from iexfinance.base import _IEXBase
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import IEXAuthenticationError


class TestAuth(object):
    def test_cloud_fails_no_token(self, block_keys):
        with pytest.raises(IEXAuthenticationError):
            _IEXBase()

    def test_token_env(self, set_keys):
        a = _IEXBase()

        assert a.token == "TESTKEY"

    def test_token_arg(self, set_keys):
        a = _IEXBase(token="TESTKEY2")

        assert a.token == "TESTKEY2"

    def test_stock_quote_fails_no_key(self, block_keys):
        with pytest.raises(IEXAuthenticationError):
            a = Stock("AAPL")
            a.get_quote()
