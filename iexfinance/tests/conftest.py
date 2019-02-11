import pytest

from iexfinance.tests.fixtures import *  # noqa: F403,F401
from iexfinance.utils.testing import using_cloud


def pytest_runtest_setup(item):
    # Skip all IEX cloud tests if cloud API version not selected
    cloud = [mark for mark in item.iter_markers(name='cloud')]
    if cloud:
        if using_cloud() is False:
            pytest.skip("IEX Cloud endpoint. Skipped when using v1")

    legacy = [mark for mark in item.iter_markers(name=('legacy'))]
    if legacy:
        if using_cloud() is True:
            pytest.skip("Legacy IEX Developer API 1.0 endpoint. Skipped "
                        "when using IEX Cloud.")
