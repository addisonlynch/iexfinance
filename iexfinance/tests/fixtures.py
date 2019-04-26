import os
import pytest

from iexfinance.stocks import Stock


__all__ = ["use_cloud", "use_legacy", "block_keys", "set_keys",
           "stock_single", "stock_multiple", "stock_etf", "stock_special_char"]


########################
# Environment Fixtures #
########################

@pytest.yield_fixture
def use_cloud(scope='function'):
    old = os.getenv("IEX_API_VERSION")
    os.environ["IEX_API_VERSION"] = 'iexcloud-sandbox'
    yield
    os.environ["IEX_API_VERSION"] = old


@pytest.yield_fixture
def use_legacy(scope='function'):
    old = os.getenv("IEX_API_VERSION")
    os.environ["IEX_API_VERSION"] = 'v1'
    yield
    os.environ["IEX_API_VERSION"] = old


@pytest.fixture
def block_keys(scope='function'):
    token = os.getenv("IEX_TOKEN")
    if token:
        del os.environ["IEX_TOKEN"]
        yield
        os.environ["IEX_TOKEN"] = token


@pytest.yield_fixture
def set_keys(scope='function'):
    token = os.getenv("IEX_TOKEN")
    os.environ["IEX_TOKEN"] = "TESTKEY"
    yield
    os.environ["IEX_TOKEN"] = token


###################
# Stocks fixtures #
###################

@pytest.fixture(scope='class')
def stock_single():
    return Stock("AAPL")


@pytest.fixture(scope='class')
def stock_multiple():
    return Stock(["AAPL", "TSLA"])


@pytest.fixture(scope='class')
def stock_etf():
    return Stock("SPY")


@pytest.fixture(scope='class')
def stock_special_char():
    return Stock("GIG^")
