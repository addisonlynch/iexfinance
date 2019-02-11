import os
import pytest


__all__ = ["use_cloud", "use_legacy", "block_keys", "set_keys"]


@pytest.fixture
def use_cloud(scope='function'):
    os.environ["IEX_API_VERSION"] = "iexcloud-beta"
    yield
    del os.environ["IEX_API_VERSION"]


@pytest.fixture
def use_legacy(scope='function'):
    os.environ["IEX_API_VERSION"] = 'v1'
    yield
    del os.environ["IEX_API_VERSION"]


@pytest.fixture
def block_keys(scope='function'):
    if os.getenv("IEX_TOKEN"):
        del os.environ["IEX_TOKEN"]


@pytest.fixture
def set_keys(scope='function'):
    os.environ["IEX_TOKEN"] = "TESTKEY"
    yield
    del os.environ["IEX_TOKEN"]
