import os
import pytest

from iexfinance.stocks import Stock


__all__ = [
    "block_keys",
    "set_keys",
    "stock_single",
    "stock_multiple",
    "stock_etf",
    "stock_special_char",
]


########################
# Environment Fixtures #
########################


@pytest.fixture
def block_keys(scope="function"):
    token = os.getenv("IEX_TOKEN")
    if token:
        del os.environ["IEX_TOKEN"]
        yield
        os.environ["IEX_TOKEN"] = token


@pytest.yield_fixture
def set_keys(scope="function"):
    token = os.getenv("IEX_TOKEN")
    os.environ["IEX_TOKEN"] = "TESTKEY"
    yield
    os.environ["IEX_TOKEN"] = token


###################
# Stocks fixtures #
###################


@pytest.fixture(scope="class")
def stock_single():
    return Stock("AAPL", pause=3)


@pytest.fixture(scope="class")
def stock_multiple():
    return Stock(["AAPL", "TSLA"], pause=3)


@pytest.fixture(scope="class")
def stock_etf():
    return Stock("SPY", pause=3)


@pytest.fixture(scope="class")
def stock_special_char():
    return Stock("GIG^", pause=3)
