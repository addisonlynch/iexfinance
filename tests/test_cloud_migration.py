import os
import pytest


from iexfinance.base import _IEXBase
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import (IEXAuthenticationError,
                                         IEXVersionError)


@pytest.fixture
def use_cloud(scope='function'):
    os.environ["IEX_API_VERSION"] = "iexcloud-beta"


@pytest.fixture
def use_legacy(scope='function'):
    os.environ["IEX_API_VERSION"] = 'v1'


@pytest.fixture
def block_keys(scope='function'):
    if os.getenv("IEX_API_KEY"):
        del os.environ["IEX_API_KEY"]


@pytest.fixture
def set_keys(scope='function'):
    os.environ["IEX_API_KEY"] = "TESTKEY"


class TestCloudMigration(object):

    def test_fails_api_key(self, use_cloud, block_keys):
        with pytest.raises(IEXAuthenticationError):
            _IEXBase()

    def test_api_key_env(self, use_cloud, set_keys):
        a = _IEXBase()

        assert a.api_key == "TESTKEY"

    def test_api_key_arg(self, use_cloud, set_keys):
        a = _IEXBase(token="TESTKEY2")

        assert a.api_key == "TESTKEY2"

    def test_cloud_endpoint_decorator(self, use_legacy):
        a = Stock("AAPL")

        with pytest.raises(IEXVersionError):
            a.get_balance_sheet()
