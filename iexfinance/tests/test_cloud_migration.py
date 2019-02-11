import pytest

from iexfinance.refdata import get_iex_listed_symbol_dir
from iexfinance.stocks import Stock
from iexfinance.utils.exceptions import (IEXVersionError)


class TestCloudMigration(object):

    def test_cloud_endpoint_decorator(self, use_legacy):
        a = Stock("AAPL", output_format='pandas')

        with pytest.raises(IEXVersionError):
            a.get_balance_sheet()

    def test_legacy_endpoint_decorator(self, use_cloud, set_keys):
        with pytest.raises(IEXVersionError):
            get_iex_listed_symbol_dir(output_format='pandas')
