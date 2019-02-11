import pytest

from iexfinance.base import _IEXBase
from iexfinance.refdata import get_iex_listed_symbol_dir
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import (IEXAuthenticationError)


class TestAuth(object):

    def test_cloud_fails_no_token(self, use_cloud, block_keys):
        with pytest.raises(IEXAuthenticationError):
            _IEXBase()

    def test_token_env(self, use_cloud, set_keys):
        a = _IEXBase()

        assert a.token == "TESTKEY"

    def test_token_arg(self, use_cloud, set_keys):
        a = _IEXBase(token="TESTKEY2")

        assert a.token == "TESTKEY2"

    def test_stock_quote_fails_no_key(self, use_cloud, block_keys):
        with pytest.raises(IEXAuthenticationError):
            a = Stock("AAPL")
            a.get_quote()

    @pytest.mark.legacy
    def test_v1_requires_no_key(self, use_legacy):
        a = get_iex_listed_symbol_dir()

        assert isinstance(a, list)
        assert len(a) > 1
