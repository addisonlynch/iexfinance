import os
import pytest

from iexfinance.base import _IEXBase


@pytest.fixture
def block_format_env():
    if os.getenv("IEX_OUTPUT_FORMAT"):
        del os.environ["IEX_OUTPUT_FORMAT"]


class TestBase(object):

    def test_all_defaults(self, block_format_env):
        base = _IEXBase()

        assert base.output_format == 'json'
        assert base.pause == 0.5
        assert base.token is None

    def test_output_format_passed(self):
        base = _IEXBase(output_format='pandas')

        assert base.output_format == 'pandas'

    def test_output_format_env(self):
        os.environ["IEX_OUTPUT_FORMAT"] = 'pandas'
        base = _IEXBase()

        assert base.output_format == 'pandas'

    def test_invalid_output_format(self):
        with pytest.raises(ValueError):
            _IEXBase(output_format='BADFORMAT')

    def test_invalid_format_env(self):
        os.environ["IEX_OUTPUT_FORMAT"] = "BADFORMAT"
        with pytest.raises(ValueError):
            _IEXBase()
