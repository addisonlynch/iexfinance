import os

import pytest

from iexfinance.tests.fixtures import *  # noqa: F403,F401


def pytest_sessionstart(session):
    iex_token = os.getenv("IEX_TOKEN")
    if not iex_token:
        pytest.exit(
            (
                "IEX_TOKEN not found. Please export a test 'IEX_TOKEN' in your"
                'environment to run pytests: export IEX_TOKEN="Tpk_..."'
            ),
            returncode=1,
        )
    if not iex_token.startswith(("Tpk", "Tsk")):
        pytest.exit(
            (
                "The IEX_TOKEN exported is not a test token. This should not be"
                "used for tests."
            ),
            returncode=1,
        )
