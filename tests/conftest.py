import pytest

from iexfinance.utils.testing import using_cloud


def pytest_runtest_setup(item):
    # Skip all IEX cloud tests if cloud API version not selected
    cloud = [mark for mark in item.iter_markers(name='cloud')]
    if cloud:
        if using_cloud() is False:
            pytest.skip("IEX Cloud endpoint. Skipping when using v1")
